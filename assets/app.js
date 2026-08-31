(function(){
'use strict';
var _D=window._DATA;

/* ============================================================
   THE HANDBOOK  -  five sections, one state object, one file.
   Everything the app knows lives in S. S is written to
   localStorage on every change and can be saved to / loaded
   from a real .json file so it can be handed back for edits.
   ============================================================ */
var R=_D.recipes, BASEING=_D.ing, AISLES=_D.aisles, LEARN=_D.learn;
var EX=_D.exercises, SESS=_D.sessions, SEEDCOST=_D.costs, SEEDJOB=_D.jobs;
var KEY='handbook.v5';

/* ---------------- state ---------------- */
function DEF(){return{
 v:5, who:'j', savedAt:null,
 prof:{j:{name:'Me',sex:'m',w:150,h:68,age:20,bf:20,act:1.55,goal:1.09,pf:1.1},
       a:{name:'Aaliyah',sex:'f',w:120,h:66.5,age:20,bf:24,act:1.45,goal:1.0,pf:0.8}},
 ingOv:{}, fav:[], lists:{}, mine:[], photos:{},
 shop:{active:'Weekly shop', lists:{'Weekly shop':{cat:'Groceries',fav:true,items:[]}}},
 days:{},
 fin:{jobs:[],shifts:[],costs:[],scenarios:{},purchases:{},costMode:'real',path:'rent',
      activeScenario:null, draft:null},
 sched:{tmpl:{}, },
 exLog:{}, seeded:false
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

/* seed financial data from the Moving In workbook, once */
if(!S.seeded){
  S.fin.costs=SEEDCOST.map(function(c,i){return{id:'c'+i,name:c.name,section:c.section,
    who:c.who,low:c.low,real:c.real,high:c.high,actual:c.exact||null};});
  S.fin.jobs=SEEDJOB.map(function(j,i){return{id:'j'+i,who:j.who,name:j.name,
    employer:j.employer,title:j.title,rate:null,low:j.low,real:j.real,high:j.high};});
  S.seeded=true; save();
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
function exportAll(){
  var blob={app:'handbook',version:5,exported:new Date().toISOString(),state:S};
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
  var sc=S.fin.scenarios[name]; if(!sc) return false;
  S.fin.jobs=JSON.parse(JSON.stringify(sc.jobs));
  S.fin.costs=JSON.parse(JSON.stringify(sc.costs));
  S.fin.costMode=sc.mode||'real'; S.fin.path=sc.path||'rent';
  S.fin.activeScenario=name; S.fin.draft=null; save(); return true;
}
function scenDirty(){
  var n=S.fin.activeScenario; if(!n||!S.fin.scenarios[n]) return false;
  var a=S.fin.scenarios[n], b=snapshot();
  return JSON.stringify([a.jobs,a.costs,a.mode,a.path])!==JSON.stringify([b.jobs,b.costs,b.mode,b.path]);
}
function scenRevert(){ if(S.fin.activeScenario) scenLoad(S.fin.activeScenario); }
function csvEsc(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function toCSV(rows){return rows.map(function(r){return r.map(csvEsc).join(',');}).join('\n');}

/* ============================ MEALS ============================ */
var CATC={'Breakfast':['#D89A3C','#B0651F'],'Lunch/Dinner':['#2C6B50','#173C2C'],
 'Snack':['#4E8C7A','#28584A'],'Drink':['#6E5AA8','#3F3168'],
 'SDA Meat/Fish':['#C4614B','#8A3826'],'My recipe':['#6B6B5E','#3E3E36']};
function ringSVG(r){
  var tot=r.p*4+r.c*4+r.f*9||1, C=2*Math.PI*15.9155;
  var segs=[[r.p*4/tot,'#1F4D3A'],[r.c*4/tot,'#C2860E'],[r.f*9/tot,'#5C4A78']],off=25,h='';
  segs.forEach(function(s){var L=s[0]*C;
    h+='<circle cx="18" cy="18" r="15.9155" fill="none" stroke="'+s[1]+'" stroke-width="4.4" '+
       'stroke-dasharray="'+L.toFixed(2)+' '+(C-L).toFixed(2)+'" stroke-dashoffset="'+off.toFixed(2)+'"/>';
    off-=L;});
  return '<svg class="ring" viewBox="0 0 36 36" width="58" height="58">'+
    '<circle cx="18" cy="18" r="15.9155" fill="rgba(255,255,255,.14)" stroke="rgba(255,255,255,.22)" stroke-width="4.4"/>'+
    h+'<text x="18" y="19.4" text-anchor="middle" font-size="8.2" font-weight="800" fill="#fff">'+Math.round(r.k)+'</text>'+
    '<text x="18" y="25" text-anchor="middle" font-size="4.2" font-weight="700" fill="rgba(255,255,255,.8)">KCAL</text></svg>';
}
function art(r){
  var ph=S.photos[r.id];
  if(ph) return '<div class="rcart"><img src="'+ph+'" alt=""></div>';
  var c=CATC[r.cat]||CATC['My recipe'];
  return '<div class="rcart" style="background:linear-gradient(135deg,'+c[0]+','+c[1]+')">'+
    '<svg class="plate" viewBox="0 0 120 70" preserveAspectRatio="xMidYMid meet">'+
    '<circle cx="45" cy="35" r="21" fill="none" stroke="rgba(255,255,255,.30)" stroke-width="3"/>'+
    '<circle cx="45" cy="35" r="12" fill="none" stroke="rgba(255,255,255,.20)" stroke-width="2"/>'+
    '<path d="M78 18v34M86 18v12a4 4 0 004 4h0v18M96 18v34" stroke="rgba(255,255,255,.28)" stroke-width="3" fill="none" stroke-linecap="round"/>'+
    '</svg>'+ringSVG(r)+'</div>';
}
function pscale(v){return v<1.6?'$':v<3.2?'$$':'$$$';}
function bestFor(r){
  if(r.tg.indexOf('LEUCINE PRIORITY')>=0||r.p>=40)return 'Protein';
  if(r.tg.indexOf('CHEAT MEAL')>=0)return 'Cheat';
  if(r.tg.indexOf('HEALTHY DESSERT')>=0||r.tg.indexOf('CHEAT DESSERT')>=0)return 'Dessert';
  if(r.c>=70)return 'Carbs'; if(r.tg.indexOf('HIGH FIBER')>=0)return 'Fiber';
  if(r.k<=350)return 'Lean'; if(r.k>=600)return 'Calories'; return 'Balanced';}
function rcard(r){
  var f=S.fav.indexOf(r.id)>=0, dc=r.diff==='EASY'?'d1':r.diff==='MODERATE'?'d2':'d3';
  return '<article class="rc" data-go="'+r.id+'">'+art(r)+
   '<button class="fav'+(f?' on':'')+'" data-fav="'+r.id+'">'+(f?'\u2605':'\u2606')+'</button>'+
   '<div class="rcbadge">'+r.id+'</div><div class="rcb"><div class="rcn">'+E(r.n)+'</div>'+
   '<div class="chips"><span class="chip">'+r.t+' min</span>'+
   '<span class="chip '+dc+'">'+(r.diff||'EASY').charAt(0)+(r.diff||'EASY').slice(1).toLowerCase()+'</span>'+
   '<span class="chip p">'+pscale(cps(r))+' '+$$$(cps(r))+'</span>'+
   '<span class="chip t">'+bestFor(r)+'</span></div>'+
   '<div class="rcm"><div><b>'+Math.round(r.k)+'</b><span>kcal</span></div>'+
   '<div><b>'+Math.round(r.p)+'</b><span>prot</span></div>'+
   '<div><b>'+Math.round(r.c)+'</b><span>carb</span></div>'+
   '<div><b>'+Math.round(r.f)+'</b><span>fat</span></div></div></div></article>';
}
var flt={q:'',cat:'',tag:'',sort:'rec'};
function vMeals(){
  var ds=today(),d=dayLog(ds),tgt=dayTarget(S.who,d.workout),got=eaten(ds);
  var left={k:Math.max(150,tgt.kcal-got.kcal),p:Math.max(10,tgt.p-got.p)};
  var rec=rank(left,d.workout).slice(0,8);
  var est=estDayCost(tgt,S.costMode||'all');
  return '<div class="page"><div class="phead"><h1>Meals</h1>'+
   '<p>'+all().length+' recipes, all gluten-free. Average '+$$$(avgCost())+' a serving at the cheaper of Walmart or Costco.</p></div>'+

   '<div class="sec"><h2>What '+(S.who==='j'?'I':E(P().name))+' need today</h2>'+
   '<p class="sub">Adjusted for '+TRAIN[d.workout].n.toLowerCase()+'. Change it on the Training tab.</p>'+
   '<div class="grid g2"><div class="card pad">'+statRow(tgt)+
   '<div class="mrow" style="margin-top:16px"></div>'+
   bar('Calories',got.kcal,tgt.kcal,'pk')+bar('Protein',got.p,tgt.p,'pp')+
   bar('Carbs',got.c,tgt.c,'pc')+bar('Fat',got.f,tgt.f,'pf')+
   '<p class="sm muted" style="margin-top:12px">Left today: <b>'+Math.round(left.k)+' kcal</b>, <b>'+
   Math.round(left.p)+' g protein</b> &middot; spent '+$$$(got.cost)+'</p></div>'+

   '<div class="card pad"><h3 style="font-size:15px">What that costs</h3>'+
   '<p class="sub sm">Estimated food cost to actually hit today\'s numbers.</p>'+
   '<label class="f"><span>Base the estimate on</span><select id="costMode">'+
   opt([['all','Every recipe (average)'],['cheap','The cheapest 40 per calorie'],
        ['fav','My favourites only'],['logged','What we actually logged']],S.costMode||'all')+
   '</select></label>'+
   '<div class="stats"><div class="stat acc"><b>'+$$$(est.byKcal)+'</b><span>Today</span></div>'+
   (est.byProt?'<div class="stat"><b>'+$$$(est.byProt)+'</b><span>By protein</span></div>':'')+
   '<div class="stat"><b>'+$$$(est.byKcal*7)+'</b><span>Per week</span></div>'+
   '<div class="stat"><b>'+$$$(est.byKcal*30)+'</b><span>Per month</span></div></div>'+
   '<p class="xs muted" style="margin-top:10px">From '+E(est.src)+'. '+
   (est.byProt?'The two figures differ because protein is the expensive macro; if they are far apart the day is protein-heavy relative to its calories.':'')+
   '</p><div class="row" style="margin-top:12px">'+
   '<button class="b o s" id="bothCost">Cost for both of us</button></div>'+
   '<div id="bothOut"></div></div></div></div>'+

   '<div class="sec"><h2>For today</h2><p class="sub">Ranked for the session and what is left.</p>'+
   '<div class="grid g3">'+rec.map(rcard).join('')+'</div></div>'+

   (S.fav.length?'<div class="sec"><h2>Favourites</h2><div class="grid g3">'+
     S.fav.map(byId).filter(Boolean).map(rcard).join('')+'</div></div>':'')+

   '<div class="sec"><h2>Everything</h2><div class="card pad" style="margin-bottom:14px"><div class="fr">'+
   '<label class="f"><span>Search</span><input id="fq" placeholder="tofu, oats, burger..." value="'+E(flt.q)+'"></label>'+
   '<label class="f"><span>Category</span><select id="fcat">'+opt([['','All'],['Breakfast','Breakfast'],
     ['Lunch/Dinner','Mains'],['Snack','Snacks'],['Drink','Drinks'],['SDA Meat/Fish','Meat and fish'],
     ['My recipe','Mine']],flt.cat)+'</select></label>'+
   '<label class="f"><span>Best for</span><select id="ftag">'+opt([['','Any'],
     ['LEUCINE PRIORITY','High protein'],['CHEAT MEAL','Cheat meal'],['HEALTHY DESSERT','Dessert'],
     ['BUDGET FRIENDLY','Cheap'],['NO-COOK','No cooking'],['MEAL PREP','Meal prep'],
     ['HIGH FIBER','High fiber']],flt.tag)+'</select></label>'+
   '<label class="f"><span>Sort</span><select id="fsort">'+opt([['rec','Protein'],['cheap','Cheapest'],
     ['t','Fastest'],['k','Most calories'],['az','A to Z']],flt.sort)+'</select></label></div>'+
   '<div class="row"><button class="b o s" id="addOwn">Add my own recipe</button>'+
   '<span class="right sm muted" id="fcount"></span></div></div>'+
   '<div class="grid g3" id="fgrid"></div></div>'+
   explain()+'</div>';
}
/* Explanations live at the bottom, out of the way of the daily screens. */
function explain(){
  var p=P(), c=calc(p);
  function D(q,a){return '<details><summary>'+q+'</summary><div class="dc">'+a+'</div></details>';}
  return '<div class="sec"><h2>Why these numbers</h2>'+
   '<p class="sub">Open what is useful, ignore the rest. Everything here uses '+E(p.name)+"'s current figures.</p>"+
   D('Protein','<p>Nine of the twenty amino acids are essential, meaning food is the only source. '+
     'Muscle is built from them.</p><p><b>How much.</b> '+p.pf+' g per lb of bodyweight, so <b>'+c.p+
     ' g a day</b>. A plant-heavy diet gets pushed to the upper end because dairy and plant proteins '+
     'are less digestible and lower in leucine than meat.</p><p>Above about 1.5 g per lb the extra is '+
     'oxidised. Not harmful, just calories that would do more good as carbs.</p>')+
   D('Carbohydrate','<p>Training fuel, and what keeps muscle glycogen full. Full glycogen is why muscle '+
     'looks full rather than flat, which is a fast and real visual change.</p><p><b>How much.</b> '+
     'Whatever is left: (calories - protein x 4 - fat x 9) / 4 = <b>'+c.c+' g</b>.</p>'+
     '<p>Storage capacity is roughly 15 g per kg bodyweight, about 1,000 g, worth 4,000 calories and '+
     '3 kg of water. Refilling it is most of what the first two weeks of eating properly shows on the scale.</p>')+
   D('Fat','<p>Hormones, cell membranes, and absorbing vitamins A, D, E and K.</p>'+
     '<p><b>Floor.</b> 0.3 g per lb, so <b>'+Math.round(p.w*0.3)+' g</b>. Below that testosterone suffers. '+
     'The target here is 25% of calories, <b>'+c.f+' g</b>.</p><p>Fat is also the easiest way to add '+
     'calories without volume, at 9 kcal per gram against 4 for the others.</p>')+
   D('Fiber and water','<p>Fiber target is 14 g per 1,000 kcal, so <b>'+c.fib+' g</b>. Raising it fast '+
     'is unpleasant, so add about 5 g a week.</p><p>Water is 0.6 oz per lb plus training and altitude, '+
     'about <b>'+c.w+' oz</b>. Colorado is dry enough that thirst lags behind actual need.</p>')+
   D('Leucine','<p>The amino acid that flips the switch on muscle protein synthesis. Roughly 2.5 to 3 g '+
     'per feeding saturates the signal.</p><p>It is ignition, not fuel. Hitting leucine without adequate '+
     'total protein, calories and training does close to nothing, which is what the isolated BCAA '+
     'research found once total protein was controlled for.</p>')+
   D('How the calorie target is worked out','<p><b>1. RMR.</b> Mifflin-St Jeor: (10 x kg) + (6.25 x cm) '+
     '- (5 x age) + 5 for men, -161 for women. For '+E(p.name)+' that is <b>'+c.rmr+'</b>.</p>'+
     '<p><b>2. TDEE.</b> RMR x activity factor. At x'+p.act+' that is <b>'+c.tdee+'</b>.</p>'+
     '<p><b>3. Goal.</b> TDEE x '+p.goal+' = <b>'+c.kcal+'</b> a day.</p>'+
     '<p>Then the session adjustment on top, which the Training tab controls. Katch-McArdle gives '+
     c.katch+' for comparison; it is the better equation but only once body fat comes from a DEXA '+
     'rather than a scale.</p>')+
   D('Why the scale is not the whole story','<p>Daily swings of 2 to 4 lb are sodium, carb loading, '+
     'water retention after hard training, gut contents and sleep. Compare a seven-day average to the '+
     'average three weeks ago, never single days.</p><p>With celiac there is one more: an accidental '+
     'gluten exposure causes several days of inflammatory water retention that looks exactly like fat gain.</p>')+
   D('FFMI and the ceiling','<p>Fat-free mass index is lean mass in kg over height in metres squared, '+
     'height-corrected. '+E(p.name)+' is at <b>'+c.ffmi+'</b>, on '+c.lbm+' lb of lean mass. Around 25 is '+
     'the practical natural limit, so there is <b>'+(25-c.ffmi).toFixed(1)+' points</b> of room. That is '+
     'real, and worth several years of training.</p>')+
   D('Celiac: where the risk actually is','<p>Every recipe here is gluten-free by ingredient. The risk is '+
     'brands, not foods. Worth reading a label on: oats (cross-contaminated in harvest and milling, buy '+
     'certified), soy sauce (wheat, use tamari), buffalo sauce and curry paste (wheat thickeners), frozen '+
     'fries (flour anti-stick coating), protein powder (shared lines), and anything labelled panko.</p>'+
     '<p>Kitchen side: separate toaster, squeeze bottles rather than jars, no shared colander or wooden board.</p>')+
   D('Nutrients that run low for us','<p>Celiac damages the duodenum, where iron is absorbed, and a '+
     'vegetarian base limits iron, B12 and zinc on top of that. Highest risk five: iron, B12, vitamin D, '+
     'calcium, zinc.</p><p>Pair plant iron with vitamin C, which multiplies absorption several-fold. Do not '+
     'drink tea or coffee with an iron-heavy meal.</p><p>Worth testing yearly: ferritin, CBC, B12, '+
     '25-OH vitamin D, and tTG-IgA to confirm the diet is controlling the disease.</p>')+
   '</div>';
}
function avgCost(){var A=all();return A.reduce(function(a,r){return a+cps(r);},0)/A.length;}
function rank(left,tr){
  var t=TRAIN[tr]||TRAIN.rest;
  return all().map(function(r){var s=0;
    s-=Math.abs(r.k-left.k)/26; s+=Math.min(r.p,left.p*1.4)*1.9*t.p;
    s+=Math.min(r.c,140)*0.15*t.c; s+=(r.leu||0)*7;
    if(S.fav.indexOf(r.id)>=0)s+=14; return {r:r,s:s};})
    .sort(function(a,b){return b.s-a.s;}).map(function(o){return o.r;});
}
function applyFilters(){
  var g=$('#fgrid'); if(!g)return; var q=flt.q.toLowerCase();
  var L=all().filter(function(r){
    if(flt.cat&&r.cat!==flt.cat)return false;
    if(flt.tag&&r.tg.indexOf(flt.tag)<0)return false;
    if(q){var h=(r.n+' '+r.cat+' '+r.tg.join(' ')+' '+(r.ing||[]).map(function(i){
      var m=ING(i[1]);return m?m.n:'';}).join(' ')).toLowerCase();
      if(h.indexOf(q)<0)return false;}
    return true;});
  L.sort(function(a,b){var s=flt.sort;
    if(s==='cheap')return cps(a)-cps(b); if(s==='t')return a.t-b.t;
    if(s==='k')return b.k-a.k; if(s==='az')return a.n.localeCompare(b.n); return b.p-a.p;});
  g.innerHTML=L.length?L.map(rcard).join(''):'<p class="empty">Nothing matches.</p>';
  $('#fcount').textContent=L.length+' shown';
}

/* ============================ RECIPE DETAIL ============================ */
function vRecipe(id){
  var r=byId(id); if(!r)return '<div class="page"><p class="empty">Not found. <a href="#/meals">Back</a></p></div>';
  var sv=r.sv||1, f=S.fav.indexOf(id)>=0, ph=S.photos[id];
  var c=CATC[r.cat]||CATC['My recipe'];
  return '<div class="page">'+
   '<div class="row" style="margin:16px 0 14px"><button class="b o s" data-nav="meals">&larr; Meals</button>'+
   '<span class="chip">'+r.id+'</span></div>'+
   '<div class="dhero" style="background:linear-gradient(135deg,'+c[0]+','+c[1]+')">'+
   (ph?'<img src="'+ph+'" alt="">':'')+'<div class="scrim"></div><div class="in">'+
   '<div class="chips"><span class="chip">'+E(r.cat)+'</span><span class="chip">'+r.diff+'</span>'+
   '<span class="chip">'+r.t+' min</span><span class="chip">'+bestFor(r)+'</span></div>'+
   '<h1>'+E(r.n)+'</h1><div class="sm" style="color:rgba(255,255,255,.85)">makes '+
   '<span id="svHero">'+sv+'</span> &middot; '+$$$(cps(r))+' per serving, <span id="totHero">'+
   $$$(ctot(r))+'</span> total</div></div></div>'+
   '<div class="row" style="margin:16px 0"><button class="b" data-log="'+id+'">Log to today</button>'+
   '<button class="b o" data-fav="'+id+'">'+(f?'\u2605 Favourited':'\u2606 Favourite')+'</button>'+
   '<button class="b o" data-tolist="'+id+'">Add to a list</button>'+
   '<button class="b o" data-groc="'+id+'">Add to shopping</button>'+
   '<button class="b o" data-photo="'+id+'">'+(ph?'Change photo':'Add photo')+'</button>'+
   '<button class="b o" data-card="'+id+'">Save card</button></div>'+
   '<div class="sec"><div class="stats">'+
   '<div class="stat acc"><b>'+Math.round(r.k)+'</b><span>Calories</span></div>'+
   '<div class="stat"><b>'+Math.round(r.p)+'g</b><span>Protein</span></div>'+
   '<div class="stat"><b>'+Math.round(r.c)+'g</b><span>Carbs</span></div>'+
   '<div class="stat"><b>'+Math.round(r.f)+'g</b><span>Fat</span></div>'+
   '<div class="stat"><b>'+Math.round(r.fib||0)+'g</b><span>Fiber</span></div>'+
   '<div class="stat"><b>'+(r.leu||0).toFixed(1)+'g</b><span>Leucine</span></div></div>'+
   '<p class="muted sm" style="margin-top:9px">Every number above is <b>one plated serving</b>. '+
   'Making <span id="batchSv">'+sv+'</span> total: <span id="batchAll">'+Math.round(r.k*sv)+
   ' kcal, '+Math.round(r.p*sv)+' g protein, '+Math.round(r.c*sv)+' g carbs, '+
   Math.round(r.f*sv)+' g fat, '+$$$(ctot(r))+'</span>.</p></div>'+
   '<div class="grid g2"><div class="card pad">'+
   '<div class="spread" style="margin-bottom:10px"><h3 style="font-size:16px">Ingredients '+
   '<span class="muted sm" id="svLabel">for '+sv+'</span></h3></div>'+
   '<div class="row" style="margin-bottom:12px"><span class="muted sm">Scale</span>'+
   [0.5,1,1.5,2,3,4].map(function(x){return '<button class="pill'+(x===1?' on':'')+
     '" data-scale="'+x+'">'+x+'x</button>';}).join('')+'</div>'+
   '<ul class="ing" id="ingList"></ul>'+
   '<p class="xs muted" style="margin-top:10px">Prices come from the ingredient list. '+
   '<a href="#/shopping/ingredients">Edit an ingredient</a> and every recipe using it updates.</p></div>'+
   '<div class="card pad"><h3 style="font-size:16px;margin-bottom:12px">Method</h3><ol class="stp">'+
   (r.st||[]).map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ol></div></div>'+
   (r.prep?'<div class="note"><b>Note.</b> '+E(r.prep)+'</div>':'')+
   '<div class="grid g2" style="margin-top:14px">'+
   (r.storage?'<div class="card pad"><h4 class="lbl">Storage</h4><p class="sm" style="margin:8px 0 0">'+E(r.storage)+'</p></div>':'')+
   ((r.subs||[]).length?'<div class="card pad"><h4 class="lbl">Substitutions</h4><ul class="sm" style="margin:8px 0 0;padding-left:18px">'+
     r.subs.map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ul></div>':'')+
   ((r.vars||[]).length?'<div class="card pad"><h4 class="lbl">Variations</h4><ul class="sm" style="margin:8px 0 0;padding-left:18px">'+
     r.vars.map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ul></div>':'')+
   '</div></div>';
}
function drawIng(r,mult){
  var el=$('#ingList'); if(!el)return;
  el.innerHTML=(r.ing||[]).map(function(i){
    var meas=i[0],key=i[1],g=i[2]||0,q=ING(key);
    var nm=q?q.n:meas, pr=q?(g*mult/100)*best(q):0;
    var gs=g?Math.round(g*mult)+' g':'';
    var sub=(q&&meas)?' <span class="muted xs">('+E(meas)+')</span>':'';
    return '<li><b>'+gs+'</b><span>'+E(nm)+sub+'</span>'+
      (pr?'<span class="c">'+$$$(pr)+'</span>':'')+'</li>';}).join('');
  var sv=(r.sv||1)*mult, nice=function(x){return Math.round(x*10)/10;};
  var t=ctot(r)*mult;
  set('#svLabel','for '+nice(sv)+' serving'+(sv===1?'':'s'));
  set('#svHero',nice(sv)); set('#totHero',$$$(t)); set('#batchSv',nice(sv));
  var a=$('#batchAll'); if(a)a.innerHTML=Math.round(r.k*sv)+' kcal, '+Math.round(r.p*sv)+
    ' g protein, '+Math.round(r.c*sv)+' g carbs, '+Math.round(r.f*sv)+' g fat, '+$$$(t);
}
function set(sel,v){var e=$(sel); if(e)e.textContent=v;}

/* ============================ SHOPPING ============================ */
function shopLists(){return S.shop.lists;}
function curList(){var L=shopLists(); if(!L[S.shop.active]){var k=Object.keys(L)[0];
  if(!k){L['Weekly shop']={cat:'Groceries',fav:true,items:[]};k='Weekly shop';}
  S.shop.active=k;} return L[S.shop.active];}
function vShopping(sub){
  if(sub==='ingredients') return vIngredients();
  var L=shopLists(), names=Object.keys(L), cur=curList(), items=cur.items||[];
  var byA={}; items.forEach(function(it,i){(byA[it.aisle]=byA[it.aisle]||[]).push([it,i]);});
  var order=AISLES.map(function(a){return a[0];}).concat(['Other']);
  var tot=items.reduce(function(a,i){return a+(i.done?0:i.price*i.qty);},0);
  var got=items.reduce(function(a,i){return a+(i.done?i.price*i.qty:0);},0);
  var cats={}; names.forEach(function(n){var c=L[n].cat||'Lists';(cats[c]=cats[c]||[]).push(n);});
  return '<div class="page"><div class="phead"><h1>Shopping</h1>'+
   '<p>Every item priced at whichever of Walmart Fort Collins or Costco Timnath is cheaper for that item.</p></div>'+

   '<div class="sec"><div class="spread"><h2>Lists</h2>'+
   '<div class="row"><button class="b o s" id="newList">New list</button>'+
   '<button class="b o s" data-nav="shopping/ingredients">Ingredient list</button></div></div>'+
   Object.keys(cats).sort().map(function(c){
     return '<div style="margin:10px 0"><div class="lbl" style="margin-bottom:7px">'+E(c)+'</div>'+
     '<div class="row">'+cats[c].map(function(n){
       return '<button class="pill'+(n===S.shop.active?' on':'')+'" data-list="'+E(n)+'">'+
       (L[n].fav?'\u2605 ':'')+E(n)+' <span class="muted">'+L[n].items.length+'</span></button>';
     }).join('')+'</div></div>';}).join('')+'</div>'+

   '<div class="sec"><div class="spread"><h2>'+E(S.shop.active)+'</h2>'+
   '<div class="row"><button class="b o s" id="listFav">'+(cur.fav?'\u2605 Favourite':'\u2606 Favourite')+'</button>'+
   '<button class="b o s" id="listRename">Rename</button>'+
   '<button class="b o s" id="listDup">Duplicate</button>'+
   '<button class="b o s dz" id="listDel">Delete</button></div></div>'+
   '<div class="stats" style="margin:12px 0">'+
   '<div class="stat acc"><b>'+M(tot)+'</b><span>Still to buy</span></div>'+
   '<div class="stat"><b>'+items.length+'</b><span>Items</span></div>'+
   '<div class="stat"><b>'+M(got)+'</b><span>In the cart</span></div>'+
   '<div class="stat"><b>'+Object.keys(byA).length+'</b><span>Aisles</span></div></div>'+
   '<div class="row" style="margin-bottom:14px">'+
   '<button class="b" id="gAdd">Add item</button>'+
   '<button class="b o" id="gRecipe">Add from a recipe</button>'+
   '<button class="b o" id="gTxt">Checklist</button>'+
   '<button class="b o" id="gCsv">CSV</button>'+
   '<button class="b o" id="gSave">Save list to file</button>'+
   '<button class="b o" id="gLoad">Load list</button>'+
   '<button class="b o dz right" id="gClear">Clear checked</button></div>'+
   (items.length? order.filter(function(a){return byA[a];}).map(function(a){
     var L2=byA[a], st=L2.reduce(function(x,p){return x+(p[0].done?0:p[0].price*p[0].qty);},0);
     return '<div class="card" style="margin-bottom:12px;overflow:hidden">'+
      '<div class="aisle">'+E(a)+'<span>'+M(st)+'</span></div>'+
      L2.map(function(p){var it=p[0],i=p[1];
        return '<div class="gitem'+(it.done?' done':'')+'">'+
        '<input type="checkbox" data-gt="'+i+'"'+(it.done?' checked':'')+'>'+
        '<div style="flex:1;min-width:0"><div class="gn">'+E(it.name)+'</div>'+
        '<div class="gq">'+(it.qty>1?it.qty+' x ':'')+E(it.note||'')+
        (it.key?' &middot; '+E(bestStore(ING(it.key))):'')+'</div></div>'+
        '<span class="gp">'+$$$(it.price*it.qty)+'</span>'+
        '<button class="b o s" data-ge="'+i+'">Edit</button>'+
        '<button class="x" data-gd="'+i+'">&times;</button></div>';}).join('')+'</div>';}).join('')
    : '<div class="empty"><p>Nothing on this list.</p><p class="sm">Add an item, or open a recipe and hit Add to shopping.</p></div>')+
   '</div></div>';
}
function vIngredients(){
  var keys=allIngKeys().sort(function(a,b){return ING(a).n.localeCompare(ING(b).n);});
  var edited=Object.keys(S.ingOv).length;
  return '<div class="page"><div class="phead"><h1>Ingredient list</h1>'+
   '<p>The master list every recipe price comes from. Edit a price here and all '+
   all().length+' recipes recost instantly. '+edited+' edited or added so far.</p></div>'+
   '<div class="row" style="margin-bottom:14px">'+
   '<button class="b" id="ingNew">Add an ingredient</button>'+
   '<button class="b o" data-nav="shopping">&larr; Back to lists</button>'+
   '<button class="b o" id="ingCsv">Export list</button>'+
   '<input class="right" id="ingQ" placeholder="Search "+keys.length+" ingredients" '+
   'style="padding:10px 13px;border:1px solid var(--line-2);border-radius:9px;min-width:220px">'+
   '</div><div class="tw"><table><thead><tr><th>Ingredient</th><th>Aisle</th>'+
   '<th>Walmart /100g</th><th>Costco /100g</th><th>Best</th><th>Used in</th><th></th></tr></thead>'+
   '<tbody id="ingBody"></tbody></table></div></div>';
}
function ingUsage(k){var n=0;all().forEach(function(r){(r.ing||[]).forEach(function(i){
  if(i[1]===k)n++;});});return n;}
function drawIngTable(q){
  var b=$('#ingBody'); if(!b)return; q=(q||'').toLowerCase();
  var keys=allIngKeys().filter(function(k){return ING(k).n.toLowerCase().indexOf(q)>=0;})
    .sort(function(a,b2){return ING(a).n.localeCompare(ING(b2).n);});
  b.innerHTML=keys.slice(0,400).map(function(k){var g=ING(k),ov=S.ingOv[k];
    return '<tr><td><b>'+E(g.n)+'</b>'+(ov?' <span class="chip t">edited</span>':'')+'</td>'+
    '<td class="sm muted">'+E(g.a||'Other')+'</td>'+
    '<td>'+(g.w!=null?$$$(g.w):'-')+'</td><td>'+(g.c!=null&&g.c>0?$$$(g.c):'-')+'</td>'+
    '<td><b>'+$$$(best(g))+'</b> <span class="xs muted">'+bestStore(g)+'</span></td>'+
    '<td class="sm">'+ingUsage(k)+'</td>'+
    '<td><button class="b o s" data-ie="'+k+'">Edit</button></td></tr>';}).join('');
}
function ingEditor(k){
  var g=k?ING(k):{n:'',a:'Other',w:null,c:null};
  var isNew=!k;
  var body='<div class="fr">'+
   '<label class="f"><span>Name</span><input id="ieN" value="'+E(g.n)+'"></label>'+
   '<label class="f"><span>Aisle</span><select id="ieA">'+
   AISLES.map(function(a){return a[0];}).concat(['Other']).map(function(a){
     return '<option'+(a===(g.a||'Other')?' selected':'')+'>'+E(a)+'</option>';}).join('')+
   '</select></label></div><div class="fr">'+
   '<label class="f"><span>Walmart $ per 100 g</span><input id="ieW" type="number" step="0.01" value="'+(g.w!=null?g.w:'')+'"></label>'+
   '<label class="f"><span>Costco $ per 100 g</span><input id="ieC" type="number" step="0.01" value="'+(g.c!=null&&g.c>0?g.c:'')+'"></label>'+
   '</div>'+
   (isNew?'<div class="fr"><label class="f"><span>kcal /100g</span><input id="ieK" type="number"></label>'+
     '<label class="f"><span>Protein</span><input id="ieP" type="number" step="0.1"></label>'+
     '<label class="f"><span>Carbs</span><input id="ieCb" type="number" step="0.1"></label>'+
     '<label class="f"><span>Fat</span><input id="ieF" type="number" step="0.1"></label></div>':'')+
   '<p class="sm muted">Leave a price blank if that store does not stock a sensible size. '+
   'The cheaper of the two is always what gets used.</p>'+
   (k?'<p class="sm muted">Used in <b>'+ingUsage(k)+'</b> recipes. Changing the price updates all of them.</p>':'');
  var m=modal(isNew?'Add an ingredient':'Edit '+g.n,body,
    (k&&S.ingOv[k]?'<button class="b o dz" id="ieReset">Reset to default</button>':'')+
    '<button class="b o" data-x>Cancel</button><button class="b" id="ieSave">Save</button>');
  $$('[data-x]',m).forEach(function(b){b.onclick=function(){m.remove();};});
  var rs=$('#ieReset',m); if(rs)rs.onclick=function(){delete S.ingOv[k];save();m.remove();route();toast('Reset');};
  $('#ieSave',m).onclick=function(){
    var nm=$('#ieN',m).value.trim(); if(!nm){toast('Needs a name');return;}
    var key=k||('u_'+nm.toLowerCase().replace(/[^a-z0-9]+/g,'_').slice(0,28));
    var w=$('#ieW',m).value, c=$('#ieC',m).value;
    var o=S.ingOv[key]||{};
    o.n=nm; o.a=$('#ieA',m).value;
    o.w=w===''?null:num(w); o.c=c===''?null:num(c);
    if(isNew){o.k=num($('#ieK',m).value);o.p=num($('#ieP',m).value);
      o.cb=num($('#ieCb',m).value);o.f=num($('#ieF',m).value);o.userAdded=true;}
    S.ingOv[key]=o; save(); m.remove(); route();
    toast(isNew?'Ingredient added':'Updated. '+ingUsage(key)+' recipes recosted.');
  };
}

/* ============================ TRAINING ============================ */
var exFlt={q:'',mg:'',eq:'',hero:false};
function vTraining(sub){
  if(sub==='exercises') return vExercises();
  var ds=today(), d=dayLog(ds), t=dayTarget(S.who,d.workout);
  var wk=[]; for(var i=6;i>=0;i--){var dd=new Date();dd.setDate(dd.getDate()-i);
    var k=dd.getFullYear()+'-'+p2(dd.getMonth()+1)+'-'+p2(dd.getDate());
    wk.push([k,S.days[k]?S.days[k].workout:null,dd]);}
  var trained=wk.filter(function(x){return x[1];}).length;
  return '<div class="page"><div class="phead"><h1>Training</h1>'+
   '<p>'+EX.length+' exercises, '+SESS.length+' sessions, and what each session type does to the day\'s macros.</p></div>'+

   '<div class="sec"><div class="grid g2">'+
   '<div class="card pad"><h3 style="font-size:16px;margin-bottom:14px">Today</h3>'+
   '<label class="f"><span>Session</span><select id="tWorkout">'+
   Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
   '</select></label>'+
   '<label class="f"><span>Notes, lifts, PRs</span><textarea id="tNotes" rows="3" placeholder="Weighted pull-up 3x5 +25 lb">'+E(d.notes||'')+'</textarea></label>'+
   '<label class="f"><span>Bodyweight this morning</span><input id="tW" type="number" step="0.1" value="'+(d.w||'')+'"></label>'+
   '<button class="b" id="tSave">Save</button>'+
   '<p class="xs muted" style="margin-top:10px">Logged as <b>'+E(ME())+'</b>. This appears on the schedule automatically.</p></div>'+
   '<div class="card pad"><h3 style="font-size:16px;margin-bottom:12px">What the day needs</h3>'+
   statRow(t)+'<div class="note" style="margin-bottom:0">'+E(TRAIN[d.workout].why)+'</div></div>'+
   '</div></div>'+

   '<div class="sec"><h2>The week</h2><p class="sub">'+trained+' of the last 7 days trained.</p>'+
   '<div class="card pad"><div class="row" style="gap:6px">'+
   wk.map(function(x){
     var on=x[1]&&x[1]!=='rest';
     return '<div style="flex:1;min-width:64px;text-align:center;padding:12px 6px;border-radius:var(--r-s);'+
     'border:1px solid '+(on?'var(--sage)':'var(--line)')+';background:'+(on?'rgba(127,168,127,.10)':'var(--panel-2)')+'">'+
     '<div class="lbl">'+DOW[x[2].getDay()]+'</div>'+
     '<div class="mono" style="font-size:15px;font-weight:700;margin-top:6px;color:'+(on?'var(--sage)':'var(--ink-4)')+'">'+
     x[2].getDate()+'</div>'+
     '<div class="xs muted" style="margin-top:4px">'+(x[1]?TRAIN[x[1]].n.split(/[ ,]/)[0]:'-')+'</div></div>';
   }).join('')+'</div></div></div>'+

   '<div class="sec"><div class="spread"><h2>Sessions</h2>'+
   '<button class="b o s" data-nav="training/exercises">Exercise database &rarr;</button></div>'+
   '<p class="sub">From the printable guide. Open one for the full list.</p>'+
   '<div class="grid g3">'+SESS.map(function(x,i){
     var kind=/skill/i.test(x.name)?'Skill':/upper/i.test(x.name)?'Upper':/lower/i.test(x.name)?'Lower':
              /fallback|full/i.test(x.name)?'Full body':'Accessory';
     return '<button class="card pad" data-sess="'+i+'" style="text-align:left;cursor:pointer;border-color:var(--line)">'+
     '<div class="lbl" style="color:var(--brass)">'+kind+'</div>'+
     '<div style="font-family:var(--f-disp);font-size:17px;font-weight:600;margin:8px 0 6px;color:var(--ink)">'+
     E(x.name)+'</div>'+
     '<div class="row" style="gap:5px"><span class="chip">'+x.ex.length+' exercises</span>'+
     '<span class="chip">'+Math.round(x.ex.length*7)+' min</span></div></button>';}).join('')+
   '</div></div>'+

   '<div class="sec"><h2>Macro shift by session</h2>'+
   '<p class="sub">Carbs swing roughly 50% across session types, protein about 8%. Glycogen is local '+
   'and gets emptied by the session; protein demand is a daily total.</p>'+
   '<div class="tw"><table><thead><tr><th>Session</th><th class="num">Kcal</th><th class="num">Protein</th>'+
   '<th class="num">Carbs</th><th class="num">Fat</th><th>Leads with</th></tr></thead><tbody>'+
   Object.keys(TRAIN).map(function(k){var tt=dayTarget(S.who,k),T2=TRAIN[k];
     var lead=T2.c>=1.15?'Carbs':T2.p>=1.06?'Protein':T2.k<1?'Volume and fiber':'Balance';
     return '<tr'+(d.workout===k?' style="background:var(--panel-2)"':'')+'>'+
     '<td><b>'+T2.n+'</b>'+(d.workout===k?' <span class="chip t">today</span>':'')+'</td>'+
     '<td class="num">'+N(tt.kcal)+'</td><td class="num">'+tt.p+' g</td>'+
     '<td class="num">'+tt.c+' g</td><td class="num">'+tt.f+' g</td>'+
     '<td class="sm muted">'+lead+'</td></tr>';}).join('')+
   '</tbody></table></div></div></div>';
}
function vExercises(){
  var mgs=[];EX.forEach(function(e){if(mgs.indexOf(e.mg)<0)mgs.push(e.mg);});mgs.sort();
  return '<div class="page"><div class="phead"><h1>Exercise database</h1>'+
   '<p>'+EX.length+' exercises with technique, mistakes, progressions and regressions.</p></div>'+
   '<div class="card pad" style="margin-bottom:14px"><div class="fr">'+
   '<label class="f"><span>Search</span><input id="exq" placeholder="pull-up, planche..." value="'+E(exFlt.q)+'"></label>'+
   '<label class="f"><span>Muscle group</span><select id="exmg">'+
   opt([['','All']].concat(mgs.map(function(m){return [m,m];})),exFlt.mg)+'</select></label>'+
   '<label class="f"><span>Equipment</span><select id="exeq">'+
   opt([['','Anything'],['Bodyweight','Bodyweight'],['Dumbbell','Dumbbells'],['Pull-up','Pull-up bar'],
        ['Dip','Dip station'],['Parallettes','Parallettes'],['vest','Weighted vest'],
        ['Band','Bands'],['Rings','Rings']],exFlt.eq)+'</select></label></div>'+
   '<div class="row"><button class="pill'+(exFlt.hero?' on':'')+'" id="exhero">Hero lifts only</button>'+
   '<span class="right sm muted" id="excount"></span></div></div>'+
   '<div id="exList"></div><button class="b o" data-nav="training" style="margin-top:16px">&larr; Training</button></div>';
}
function drawEx(){
  var el=$('#exList'); if(!el)return; var q=exFlt.q.toLowerCase();
  var L=EX.filter(function(e){
    if(exFlt.mg&&e.mg!==exFlt.mg)return false;
    if(exFlt.hero&&!e.hero)return false;
    if(exFlt.eq&&e.eq.toLowerCase().indexOf(exFlt.eq.toLowerCase())<0)return false;
    if(q&&(e.n+' '+e.pri+' '+e.tags).toLowerCase().indexOf(q)<0)return false;
    return true;});
  $('#excount').textContent=L.length+' exercises';
  el.innerHTML=L.slice(0,120).map(function(e){
    return '<details><summary>'+E(e.n)+
    ' <span class="chip">'+E(e.mg)+'</span>'+(e.hero?' <span class="chip t">Hero</span>':'')+
    '</summary><div class="dc">'+
    '<div class="chips"><span class="chip">'+E(e.eq)+'</span><span class="chip">'+E(e.df)+'</span>'+
    '<span class="chip">'+E(e.sets)+' x '+E(e.reps)+'</span><span class="chip">RIR '+E(e.rir)+'</span>'+
    '<span class="chip">'+E(e.rest)+'</span></div>'+
    '<p><b>Technique.</b> '+E(e.tech)+'</p>'+
    (e.mist?'<p><b>Common mistakes.</b> '+E(e.mist)+'</p>':'')+
    (e.prog?'<p><b>Progress it.</b> '+E(e.prog)+'</p>':'')+
    (e.reg?'<p><b>Regress it.</b> '+E(e.reg)+'</p>':'')+
    (e.use?'<p><b>Best use.</b> '+E(e.use)+'</p>':'')+
    '<p class="sm muted">Primary: '+E(e.pri)+(e.sec?'. Secondary: '+E(e.sec):'')+'</p>'+
    '</div></details>';}).join('');
}
function sessModal(i){
  var s=SESS[i]; if(!s)return;
  var body='<div class="tw"><table><thead><tr><th>Exercise</th><th>Sets</th><th>Reps</th><th>Note</th></tr></thead><tbody>'+
   s.ex.map(function(x){return '<tr><td><b>'+E(x.n)+'</b></td><td>'+E(x.sets)+'</td><td>'+E(x.reps)+
     '</td><td class="sm muted">'+E(x.note)+'</td></tr>';}).join('')+'</tbody></table></div>';
  modal(s.name,body,'<button class="b" data-x>Close</button>').querySelectorAll('[data-x]')
    .forEach(function(b){b.onclick=function(){b.closest('.mask').remove();};});
}

/* ============================ FINANCIAL ============================ */
function finIncome(who,mode){
  return S.fin.jobs.filter(function(j){return who==='both'||j.who===who||j.who==='Both';})
    .reduce(function(a,j){return a+(j[mode]||0);},0);
}
function finCost(mode,path){
  return S.fin.costs.filter(function(c){
    if(c.section==='Housing (rent)') return path!=='buy';
    if(c.section==='Housing (buy)') return path==='buy';
    return true;}).reduce(function(a,c){return a+(c[mode]||0);},0);
}
function shiftsFor(who,from){
  return S.fin.shifts.filter(function(s){
    var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
    if(who&&j&&j.who!==who&&j.who!=='Both')return false;
    if(from&&s.date<from)return false; return true;});
}
function vFinancial(sub){
  if(sub==='purchases') return vPurchases();
  if(sub==='actual') return vActual();
  var mode=S.fin.costMode||'real', path=S.fin.path||'rent';
  var inc=finIncome('both',mode), cost=finCost(mode,path), gap=inc-cost;
  var byS={}; S.fin.costs.forEach(function(c){
    if(c.section==='Housing (rent)'&&path==='buy')return;
    if(c.section==='Housing (buy)'&&path!=='buy')return;
    byS[c.section]=(byS[c.section]||0)+(c[mode]||0);});
  var names=Object.keys(S.fin.scenarios||{});
  var act=S.fin.activeScenario, dirty=scenDirty();
  var cmp='';
  if(names.length){
    cmp='<div class="sec"><h2>Scenarios side by side</h2>'+
      '<p class="sub">Each one stores every income and cost line as it was when saved.</p>'+
      '<div class="tw"><table><thead><tr><th>Scenario</th><th>Basis</th><th>Housing</th>'+
      '<th class="num">Income</th><th class="num">Costs</th><th class="num">Monthly</th>'+
      '<th class="num">Yearly</th><th></th></tr></thead><tbody>'+
      names.map(function(n){var sc=S.fin.scenarios[n];
        var si=sc.jobs.reduce(function(a,j){return a+(j[sc.mode]||0);},0);
        var scst=sc.costs.filter(function(c){
          if(c.section==='Housing (rent)')return sc.path!=='buy';
          if(c.section==='Housing (buy)')return sc.path==='buy';return true;})
          .reduce(function(a,c){return a+(c[sc.mode]||0);},0);
        var g=si-scst;
        return '<tr'+(n===act?' style="background:var(--panel-2)"':'')+'>'+
        '<td><b>'+E(n)+'</b>'+(n===act?' <span class="chip t">open</span>':'')+'</td>'+
        '<td class="sm muted">'+E(sc.mode)+'</td><td class="sm muted">'+E(sc.path)+'</td>'+
        '<td class="num">'+M(si)+'</td><td class="num">'+M(scst)+'</td>'+
        '<td class="num" style="color:'+(g>=0?'var(--sage)':'var(--clay)')+'"><b>'+M(g)+'</b></td>'+
        '<td class="num">'+M(g*12)+'</td>'+
        '<td><button class="b o s" data-scload="'+E(n)+'">Open</button> '+
        '<button class="x" data-scdel="'+E(n)+'">&times;</button></td></tr>';}).join('')+
      '</tbody></table></div></div>';
  }
  return '<div class="page"><div class="phead"><h1>Financial</h1>'+
   '<p>Every income and cost line, saved into scenarios you can compare. Nothing overwrites a saved '+
   'scenario until you press Save.</p></div>'+

   '<div class="sec"><div class="spread"><h2>'+(act?E(act):'Working numbers')+'</h2>'+
   '<div class="row">'+(dirty?'<span class="dirty">Unsaved changes</span>':'')+
   '<button class="b o s" data-nav="financial/actual">Actual earnings</button>'+
   '<button class="b o s" data-nav="financial/purchases">Big purchases</button></div></div>'+

   '<div class="card pad"><div class="fr">'+
   '<label class="f"><span>Which estimate column</span><select id="finMode">'+
   opt([['low','Lean (low)'],['real','Realistic'],['high','Good month (high)'],
        ['actual','Actual / researched']],mode)+'</select></label>'+
   '<label class="f"><span>Housing path</span><select id="finPath">'+
   opt([['rent','Renting'],['buy','Buying']],path)+'</select></label>'+
   '<label class="f"><span>Open a scenario</span><select id="finScen">'+
   opt([['','-- working numbers --']].concat(names.map(function(n){return [n,n];})),act||'')+
   '</select></label></div>'+
   '<div class="row">'+
   '<button class="b" id="scenNew">New scenario</button>'+
   (act?'<button class="b'+(dirty?'':' o')+'" id="scenUpdate">Save to "'+E(act)+'"</button>'+
        '<button class="b o" id="scenRevert">Revert</button>':'')+
   '<button class="b o" id="scenSaveAs">Save as new</button>'+
   '</div>'+
   (dirty?'<div class="note warn" style="margin-bottom:0"><b>Not saved.</b> '+
     'Changes to income or cost lines are live on screen but "'+E(act)+'" still holds the old figures. '+
     'Save to keep them, or Revert to throw them away.</div>':'')+
   '</div>'+

   '<div class="stats" style="margin-top:14px">'+
   '<div class="stat"><b>'+M(inc)+'</b><span>Income / mo</span></div>'+
   '<div class="stat"><b>'+M(cost)+'</b><span>Costs / mo</span></div>'+
   '<div class="stat '+(gap>=0?'good':'bad')+'"><b>'+M(gap)+'</b><span>'+
   (gap>=0?'Surplus':'Shortfall')+'</span></div>'+
   '<div class="stat"><b>'+M(gap*12)+'</b><span>Per year</span></div></div>'+
   (gap<0?'<div class="note warn"><b>The gap is real.</b> At these numbers we are '+M(-gap)+
     ' short every month. Income has to rise by that, or costs have to fall.</div>':'')+
   '</div>'+cmp+

   '<div class="sec"><h2>Where the money goes</h2><div class="grid g2">'+
   '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">Costs by section</h3>'+
   Object.keys(byS).sort(function(a,b){return byS[b]-byS[a];}).map(function(k){
     var pct=cost?byS[k]/cost*100:0;
     return '<div class="mrow"><div class="spread"><span>'+E(k)+'</span><em>'+M(byS[k])+'</em></div>'+
     '<div class="bar"><i class="pk" style="width:'+pct+'%"></i></div></div>';}).join('')+'</div>'+
   '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">Income by person</h3>'+
   ['Jaron','Aaliyah','Both'].map(function(w){
     var v=S.fin.jobs.filter(function(j){return j.who===w;})
       .reduce(function(a,j){return a+(j[mode]||0);},0);
     if(!v)return ''; var pct=inc?v/inc*100:0;
     return '<div class="mrow"><div class="spread"><span>'+E(w==='Both'?'Shared / gig':w)+'</span>'+
     '<em>'+M(v)+'</em></div><div class="bar"><i class="pp" style="width:'+pct+'%"></i></div></div>';
   }).join('')+'<button class="b o s" id="jobAdd" style="margin-top:10px">Add income</button></div>'+
   '</div></div>'+

   '<div class="sec"><div class="spread"><h2>Income lines</h2>'+
   '<button class="b o s" id="jobAdd2">Add</button></div><div class="tw"><table>'+
   '<thead><tr><th>Who</th><th>Name</th><th>Employer</th><th class="num">Low</th>'+
   '<th class="num">Realistic</th><th class="num">High</th><th class="num">Actual</th><th></th></tr></thead><tbody>'+
   S.fin.jobs.map(function(j){
     return '<tr><td><span class="chip">'+E(j.who)+'</span></td><td><b>'+E(j.name)+'</b>'+
     (j.rate?'<div class="xs muted">'+$$$(j.rate)+'/hr</div>':'')+'</td>'+
     '<td class="sm muted">'+E(j.employer||'')+'</td>'+
     '<td class="num">'+M(j.low)+'</td><td class="num"><b>'+M(j.real)+'</b></td>'+
     '<td class="num">'+M(j.high)+'</td>'+
     '<td class="num">'+(j.actual?M(j.actual):'<span class="muted">-</span>')+'</td>'+
     '<td><button class="b o s" data-jobe="'+j.id+'">Edit</button></td></tr>';}).join('')+
   '<tr style="background:var(--panel-2)"><td colspan="3"><b>Total</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','low'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','real'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','high'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','actual'))+'</b></td><td></td></tr>'+
   '</tbody></table></div></div>'+

   '<div class="sec"><div class="spread"><h2>Cost lines</h2>'+
   '<button class="b o s" id="costAdd">Add</button></div><div class="tw"><table>'+
   '<thead><tr><th>Section</th><th>Cost</th><th>Who</th><th class="num">Low</th>'+
   '<th class="num">Realistic</th><th class="num">High</th><th class="num">Actual</th><th></th></tr></thead><tbody>'+
   S.fin.costs.map(function(c){return '<tr><td class="sm muted">'+E(c.section)+'</td>'+
     '<td><b>'+E(c.name)+'</b></td><td><span class="chip">'+E(c.who)+'</span></td>'+
     '<td class="num">'+M(c.low)+'</td><td class="num"><b>'+M(c.real)+'</b></td>'+
     '<td class="num">'+M(c.high)+'</td>'+
     '<td class="num">'+(c.actual?M(c.actual):'<span class="muted">-</span>')+'</td>'+
     '<td><button class="b o s" data-coste="'+c.id+'">Edit</button></td></tr>';}).join('')+
   '<tr style="background:var(--panel-2)"><td colspan="3"><b>Total</b></td>'+
   '<td class="num"><b>'+M(finCost('low',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('real',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('high',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('actual',path))+'</b></td><td></td></tr>'+
   '</tbody></table></div></div></div>';
}
function vActual(){
  var from=new Date();from.setDate(from.getDate()-90);
  var f=from.getFullYear()+'-'+p2(from.getMonth()+1)+'-'+p2(from.getDate());
  var sh=S.fin.shifts.slice().sort(function(a,b){return b.date<a.date?-1:1;});
  function tot(who,field){return shiftsFor(who,f).reduce(function(a,s){return a+(s[field]||0);},0);}
  var jH=tot('Jaron','hours'),aH=tot('Aaliyah','hours');
  var jG=tot('Jaron','gross'),aG=tot('Aaliyah','gross');
  var jN=tot('Jaron','net'),aN=tot('Aaliyah','net');
  var eff=function(g,h){return h>0?g/h:0;};
  var months=Math.max(1,90/30.4);
  return '<div class="page"><div class="phead"><h1>Actual earnings</h1>'+
   '<p>Log real shifts. Averages, effective hourly and after-tax rate all come from what actually landed, not the plan.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b" id="shAdd">Log a shift</button>'+
   '<button class="b o" id="shCsv">Export shifts</button>'+
   '<button class="b o" data-nav="financial">&larr; Plan</button></div>'+
   '<div class="sec"><h2>Last 90 days</h2><div class="grid g2">'+
   ['Jaron','Aaliyah'].map(function(w){
     var h=w==='Jaron'?jH:aH,g=w==='Jaron'?jG:aG,n=w==='Jaron'?jN:aN;
     return '<div class="card pad"><h3 style="font-size:16px;margin-bottom:12px">'+w+'</h3>'+
     '<div class="stats"><div class="stat acc"><b>'+M(n/months)+'</b><span>Net / mo</span></div>'+
     '<div class="stat"><b>'+h.toFixed(0)+'</b><span>Hours</span></div>'+
     '<div class="stat"><b>'+$$$(eff(g,h))+'</b><span>Gross / hr</span></div>'+
     '<div class="stat"><b>'+$$$(eff(n,h))+'</b><span>Net / hr</span></div></div>'+
     '<p class="sm muted" style="margin-top:10px">'+(g>0?'Take-home is '+Math.round(n/g*100)+'% of gross.':'No shifts logged yet.')+'</p>'+
     '</div>';}).join('')+'</div>'+
   '<div class="note" style="margin-top:14px"><b>Auto scenario.</b> '+
   'Combined that is <b>'+M((jN+aN)/months)+'</b> net a month from real data, against a plan of <b>'+
   M(finIncome('both','real'))+'</b>. '+
   '<button class="b o s" id="scenFromActual" style="margin-left:8px">Save that as a scenario</button></div></div>'+
   '<div class="sec"><h2>Shifts</h2>'+(sh.length?'<div class="tw"><table>'+
   '<thead><tr><th>Date</th><th>Job</th><th>Hours</th><th>Gross</th><th>Net</th><th>Note</th><th></th></tr></thead><tbody>'+
   sh.slice(0,80).map(function(s){var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
     return '<tr><td>'+shortD(s.date)+'</td><td>'+E(j?j.name:'?')+'</td><td>'+s.hours+'</td>'+
     '<td>'+M(s.gross)+'</td><td>'+M(s.net)+'</td><td class="sm muted">'+E(s.note||'')+'</td>'+
     '<td><button class="x" data-shd="'+s.id+'">&times;</button></td></tr>';}).join('')+
   '</tbody></table></div>':'<div class="empty">No shifts logged.</div>')+'</div></div>';
}
function vPurchases(){
  var P_=S.fin.purchases||{}, names=Object.keys(P_);
  return '<div class="page"><div class="phead"><h1>Big purchases</h1>'+
   '<p>Houses, cars, anything worth comparing side by side before committing.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b" id="bpNew">New list</button>'+
   '<button class="b o" data-nav="financial">&larr; Financial</button></div>'+
   (names.length?names.map(function(n){var L=P_[n];
     return '<div class="sec"><div class="spread"><h2>'+E(n)+' <span class="chip">'+E(L.cat||'')+'</span></h2>'+
     '<div class="row"><button class="b o s" data-bpadd="'+E(n)+'">Add item</button>'+
     '<button class="b o s dz" data-bpdel="'+E(n)+'">Delete list</button></div></div>'+
     (L.items.length?'<div class="grid g3">'+L.items.map(function(it,i){
       return '<div class="card pad"><div class="spread"><b style="font-family:var(--fd);font-size:16px">'+E(it.name)+'</b>'+
       '<button class="x" data-bpi="'+E(n)+'|'+i+'">&times;</button></div>'+
       '<div style="font-size:22px;font-weight:700;color:var(--forest);margin:6px 0">'+M(it.price)+'</div>'+
       (it.fields?Object.keys(it.fields).map(function(k){
         return '<div class="spread sm" style="border-bottom:1px solid var(--line);padding:5px 0">'+
         '<span class="muted">'+E(k)+'</span><b>'+E(it.fields[k])+'</b></div>';}).join(''):'')+
       (it.notes?'<p class="sm muted" style="margin-top:8px">'+E(it.notes)+'</p>':'')+
       (it.link?'<a class="b o s" href="'+E(it.link)+'" target="_blank" rel="noopener" style="margin-top:10px">Open link</a>':'')+
       '</div>';}).join('')+'</div>':'<div class="empty sm">Nothing on this list yet.</div>')+'</div>';}).join('')
    :'<div class="empty"><p>No lists yet.</p><p class="sm">Make one for apartments, or cars, or anything you are comparing.</p></div>')+
   '</div>';
}

/* ============================ SCHEDULE ============================ */
var DOW=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
var calY=new Date().getFullYear(), calM=new Date().getMonth(), calSel=today();
function dayTimeline(ds){
  var d=dayLog(ds), out=[];
  (d.sched||[]).forEach(function(e,i){
    out.push({t:e.from||'',kind:'e',who:e.who,title:e.what,
      sub:[(e.from?e.from+(e.to?' - '+e.to:''):''),e.where||''].filter(Boolean).join('  \u00B7  '),
      rm:i});});
  if(d.workout&&d.workout!=='rest')
    out.push({t:d.trainAt||'17:30',kind:'w',who:d.trainWho||ME(),
      title:TRAIN[d.workout].n,sub:'Training  \u00B7  auto from the Training tab'});
  (d.meals||[]).forEach(function(mm,i){
    var r=byId(mm.id); if(!r)return;
    out.push({t:mm.at||defMealTime(i),kind:'m',who:mm.who||ME(),title:r.n,
      sub:Math.round(r.k*(mm.q||1))+' kcal  \u00B7  '+Math.round(r.p*(mm.q||1))+' g protein  \u00B7  '+
        $$$(cps(r)*(mm.q||1)),mi:i});});
  (d.spend||[]).forEach(function(x,i){
    out.push({t:x.at||'',kind:'s',who:x.who,title:x.what,sub:$$$(x.amt),si:i});});
  out.sort(function(a,b){
    if(!a.t&&!b.t)return 0; if(!a.t)return 1; if(!b.t)return -1;
    return a.t<b.t?-1:a.t>b.t?1:0;});
  return out;
}
function defMealTime(i){return ['08:00','12:30','16:00','19:00','21:00'][i]||'20:00';}
function tl(ds){
  var items=dayTimeline(ds);
  if(!items.length) return '<div class="empty sm"><p>Nothing on this day yet.</p>'+
    '<p class="xs">Training and meals logged elsewhere show up here automatically.</p></div>';
  return '<ul class="tl">'+items.map(function(x){
    return '<li><div class="tm">'+(x.t?E(x.t):'&mdash;')+'</div>'+
    '<span class="pip '+x.kind+'"></span><div class="bd">'+
    '<div class="ti">'+E(x.title)+' <span class="chip">'+E(x.who||'Both')+'</span></div>'+
    (x.sub?'<div class="ts">'+E(x.sub)+'</div>':'')+'</div>'+
    (x.rm!=null?'<button class="x" data-evd="'+x.rm+'">&times;</button>':'')+
    (x.mi!=null?'<button class="x" data-mld="'+x.mi+'">&times;</button>':'')+
    (x.si!=null?'<button class="x" data-spd="'+x.si+'">&times;</button>':'')+
    '</li>';}).join('')+'</ul>';
}
function vSchedule(sub){
  if(sub==='week') return vWeekTemplate();
  var first=new Date(calY,calM,1), start=first.getDay(), days=new Date(calY,calM+1,0).getDate();
  var cells='';
  for(var i=0;i<start;i++)cells+='<div class="day out"></div>';
  for(var dn=1;dn<=days;dn++){
    var ds=calY+'-'+p2(calM+1)+'-'+p2(dn), rec=S.days[ds];
    var n=rec?dayTimeline(ds).length:0;
    cells+='<div class="day'+(ds===today()?' today':'')+(ds===calSel?' sel':'')+'" data-d="'+ds+'">'+
      '<span class="dn">'+dn+'</span><span class="dots">'+
      (rec&&rec.sched&&rec.sched.length?'<i class="dot e"></i>':'')+
      (rec&&rec.workout&&rec.workout!=='rest'?'<i class="dot w"></i>':'')+
      (rec&&rec.meals&&rec.meals.length?'<i class="dot m"></i>':'')+
      '</span><span class="dk">'+(n||'')+'</span></div>';}
  var d=dayLog(calSel), t=dayTarget(S.who,d.workout), got=eaten(calSel);
  var spend=(d.spend||[]).reduce(function(a,x){return a+(x.amt||0);},0);
  return '<div class="page"><div class="phead"><h1>Schedule</h1>'+
   '<p>Everything either of us is doing that day, in time order. Training and meals appear here on '+
   'their own from the other tabs.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b o" data-nav="schedule/week">Weekly template</button>'+
   '<button class="b o" id="applyTmpl">Apply template to this week</button>'+
   '<button class="b o" id="calCsv">Export the log</button></div>'+
   '<div class="card pad"><div class="spread" style="margin-bottom:12px">'+
   '<button class="b o s" id="cPrev">&larr;</button>'+
   '<h3>'+new Date(calY,calM,1).toLocaleDateString(undefined,{month:'long',year:'numeric'})+'</h3>'+
   '<button class="b o s" id="cNext">&rarr;</button></div>'+
   '<div class="cal">'+DOW.map(function(x){return '<div class="dow">'+x+'</div>';}).join('')+cells+'</div>'+
   '<div class="row xs muted" style="margin-top:12px">'+
   '<span><i class="dot e" style="display:inline-block"></i> plans</span>'+
   '<span><i class="dot w" style="display:inline-block"></i> training</span>'+
   '<span><i class="dot m" style="display:inline-block"></i> meals</span></div></div>'+
   '<div class="sec"><div class="spread"><h2>'+pretty(calSel)+'</h2>'+
   '<div class="row"><button class="b" id="evAdd">Add plan</button>'+
   '<button class="b o" id="mealAdd">Log meal</button>'+
   '<button class="b o" id="spAdd">Log spend</button></div></div>'+
   '<div class="grid g2"><div class="card pad">'+tl(calSel)+freeSlots(d)+'</div>'+
   '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">The day</h3>'+
   '<label class="f"><span>Training</span><select id="schWorkout">'+
   Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
   '</select></label>'+
   (d.workout!=='rest'?'<label class="f"><span>Session time</span><input id="schTrainAt" type="time" value="'+(d.trainAt||'17:30')+'"></label>':'')+
   bar('Calories',got.kcal,t.kcal,'pk')+bar('Protein',got.p,t.p,'pp')+
   '<div class="spread sm" style="margin-top:12px"><span class="muted">Food</span><b>'+$$$(got.cost)+'</b></div>'+
   '<div class="spread sm"><span class="muted">Other spend</span><b>'+$$$(spend)+'</b></div>'+
   '<div class="spread" style="margin-top:6px;padding-top:8px;border-top:1px solid var(--line)">'+
   '<span><b>Day total</b></span><b style="color:var(--brass)">'+$$$(got.cost+spend)+'</b></div>'+
   '</div></div></div></div>';
}
function freeSlots(d){
  var busy={Jaron:[],Aaliyah:[]};
  (d.sched||[]).forEach(function(e){ if(e.from&&e.to&&busy[e.who]) busy[e.who].push([e.from,e.to]); });
  if(!busy.Jaron.length&&!busy.Aaliyah.length) return '';
  function mins(t){var p=String(t).split(':');return (+p[0])*60+(+(p[1]||0));}
  var free=[],start=8*60,end=22*60,step=30;
  for(var m=start;m<end;m+=step){
    var clash=false;
    ['Jaron','Aaliyah'].forEach(function(w){busy[w].forEach(function(b){
      if(m>=mins(b[0])&&m<mins(b[1]))clash=true;});});
    if(!clash)free.push(m);
  }
  if(!free.length) return '<div class="note" style="margin-top:12px">No overlapping free time today.</div>';
  var blocks=[],cur=[free[0],free[0]+step];
  for(var i=1;i<free.length;i++){ if(free[i]===cur[1])cur[1]=free[i]+step; else {blocks.push(cur);cur=[free[i],free[i]+step];} }
  blocks.push(cur);
  var fmt=function(m){var h=Math.floor(m/60),mm=m%60;var ap=h>=12?'pm':'am';var hh=h%12||12;
    return hh+(mm?':'+p2(mm):'')+ap;};
  return '<div class="note" style="margin-top:12px"><b>Both free.</b> '+
    blocks.filter(function(b){return b[1]-b[0]>=60;}).map(function(b){return fmt(b[0])+' to '+fmt(b[1]);}).join(', ')+'</div>';
}
function vWeekTemplate(){
  var t=S.sched.tmpl||{};
  return '<div class="page"><div class="phead"><h1>Weekly template</h1>'+
   '<p>The regular week: work, class, church, gym. Put it in once with times and places, then push '+
   'it onto any week.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b o" data-nav="schedule">&larr; Calendar</button>'+
   '<button class="b" id="applyTmpl2">Apply to this week</button></div>'+
   '<div class="grid g3">'+DOW.map(function(dn,i){
     var items=(t[i]||[]).slice().sort(function(a,b){return (a.from||'')<(b.from||'')?-1:1;});
     return '<div class="card pad"><div class="spread"><h3 style="font-size:16px">'+dn+'</h3>'+
     '<button class="b o s" data-tadd="'+i+'">Add</button></div>'+
     (items.length?'<ul class="tl" style="margin-top:12px">'+items.map(function(x,j){
       return '<li><div class="tm">'+E(x.from||'')+'</div><span class="pip e"></span>'+
       '<div class="bd"><div class="ti">'+E(x.what)+' <span class="chip">'+E(x.who)+'</span></div>'+
       '<div class="ts">'+[(x.from?x.from+(x.to?' - '+x.to:''):''),x.where||''].filter(Boolean).join('  \u00B7  ')+
       '</div></div><button class="x" data-td="'+i+'|'+j+'">&times;</button></li>';}).join('')+'</ul>'
       :'<p class="empty sm" style="padding:14px 0">Nothing regular.</p>')+'</div>';}).join('')+
   '</div></div>';
}
/* ============================ shared UI ============================ */
function statRow(t){
  return '<div class="stats"><div class="stat acc"><b>'+N(t.kcal)+'</b><span>Calories</span></div>'+
   '<div class="stat"><b>'+t.p+'g</b><span>Protein</span></div>'+
   '<div class="stat"><b>'+t.c+'g</b><span>Carbs</span></div>'+
   '<div class="stat"><b>'+t.f+'g</b><span>Fat</span></div>'+
   '<div class="stat"><b>'+t.fib+'g</b><span>Fiber</span></div>'+
   '<div class="stat"><b>'+t.w+'oz</b><span>Water</span></div></div>';
}
function bar(l,have,need,cls){
  var pct=Math.min(100,need?have/need*100:0);
  return '<div class="mrow"><div class="spread"><span>'+l+'</span><em>'+Math.round(have)+' / '+Math.round(need)+'</em></div>'+
   '<div class="bar"><i class="'+cls+'" style="width:'+pct+'%"></i></div></div>';
}
function opt(a,sel){return a.map(function(o){return '<option value="'+E(o[0])+'"'+
  (String(o[0])===String(sel)?' selected':'')+'>'+E(o[1])+'</option>';}).join('');}
function modal(title,body,foot){
  var m=document.createElement('div');m.className='mask';
  m.innerHTML='<div class="modal"><div class="mhead"><h3>'+E(title)+'</h3><button class="x" data-close>&times;</button></div>'+
   '<div class="mbody">'+body+'</div>'+(foot?'<div class="mfoot">'+foot+'</div>':'')+'</div>';
  document.body.appendChild(m);
  m.addEventListener('click',function(e){ if(e.target===m||e.target.hasAttribute('data-close'))m.remove(); });
  return m;
}
function form(fields){
  return '<div class="fr">'+fields.map(function(f){
    if(f.t==='select') return '<label class="f"><span>'+E(f.l)+'</span><select id="'+f.id+'">'+
      opt(f.o,f.v)+'</select></label>';
    if(f.t==='area') return '<label class="f" style="grid-column:1/-1"><span>'+E(f.l)+'</span>'+
      '<textarea id="'+f.id+'" rows="3">'+E(f.v||'')+'</textarea></label>';
    return '<label class="f"><span>'+E(f.l)+'</span><input id="'+f.id+'" type="'+(f.t||'text')+
      '"'+(f.step?' step="'+f.step+'"':'')+' value="'+E(f.v==null?'':f.v)+'"'+
      (f.ph?' placeholder="'+E(f.ph)+'"':'')+'></label>';}).join('')+'</div>';
}

/* ============================ router ============================ */
var TABS=[['meals','Meals'],['training','Training'],['shopping','Shopping'],
          ['financial','Financial'],['schedule','Schedule']];
var ICO={meals:'<path d="M4 3v8a3 3 0 006 0V3M7 11v10M16 3c-1.5 2-2 4-2 6s.5 3 2 3 2-1 2-3-.5-4-2-6zM16 12v9"/>',
 training:'<path d="M6 8v8M18 8v8M3 10v4M21 10v4M6 12h12"/>',
 shopping:'<path d="M3 4h2l2 12h11M7 8h14l-2 6H8"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/>',
 financial:'<path d="M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>',
 schedule:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'};
function chrome(){
  $('#tabs').innerHTML=TABS.map(function(t){return '<button class="tab" data-v="'+t[0]+'" data-nav="'+t[0]+'">'+t[1]+'</button>';}).join('');
  $('#btm').innerHTML=TABS.map(function(t){return '<button data-v="'+t[0]+'" data-nav="'+t[0]+'">'+
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'+
    ICO[t[0]]+'</svg><span>'+t[1]+'</span></button>';}).join('');
  $('#who').innerHTML=['j','a'].map(function(k){return '<button data-w="'+k+'"'+
    (S.who===k?' class="on"':'')+'>'+E(S.prof[k].name)+'</button>';}).join('');
  var g=$('#settings');
  if(g) g.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'+
    '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06A1.65 1.65 0 009 4.6h.09A1.65 1.65 0 0010.6 3.09V3a2 2 0 114 0v.09A1.65 1.65 0 0015 4.6a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06A1.65 1.65 0 0019.4 9v.09A1.65 1.65 0 0021 10.6a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>';
}
function route(){
  var h=(location.hash||'#/meals').slice(2).split('/'), v=h[0]||'meals', sub=h[1]||'';
  var m=$('#view');
  m.innerHTML = v==='r'?vRecipe(sub) : v==='training'?vTraining(sub) : v==='shopping'?vShopping(sub)
    : v==='financial'?vFinancial(sub) : v==='schedule'?vSchedule(sub) : vMeals();
  try{window.scrollTo(0,0);}catch(e){}
  $$('.tab,.btmnav button').forEach(function(b){
    b.classList.toggle('on', b.dataset.v===(v==='r'?'meals':v));});
  $$('#who button').forEach(function(b){b.classList.toggle('on', b.dataset.w===S.who);});
  bind();
}
window.addEventListener('hashchange',route);
function nav(p){location.hash='#/'+p;}

/* ============================ per-view binding ============================ */
function bind(){
  var h=(location.hash||'#/meals').slice(2).split('/'), v=h[0];
  if(v==='meals'){ applyFilters();
    on('#fq','input',function(){flt.q=this.value;applyFilters();});
    ['fcat','ftag','fsort'].forEach(function(id){
      on('#'+id,'change',function(){flt[id.slice(1)]=this.value;applyFilters();});});
    on('#costMode','change',function(){S.costMode=this.value;save();route();});
    on('#bothCost','click',function(){
      var a=estDayCost(dayTarget('j',dayLog(today()).workout),S.costMode||'all');
      var b=estDayCost(dayTarget('a',dayLog(today()).workout),S.costMode||'all');
      $('#bothOut').innerHTML='<div class="note" style="margin-top:12px"><b>Both of us.</b> '+
        $$$(a.byKcal)+' for me plus '+$$$(b.byKcal)+' for '+E(S.prof.a.name)+' is <b>'+
        $$$(a.byKcal+b.byKcal)+' a day</b>, '+$$$((a.byKcal+b.byKcal)*30)+' a month.</div>';});
    on('#addOwn','click',ownRecipe);
  }
  if(v==='r'){ var r=byId(h[1]); if(r){ drawIng(r,1);
    $$('[data-scale]').forEach(function(b){b.onclick=function(){
      $$('[data-scale]').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on'); drawIng(r,parseFloat(b.dataset.scale));};});}}
  if(v==='shopping'&&h[1]==='ingredients'){ drawIngTable('');
    on('#ingQ','input',function(){drawIngTable(this.value);});
    on('#ingNew','click',function(){ingEditor(null);});
    on('#ingCsv','click',function(){
      var rows=[['Ingredient','Aisle','Walmart/100g','Costco/100g','Best','BestStore','UsedIn','Edited']];
      allIngKeys().forEach(function(k){var g=ING(k);
        rows.push([g.n,g.a||'',g.w,g.c,best(g).toFixed(3),bestStore(g),ingUsage(k),S.ingOv[k]?'yes':'']);});
      dl('ingredients-'+today()+'.csv',toCSV(rows),'text/csv');});
  }
  if(v==='shopping'&&h[1]!=='ingredients'){ bindShop(); }
  if(v==='training'&&h[1]==='exercises'){ drawEx();
    on('#exq','input',function(){exFlt.q=this.value;drawEx();});
    on('#exmg','change',function(){exFlt.mg=this.value;drawEx();});
    on('#exeq','change',function(){exFlt.eq=this.value;drawEx();});
    on('#exhero','click',function(){exFlt.hero=!exFlt.hero;this.classList.toggle('on');drawEx();});
  }
  if(v==='training'&&h[1]!=='exercises'){
    on('#tWorkout','change',function(){var dd=dayLog(today());dd.workout=this.value;
    dd.trainWho=ME(); if(!dd.trainAt)dd.trainAt='17:30'; save();route();});
    on('#tSave','click',function(){var d=dayLog(today());d.notes=$('#tNotes').value;
      var w=parseFloat($('#tW').value); if(w)d.w=w; save();toast('Saved');});
  }
  if(v==='financial') bindFin(h[1]);
  if(v==='schedule') bindSched(h[1]);
}
function on(sel,ev,fn){var e=$(sel); if(e)e.addEventListener(ev,fn);}

/* ============================ shopping wiring ============================ */
function bindShop(){
  on('#newList','click',function(){
    var n=prompt('Name the list'); if(!n)return;
    var c=prompt('Category (Groceries, Household, Costco run, Party...)','Groceries')||'Lists';
    S.shop.lists[n]={cat:c,fav:false,items:[]}; S.shop.active=n; save(); route();});
  on('#listRename','click',function(){
    var n=prompt('Rename to',S.shop.active); if(!n||n===S.shop.active)return;
    S.shop.lists[n]=S.shop.lists[S.shop.active]; delete S.shop.lists[S.shop.active];
    S.shop.active=n; save(); route();});
  on('#listDup','click',function(){
    var n=S.shop.active+' copy';
    S.shop.lists[n]=JSON.parse(JSON.stringify(S.shop.lists[S.shop.active]));
    S.shop.active=n; save(); route();});
  on('#listFav','click',function(){var L=curList();L.fav=!L.fav;save();route();});
  on('#listDel','click',function(){
    if(Object.keys(S.shop.lists).length<2){toast('Keep at least one list');return;}
    if(!confirm('Delete "'+S.shop.active+'"?'))return;
    delete S.shop.lists[S.shop.active]; S.shop.active=Object.keys(S.shop.lists)[0]; save(); route();});
  on('#gClear','click',function(){var L=curList();
    L.items=L.items.filter(function(i){return !i.done;}); save(); route();});
  on('#gAdd','click',function(){ingPicker(function(it){curList().items.push(it);save();route();});});
  on('#gRecipe','click',recipePicker);
  on('#gTxt','click',shopTxt);
  on('#gCsv','click',shopCsv);
  on('#gSave','click',function(){
    dl('list-'+S.shop.active.replace(/[^a-z0-9]+/gi,'-').toLowerCase()+'.json',
      JSON.stringify({app:'handbook-list',name:S.shop.active,list:curList()},null,1),'application/json');
    toast('List saved');});
  on('#gLoad','click',function(){
    var i=document.createElement('input');i.type='file';i.accept='.json';
    i.onchange=function(){var fr=new FileReader();fr.onload=function(){
      try{var o=JSON.parse(fr.result); var nm=o.name||'Imported list';
        while(S.shop.lists[nm]) nm=nm+' 2';
        S.shop.lists[nm]=o.list||o; S.shop.active=nm; save(); route(); toast('List loaded');}
      catch(e){alert('Not a saved list file.');}};
      fr.readAsText(i.files[0]);};i.click();});
}
function ingPicker(cb){
  var keys=allIngKeys().sort(function(a,b){return ING(a).n.localeCompare(ING(b).n);});
  var body='<label class="f"><span>Search the '+keys.length+' ingredients we already have</span>'+
   '<input id="ipq" placeholder="Type to filter..." autocomplete="off"></label>'+
   '<div id="iplist" style="max-height:300px;overflow:auto;border:1px solid var(--line);border-radius:9px"></div>'+
   '<div class="note" style="margin-top:14px"><b>Not there?</b> Adding it below puts it in the '+
   'master ingredient list permanently, not just this shop.</div>';
  var m=modal('Add to '+S.shop.active,body,
    '<button class="b o" data-close>Cancel</button><button class="b" id="ipNew">Add a new ingredient</button>');
  function draw(q){q=(q||'').toLowerCase();
    var hit=keys.filter(function(k){return ING(k).n.toLowerCase().indexOf(q)>=0;}).slice(0,60);
    $('#iplist',m).innerHTML=hit.map(function(k){var g=ING(k);
      return '<div class="pickrow" data-k="'+k+'"><div style="flex:1"><b>'+E(g.n)+'</b>'+
      '<div class="xs muted">'+E(g.a||'Other')+' &middot; '+$$$(best(g))+'/100g at '+bestStore(g)+'</div></div>'+
      '<span class="b s">Add</span></div>';}).join('')||
      '<p class="empty sm">No match. Nothing by that name exists yet.</p>';
    $$('[data-k]',m).forEach(function(row){row.onclick=function(){
      var k=row.dataset.k,g=ING(k);
      cb({key:k,name:g.n,qty:1,price:best(g)*2,grams:200,note:'about 200 g',
          aisle:g.a||'Other',done:false});
      m.remove();toast('Added '+g.n);};});}
  draw(''); $('#ipq',m).oninput=function(){draw(this.value);};
  $('#ipNew',m).onclick=function(){m.remove();ingEditor(null);};
}
function recipePicker(){
  var body='<label class="f"><span>Search</span><input id="rpq" placeholder="Filter recipes..."></label>'+
   '<div id="rplist" style="max-height:340px;overflow:auto;border:1px solid var(--line);border-radius:9px"></div>';
  var m=modal('Add a recipe to '+S.shop.active,body,'<button class="b" data-close>Done</button>');
  m.addEventListener('click',function(e){if(e.target.hasAttribute('data-close'))route();});
  function draw(q){q=(q||'').toLowerCase();
    var hit=all().filter(function(r){return r.n.toLowerCase().indexOf(q)>=0;}).slice(0,70);
    $('#rplist',m).innerHTML=hit.map(function(r){
      return '<div class="pickrow" data-r="'+r.id+'"><div style="flex:1"><b>'+E(r.n)+'</b>'+
      '<div class="xs muted">'+r.id+' &middot; makes '+r.sv+' &middot; '+$$$(ctot(r))+'</div></div>'+
      '<span class="b s">Add</span></div>';}).join('');
    $$('[data-r]',m).forEach(function(row){row.onclick=function(){
      addRecipeToShop(byId(row.dataset.r));toast('Ingredients added');};});}
  draw('');$('#rpq',m).oninput=function(){draw(this.value);};
}
function addRecipeToShop(r){
  if(!r)return; var L=curList();
  (r.ing||[]).forEach(function(i){
    var k=i[1],g=i[2]||0,q=ING(k); if(!q)return;
    var ex=L.items.filter(function(x){return x.key===k;})[0];
    if(ex){ ex.grams=(ex.grams||0)+g; ex.price=(ex.grams/100)*best(q); ex.qty=1;
            ex.note=Math.round(ex.grams)+' g'; }
    else L.items.push({key:k,name:q.n,qty:1,price:(g/100)*best(q),grams:g,
      note:Math.round(g)+' g',aisle:q.a||'Other',done:false});
  });
  save();
}
function shopTxt(){
  var L=curList(),byA={};
  L.items.forEach(function(i){(byA[i.aisle]=byA[i.aisle]||[]).push(i);});
  var out=['SHOPPING LIST  -  '+S.shop.active,pretty(today()),
    'Best price of Walmart Fort Collins / Costco Timnath',''];
  var tot=0;
  AISLES.map(function(a){return a[0];}).concat(['Other']).forEach(function(a){
    if(!byA[a])return; out.push(a.toUpperCase());
    byA[a].forEach(function(i){tot+=i.price*i.qty;
      out.push('  ['+(i.done?'x':' ')+'] '+i.name+'  -  '+(i.note||'')+'   '+$$$(i.price*i.qty));});
    out.push('');});
  out.push('TOTAL  '+$$$(tot));
  dl('shopping-'+today()+'.txt',out.join('\n'));
}
function shopCsv(){
  var rows=[['List','Aisle','Item','Qty','Grams','Price','Done']];
  curList().items.forEach(function(i){
    rows.push([S.shop.active,i.aisle,i.name,i.qty,i.grams||'',i.price.toFixed(2),i.done?'yes':'']);});
  dl('shopping-'+today()+'.csv',toCSV(rows),'text/csv');
}

/* ============================ financial wiring ============================ */
function bindFin(sub){
  on('#finMode','change',function(){S.fin.costMode=this.value;save();route();});
  on('#finPath','change',function(){S.fin.path=this.value;save();route();});
  on('#finScen','change',function(){
    var v=this.value;
    if(!v){S.fin.activeScenario=null;save();route();return;}
    if(scenDirty()&&!confirm('"'+S.fin.activeScenario+'" has unsaved changes. Open "'+v+
      '" anyway and lose them?')){route();return;}
    scenLoad(v);route();toast('Opened '+v);});
  on('#scenNew','click',function(){
    var n=prompt('Name the new scenario','Renting, both grinding'); if(!n)return;
    if(S.fin.scenarios[n]&&!confirm('"'+n+'" exists. Overwrite it?'))return;
    scenSave(n);route();toast('"'+n+'" created from the current numbers');});
  on('#scenSaveAs','click',function(){
    var n=prompt('Save these numbers as','Copy of '+(S.fin.activeScenario||'working')); if(!n)return;
    scenSave(n);route();toast('Saved as "'+n+'"');});
  on('#scenUpdate','click',function(){
    if(!S.fin.activeScenario)return;
    scenSave(S.fin.activeScenario);route();toast('Saved');});
  on('#scenRevert','click',function(){
    if(!S.fin.activeScenario)return;
    if(!confirm('Throw away the changes and go back to the saved "'+S.fin.activeScenario+'"?'))return;
    scenRevert();route();toast('Reverted');});
  ['#jobAdd','#jobAdd2'].forEach(function(s){on(s,'click',function(){jobEditor(null);});});
  on('#costAdd','click',function(){costEditor(null);});
  on('#shAdd','click',function(){shiftEditor();});
  on('#shCsv','click',function(){
    var rows=[['Date','Who','Job','Hours','Gross','Net','Note']];
    S.fin.shifts.forEach(function(s){var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
      rows.push([s.date,j?j.who:'',j?j.name:'',s.hours,s.gross,s.net,s.note||'']);});
    dl('shifts-'+today()+'.csv',toCSV(rows),'text/csv');});
  on('#scenFromActual','click',function(){
    var from=new Date();from.setDate(from.getDate()-90);
    var f=from.getFullYear()+'-'+p2(from.getMonth()+1)+'-'+p2(from.getDate());
    var net=shiftsFor(null,f).reduce(function(a,s){return a+(s.net||0);},0)/(90/30.4);
    S.fin.scenarios['From actual earnings']={mode:'actual',path:S.fin.path||'rent',
      inc:Math.round(net),cost:finCost('real',S.fin.path||'rent'),saved:today(),auto:true};
    save();toast('Saved from real data');route();});
  on('#bpNew','click',function(){
    var n=prompt('List name','Apartments'); if(!n)return;
    var c=prompt('What kind? (Housing, Cars, Furniture...)','Housing')||'Other';
    S.fin.purchases[n]={cat:c,items:[]}; save(); route();});
}
function jobEditor(id){
  var j=id?S.fin.jobs.filter(function(x){return x.id===id;})[0]:{who:'Jaron',name:'',employer:'',title:'',rate:'',low:'',real:'',high:''};
  var m=modal(id?'Edit income':'Add income',
    form([{id:'jw',l:'Who',t:'select',o:[['Jaron','Jaron'],['Aaliyah','Aaliyah'],['Both','Shared / gig']],v:j.who},
      {id:'jn',l:'Name',v:j.name,ph:'Ritchey day job'},
      {id:'je',l:'Employer',v:j.employer},{id:'jt',l:'Title',v:j.title},
      {id:'jr',l:'Hourly rate',t:'number',step:'0.01',v:j.rate},
      {id:'jl',l:'Low / mo',t:'number',v:j.low},{id:'jm',l:'Realistic / mo',t:'number',v:j.real},
      {id:'jh',l:'High / mo',t:'number',v:j.high}]),
    (id?'<button class="b o dz" id="jDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="jSave">Save</button>');
  var dl_=$('#jDel',m); if(dl_)dl_.onclick=function(){
    S.fin.jobs=S.fin.jobs.filter(function(x){return x.id!==id;});save();m.remove();route();};
  $('#jSave',m).onclick=function(){
    var o={id:id||uid(),who:$('#jw',m).value,name:$('#jn',m).value.trim()||'Income',
      employer:$('#je',m).value,title:$('#jt',m).value,rate:num($('#jr',m).value)||null,
      low:num($('#jl',m).value),real:num($('#jm',m).value),high:num($('#jh',m).value)};
    if(id)S.fin.jobs=S.fin.jobs.map(function(x){return x.id===id?o:x;}); else S.fin.jobs.push(o);
    save();m.remove();route();};
}
function costEditor(id){
  var c=id?S.fin.costs.filter(function(x){return x.id===id;})[0]:{name:'',section:'Living',who:'Both',low:'',real:'',high:'',actual:''};
  var m=modal(id?'Edit cost':'Add cost',
    form([{id:'cn',l:'Cost',v:c.name},
      {id:'cs',l:'Section',t:'select',o:[['Living','Living'],['Utilities','Utilities'],
        ['Health','Health'],['Housing (rent)','Housing (rent)'],['Housing (buy)','Housing (buy)'],
        ['Debt','Debt'],['Savings','Savings']],v:c.section},
      {id:'cw',l:'Who',t:'select',o:[['Both','Both'],['Jaron','Jaron'],['Aaliyah','Aaliyah']],v:c.who},
      {id:'cl',l:'Low',t:'number',v:c.low},{id:'cr',l:'Realistic',t:'number',v:c.real},
      {id:'ch',l:'High',t:'number',v:c.high},{id:'ca',l:'Actual',t:'number',v:c.actual}]),
    (id?'<button class="b o dz" id="cDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="cSave">Save</button>');
  var d=$('#cDel',m); if(d)d.onclick=function(){
    S.fin.costs=S.fin.costs.filter(function(x){return x.id!==id;});save();m.remove();route();};
  $('#cSave',m).onclick=function(){
    var o={id:id||uid(),name:$('#cn',m).value.trim()||'Cost',section:$('#cs',m).value,
      who:$('#cw',m).value,low:num($('#cl',m).value),real:num($('#cr',m).value),
      high:num($('#ch',m).value),actual:num($('#ca',m).value)||null};
    if(id)S.fin.costs=S.fin.costs.map(function(x){return x.id===id?o:x;}); else S.fin.costs.push(o);
    save();m.remove();route();};
}
function shiftEditor(){
  if(!S.fin.jobs.length){toast('Add a job first');return;}
  var m=modal('Log a shift',
    form([{id:'sd',l:'Date',t:'date',v:today()},
      {id:'sj',l:'Job',t:'select',o:S.fin.jobs.map(function(j){return [j.id,j.who+' - '+j.name];}),v:S.fin.jobs[0].id},
      {id:'sh',l:'Hours',t:'number',step:'0.25',v:8},
      {id:'sg',l:'Gross $',t:'number',step:'0.01',v:''},
      {id:'sn',l:'Net (after tax) $',t:'number',step:'0.01',v:''},
      {id:'sx',l:'Note',v:''}])+
    '<p class="sm muted">Leave gross blank and it uses the job hourly rate. Leave net blank and it estimates 80% of gross.</p>',
    '<button class="b o" data-close>Cancel</button><button class="b" id="sSave">Save</button>');
  $('#sSave',m).onclick=function(){
    var jid=$('#sj',m).value, j=S.fin.jobs.filter(function(x){return x.id===jid;})[0];
    var hrs=num($('#sh',m).value), g=num($('#sg',m).value), n=num($('#sn',m).value);
    if(!g&&j&&j.rate) g=hrs*j.rate;
    if(!n&&g) n=g*0.8;
    S.fin.shifts.push({id:uid(),date:$('#sd',m).value||today(),jobId:jid,hours:hrs,
      gross:Math.round(g*100)/100,net:Math.round(n*100)/100,note:$('#sx',m).value});
    save();m.remove();route();toast('Shift logged');};
}
function bpItemEditor(listName){
  var L=S.fin.purchases[listName]; var cat=(L.cat||'').toLowerCase();
  var extra = cat.indexOf('hous')>=0 ? [{id:'f1',l:'Beds'},{id:'f2',l:'Baths'},{id:'f3',l:'Sq ft'},{id:'f4',l:'To CSU (min)'}]
            : cat.indexOf('car')>=0 ? [{id:'f1',l:'Year'},{id:'f2',l:'Miles'},{id:'f3',l:'MPG'},{id:'f4',l:'Condition'}]
            : [{id:'f1',l:'Detail 1'},{id:'f2',l:'Detail 2'}];
  var m=modal('Add to '+listName,
    form([{id:'bn',l:'Name',v:''},{id:'bp',l:'Price / rent',t:'number',v:''},
      {id:'bl',l:'Link',v:''}].concat(extra).concat([{id:'bo',l:'Notes',t:'area',v:''}])),
    '<button class="b o" data-close>Cancel</button><button class="b" id="bSave">Save</button>');
  $('#bSave',m).onclick=function(){
    var f={}; extra.forEach(function(x){var v=$('#'+x.id,m).value; if(v)f[x.l]=v;});
    L.items.push({name:$('#bn',m).value.trim()||'Item',price:num($('#bp',m).value),
      link:$('#bl',m).value,notes:$('#bo',m).value,fields:f});
    save();m.remove();route();};
}

/* ============================ schedule wiring ============================ */
function bindSched(sub){
  on('#cPrev','click',function(){calM--;if(calM<0){calM=11;calY--;}route();});
  on('#cNext','click',function(){calM++;if(calM>11){calM=0;calY++;}route();});
  on('#schWorkout','change',function(){var dd=dayLog(calSel);dd.workout=this.value;
    dd.trainWho=ME(); if(!dd.trainAt)dd.trainAt='17:30'; save();route();});
  on('#schTrainAt','change',function(){dayLog(calSel).trainAt=this.value;save();route();});
  on('#evAdd','click',function(){evEditor(calSel);});
  on('#spAdd','click',function(){spendEditor(calSel);});
  on('#mealAdd','click',function(){mealPicker(calSel);});
  ['#applyTmpl','#applyTmpl2'].forEach(function(s){on(s,'click',applyTemplate);});
  on('#calCsv','click',function(){
    var rows=[['Date','Who','Training','Kcal','Protein','FoodCost','OtherSpend','Plans','Notes']];
    Object.keys(S.days).sort().forEach(function(d){var r=S.days[d],e=eaten(d);
      var sp=(r.spend||[]).reduce(function(a,x){return a+(x.amt||0);},0);
      rows.push([d,P().name,TRAIN[r.workout]?TRAIN[r.workout].n:r.workout,Math.round(e.kcal),
        Math.round(e.p),e.cost.toFixed(2),sp.toFixed(2),
        (r.sched||[]).map(function(x){return x.who+':'+x.what;}).join('; '),r.notes||'']);});
    dl('log-'+today()+'.csv',toCSV(rows),'text/csv');});
}
function evEditor(ds){
  var m=modal('Add to '+shortD(ds),
    form([{id:'ew',l:'Who',t:'select',o:whoOpts(),v:ME()},
      {id:'ex',l:'What',v:'',ph:'Class, shift, gym'},
      {id:'ef',l:'From',t:'time',v:'09:00'},{id:'et',l:'To',t:'time',v:'17:00'},
      {id:'el',l:'Where',v:''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="eSave">Add</button>');
  $('#eSave',m).onclick=function(){
    dayLog(ds).sched.push({who:$('#ew',m).value,what:$('#ex',m).value.trim()||'Busy',
      from:$('#ef',m).value,to:$('#et',m).value,where:$('#el',m).value});
    save();m.remove();route();};
}
function spendEditor(ds){
  var m=modal('Log a spend',
    form([{id:'sw',l:'Who',t:'select',o:whoOpts(),v:ME()},
      {id:'sx',l:'What',v:'',ph:'Gas, coffee, parts'},
      {id:'sa',l:'Amount',t:'number',step:'0.01',v:''},
      {id:'sat',l:'Time',t:'time',v:''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="spSave">Add</button>');
  $('#spSave',m).onclick=function(){
    dayLog(ds).spend.push({who:$('#sw',m).value,what:$('#sx',m).value.trim()||'Spend',
      amt:num($('#sa',m).value),at:$('#sat',m).value});
    save();m.remove();route();};
}
function mealPicker(ds){
  var body='<label class="f"><span>Search</span><input id="mpq" placeholder="What did we eat?"></label>'+
   '<div id="mplist" style="max-height:340px;overflow:auto;border:1px solid var(--line);border-radius:9px"></div>';
  var m=modal('Log a meal on '+shortD(ds),body,'<button class="b" data-close>Done</button>');
  m.addEventListener('click',function(e){if(e.target.hasAttribute('data-close'))route();});
  function draw(q){q=(q||'').toLowerCase();
    var hit=all().filter(function(r){return r.n.toLowerCase().indexOf(q)>=0;}).slice(0,60);
    $('#mplist',m).innerHTML=hit.map(function(r){
      return '<div class="pickrow" data-a="'+r.id+'"><div style="flex:1"><b>'+E(r.n)+'</b>'+
      '<div class="xs muted">'+Math.round(r.k)+' kcal &middot; '+Math.round(r.p)+'g protein &middot; '+$$$(cps(r))+'</div></div>'+
      '<span class="b s">Add</span></div>';}).join('');
    $$('[data-a]',m).forEach(function(row){row.onclick=function(){
      var dd=dayLog(ds);dd.meals.push({id:row.dataset.a,q:1,who:ME(),at:defMealTime(dd.meals.length)});save();toast('Logged for '+ME());};});}
  draw('');$('#mpq',m).oninput=function(){draw(this.value);};
}
function tmplEditor(dayIdx){
  var m=modal('Every '+DOW[dayIdx],
    form([{id:'tw',l:'Who',t:'select',o:whoOpts(),v:ME()},
      {id:'tx',l:'What',v:'',ph:'Church, work, class, gym'},
      {id:'tl',l:'Where',v:'',ph:'Fort Collins SDA, the shop, CSU'},
      {id:'tf',l:'From',t:'time',v:'09:00'},{id:'tt',l:'To',t:'time',v:'17:00'}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="tSave2">Add</button>');
  $('#tSave2',m).onclick=function(){
    if(!S.sched.tmpl[dayIdx])S.sched.tmpl[dayIdx]=[];
    S.sched.tmpl[dayIdx].push({who:$('#tw',m).value,what:$('#tx',m).value.trim()||'Busy',
      where:$('#tl',m).value.trim(),from:$('#tf',m).value,to:$('#tt',m).value});
    save();m.remove();route();};
}
function applyTemplate(){
  var t=S.sched.tmpl||{}, n=0, base=new Date();
  base.setDate(base.getDate()-base.getDay());
  for(var i=0;i<7;i++){
    var d=new Date(base); d.setDate(base.getDate()+i);
    var ds=d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());
    (t[i]||[]).forEach(function(x){
      var log=dayLog(ds);
      var dupe=log.sched.some(function(e){return e.what===x.what&&e.who===x.who&&e.from===x.from;});
      if(!dupe){log.sched.push({who:x.who,what:x.what,from:x.from,to:x.to,where:x.where||''});n++;}
    });
  }
  save();route();toast(n?n+' items added to this week':'Already applied');
}

/* ============================ global events ============================ */
document.addEventListener('click',function(e){
  var el;
  if((el=e.target.closest('[data-nav]'))){nav(el.dataset.nav);return;}
  if((el=e.target.closest('[data-w]'))){S.who=el.dataset.w;save();route();return;}
  if((el=e.target.closest('[data-fav]'))){e.stopPropagation();
    var id=el.dataset.fav,i=S.fav.indexOf(id);
    if(i>=0)S.fav.splice(i,1);else S.fav.push(id); save();route();return;}
  if((el=e.target.closest('[data-go]'))){nav('r/'+el.dataset.go);return;}
  if((el=e.target.closest('[data-log]'))){var dt=dayLog(today());
    dt.meals.push({id:el.dataset.log,q:1,who:ME(),at:defMealTime(dt.meals.length)});
    save();toast('Logged to today for '+ME());return;}
  if((el=e.target.closest('[data-groc]'))){addRecipeToShop(byId(el.dataset.groc));
    toast('Added to '+S.shop.active);return;}
  if((el=e.target.closest('[data-tolist]'))){listModal(el.dataset.tolist);return;}
  if((el=e.target.closest('[data-photo]'))){pickPhoto(el.dataset.photo);return;}
  if((el=e.target.closest('[data-card]'))){cardPNG(byId(el.dataset.card));return;}
  if((el=e.target.closest('[data-list]'))){S.shop.active=el.dataset.list;save();route();return;}
  if((el=e.target.closest('[data-gt]'))){var L=curList();
    L.items[+el.dataset.gt].done=el.checked;save();route();return;}
  if((el=e.target.closest('[data-gd]'))){curList().items.splice(+el.dataset.gd,1);save();route();return;}
  if((el=e.target.closest('[data-ge]'))){shopItemEditor(+el.dataset.ge);return;}
  if((el=e.target.closest('[data-ie]'))){ingEditor(el.dataset.ie);return;}
  if((el=e.target.closest('[data-sess]'))){sessModal(+el.dataset.sess);return;}
  if((el=e.target.closest('[data-jobe]'))){jobEditor(el.dataset.jobe);return;}
  if((el=e.target.closest('[data-coste]'))){costEditor(el.dataset.coste);return;}
  if((el=e.target.closest('[data-shd]'))){S.fin.shifts=S.fin.shifts.filter(function(x){
    return x.id!==el.dataset.shd;});save();route();return;}
  if((el=e.target.closest('[data-scload]'))){
    if(scenDirty()&&!confirm('Unsaved changes will be lost. Continue?')){return;}
    scenLoad(el.dataset.scload);route();toast('Opened '+el.dataset.scload);return;}
  if((el=e.target.closest('[data-scdel]'))){
    if(confirm('Delete scenario "'+el.dataset.scdel+'"?')){
      delete S.fin.scenarios[el.dataset.scdel];
      if(S.fin.activeScenario===el.dataset.scdel)S.fin.activeScenario=null;
      save();route();}return;}
  if((el=e.target.closest('[data-bpadd]'))){bpItemEditor(el.dataset.bpadd);return;}
  if((el=e.target.closest('[data-bpdel]'))){if(confirm('Delete list?')){
    delete S.fin.purchases[el.dataset.bpdel];save();route();}return;}
  if((el=e.target.closest('[data-bpi]'))){var p=el.dataset.bpi.split('|');
    S.fin.purchases[p[0]].items.splice(+p[1],1);save();route();return;}
  if((el=e.target.closest('[data-d]'))){calSel=el.dataset.d;route();return;}
  if((el=e.target.closest('[data-evd]'))){dayLog(calSel).sched.splice(+el.dataset.evd,1);save();route();return;}
  if((el=e.target.closest('[data-spd]'))){dayLog(calSel).spend.splice(+el.dataset.spd,1);save();route();return;}
  if((el=e.target.closest('[data-mld]'))){dayLog(calSel).meals.splice(+el.dataset.mld,1);save();route();return;}
  if((el=e.target.closest('[data-tadd]'))){tmplEditor(+el.dataset.tadd);return;}
  if((el=e.target.closest('[data-td]'))){var q=el.dataset.td.split('|');
    S.sched.tmpl[q[0]].splice(+q[1],1);save();route();return;}
  if(e.target.closest('#settings')){settingsModal();return;}
});
function settingsModal(){
  var when=S.savedAt?new Date(S.savedAt).toLocaleString():'never';
  var size=0; try{size=(localStorage.getItem(KEY)||'').length;}catch(e){}
  var body=
   '<h4 class="lbl">Your data</h4>'+
   '<p class="sm muted" style="margin:8px 0 14px">Everything lives in this browser on this device. '+
   'Nothing is uploaded. Save to a file to move it, back it up, or hand it over for changes.</p>'+
   '<div class="stats" style="margin-bottom:16px">'+
   '<div class="stat"><b>'+all().length+'</b><span>Recipes</span></div>'+
   '<div class="stat"><b>'+Object.keys(S.ingOv).length+'</b><span>Ingredient edits</span></div>'+
   '<div class="stat"><b>'+Object.keys(S.days).length+'</b><span>Days logged</span></div>'+
   '<div class="stat"><b>'+Math.round(size/1024)+'k</b><span>Stored</span></div></div>'+
   '<div class="row" style="margin-bottom:18px">'+
   '<button class="b" id="stSave">Save to a file</button>'+
   '<button class="b o" id="stLoad">Load a file</button></div>'+
   '<p class="xs muted">Last saved: '+E(when)+'</p>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Profiles</h4><div class="fr" style="margin-top:10px">'+
   '<label class="f"><span>My name</span><input id="stJ" value="'+E(S.prof.j.name)+'"></label>'+
   '<label class="f"><span>Her name</span><input id="stA" value="'+E(S.prof.a.name)+'"></label></div>'+
   '<p class="xs muted">Whoever is selected in the top bar is who new entries get logged as. '+
   'You can still change it on any entry.</p>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Exports</h4><div class="row" style="margin-top:10px">'+
   '<button class="b o s" id="stIng">Ingredients CSV</button>'+
   '<button class="b o s" id="stLog">Daily log CSV</button>'+
   '<button class="b o s" id="stShift">Shifts CSV</button>'+
   '<button class="b o s" id="stFin">Budget CSV</button></div>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Danger</h4>'+
   '<p class="sm muted" style="margin:8px 0 12px">This wipes everything on this device. '+
   'Save a file first.</p>'+
   '<button class="b dz" id="stReset">Erase all data</button>';
  var m=modal('Settings',body,'<button class="b o" data-close>Close</button>');
  $('#stSave',m).onclick=function(){exportAll();};
  $('#stLoad',m).onclick=function(){var i=document.createElement('input');i.type='file';i.accept='.json';
    i.onchange=function(){importAll(i.files[0],function(ok){if(ok){m.remove();route();toast('Loaded');}});};
    i.click();};
  $('#stJ',m).onchange=function(){S.prof.j.name=this.value||'Me';save();chrome();};
  $('#stA',m).onchange=function(){S.prof.a.name=this.value||'Aaliyah';save();chrome();};
  $('#stIng',m).onclick=function(){
    var rows=[['Ingredient','Aisle','Walmart/100g','Costco/100g','Best','Store','UsedIn','Edited']];
    allIngKeys().forEach(function(k){var g=ING(k);
      rows.push([g.n,g.a||'',g.w,g.c,best(g).toFixed(3),bestStore(g),ingUsage(k),S.ingOv[k]?'yes':'']);});
    dl('ingredients-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stLog',m).onclick=function(){
    var rows=[['Date','Training','Kcal','Protein','FoodCost','OtherSpend','Plans','Notes']];
    Object.keys(S.days).sort().forEach(function(d){var r=S.days[d],e=eaten(d);
      var sp=(r.spend||[]).reduce(function(a,x){return a+(x.amt||0);},0);
      rows.push([d,TRAIN[r.workout]?TRAIN[r.workout].n:r.workout,Math.round(e.kcal),
        Math.round(e.p),e.cost.toFixed(2),sp.toFixed(2),
        (r.sched||[]).map(function(x){return x.who+':'+x.what;}).join('; '),r.notes||'']);});
    dl('daily-log-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stShift',m).onclick=function(){
    var rows=[['Date','Who','Job','Hours','Gross','Net','Note']];
    S.fin.shifts.forEach(function(s){var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
      rows.push([s.date,j?j.who:'',j?j.name:'',s.hours,s.gross,s.net,s.note||'']);});
    dl('shifts-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stFin',m).onclick=function(){
    var rows=[['Type','Section','Name','Who','Low','Realistic','High','Actual']];
    S.fin.jobs.forEach(function(j){rows.push(['Income','',j.name,j.who,j.low,j.real,j.high,j.actual||'']);});
    S.fin.costs.forEach(function(c){rows.push(['Cost',c.section,c.name,c.who,c.low,c.real,c.high,c.actual||'']);});
    dl('budget-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stReset',m).onclick=function(){
    if(!confirm('Erase every list, log, edit and photo on this device?'))return;
    if(!confirm('Really sure? This cannot be undone without a saved file.'))return;
    try{localStorage.removeItem(KEY);}catch(e){} location.reload();};
}
function shopItemEditor(idx){
  var it=curList().items[idx];
  var m=modal('Edit '+it.name,
    form([{id:'sen',l:'Name',v:it.name},
      {id:'seq',l:'Qty',t:'number',step:'0.5',v:it.qty},
      {id:'sep',l:'Price each',t:'number',step:'0.01',v:it.price},
      {id:'sea',l:'Aisle',t:'select',o:AISLES.map(function(a){return [a[0],a[0]];}).concat([['Other','Other']]),v:it.aisle},
      {id:'sen2',l:'Note',v:it.note||''}])+
    (it.key?'<p class="sm muted">Changing the price here only affects this list. To change it '+
      'everywhere, edit it in the <a href="#/shopping/ingredients">ingredient list</a>.</p>':''),
    '<button class="b o dz" id="seDel">Remove</button>'+
    '<button class="b o" data-close>Cancel</button><button class="b" id="seSave">Save</button>');
  $('#seDel',m).onclick=function(){curList().items.splice(idx,1);save();m.remove();route();};
  $('#seSave',m).onclick=function(){
    it.name=$('#sen',m).value;it.qty=num($('#seq',m).value,1);it.price=num($('#sep',m).value);
    it.aisle=$('#sea',m).value;it.note=$('#sen2',m).value;save();m.remove();route();};
}
function listModal(id){
  var names=Object.keys(S.lists);
  var body=(names.length?names.map(function(n){var has=S.lists[n].indexOf(id)>=0;
    return '<div class="pickrow" data-l="'+E(n)+'"><input type="checkbox"'+(has?' checked':'')+
    ' style="width:18px;height:18px;accent-color:var(--forest)"><div><b>'+E(n)+'</b>'+
    '<div class="xs muted">'+S.lists[n].length+' recipes</div></div></div>';}).join('')
    :'<p class="sm muted">No recipe lists yet.</p>')+
   '<label class="f" style="margin-top:14px"><span>Or make a new one</span><input id="nl" placeholder="Sunday prep"></label>';
  var m=modal('Add to a recipe list',body,
    '<button class="b o" data-close>Cancel</button><button class="b" id="lS">Save</button>');
  $('#lS',m).onclick=function(){
    $$('.pickrow',m).forEach(function(r){var n=r.dataset.l;if(!n)return;
      var on_=r.querySelector('input').checked,i=S.lists[n].indexOf(id);
      if(on_&&i<0)S.lists[n].push(id); if(!on_&&i>=0)S.lists[n].splice(i,1);});
    var nl=$('#nl',m).value.trim();
    if(nl){if(!S.lists[nl])S.lists[nl]=[];if(S.lists[nl].indexOf(id)<0)S.lists[nl].push(id);}
    save();m.remove();toast('Saved');};
}
function pickPhoto(id){
  var inp=document.createElement('input');inp.type='file';inp.accept='image/*';
  inp.onchange=function(){var f=inp.files[0];if(!f)return;
    var fr=new FileReader();
    fr.onload=function(){var img=new Image();
      img.onload=function(){var sc=Math.min(1,900/Math.max(img.width,img.height));
        var cv=document.createElement('canvas');cv.width=img.width*sc|0;cv.height=img.height*sc|0;
        cv.getContext('2d').drawImage(img,0,0,cv.width,cv.height);
        S.photos[id]=cv.toDataURL('image/jpeg',0.72);save();route();toast('Photo saved');};
      img.src=fr.result;};
    fr.readAsDataURL(f);};
  inp.click();
}
function ownRecipe(){
  var m=modal('Add my own recipe',
    form([{id:'on',l:'Name',v:''},
      {id:'oc',l:'Category',t:'select',o:[['Breakfast','Breakfast'],['Lunch/Dinner','Mains'],
        ['Snack','Snack'],['Drink','Drink'],['SDA Meat/Fish','Meat and fish']],v:'Lunch/Dinner'},
      {id:'osv',l:'Servings',t:'number',v:2},{id:'ot',l:'Minutes',t:'number',v:20},
      {id:'ok',l:'Kcal / serving',t:'number',v:''},{id:'op',l:'Protein g',t:'number',v:''},
      {id:'ocb',l:'Carbs g',t:'number',v:''},{id:'of',l:'Fat g',t:'number',v:''},
      {id:'ocost',l:'Cost / serving',t:'number',step:'0.01',v:''},
      {id:'oi',l:'Ingredients, one per line',t:'area',v:''},
      {id:'os',l:'Method, one step per line',t:'area',v:''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="oSave">Save</button>');
  $('#oSave',m).onclick=function(){
    var n=$('#on',m).value.trim(); if(!n){toast('Needs a name');return;}
    var sv=num($('#osv',m).value,1), c=num($('#ocost',m).value);
    S.mine.push({id:'X-'+(S.mine.length+1),n:n,cat:$('#oc',m).value,sv:sv,t:num($('#ot',m).value,20),
      diff:'MODERATE',k:num($('#ok',m).value),p:num($('#op',m).value),c:num($('#ocb',m).value),
      f:num($('#of',m).value),fib:0,leu:0,tg:['MY RECIPE'],cw:c*sv,cws:c,cc:c*sv,ccs:c,
      ing:$('#oi',m).value.split('\n').filter(Boolean).map(function(l){return [l.trim(),'',0];}),
      st:$('#os',m).value.split('\n').filter(Boolean),storage:'',prep:'',subs:[],vars:[]});
    save();m.remove();route();toast('Recipe saved');};
}
function cardPNG(r){
  if(!r)return;
  var W=900,H=1280,cv=document.createElement('canvas');cv.width=W;cv.height=H;
  var x=cv.getContext('2d'),col=CATC[r.cat]||CATC['My recipe'];
  var g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,'#14140F');g.addColorStop(.58,'#1F3A2C');g.addColorStop(1,col[1]);
  x.fillStyle=g;x.fillRect(0,0,W,H);x.fillStyle=col[0];x.fillRect(0,0,W,9);
  x.fillStyle='#A8CDB8';x.font='700 19px Helvetica,Arial';
  x.fillText(r.id+'   \u00B7   '+r.cat.toUpperCase()+'   \u00B7   '+r.diff,56,80);
  x.fillStyle='#fff';x.font='800 52px Helvetica,Arial';
  var y=142+wrapT(x,r.n,56,142,780,56);
  var mac=[[Math.round(r.k),'KCAL'],[Math.round(r.p)+'g','PROTEIN'],[Math.round(r.c)+'g','CARBS'],
           [Math.round(r.f)+'g','FAT'],[Math.round(r.fib||0)+'g','FIBER'],[(r.leu||0).toFixed(1)+'g','LEUCINE']];
  var bw=(788-25)/6;
  mac.forEach(function(mm,i){var bx=56+i*(bw+5);
    x.fillStyle='rgba(255,255,255,.10)';x.fillRect(bx,y,bw,90);
    x.fillStyle='#fff';x.font='800 25px Helvetica,Arial';x.textAlign='center';
    x.fillText(String(mm[0]),bx+bw/2,y+40);
    x.fillStyle='#A8CDB8';x.font='700 11px Helvetica,Arial';x.fillText(mm[1],bx+bw/2,y+66);x.textAlign='left';});
  y+=128;
  x.fillStyle='#1F4D3A';x.fillRect(56,y,788,62);x.fillStyle='#fff';x.font='700 23px Helvetica,Arial';
  x.fillText(r.t+' min   \u00B7   makes '+r.sv+'   \u00B7   '+$$$(cps(r))+'/serving   \u00B7   '+$$$(ctot(r))+' batch',78,y+39);
  y+=100;
  x.fillStyle='#A8CDB8';x.font='700 16px Helvetica,Arial';x.fillText('INGREDIENTS',56,y);y+=28;
  x.fillStyle='#E6EDE7';x.font='400 18px Helvetica,Arial';
  (r.ing||[]).slice(0,15).forEach(function(i){var q=ING(i[1]);
    x.fillText('\u2022  '+(i[2]?Math.round(i[2])+' g  ':'')+(q?q.n:i[0]),56,y);y+=26;});
  y+=20;x.fillStyle='#A8CDB8';x.font='700 16px Helvetica,Arial';x.fillText('METHOD',56,y);y+=28;
  x.fillStyle='#C9D6CB';x.font='400 16px Helvetica,Arial';
  (r.st||[]).slice(0,6).forEach(function(s,i){y+=wrapT(x,(i+1)+'. '+s,56,y,788,23)+7;});
  x.fillStyle='#6E8A76';x.font='700 13px Helvetica,Arial';x.fillText('The Handbook',56,H-40);
  var a=document.createElement('a');
  a.download=r.id+'-'+r.n.replace(/[^a-z0-9]+/gi,'-').toLowerCase()+'.png';
  a.href=cv.toDataURL('image/png');a.click();
}
function wrapT(x,t,px,py,mw,lh){var w=String(t).split(' '),line='',yy=py,used=0;
  for(var i=0;i<w.length;i++){var tt=line+w[i]+' ';
    if(x.measureText(tt).width>mw&&line){x.fillText(line,px,yy);line=w[i]+' ';yy+=lh;used+=lh;}else line=tt;}
  x.fillText(line,px,yy);return used+lh;}

chrome();
if(!location.hash)location.hash='#/meals';
route();

})();
