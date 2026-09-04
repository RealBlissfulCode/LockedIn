# -*- coding: utf-8 -*-
"""Pulling and pushing the account's state.

The old sync layer merged one shared JSON document per branch and used a token
derived from the passcode. This replaces it. There are now two documents: the
household's, which everyone in it reads and writes, and your own private one,
which the server will not hand to anybody else.

Writes are optimistic. Send the version you last read, and if somebody else got
there first the server sends back what is actually there so we can merge per
branch rather than one phone silently winning.
"""

APP_STATE = r"""
/* ============================ state sync ============================ */
/* Shared across the household. `days` is absent on purpose, it merges one date
   at a time below because the calendar is what two people touch at once. */
var BRANCHES=['members','household','ingOv','fav','lists','mine','photos','shop','fin','plan',
              'sched','exLog','prefs','onboarded'];
/* Never leaves this device. Which member is selected and whether it is dark are
   properties of the phone in your hand, not of the plan. */
var LOCAL_ONLY=['who','theme','__v','__t','__td'];
/* Lives in the private document, so nobody else in the household ever receives
   it. This is what makes hiding a surprise actually hidden. */
var PRIVATE=['secret'];

var docVer=0, privVer=0;
var syncState='off', syncAt=null, syncMsg='', syncTimer=null;
var syncPending=false, syncBusy=false, syncFails=0;
var _snap={}, _snapDays={};

function syncSet(st,msg){
  syncState=st; syncMsg=msg||'';
  var e=document.getElementById('syncPill');
  if(e) e.outerHTML=syncPill();
}
function syncPill(){
  var label={off:'Offline',idle:'Saved',pull:'Checking',push:'Saving',
    offline:'Offline',error:'Not saving'}[syncState]||syncState;
  var cls={idle:'ok',push:'busy',pull:'busy',offline:'warn',error:'bad',off:'off'}[syncState]||'';
  var title=syncMsg||(syncAt?('Last saved '+new Date(syncAt).toLocaleTimeString()):'');
  return '<button class="syncpill '+cls+'" id="syncPill" title="'+E(title)+'">'+
    '<i></i><span>'+E(label)+'</span></button>';
}

function stripLocal(o){
  var c={}; for(var k in o) if(LOCAL_ONLY.indexOf(k)<0&&PRIVATE.indexOf(k)<0) c[k]=o[k];
  return c;
}
function privatePart(){
  var c={}; PRIVATE.forEach(function(k){ if(S[k]!==undefined) c[k]=S[k]; });
  return c;
}

/* Stamp only what actually changed, so a phone that touched the shopping list
   does not claim to be the newer author of the budget as well. */
function syncTouch(){
  var nowT=Date.now(), first=!_snap.__init;
  S.__t=S.__t||{}; S.__td=S.__td||{};
  BRANCHES.forEach(function(b){
    var cur=JSON.stringify(S[b]===undefined?null:S[b]);
    if(first){ _snap[b]=cur; if(!S.__t[b]) S.__t[b]=nowT; return; }
    if(_snap[b]!==cur){ _snap[b]=cur; S.__t[b]=nowT; }
  });
  var days=S.days||{};
  Object.keys(days).forEach(function(d){
    var cur=JSON.stringify(days[d]);
    if(first){ _snapDays[d]=cur; if(!S.__td[d]) S.__td[d]=nowT; return; }
    if(_snapDays[d]!==cur){ _snapDays[d]=cur; S.__td[d]=nowT; }
  });
  _snap.__init=true;
  if(!first) queuePush();
}

/* Branch by branch, newest stamp wins. Days are merged one date at a time. */
function mergeIn(remote){
  if(!remote||typeof remote!=='object') return false;
  var rt=remote.__t||{}, rd=remote.__td||{}, changed=false;
  S.__t=S.__t||{}; S.__td=S.__td||{};
  BRANCHES.forEach(function(b){
    if(!(b in remote)) return;
    if((rt[b]||0)>(S.__t[b]||0)){ S[b]=remote[b]; S.__t[b]=rt[b]; changed=true; }
  });
  var rdays=remote.days||{};
  S.days=S.days||{};
  Object.keys(rdays).forEach(function(d){
    if((rd[d]||0)>(S.__td[d]||0)){ S.days[d]=rdays[d]; S.__td[d]=rd[d]; changed=true; }
  });
  return changed;
}

function pullState(){
  syncSet('pull');
  return api('doc.php?do=all').then(function(r){
    if(!r.ok){
      syncSet(r.__status===401?'off':'error', r.error||'');
      return;
    }
    docVer=r.shared.version||0;
    privVer=r.private.version||0;
    var changed=false;
    if(r.shared.body) changed=mergeIn(r.shared.body)||changed;
    if(r.private.body){ PRIVATE.forEach(function(k){
      if(r.private.body[k]!==undefined) S[k]=r.private.body[k]; }); }
    syncAt=Date.now();
    syncSet('idle');
    /* Take a snapshot without stamping, otherwise arriving data looks like a
       local edit and gets pushed straight back. */
    _snap={}; _snapDays={}; syncTouch();
    if(changed) try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
  }).catch(function(){ syncSet('offline'); });
}

function queuePush(){
  if(syncState==='off') return;
  syncPending=true;
  if(syncTimer) clearTimeout(syncTimer);
  syncTimer=setTimeout(pushState,1200);
}

function pushState(){
  if(syncBusy||!syncPending||syncState==='off') return;
  syncBusy=true; syncPending=false;
  syncSet('push');
  var payload=stripLocal(S);
  payload.days=S.days; payload.__t=S.__t; payload.__td=S.__td;
  api('doc.php?scope=shared',{body:{version:docVer,body:payload}}).then(function(r){
    if(r.ok){
      docVer=r.version; syncAt=Date.now(); syncFails=0; syncSet('idle');
      return pushPrivate();
    }
    if(r.__status===409){
      /* Somebody else wrote while we were typing. Merge theirs in, take their
         version, and try once more on the next tick. */
      docVer=r.version||docVer;
      if(mergeIn(r.body)){ try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){} }
      syncPending=true; syncSet('idle');
      setTimeout(function(){ syncBusy=false; pushState(); },400);
      return 'retry';
    }
    if(r.__status===401){ syncSet('off','Signed out'); return; }
    syncFails++;
    syncSet(syncFails>2?'error':'offline', r.error||'');
  }).catch(function(){
    syncFails++; syncSet('offline');
  }).then(function(res){
    if(res!=='retry') syncBusy=false;
  });
}

function pushPrivate(){
  var mine=privatePart();
  if(!Object.keys(mine).length) return;
  return api('doc.php?scope=private:'+(ACCOUNT?ACCOUNT.id:0),
             {body:{version:privVer,body:mine}}).then(function(r){
    if(r.ok) privVer=r.version;
    else if(r.__status===409) privVer=r.version||privVer;
  });
}

function syncStart(){
  syncSet('idle');
  window.addEventListener('focus',function(){ if(!syncBusy) pullState(); });
  window.addEventListener('online',function(){ pullState(); });
  setInterval(function(){ if(!syncBusy&&!syncPending) pullState(); },90000);
  /* A tab closing mid-edit should still land. */
  window.addEventListener('pagehide',function(){
    if(syncPending&&!syncBusy){ if(syncTimer) clearTimeout(syncTimer); pushState(); }
  });
}
"""
