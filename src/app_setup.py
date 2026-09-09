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
 ['Home (renting)','Rent'],['Home (renting)','Renters insurance'],
 ['Home (buying)','Mortgage'],['Home (buying)','Property tax'],
 ['Home (buying)','Home insurance'],['Home (buying)','Repairs and upkeep'],
 ['Utilities','Electric'],['Utilities','Gas'],['Utilities','Water and sewer'],
 ['Utilities','Trash'],['Utilities','Internet'],['Utilities','Phone'],
 ['Food','Groceries'],['Food','Eating out'],['Food','Coffee'],
 ['Getting around','Car payment'],['Getting around','Car insurance'],
 ['Getting around','Fuel'],['Getting around','Maintenance and repairs'],
 ['Getting around','Registration and tags'],['Getting around','Parking and transit'],
 ['Health','Health insurance'],['Health','Appointments and copays'],
 ['Health','Dental and eye'],['Health','Prescriptions'],['Health','Gym'],
 ['Personal','Clothes and shoes'],['Personal','Haircuts and grooming'],
 ['Personal','Subscriptions'],['Personal','Things for the house'],
 ['Fun','Going out'],['Fun','Hobbies'],['Fun','Travel'],['Fun','Presents and birthdays'],
 ['People and pets','Pets'],['People and pets','Childcare'],['People and pets','Helping family'],
 ['Debt','Credit cards'],['Debt','Student loans'],['Debt','Anything else being paid down'],
 ['Saving','Emergency fund'],['Saving','Retirement'],['Saving','Saving up for something']
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
/* Gluten free is on the list even though every recipe in the book already is.
   Leaving it off makes people who need it assume it was not considered, and it
   is the one thing this recipe set was actually built around. */
