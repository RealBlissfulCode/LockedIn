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
/* Everything personal arrives decrypted from the gate, never from _D. */
var SEED=window._SEED||{};
var SEEDCOST=SEED.costs||[], SEEDJOB=SEED.jobs||[];
var KEY='handbook.v5';

/* ---------------- state ---------------- */
function DEF(){return{
 v:6, who:'j', savedAt:null, theme:'dark',
 prof:{j:{name:'Me',sex:'m',w:150,h:68,age:20,bf:20,act:1.55,goal:1.09,pf:1.1},
       a:{name:'Aaliyah',sex:'f',w:120,h:66.5,age:20,bf:24,act:1.45,goal:1.0,pf:0.8}},
 ingOv:{}, fav:[], lists:{}, mine:[], photos:{},
 shop:{active:'Weekly shop', lists:{'Weekly shop':{cat:'Groceries',fav:true,items:[]}}},
 days:{},
 fin:{jobs:[],shifts:[],costs:[],scenarios:{},purchases:{},strategies:{},
      costMode:'real',path:'rent',activeScenario:null, draft:null},
 plan:{cols:[]},
 sched:{tmpl:{}, },
 exLog:{}, seeded:false, seeded6:false
};}
var S=(function(){
  try{var raw=localStorage.getItem(KEY);
    if(raw){var o=JSON.parse(raw),d=DEF();
      for(var k in d) if(!(k in o)) o[k]=d[k];
      for(var p in d.prof) if(!o.prof[p]) o.prof[p]=d.prof[p];
      for(var f in d.fin) if(!(f in o.fin)) o.fin[f]=d.fin[f];
      return o;}
  }catch(e){}
  return DEF();
})();
function save(){ S.savedAt=Date.now();
  try{localStorage.setItem(KEY,JSON.stringify(S));}
  catch(e){toast('Storage full. Save to file, then remove some photos.');}}

/* Seed from the Moving In workbook, ONCE per browser.

   These are not templates and they are not owned by the app. The moment they
   land they are ordinary rows: rename them, edit them, delete them, and they
   stay however you left them. Nothing here re-appears on the next deploy, and
   deleting the last strategy list does not bring it back. The flags below are
   the whole mechanism. */
if(!S.seeded){
  S.fin.costs=SEEDCOST.map(function(c,i){return{id:'c'+i,name:c.name,section:c.section,
    who:c.who,low:c.low,real:c.real,high:c.high,actual:c.exact||null};});
  S.fin.jobs=SEEDJOB.map(function(j,i){return{id:'j'+i,who:j.who,name:j.name,
    employer:j.employer,title:j.title,rate:null,low:j.low,real:j.real,high:j.high};});
  S.seeded=true; save();
}
if(!S.seeded6){
  var SP=SEED.purchases||{}, SS=SEED.strategies||{}, SL=SEED.planning||[];
  /* Only fill a slot that is genuinely empty, so nothing you already made is
     touched and a list you deleted before this build does not come back. */
  Object.keys(SP).forEach(function(n){
    if(S.fin.purchases[n]) return;
    S.fin.purchases[n]={cat:SP[n].cat,note:SP[n].note||'',
      items:SP[n].items.map(function(it){
        return {id:uid(),name:it.name,price:it.price,link:it.link||'',
                notes:it.notes||'',fields:it.fields||{}};})};
  });
  Object.keys(SS).forEach(function(n){
    if(S.fin.strategies[n]) return;
    S.fin.strategies[n]={note:SS[n].note||'',
      items:SS[n].items.map(function(it){
        return {id:uid(),name:it.name,low:it.low,real:it.real,high:it.high,
                rate:it.rate||'',effort:it.effort||'',when:it.when||'',
                status:it.status||'',how:it.how||''};})};
  });
  SL.forEach(function(c){
    if(S.plan.cols.some(function(x){return x.name===c.name;})) return;
    S.plan.cols.push({id:uid(),name:c.name,note:c.note||'',
      subs:(c.subs||[]).map(function(s){
        return {id:uid(),name:s.name,note:s.note||'',
          items:(s.items||[]).map(function(i){
            return {id:uid(),text:i.text,note:i.note||'',done:false};})};})});
  });
  S.seeded6=true; save();
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
function P(){return S.prof[S.who];}
/* whoever is selected up top is the default actor for anything logged */
function ME(){return S.who==='j'?'Jaron':'Aaliyah';}
function whoOpts(){return [['Jaron','Jaron'],['Aaliyah','Aaliyah'],['Both','Both of us']];}
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
function dayTarget(who,tt){
  var b=calc(S.prof[who]), t=TRAIN[tt||'rest'];
  var kcal=Math.round(b.kcal*t.k), pr=Math.round(b.p*t.p), cb=Math.round(b.c*t.c);
  var ft=Math.round((kcal-pr*4-cb*4)/9), floor=Math.round(S.prof[who].w*0.3);
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
      S=st; save(); cb&&cb(true);
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
