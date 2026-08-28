# -*- coding: utf-8 -*-
"""The interactive layer. Runs in the HTML edition; prints as static panels."""

import json, html


def data_blob(DATA, cost_fn):
    rows = []
    for d in DATA:
        r = d["r"]; p = d["per"]
        wal, wps, _ = cost_fn(r, r["servings"], "walmart")
        cos, cps, _ = cost_fn(r, r["servings"], "costco")
        rows.append({
            "id": r["id"], "n": r["name"], "cat": r["cat"], "sv": r["servings"],
            "t": d["time"], "k": round(p["kcal"]), "p": round(p["p"], 1),
            "c": round(p["c"], 1), "f": round(p["f"], 1), "fib": round(p["fib"], 1),
            "leu": round(p["leu"], 2), "tg": d["tags"],
            "cw": round(wal, 2), "cws": round(wps, 2),
            "cc": round(cos, 2), "ccs": round(cps, 2),
            "ing": [[ii[2], ii[0]] for ii in r["ing"]],
            "st": r["steps"],
        })
    return rows


PANEL = """
<h2 id="app">The kitchen app</h2>
<p>Everything on this page saves to this browser. Favourites, custom lists, my own recipes and any
photos I add. Nothing leaves the device, so back it up with Export now and then, especially before
moving it to a new phone or laptop.</p>

<div class="appbar">
  <div class="whoblock">
    <span class="wholabel">Cooking for</span>
    <div class="whotoggle">
      <button class="who on" data-who="j">Me</button>
      <button class="who" data-who="a">Aaliyah</button>
      <button class="who" data-who="b">Both of us</button>
    </div>
  </div>
  <div class="whoblock">
    <span class="wholabel">Prices from</span>
    <div class="whotoggle">
      <button class="store on" data-store="walmart">Walmart FC</button>
      <button class="store" data-store="costco">Costco Timnath</button>
    </div>
  </div>
  <div class="whoblock grow">
    <span class="wholabel">Daily target for this selection</span>
    <div class="targetrow" id="tgtRow"></div>
  </div>
</div>

<h3 id="recommend">What should we eat after today's session</h3>
<p class="small">Pick what got trained and roughly what is left in the day. The list reorders by
what that session actually needs, not by what sounds healthy.</p>

<div class="recbox">
  <div class="recinputs">
    <label>Trained today
      <select id="rcTrain">
        <option value="rest">Rest day</option>
        <option value="pull">Back and biceps (pull)</option>
        <option value="push">Chest, shoulders, triceps (push)</option>
        <option value="legs">Legs</option>
        <option value="arms">Arms only</option>
        <option value="abs">Abs and core</option>
        <option value="cardio">Cardio or conditioning</option>
        <option value="skill">Skill work, planche, handstands</option>
        <option value="full" selected>Full body or a mixture</option>
      </select>
    </label>
    <label>Calories left
      <select id="rcKcal">
        <option value="250">Under 300</option>
        <option value="450">300 to 550</option>
        <option value="700" selected>550 to 850</option>
        <option value="1100">850 to 1,300</option>
        <option value="1600">Over 1,300</option>
      </select>
    </label>
    <label>Protein still needed
      <select id="rcProt">
        <option value="15">Barely any</option>
        <option value="30">Around 30 g</option>
        <option value="45" selected>Around 45 g</option>
        <option value="60">60 g or more</option>
      </select>
    </label>
    <label>Time I have
      <select id="rcTime">
        <option value="10">10 minutes</option>
        <option value="25" selected>25 minutes</option>
        <option value="45">45 minutes</option>
        <option value="999">However long it takes</option>
      </select>
    </label>
    <label>Mood
      <select id="rcMood">
        <option value="any" selected>Anything</option>
        <option value="CHEAT MEAL">Cheat meal</option>
        <option value="HEALTHY DESSERT">Something sweet</option>
        <option value="SAVORY">Savory</option>
        <option value="BUDGET FRIENDLY">Cheap</option>
        <option value="NO-COOK">No cooking</option>
        <option value="MEAL PREP">Batch for the week</option>
      </select>
    </label>
    <label>Include meat
      <select id="rcMeat">
        <option value="veg">Vegetarian only</option>
        <option value="some" selected>Mostly veg, chicken is fine</option>
        <option value="push">Push me toward chicken and fish</option>
      </select>
    </label>
  </div>
  <p class="recwhy" id="rcWhy"></p>
  <div class="reccards" id="rcOut"></div>
</div>

<h3 id="lists">Favourites and lists</h3>
<div class="listbar">
  <button class="btn" id="btnNewList">New list</button>
  <button class="btn" id="btnAddRecipe">Add my own recipe</button>
  <button class="btn ghost" id="btnExport">Export backup</button>
  <button class="btn ghost" id="btnImport">Import backup</button>
  <input type="file" id="fileImport" accept="application/json" hidden>
  <span class="small" id="saveNote"></span>
</div>
<div class="listgrid" id="listOut"></div>

<h3 id="mine">My own recipes</h3>
<div class="mineform" id="mineForm" hidden>
  <div class="mfrow">
    <label>Name<input id="mfName" placeholder="Aaliyah's tortilla soup"></label>
    <label>Servings<input id="mfSv" type="number" value="2" min="1"></label>
    <label>Minutes<input id="mfT" type="number" value="20" min="1"></label>
  </div>
  <div class="mfrow">
    <label>Calories / serving<input id="mfK" type="number" placeholder="620"></label>
    <label>Protein g<input id="mfP" type="number" placeholder="42"></label>
    <label>Carbs g<input id="mfC" type="number" placeholder="60"></label>
    <label>Fat g<input id="mfF" type="number" placeholder="18"></label>
    <label>Cost / serving $<input id="mfCost" type="number" step="0.01" placeholder="3.20"></label>
  </div>
  <label>Ingredients, one per line<textarea id="mfIng" rows="5"
    placeholder="200 g chicken breast&#10;1 can black beans&#10;2 corn tortillas"></textarea></label>
  <label>Method<textarea id="mfSteps" rows="5" placeholder="One step per line"></textarea></label>
  <label class="photolab">Photo
    <input type="file" id="mfPhoto" accept="image/*"></label>
  <img id="mfPrev" class="photoprev" hidden alt="">
  <div class="mfrow">
    <button class="btn" id="mfSave">Save recipe</button>
    <button class="btn ghost" id="mfCancel">Cancel</button>
  </div>
</div>
<div class="listgrid" id="mineOut"></div>
"""


