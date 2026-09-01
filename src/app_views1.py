# -*- coding: utf-8 -*-
APP_VIEWS1 = r"""
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

   '<div class="sec"><h2>Everything</h2><div class="card pad gap-b"><div class="fr">'+
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
   '<button class="b o s" data-nav="lists">Recipe lists'+
   (Object.keys(S.lists||{}).length?' <span class="chip p">'+Object.keys(S.lists).length+'</span>':'')+
   '</button>'+
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

/* ============================ RECIPE LISTS ============================
   Recipes could always be added to a named list; there was just never a screen
   that showed one back. This is it. */
function vRecipeLists(){
  var L=S.lists||{}, names=Object.keys(L).sort();
  return '<div class="page"><div class="phead"><h1>Recipe lists</h1>'+
   '<p>Collections of recipes: a Sunday prep list, the things she actually eats, '+
   'whatever is worth keeping together.</p></div>'+
   '<div class="row toolbar"><button class="b" id="rlNew">New list</button>'+
   '<button class="b o" data-nav="meals">&larr; Meals</button></div>'+
   (names.length?names.map(function(n){
     var ids=(L[n]||[]), rs=ids.map(byId).filter(Boolean);
     var cost=rs.reduce(function(a,r){return a+cps(r);},0);
     return '<div class="sec"><div class="spread"><h2>'+E(n)+'</h2>'+
     '<div class="row"><span class="chip p">'+rs.length+' recipe'+(rs.length===1?'':'s')+'</span>'+
     (rs.length?'<span class="chip p">'+$$$(cost)+' a serving each</span>':'')+
     '<button class="b o s" data-rle="'+E(n)+'">Rename</button>'+
     '<button class="b o s" data-rlgroc="'+E(n)+'">Add all to shopping</button>'+
     '<button class="b o s dz" data-rld="'+E(n)+'">Delete</button></div></div>'+
     (rs.length?'<div class="grid g3">'+rs.map(function(r){
       return '<div class="rlwrap">'+rcard(r)+
       '<button class="x rlrm" data-rlrm="'+E(n)+'|'+E(r.id)+'" title="Remove from this list">&times;</button>'+
       '</div>';}).join('')+'</div>'
      :'<div class="empty sm">Nothing on this list yet. Open a recipe and use "Add to a list".</div>')+
     '</div>';}).join('')
    :'<div class="empty"><p>No recipe lists yet.</p>'+
     '<p class="sm">Open any recipe and use "Add to a list" to start one.</p></div>')+
   '</div>';
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
   '<div class="card pad"><h3 class="ctitle">Method</h3><ol class="stp">'+
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
   '<div class="row toolbar">'+
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
   '<div class="row toolbar">'+
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
"""
