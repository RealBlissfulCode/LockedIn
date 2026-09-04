# -*- coding: utf-8 -*-
"""Signing up, and what a brand new account actually gets.

Nothing is seeded blindly. The questionnaire is short on purpose and every
answer does something you can see: the diet answers filter the recipe book, the
goal answers rank it, the training answers build a starting exercise list, and
the money answer lays out the categories most people forget with the amounts
left blank, because what a haircut costs is not something an app should guess.
"""

APP_SETUP = r"""
/* ============================ what a new account gets ============================ */

/* The categories almost everyone has and half of people forget, with no
   numbers in them. Seeing the row is the useful part. Filling it in is the
   user's job and guessing on their behalf would be worse than blank. */
var COST_SKELETON=[
 ['Housing (rent)','Rent'],['Housing (rent)','Renters insurance'],
 ['Housing (buy)','Mortgage'],['Housing (buy)','Property tax'],
 ['Housing (buy)','Home insurance'],['Housing (buy)','Repairs and upkeep'],
 ['Utilities','Electric'],['Utilities','Gas'],['Utilities','Water and sewer'],
 ['Utilities','Trash'],['Utilities','Internet'],['Utilities','Phone'],
 ['Living','Groceries'],['Living','Eating out'],['Living','Fuel'],
 ['Living','Car insurance'],['Living','Car registration'],['Living','Car maintenance'],
 ['Living','Household supplies'],['Living','Clothing'],['Living','Haircuts'],
 ['Living','Subscriptions'],['Living','Gifts and birthdays'],['Living','Pets'],
 ['Health','Health insurance'],['Health','Doctor and copays'],['Health','Dental'],
 ['Health','Prescriptions'],['Health','Gym'],
 ['Debt','Credit cards'],['Debt','Student loans'],['Debt','Car payment'],
 ['Savings','Emergency fund'],['Savings','Retirement'],['Savings','Sinking fund']
];

function buildCostSkeleton(who){
  return COST_SKELETON.map(function(r){
    return {id:uid(),section:r[0],name:r[1],who:who,
            low:0,real:0,high:0,actual:null,off:false};
  });
}

/* Hard filters come from what somebody cannot or will not eat. Soft ones rank
   what is left. Mixing the two is how you end up recommending steak to a
   vegetarian because it scored well on protein. */
var DIET_Q=[
 ['vegetarian','Vegetarian','No meat or fish'],
 ['vegan','Vegan','No animal products at all'],
 ['dairyfree','Dairy free','No milk, cheese, yogurt or whey'],
 ['eggfree','Egg free','No eggs'],
 ['peanutfree','Peanut free','No peanuts or peanut butter'],
 ['treenutfree','Tree nut free','No almonds, cashews, walnuts'],
 ['soyfree','Soy free','No soy, tofu or tamari'],
 ['fishfree','No fish','No fish or seafood'],
 ['cornfree','Corn free','No corn, cornmeal or cornstarch']
];

/* Each one maps to tags the build already computes, so these are real filters
   rather than labels. */
var GOAL_Q=[
 ['protein','High protein','Lean gain, or holding muscle while cutting',
  ['HIGH PROTEIN','VERY HIGH PROTEIN','MUSCLE-BUILDING PRIORITY']],
 ['gym','Gym gains','Built around training days and recovery',
  ['MUSCLE-BUILDING PRIORITY','POST-WORKOUT FRIENDLY','LEUCINE PRIORITY']],
 ['lean','Leaner','Lower calorie, high fullness, easier to stay under',
  ['LOW CALORIE','HIGH SATIETY','HIGH FIBER']],
 ['bulk','Eating more','Higher calorie without eating all day',
  ['HIGH CALORIE','TWO-MEAL-DAY FRIENDLY']],
 ['balanced','Just healthy','Even macros and a wide spread of micronutrients',
  ['BALANCED MACRO','HIGH MICRONUTRIENT DENSITY','OMEGA-3 RICH']],
 ['quick','Quick','Ten minutes or less, most nights',['QUICK']],
 ['cheap','Cheap','Sorted by what it actually costs to make',[]]
];

var TRAIN_GOAL_Q=[
 ['hyp','Build muscle','Hypertrophy work, moderate reps'],
 ['str','Get stronger','Heavier, lower reps, longer rests'],
 ['lean','Lose fat','Full body plus conditioning'],
 ['mob','Move better','Mobility and stability first'],
 ['gen','Stay in shape','A bit of everything']
];
var EQUIP_Q=[
 ['Bodyweight','Nothing at all'],
 ['Dumbbells','Dumbbells'],
 ['Resistance band','Resistance bands'],
 ['Pull-up bar','A pull-up bar'],
 ['Elevated surface','A bench or a chair'],
 ['Barbell','A barbell'],
 ['Machine','Gym machines']
];

/* ============================ the wizard ============================ */
var setupStep=0, setupAns=null;

function startOnboarding(){
  setupStep=0;
  setupAns={name:(ACCOUNT&&ACCOUNT.name)||'',sex:'m',w:'',h:'',age:'',
            house:'',others:[],diet:[],goals:[],
            train:{goal:'gen',days:3,eq:['Bodyweight'],exp:'new'},
            money:true};
  drawSetup();
}

function setupShell(title,sub,body,foot,step,total){
  var app=document.getElementById('app');
  app.hidden=false;
  /* No tabs, no member switcher, no sync pill while somebody is still
     answering questions. There is nothing behind them yet to go and look at. */
  document.body.classList.add('unlocked','signup');
  var g=document.getElementById('gate');
  if(g&&g.parentNode) g.parentNode.removeChild(g);
  document.getElementById('view').innerHTML=
    '<div class="page setup"><div class="setuphead">'+
    '<div class="setupbar"><i style="width:'+Math.round(step/total*100)+'%"></i></div>'+
    '<p class="setupstep">Step '+step+' of '+total+'</p>'+
    '<h1>'+E(title)+'</h1><p>'+E(sub)+'</p></div>'+
    '<div class="setupbody">'+body+'</div>'+
    '<div class="setupfoot">'+foot+'</div></div>';
  window.scrollTo(0,0);
}

function pickList(items,chosen,attr){
  return '<div class="picks">'+items.map(function(it){
    var on=chosen.indexOf(it[0])>=0;
    return '<button class="pick'+(on?' on':'')+'" data-'+attr+'="'+E(it[0])+'">'+
      '<b>'+E(it[1])+'</b>'+(it[2]?'<span>'+E(it[2])+'</span>':'')+'</button>';
  }).join('')+'</div>';
}

var SETUP_TOTAL=5;

function drawSetup(){
  var a=setupAns;
  if(setupStep===0){
    setupShell('Who are you?','Your name is what shows up around the app. The rest '+
      'sets your calorie and protein targets, and you can skip it and fill it in later.',
      '<div class="fr">'+
      '<label class="f"><span>Name</span><input id="suName" value="'+E(a.name)+'" placeholder="Your name"></label>'+
      '<label class="f"><span>Sex</span><select id="suSex">'+opt([['m','Male'],['f','Female']],a.sex)+'</select></label>'+
      '<label class="f"><span>Weight (lb)</span><input id="suW" type="number" value="'+E(a.w)+'" placeholder="optional"></label>'+
      '<label class="f"><span>Height (in)</span><input id="suH" type="number" step="0.5" value="'+E(a.h)+'" placeholder="optional"></label>'+
      '<label class="f"><span>Age</span><input id="suAge" type="number" value="'+E(a.age)+'" placeholder="optional"></label>'+
      '</div>',
      '<button class="b" id="suNext">Continue</button>',1,SETUP_TOTAL);
    $('#suNext').onclick=function(){
      a.name=$('#suName').value.trim()||'Me';
      a.sex=$('#suSex').value;
      a.w=$('#suW').value; a.h=$('#suH').value; a.age=$('#suAge').value;
      setupStep++; drawSetup();
    };
    return;
  }
  if(setupStep===1){
    var seats=HOUSE?HOUSE.seats:2;
    setupShell('Anyone else?','Add the people you plan with. You can put someone on the '+
      'meal plan and the schedule now and invite them to their own login later, or leave '+
      'this empty and it stays just you.',
      '<div id="suPeople"></div>'+
      '<div class="row" style="margin-top:12px">'+
      '<button class="b o s" id="suAdd">Add someone</button></div>'+
      '<p class="sm muted" style="margin-top:14px">Your plan has '+seats+' seats, '+
      'and you are using one of them.</p>',
      '<button class="b o" id="suBack">Back</button><button class="b" id="suNext">Continue</button>',
      2,SETUP_TOTAL);
    drawSetupPeople();
    $('#suAdd').onclick=function(){
      if(a.others.length+1>=(HOUSE?HOUSE.seats:2)){
        toast('That is every seat on this plan'); return;
      }
      a.others.push({name:'',sex:'f'}); drawSetupPeople();
    };
    $('#suBack').onclick=function(){setupStep--;drawSetup();};
    $('#suNext').onclick=function(){
      a.others=a.others.filter(function(o){return o.name.trim();});
      setupStep++; drawSetup();
    };
    return;
  }
  if(setupStep===2){
    setupShell('How do you eat?','Anything you pick here is a hard filter. Recipes that '+
      'break it never show up again, so be honest rather than aspirational.',
      pickList(DIET_Q,a.diet,'diet')+
      '<h3 class="ctitle" style="margin-top:26px">And what are you going for?</h3>'+
      '<p class="sub" style="margin-bottom:14px">These sort the book rather than cut it '+
      'down. Pick as many as fit.</p>'+
      pickList(GOAL_Q,a.goals,'goal'),
      '<button class="b o" id="suBack">Back</button><button class="b" id="suNext">Continue</button>',
      3,SETUP_TOTAL);
    $$('[data-diet]').forEach(function(b){b.onclick=function(){
      togglePick(a.diet,this.dataset.diet);
      /* Vegan is vegetarian with more taken out, so ticking it ticks both and
         un-ticking vegetarian cannot leave vegan stranded. */
      if(a.diet.indexOf('vegan')>=0&&a.diet.indexOf('vegetarian')<0) a.diet.push('vegetarian');
      if(a.diet.indexOf('vegetarian')<0) a.diet=a.diet.filter(function(x){return x!=='vegan';});
      drawSetup();};});
    $$('[data-goal]').forEach(function(b){b.onclick=function(){
      togglePick(a.goals,this.dataset.goal); drawSetup();};});
    $('#suBack').onclick=function(){setupStep--;drawSetup();};
    $('#suNext').onclick=function(){setupStep++;drawSetup();};
    return;
  }
  if(setupStep===3){
    setupShell('Training','This builds your starting exercise list. Nothing here is '+
      'locked in, it just stops you staring at two hundred exercises on day one.',
      '<h3 class="ctitle">What are you training for?</h3>'+
      pickList(TRAIN_GOAL_Q,[a.train.goal],'tgoal')+
      '<h3 class="ctitle" style="margin-top:26px">What have you got?</h3>'+
      pickList(EQUIP_Q,a.train.eq,'teq')+
      '<div class="fr" style="margin-top:22px">'+
      '<label class="f"><span>Days a week</span><select id="suDays">'+
        opt([['2','2'],['3','3'],['4','4'],['5','5'],['6','6']],String(a.train.days))+'</select></label>'+
      '<label class="f"><span>How long have you trained</span><select id="suExp">'+
        opt([['new','Just starting'],['some','On and off'],['yrs','Years']],a.train.exp)+'</select></label>'+
      '</div>',
      '<button class="b o" id="suBack">Back</button><button class="b" id="suNext">Continue</button>',
      4,SETUP_TOTAL);
    $$('[data-tgoal]').forEach(function(b){b.onclick=function(){
      a.train.goal=this.dataset.tgoal; drawSetup();};});
    $$('[data-teq]').forEach(function(b){b.onclick=function(){
      togglePick(a.train.eq,this.dataset.teq);
      if(!a.train.eq.length) a.train.eq=['Bodyweight'];
      drawSetup();};});
    $('#suBack').onclick=function(){
      a.train.days=+$('#suDays').value; a.train.exp=$('#suExp').value;
      setupStep--;drawSetup();};
    $('#suNext').onclick=function(){
      a.train.days=+$('#suDays').value; a.train.exp=$('#suExp').value;
      setupStep++;drawSetup();};
    return;
  }
  setupShell('Money','Start the budget with the categories most people forget, all left '+
    'blank. Seeing the row is the useful part. What a haircut costs where you live is not '+
    'something we should be guessing at.',
    '<div class="picks">'+
    '<button class="pick'+(setupAns.money?' on':'')+'" data-money="1">'+
    '<b>Lay out the categories</b><span>About thirty rows across housing, utilities, '+
    'living, health, debt and savings, every amount empty</span></button>'+
    '<button class="pick'+(setupAns.money?'':' on')+'" data-money="0">'+
    '<b>Start from nothing</b><span>An empty budget you build yourself</span></button>'+
    '</div>',
    '<button class="b o" id="suBack">Back</button>'+
    '<button class="b" id="suDone">Finish</button>',5,SETUP_TOTAL);
  $$('[data-money]').forEach(function(b){b.onclick=function(){
    setupAns.money=this.dataset.money==='1'; drawSetup();};});
  $('#suBack').onclick=function(){setupStep--;drawSetup();};
  $('#suDone').onclick=finishOnboarding;
}

function drawSetupPeople(){
  var box=$('#suPeople'); if(!box) return;
  var a=setupAns;
  box.innerHTML=a.others.length?a.others.map(function(o,i){
    return '<div class="card pad" style="margin-top:10px"><div class="fr">'+
    '<label class="f"><span>Name</span><input data-pn="'+i+'" value="'+E(o.name)+'" placeholder="Their name"></label>'+
    '<label class="f"><span>Sex</span><select data-ps="'+i+'">'+opt([['m','Male'],['f','Female']],o.sex)+'</select></label>'+
    '</div><button class="b o s dz" data-prm="'+i+'">Remove</button></div>';
  }).join(''):'<div class="empty sm">Just you so far.</div>';
  $$('[data-pn]',box).forEach(function(i2){i2.oninput=function(){
    a.others[+this.dataset.pn].name=this.value;};});
  $$('[data-ps]',box).forEach(function(i2){i2.onchange=function(){
    a.others[+this.dataset.ps].sex=this.value;};});
  $$('[data-prm]',box).forEach(function(b){b.onclick=function(){
    a.others.splice(+this.dataset.prm,1); drawSetupPeople();};});
}

function togglePick(arr,v){
  var i=arr.indexOf(v);
  if(i>=0) arr.splice(i,1); else arr.push(v);
}

function finishOnboarding(){
  var a=setupAns;
  var me=blankMember(a.name,a.sex);
  if(a.w) me.w=num(a.w);
  if(a.h) me.h=num(a.h);
  if(a.age) me.age=num(a.age);
  S.members=[me];
  a.others.forEach(function(o){
    S.members.push(blankMember(o.name.trim(),o.sex));
  });
  S.who=me.id;
  S.household=(HOUSE&&HOUSE.name)||'';
  S.prefs={diet:a.diet,goals:a.goals,train:a.train};
  S.fin.costs=a.money?buildCostSkeleton(shared()?EVERYONE:me.id):[];
  S.fin.jobs=[];
  S.shop={active:'Weekly shop',lists:{'Weekly shop':{cat:'Groceries',fav:true,items:[]}}};
  S.fav=startingFavourites(24);
  S.onboarded=true;
  document.body.classList.remove('signup');
  save();
  api('auth.php?do=onboarded',{body:{}});
  if(ACCOUNT) ACCOUNT.onboarded=true;
  chrome();
  location.hash='#/meals';
  route();
  syncStart();
  toast('You are set up. Everything here is yours to change.');
}

/* ============================ using the answers ============================ */

/* Hard filters first, then a score. A recipe that breaks a diet is gone, not
   ranked last, because ranking it last still shows it on a short list. */
function dietOK(r,diet){
  var df=r.df||[];
  for(var i=0;i<diet.length;i++) if(df.indexOf(diet[i])<0) return false;
  return true;
}
function goalScore(r,goals){
  var tg=r.tg||[], sc=0;
  goals.forEach(function(g){
    if(g==='cheap'){ sc+=Math.max(0,3-cps(r)); return; }
    var def=GOAL_Q.filter(function(x){return x[0]===g;})[0];
    if(!def) return;
    def[3].forEach(function(t){ if(tg.indexOf(t)>=0) sc+=2; });
  });
  return sc;
}
function recipesFor(diet,goals){
  var out=R.filter(function(r){return dietOK(r,diet||[]);});
  var g=goals||[];
  if(g.length) out.sort(function(x,y){return goalScore(y,g)-goalScore(x,g);});
  return out;
}
/* A starting book rather than the whole database, spread across the meal
   categories so the first thing somebody sees is a usable day of food. */
function startingFavourites(n){
  var pr=S.prefs||{};
  var byCat={}, out=[];
  recipesFor(pr.diet,pr.goals).forEach(function(r){
    (byCat[r.cat]=byCat[r.cat]||[]).push(r);
  });
  var cats=Object.keys(byCat), i=0;
  while(out.length<n){
    var added=false;
    for(var c=0;c<cats.length;c++){
      var list=byCat[cats[c]];
      if(i<list.length){ out.push(list[i].id); added=true; if(out.length>=n) break; }
    }
    if(!added) break;
    i++;
  }
  return out;
}

/* ============================ meal plans ============================
   Fill a run of days against somebody's calorie target. Greedy rather than
   clever: take the categories in the order people actually eat them, pick the
   recipe that gets the day closest to target without going over by much, and
   never repeat anything inside the window. Good enough that the plan is worth
   editing, which is the point. A plan you cannot argue with is a plan you
   cannot use. */
function makeMealPlan(opts){
  opts=opts||{};
  var who=opts.who||ME();
  var days=opts.days||7;
  var start=opts.start||today();
  var pr=S.prefs||{};
  var pool=recipesFor(pr.diet,pr.goals);
  if(opts.favOnly&&S.fav.length){
    var favSet={}; S.fav.forEach(function(id){favSet[id]=1;});
    var narrowed=pool.filter(function(r){return favSet[r.id];});
    if(narrowed.length>=8) pool=narrowed;
  }
  if(!pool.length) return null;

  var byCat={};
  pool.forEach(function(r){ (byCat[r.cat]=byCat[r.cat]||[]).push(r); });
  var order=['Breakfast','Lunch/Dinner','Lunch/Dinner','Snack'];

  var used={}, plan=[];
  var d0=dOf(start);
  for(var d=0;d<days;d++){
    var dt=new Date(d0.getFullYear(),d0.getMonth(),d0.getDate()+d);
    var ds=dt.getFullYear()+'-'+p2(dt.getMonth()+1)+'-'+p2(dt.getDate());
    var wk=(S.days[ds]||{}).workout||'rest';
    var tgt=dayTarget(who,wk);
    var got={kcal:0,p:0}, meals=[];
    order.forEach(function(cat,slot){
      var list=byCat[cat]||byCat['Lunch/Dinner']||pool;
      var left=order.length-slot;
      var want=(tgt.kcal-got.kcal)/Math.max(1,left);
      var best=null,bestScore=1e9;
      for(var i=0;i<list.length;i++){
        var r=list[i];
        if(used[r.id]) continue;
        /* Distance from the share of the day this slot should carry, with a
           nudge towards hitting protein, which is the target people actually
           miss. */
        var miss=Math.abs(r.k-want);
        var pGap=Math.max(0,(tgt.p-got.p)/Math.max(1,left)-r.p);
        var score=miss+pGap*12;
        if(score<bestScore){ bestScore=score; best=r; }
      }
      if(!best) return;
      used[best.id]=1;
      got.kcal+=best.k; got.p+=best.p;
      meals.push({id:best.id,q:1,who:who,at:defMealTime(slot)});
    });
    /* Let the pool come back round rather than running dry on day four. */
    if(Object.keys(used).length>pool.length-8) used={};
    plan.push({date:ds,meals:meals,kcal:Math.round(got.kcal),p:Math.round(got.p),
               target:tgt.kcal,protein:tgt.p});
  }
  return plan;
}

function applyMealPlan(plan,replace){
  if(!plan) return 0;
  var n=0;
  plan.forEach(function(day){
    var d=dayLog(day.date);
    if(replace) d.meals=[];
    day.meals.forEach(function(m){ d.meals.push(m); n++; });
  });
  save();
  return n;
}
"""

