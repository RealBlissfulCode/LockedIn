# -*- coding: utf-8 -*-
"""Cross-device sync.

The server holds one JSON document and a version number. Every device pulls on
open, on focus, and on a slow timer, and pushes a debounced copy after a change.
If the version moved underneath us the push comes back 409 with the server's
copy, and the two are merged rather than one overwriting the other.

The merge is per branch, not per document. Each top-level part of the state
carries the time it last actually changed, so editing the budget on a laptop and
the shopping list on a phone keeps both. `days` is merged one date at a time,
because the calendar is the part two people are most likely to touch at once.

What it does not do is merge two edits to the same branch in the same moment.
The newer one wins and the older is lost. Doing better needs per-field history,
which is a lot of machinery for two people who are rarely in the same list at
the same second.

`who` and `theme` are deliberately NOT synced. Whose day is on screen and
whether it is dark are properties of the device, not of the shared plan.
"""

APP_SYNC = r"""
/* ============================ sync ============================ */
var SYNC_URL='api/sync.php';
/* Everything shared. `days` is absent on purpose: it merges per date below. */
var BRANCHES=['prof','ingOv','fav','lists','mine','photos','shop','fin','plan',
              'sched','exLog','seeded','seeded6'];
var LOCAL_ONLY=['who','theme','__v'];

var syncTok=null, syncOn=false, syncState='off', syncAt=null, syncMsg='';
var syncTimer=null, syncPending=false, syncBusy=false, syncFails=0;
var _snap={}, _snapDays={};

function syncSet(st,msg){
  syncState=st; syncMsg=msg||'';
  var e=document.getElementById('syncPill');
  if(e) e.outerHTML=syncPill();
}
/* Small readout in the header, so it is obvious whether the thing is actually
   saving anywhere or just sitting in this browser. */
function syncPill(){
  var label={off:'Local only',idle:'Synced',pull:'Checking',push:'Saving',
    offline:'Offline',error:'Sync error'}[syncState]||syncState;
  var cls={idle:'ok',push:'busy',pull:'busy',offline:'warn',error:'bad',off:'off'}[syncState]||'';
  var title=syncMsg||(syncAt?('Last synced '+new Date(syncAt).toLocaleTimeString()):'');
  return '<button class="syncpill '+cls+'" id="syncPill" title="'+E(title)+'">'+
    '<i></i><span>'+E(label)+'</span></button>';
}

function stripLocal(o){
  var c={}; for(var k in o) if(LOCAL_ONLY.indexOf(k)<0) c[k]=o[k];
  return c;
}
/* Stamp only what genuinely changed. Called from save(), so no call site has to
   remember to say which part it touched. */
function syncTouch(){
  var now=Date.now(), first=!_snap.__init;
  S.__t=S.__t||{}; S.__td=S.__td||{};
  BRANCHES.forEach(function(b){
    var s=JSON.stringify(S[b]===undefined?null:S[b]);
    if(!first&&_snap[b]!==s) S.__t[b]=now;
    _snap[b]=s;
  });
  var days=S.days||{};
  for(var d in days){
    var sd=JSON.stringify(days[d]);
    if(!first&&_snapDays[d]!==sd) S.__td[d]=now;
    _snapDays[d]=sd;
  }
  _snap.__init=1;
}
/* Anything that swaps S wholesale (a pull, a merge, a restored file) has to
   re-baseline, or the next save diffs against the old document and stamps
   branches nobody touched. A spurious stamp is not cosmetic: it makes this
   device look like the newer author of a branch it never edited, and the next
   merge would hand its stale copy to the other device. */
function syncRebase(){
  _snap={}; _snapDays={};
  BRANCHES.forEach(function(b){ _snap[b]=JSON.stringify(S[b]===undefined?null:S[b]); });
  var days=S.days||{};
  for(var d in days) _snapDays[d]=JSON.stringify(days[d]);
  _snap.__init=1;
}
/* A restored file is a deliberate wholesale change, so it does claim every
   branch. Without this it would sync nowhere. */
function syncClaimAll(){
  var now=Date.now();
  S.__t=S.__t||{}; S.__td=S.__td||{};
  BRANCHES.forEach(function(b){ S.__t[b]=now; });
  for(var d in (S.days||{})) S.__td[d]=now;
  syncRebase();
}

function syncMerge(local,remote){
  if(!remote||typeof remote!=='object') return local;
  var out=JSON.parse(JSON.stringify(local));
  var lt=local.__t||{}, rt=remote.__t||{};
  out.__t=out.__t||{};
  BRANCHES.forEach(function(b){
    var l=lt[b]||0, r=rt[b]||0;
    if(r>l&&remote[b]!==undefined){ out[b]=remote[b]; out.__t[b]=r; }
  });
  var ld=local.__td||{}, rd=remote.__td||{};
  var days={}, seen={};
  out.__td=out.__td||{};
  [local.days||{},remote.days||{}].forEach(function(src){
    for(var d in src) seen[d]=1;
  });
  for(var d in seen){
    var l=ld[d]||0, r=rd[d]||0;
    var pick=(r>l&&remote.days&&remote.days[d]!==undefined)?remote.days[d]
            :((local.days&&local.days[d]!==undefined)?local.days[d]:(remote.days||{})[d]);
    days[d]=pick;
    out.__td[d]=Math.max(l,r);
  }
  out.days=days;
  return out;
}

/* A device that has never synced adopts the server copy whole. Merging a
   freshly seeded state against a real one would fight over every branch. */
function syncAdopt(remote){
  var keep={}; LOCAL_ONLY.forEach(function(k){ keep[k]=S[k]; });
  S=JSON.parse(JSON.stringify(remote));
  for(var k in keep) if(keep[k]!==undefined) S[k]=keep[k];
  var d=DEF(); for(var f in d) if(!(f in S)) S[f]=d[f];
  for(var g in d.fin) if(!(g in S.fin)) S.fin[g]=d.fin[g];
}

function syncReq(method,body,cb){
  var x=new XMLHttpRequest();
  x.open(method,SYNC_URL,true);
  x.setRequestHeader('X-Handbook-Token',syncTok);
  if(body) x.setRequestHeader('Content-Type','application/json');
  x.timeout=20000;
  x.onload=function(){
    var j=null;
    try{ j=JSON.parse(x.responseText); }catch(e){}
    /* No PHP on the host means the rewrite hands back index.html. That is not
       an error to retry, it is a host that cannot sync. */
    if(j===null){ cb('nosync',null,x.status); return; }
    cb(null,j,x.status);
  };
  x.ontimeout=function(){cb('offline',null,0);};
  x.onerror=function(){cb('offline',null,0);};
  x.send(body?JSON.stringify(body):null);
}

function syncPull(after){
  if(!syncOn||syncBusy) { after&&after(); return; }
  syncBusy=true; syncSet('pull');
  syncReq('GET',null,function(err,j,code){
    syncBusy=false;
    if(err==='nosync'){ syncOn=false; syncSet('off','This host is not running the sync endpoint.'); after&&after(); return; }
    if(err){ syncFails++; syncSet('offline','Could not reach the server. Changes are safe on this device.'); after&&after(); return; }
    if(code===401){ syncOn=false; syncSet('error','The server rejected the code.'); after&&after(); return; }
    if(code!==200){ syncSet('error','Server said '+code); after&&after(); return; }
    syncFails=0;
    var sv=j.version||0;
    if(sv>0&&j.state){
      if(!S.__v){ syncAdopt(j.state); syncRebase(); }
      else if(sv!==S.__v){ S=syncMerge(S,j.state); syncRebase(); }
    }
    S.__v=sv; syncAt=Date.now();
    try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
    syncSet('idle');
    /* Do not yank the page out from under an open editor. chrome() has to run
       too: the header holds the profile names and the theme, and route() only
       ever touches #view. Without it a name changed on another device stayed
       stale up there until a full reload. */
    if(sv>0&&!document.querySelector('.mask')){
      try{applyTheme();}catch(e){}
      try{chrome();}catch(e){}
      try{route();}catch(e){}
    }
    after&&after();
  });
}

function syncPush(){
  if(!syncOn||!syncTok) return;
  if(syncBusy){ syncPending=true; return; }
  syncBusy=true; syncSet('push');
  syncReq('POST',{baseVersion:S.__v||0,state:stripLocal(S)},function(err,j,code){
    syncBusy=false;
    if(err==='nosync'){ syncOn=false; syncSet('off','This host is not running the sync endpoint.'); return; }
    if(err){ syncFails++; syncSet('offline','Not saved to the server yet. It will retry.'); syncPending=true; return; }
    if(code===409){
      /* Someone else wrote first. Merge onto theirs and try again. */
      S=syncMerge(S,j.state); S.__v=j.version||0; syncRebase();
      try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
      syncPending=true; syncSet('push','Merging a change from the other device');
      setTimeout(syncFlush,120);
      return;
    }
    if(code===401){ syncOn=false; syncSet('error','The server rejected the code.'); return; }
    if(code!==200){ syncSet('error','Server said '+code); return; }
    syncFails=0; S.__v=j.version||0; syncAt=Date.now();
    try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
    syncSet('idle');
    if(syncPending){ syncPending=false; setTimeout(syncFlush,80); }
  });
}
function syncFlush(){ clearTimeout(syncTimer); syncTimer=null; syncPush(); }
/* Debounced, so dragging a slider does not mean a hundred writes. */
function syncSchedule(){
  if(!syncOn) return;
  clearTimeout(syncTimer);
  syncTimer=setTimeout(syncFlush,1400);
}

function syncInit(token){
  syncTok=token; syncOn=true; syncSet('pull');
  syncPull(function(){
    /* Anything typed before the first pull landed still needs to go up. */
    if(S.__v===0||S.__v===undefined) syncSchedule();
  });
  setInterval(function(){ if(!document.hidden) syncPull(); },25000);
  document.addEventListener('visibilitychange',function(){ if(!document.hidden) syncPull(); });
  window.addEventListener('online',function(){ syncPull(); syncSchedule(); });
  window.addEventListener('focus',function(){ syncPull(); });
  /* Best effort on the way out, so closing a tab does not lose the last edit. */
  window.addEventListener('pagehide',function(){
    if(!syncTimer||!syncOn) return;
    try{
      var b=new Blob([JSON.stringify({baseVersion:S.__v||0,state:stripLocal(S)})],
        {type:'application/json'});
      navigator.sendBeacon&&navigator.sendBeacon(SYNC_URL+'?t='+encodeURIComponent(syncTok),b);
    }catch(e){}
  });
}
"""
