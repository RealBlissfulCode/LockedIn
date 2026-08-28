# -*- coding: utf-8 -*-
APP_JS = r"""
<script>
(function(){
'use strict';
var R=__RECIPES__, ING=__ING__, AISLES=__AISLES__, LEARN=__LEARN__;
/* Price is always whichever store is cheaper for that specific item. */
function best(q){if(!q)return 0;var w=q.w,c=q.c;
  if(c!=null&&c>0&&(w==null||w<=0||c<w))return c; return w||0;}
function bestStore(q){if(!q)return '';var w=q.w,c=q.c;
  if(c!=null&&c>0&&(w==null||w<=0||c<w))return 'Costco'; return 'Walmart';}
var KEY='mh.v4';

/* ============ state ============ */
var DEF={who:'j',fav:[],lists:{'Weeknight go-tos':[],'Aaliyah likes':[],'Move-in week':[]},
  mine:[],photos:{},days:{},grocery:[],
  prof:{j:{name:'Me',sex:'m',w:150,h:68,age:20,bf:20,act:1.55,goal:1.09,pf:1.1},
        a:{name:'Aaliyah',sex:'f',w:120,h:66.5,age:20,bf:24,act:1.45,goal:1.0,pf:0.8}}};
var S=(function(){try{var r=localStorage.getItem(KEY);if(r){var o=JSON.parse(r);
  for(var k in DEF){if(!(k in o))o[k]=DEF[k];} return o;}}catch(e){} return JSON.parse(JSON.stringify(DEF));})();
function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){toast('Storage full. Remove a photo or export a backup.');}}

/* ============ helpers ============ */
function $(s,r){return (r||document).querySelector(s);}
function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}
function E(t){return String(t==null?'':t).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function $$$(v){return '$'+(Number(v)||0).toFixed(2);}
function p2(n){n=String(n);return n.length<2?'0'+n:n;}
function today(){var d=new Date();return d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());}
function pretty(ds){var p=ds.split('-');return new Date(+p[0],+p[1]-1,+p[2]).toLocaleDateString(undefined,{weekday:'long',month:'short',day:'numeric'});}
function toast(m){var t=document.createElement('div');t.className='toast';t.textContent=m;document.body.appendChild(t);
  setTimeout(function(){t.style.opacity='0';setTimeout(function(){t.remove();},300);},2000);}
function all(){return R.concat(S.mine);}
function byId(id){var a=all();for(var i=0;i<a.length;i++)if(a[i].id===id)return a[i];return null;}
function cps(r){var a=r.cws,b=r.ccs;return (b!=null&&b>0&&b<a)?b:a;}
function ctot(r){var a=r.cw,b=r.cc;return (b!=null&&b>0&&b<a)?b:a;}
function dl(name,text,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');
  a.href=URL.createObjectURL(b);a.download=name;a.click();setTimeout(function(){URL.revokeObjectURL(a.href);},900);}

/* ============ nutrition math ============ */
function calc(p){
  var kg=p.w*0.45359237, cm=p.h*2.54, m=cm/100, lbmKg=kg*(1-p.bf/100);
  var rmr=(10*kg)+(6.25*cm)-(5*p.age)+(p.sex==='f'?-161:5);
  var katch=370+21.6*lbmKg;
  var tdee=rmr*p.act, kcal=tdee*p.goal;
  var prot=p.w*p.pf, fat=kcal*0.25/9, carb=(kcal-prot*4-fat*9)/4;
  return {rmr:rmr,katch:katch,tdee:tdee,kcal:kcal,p:prot,c:carb,f:fat,
    fib:kcal/1000*14, w:p.w*0.6+25+10, lbm:p.w*(1-p.bf/100),
    ffmi:(lbmKg/(m*m))+6.1*(1.8-m), rate:(kcal-tdee)*7/3500};
}
var TRAIN={
 rest:{n:'Rest day',pm:1.0,cm:0.85,km:0.97,tag:['HIGH FIBER','HIGH MICRONUTRIENT DENSITY','HIGH SATIETY'],
   why:'Repair happens on rest days, so protein holds. Carbs ease back, fiber and micronutrients come up.'},
 pull:{n:'Back and biceps',pm:1.06,cm:1.05,km:1.02,tag:['LEUCINE PRIORITY','HIGH MICRONUTRIENT DENSITY','OMEGA-3 RICH'],
   why:'Biggest upper-body muscle group. Protein and leucine lead, and iron-rich picks get weighted up because pulling volume on a plant-heavy diet is where iron thins out.'},
 push:{n:'Chest, shoulders, triceps',pm:1.06,cm:1.0,km:1.01,tag:['LEUCINE PRIORITY'],
   why:'Straight hypertrophy demand. Leucine per feeding is the lever.'},
 legs:{n:'Legs',pm:1.03,cm:1.30,km:1.09,tag:['HIGH CALORIE','POST-WORKOUT FRIENDLY','HIGH SATIETY'],
   why:'Legs drain more glycogen than anything else. Carbs and total calories lead. This is the day to eat the big meal.'},
 arms:{n:'Arms',pm:1.03,cm:0.95,km:0.99,tag:['QUICK'],
   why:'Small muscle group, small systemic cost. Protein still matters, calories do not need to spike.'},
 abs:{n:'Abs and core',pm:1.0,cm:0.9,km:0.97,tag:['HIGH SATIETY','HIGH FIBER','LOW CALORIE'],
   why:'Low energy cost. Volume and fiber over calories.'},
 cardio:{n:'Cardio',pm:0.98,cm:1.25,km:1.05,tag:['POST-WORKOUT FRIENDLY','HEALTH DRINK'],
   why:'Carbs and fluid lead. Sodium matters more than usual in dry Colorado air.'},
 skill:{n:'Skill work',pm:1.02,cm:1.1,km:1.02,tag:['OMEGA-3 RICH','HIGH MICRONUTRIENT DENSITY'],
   why:'Planche and handstand work loads connective tissue more than muscle. Being properly fed beats any single macro.'},
 full:{n:'Full body',pm:1.06,cm:1.15,km:1.05,tag:['LEUCINE PRIORITY','HIGH CALORIE','POST-WORKOUT FRIENDLY'],
   why:'Everything trained, everything demanded.'}
};
function dayTarget(who,tt){
  var b=calc(S.prof[who]), t=TRAIN[tt||'rest'];
  return {kcal:b.kcal*t.km,p:b.p*t.pm,c:b.c*t.cm,f:b.f,fib:b.fib,w:b.w,base:b,tr:t};
}
function dayLog(ds){ if(!S.days[ds]) S.days[ds]={meals:[],workout:'rest',notes:''}; return S.days[ds]; }
function eaten(ds){
  var d=dayLog(ds),t={kcal:0,p:0,c:0,f:0,fib:0,cost:0};
  d.meals.forEach(function(m){var r=byId(m.id);if(!r)return;var n=m.sv||1;
    t.kcal+=r.k*n;t.p+=r.p*n;t.c+=r.c*n;t.f+=r.f*n;t.fib+=(r.fib||0)*n;t.cost+=cps(r)*n;});
  return t;
}

/* ============ visuals ============ */
function ring(r,size){
  var s=size||44,tot=r.p*4+r.c*4+r.f*9;if(!tot)tot=1;
  var cf=2*Math.PI*15.9155,segs=[[r.p*4/tot,'#1F4D3A'],[r.c*4/tot,'#C2860E'],[r.f*9/tot,'#5C4A78']],off=25,h='';
  segs.forEach(function(g){var d=g[0]*100;h+='<circle cx="18" cy="18" r="15.9155" fill="none" stroke="'+g[1]+
    '" stroke-width="4.2" stroke-dasharray="'+d.toFixed(2)+' '+(100-d).toFixed(2)+'" stroke-dashoffset="'+off+'"></circle>';off-=d;});
  return '<svg class="ring" viewBox="0 0 36 36" width="'+s+'" height="'+s+'">'+
    '<circle cx="18" cy="18" r="15.9155" fill="rgba(255,255,255,.9)" stroke="#E6EDF5" stroke-width="4.2"></circle>'+h+
    '<text x="18" y="19.6" text-anchor="middle" font-size="8.4" font-weight="800" fill="#14140F">'+Math.round(r.k)+'</text>'+
    '<text x="18" y="25" text-anchor="middle" font-size="4.4" font-weight="700" fill="#5D7186">KCAL</text></svg>';
}
var CATC={'Breakfast':['#D89A3C','#B0651F'],'Lunch/Dinner':['#2C6B50','#173C2C'],'Snack':['#4E8C7A','#28584A'],
 'Drink':['#8B6FD4','#5B3FA0'],'SDA Meat/Fish':['#E2725B','#B0432F'],'My recipe':['#5D7186','#2F3F4F']};
function art(r){
  var ph=S.photos[r.id];
  if(ph) return '<div class="rcart"><img src="'+ph+'" alt=""></div>';
  var c=CATC[r.cat]||CATC['My recipe'];
  return '<div class="rcart" style="background:linear-gradient(135deg,'+c[0]+','+c[1]+')">'+
    '<svg viewBox="0 0 100 60" style="width:100%;height:100%;opacity:.19"><circle cx="26" cy="30" r="17" fill="#fff"/>'+
    '<circle cx="26" cy="30" r="10" fill="'+c[1]+'"/><rect x="56" y="14" width="4" height="33" rx="2" fill="#fff"/>'+
    '<rect x="66" y="14" width="4" height="16" rx="2" fill="#fff"/><rect x="74" y="14" width="4" height="16" rx="2" fill="#fff"/>'+
    '<rect x="66" y="30" width="12" height="4" rx="2" fill="#fff"/><rect x="70" y="32" width="4" height="15" rx="2" fill="#fff"/></svg></div>';
}
function pscale(v){return v<1.6?'$':v<3.2?'$$':'$$$';}
function bestFor(r){
  if(r.tg.indexOf('LEUCINE PRIORITY')>=0||r.p>=42)return 'Protein';
  if(r.tg.indexOf('CHEAT MEAL')>=0)return 'Cheat';
  if(r.tg.indexOf('HEALTHY DESSERT')>=0||r.tg.indexOf('CHEAT DESSERT')>=0)return 'Dessert';
  if(r.c>=70)return 'Carbs';
  if(r.tg.indexOf('HIGH FIBER')>=0)return 'Fiber';
  if(r.k<=330)return 'Lean';
  if(r.tg.indexOf('OMEGA-3 RICH')>=0)return 'Omega-3';
  return 'Balanced';
}
function rcard(r){
  var f=S.fav.indexOf(r.id)>=0,dc=r.diff==='EASY'?'d1':r.diff==='MODERATE'?'d2':'d3';
  return '<article class="rc" data-go="'+r.id+'">'+art(r)+
    '<button class="fav'+(f?' on':'')+'" data-fav="'+r.id+'" title="Favourite">'+(f?'\u2605':'\u2606')+'</button>'+
    '<div class="rcbadge">'+r.id+'</div>'+
    '<div class="rcb"><div class="rcn">'+E(r.n)+'</div>'+
    '<div class="chips"><span class="chip">'+r.t+' min</span><span class="chip '+dc+'">'+
    (r.diff||'EASY').charAt(0)+(r.diff||'EASY').slice(1).toLowerCase()+'</span>'+
    '<span class="chip p">'+pscale(cps(r))+' '+$$$(cps(r))+'</span>'+
    '<span class="chip t">'+bestFor(r)+'</span></div>'+
    '<div class="rcm"><div><b>'+Math.round(r.k)+'</b><span>kcal</span></div>'+
    '<div><b>'+Math.round(r.p)+'</b><span>prot</span></div>'+
    '<div><b>'+Math.round(r.c)+'</b><span>carb</span></div>'+
    '<div><b>'+Math.round(r.f)+'</b><span>fat</span></div></div></div></article>';
}
function macroRows(got,tgt){
  var rows=[['Calories','kcal',got.kcal,tgt.kcal,'pk'],['Protein','g',got.p,tgt.p,'pp'],
            ['Carbs','g',got.c,tgt.c,'pc'],['Fat','g',got.f,tgt.f,'pf']];
  return rows.map(function(x){
    var pc=Math.min(100,x[3]?x[2]/x[3]*100:0);
    return '<div class="mrow"><div class="spread"><span>'+x[0]+'</span>'+
      '<em>'+Math.round(x[2])+' / '+Math.round(x[3])+' '+x[1]+'</em></div>'+
      '<div class="bar"><i class="'+x[4]+'" style="width:'+pc+'%"></i></div></div>';
  }).join('');
}

/* ============ router ============ */
var TABS=[['home','Home'],['recipes','Recipes'],['grocery','Grocery'],['training','Training'],['calendar','Calendar'],['learn','Learn']];
function go(h){location.hash=h;}
function route(){
  var h=(location.hash||'#/home').slice(2).split('/');
  var v=h[0]||'home';
  var m=$('#view');
  m.innerHTML = v==='r'?vRecipe(h[1]) : v==='recipes'?vRecipes() : v==='grocery'?vGrocery()
    : v==='training'?vTraining() : v==='calendar'?vCalendar() : v==='learn'?vLearn() : vHome();
  try{window.scrollTo(0,0);}catch(e){}
  $$('.tab,.btmnav button').forEach(function(b){b.classList.toggle('on',b.dataset.v===(v==='r'?'recipes':v));});
  $$('#who button').forEach(function(b){b.classList.toggle('on',b.dataset.w===S.who);});
  bind();
}
window.addEventListener('hashchange',route);

/* ============ HOME ============ */
function vHome(){
  var ds=today(),d=dayLog(ds),tgt=dayTarget(S.who,d.workout),got=eaten(ds),b=tgt.base;
  var p=S.prof[S.who];
  return '<div class="page"><div class="phead"><h1>'+pretty(ds)+'</h1>'+
   '<p>Everything starts here. Numbers first, explanations last.</p></div>'+

   '<div class="sec"><h2>What '+(S.who==='j'?'I':'she')+' need'+(S.who==='j'?'':'s')+' today</h2>'+
   '<p class="sub">Adjusted for the session logged below. Change the training and it moves.</p>'+
   '<div class="grid g2">'+
     '<div class="card pad"><div class="stats" style="margin-bottom:16px">'+
       '<div class="stat acc"><b>'+Math.round(tgt.kcal)+'</b><span>Calories</span></div>'+
       '<div class="stat"><b>'+Math.round(tgt.p)+'g</b><span>Protein</span></div>'+
       '<div class="stat"><b>'+Math.round(tgt.c)+'g</b><span>Carbs</span></div>'+
       '<div class="stat"><b>'+Math.round(tgt.f)+'g</b><span>Fat</span></div>'+
       '<div class="stat"><b>'+Math.round(tgt.fib)+'g</b><span>Fiber</span></div>'+
       '<div class="stat"><b>'+Math.round(tgt.w)+'</b><span>oz water</span></div></div>'+
       '<label class="f"><span>Trained today</span><select id="hTrain">'+
        Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
       '</select></label><div class="note">'+E(tgt.tr.why)+'</div>'+
       '<div class="row"><button class="b" id="hCard">Download today card</button>'+
       '<button class="b o" data-nav="#/recipes">Find a meal</button></div></div>'+

     '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">Logged so far</h3>'+
       macroRows(got,tgt)+
       '<div class="spread sm" style="margin-top:14px;padding-top:12px;border-top:1px solid var(--line)">'+
       '<span class="muted">'+d.meals.length+' item'+(d.meals.length===1?'':'s')+' logged</span>'+
       '<b>'+$$$(got.cost)+' spent</b></div>'+
       '<div class="row" style="margin-top:12px"><button class="b o" data-nav="#/calendar">Open the log</button></div>'+
       (got.kcal>0?'<div class="note" style="margin-top:12px"><b>'+Math.max(0,Math.round(tgt.kcal-got.kcal))+
        ' kcal</b> and <b>'+Math.max(0,Math.round(tgt.p-got.p))+' g protein</b> left to go.</div>':'')+
     '</div></div></div>'+

   '<div class="sec"><h2>Calculator</h2><p class="sub">Change anything and every number below updates. Saved per person.</p>'+
   '<div class="card pad"><div class="fr">'+
     fld('Weight (lb)','cW','number',p.w)+fld('Height (in)','cH','number',p.h)+
     fld('Age','cA','number',p.age)+fld('Body fat %','cB','number',p.bf)+
     '<label class="f"><span>Sex</span><select id="cS"><option value="m"'+(p.sex==='m'?' selected':'')+'>Male</option>'+
     '<option value="f"'+(p.sex==='f'?' selected':'')+'>Female</option></select></label>'+
     '<label class="f"><span>Activity</span><select id="cAct">'+
       [[1.2,'Sedentary desk'],[1.3,'Desk + training'],[1.4,'Light standing + training'],
        [1.5,'Bench work + training'],[1.55,'Engraving shop + daily training'],[1.62,'On feet all shift'],
        [1.7,'Very active'],[1.8,'Trade work + training'],[1.9,'Heavy labour']].map(function(o){
        return '<option value="'+o[0]+'"'+(Math.abs(p.act-o[0])<0.001?' selected':'')+'>'+o[0]+' '+o[1]+'</option>';}).join('')+
     '</select></label>'+
     '<label class="f"><span>Goal</span><select id="cG">'+
       [[0.78,'Cut'],[0.85,'Slow cut'],[1.0,'Maintain'],[1.03,'Recomp'],[1.06,'Slow gain'],
        [1.09,'Lean gain'],[1.15,'Bulk']].map(function(o){
        return '<option value="'+o[0]+'"'+(Math.abs(p.goal-o[0])<0.001?' selected':'')+'>'+o[1]+' ('+o[0]+'x)</option>';}).join('')+
     '</select></label>'+
     '<label class="f"><span>Protein g/lb</span><select id="cP">'+
       [0.7,0.8,0.9,1.0,1.1,1.25,1.4].map(function(o){
        return '<option value="'+o+'"'+(Math.abs(p.pf-o)<0.001?' selected':'')+'>'+o+'</option>';}).join('')+
     '</select></label>'+
   '</div><div id="cOut"></div>'+
   '<div class="row" style="margin-top:14px"><button class="b" id="cSave">Save to profile</button>'+
   '<button class="b o" id="cCard">Download nutrient card</button></div></div></div>'+

   '<div class="sec"><h2>Both of us</h2><p class="sub">Household totals for the shop.</p>'+
   (function(){var j=calc(S.prof.j),a=calc(S.prof.a);
    return '<div class="stats"><div class="stat hero"><b>'+Math.round(j.kcal+a.kcal)+'</b><span>Household kcal</span></div>'+
    '<div class="stat"><b>'+Math.round(j.p+a.p)+'g</b><span>Protein</span></div>'+
    '<div class="stat"><b>'+Math.round(j.kcal)+'</b><span>Me</span></div>'+
    '<div class="stat"><b>'+Math.round(a.kcal)+'</b><span>Aaliyah</span></div>'+
    '<div class="stat"><b>'+$$$((j.kcal+a.kcal)/1000*3.92)+'</b><span>Food / day</span></div>'+
    '<div class="stat"><b>'+$$$((j.kcal+a.kcal)/1000*3.92*30)+'</b><span>Food / month</span></div></div>';})()+
   '</div>'+

   '<div class="sec"><h2>Jump to</h2><div class="grid g4">'+
     tile('#/recipes','Recipe book',all().length+' recipes')+
     tile('#/grocery','Grocery list',S.grocery.length+' items')+
     tile('#/training','Training','Macro builder')+
     tile('#/calendar','Calendar','Track the day')+
     tile('#/learn','Learn','Why any of it works')+
     tile('#/recipes','Favourites',S.fav.length+' saved')+
   '</div></div></div>';
}
function fld(l,id,t,v){return '<label class="f"><span>'+l+'</span><input id="'+id+'" type="'+t+'" value="'+v+'" step="0.5"></label>';}
function tile(h,t,s){return '<a class="card pad" href="'+h+'" style="text-decoration:none"><b style="display:block;color:var(--navy);font-size:15px">'+t+'</b><span class="muted sm">'+s+'</span></a>';}

function calcOut(){
  var p=readProf(),r=calc(p);
  $('#cOut').innerHTML='<div class="stats" style="margin-top:6px">'+
   '<div class="stat acc"><b>'+Math.round(r.kcal)+'</b><span>Calories</span></div>'+
   '<div class="stat"><b>'+Math.round(r.p)+'g</b><span>Protein</span></div>'+
   '<div class="stat"><b>'+Math.round(r.c)+'g</b><span>Carbs</span></div>'+
   '<div class="stat"><b>'+Math.round(r.f)+'g</b><span>Fat</span></div>'+
   '<div class="stat"><b>'+Math.round(r.fib)+'g</b><span>Fiber</span></div>'+
   '<div class="stat"><b>'+Math.round(r.w)+'</b><span>oz water</span></div></div>'+
   '<div class="tw" style="margin-top:12px"><table><tr><th>Value</th><th>Result</th><th>How</th></tr>'+
   tr('RMR (Mifflin)',Math.round(r.rmr),'(10 x kg)+(6.25 x cm)-(5 x age)'+(p.sex==='f'?'-161':'+5'))+
   tr('RMR (Katch)',Math.round(r.katch),'370 + 21.6 x lean kg')+
   tr('Maintenance',Math.round(r.tdee),'RMR x '+p.act)+
   tr('Lean mass',Math.round(r.lbm)+' lb','weight x (1 - bf)')+
   tr('FFMI (norm)',r.ffmi.toFixed(1),'natural ceiling about 25')+
   tr('Weekly change',(r.rate>=0?'+':'')+r.rate.toFixed(2)+' lb','(intake - maintenance) x 7 / 3500')+
   tr('Per feeding',Math.round(r.p/4)+' g protein','daily protein / 4 meals')+
   '</table></div>';
}
function tr(a,b,c){return '<tr><td>'+a+'</td><td><b>'+b+'</b></td><td class="muted sm">'+c+'</td></tr>';}
function readProf(){
  return {sex:$('#cS').value,w:+$('#cW').value,h:+$('#cH').value,age:+$('#cA').value,
    bf:+$('#cB').value,act:+$('#cAct').value,goal:+$('#cG').value,pf:+$('#cP').value,
    name:S.prof[S.who].name};
}

/* ============ RECIPES ============ */
var flt={q:'',cat:'',tag:'',sort:'match'};
function vRecipes(){
  return '<div class="page"><div class="phead"><h1>Recipe book</h1>'+
   '<p>'+all().length+' recipes. Everything gluten-free, mains vegetarian, clean meat and fish in its own section.</p></div>'+
   '<div class="sec"><h2>For today</h2><p class="sub" id="recWhy"></p><div class="grid g3" id="recOut"></div></div>'+
   (S.fav.length?'<div class="sec"><h2>Favourites</h2><div class="grid g3">'+
     S.fav.map(function(i){var r=byId(i);return r?rcard(r):'';}).join('')+'</div></div>':'')+
   (Object.keys(S.lists).some(function(k){return S.lists[k].length;})?
     '<div class="sec"><h2>My lists</h2>'+Object.keys(S.lists).map(function(k){
       if(!S.lists[k].length)return '';
       return '<h3 style="margin:18px 0 10px">'+E(k)+' <span class="muted sm">'+S.lists[k].length+'</span></h3>'+
        '<div class="grid g3">'+S.lists[k].map(function(i){var r=byId(i);return r?rcard(r):'';}).join('')+'</div>';
     }).join('')+'</div>':'')+
   (S.mine.length?'<div class="sec"><h2>My own recipes</h2><div class="grid g3">'+S.mine.map(rcard).join('')+'</div></div>':'')+
   '<div class="sec"><h2>Everything</h2>'+
   '<div class="card pad" style="margin-bottom:14px"><div class="fr">'+
     '<label class="f"><span>Search</span><input id="fq" placeholder="tofu, oats, burger..." value="'+E(flt.q)+'"></label>'+
     '<label class="f"><span>Category</span><select id="fcat"><option value="">All</option>'+
      ['Breakfast','Lunch/Dinner','Snack','Drink','SDA Meat/Fish'].map(function(c){
        return '<option'+(flt.cat===c?' selected':'')+'>'+c+'</option>';}).join('')+'</select></label>'+
     '<label class="f"><span>Best for</span><select id="ftag"><option value="">Anything</option>'+
      ['LEUCINE PRIORITY','HIGH FIBER','CHEAT MEAL','HEALTHY DESSERT','QUICK','BUDGET FRIENDLY','NO-COOK','MEAL PREP','LOW CALORIE','HIGH CALORIE','OMEGA-3 RICH'].map(function(t){
        return '<option value="'+t+'"'+(flt.tag===t?' selected':'')+'>'+t.charAt(0)+t.slice(1).toLowerCase()+'</option>';}).join('')+'</select></label>'+
     '<label class="f"><span>Sort</span><select id="fsort">'+
      [['match','Recommended'],['p','Most protein'],['k','Most calories'],['kl','Fewest calories'],['c','Cheapest'],['t','Fastest']].map(function(o){
        return '<option value="'+o[0]+'"'+(flt.sort===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select></label>'+
   '</div><div class="row"><button class="b o s" id="addOwn">Add my own recipe</button>'+
   '<button class="b o s" id="expAll">Export backup</button><button class="b o s" id="impAll">Import backup</button>'+
   '<span class="muted sm right" id="fcount"></span></div></div>'+
   '<div class="grid g3" id="allOut"></div></div></div>';
}
function recommend(){
  var ds=today(),d=dayLog(ds),tgt=dayTarget(S.who,d.workout),got=eaten(ds),t=tgt.tr;
  var lk=Math.max(180,tgt.kcal-got.kcal), lp=Math.max(10,tgt.p-got.p);
  var meals=Math.max(1,Math.round(lk/620));
  var pk=lk/meals, pp=lp/meals;
  var sc=all().map(function(r){
    var s=0;
    s-=Math.abs(r.k-pk)/26;
    s+=Math.min(r.p,pp*1.4)*2.0;
    s+=(r.leu||0)*7;
    t.tag.forEach(function(x){if(r.tg.indexOf(x)>=0)s+=17;});
    if(S.fav.indexOf(r.id)>=0)s+=14;
    if(r.cat==='SDA Meat/Fish')s-=6;
    if(r.t<=20)s+=5;
    return {r:r,s:s};
  }).sort(function(a,b){return b.s-a.s;}).slice(0,6);
  var e=$('#recWhy'); if(e) e.innerHTML='After <b>'+E(t.n)+'</b>, about <b>'+Math.round(lk)+
    ' kcal</b> and <b>'+Math.round(lp)+' g protein</b> left across roughly '+meals+' more '+(meals===1?'meal':'meals')+'. '+E(t.why);
  var o=$('#recOut'); if(o){o.innerHTML=sc.map(function(x){return rcard(x.r);}).join('');}
}
function renderAll(){
  var out=$('#allOut'); if(!out)return;
  var L=all().filter(function(r){
    if(flt.cat&&r.cat!==flt.cat)return false;
    if(flt.tag&&r.tg.indexOf(flt.tag)<0)return false;
    if(flt.q){var q=flt.q.toLowerCase();
      if(r.n.toLowerCase().indexOf(q)<0 && !(r.ing||[]).some(function(i){
        var nm=(i[1]&&ING[i[1]])?ING[i[1]].n:String(i[0]);
        return nm.toLowerCase().indexOf(q)>=0||String(i[0]).toLowerCase().indexOf(q)>=0;}))return false;}
    return true;});
  var s=flt.sort;
  L.sort(function(a,b){return s==='p'?b.p-a.p:s==='k'?b.k-a.k:s==='kl'?a.k-b.k:
    s==='c'?cps(a)-cps(b):s==='t'?a.t-b.t:(b.p*2+b.leu*6)-(a.p*2+a.leu*6);});
  $('#fcount').textContent=L.length+' shown';
  out.innerHTML=L.length?L.map(rcard).join(''):'<div class="empty">Nothing matches. Loosen a filter.</div>';
}

/* ============ RECIPE DETAIL ============ */
function vRecipe(id){
  var r=byId(id);
  if(!r)return '<div class="page"><div class="empty">Recipe not found. <a href="#/recipes">Back to the book</a></div></div>';
  var ph=S.photos[r.id],c=CATC[r.cat]||CATC['My recipe'],f=S.fav.indexOf(r.id)>=0;
  var sv=r.sv||1;
  return '<div class="page">'+
  '<div class="row" style="padding:16px 0 10px"><button class="b o s" data-nav="#/recipes">Back to recipes</button>'+
  '<button class="b o s" data-fav="'+r.id+'">'+(f?'\u2605 Favourited':'\u2606 Favourite')+'</button>'+
  '<button class="b o s" data-list="'+r.id+'">Add to list</button>'+
  '<button class="b o s" data-photo="'+r.id+'">'+(ph?'Change photo':'Add photo')+'</button>'+
  '<button class="b o s" data-cardpng="'+r.id+'">Save card</button>'+
  '<button class="b s" data-log="'+r.id+'">Log to today</button>'+
  '<button class="b o s" data-groc="'+r.id+'">Add to grocery</button></div>'+

  '<div class="dhero" style="background:linear-gradient(135deg,'+c[0]+','+c[1]+')">'+
   (ph?'<img src="'+ph+'" alt="">':'')+'<div class="scrim"></div><div class="in">'+
   '<div class="chips"><span class="chip" style="background:rgba(255,255,255,.2);color:#fff">'+r.id+'</span>'+
   '<span class="chip" style="background:rgba(255,255,255,.2);color:#fff">'+E(r.cat)+'</span></div>'+
   '<h1>'+E(r.n)+'</h1>'+
   '<div class="sm" style="opacity:.9">'+r.t+' min &middot; '+(r.diff||'EASY').toLowerCase()+
   ' &middot; makes '+sv+' &middot; '+$$$(cps(r))+' per serving, '+$$$(ctot(r))+' total</div></div></div>'+

  '<div class="sec"><div class="stats">'+
   '<div class="stat acc"><b>'+Math.round(r.k)+'</b><span>Calories</span></div>'+
   '<div class="stat"><b>'+Math.round(r.p)+'g</b><span>Protein</span></div>'+
   '<div class="stat"><b>'+Math.round(r.c)+'g</b><span>Carbs</span></div>'+
   '<div class="stat"><b>'+Math.round(r.f)+'g</b><span>Fat</span></div>'+
   '<div class="stat"><b>'+Math.round(r.fib||0)+'g</b><span>Fiber</span></div>'+
   '<div class="stat"><b>'+(r.leu||0).toFixed(1)+'g</b><span>Leucine</span></div></div>'+
   '<p class="muted sm" style="margin-top:8px">Per serving. Whole recipe: '+Math.round(r.k*sv)+
   ' kcal, '+Math.round(r.p*sv)+' g protein, '+$$$(ctot(r))+'.</p></div>'+

  '<div class="grid g2">'+
   '<div class="card pad"><h3 style="font-size:15px;margin-bottom:10px">Ingredients '+
   '<span class="muted sm" id="svLabel">for '+sv+'</span></h3>'+
   '<div class="row" style="margin-bottom:10px"><span class="muted sm">Scale</span>'+
   [0.5,1,1.5,2,3].map(function(x){return '<button class="pill'+(x===1?' on':'')+'" data-scale="'+x+'">'+x+'x</button>';}).join('')+
   '</div><ul class="ing" id="ingList"></ul></div>'+
   '<div class="card pad"><h3 style="font-size:15px;margin-bottom:10px">Method</h3>'+
   '<ol class="stp">'+(r.st||[]).map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ol></div></div>'+

  (r.prep?'<div class="note" style="margin-top:16px"><b>Note.</b> '+E(r.prep)+'</div>':'')+
  '<div class="grid g2" style="margin-top:14px">'+
   (r.storage?'<div class="card pad"><h4 class="muted xs" style="letter-spacing:1px">STORAGE</h4><p class="sm" style="margin:6px 0 0">'+E(r.storage)+'</p></div>':'')+
   ((r.subs||[]).length?'<div class="card pad"><h4 class="muted xs" style="letter-spacing:1px">SUBSTITUTIONS</h4><ul class="sm" style="margin:6px 0 0;padding-left:17px">'+
     r.subs.map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ul></div>':'')+
   ((r.vars||[]).length?'<div class="card pad"><h4 class="muted xs" style="letter-spacing:1px">VARIATIONS</h4><ul class="sm" style="margin:6px 0 0;padding-left:17px">'+
     r.vars.map(function(s){return '<li>'+E(s)+'</li>';}).join('')+'</ul></div>':'')+
   (r.tg.length?'<div class="card pad"><h4 class="muted xs" style="letter-spacing:1px">TAGS</h4><div class="chips" style="margin-top:8px">'+
     r.tg.map(function(t){return '<span class="chip">'+E(t)+'</span>';}).join('')+'</div></div>':'')+
  '</div></div>';
}
function drawIng(r,mult){
  var el=$('#ingList'); if(!el)return;
  el.innerHTML=(r.ing||[]).map(function(i){
    var measure=i[0],key=i[1],g=i[2]||0,pr=0,name=key&&ING[key]?ING[key].n:measure;
    if(key&&ING[key]){var q=ING[key];pr=(g*mult/100)*best(q);}
    var gs=g?Math.round(g*mult)+' g':'';
    var sub=(key&&ING[key]&&measure)?' <span class="muted xs">('+E(measure)+')</span>':'';
    return '<li><b>'+gs+'</b><span>'+E(name)+sub+'</span>'+(pr?'<span class="c">'+$$$(pr)+'</span>':'')+'</li>';
  }).join('');
  var s=$('#svLabel'); if(s)s.textContent='for '+((r.sv||1)*mult);
}

/* ============ GROCERY ============ */
function vGrocery(){
  var byA={};S.grocery.forEach(function(it,i){(byA[it.aisle]=byA[it.aisle]||[]).push([it,i]);});
  var order=AISLES.map(function(a){return a[0];}).concat(['Other']);
  var tot=S.grocery.reduce(function(a,i){return a+(i.done?0:i.price*i.qty);},0);
  var done=S.grocery.filter(function(i){return i.done;}).length;
  return '<div class="page"><div class="phead"><h1>Grocery list</h1>'+
   '<p>Grouped the way the store is laid out. Each item is priced at whichever of Walmart Fort Collins or Costco Timnath is cheaper for that item.</p></div>'+
   '<div class="card pad" style="margin-bottom:14px"><div class="stats">'+
     '<div class="stat acc"><b>'+$$$(tot)+'</b><span>Still to buy</span></div>'+
     '<div class="stat"><b>'+S.grocery.length+'</b><span>Items</span></div>'+
     '<div class="stat"><b>'+done+'</b><span>In the cart</span></div>'+
     '<div class="stat"><b>'+Object.keys(byA).length+'</b><span>Aisles</span></div></div>'+
   '<div class="row" style="margin-top:14px">'+
     '<button class="b" id="gAdd">Add ingredient</button>'+
     '<button class="b o" id="gFromList">Add from a list</button>'+
     '<button class="b o" id="gTxt">Download checklist</button>'+
     '<button class="b o" id="gCsv">Download CSV</button>'+
     '<button class="b o dz right" id="gClear">Clear list</button></div></div>'+
   (S.grocery.length? order.filter(function(a){return byA[a];}).map(function(a){
     var items=byA[a],st=items.reduce(function(x,p){return x+(p[0].done?0:p[0].price*p[0].qty);},0);
     return '<div class="card" style="margin-bottom:12px;overflow:hidden">'+
      '<div class="aisle">'+E(a)+'<span>'+$$$(st)+'</span></div>'+
      items.map(function(p){var it=p[0],i=p[1];
        return '<div class="gitem'+(it.done?' done':'')+'">'+
        '<input type="checkbox" data-gtoggle="'+i+'"'+(it.done?' checked':'')+'>'+
        '<span class="gn">'+E(it.name)+'<div class="gq">'+E(it.qty>1?it.qty+' x ':'')+E(it.note||'')+'</div></span>'+
        '<span class="gp">'+$$$(it.price*it.qty)+'</span>'+
        '<button class="b o s" data-gedit="'+i+'">Edit</button>'+
        '<button class="b o s dz" data-gdel="'+i+'">&times;</button></div>';}).join('')+'</div>';
   }).join('') : '<div class="empty"><p>Nothing on the list yet.</p><p class="sm">Add ingredients directly, or open a recipe and hit <b>Add to grocery</b>.</p></div>')+
   '</div>';
}

/* ============ TRAINING ============ */
function vTraining(){
  var ds=today(),d=dayLog(ds);
  var rows=Object.keys(TRAIN).map(function(k){
    var t=dayTarget(S.who,k),b=t.base;
    return '<tr'+(d.workout===k?' style="background:var(--ice)"':'')+'><td><b>'+TRAIN[k].n+'</b></td>'+
     '<td>'+Math.round(t.kcal)+'</td><td>'+Math.round(t.p)+' g</td><td>'+Math.round(t.c)+' g</td>'+
     '<td>'+Math.round(t.f)+' g</td><td class="muted sm">'+E(TRAIN[k].why.split('.')[0])+'.</td></tr>';}).join('');
  return '<div class="page"><div class="phead"><h1>Training</h1>'+
   '<p>What each session type does to the day\'s numbers, and where to log it.</p></div>'+
   '<div class="sec"><h2>Log today</h2>'+
   '<div class="card pad"><label class="f"><span>Session</span><select id="tTrain">'+
    Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
   '</select></label><label class="f"><span>Notes, lifts, PRs</span><textarea id="tNotes" rows="3" placeholder="Weighted pull-up 3x5 +25 lb...">'+E(d.notes||'')+'</textarea></label>'+
   '<button class="b" id="tSave">Save to today</button></div></div>'+
   '<div class="sec"><h2>Macro builder</h2><p class="sub">Same body, different session. This is how much the day actually shifts.</p>'+
   '<div class="tw"><table><tr><th>Session</th><th>Calories</th><th>Protein</th><th>Carbs</th><th>Fat</th><th>Why</th></tr>'+rows+'</table></div></div>'+
   '<div class="sec"><h2>The split this is built around</h2>'+
   '<div class="tw"><table><tr><th>Day</th><th>Focus</th><th>Nutrition emphasis</th></tr>'+
    [['Mon','Push + skill','Protein and leucine, moderate carbs'],
     ['Tue','Pull + core','Protein, leucine, iron-rich picks'],
     ['Wed','Legs','Highest carb and calorie day of the week'],
     ['Thu','Skill + conditioning','Omega-3, nutrient density, fluids'],
     ['Fri','Full body','Protein and carbs both up'],
     ['Sat','Rest or light','Fiber and micronutrients, protein holds'],
     ['Sun','Legs or full body + meal prep','Big carbs, then batch cook']].map(function(r){
      return '<tr><td><b>'+r[0]+'</b></td><td>'+r[1]+'</td><td class="muted">'+r[2]+'</td></tr>';}).join('')+
   '</table></div>'+
   '<div class="note">Back, side delts, quads, hamstrings and calves are the lagging areas, so pull and leg days carry the most volume. Planche progression sits at the front of skill days while the nervous system is fresh.</div></div></div>';
}

/* ============ CALENDAR ============ */
var calM=new Date().getMonth(), calY=new Date().getFullYear(), calSel=today();
function vCalendar(){
  var first=new Date(calY,calM,1),start=first.getDay(),dim=new Date(calY,calM+1,0).getDate();
  var cells='';
  for(var i=0;i<start;i++)cells+='<div class="day out"></div>';
  for(var dnum=1;dnum<=dim;dnum++){
    var ds=calY+'-'+p2(calM+1)+'-'+p2(dnum);
    var lg=S.days[ds],e=lg?eaten(ds):null;
    cells+='<div class="day'+(ds===today()?' today':'')+(ds===calSel?' sel':'')+'" data-day="'+ds+'">'+
      '<span class="dn">'+dnum+'</span>'+
      (lg&&(lg.meals.length||lg.workout!=='rest')?'<div class="dots">'+
        (lg.meals.length?'<span class="dot"></span>':'')+
        (lg.workout&&lg.workout!=='rest'?'<span class="dot w"></span>':'')+'</div>':'')+
      (e&&e.kcal?'<span class="dk">'+Math.round(e.kcal)+'</span>':'')+'</div>';
  }
  var d=dayLog(calSel),tgt=dayTarget(S.who,d.workout),got=eaten(calSel);
  return '<div class="page"><div class="phead"><h1>Calendar</h1><p>Opens on today. Tap any day to edit it.</p></div>'+
   '<div class="grid g2"><div class="card pad">'+
    '<div class="spread" style="margin-bottom:12px"><button class="b o s" id="cPrev">&larr;</button>'+
    '<b>'+new Date(calY,calM,1).toLocaleDateString(undefined,{month:'long',year:'numeric'})+'</b>'+
    '<button class="b o s" id="cNext">&rarr;</button></div>'+
    '<div class="cal">'+['S','M','T','W','T','F','S'].map(function(x){return '<div class="dow">'+x+'</div>';}).join('')+cells+'</div>'+
    '<div class="row" style="margin-top:12px"><button class="b o s" id="calCsv">Download month CSV</button>'+
    '<button class="b o s" id="calToday">Jump to today</button></div></div>'+

   '<div class="card pad"><h3 style="font-size:16px;margin-bottom:4px">'+pretty(calSel)+'</h3>'+
    '<p class="muted sm" style="margin-bottom:14px">'+(calSel===today()?'Today':'')+'</p>'+
    macroRows(got,tgt)+
    '<label class="f" style="margin-top:14px"><span>Training that day</span><select id="dTrain">'+
     Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
    '</select></label>'+
    '<label class="f"><span>Notes</span><textarea id="dNotes" rows="2">'+E(d.notes||'')+'</textarea></label>'+
    '<h4 class="muted xs" style="letter-spacing:1px;margin:14px 0 8px">MEALS LOGGED</h4>'+
    (d.meals.length?'<ul class="ing">'+d.meals.map(function(m,i){var r=byId(m.id);if(!r)return '';
      return '<li><b>'+(m.sv||1)+'x</b><span><a href="#/r/'+r.id+'">'+E(r.n)+'</a></span>'+
      '<span class="c">'+Math.round(r.k*(m.sv||1))+' kcal</span>'+
      '<button class="b o s dz" data-unlog="'+i+'">&times;</button></li>';}).join('')+'</ul>'
      :'<p class="muted sm">Nothing logged. Open a recipe and hit Log to today.</p>')+
    '<div class="row" style="margin-top:12px"><button class="b" id="dSave">Save day</button>'+
    '<button class="b o" data-nav="#/recipes">Add a meal</button></div></div></div></div>';
}

/* ============ LEARN ============ */
function vLearn(){
  return '<div class="page"><div class="phead"><h1>Learn</h1>'+
   '<p>The reasoning behind every number on the other pages. Kept back here so it is not in the way every time the app opens.</p></div>'+
   LEARN.map(function(g){
     return '<div class="sec"><h2>'+E(g[0])+'</h2>'+g[1].map(function(q){
       return '<details><summary>'+E(q[0])+'</summary><div class="dc">'+q[1]+'</div></details>';}).join('')+'</div>';
   }).join('')+
   '<div class="note">The full 300-page reference, with every formula, the complete micronutrient chapter and the printable index, is in the PDF alongside this file.</div></div>';
}

/* ============ modals ============ */
function modal(title,body,foot){
  var m=document.createElement('div');m.className='mask';
  m.innerHTML='<div class="modal"><div class="mhead"><h3>'+E(title)+'</h3><button class="x">&times;</button></div>'+
    '<div class="mbody">'+body+'</div>'+(foot?'<div class="mfoot">'+foot+'</div>':'')+'</div>';
  m.addEventListener('click',function(e){if(e.target===m||e.target.classList.contains('x'))m.remove();});
  document.body.appendChild(m);return m;
}
function pickList(id){
  var names=Object.keys(S.lists);
  var m=modal('Add to a list',
    names.map(function(n){return '<div class="pickrow" data-pick="'+E(n)+'"><b>'+E(n)+'</b>'+
      '<span class="muted sm right">'+S.lists[n].length+'</span></div>';}).join('')+
    '<label class="f" style="margin-top:14px"><span>Or make a new list</span>'+
    '<input id="newList" placeholder="Sunday prep"></label>',
    '<button class="b o" data-close>Cancel</button><button class="b" id="mkList">Create and add</button>');
  m.addEventListener('click',function(e){
    var p=e.target.closest('[data-pick]');
    if(p){var n=p.dataset.pick;if(S.lists[n].indexOf(id)<0)S.lists[n].push(id);save();m.remove();toast('Added to '+n);route();return;}
    if(e.target.hasAttribute('data-close'))m.remove();
    if(e.target.id==='mkList'){var v=$('#newList',m).value.trim();if(!v)return;
      if(!S.lists[v])S.lists[v]=[];if(S.lists[v].indexOf(id)<0)S.lists[v].push(id);
      save();m.remove();toast('Added to '+v);route();}
  });
}
function ingBrowser(cb){
  var keys=Object.keys(ING).sort(function(a,b){return ING[a].n.localeCompare(ING[b].n);});
  var m=modal('Ingredient list',
    '<label class="f"><span>Search '+keys.length+' ingredients</span><input id="ibq" placeholder="Type to filter..." autocomplete="off"></label>'+
    '<p class="muted sm">Alphabetical, so it is easy to check something is not already on the list under another name.</p>'+
    '<div id="ibList" style="max-height:44vh;overflow:auto"></div>'+
    '<label class="f" style="margin-top:12px;border-top:1px solid var(--line);padding-top:12px">'+
    '<span>Not in the list? Add it manually</span><input id="ibNew" placeholder="Name"></label>'+
    '<div class="fr"><label class="f"><span>Price $</span><input id="ibP" type="number" step="0.01" value="2.00"></label>'+
    '<label class="f"><span>Aisle</span><select id="ibA">'+AISLES.map(function(a){return '<option>'+E(a[0])+'</option>';}).join('')+
    '<option>Other</option></select></label></div>',
    '<button class="b o" data-close>Cancel</button><button class="b" id="ibAdd">Add manual item</button>');
  function draw(){
    var q=($('#ibq',m).value||'').toLowerCase();
    var L=keys.filter(function(k){return ING[k].n.toLowerCase().indexOf(q)>=0;}).slice(0,140);
    $('#ibList',m).innerHTML=L.map(function(k){var g=ING[k];
      return '<div class="pickrow" data-ing="'+k+'"><b>'+E(g.n)+'</b>'+
      '<span class="muted sm right">'+$$$(best(g))+'/100g &middot; '+E(bestStore(g))+' &middot; '+E(g.aisle)+'</span></div>';}).join('')
      ||'<p class="muted sm">No match. Add it manually below.</p>';
  }
  draw();$('#ibq',m).addEventListener('input',draw);
  m.addEventListener('click',function(e){
    var p=e.target.closest('[data-ing]');
    if(p){var k=p.dataset.ing,g=ING[k];
      cb({key:k,name:g.n,qty:1,price:best(g)*2,aisle:g.aisle,note:'about 200 g',done:false});
      m.remove();return;}
    if(e.target.hasAttribute('data-close'))m.remove();
    if(e.target.id==='ibAdd'){var n=$('#ibNew',m).value.trim();if(!n)return;
      cb({key:null,name:n,qty:1,price:+$('#ibP',m).value||0,aisle:$('#ibA',m).value,note:'',done:false});m.remove();}
  });
}
function addOwnRecipe(){
  var m=modal('Add my own recipe',
    '<div class="fr">'+fld('Name','oN','text','')+fld('Servings','oS','number',2)+fld('Minutes','oT','number',20)+'</div>'+
    '<div class="fr">'+fld('Calories / serving','oK','number',600)+fld('Protein g','oP','number',40)+
    fld('Carbs g','oC','number',55)+fld('Fat g','oF','number',18)+fld('Cost / serving $','oCo','number',3)+'</div>'+
    '<label class="f"><span>Category</span><select id="oCat"><option>Breakfast</option><option>Lunch/Dinner</option>'+
    '<option>Snack</option><option>Drink</option><option>SDA Meat/Fish</option></select></label>'+
    '<label class="f"><span>Ingredients, one per line</span><textarea id="oI" rows="5" placeholder="200 g chicken breast"></textarea></label>'+
    '<label class="f"><span>Method, one step per line</span><textarea id="oM" rows="5"></textarea></label>'+
    '<label class="f"><span>Photo</span><input type="file" id="oPh" accept="image/*"></label>',
    '<button class="b o" data-close>Cancel</button><button class="b" id="oSave">Save recipe</button>');
  var photo=null;
  $('#oPh',m).addEventListener('change',function(){var f=this.files[0];if(f)shrink(f,760,function(d){photo=d;});});
  m.addEventListener('click',function(e){
    if(e.target.hasAttribute('data-close'))m.remove();
    if(e.target.id==='oSave'){
      var n=$('#oN',m).value.trim();if(!n){toast('Needs a name');return;}
      var id='X-'+(S.mine.length+1),sv=+$('#oS',m).value||1,co=+$('#oCo',m).value||0;
      var rec={id:id,n:n,cat:$('#oCat',m).value,sv:sv,t:+$('#oT',m).value||20,diff:'MODERATE',
        k:+$('#oK',m).value||0,p:+$('#oP',m).value||0,c:+$('#oC',m).value||0,f:+$('#oF',m).value||0,
        fib:0,leu:0,tg:[],cw:co*sv,cws:co,cc:co*sv,ccs:co,
        ing:$('#oI',m).value.split('\n').filter(Boolean).map(function(l){return [l.trim(),null,0];}),
        st:$('#oM',m).value.split('\n').filter(Boolean),storage:'',prep:'',subs:[],vars:[]};
      S.mine.push(rec);if(photo)S.photos[id]=photo;save();m.remove();toast('Saved');go('#/r/'+id);
    }
  });
}
function shrink(file,max,cb){
  var fr=new FileReader();
  fr.onload=function(){var img=new Image();img.onload=function(){
    var s=Math.min(1,max/Math.max(img.width,img.height)),c=document.createElement('canvas');
    c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);
    c.getContext('2d').drawImage(img,0,0,c.width,c.height);cb(c.toDataURL('image/jpeg',.72));};
    img.src=fr.result;};
  fr.readAsDataURL(file);
}
function pickPhoto(id){
  var i=document.createElement('input');i.type='file';i.accept='image/*';
  i.onchange=function(){var f=i.files[0];if(f)shrink(f,760,function(d){S.photos[id]=d;save();toast('Photo saved');route();});};
  i.click();
}

/* ============ downloads ============ */
function cardPNG(r){
  var W=900,H=1280,cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
  var g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,'#14140F');g.addColorStop(.58,'#1F3A2C');g.addColorStop(1,'#2C6B50');
  x.fillStyle=g;x.fillRect(0,0,W,H);x.fillStyle='#A8CDB8';x.fillRect(0,0,W,7);
  x.fillStyle='#A8CDB8';x.font='700 19px Helvetica,Arial';
  x.fillText(r.id+'   \u00B7   '+(r.cat||'').toUpperCase(),54,80);
  x.fillStyle='#fff';x.font='800 52px Helvetica,Arial';
  var y=146+wrap(x,r.n,54,146,790,56);
  var mac=[[Math.round(r.k),'KCAL'],[Math.round(r.p)+'g','PROTEIN'],[Math.round(r.c)+'g','CARBS'],
           [Math.round(r.f)+'g','FAT'],[Math.round(r.fib||0)+'g','FIBER'],[(r.leu||0).toFixed(1)+'g','LEUCINE']];
  var bw=(790-25)/6;
  mac.forEach(function(mm,i){var bx=54+i*(bw+5);
    x.fillStyle='rgba(255,255,255,.10)';x.fillRect(bx,y,bw,90);
    x.fillStyle='#fff';x.font='800 25px Helvetica,Arial';x.textAlign='center';x.fillText(String(mm[0]),bx+bw/2,y+41);
    x.fillStyle='#A8CDB8';x.font='700 11px Helvetica,Arial';x.fillText(mm[1],bx+bw/2,y+66);x.textAlign='left';});
  y+=130;
  x.fillStyle='#1F4D3A';x.fillRect(54,y,790,62);x.fillStyle='#fff';x.font='700 23px Helvetica,Arial';
  x.fillText('Makes '+(r.sv||1)+'   \u00B7   '+$$$(cps(r))+'/serving   \u00B7   '+$$$(ctot(r))+' total   \u00B7   '+r.t+' min',78,y+39);
  y+=100;
  x.fillStyle='#A8CDB8';x.font='700 16px Helvetica,Arial';x.fillText('INGREDIENTS',54,y);y+=28;
  x.fillStyle='#E6EDE7';x.font='400 18px Helvetica,Arial';
  (r.ing||[]).slice(0,15).forEach(function(it){var nm=(it[1]&&ING[it[1]])?ING[it[1]].n:it[0];
    var g=it[2]?Math.round(it[2])+' g ':'';x.fillText('\u2022  '+g+nm,54,y);y+=26;});
  y+=20;x.fillStyle='#A8CDB8';x.font='700 16px Helvetica,Arial';x.fillText('METHOD',54,y);y+=28;
  x.fillStyle='#C4DAF3';x.font='400 16px Helvetica,Arial';
  (r.st||[]).slice(0,6).forEach(function(s,i){y+=wrap(x,(i+1)+'. '+s,54,y,790,23)+7;});
  x.fillStyle='#5C8CC4';x.font='700 13px Helvetica,Arial';x.fillText('The Meal Handbook',54,H-40);
  var a=document.createElement('a');a.download=r.id+'-'+r.n.replace(/[^a-z0-9]+/gi,'-').toLowerCase()+'.png';
  a.href=cv.toDataURL('image/png');a.click();
}
function nutrientCard(){
  var p=S.prof[S.who],r=calc(p),d=dayLog(today()),t=dayTarget(S.who,d.workout);
  var W=900,H=1120,cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
  var g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,'#14140F');g.addColorStop(1,'#1F4D3A');
  x.fillStyle=g;x.fillRect(0,0,W,H);x.fillStyle='#1F4D3A';x.fillRect(0,0,W,7);
  x.fillStyle='#A8CDB8';x.font='700 18px Helvetica,Arial';x.fillText('DAILY NUTRIENT TARGETS',54,74);
  x.fillStyle='#fff';x.font='800 54px Helvetica,Arial';x.fillText(p.name,54,140);
  x.fillStyle='#A9C6E4';x.font='400 20px Helvetica,Arial';
  x.fillText(pretty(today())+'   \u00B7   '+TRAIN[d.workout].n,54,176);
  var items=[['Calories',Math.round(t.kcal)],['Protein',Math.round(t.p)+' g'],['Carbs',Math.round(t.c)+' g'],
             ['Fat',Math.round(t.f)+' g'],['Fiber',Math.round(t.fib)+' g'],['Water',Math.round(t.w)+' oz']];
  var y=220;
  items.forEach(function(it,i){
    var col=i%2,row=Math.floor(i/2),bx=54+col*400,by=y+row*118;
    x.fillStyle='rgba(255,255,255,.09)';x.fillRect(bx,by,380,100);
    x.fillStyle='#A8CDB8';x.font='700 13px Helvetica,Arial';x.fillText(it[0].toUpperCase(),bx+22,by+34);
    x.fillStyle='#fff';x.font='800 42px Helvetica,Arial';x.fillText(String(it[1]),bx+22,by+80);});
  y+=380;
  x.fillStyle='#A8CDB8';x.font='700 16px Helvetica,Arial';x.fillText('HOW THESE ARE BUILT',54,y);y+=32;
  x.fillStyle='#E6EDE7';x.font='400 17px Helvetica,Arial';
  [['RMR',Math.round(r.rmr)+' kcal, Mifflin-St Jeor'],
   ['Maintenance',Math.round(r.tdee)+' kcal at '+p.act+'x activity'],
   ['Goal',(p.goal>1?'+':'')+Math.round((p.goal-1)*100)+'% of maintenance'],
   ['Protein',p.pf+' g per lb bodyweight'],
   ['Session',TRAIN[d.workout].n+' adjustment applied'],
   ['Expected',(r.rate>=0?'+':'')+r.rate.toFixed(2)+' lb per week']].forEach(function(l){
    x.fillStyle='#A8CDB8';x.fillText(l[0],54,y);x.fillStyle='#E6EDE7';x.fillText(l[1],250,y);y+=31;});
  x.fillStyle='#5C8CC4';x.font='700 13px Helvetica,Arial';x.fillText('The Meal Handbook',54,H-40);
  var a=document.createElement('a');a.download='targets-'+p.name.toLowerCase()+'-'+today()+'.png';
  a.href=cv.toDataURL('image/png');a.click();
}
function wrap(x,t,px,py,mw,lh){
  var w=String(t).split(' '),line='',yy=py,used=0;
  for(var i=0;i<w.length;i++){var test=line+w[i]+' ';
    if(x.measureText(test).width>mw&&line){x.fillText(line,px,yy);line=w[i]+' ';yy+=lh;used+=lh;}else line=test;}
  x.fillText(line,px,yy);return used+lh;
}

/* ============ events ============ */
function bind(){
  var t=$('#hTrain')||$('#tTrain');
  if($('#hTrain'))$('#hTrain').onchange=function(){dayLog(today()).workout=this.value;save();route();};
  if($('#cOut')){calcOut();['cW','cH','cA','cB','cS','cAct','cG','cP'].forEach(function(i){
    var e=$('#'+i);if(e){e.oninput=calcOut;e.onchange=calcOut;}});}
  if($('#cSave'))$('#cSave').onclick=function(){S.prof[S.who]=readProf();save();toast('Profile saved');route();};
  if($('#cCard'))$('#cCard').onclick=nutrientCard;
  if($('#hCard'))$('#hCard').onclick=nutrientCard;
  if($('#recOut')){recommend();renderAll();
    ['fq','fcat','ftag','fsort'].forEach(function(i){var e=$('#'+i);if(!e)return;
      e.oninput=function(){flt.q=$('#fq').value;renderAll();};
      e.onchange=function(){flt.cat=$('#fcat').value;flt.tag=$('#ftag').value;flt.sort=$('#fsort').value;renderAll();};});
    if($('#addOwn'))$('#addOwn').onclick=addOwnRecipe;
    if($('#expAll'))$('#expAll').onclick=function(){dl('meal-handbook-backup.json',JSON.stringify(S,null,1),'application/json');};
    if($('#impAll'))$('#impAll').onclick=function(){var i=document.createElement('input');i.type='file';i.accept='.json';
      i.onchange=function(){var f=i.files[0];var fr=new FileReader();fr.onload=function(){
        try{S=JSON.parse(fr.result);save();toast('Restored');route();}catch(e){toast('That file did not read');}};fr.readAsText(f);};i.click();};
  }
  var scaleBtns=$$('[data-scale]');
  if(scaleBtns.length){var id=location.hash.split('/')[2],r=byId(id);
    drawIng(r,1);
    scaleBtns.forEach(function(b){b.onclick=function(){scaleBtns.forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');drawIng(r,+b.dataset.scale);};});}
  if($('#tSave'))$('#tSave').onclick=function(){var d=dayLog(today());
    d.workout=$('#tTrain').value;d.notes=$('#tNotes').value;save();toast('Logged');route();};
  if($('#dSave'))$('#dSave').onclick=function(){var d=dayLog(calSel);
    d.workout=$('#dTrain').value;d.notes=$('#dNotes').value;save();toast('Day saved');route();};
  if($('#cPrev'))$('#cPrev').onclick=function(){calM--;if(calM<0){calM=11;calY--;}route();};
  if($('#cNext'))$('#cNext').onclick=function(){calM++;if(calM>11){calM=0;calY++;}route();};
  if($('#calToday'))$('#calToday').onclick=function(){var d=new Date();calM=d.getMonth();calY=d.getFullYear();calSel=today();route();};
  if($('#calCsv'))$('#calCsv').onclick=exportMonth;
  if($('#gAdd'))$('#gAdd').onclick=function(){ingBrowser(function(it){S.grocery.push(it);save();route();});};
  if($('#gFromList'))$('#gFromList').onclick=groceryFromList;
  if($('#gTxt'))$('#gTxt').onclick=groceryTxt;
  if($('#gCsv'))$('#gCsv').onclick=groceryCsv;
  if($('#gClear'))$('#gClear').onclick=function(){if(confirm('Clear the whole list?')){S.grocery=[];save();route();}};
}
document.addEventListener('click',function(e){
  var el;
  if((el=e.target.closest('[data-nav]'))){go(el.dataset.nav);return;}
  if((el=e.target.closest('[data-fav]'))){e.stopPropagation();var id=el.dataset.fav,i=S.fav.indexOf(id);
    if(i>=0)S.fav.splice(i,1);else S.fav.push(id);save();route();return;}
  if((el=e.target.closest('[data-list]'))){pickList(el.dataset.list);return;}
  if((el=e.target.closest('[data-photo]'))){pickPhoto(el.dataset.photo);return;}
  if((el=e.target.closest('[data-cardpng]'))){cardPNG(byId(el.dataset.cardpng));return;}
  if((el=e.target.closest('[data-log]'))){var d=dayLog(today());d.meals.push({id:el.dataset.log,sv:1});
    save();toast('Logged to today');return;}
  if((el=e.target.closest('[data-groc]'))){addRecipeToGrocery(byId(el.dataset.groc));return;}
  if((el=e.target.closest('[data-unlog]'))){dayLog(calSel).meals.splice(+el.dataset.unlog,1);save();route();return;}
  if((el=e.target.closest('[data-day]'))&&el.dataset.day){calSel=el.dataset.day;route();return;}
  if((el=e.target.closest('[data-gdel]'))){S.grocery.splice(+el.dataset.gdel,1);save();route();return;}
  if((el=e.target.closest('[data-gedit]'))){editGrocery(+el.dataset.gedit);return;}
  if((el=e.target.closest('[data-go]'))){go('#/r/'+el.dataset.go);return;}
},false);
document.addEventListener('change',function(e){
  var el=e.target.closest('[data-gtoggle]');
  if(el){S.grocery[+el.dataset.gtoggle].done=el.checked;save();route();}
},false);

/* ============ grocery helpers ============ */
function addRecipeToGrocery(r){
  if(!r||!r.ing){toast('No ingredients on that one');return;}
  var n=0;
  r.ing.forEach(function(i){
    var key=i[1],g=i[2]||0;if(!key||!ING[key])return;
    var q=ING[key],ex=null;
    S.grocery.forEach(function(it){if(it.key===key)ex=it;});
    var price=(g/100)*best(q);
    if(ex){ex.grams=(ex.grams||0)+g;ex.price+=price;ex.note=Math.round(ex.grams)+' g';}
    else{S.grocery.push({key:key,name:q.n,qty:1,price:price,grams:g,note:Math.round(g)+' g',aisle:q.aisle,done:false});}
    n++;
  });
  save();toast(n+' ingredients added');
}
function groceryFromList(){
  var names=Object.keys(S.lists).filter(function(k){return S.lists[k].length;});
  if(S.fav.length)names.unshift('Favourites');
  if(!names.length){toast('No lists with anything in them yet');return;}
  var m=modal('Add every ingredient from',names.map(function(n){
    var c=(n==='Favourites'?S.fav:S.lists[n]).length;
    return '<div class="pickrow" data-pick="'+E(n)+'"><b>'+E(n)+'</b><span class="muted sm right">'+c+' recipes</span></div>';}).join(''));
  m.addEventListener('click',function(e){var p=e.target.closest('[data-pick]');if(!p)return;
    var ids=p.dataset.pick==='Favourites'?S.fav:S.lists[p.dataset.pick];
    ids.forEach(function(i){var r=byId(i);if(r)addRecipeToGrocery(r);});
    m.remove();route();});
}
function editGrocery(i){
  var it=S.grocery[i];
  var m=modal('Edit item','<div class="fr">'+
    '<label class="f"><span>Name</span><input id="eN" value="'+E(it.name)+'"></label>'+
    '<label class="f"><span>Quantity</span><input id="eQ" type="number" step="1" value="'+it.qty+'"></label>'+
    '<label class="f"><span>Price $</span><input id="eP" type="number" step="0.01" value="'+it.price.toFixed(2)+'"></label>'+
    '<label class="f"><span>Aisle</span><select id="eA">'+AISLES.map(function(a){
      return '<option'+(it.aisle===a[0]?' selected':'')+'>'+E(a[0])+'</option>';}).join('')+
    '<option'+(it.aisle==='Other'?' selected':'')+'>Other</option></select></label></div>'+
    '<label class="f"><span>Note</span><input id="eNo" value="'+E(it.note||'')+'"></label>',
    '<button class="b o dz" id="eDel">Delete</button><button class="b" id="eOk">Save</button>');
  m.addEventListener('click',function(e){
    if(e.target.id==='eOk'){it.name=$('#eN',m).value;it.qty=+$('#eQ',m).value||1;
      it.price=+$('#eP',m).value||0;it.aisle=$('#eA',m).value;it.note=$('#eNo',m).value;
      save();m.remove();route();}
    if(e.target.id==='eDel'){S.grocery.splice(i,1);save();m.remove();route();}});
}
function groceryTxt(){
  var byA={};S.grocery.forEach(function(it){(byA[it.aisle]=byA[it.aisle]||[]).push(it);});
  var out='GROCERY LIST  '+pretty(today())+'\n'+'Best price of Walmart Fort Collins / Costco Timnath'+
    '\n'+'='.repeat(46)+'\n\n';
  var tot=0;
  AISLES.map(function(a){return a[0];}).concat(['Other']).forEach(function(a){
    if(!byA[a])return;
    out+=a.toUpperCase()+'\n';
    byA[a].forEach(function(it){var c=it.price*it.qty;tot+=c;
      out+='  [ ] '+it.name+(it.note?'  ('+it.note+')':'')+'  '+$$$(c)+'\n';});
    out+='\n';});
  out+='='.repeat(46)+'\nESTIMATED TOTAL  '+$$$(tot)+'\n';
  dl('grocery-'+today()+'.txt',out);
}
function groceryCsv(){
  var rows=[['Aisle','Item','Qty','Note','UnitPrice','LineTotal','InCart']];
  S.grocery.forEach(function(it){rows.push([it.aisle,it.name,it.qty,it.note||'',it.price.toFixed(2),
    (it.price*it.qty).toFixed(2),it.done?'yes':'no']);});
  dl('grocery-'+today()+'.csv',rows.map(function(r){return r.map(function(c){
    return '"'+String(c).replace(/"/g,'""')+'"';}).join(',');}).join('\n'),'text/csv');
}
function exportMonth(){
  var rows=[['Date','Training','Calories','Protein','Carbs','Fat','Fiber','Cost','Meals','Notes']];
  Object.keys(S.days).sort().forEach(function(ds){
    var d=S.days[ds],e=eaten(ds);
    rows.push([ds,TRAIN[d.workout]?TRAIN[d.workout].n:d.workout,Math.round(e.kcal),Math.round(e.p),
      Math.round(e.c),Math.round(e.f),Math.round(e.fib),e.cost.toFixed(2),
      d.meals.map(function(m){var r=byId(m.id);return r?r.n:m.id;}).join(' | '),d.notes||'']);});
  dl('nutrition-log.csv',rows.map(function(r){return r.map(function(c){
    return '"'+String(c).replace(/"/g,'""')+'"';}).join(',');}).join('\n'),'text/csv');
}

/* ============ chrome ============ */
function chrome(){
  $('#tabs').innerHTML=TABS.map(function(t){
    return '<button class="tab" data-v="'+t[0]+'" onclick="location.hash=\'#/'+t[0]+'\'">'+t[1]+'</button>';}).join('');
  $('#btm').innerHTML=TABS.map(function(t){
    return '<button data-v="'+t[0]+'" onclick="location.hash=\'#/'+t[0]+'\'">'+ICO[t[0]]+'<span>'+t[1]+'</span></button>';}).join('');
  $('#who').innerHTML=['j','a'].map(function(k){
    return '<button data-w="'+k+'"'+(S.who===k?' class="on"':'')+'>'+E(S.prof[k].name)+'</button>';}).join('');
  $('#who').onclick=function(e){var b=e.target.closest('[data-w]');if(!b)return;
    S.who=b.dataset.w;save();route();};
}
var ICO={home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10l9-7 9 7v10a2 2 0 01-2 2H5a2 2 0 01-2-2z"/></svg>',
recipes:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h13a2 2 0 012 2v14H6a2 2 0 01-2-2z"/><path d="M8 8h7M8 12h7"/></svg>',
grocery:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4h2l2 12h11"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/><path d="M7 8h14l-2 6H8"/></svg>',
training:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6v12M18 6v12M3 9v6M21 9v6M6 12h12"/></svg>',
calendar:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
learn:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 7c0-2 2-3 4-3h4v14h-4c-2 0-4 1-4 3z"/><path d="M12 7c0-2-2-3-4-3H4v14h4c2 0 4 1 4 3z"/></svg>'};

chrome();
if(!location.hash)location.hash='#/home';
route();
})();
</script>
"""