APP_PLANNER = r"""
/* ============================ the meal plan screen ============================
   Generate, look at it, change your mind, then put it on the calendar. The
   plan is never written anywhere until somebody presses the button, because a
   plan that applies itself is a plan you have to undo. */
var lastPlan=null, planDays=7, planWho=null, planFav=false;

function planTotals(p){
  var k=0,pr=0,c=0;
  p.forEach(function(d){k+=d.kcal;pr+=d.p;c+=d.target;});
  return {kcal:Math.round(k/p.length),p:Math.round(pr/p.length),target:Math.round(c/p.length)};
}

function vMealPlan(){
  var who=planWho||ME();
  var pr=S.prefs||{};
  var pool=recipesFor(pr.diet,pr.goals).length;
  return '<div class="page"><div class="phead"><h1>Meal plan</h1>'+
   '<p>Built from the '+pool+' recipes that fit how you eat, against '+E(WHO(who))+'&#39;s '+
   'calorie and protein targets for each day. Training days get more, rest days get less.</p></div>'+

   '<div class="row toolbar">'+
   (shared()?'<label class="f inline"><span>For</span><select id="mpWho">'+
     opt(MEMS().map(function(m){return [m.id,m.name];}),who)+'</select></label>':'')+
   '<label class="f inline"><span>Days</span><select id="mpDays">'+
     opt([['3','3'],['5','5'],['7','7'],['14','14']],String(planDays))+'</select></label>'+
   '<button class="b" id="mpGo">Generate</button>'+
   '<button class="b o s'+(planFav?' on':'')+'" id="mpFav">'+
     (planFav?'Favourites only':'Whole book')+'</button>'+
   '<button class="b o" data-nav="meals">&larr; Meals</button></div>'+

   (lastPlan?planBody():'<div class="empty"><p>Nothing generated yet.</p>'+
     '<p class="sm">Press Generate. Nothing touches your calendar until you say so.</p></div>')+
   '</div>';
}

function planBody(){
  var t=planTotals(lastPlan);
  return '<div class="stats gap-b">'+
   '<div class="stat"><b data-cv="'+t.kcal+'" data-cf="n">'+N(t.kcal)+'</b><span>Avg kcal</span></div>'+
   '<div class="stat"><b data-cv="'+t.target+'" data-cf="n">'+N(t.target)+'</b><span>Avg target</span></div>'+
   '<div class="stat"><b data-cv="'+t.p+'" data-cf="n">'+N(t.p)+'</b><span>Avg protein</span></div>'+
   '<div class="stat"><b>'+lastPlan.length+'</b><span>Days</span></div></div>'+
   '<div class="row gap-b">'+
   '<button class="b" id="mpApply">Add to my calendar</button>'+
   '<button class="b o" id="mpReplace">Replace what is there</button>'+
   '<button class="b o" id="mpGo2">Try again</button></div>'+
   lastPlan.map(function(d,i){
     var off=d.kcal-d.target, pct=d.target?Math.round(d.kcal/d.target*100):0;
     return '<div class="sec"><div class="spread"><h2>'+E(pretty(d.date))+'</h2>'+
     '<span class="chip p'+(Math.abs(off)<250?' t':'')+'">'+N(d.kcal)+' kcal, '+pct+'% of target'+
     ' &middot; '+N(d.p)+'g protein</span></div>'+
     '<div class="tw"><table><thead><tr><th>When</th><th>Meal</th><th class="num">kcal</th>'+
     '<th class="num">Protein</th><th></th></tr></thead><tbody>'+
     d.meals.map(function(m,j){var r=byId(m.id);if(!r)return '';
       return '<tr><td class="sm muted">'+E(t12(m.at))+'</td>'+
       '<td><b>'+E(r.n)+'</b><div class="xs muted">'+E(r.cat)+'</div></td>'+
       '<td class="num">'+N(r.k)+'</td><td class="num">'+N(r.p)+'g</td>'+
       '<td><button class="b o s" data-mpswap="'+i+'|'+j+'">Swap</button></td></tr>';
     }).join('')+'</tbody></table></div></div>';
   }).join('');
}

function bindMealPlan(){
  on('#mpWho','change',function(){planWho=this.value;});
  on('#mpDays','change',function(){planDays=+this.value;});
  on('#mpFav','click',function(){planFav=!planFav;route();});
  function gen(){
    lastPlan=makeMealPlan({who:planWho||ME(),days:planDays,favOnly:planFav});
    if(!lastPlan) toast('Nothing matches those diet filters yet');
    route();
  }
  on('#mpGo','click',gen);
  on('#mpGo2','click',gen);
  on('#mpApply','click',function(){
    var n=applyMealPlan(lastPlan,false);
    toast(n+' meals added'); location.hash='#/schedule';
  });
  on('#mpReplace','click',function(){
    if(!confirm('Replace everything already logged on those days?'))return;
    var n=applyMealPlan(lastPlan,true);
    toast(n+' meals set'); location.hash='#/schedule';
  });
  countUp($('#view'));
}

/* Swap one meal for the next best thing in the same category that is not
   already somewhere in the plan. */
function swapPlanMeal(di,mi){
  var day=lastPlan[di]; if(!day) return;
  var cur=byId(day.meals[mi].id); if(!cur) return;
  var inPlan={};
  lastPlan.forEach(function(d){d.meals.forEach(function(m){inPlan[m.id]=1;});});
  var pr=S.prefs||{};
  var cand=recipesFor(pr.diet,pr.goals).filter(function(r){
    return r.cat===cur.cat&&!inPlan[r.id];});
  if(!cand.length){toast('Nothing else in that category fits');return;}
  cand.sort(function(a,b){return Math.abs(a.k-cur.k)-Math.abs(b.k-cur.k);});
  day.meals[mi].id=cand[0].id;
  day.kcal=day.meals.reduce(function(a,m){var r=byId(m.id);return a+(r?r.k:0);},0);
  day.p=day.meals.reduce(function(a,m){var r=byId(m.id);return a+(r?r.p:0);},0);
  route();
}
"""

