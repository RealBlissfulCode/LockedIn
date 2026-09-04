# -*- coding: utf-8 -*-
APP_CORE = r"""
/* ============================================================
   THE HANDBOOK  -  five sections, one state object, one file.
   Everything the app knows lives in S. S is written to
   localStorage on every change and can be saved to / loaded
   from a real .json file so it can be handed back for edits.
   ============================================================ */
var R=_D.recipes, BASEING=_D.ing, AISLES=_D.aisles, LEARN=_D.learn;
var EX=_D.exercises, SESS=_D.sessions;
/* Local cache of the signed in account's state. The server holds the copy that
   matters; this is what makes the app usable on a plane. */
var KEY='lockedin.v7';

/* ---------------- state ---------------- */
/* A fresh account is one person and nothing else. No second profile waiting to
   be renamed, no seeded shopping list, no costs already filled in. Everything
   in here past the first member is something you chose to add. */
function blankMember(name,sex){
  return {id:uid(),name:name||'Me',sex:sex||'m',w:null,h:null,age:null,bf:null,
          act:1.45,goal:1,pf:1,accent:''};
}
function DEF(){return{
 v:7, who:null, savedAt:null, theme:'dark',
 members:[], household:'',
 ingOv:{}, fav:[], lists:{}, mine:[], photos:{},
 shop:{active:null, lists:{}},
 days:{},
 fin:{jobs:[],shifts:[],costs:[],scenarios:{},purchases:{},strategies:{},
      costMode:'real',path:'rent',activeScenario:null, draft:null},
 plan:{cols:[]},
 sched:{tmpl:{}, cols:[]},
 exLog:{}, prefs:{}, onboarded:false, seeded:false, seeded6:false
};}
/* Anything saved before the household rewrite has two profiles and rows tagged
   with names. Turn those two profiles into members, then walk every row that
   ever stored a person and swap the name for the new id. Miss one and an
   income line ends up belonging to nobody, so the list below is the full set
   of places a person token was ever written. */
function migrateToMembers(o){
  if(o.members&&o.members.length) return o;
  var map={};
  o.members=[];
  ['j','a'].forEach(function(k){
    var pr=(o.prof||{})[k]; if(!pr) return;
    var m=blankMember(pr.name||(k==='j'?'Me':'Her'),pr.sex||(k==='j'?'m':'f'));
    ['w','h','age','bf','act','goal','pf'].forEach(function(f){
      if(pr[f]!==undefined&&pr[f]!==null) m[f]=pr[f];});
    o.members.push(m);
    map[k]=m.id;
  });
  /* The old fixed tokens, and the names they were showing under. */
  map['Jaron']=map.j; map['Aaliyah']=map.a; map['Both']=EVERYONE;
  if((o.prof||{}).j&&o.prof.j.name) map[o.prof.j.name]=map.j;
  if((o.prof||{}).a&&o.prof.a.name) map[o.prof.a.name]=map.a;

  function fix(v){
    if(v===undefined||v===null||v==='') return v;
    if(map[v]!==undefined) return map[v];
    return v;
  }
  o.who=map[o.who]||map.j||null;

  (o.fin&&o.fin.jobs||[]).forEach(function(x){x.who=fix(x.who);});
  (o.fin&&o.fin.costs||[]).forEach(function(x){x.who=fix(x.who);});
  Object.keys(o.fin&&o.fin.scenarios||{}).forEach(function(n){
    var sc=o.fin.scenarios[n]||{};
    (sc.jobs||[]).forEach(function(x){x.who=fix(x.who);});
    (sc.costs||[]).forEach(function(x){x.who=fix(x.who);});
  });
  Object.keys(o.days||{}).forEach(function(ds){
    var d=o.days[ds]||{};
    if(d.trainWho) d.trainWho=fix(d.trainWho);
    (d.meals||[]).forEach(function(x){x.who=fix(x.who);});
    (d.sched||[]).forEach(function(x){x.who=fix(x.who);});
  });
  ((o.sched||{}).cols||[]).forEach(function(c){
    Object.keys(c.days||{}).forEach(function(k){
      (c.days[k]||[]).forEach(function(x){x.who=fix(x.who);});});
  });
  Object.keys((o.sched||{}).tmpl||{}).forEach(function(k){
    (o.sched.tmpl[k]||[]).forEach(function(x){x.who=fix(x.who);});
  });
  delete o.prof;
  o.v=7;
  return o;
}
var S=(function(){
  try{var raw=localStorage.getItem(KEY);
    if(raw){var o=JSON.parse(raw),d=DEF();
      for(var k in d) if(!(k in o)) o[k]=d[k];
      for(var f in d.fin) if(!(f in o.fin)) o.fin[f]=d.fin[f];
      return migrateToMembers(o);}
  }catch(e){}
  return DEF();
})();
function save(){ S.savedAt=Date.now();
  try{syncTouch();}catch(e){}
  try{localStorage.setItem(KEY,JSON.stringify(S));}
  catch(e){toast('Storage full. Save to file, then remove some photos.');}
  try{syncSchedule();}catch(e){}}

/* The old build shipped one household's costs, jobs, purchase lists and plans
   baked into the page and dropped them into the first browser that opened it.
   A product cannot do that. New accounts start empty and get their starting
   points from onboarding instead, which is in app_setup. */

/* There used to be exactly one weekly template. Fold whatever is in it into a
   collection so nothing already entered is lost, and clear the old slot so this
   cannot fire twice. No flag needed, and nothing is written unless there was
   something to move, which matters because a pointless save would stamp the
   branch and make this device look like the newer author of it. */
if(S.sched){
  if(!S.sched.cols) S.sched.cols=[];
  var _legacy=S.sched.tmpl||{}, _anyLegacy=false;
  for(var _lk in _legacy){ if((_legacy[_lk]||[]).length){ _anyLegacy=true; break; } }
  if(_anyLegacy){
    var _ld={};
    for(var _q=0;_q<7;_q++) _ld[_q]=(_legacy[_q]||[]).map(function(x){
      return {id:uid(),who:x.who,what:x.what,where:x.where||'',
              from:x.from||'',to:x.to||''};});
    S.sched.cols.push({id:uid(),name:'My week',
      note:'Brought over from the old weekly template.',
      fav:true,active:false,repeat:'weekly',anchor:today(),days:_ld});
    S.sched.tmpl={};
    save();
  }
}

/* ---------------- schedule templates ----------------
   A template is a named set of items keyed by weekday. It can be applied once
   over a range, or left standing, in which case its items are computed when a
   day is drawn rather than copied in. Standing beats copying: turning one off
   clears it everywhere at once and there are never stale duplicates to hunt. */
var REPEATS=[['weekly','Every week'],['biweekly','Every other week'],
             ['monthly','Once a month, same week'],['once','Only when I apply it']];
var SCOPES=[['week','This week'],['month','This month'],
            ['next4','The next 4 weeks'],['next3m','The next 3 months']];
function tmplCols(){ return (S.sched&&S.sched.cols)||[]; }
function tmplCol(id){var c=tmplCols().filter(function(x){return x.id===id;});return c[0]||null;}
function tmplCount(c){var n=0;for(var i=0;i<7;i++)n+=((c.days||{})[i]||[]).length;return n;}
function weekStart(d){var x=new Date(d.getFullYear(),d.getMonth(),d.getDate());
  x.setDate(x.getDate()-x.getDay());return x;}
function tmplMatches(c,ds){
  var d=dOf(ds), wd=d.getDay();
  if(!((c.days||{})[wd]||[]).length) return false;
  var rep=c.repeat||'weekly';
  if(rep==='once') return false;
  if(rep==='weekly') return true;
  var anchor=dOf(c.anchor||ds);
  if(rep==='biweekly'){
    var wk=Math.round((weekStart(d)-weekStart(anchor))/604800000);
    return ((wk%2)+2)%2===0;
  }
  /* "Same week of the month" as the anchor, so a first-Sunday thing stays a
     first-Sunday thing rather than drifting by date. */
  if(rep==='monthly') return Math.ceil(d.getDate()/7)===Math.ceil(anchor.getDate()/7);
  return true;
}
function tmplItemsFor(ds){
  var out=[], wd=dOf(ds).getDay(), log=S.days[ds];
  tmplCols().forEach(function(c){
    if(!c.active||!tmplMatches(c,ds)) return;
    ((c.days||{})[wd]||[]).forEach(function(x){
      /* Already applied by hand on this day: show it once, not twice. */
      if(log&&(log.sched||[]).some(function(e){
        return e.what===x.what&&e.who===x.who&&(e.from||'')===(x.from||'');})) return;
      out.push({who:x.who,what:x.what,where:x.where||'',
                from:x.from||'',to:x.to||'',col:c.name});
    });
  });
  return out;
}
function applyCollection(id,scope){
  var c=tmplCol(id); if(!c) return 0;
  var now=new Date(), start, end;
  if(scope==='month'){ start=new Date(calY,calM,1); end=new Date(calY,calM+1,0); }
  else if(scope==='next4'){ start=new Date(now); end=new Date(now); end.setDate(end.getDate()+27); }
  else if(scope==='next3m'){ start=new Date(now); end=new Date(now); end.setMonth(end.getMonth()+3); }
  else { start=new Date(now); start.setDate(start.getDate()-start.getDay());
         end=new Date(start); end.setDate(start.getDate()+6); }
  var n=0, cur=new Date(start);
  while(cur<=end){
    var ds=cur.getFullYear()+'-'+p2(cur.getMonth()+1)+'-'+p2(cur.getDate());
    /* A one-off template has no schedule of its own, so applying it just means
       "every matching weekday in this range". */
    if(c.repeat==='once'||tmplMatches(c,ds)){
      var items=((c.days||{})[cur.getDay()]||[]), log=dayLog(ds);
      for(var i=0;i<items.length;i++){
        var x=items[i];
        var dupe=log.sched.some(function(e){
          return e.what===x.what&&e.who===x.who&&(e.from||'')===(x.from||'');});
        if(!dupe){log.sched.push({who:x.who,what:x.what,from:x.from,to:x.to,
          where:x.where||''});n++;}
      }
    }
    cur.setDate(cur.getDate()+1);
  }
  if(n) save();
  return n;
}

/* ---------------- who is who ----------------
   The app used to know about exactly two people, stored as prof.j and prof.a,
   with rows tagged 'Jaron', 'Aaliyah' or 'Both'. That worked for one household
   and nothing else. Now a household is a list of members, each with an id, and
   a row is tagged with that id or with 'all' for something shared.

   Everything user facing goes through WHO so renaming somebody updates the
   whole app at once, and nothing stored ever holds a name. */
var EVERYONE='all';
function MEMS(){return S.members||[];}
function MEM(id){
  var m=MEMS();
  for(var i=0;i<m.length;i++) if(m[i].id===id) return m[i];
  return null;
}
function firstMember(){var m=MEMS();return m.length?m[0]:null;}
/* Whoever is selected up top is the default actor for anything logged. If the
   selection points at somebody who has since been removed, fall back rather
   than handing every caller a null. */
function ME(){
  if(S.who&&MEM(S.who)) return S.who;
  var f=firstMember();
  return f?f.id:null;
}
function P(){return MEM(ME())||blankMember();}
function WHO(tok){
  if(tok===EVERYONE) return MEMS().length>2?'Everyone':'Both of us';
  var m=MEM(tok);
  return m?m.name:'';
}
function MENAME(){return WHO(ME());}
function whoOpts(){
  var o=MEMS().map(function(m){return [m.id,m.name];});
  if(MEMS().length>1) o.push([EVERYONE,MEMS().length>2?'Everyone':'Both of us']);
  return o;
}
/* Only ever true when there is somebody else to share with, so a solo account
   never sees a Who dropdown offering to split things with nobody. */
function shared(){return MEMS().length>1;}
/* Every token a row can be tagged with, members first and the shared bucket
   last, for anything that groups by person. */
function whoTokens(){
  return MEMS().map(function(m){return m.id;}).concat([EVERYONE]);
}

/* ---------------- helpers ---------------- */
function $(s,r){return (r||document).querySelector(s);}
function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}
function E(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
/* Money formatting done by hand. toLocaleString with options is ignored by some
   engines, which then prints the raw float. */
function commas(s){var p=String(s).split('.'),i=p[0],out='',c=0;
  for(var x=i.length-1;x>=0;x--){out=i.charAt(x)+out;if(++c%3===0&&x>0)out=','+out;}
  return p.length>1?out+'.'+p[1]:out;}
function $$$(v){var n=Number(v);if(!isFinite(n))n=0;
  return (n<0?'-$':'$')+commas(Math.abs(n).toFixed(2));}
function M(v){var n=Math.round(Number(v)||0);
  return (n<0?'-$':'$')+commas(Math.abs(n));}
function N(v){return commas(Math.round(Number(v)||0));}
function p2(n){n=String(n);return n.length<2?'0'+n:n;}
/* Times are stored as 24h "HH:MM" because that is what <input type="time">
   speaks and what sorts correctly. Nothing is ever SHOWN that way. */
function t12(t){
  if(!t) return '';
  var p=String(t).split(':'), h=parseInt(p[0],10), m=parseInt(p[1]||'0',10);
  if(isNaN(h)||isNaN(m)) return t;
  return (h%12||12)+(m?':'+p2(m):'')+(h>=12?'pm':'am');
}
/* Same thing from minutes past midnight, for the free-time finder. */
function t12m(mins){
  var h=Math.floor(mins/60), m=mins%60;
  return (h%12||12)+(m?':'+p2(m):'')+(h>=12?'pm':'am');
}
function range12(from,to){
  if(!from) return '';
  return t12(from)+(to?' – '+t12(to):'');
}
function today(){var d=new Date();return d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());}
function dOf(ds){var p=ds.split('-');return new Date(+p[0],+p[1]-1,+p[2]);}
function pretty(ds){return dOf(ds).toLocaleDateString(undefined,{weekday:'long',month:'short',day:'numeric'});}
function shortD(ds){return dOf(ds).toLocaleDateString(undefined,{month:'short',day:'numeric'});}
function uid(){return Math.random().toString(36).slice(2,9);}
function toast(m){var t=document.createElement('div');t.className='toast';t.textContent=m;
  document.body.appendChild(t);setTimeout(function(){t.remove();},2600);}
function dl(name,text,mime){var b=new Blob([text],{type:mime||'text/plain'});
  var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href);},1200);}
function applyTheme(){
  var t=S.theme||'dark';
  if(t==='auto'){
    try{t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches)?'light':'dark';}
    catch(e){t='dark';}
  }
  document.documentElement.setAttribute('data-theme',t);
}
function num(x,d){var n=parseFloat(x);return isNaN(n)?(d||0):n;}

/* ---------------- ingredients: base + user overrides ---------------- */
function ING(k){
  var b=BASEING[k], o=S.ingOv[k];
  if(!b&&!o) return null;
  var m={};
  if(b) for(var x in b) m[x]=b[x];
  if(o) for(var y in o) if(o[y]!==null&&o[y]!==undefined&&o[y]!=='') m[y]=o[y];
  return m;
}
function allIngKeys(){
  var s={};for(var k in BASEING)s[k]=1;for(var j in S.ingOv)s[j]=1;
  return Object.keys(s).filter(function(k){return !S.ingOv[k]||!S.ingOv[k].deleted;});
}
function best(q){ if(!q) return 0;
  var w=q.w,c=q.c;
  if(c!=null&&c>0&&(w==null||w<=0||c<w)) return c;
  return w||0;}
function bestStore(q){ if(!q) return '';
  var w=q.w,c=q.c;
  if(c!=null&&c>0&&(w==null||w<=0||c<w)) return 'Costco';
  return 'Walmart';}
/* recipe cost is always recomputed from live ingredient prices, so an
   edited price flows straight through to every recipe that uses it */
function rcost(r){
  var t=0,any=false;
  (r.ing||[]).forEach(function(i){
    var q=ING(i[1]); if(!q) return;
    var p=best(q); if(p>0){any=true;t+=(i[2]||0)/100*p;}
  });
  if(!any) return {tot:r.cw||0,per:r.cws||0};
  return {tot:t, per:t/Math.max(r.sv||1,1)};
}
function cps(r){return rcost(r).per;}
function ctot(r){return rcost(r).tot;}
function all(){return R.concat(S.mine);}
function byId(id){var A=all();for(var i=0;i<A.length;i++)if(A[i].id===id)return A[i];return null;}

/* ---------------- nutrition ---------------- */
function calc(p){
  var kg=p.w*0.45359237, cm=p.h*2.54, m=cm/100, lbm=kg*(1-p.bf/100);
  var rmr=(10*kg)+(6.25*cm)-(5*p.age)+(p.sex==='f'?-161:5);
  var tdee=rmr*p.act, kcal=tdee*p.goal;
  var prot=p.w*p.pf, fat=kcal*0.25/9, carb=(kcal-prot*4-fat*9)/4;
  return {rmr:Math.round(rmr),katch:Math.round(370+21.6*lbm),tdee:Math.round(tdee),
    kcal:Math.round(kcal),p:Math.round(prot),c:Math.round(carb),f:Math.round(fat),
    fib:Math.round(kcal/1000*14),w:Math.round(p.w*0.6+35),lbm:Math.round(p.w*(1-p.bf/100)),
    ffmi:(lbm/(m*m)+6.1*(1.8-m)).toFixed(1),rate:(kcal-tdee)*7/3500};
}
var TRAIN={
 rest:{n:'Rest day',k:0.94,c:0.80,p:1.00,why:'Repair happens on rest days, so protein holds. Carbs ease back, fiber and micronutrients come up.'},
 pull:{n:'Back and biceps',k:1.02,c:1.05,p:1.08,why:'Biggest upper-body group. Protein and leucine lead, and iron-rich meals get weighted up.'},
 push:{n:'Chest, shoulders, triceps',k:1.02,c:1.02,p:1.08,why:'Straight hypertrophy demand. Leucine per feeding matters most.'},
 legs:{n:'Legs',k:1.10,c:1.30,p:1.04,why:'Legs empty the most glycogen of any session. Carbs and total calories lead.'},
 arms:{n:'Arms',k:0.99,c:0.95,p:1.05,why:'Small group, small systemic cost. Protein holds, calories do not spike.'},
 abs:{n:'Abs and core',k:0.96,c:0.88,p:1.02,why:'Low energy cost. Food volume and fiber over calories.'},
 cardio:{n:'Cardio',k:1.06,c:1.25,p:0.98,why:'Carbs and fluid lead. Sodium matters more in dry Colorado air.'},
 skill:{n:'Skill work',k:1.01,c:1.10,p:1.04,why:'Loads connective tissue more than muscle. Omega-3 and nutrient density weighted up.'},
 full:{n:'Full body',k:1.06,c:1.15,p:1.08,why:'Everything trained, everything demanded.'}
};
function dayLog(ds){ if(!S.days[ds]) S.days[ds]={workout:'rest',meals:[],notes:'',w:null,sched:[],spend:[]};
  var d=S.days[ds]; if(!d.sched)d.sched=[]; if(!d.spend)d.spend=[]; return d;}
/* who is a member id. A member who has not filled in their body stats yet gets
   the neutral defaults rather than a division by nothing, so the meals page
   still works on day one. */
function dayTarget(who,tt){
  var m=MEM(who)||P();
  var b=calc(m), t=TRAIN[tt||'rest'];
  var kcal=Math.round(b.kcal*t.k), pr=Math.round(b.p*t.p), cb=Math.round(b.c*t.c);
  var ft=Math.round((kcal-pr*4-cb*4)/9), floor=Math.round((m.w||150)*0.3);
  if(ft<floor){ft=floor;cb=Math.round((kcal-pr*4-ft*9)/4);}
  return {kcal:kcal,p:pr,c:cb,f:ft,fib:Math.round(kcal/1000*14),w:b.w,tr:t,base:b};
}
function eaten(ds){var d=dayLog(ds),o={kcal:0,p:0,c:0,f:0,fib:0,cost:0};
  d.meals.forEach(function(m){var r=byId(m.id);if(!r)return;var q=m.q||1;
    o.kcal+=r.k*q;o.p+=r.p*q;o.c+=r.c*q;o.f+=r.f*q;o.fib+=(r.fib||0)*q;o.cost+=cps(r)*q;});
  return o;}

/* cost per macro: what a day of these targets actually costs, from real recipes */
function costModel(){
  var A=all().filter(function(r){return r.k>60;});
  var pk=0,pp=0,n=0;
  A.forEach(function(r){var c=cps(r); if(c<=0)return;
    pk+=c/r.k; pp+=(r.p>0?c/r.p:0); n++;});
  return {perKcal:pk/n, perProtein:pp/n, n:n};
}
function estDayCost(t,mode){
  var A=all().filter(function(r){return r.k>60;});
  if(mode==='fav'&&S.fav.length) A=S.fav.map(byId).filter(Boolean);
  if(mode==='cheap') A=A.slice().sort(function(a,b){return (cps(a)/a.k)-(cps(b)/b.k);}).slice(0,40);
  if(mode==='logged'){
    var days=Object.keys(S.days).filter(function(d){return S.days[d].meals.length;});
    if(days.length){var c=0,k=0;
      days.forEach(function(d){var e=eaten(d);c+=e.cost;k+=e.kcal;});
      if(k>0) return {byKcal:t.kcal*(c/k), byProt:null, src:days.length+' logged days'};}
  }
  if(!A.length) A=all();
  var pk=0,n=0,pp=0,np=0;
  A.forEach(function(r){var c=cps(r);if(c<=0)return;pk+=c/r.k;n++;
    if(r.p>3){pp+=c/r.p;np++;}});
  return {byKcal:t.kcal*(pk/Math.max(n,1)), byProt:t.p*(pp/Math.max(np,1)),
          src:(mode==='fav'?'favourites':mode==='cheap'?'the 40 cheapest per calorie':'all '+n+' recipes')};
}

/* ---------------- file persistence ---------------- */
/* Forget the passcode on this device. The data itself is untouched; the next
   load just asks for the code again. */
function lock(){
  try{localStorage.removeItem('handbook.unlocked');}catch(e){}
  location.reload();
}
function exportAll(){
  var blob={app:'handbook',version:6,exported:new Date().toISOString(),state:S};
  dl('handbook-data-'+today()+'.json',JSON.stringify(blob,null,1),'application/json');
  toast('Saved to file');
}
function importAll(file,cb){
  var fr=new FileReader();
  fr.onload=function(){
    try{
      var o=JSON.parse(fr.result);
      var st=o.state||o;
      if(!st.prof) throw new Error('not a handbook file');
      var d=DEF(); for(var k in d) if(!(k in st)) st[k]=d[k];
      var keepV=S.__v;
      S=st; S.__v=keepV;
      /* A restored file replaces everything on purpose, so it claims every
         branch. Otherwise the merge would treat it as older than the server
         and quietly undo the restore on the next sync. */
      try{syncClaimAll();}catch(e){}
      save(); cb&&cb(true);
    }catch(e){ alert('That did not read as a handbook file.\n\n'+e.message); cb&&cb(false); }
  };
  fr.readAsText(file);
}
/* ---------------- scenarios ----------------
   A scenario is a complete snapshot: every income line, every cost line, the
   mode and the housing path. Editing while a scenario is open writes to a
   draft; nothing overwrites the saved copy until Save is pressed. */
/* Scenarios saved by earlier versions only held summary numbers. Upgrade them
   on read so the comparison table never meets an undefined array. */
function scenFix(n){
  var sc=S.fin.scenarios[n]; if(!sc) return null;
  if(!sc.jobs||!sc.jobs.length||!sc.costs||!sc.costs.length){
    sc.jobs=(sc.jobs&&sc.jobs.length)?sc.jobs:JSON.parse(JSON.stringify(S.fin.jobs));
    sc.costs=(sc.costs&&sc.costs.length)?sc.costs:JSON.parse(JSON.stringify(S.fin.costs));
    sc.mode=sc.mode||'real'; sc.path=sc.path||'rent'; sc.legacy=true;
  }
  return sc;
}
function scenAllFixed(){
  var out=[],names=Object.keys(S.fin.scenarios||{}),changed=false;
  names.forEach(function(n){var before=S.fin.scenarios[n].jobs?1:0;
    var sc=scenFix(n); if(!before&&sc)changed=true; out.push([n,sc]);});
  if(changed) save();
  return out;
}
function snapshot(){
  return {mode:S.fin.costMode,path:S.fin.path,
    jobs:JSON.parse(JSON.stringify(S.fin.jobs)),
    costs:JSON.parse(JSON.stringify(S.fin.costs)),
    saved:today()};
}
function scenSave(name){
  if(!name) return false;
  S.fin.scenarios[name]=snapshot();
  S.fin.activeScenario=name; S.fin.draft=null; save(); return true;
}
function scenLoad(name){
  var sc=scenFix(name); if(!sc) return false;
  S.fin.jobs=JSON.parse(JSON.stringify(sc.jobs));
  S.fin.costs=JSON.parse(JSON.stringify(sc.costs));
  S.fin.costMode=sc.mode||'real'; S.fin.path=sc.path||'rent';
  S.fin.activeScenario=name; S.fin.draft=null; save(); return true;
}
function scenDirty(){
  var n=S.fin.activeScenario; if(!n||!S.fin.scenarios[n]) return false;
  var a=scenFix(n); if(!a) return false;
  var b=snapshot();
  return JSON.stringify([a.jobs,a.costs,a.mode,a.path])!==JSON.stringify([b.jobs,b.costs,b.mode,b.path]);
}
function scenRevert(){ if(S.fin.activeScenario) scenLoad(S.fin.activeScenario); }
function csvEsc(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function toCSV(rows){return rows.map(function(r){return r.map(csvEsc).join(',');}).join('\n');}
"""