def script(rows, targets_json):
    return """
<script>
(function(){
var R = __ROWS__;
var TGT = __TGT__;
var KEY='mealhandbook.v2';
var S = load();

function load(){
  try{var raw=localStorage.getItem(KEY); if(raw) return JSON.parse(raw);}catch(e){}
  return {fav:[], lists:{'Favourites':[], 'Aaliyah likes':[], 'Move-in week':[]}, mine:[], photos:{},
          who:'j', store:'walmart', prices:{}};
}
function save(){
  try{localStorage.setItem(KEY, JSON.stringify(S)); note('Saved');}
  catch(e){note('Could not save. Storage may be full, try removing a photo.');}
}
function note(t){var e=q('#saveNote'); if(e){e.textContent=t; setTimeout(function(){e.textContent='';},2200);}}
function q(s){return document.querySelector(s);} function qa(s){return [].slice.call(document.querySelectorAll(s));}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function money(v){return '$'+Number(v||0).toFixed(2);}

/* ---------------- who / targets ---------------- */
function curTgt(){return TGT[S.who]||TGT.j;}
function drawTargets(){
  var t=curTgt();
  q('#tgtRow').innerHTML =
    ['<b>'+t.kcal.toLocaleString()+'</b><i>kcal</i>','<b>'+t.p+' g</b><i>protein</i>',
     '<b>'+t.c+' g</b><i>carbs</i>','<b>'+t.f+' g</b><i>fat</i>',
     '<b>'+t.fib+' g</b><i>fiber</i>','<b>'+t.w+' oz</b><i>water</i>']
    .map(function(h){return '<span>'+h+'</span>';}).join('');
}
qa('.who').forEach(function(b){b.onclick=function(){
  qa('.who').forEach(function(x){x.classList.remove('on');});
  b.classList.add('on'); S.who=b.dataset.who; save(); drawTargets(); recommend(); renderAll();};});
qa('.store').forEach(function(b){b.onclick=function(){
  qa('.store').forEach(function(x){x.classList.remove('on');});
  b.classList.add('on'); S.store=b.dataset.store; save(); recommend(); renderAll(); repriceLibrary();};});

/* ---------------- training profiles ---------------- */
var TRAIN = {
  rest:  {label:'a rest day', p:1.15, c:0.75, boost:['HIGH FIBER','HIGH MICRONUTRIENT DENSITY','HIGH SATIETY'], why:'Protein stays high because repair happens on rest days. Carbs come down slightly, fiber and micronutrients go up.'},
  pull:  {label:'back and biceps', p:1.35, c:1.05, boost:['LEUCINE PRIORITY','HIGH MICRONUTRIENT DENSITY','OMEGA-3 RICH'], why:'Back is the biggest muscle group up top, so protein and leucine lead. Iron-rich options are weighted up because pulling volume plus a plant-heavy diet is where iron gets thin.'},
  push:  {label:'chest, shoulders and triceps', p:1.35, c:1.0, boost:['LEUCINE PRIORITY','HIGH PROTEIN'], why:'Straight hypertrophy demand. Leucine per feeding is what matters most here.'},
  legs:  {label:'legs', p:1.25, c:1.45, boost:['HIGH CALORIE','POST-WORKOUT FRIENDLY','HIGH SATIETY'], why:'Legs empty more glycogen than anything else, so carbs and total calories lead. This is the day to eat the big meal.'},
  arms:  {label:'arms', p:1.25, c:0.9, boost:['HIGH PROTEIN','QUICK'], why:'Small muscle group, small systemic cost. Protein still matters, calories do not need to spike.'},
  abs:   {label:'abs and core', p:1.15, c:0.85, boost:['HIGH SATIETY','HIGH FIBER','LOW CALORIE'], why:'Low energy cost. Volume and fiber over calories, because abs are a body fat outcome and this is not the session to overshoot on.'},
  cardio:{label:'cardio', p:1.1, c:1.4, boost:['POST-WORKOUT FRIENDLY','HIGH CARB','HEALTH DRINK'], why:'Carbs and fluid replacement lead. Sodium matters more than usual, especially in dry Colorado air.'},
  skill: {label:'skill work', p:1.2, c:1.15, boost:['OMEGA-3 RICH','HIGH MICRONUTRIENT DENSITY','POST-WORKOUT FRIENDLY'], why:'Planche and handstand work loads connective tissue more than muscle. Omega-3 and overall nutrient density get weighted up, and being properly fed matters more than any single macro.'},
  full:  {label:'a full body session', p:1.3, c:1.25, boost:['LEUCINE PRIORITY','HIGH CALORIE','POST-WORKOUT FRIENDLY'], why:'Everything trained, so everything demanded. Protein and carbs both lead.'}
};

function recommend(){
  var tr=TRAIN[q('#rcTrain').value], kcal=+q('#rcKcal').value, pr=+q('#rcProt').value;
  var tm=+q('#rcTime').value, mood=q('#rcMood').value, meat=q('#rcMeat').value;
  var mult = S.who==='b'?1.9 : S.who==='a'?0.72 : 1.0;
  var tk = kcal*mult, tp = pr*mult;

  var scored = R.map(function(r){
    var s=0;
    s -= Math.abs(r.k - tk)/28;
    s += Math.min(r.p, tp*1.35) * 1.9 * tr.p;
    s += Math.min(r.c, 130) * 0.16 * tr.c;
    s += r.leu * 7;
    if(r.t > tm) s -= (r.t - tm) * 2.2;
    tr.boost.forEach(function(t){ if(r.tg.indexOf(t)>=0) s += 16; });
    if(mood!=='any'){ s += (r.tg.indexOf(mood)>=0 ? 55 : -32); }
    var isMeat = r.cat==='SDA Meat/Fish';
    if(meat==='veg' && isMeat) s -= 900;
    if(meat==='push' && isMeat) s += 34;
    if(S.fav.indexOf(r.id)>=0) s += 12;
    return {r:r, s:s};
  }).sort(function(a,b){return b.s-a.s;}).slice(0,9);

  q('#rcWhy').innerHTML = 'Ranked for <b>'+tr.label+'</b>. '+esc(tr.why);
  q('#rcOut').innerHTML = scored.map(function(o){return card(o.r);}).join('');
  wire(q('#rcOut'));
}

/* ---------------- cards ---------------- */
function cost(r){ return S.store==='costco' ? r.ccs : r.cws; }
function costFull(r){ return S.store==='costco' ? r.cc : r.cw; }
function card(r){
  var fav = S.fav.indexOf(r.id)>=0;
  var ph = S.photos[r.id];
  return '<article class="rcard" data-id="'+r.id+'">'
   + (ph? '<div class="rcphoto"><img src="'+ph+'" alt=""></div>' : '')
   + '<div class="rchead"><span class="rcid">'+r.id+'</span>'
   + '<button class="fav'+(fav?' on':'')+'" title="Favourite">'+(fav?'\\u2605':'\\u2606')+'</button></div>'
   + '<h4 class="rcname">'+esc(r.n)+'</h4>'
   + '<div class="rcmeta">'+r.t+' min &middot; makes '+r.sv+' &middot; <b>'+money(cost(r))+'</b>/serving'
   + ' <span class="hh">('+money(costFull(r))+' total)</span></div>'
   + '<div class="rcmac"><span><b>'+r.k+'</b>kcal</span><span><b>'+r.p+'</b>P</span>'
   + '<span><b>'+r.c+'</b>C</span><span><b>'+r.f+'</b>F</span><span><b>'+r.fib+'</b>fib</span>'
   + '<span><b>'+r.leu+'</b>leu</span></div>'
   + '<div class="rcacts"><a class="btn tiny" href="#'+r.id+'">Recipe</a>'
   + '<button class="btn tiny ghost act-card">Save card</button>'
   + '<button class="btn tiny ghost act-photo">Photo</button>'
   + '<button class="btn tiny ghost act-list">Add to list</button></div></article>';
}

function wire(root){
  root.querySelectorAll('.rcard').forEach(function(el){
    var id=el.dataset.id, r=byId(id);
    var fb=el.querySelector('.fav');
    if(fb) fb.onclick=function(){
      var i=S.fav.indexOf(id);
      if(i>=0){S.fav.splice(i,1);} else {S.fav.push(id);}
      save(); renderAll(); recommend();
    };
    var cb=el.querySelector('.act-card'); if(cb) cb.onclick=function(){drawCardPNG(r);};
    var pb=el.querySelector('.act-photo'); if(pb) pb.onclick=function(){pickPhoto(id);};
    var lb=el.querySelector('.act-list'); if(lb) lb.onclick=function(){addToList(id);};
  });
}
function byId(id){
  for(var i=0;i<R.length;i++){ if(R[i].id===id) return R[i]; }
  for(var j=0;j<S.mine.length;j++){ if(S.mine[j].id===id) return S.mine[j]; }
  return null;
}

/* ---------------- photos ---------------- */
function pickPhoto(id){
  var inp=document.createElement('input'); inp.type='file'; inp.accept='image/*';
  inp.onchange=function(){
    var f=inp.files[0]; if(!f) return;
    shrink(f, 720, function(dataUrl){ S.photos[id]=dataUrl; save(); renderAll(); recommend(); });
  };
  inp.click();
}
function shrink(file, max, cb){
  var fr=new FileReader();
  fr.onload=function(){
    var img=new Image();
    img.onload=function(){
      var sc=Math.min(1, max/Math.max(img.width,img.height));
      var c=document.createElement('canvas');
      c.width=Math.round(img.width*sc); c.height=Math.round(img.height*sc);
      c.getContext('2d').drawImage(img,0,0,c.width,c.height);
      cb(c.toDataURL('image/jpeg',0.72));
    };
    img.src=fr.result;
  };
  fr.readAsDataURL(file);
}

/* ---------------- downloadable recipe card ---------------- */
function drawCardPNG(r){
  var W=900,H=1250,c=document.createElement('canvas');
  c.width=W;c.height=H;var x=c.getContext('2d');
  var g=x.createLinearGradient(0,0,W,H);
  g.addColorStop(0,'#0B1F3A');g.addColorStop(.6,'#12365F');g.addColorStop(1,'#1B4B85');
  x.fillStyle=g;x.fillRect(0,0,W,H);
  x.fillStyle='#1E6FD9';x.fillRect(0,0,W,8);
  x.fillStyle='#79A7DE';x.font='600 20px Helvetica,Arial';
  x.fillText(r.id+'   \\u00B7   '+(r.cat||'My recipe').toUpperCase(),56,84);
  x.fillStyle='#fff';x.font='800 54px Helvetica,Arial';
  wrap(x,r.n,56,150,790,58);
  var y=Math.max(250, 150+wrapH(x,r.n,790,58));
  // macro row
  var mac=[[r.k,'KCAL'],[r.p+'g','PROTEIN'],[r.c+'g','CARBS'],[r.f+'g','FAT'],[r.fib+'g','FIBER'],[r.leu+'g','LEUCINE']];
  var bw=(790-25)/6;
  mac.forEach(function(m,i){
    var bx=56+i*(bw+5);
    x.fillStyle='rgba(255,255,255,.09)';x.fillRect(bx,y,bw,92);
    x.fillStyle='#fff';x.font='800 27px Helvetica,Arial';x.textAlign='center';
    x.fillText(String(m[0]),bx+bw/2,y+42);
    x.fillStyle='#79A7DE';x.font='600 12px Helvetica,Arial';
    x.fillText(m[1],bx+bw/2,y+68);x.textAlign='left';
  });
  y+=134;
  x.fillStyle='#1E6FD9';x.fillRect(56,y,790,64);
  x.fillStyle='#fff';x.font='700 24px Helvetica,Arial';
  x.fillText('Makes '+r.sv+'   \\u00B7   '+money(cost(r))+' per serving   \\u00B7   '+money(costFull(r))+' total',80,y+41);
  y+=104;
  x.fillStyle='#7FD4FF';x.font='700 17px Helvetica,Arial';x.fillText('INGREDIENTS',56,y);y+=30;
  x.fillStyle='#DCE9FA';x.font='400 19px Helvetica,Arial';
  (r.ing||[]).slice(0,16).forEach(function(it){
    x.fillText('\\u2022  '+(it[0]||it),56,y); y+=27;
  });
  y+=22;
  x.fillStyle='#7FD4FF';x.font='700 17px Helvetica,Arial';x.fillText('METHOD',56,y);y+=30;
  x.fillStyle='#C4DAF3';x.font='400 17px Helvetica,Arial';
  (r.st||[]).slice(0,6).forEach(function(s,i){
    y+=wrap(x,(i+1)+'. '+s,56,y,790,24)+8;
  });
  x.fillStyle='#5C8CC4';x.font='600 14px Helvetica,Arial';
  x.fillText('The Meal Handbook',56,H-42);
  var a=document.createElement('a');
  a.download=r.id+'-'+r.n.replace(/[^a-z0-9]+/gi,'-').toLowerCase()+'.png';
  a.href=c.toDataURL('image/png'); a.click();
}
function wrap(x,t,px,py,mw,lh){
  var words=String(t).split(' '),line='',yy=py,used=0;
  for(var i=0;i<words.length;i++){
    var test=line+words[i]+' ';
    if(x.measureText(test).width>mw && line){x.fillText(line,px,yy);line=words[i]+' ';yy+=lh;used+=lh;}
    else line=test;
  }
  x.fillText(line,px,yy);return used+lh;
}
function wrapH(x,t,mw,lh){
  var words=String(t).split(' '),line='',h=lh;
  for(var i=0;i<words.length;i++){
    var test=line+words[i]+' ';
    if(x.measureText(test).width>mw && line){line=words[i]+' ';h+=lh;} else line=test;
  }
  return h;
}

/* ---------------- lists ---------------- */
function addToList(id){
  var names=Object.keys(S.lists);
  var pick=prompt('Add to which list?\\n\\n'+names.join('\\n')+'\\n\\nType a name, or a new one.', names[0]);
  if(!pick) return;
  if(!S.lists[pick]) S.lists[pick]=[];
  if(S.lists[pick].indexOf(id)<0) S.lists[pick].push(id);
  save(); renderAll();
}
q('#btnNewList').onclick=function(){
  var n=prompt('Name the list'); if(!n) return;
  if(!S.lists[n]) S.lists[n]=[]; save(); renderAll();
};
function renderLists(){
  var out=[];
  if(S.fav.length){
    out.push(listBlock('Favourites \\u2605', S.fav, null));
  }
  Object.keys(S.lists).forEach(function(name){
    out.push(listBlock(name, S.lists[name], name));
  });
  q('#listOut').innerHTML = out.join('') || '<p class="small">No lists yet. Star something, or make one.</p>';
  q('#listOut').querySelectorAll('.dellist').forEach(function(b){
    b.onclick=function(){ if(confirm('Delete list "'+b.dataset.l+'"?')){ delete S.lists[b.dataset.l]; save(); renderAll(); } };
  });
  q('#listOut').querySelectorAll('.rmitem').forEach(function(b){
    b.onclick=function(){
      var l=b.dataset.l, id=b.dataset.i;
      if(l===null||l==='') { var k=S.fav.indexOf(id); if(k>=0) S.fav.splice(k,1); }
      else { var arr=S.lists[l]; var k2=arr.indexOf(id); if(k2>=0) arr.splice(k2,1); }
      save(); renderAll();
    };
  });
}
function listBlock(title, ids, delName){
  var items = ids.map(function(id){
    var r=byId(id); if(!r) return '';
    return '<li><a href="#'+id+'">'+esc(r.n)+'</a>'
      +'<span class="li-meta">'+r.k+' kcal &middot; '+r.p+'P &middot; '+money(cost(r))+'</span>'
      +'<button class="rmitem" data-l="'+(delName||'')+'" data-i="'+id+'" title="Remove">\\u00D7</button></li>';
  }).join('');
  var tot = ids.reduce(function(a,id){var r=byId(id);return a+(r?costFull(r):0);},0);
  return '<section class="listcard"><header><h4>'+esc(title)+'</h4>'
    + (delName? '<button class="dellist" data-l="'+esc(delName)+'">Delete</button>':'')
    + '</header><ul>'+(items||'<li class="small">Empty</li>')+'</ul>'
    + (ids.length? '<p class="listtot">Shopping total '+money(tot)+' at '+(S.store==='costco'?'Costco':'Walmart')+'</p>':'')
    + '</section>';
}

/* ---------------- my own recipes ---------------- */
var pendingPhoto=null;
q('#btnAddRecipe').onclick=function(){ q('#mineForm').hidden=false; q('#mfName').focus(); };
q('#mfCancel').onclick=function(){ q('#mineForm').hidden=true; pendingPhoto=null; q('#mfPrev').hidden=true; };
q('#mfPhoto').onchange=function(){
  var f=q('#mfPhoto').files[0]; if(!f) return;
  shrink(f,720,function(d){pendingPhoto=d; q('#mfPrev').src=d; q('#mfPrev').hidden=false;});
};
q('#mfSave').onclick=function(){
  var name=q('#mfName').value.trim(); if(!name){alert('Give it a name.');return;}
  var id='X-'+(S.mine.length+1);
  var sv=+q('#mfSv').value||1, cps=+q('#mfCost').value||0;
  var rec={id:id,n:name,cat:'My recipe',sv:sv,t:+q('#mfT').value||20,
    k:+q('#mfK').value||0,p:+q('#mfP').value||0,c:+q('#mfC').value||0,f:+q('#mfF').value||0,
    fib:0,leu:0,tg:[],cw:cps*sv,cws:cps,cc:cps*sv,ccs:cps,
    ing:q('#mfIng').value.split('\\n').filter(Boolean).map(function(l){return [l.trim(),0];}),
    st:q('#mfSteps').value.split('\\n').filter(Boolean)};
  S.mine.push(rec);
  if(pendingPhoto) S.photos[id]=pendingPhoto;
  pendingPhoto=null;
  ['#mfName','#mfK','#mfP','#mfC','#mfF','#mfCost','#mfIng','#mfSteps'].forEach(function(s){q(s).value='';});
  q('#mfPrev').hidden=true; q('#mineForm').hidden=true;
  save(); renderAll();
};
function renderMine(){
  if(!S.mine.length){ q('#mineOut').innerHTML='<p class="small">Nothing yet. Add one and it shows up here and in the recommender.</p>'; return; }
  q('#mineOut').innerHTML = '<div class="reccards">'+S.mine.map(card).join('')+'</div>';
  wire(q('#mineOut'));
}

/* ---------------- backup ---------------- */
q('#btnExport').onclick=function(){
  var b=new Blob([JSON.stringify(S,null,1)],{type:'application/json'});
  var a=document.createElement('a'); a.href=URL.createObjectURL(b);
  a.download='meal-handbook-backup.json'; a.click();
};
q('#btnImport').onclick=function(){ q('#fileImport').click(); };
q('#fileImport').onchange=function(){
  var f=q('#fileImport').files[0]; if(!f) return;
  var fr=new FileReader();
  fr.onload=function(){ try{ S=JSON.parse(fr.result); save(); location.reload(); }
    catch(e){ alert('That file did not read as a backup.'); } };
  fr.readAsText(f);
};

/* ---------------- library price swap ---------------- */
function repriceLibrary(){
  qa('[data-cost-w]').forEach(function(el){
    el.textContent = S.store==='costco' ? el.dataset.costC : el.dataset.costW;
  });
  qa('[data-store-label]').forEach(function(el){
    el.textContent = S.store==='costco' ? 'Costco' : 'Walmart';
  });
}

function renderAll(){ renderLists(); renderMine(); }

['#rcTrain','#rcKcal','#rcProt','#rcTime','#rcMood','#rcMeat'].forEach(function(s){
  var e=q(s); if(e) e.onchange=recommend;
});
qa('.who').forEach(function(b){ if(b.dataset.who===S.who) b.click(); });
qa('.store').forEach(function(b){ if(b.dataset.store===S.store) b.click(); });
drawTargets(); recommend(); renderAll(); repriceLibrary();

/* reveal-on-scroll */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('vis'); io.unobserve(e.target);} });
  },{rootMargin:'0px 0px -8% 0px'});
  qa('h2, .recipe, .callout, .stripe, .listcard, table').forEach(function(el){
    el.classList.add('rev'); io.observe(el);
  });
}
})();
</script>
""".replace("__ROWS__", json.dumps(rows, separators=(",", ":"))).replace("__TGT__", targets_json)