APP_HOUSEHOLD = r"""
/* ============================ the household page ============================
   Seats, invites, and the two things people get wrong: leaving, and handing
   over. Both are spelled out here rather than hidden behind a confirm dialog,
   because both move real data around. */
var houseBusy=false;

function vHousehold(){
  if(!HOUSE) return '<div class="page"><div class="empty">Not signed in.</div></div>';
  var owner=HOUSE.role==='owner';
  var full=HOUSE.used>=HOUSE.seats;
  return '<div class="page"><div class="phead"><h1>'+E(HOUSE.name)+'</h1>'+
   '<p>Everyone here shares the meal plan, the shopping lists, the budget and the '+
   'calendar. Anything you mark private stays yours and never leaves your account.</p></div>'+

   '<div class="stats gap-b">'+
   '<div class="stat"><b>'+HOUSE.used+' of '+HOUSE.seats+'</b><span>Seats used</span></div>'+
   '<div class="stat"><b>'+E(HOUSE.plan==='pro'?'Paid':'Free')+'</b><span>Plan</span></div>'+
   '<div class="stat"><b>'+E(owner?'Owner':'Member')+'</b><span>You are</span></div></div>'+

   (full&&HOUSE.plan!=='pro'?'<div class="note"><b>Every seat is taken.</b> '+
     'The free plan covers '+HOUSE.seats+' people. Paid covers six, and everything already '+
     'here carries over.</div>':'')+

   '<div class="sec"><div class="spread"><h2>People</h2>'+
   (owner&&!full?'<div class="row"><button class="b o s" id="hAddSeat">Add a person</button>'+
     '<button class="b s" id="hInvite">Invite someone</button></div>':'')+'</div>'+
   '<div class="tw"><table><thead><tr><th>Name</th><th>Account</th><th>Role</th><th></th></tr></thead>'+
   '<tbody>'+HOUSE.members.map(function(m){
     var isMe=ACCOUNT&&m.account_id&&(+m.account_id===+ACCOUNT.id);
     return '<tr><td><b>'+E(m.display_name)+'</b>'+(isMe?' <span class="chip t">you</span>':'')+'</td>'+
     '<td class="sm muted">'+(m.email?E(m.email):'<span class="chip">no login yet</span>')+'</td>'+
     '<td class="sm muted">'+E(m.role)+'</td>'+
     '<td>'+((owner&&m.role!=='owner')
       ?'<button class="b o s" data-hover="'+m.id+'">Make owner</button> '+
        '<button class="b o s dz" data-hdrop="'+m.id+'">Remove</button>':'')+'</td></tr>';
   }).join('')+'</tbody></table></div></div>'+

   '<div class="sec"><h2>Open invites</h2>'+
   '<p class="sub">A code lasts two weeks and works once. Whoever types it lands straight '+
   'in here with everything already shared.</p>'+
   '<div id="hInvites"><div class="empty sm">Loading</div></div></div>'+

   '<div class="sec"><h2>Leaving</h2>'+
   (owner&&HOUSE.used>1
     ? '<div class="note warn"><b>You own this household.</b> Hand it to somebody else '+
       'before you go, otherwise everyone here loses the shared plan.</div>'
     : '<p class="sub">You keep your account and start again on your own. Your private '+
       'notes come with you. The shared plan stays behind with everyone else.</p>'+
       '<button class="b o dz" id="hLeave">Leave this household</button>')+
   '</div>'+

   '<div class="sec"><h2>Account</h2>'+
   '<p class="sub">Signed in as '+E(ACCOUNT?ACCOUNT.email:'')+'.</p>'+
   '<button class="b o" id="hOut">Sign out</button></div>'+
   '</div>';
}

function refreshHouse(){
  return api('household.php?do=get').then(function(r){
    if(r.ok) HOUSE=r.household;
    return r;
  });
}

function drawInvites(){
  var box=$('#hInvites'); if(!box) return;
  if(HOUSE.role!=='owner'){
    box.innerHTML='<div class="empty sm">Only the owner can invite people.</div>';
    return;
  }
  api('household.php?do=invites').then(function(r){
    if(!r.ok||!r.invites.length){
      box.innerHTML='<div class="empty sm">No open invites.</div>';
      return;
    }
    box.innerHTML='<div class="tw"><table><thead><tr><th>Code</th><th>For</th>'+
      '<th>Expires</th><th></th></tr></thead><tbody>'+
      r.invites.map(function(i){
        return '<tr><td><b class="invcode">'+E(i.code)+'</b></td>'+
        '<td class="sm muted">'+E(i.display_name||'anyone')+'</td>'+
        '<td class="sm muted">'+E(String(i.expires_at).slice(0,10))+'</td>'+
        '<td><button class="b o s" data-hcopy="'+E(i.code)+'">Copy</button> '+
        '<button class="x" data-hrevoke="'+E(i.code)+'">&times;</button></td></tr>';
      }).join('')+'</tbody></table></div>';
  });
}

function bindHousehold(){
  drawInvites();
  on('#hAddSeat','click',function(){
    var n=prompt('Who is it? You can invite them to their own login later.');
    if(!n) return;
    api('household.php?do=addSeat',{body:{name:n}}).then(function(r){
      if(!r.ok){toast(r.error==='no_seats'?'Every seat on this plan is taken':'Could not add');return;}
      /* Give them a member row too, so they show up on the plans right away. */
      if(!MEMS().some(function(m){return m.name===n;})){
        S.members.push(blankMember(n,'f')); save(); chrome();
      }
      refreshHouse().then(route);
    });
  });
  on('#hInvite','click',function(){
    var n=prompt('Who is this code for? (their name, so their seat is waiting)')||'';
    api('household.php?do=invite',{body:{name:n}}).then(function(r){
      if(!r.ok){toast(r.error==='no_seats'?'Every seat on this plan is taken':'Could not make a code');return;}
      modal('Their invite code',
        '<p>Send them this. It works once and lasts two weeks.</p>'+
        '<div class="invbig">'+E(r.code)+'</div>'+
        '<p class="sm muted">They open LockedIn, tap <b>I have an invite code</b>, type it, '+
        'and sign in with Google. Everything here is shared the moment they land.</p>',
        '<button class="b" data-close>Done</button>');
      drawInvites();
    });
  });
  on('#hLeave','click',function(){
    if(!confirm('Leave '+HOUSE.name+'? The shared plan stays with them. You start fresh on your own.'))return;
    api('household.php?do=leave',{body:{}}).then(function(r){
      if(!r.ok){toast(r.error==='owner_must_hand_over'?'Hand the household over first':'Could not leave');return;}
      try{localStorage.removeItem(KEY);}catch(e){}
      location.reload();
    });
  });
  on('#hOut','click',signOut);
}
"""
