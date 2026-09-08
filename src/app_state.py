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
/* __migrated is a note this device leaves itself for one load. It must never
   reach the account: it used to, and then every device that pulled the account
   picked it up, decided on its next load that it had personally edited the
   whole financial section, refused the account's copy, and pushed its own back.
   Two devices did that to each other forever. */
var LOCAL_ONLY=['who','theme','__v','__t','__td','__migrated'];
/* Lives in the private document, so nobody else in the household ever receives
   it. This is what makes hiding a surprise actually hidden. */
var PRIVATE=['secret'];

var docVer=0, privVer=0;
var syncState='off', syncAt=null, syncMsg='', syncTimer=null;
var syncPending=false, syncBusy=false, syncFails=0;
var _snap={}, _snapDays={};
/* The branch version numbers this device has seen, straight from the server.
   Higher on the server than in here means somebody else changed that branch
   after the last time we looked. See branch_versions in api/lib/store.php. */
var baseBv={}, baseDv={};
var forceNext=false;

/* Seconds on a "last saved" stamp are noise, and they push the time onto two
   lines in a narrow tile. */
function clockTime(t){
  try{ return new Date(t).toLocaleTimeString([],{hour:'numeric',minute:'2-digit'}); }
  catch(e){ return new Date(t).toLocaleTimeString(); }
}
function syncSet(st,msg){
  syncState=st; syncMsg=msg||'';
  var e=document.getElementById('syncPill');
  if(e) e.outerHTML=syncPill();
}
function syncPill(){
  var label={off:'Offline',idle:'Saved',pull:'Checking',push:'Saving',
    offline:'Offline',error:'Not saving'}[syncState]||syncState;
  var cls={idle:'ok',push:'busy',pull:'busy',offline:'warn',error:'bad',off:'off'}[syncState]||'';
  var title=syncMsg||(syncAt?('Last saved '+clockTime(syncAt)):'');
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

/* The pieces the document is merged in, matching doc_units in api/lib/store.php.
 *
 * A whole branch is too coarse. fin holds the cost lines, the income lines, the
 * purchase lists and the scenarios, so merging fin as one unit means two people
 * touching anything financial at the same moment costs one of them everything
 * they just did. Anything shaped like a map splits one level down, so a cost
 * rename on a phone and a new list on a laptop both survive. Arrays stay whole,
 * because half an array is not something anybody wants merged. */
var USEP='\u0001';
function isMap(v){ return v&&typeof v==='object'&&!Array.isArray(v); }
function unitsOf(o){
  var out={};
  BRANCHES.forEach(function(b){
    var v=o?o[b]:undefined;
    if(isMap(v)){ for(var k in v) out[b+USEP+k]=1; }
    else out[b]=1;
  });
  return out;
}
function unitGet(o,u){
  if(!o) return undefined;
  var i=u.indexOf(USEP);
  if(i<0) return o[u];
  var a=u.slice(0,i), b=u.slice(i+1);
  return isMap(o[a])?o[a][b]:undefined;
}
function unitSet(o,u,val){
  var i=u.indexOf(USEP);
  if(i<0){ if(val===undefined) delete o[u]; else o[u]=val; return; }
  var a=u.slice(0,i), b=u.slice(i+1);
  if(!isMap(o[a])) o[a]={};
  if(val===undefined) delete o[a][b]; else o[a][b]=val;
}
function allUnits(remote){
  var u=unitsOf(S);
  if(remote){ var r=unitsOf(remote); for(var k in r) u[k]=1; }
  return Object.keys(u);
}

/* What this device has changed since it last agreed with the server. _snap is
   that agreement: every pull and every successful push resets it. A unit whose
   JSON no longer matches its snapshot is one you edited, and an edit in front
   of you always beats an older copy coming down the wire. */
function dirtyBranch(u){
  return _snap[u]!==JSON.stringify(unitGet(S,u)===undefined?null:unitGet(S,u));
}
function snapOne(u){
  _snap[u]=JSON.stringify(unitGet(S,u)===undefined?null:unitGet(S,u));
}
/* A blank day is not data.
 *
 * Opening any page that shows today creates today's empty log as a side effect
 * of drawing it. That is fine on its own, but it used to count as an edit, so
 * the app sent the whole document up to record that nothing had happened, and
 * the next render made a new empty one, and it went round about twice a second
 * for as long as the tab stayed open. A day with no meals, no shifts, no
 * spending, no note and no weight has nothing in it to sync. */
function dayIsEmpty(v){
  if(!v||typeof v!=='object') return true;
  return !(v.meals&&v.meals.length)&&!(v.sched&&v.sched.length)&&!(v.spend&&v.spend.length)
    &&!v.notes&&v.w==null&&(!v.workout||v.workout==='rest');
}
function dirtyDay(d){
  var cur=(S.days||{})[d];
  /* Never seen by the server and nothing in it: there is nothing to say. */
  if(_snapDays[d]===undefined&&dayIsEmpty(cur)) return false;
  return _snapDays[d]!==JSON.stringify(cur);
}
function anyDirty(){
  if(!_snap.__init) return false;
  var n=false;
  allUnits().forEach(function(u){ if(dirtyBranch(u)) n=true; });
  Object.keys(S.days||{}).forEach(function(d){ if(dirtyDay(d)) n=true; });
  return n;
}
/* Reset the agreement to whatever is in S right now. Called after a pull and
   after a push, because both mean the server and this device match again. */
function syncSnap(){
  _snap={}; _snapDays={};
  allUnits().forEach(snapOne);
  var days=S.days||{};
  Object.keys(days).forEach(function(d){ _snapDays[d]=JSON.stringify(days[d]); });
  _snap.__init=true;
}
/* Called after anything writes to S. Work out whether that actually changed
   something and queue a save if it did. */
function syncTouch(){
  if(!_snap.__init){ syncSnap(); return; }
  if(anyDirty()) queuePush();
}

/* Branch by branch, using the version numbers the server put on them.
 *
 * Take the server's copy of a branch when its number is higher than the one we
 * hold and we have not touched that branch ourselves. If we have touched it,
 * ours stays and goes up on the next push, so typing into the schedule is never
 * undone by a refresh landing on top of it. Two people editing different things
 * both keep their work, because the decision is made per branch and per day
 * rather than over the whole document. */
function mergeIn(remote,ver){
  if(!remote||typeof remote!=='object') return false;
  var rb=remote.__bv||{}, rd=remote.__dv||{}, changed=false;
  /* A document written before the server started numbering branches has no
     numbers on it. Read the whole thing as being at the document's own version,
     which is true and gets the first pull after an update to work. */
  var fb=ver||0;
  allUnits(remote).forEach(function(u){
    var rv=rb[u]!==undefined?rb[u]:fb;
    if(rv<=(baseBv[u]||0)) return;      /* nothing new over there */
    if(dirtyBranch(u)) return;          /* being edited here, ours wins */
    var rvVal=unitGet(remote,u);
    if(rvVal===undefined&&rb[u]===undefined) return;  /* not carried, not a delete */
    unitSet(S,u,rvVal); snapOne(u); baseBv[u]=rv; changed=true;
  });
  var rdays=remote.days||{};
  S.days=S.days||{};
  Object.keys(rdays).forEach(function(d){
    var rv=rd[d]!==undefined?rd[d]:fb;
    if(rv<=(baseDv[d]||0)) return;
    if(dirtyDay(d)) return;
    /* Snapshot it as we take it, the same as a branch. Without this a day that
       arrived from the account had no snapshot to compare against, so it read
       as edited here forever, and the device sent the whole document up every
       few seconds for the rest of the session. */
    S.days[d]=rdays[d]; _snapDays[d]=JSON.stringify(S.days[d]);
    baseDv[d]=rv; changed=true;
  });
  return changed;
}
/* Everything we did not take, we still record as seen, so a branch we are
   editing does not keep looking new every time we ask. */
function seenBv(remote,ver){
  var rb=(remote&&remote.__bv)||{}, rd=(remote&&remote.__dv)||{}, fb=ver||0, d;
  allUnits(remote).forEach(function(u){
    var rv=rb[u]!==undefined?rb[u]:fb;
    if(rv>(baseBv[u]||0)&&!dirtyBranch(u)) baseBv[u]=rv;
  });
  for(d in ((remote&&remote.days)||{})){
    var dv=rd[d]!==undefined?rd[d]:fb;
    if(dv>(baseDv[d]||0)&&!dirtyDay(d)) baseDv[d]=dv;
  }
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
    serverWeight=stateWeight(r.shared.body);
    /* An account written by an older build can still be carrying this. Drop it
       on the way in so it cannot start the loop up again. */
    if(r.shared.body) delete r.shared.body.__migrated;
    /* Take the baseline before merging anything.
     *
     * A page that has just loaded has not edited a thing, so nothing on it is
     * its own work and everything on the account is newer. Without this, the
     * first pull of every session compared each unit against an empty snapshot,
     * decided all of them were being edited here, kept the stale local copy over
     * the account's, and then pushed that stale copy straight back up. Two
     * devices each did that on every load, so each one kept overwriting the
     * other and neither ever saw the other's work. Signing out and back in made
     * no difference because the reload is what caused it. */
    if(!_snap.__init) syncSnap();
    var hadLocal=anyDirty();
    if(r.shared.body){
      var moved=mergeIn(r.shared.body,docVer);
      seenBv(r.shared.body,docVer);
      /* Bring whatever arrived forward to the current shape.
       *
       * The migrations used to run only over the copy held on this device, so an
       * account last written by an older build handed back its old shape and
       * nothing brought it forward until the page was loaded again. Running them
       * here means anything that arrives is in the current shape immediately,
       * and because that counts as a change made here it goes back up, so the
       * account stops carrying the old shape too. */
      if(moved){
        /* Clear the "already done" mark first. It is set once when the page
           loads, and without clearing it the migration would look at data that
           arrived afterwards and decide it had nothing to do. Mapping a section
           that is already current returns it unchanged, so running it again
           costs nothing. */
        try{ delete S.__sections7; S=migrateSections(migrateToMembers(S)); delete S.__migrated; }
        catch(e){ if(window.console&&console.error) console.error('migrate on merge',e); }
      }
    }
    if(r.private.body){ PRIVATE.forEach(function(k){
      if(r.private.body[k]!==undefined) S[k]=r.private.body[k]; }); }
    syncAt=Date.now();
    syncSet('idle');
    /* Anything this device was still holding is left dirty on purpose, so the
       snapshot only moves forward over branches that now match the server. A
       half typed schedule is not thrown away by a poll landing on it. */
    allUnits().forEach(function(u){ if(!dirtyBranch(u)) snapOne(u); });
    var days=S.days||{};
    Object.keys(days).forEach(function(d){ if(!dirtyDay(d)) _snapDays[d]=JSON.stringify(days[d]); });
    _snap.__init=true;
    /* Always write, not only when the merge moved something. A device opening
       this account for the first time has nothing saved locally at all, and
       "nothing changed" is exactly the case where it most needs writing. */
    try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
    if(hadLocal||anyDirty()) queuePush();
    if(typeof redrawFromSync==='function') redrawFromSync();
  }).catch(function(){ syncSet('offline'); });
}