var DIET_Q=[
 ['glutenfree','Gluten free','Every recipe here already is'],
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
var setupStep=0, setupAns=null, setupDrawn=-1;

function startOnboarding(){
  setupStep=0; setupDrawn=-1;
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
  /* Ticking a box redraws the step, and redrawing is not arriving at it. Only
     move the page when the step number actually changed, otherwise every
     answer throws you back to the heading. */
  if(step!==setupDrawn){ setupDrawn=step; window.scrollTo(0,0); }
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

  /* What the questionnaire produced is a starting point, not a set of edits.
   *
   * It used to be treated as edits, which meant the answers landed on top of
   * whatever the account already had. Somebody joining a household got their
   * own blank cost lines instead of the household's real ones, and then sent
   * those blank ones up over everybody else's. The same thing happened to a
   * second device that was ever asked to sign up.
   *
   * So: take a baseline first, so none of this counts as your work, then look
   * at the account. If it already has something, that wins and all this was is
   * a way of asking who you are. If the account is empty, these answers are the
   * only thing there is, and they go up as the starting point. */
  var mine=me, myPrefs=S.prefs;
  /* Cancel anything the save above armed. It would have gone up as an edit
     and landed on the household before the check below ever ran. */
  if(syncTimer) clearTimeout(syncTimer);
  syncPending=false;
  /* Forget which versions this device has already seen. It pulled the household
     before the questionnaire started, so without this the merge below says it
     has seen all of that already and hands back nothing, leaving the answers
     sitting on top of everybody else's work. */
  baseBv={}; baseDv={};
  syncSnap();
  syncStart();
  /* Ask the account directly rather than reading it off the last pull, so a
     pull that failed cannot be mistaken for an empty account. */
  api('doc.php?scope=shared').then(function(r){
    var already=stateWeight((r&&r.ok&&r.body)||null);
    if(already>6){
      return pullState().then(function(){ joinExisting(); });
    }
    forceNext=true; syncPending=true; pushState();
    toast('You are set up. Everything here is yours to change.');
    chrome(); route();
  });

  function joinExisting(){
    {
      /* The household already has data. Keep it, and make sure this person is
         in the list of people rather than replacing it with just themselves. */
      var list=S.members||[];
      var hit=null;
      list.forEach(function(x){
        if(!hit&&(x.name||'').toLowerCase()===(mine.name||'').toLowerCase()) hit=x;
      });
      if(!hit){ mine.sort=list.length; list.push(mine); S.members=list; hit=mine; }
      S.who=hit.id;
      S.prefs=myPrefs;
      save();
      toast('You are in. Everything the household already had is here.');
    }
    chrome(); route();
  }
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

APP_IMPORT = r"""
/* ============================ bringing the old data across ============================
   Two possible sources. The state.json the old sync endpoint left on the
   server, which is the copy that was never tied to one browser, and this
   browser's own localStorage under the old key. The server one wins when both
   are there, because it is the one both phones were writing to.

   Whatever comes back goes through migrateToMembers, the same code path that
   upgrades a local save, so the two profiles become members and every row that
   held a person gets remapped. Then it replaces the account wholesale and
   pushes, because a merge between an empty new account and a full old one has
   nothing to decide. */
var LEGACY_KEY='handbook.v5';

function legacyLocal(){
  try{
    var raw=localStorage.getItem(LEGACY_KEY);
    if(!raw) return null;
    var o=JSON.parse(raw);
    return (o&&o.fin)?o:null;
  }catch(e){ return null; }
}

function importCounts(st){
  return {costs:((st.fin||{}).costs||[]).length,
          jobs:((st.fin||{}).jobs||[]).length,
          days:Object.keys(st.days||{}).length,
          plans:((st.plan||{}).cols||[]).length,
          schedules:((st.sched||{}).cols||[]).length};
}
function countLine(c){
  var bits=[];
  if(c.costs) bits.push(c.costs+' cost lines');
  if(c.jobs) bits.push(c.jobs+' income lines');
  if(c.days) bits.push(c.days+' logged days');
  if(c.plans) bits.push(c.plans+' plan collections');
  if(c.schedules) bits.push(c.schedules+' schedule collections');
  return bits.length?bits.join(', '):'not much in it';
}

/* Is this account still basically empty. Only used to decide whether to warn
   before an import, never to decide whether one is allowed.

   A day counts for nothing unless something was actually put in it. Opening
   the meals page calls dayLog for today, which creates the entry whether or
   not you touch anything, so counting keys here would mean a brand new account
   is never empty and everybody gets warned about losing data they do not have. */
function dayUsed(d){
  if(!d) return false;
  return ((d.meals||[]).length>0)||((d.sched||[]).length>0)||((d.spend||[]).length>0)
      || !!d.notes || !!d.w || (d.workout&&d.workout!=='rest');
}
function looksEmpty(){
  var days=S.days||{};
  var anyDay=Object.keys(days).some(function(k){return dayUsed(days[k]);});
  return !(S.fin.costs||[]).some(function(c){return c.real||c.low||c.high;})
      && !(S.fin.jobs||[]).length
      && !anyDay
      && !((S.plan||{}).cols||[]).length
      && !(((S.sched||{}).cols)||[]).length;
}

function applyLegacy(st){
  var keepTheme=S.theme;
  var o=JSON.parse(JSON.stringify(st));
  var d=DEF();
  for(var k in d) if(!(k in o)) o[k]=d[k];
  for(var f in d.fin) if(!(f in o.fin)) o.fin[f]=d.fin[f];
  o=migrateToMembers(o);
  o.theme=keepTheme;
  o.onboarded=true;
  o.household=S.household;
  for(var kk in o) S[kk]=o[kk];
  save();
  /* Bringing old data across is a decision, same as loading a file. It goes up
     as an overwrite so the server takes all of it and the other phone gets it,
     rather than being weighed branch by branch against what is already there.
     Re-baseline rather than blanking the snapshot: a blank one reads as a first
     run, and a first run takes a baseline instead of saving. */
  syncSnap();
  forceNext=true;
  syncPending=true;
  pushState();
}

/* ============================ putting it on a phone ============================
   Chrome hands over an install prompt if you catch the event and hold on to
   it, so on Android this is one button. Safari never offers one, so iOS gets
   told exactly which menu to open instead of a button that does nothing. */
var installEvent=null;
window.addEventListener('beforeinstallprompt',function(e){
  e.preventDefault();
  installEvent=e;
  var b=document.getElementById('instBtn');
  if(b) b.hidden=false;
});
window.addEventListener('appinstalled',function(){ installEvent=null; });

function isStandalone(){
  try{
    return window.matchMedia('(display-mode: standalone)').matches
        || window.navigator.standalone===true;
  }catch(e){ return false; }
}
function devicePlatform(){
  var ua=navigator.userAgent||'';
  if(/iPhone|iPad|iPod/i.test(ua)) return 'ios';
  if(/Android/i.test(ua)) return 'android';
  return 'desktop';
}

function vInstall(){
  var p=devicePlatform();
  var here=location.origin+location.pathname;
  var steps=
    p==='ios'
      ? '<ol class="steps"><li>Open this page in <b>Safari</b>. It has to be Safari, '+
        'Chrome on an iPhone cannot install it.</li>'+
        '<li>Tap the <b>Share</b> button, the square with the arrow coming out of it, '+
        'at the bottom of the screen.</li>'+
        '<li>Scroll down the list and tap <b>Add to Home Screen</b>.</li>'+
        '<li>Tap <b>Add</b>. It is on your home screen like any other app.</li></ol>'
    : p==='android'
      ? '<ol class="steps"><li>Tap <b>Install</b> above. If it is not there, use the '+
        '<b>three dots</b> at the top right of Chrome.</li>'+
        '<li>Tap <b>Install app</b>, or <b>Add to Home screen</b> on older versions.</li>'+
        '<li>Confirm. It lands in your app drawer and on your home screen.</li></ol>'
      : '<ol class="steps"><li>Look for the <b>install icon</b> in the address bar, a screen '+
        'with a downward arrow, at the right hand end.</li>'+
        '<li>Or open the browser menu and choose <b>Install LockedIn</b>.</li>'+
        '<li>It opens in its own window from then on, with no browser chrome.</li></ol>';

  return '<div class="page"><div class="phead"><h1>Put it on your phone</h1>'+
   '<p>It installs straight from the browser. There is no app store, no download, and no '+
   'update to ever install again: it is the same page, just without the browser around it.</p></div>'+
   (isStandalone()
     ? '<div class="note good"><b>Already installed.</b> You are looking at the installed '+
       'copy right now.</div>'
     : '<div class="row toolbar">'+
       '<button class="b" id="instBtn"'+(installEvent?'':' hidden')+'>Install</button>'+
       '<button class="b o" id="instCopy">Copy the link</button></div>')+
   '<div class="sec"><h2>'+(p==='ios'?'On an iPhone or iPad':p==='android'?'On Android':'On a computer')+'</h2>'+
   steps+'</div>'+
   '<div class="sec"><h2>The address</h2>'+
   '<p class="sub">Whatever device you are setting up, this is the only thing you need. '+
   'Sign in with the same Google account and everything is already there.</p>'+
   '<div class="addr">'+E(here)+'</div>'+
   '<div class="row"><button class="b o" id="instCopy2">Copy the link</button></div></div>'+
   '<div class="sec"><h2>If you deleted it</h2>'+
   '<p class="sub">Nothing was lost. Deleting the installed copy removes the icon and this '+
   'device&#39;s cache, and none of that is where your account lives. Open the address above, '+
   'sign in, and install it again.</p></div>'+
   '</div>';
}

function bindInstall(){
  function doCopy(){
    var t=location.origin+location.pathname;
    try{ navigator.clipboard.writeText(t); toast('Link copied'); }
    catch(e){ toast(t); }
  }
  on('#instCopy','click',doCopy);
  on('#instCopy2','click',doCopy);
  on('#instBtn','click',function(){
    if(!installEvent){ toast('Use the browser menu, the steps below say where'); return; }
    installEvent.prompt();
    installEvent.userChoice.then(function(r){
      if(r&&r.outcome==='accepted'){ installEvent=null; toast('Installed'); route(); }
    });
  });
}

/* Earlier versions of the household document, and a way back to one. */
function restoreScreen(){
  var box=$('#view');
  box.innerHTML='<div class="page"><div class="phead"><h1>Earlier versions</h1>'+
   '<p>Every time this account is saved, the copy it replaced is kept for a month. '+
   'If something went wrong you can put one of them back.</p></div>'+
   '<div id="rsBody"><div class="empty">Looking</div></div></div>';
  api('doc.php?do=history&scope=shared').then(function(r){
    var out=$('#rsBody'); if(!out) return;
    if(!r.ok||!r.versions.length){
      out.innerHTML='<div class="empty"><p>No earlier versions yet.</p>'+
        '<p class="sm">They start being kept from the next save onwards.</p></div>'+
        '<div class="row"><button class="b o" data-nav="meals">Back</button></div>';
      return;
    }
    out.innerHTML='<div class="tw cards"><table><thead><tr><th>Version</th><th>Saved</th>'+
      '<th class="num">Size</th><th></th></tr></thead><tbody>'+
      r.versions.map(function(v){
        return '<tr><td class="hd"><b>Version '+v.version+'</b></td>'+
        '<td data-l="Saved" class="sm muted">'+E(String(v.saved_at).replace('T',' ').slice(0,16))+'</td>'+
        '<td data-l="Things in it" class="num">'+v.weight+'</td>'+
        '<td class="act"><button class="b o s" data-rsv="'+v.version+'">Put this back</button></td></tr>';
      }).join('')+'</tbody></table></div>'+
      '<p class="sub" style="margin-top:12px">Size is a rough count of the lines, days and '+
      'lists in that copy. A version far smaller than the ones around it is usually the '+
      'one that went wrong.</p>'+
      '<div class="row"><button class="b o" data-nav="meals">Back</button></div>';
  });
}

function importScreen(){
  var box=$('#view');
  box.innerHTML='<div class="page"><div class="phead"><h1>Bring your old data across</h1>'+
   '<p>Everything from before accounts existed. Looking for it now.</p></div>'+
   '<div id="impBody"><div class="empty">Checking</div></div></div>';
  var localSt=legacyLocal();
  Promise.all([api('import.php?do=peek'),api('import.php?do=seed')]).then(function(both){
    var r=both[0], seed=both[1];
    var out=$('#impBody'); if(!out) return;
    var opts='';
    if(seed.ok&&seed.found){
      var c=seed.counts;
      opts+='<div class="card pad gap-b"><h3 class="ctitle">The original household</h3>'+
        '<p class="sm muted">'+c.jobs+' income lines, '+c.costs+' costs, '+
        c.purchases+' comparison lists, '+c.strategies+' strategy lists and '+
        c.plans+' plan collections.</p>'+
        '<p class="sm muted">Everything from before accounts existed, rebuilt and brought '+
        'forward to the current shape.</p>'+
        '<button class="b" id="impSeed" style="margin-top:10px">Bring this one across</button></div>';
    }
    if(r.ok&&r.found){
      opts+='<div class="card pad gap-b"><h3 class="ctitle">On the server</h3>'+
        '<p class="sm muted">Last written '+E(String(r.updatedAt||'').slice(0,10))+
        '. Contains '+E(countLine(r.counts))+'.</p>'+
        '<p class="sm muted">This is the copy every device was writing to, so it is '+
        'almost always the one you want.</p>'+
        '<button class="b" id="impServer" style="margin-top:10px">Bring this one across</button></div>';
    }
    if(localSt){
      opts+='<div class="card pad gap-b"><h3 class="ctitle">On this device</h3>'+
        '<p class="sm muted">Contains '+E(countLine(importCounts(localSt)))+'.</p>'+
        '<p class="sm muted">Only what this browser had. Use it if the server copy is '+
        'missing or older than what you remember.</p>'+
        '<button class="b o" id="impLocal" style="margin-top:10px">Bring this one across</button></div>';
    }
    if(!opts){
      out.innerHTML='<div class="empty"><p>Nothing found to import.</p>'+
        '<p class="sm">The old data is either on a different device, or the state.json '+
        'the old version wrote is no longer on the server.</p></div>'+
        '<div class="row"><button class="b o" data-nav="meals">Back to the app</button></div>';
      return;
    }
    out.innerHTML=
      (looksEmpty()?'':'<div class="note warn"><b>This account already has things in it.</b> '+
        'Importing replaces all of it. Save a file from Settings first if you want a copy.</div>')+
      opts+
      '<div class="row"><button class="b o" data-nav="meals">Not now</button></div>';
    var sd=$('#impSeed');
    if(sd) sd.onclick=function(){
      if(!looksEmpty()&&!confirm('Replace everything in this account with the original data?'))return;
      this.disabled=true; this.textContent='Bringing it across';
      applyLegacy(seed.state);
      toast('Your data is back');
      location.hash='#/financial'; route();
    };
    var sv=$('#impServer');
    if(sv) sv.onclick=function(){
      if(!looksEmpty()&&!confirm('Replace everything in this account with the old data?'))return;
      this.disabled=true; this.textContent='Bringing it across';
      api('import.php?do=fetch',{body:{}}).then(function(f){
        if(!f.ok){toast('Could not read it');route();return;}
        applyLegacy(f.state);
        toast('Your data is back');
        location.hash='#/financial'; route();
      });
    };
    var lc=$('#impLocal');
    if(lc) lc.onclick=function(){
      if(!looksEmpty()&&!confirm('Replace everything in this account with the old data?'))return;
      applyLegacy(localSt);
      toast('Your data is back');
      location.hash='#/financial'; route();
    };
  });
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
     '<div class="tw cards"><table><thead><tr><th>When</th><th>Meal</th><th class="num">kcal</th>'+
     '<th class="num">Protein</th><th></th></tr></thead><tbody>'+
     d.meals.map(function(m,j){var r=byId(m.id);if(!r)return '';
       return '<tr><td class="sm muted" data-l="When">'+E(t12(m.at))+'</td>'+
       '<td data-l="Meal"><b>'+E(r.n)+'</b><div class="xs muted">'+E(r.cat)+'</div></td>'+
       '<td class="num" data-l="kcal">'+N(r.k)+'</td>'+
       '<td class="num" data-l="Protein">'+N(r.p)+'g</td>'+
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
   '<div class="tw cards"><table><thead><tr><th>Name</th><th>Account</th><th>Role</th><th></th></tr></thead>'+
   '<tbody>'+HOUSE.members.map(function(m){
     var isMe=ACCOUNT&&m.account_id&&(+m.account_id===+ACCOUNT.id);
     return '<tr><td class="hd"><b>'+E(m.display_name)+'</b>'+(isMe?'<span class="chip t">you</span>':'')+'</td>'+
     '<td data-l="Account" class="sm muted">'+(m.email?E(m.email):'<span class="chip">no login yet</span>')+'</td>'+
     '<td data-l="Role" class="sm muted">'+E(m.role)+'</td>'+
     '<td class="act">'+((owner&&m.role!=='owner')
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
    box.innerHTML='<div class="tw cards"><table><thead><tr><th>Code</th><th>For</th>'+
      '<th>Expires</th><th></th></tr></thead><tbody>'+
      r.invites.map(function(i){
        return '<tr><td class="hd"><b class="invcode">'+E(i.code)+'</b></td>'+
        '<td data-l="For" class="sm muted">'+E(i.display_name||'anyone')+'</td>'+
        '<td data-l="Expires" class="sm muted">'+E(String(i.expires_at).slice(0,10))+'</td>'+
        '<td class="act"><button class="b o s" data-hcopy="'+E(i.code)+'">Copy</button> '+
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