function queuePush(){
  if(syncState==='off') return;
  syncPending=true;
  if(syncTimer) clearTimeout(syncTimer);
  /* Short enough that the other person sees it while you are still looking at
     the screen, long enough not to send a request per keystroke. */
  syncTimer=setTimeout(pushState,600);
}

/* A rough size for a document, used only to notice a cliff. Counting the
   things people actually make means a state that lost its content registers
   even if it still has plenty of keys on it. */
function stateWeight(o){
  if(!o) return 0;
  var f=o.fin||{};
  return (f.costs||[]).length+(f.jobs||[]).length+(f.actuals||[]).length
       + Object.keys(f.scenarios||{}).length+Object.keys(f.purchases||{}).length
       + Object.keys(f.strategies||{}).length
       + Object.keys(o.days||{}).length+((o.plan||{}).cols||[]).length
       + (((o.sched||{}).cols)||[]).length+Object.keys(o.lists||{}).length
       + (o.members||[]).length+(o.fav||[]).length;
}
var serverWeight=0;

function pushState(){
  if(syncBusy||!syncPending||syncState==='off') return;
  /* Nothing goes up from a session that could not read its own saved state. */
  if(LOAD_BROKE){ syncSet('error','Not saving: '+LOAD_BROKE); return; }
  /* And nothing goes up that would empty an account. A drop this size is a bug
     in here, not a decision somebody made, and the server copy is the only one
     left once this overwrites it. */
  var w=stateWeight(S);
  if(serverWeight>=12&&w<=Math.max(2,serverWeight*0.25)){
    syncSet('error','Not saving: this would wipe most of the account');
    if(!window.__wipeWarned){
      window.__wipeWarned=1;
      toast('Saving paused. This device is holding almost nothing and the account has data.');
    }
    return;
  }
  syncBusy=true; syncPending=false;
  syncSet('push');
  var wasForce=forceNext;
  /* Freeze what goes up, and send that exact copy.
   *
   * This used to send a live reference to S and compare the reply against a
   * separate snapshot taken a moment earlier. Anything that touched S in
   * between, and merely drawing a page touches it because opening today's log
   * creates today's entry, landed in the request but not in the snapshot. The
   * comparison then said that piece never made it, so it stayed marked as
   * unsaved, and the app sent the whole document again. And again. Roughly
   * twice a second, forever, on a shared host. */
  var payload=stripLocal(S);
  payload.days=S.days;
  if(wasForce) payload.__force=true;
  var still=JSON.parse(JSON.stringify(payload));
  api('doc.php?scope=shared',{body:{version:docVer,body:still}}).then(function(r){
    if(r.ok){
      docVer=r.version; syncAt=Date.now(); syncFails=0; syncSet('idle');
      serverWeight=stateWeight(S);
      if(wasForce) forceNext=false;
      /* The server says which branches it recorded and at what version. Anything
         that has not been edited again since we sent it now matches the server,
         so its snapshot moves up; anything typed in the meantime stays dirty and
         goes in the next push. */
      if(r.__bv) for(var b in r.__bv) baseBv[b]=r.__bv[b];
      if(r.__dv) for(var d in r.__dv) baseDv[d]=r.__dv[d];
      allUnits(still).forEach(function(u){
        if(JSON.stringify(unitGet(S,u))===JSON.stringify(unitGet(still,u))) snapOne(u);
      });
      /* The snapshot is real again. Leaving this unset made the next edit look
         like the first one this session, and a first one takes a baseline
         instead of queueing a save, so it went nowhere. */
      _snap.__init=true;
      Object.keys(S.days||{}).forEach(function(d){
        if(JSON.stringify(S.days[d])===JSON.stringify((still.days||{})[d]))
          _snapDays[d]=JSON.stringify(S.days[d]);
      });
      if(anyDirty()) queuePush();
      return pushPrivate();
    }
    if(r.__status===409&&r.error==='would_wipe'){
      /* The server refused because this would empty the account. Retrying sends
         exactly the same thing, so it would refuse forever and hammer the
         server doing it. Stop, say so, and take the account's copy back down. */
      syncSet('error','Not saving: this device is holding almost nothing');
      docVer=r.version||docVer;
      syncPending=false;
      baseBv={}; baseDv={}; syncSnap();
      setTimeout(function(){ syncBusy=false; pullState(); },600);
      return 'retry';
    }
    if(r.__status===409){
      /* Somebody else wrote while we were typing. Take what they have for the
         branches we are not touching, keep ours for the ones we are, and send
         again on the next tick. */
      docVer=r.version||docVer;
      if(r.body){ mergeIn(r.body,docVer); seenBv(r.body,docVer); }
      try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}
      if(typeof redrawFromSync==='function') redrawFromSync();
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

/* Watching for the other person.
 *
 * Two people on one household need each other's edits to turn up while they are
 * looking at the page, not on the next refresh. A full document every few
 * seconds would be rude to a shared host, so this asks for the version numbers
 * instead, which is two integers, and only pulls the document when one of them
 * has moved. Backgrounded tabs slow right down; nobody is reading them. */
var verTimer=null, verFails=0;
function checkVersions(){
  if(syncState==='off'||syncBusy) return;
  api('doc.php?do=ver').then(function(r){
    if(!r||!r.ok){ verFails++; return; }
    verFails=0;
    if((r.shared||0)!==docVer||(r.private||0)!==privVer) pullState();
  }).catch(function(){ verFails++; });
}
function watchTick(){
  if(verTimer) clearTimeout(verTimer);
  var hidden=document.hidden;
  /* Back off when the network keeps refusing rather than hammering it. */
  var every=hidden?45000:(verFails>3?30000:5000);
  verTimer=setTimeout(function(){ checkVersions(); watchTick(); },every);
}

function syncStart(){
  syncSet('idle');
  window.addEventListener('focus',function(){ if(!syncBusy) pullState(); });
  window.addEventListener('online',function(){ pullState(); });
  document.addEventListener('visibilitychange',function(){
    if(!document.hidden&&!syncBusy) pullState();
    watchTick();
  });
  watchTick();
  /* A tab closing mid-edit should still land. */
  window.addEventListener('pagehide',function(){
    if(syncPending&&!syncBusy){ if(syncTimer) clearTimeout(syncTimer); pushState(); }
  });
}
"""
