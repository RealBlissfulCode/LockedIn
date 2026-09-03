# -*- coding: utf-8 -*-
APP_WIRE = r"""
/* ============================ router ============================ */
/* [route, desktop label, bottom-bar label]. Six tabs is the most the bottom bar
   holds on a 360px phone, which is why the short labels exist. */
var TABS=[['meals','Meals','Meals'],['training','Training','Train'],
          ['shopping','Shopping','Shop'],['financial','Financial','Money'],
          ['planning','Planning','Plans'],['schedule','Schedule','Cal']];
var ICO={meals:'<path d="M4 3v8a3 3 0 006 0V3M7 11v10M16 3c-1.5 2-2 4-2 6s.5 3 2 3 2-1 2-3-.5-4-2-6zM16 12v9"/>',
 training:'<path d="M6 8v8M18 8v8M3 10v4M21 10v4M6 12h12"/>',
 shopping:'<path d="M3 4h2l2 12h11M7 8h14l-2 6H8"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/>',
 financial:'<path d="M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>',
 planning:'<path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 13l2 2 4-4"/>',
 schedule:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'};
function chrome(){
  $('#tabs').innerHTML=TABS.map(function(t){return '<button class="tab" data-v="'+t[0]+'" data-nav="'+t[0]+'">'+t[1]+'</button>';}).join('');
  $('#btm').innerHTML=TABS.map(function(t){return '<button data-v="'+t[0]+'" data-nav="'+t[0]+'" aria-label="'+t[1]+'">'+
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'+
    ICO[t[0]]+'</svg><span>'+t[2]+'</span></button>';}).join('');
  $('#who').innerHTML=['j','a'].map(function(k){return '<button data-w="'+k+'"'+
    (S.who===k?' class="on"':'')+'>'+E(S.prof[k].name)+'</button>';}).join('');
  var sp=$('#syncSlot'); if(sp) sp.innerHTML=syncPill();
  var th=$('#themeBtn');
  if(th){var cur=S.theme||'dark';
    th.title='Theme: '+cur;
    th.innerHTML = cur==='light'
      ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>'
      : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg>';
    th.onclick=function(){
      S.theme=(S.theme==='dark')?'light':(S.theme==='light')?'auto':'dark';
      save(); applyTheme(); chrome(); toast('Theme: '+S.theme);};}
  var g=$('#settings');
  if(g) g.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'+
    '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06A1.65 1.65 0 009 4.6h.09A1.65 1.65 0 0010.6 3.09V3a2 2 0 114 0v.09A1.65 1.65 0 0015 4.6a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06A1.65 1.65 0 0019.4 9v.09A1.65 1.65 0 0021 10.6a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>';
}
function errPanel(where,e){
  return '<div class="page"><div class="errbox"><h3>'+E(where)+' hit an error</h3>'+
   '<p class="sm">The rest of the app still works. Send this text along with a saved data file '+
   'and it can be fixed.</p><pre>'+E((e&&e.message)||String(e))+'\n\n'+
   E(((e&&e.stack)||'').split('\n').slice(0,4).join('\n'))+'</pre>'+
   '<div class="row" style="margin-top:12px"><button class="b o" data-nav="meals">Go to Meals</button>'+
   '<button class="b o" id="settings">Open settings</button></div></div></div>';
}
/* A redraw asked for by a switch is not a navigation. It keeps the scroll
   position and skips the page's slide-in, so the only thing that moves is the
   part that changed: the numbers roll and the bars regrow. */
var _quiet=false;
function reroute(){_quiet=true;route();}
function route(){
  var h=(location.hash||'#/meals').slice(2).split('/'), v=h[0]||'meals', sub=h[1]||'';
  var m=$('#view'); if(!m) return;
  var quiet=_quiet, keepY=quiet?(window.pageYOffset||0):0;
  _quiet=false;
  var html;
  try{
    html = v==='r'?vRecipe(sub) : v==='training'?vTraining(sub) : v==='shopping'?vShopping(sub)
      : v==='financial'?vFinancial(sub) : v==='planning'?vPlanning(sub)
      : v==='lists'?vRecipeLists()
      : v==='schedule'?vSchedule(sub) : vMeals();
  }catch(e){ html=errPanel(v.charAt(0).toUpperCase()+v.slice(1),e);
    if(window.console&&console.error)console.error(e); }
  m.innerHTML=html;
  if(quiet){var _pg=m.querySelector('.page'); if(_pg)_pg.classList.add('noanim');}
  try{window.scrollTo(0,quiet?keepY:0);}catch(e){}
  try{
    $$('.tab,.btmnav button').forEach(function(b){
      b.classList.toggle('on', b.dataset.v===(v==='r'?'meals':v));});
    $$('#who button').forEach(function(b){b.classList.toggle('on', b.dataset.w===S.who);});
  }catch(e){}
  try{ bind(); }catch(e){ if(window.console&&console.error)console.error('bind',e); }
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
  if(v==='lists'){
    on('#rlNew','click',function(){
      var n=prompt('Name the list','Sunday prep'); if(!n)return;
      if(!S.lists[n]) S.lists[n]=[];
      save();route();});
  }
  if(v==='financial') bindFin(h[1]);
  if(v==='planning') bindPlan(h[1]);
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
  ['#costAdd','#costAdd2'].forEach(function(s){on(s,'click',function(){costEditor(null);});});
  on('#shAdd','click',function(){shiftEditor();});
  on('#shCsv','click',function(){
    var rows=[['Date','Who','Job','Hours','Gross','Net','Note']];
    S.fin.shifts.forEach(function(s){var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
      rows.push([s.date,j?WHO(j.who):'',j?j.name:'',s.hours,s.gross,s.net,s.note||'']);});
    dl('shifts-'+today()+'.csv',toCSV(rows),'text/csv');});
  on('#scenFromActual','click',function(){
    var from=new Date();from.setDate(from.getDate()-90);
    var f=from.getFullYear()+'-'+p2(from.getMonth()+1)+'-'+p2(from.getDate());
    var net=shiftsFor(null,f).reduce(function(a,s){return a+(s.net||0);},0)/(90/30.4);
    S.fin.scenarios['From actual earnings']={mode:'actual',path:S.fin.path||'rent',
      inc:Math.round(net),cost:finCost('real',S.fin.path||'rent'),saved:today(),auto:true};
    save();toast('Saved from real data');route();});
  on('#bpNew','click',function(){bpListEditor(null);});
  on('#stNew','click',function(){stratListEditor(null);});
  on('#stMode','change',function(){S.fin.stratMode=this.value;save();route();});
  countUp($('#view'));
}
/* ---------------- switching lines in and out ----------------
   One writer for every switch on the page. It never deletes and never edits a
   figure: it sets `off` and redraws. Because `off` is part of the snapshot a
   scenario stores, flipping one marks the open scenario dirty exactly like
   changing a number does, which is the behaviour you want — the switches are
   part of the plan, not a view setting. */
function finToggle(kind,pred,to){
  var arr=kind==='jobs'?S.fin.jobs:S.fin.costs, n=0;
  arr.forEach(function(x){
    if(!pred(x)) return;
    var want=(to===null||to===undefined)?!x.off:!to;
    if(!!x.off===want) return;
    x.off=want; n++;});
  if(n){save();reroute();}
  return n;
}
var ONOFF=[['1','Counted in the totals'],['0','Switched off']];
function jobEditor(id){
  var j=id?S.fin.jobs.filter(function(x){return x.id===id;})[0]:{who:'Jaron',name:'',employer:'',title:'',rate:'',low:'',real:'',high:'',actual:''};
  var m=modal(id?'Edit income':'Add income',
    form([{id:'jw',l:'Who',t:'select',o:whoOpts(),v:j.who},
      {id:'jn',l:'Name',v:j.name,ph:'Ritchey day job'},
      {id:'je',l:'Employer',v:j.employer},{id:'jt',l:'Title',v:j.title},
      {id:'jr',l:'Hourly rate',t:'number',step:'0.01',v:j.rate},
      {id:'jl',l:'Low / mo',t:'number',v:j.low},{id:'jm',l:'Realistic / mo',t:'number',v:j.real},
      {id:'jh',l:'High / mo',t:'number',v:j.high},
      {id:'ja',l:'Actual / mo',t:'number',v:j.actual},
      {id:'jo',l:'Counted',t:'select',o:ONOFF,v:j.off?'0':'1'}]),
    (id?'<button class="b o dz" id="jDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="jSave">Save</button>');
  var dl_=$('#jDel',m); if(dl_)dl_.onclick=function(){
    S.fin.jobs=S.fin.jobs.filter(function(x){return x.id!==id;});save();m.remove();route();};
  $('#jSave',m).onclick=function(){
    var o={id:id||uid(),who:$('#jw',m).value,name:$('#jn',m).value.trim()||'Income',
      employer:$('#je',m).value,title:$('#jt',m).value,rate:num($('#jr',m).value)||null,
      low:num($('#jl',m).value),real:num($('#jm',m).value),high:num($('#jh',m).value),
      actual:num($('#ja',m).value)||null,off:$('#jo',m).value==='0'};
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
      {id:'cw',l:'Who',t:'select',o:whoOpts(),v:c.who},
      {id:'cl',l:'Low',t:'number',v:c.low},{id:'cr',l:'Realistic',t:'number',v:c.real},
      {id:'ch',l:'High',t:'number',v:c.high},{id:'ca',l:'Actual',t:'number',v:c.actual},
      {id:'co',l:'Counted',t:'select',o:ONOFF,v:c.off?'0':'1'}]),
    (id?'<button class="b o dz" id="cDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="cSave">Save</button>');
  var d=$('#cDel',m); if(d)d.onclick=function(){
    S.fin.costs=S.fin.costs.filter(function(x){return x.id!==id;});save();m.remove();route();};
  $('#cSave',m).onclick=function(){
    var o={id:id||uid(),name:$('#cn',m).value.trim()||'Cost',section:$('#cs',m).value,
      who:$('#cw',m).value,low:num($('#cl',m).value),real:num($('#cr',m).value),
      high:num($('#ch',m).value),actual:num($('#ca',m).value)||null,
      off:$('#co',m).value==='0'};
    if(id)S.fin.costs=S.fin.costs.map(function(x){return x.id===id?o:x;}); else S.fin.costs.push(o);
    save();m.remove();route();};
}
function shiftEditor(){
  if(!S.fin.jobs.length){toast('Add a job first');return;}
  var m=modal('Log a shift',
    form([{id:'sd',l:'Date',t:'date',v:today()},
      {id:'sj',l:'Job',t:'select',o:S.fin.jobs.map(function(j){return [j.id,WHO(j.who)+' - '+j.name];}),v:S.fin.jobs[0].id},
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
/* Lists are keyed by their name, so renaming one means rebuilding the object.
   Done in place rather than delete-and-add so the list keeps its position. */
function renameKey(obj,from,to){
  if(from===to) return true;
  if(obj[to]) { toast('"'+to+'" already exists'); return false; }
  var out={};
  Object.keys(obj).forEach(function(k){ out[k===from?to:k]=obj[k]; });
  Object.keys(obj).forEach(function(k){ delete obj[k]; });
  Object.keys(out).forEach(function(k){ obj[k]=out[k]; });
  return true;
}
function bpListEditor(name){
  var isNew=!name, L=isNew?{cat:'Housing',note:'',items:[]}:S.fin.purchases[name];
  if(!isNew&&!L) return;
  var m=modal(isNew?'New list':'Edit list',
    form([{id:'ln',l:'List name',v:isNew?'':name,ph:'Places we could rent'},
      {id:'lc',l:'What kind',v:L.cat||'',ph:'Housing, Cars, Furniture...'},
      {id:'lo',l:'Note',t:'area',v:L.note||''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="lSave">Save</button>');
  $('#lSave',m).onclick=function(){
    var n=$('#ln',m).value.trim(); if(!n){toast('Give it a name');return;}
    if(isNew){
      if(S.fin.purchases[n]){toast('"'+n+'" already exists');return;}
      S.fin.purchases[n]={cat:$('#lc',m).value.trim(),note:$('#lo',m).value.trim(),items:[]};
    }else{
      if(!renameKey(S.fin.purchases,name,n)) return;
      S.fin.purchases[n].cat=$('#lc',m).value.trim();
      S.fin.purchases[n].note=$('#lo',m).value.trim();
    }
    save();m.remove();route();};
}
function bpItemEditor(listName,idx){
  var L=S.fin.purchases[listName]; if(!L) return;
  var editing=(idx!==null&&idx!==undefined);
  var it=editing?L.items[idx]:{name:'',price:'',link:'',notes:'',fields:{}};
  if(!it) return;
  var cat=(L.cat||'').toLowerCase();
  var labels = cat.indexOf('hous')>=0 ? ['City','Beds','Baths','Sq ft','To CSU','All in']
             : cat.indexOf('car')>=0 ? ['Year','Miles','MPG','Condition']
             : ['Detail 1','Detail 2','Detail 3'];
  /* Keep whatever fields the item already carries, even ones this category
     would not have offered, so editing a seeded row never drops data. */
  Object.keys(it.fields||{}).forEach(function(k){
    if(labels.indexOf(k)<0) labels.push(k);});
  var extra=labels.map(function(l,i){return {id:'f'+i,l:l,v:(it.fields||{})[l]||''};});
  var m=modal(editing?'Edit '+it.name:'Add to '+listName,
    form([{id:'bn',l:'Name',v:it.name},{id:'bp',l:'Price / rent',t:'number',v:it.price},
      {id:'bl',l:'Link',v:it.link||''}].concat(extra)
      .concat([{id:'bo',l:'Notes',t:'area',v:it.notes||''}])),
    (editing?'<button class="b o dz" id="bDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="bSave">Save</button>');
  var d=$('#bDel',m); if(d)d.onclick=function(){
    L.items.splice(idx,1);save();m.remove();route();};
  $('#bSave',m).onclick=function(){
    var f={}; extra.forEach(function(x){var v=$('#'+x.id,m).value.trim(); if(v)f[x.l]=v;});
    var o={id:it.id||uid(),name:$('#bn',m).value.trim()||'Item',price:num($('#bp',m).value),
      link:$('#bl',m).value.trim(),notes:$('#bo',m).value.trim(),fields:f};
    if(editing) L.items[idx]=o; else L.items.push(o);
    save();m.remove();route();};
}

/* ============================ strategies wiring ============================ */
function stratListEditor(name){
  var isNew=!name, L=isNew?{note:'',items:[]}:S.fin.strategies[name];
  if(!isNew&&!L) return;
  var m=modal(isNew?'New strategy list':'Edit list',
    form([{id:'sn',l:'List name',v:isNew?'':name,ph:'Ways to earn more'},
      {id:'so',l:'Note',t:'area',v:L.note||''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="slSave">Save</button>');
  $('#slSave',m).onclick=function(){
    var n=$('#sn',m).value.trim(); if(!n){toast('Give it a name');return;}
    if(isNew){
      if(S.fin.strategies[n]){toast('"'+n+'" already exists');return;}
      S.fin.strategies[n]={note:$('#so',m).value.trim(),items:[]};
    }else{
      if(!renameKey(S.fin.strategies,name,n)) return;
      S.fin.strategies[n].note=$('#so',m).value.trim();
    }
    save();m.remove();route();};
}
function stratEditor(listName,idx){
  var L=S.fin.strategies[listName]; if(!L) return;
  var editing=(idx!==null&&idx!==undefined);
  var it=editing?L.items[idx]:{name:'',low:'',real:'',high:'',rate:'',effort:'',
    when:'',status:'NOT DONE',how:''};
  if(!it) return;
  var STATUS=['NOT DONE','READY','ACTIVE','PENDING','ON TRACK','STAGED','IN PROGRESS','DONE',
    'CRITICAL','LOCKED','KEY','CHECK FIRST','HOLD','BLOCKED','DEAD','N/A'];
  if(it.status&&STATUS.indexOf(it.status)<0) STATUS.unshift(it.status);
  var m=modal(editing?'Edit strategy':'New strategy',
    form([{id:'xn',l:'Move',v:it.name,ph:'Shop auto insurance properly'},
      {id:'xs',l:'Status',t:'select',o:STATUS.map(function(s){return [s,s];}),v:it.status},
      {id:'xl',l:'Low / mo',t:'number',v:it.low},
      {id:'xr',l:'Realistic / mo',t:'number',v:it.real},
      {id:'xh',l:'High / mo',t:'number',v:it.high},
      {id:'xp',l:'Per hour',v:it.rate,ph:'$50'},
      {id:'xe',l:'Effort',v:it.effort,ph:'1 afternoon'},
      {id:'xw',l:'When',v:it.when,ph:'Before lease'},
      {id:'xo',l:'How and why',t:'area',v:it.how}])+
    '<p class="sm muted">Anything marked Dead, Blocked or N/A is left out of the totals, so '+
    'ruling something out does not quietly inflate the plan.</p>',
    (editing?'<button class="b o dz" id="xDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="xSave">Save</button>');
  var d=$('#xDel',m); if(d)d.onclick=function(){
    L.items.splice(idx,1);save();m.remove();route();};
  $('#xSave',m).onclick=function(){
    var o={id:it.id||uid(),name:$('#xn',m).value.trim()||'Move',
      low:num($('#xl',m).value),real:num($('#xr',m).value),high:num($('#xh',m).value),
      rate:$('#xp',m).value.trim(),effort:$('#xe',m).value.trim(),
      when:$('#xw',m).value.trim(),status:$('#xs',m).value,how:$('#xo',m).value.trim()};
    if(editing) L.items[idx]=o; else L.items.push(o);
    save();m.remove();route();};
}

/* ============================ planning wiring ============================ */
function bindPlan(){
  on('#plNew','click',function(){planColEditor(null);});
}
function planSub(colId,subId){
  var c=planCol(colId); if(!c) return null;
  var s=(c.subs||[]).filter(function(x){return x.id===subId;});
  return s[0]||null;
}
function planColEditor(id){
  var c=id?planCol(id):{name:'',note:''};
  if(!c) return;
  var m=modal(id?'Edit plan':'New collection',
    form([{id:'pn',l:'Name',v:c.name,ph:'Moving in together'},
      {id:'po',l:'Note',t:'area',v:c.note||''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="pSave">Save</button>');
  $('#pSave',m).onclick=function(){
    var n=$('#pn',m).value.trim(); if(!n){toast('Give it a name');return;}
    if(id){ c.name=n; c.note=$('#po',m).value.trim(); }
    else { S.plan.cols.push({id:uid(),name:n,note:$('#po',m).value.trim(),subs:[]}); }
    save();m.remove();route();};
}
function planSubEditor(colId,subId){
  var c=planCol(colId); if(!c) return;
  var s=subId?planSub(colId,subId):{name:'',note:''};
  if(!s) return;
  var m=modal(subId?'Edit section':'New section',
    form([{id:'qn',l:'Section name',v:s.name,ph:'Memberships and accounts'},
      {id:'qo',l:'Note',t:'area',v:s.note||''}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="qSave">Save</button>');
  $('#qSave',m).onclick=function(){
    var n=$('#qn',m).value.trim(); if(!n){toast('Give it a name');return;}
    if(subId){ s.name=n; s.note=$('#qo',m).value.trim(); }
    else { c.subs.push({id:uid(),name:n,note:$('#qo',m).value.trim(),items:[]}); }
    save();m.remove();route();};
}
function planItemEditor(colId,subId,itemId){
  var s=planSub(colId,subId); if(!s) return;
  var it=itemId?(s.items||[]).filter(function(x){return x.id===itemId;})[0]:{text:'',note:''};
  if(!it) return;
  var m=modal(itemId?'Edit item':'New item',
    form([{id:'in',l:'Item',v:it.text,ph:'Costco Gold Star membership'},
      {id:'io',l:'Note',t:'area',v:it.note||''}]),
    (itemId?'<button class="b o dz" id="iDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="iSave">Save</button>');
  var d=$('#iDel',m); if(d)d.onclick=function(){
    s.items=s.items.filter(function(x){return x.id!==itemId;});save();m.remove();route();};
  $('#iSave',m).onclick=function(){
    var t=$('#in',m).value.trim(); if(!t){toast('Say what it is');return;}
    if(itemId){ it.text=t; it.note=$('#io',m).value.trim(); }
    else { s.items.push({id:uid(),text:t,note:$('#io',m).value.trim(),done:false}); }
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
  on('#tcNew','click',function(){tmplColEditor(null);});
  on('#calCsv','click',function(){
    var rows=[['Date','Who','Training','Kcal','Protein','FoodCost','OtherSpend','Plans','Notes']];
    Object.keys(S.days).sort().forEach(function(d){var r=S.days[d],e=eaten(d);
      var sp=(r.spend||[]).reduce(function(a,x){return a+(x.amt||0);},0);
      rows.push([d,P().name,TRAIN[r.workout]?TRAIN[r.workout].n:r.workout,Math.round(e.kcal),
        Math.round(e.p),e.cost.toFixed(2),sp.toFixed(2),
        (r.sched||[]).map(function(x){return WHO(x.who)+':'+x.what;}).join('; '),r.notes||'']);});
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
      var dd=dayLog(ds);dd.meals.push({id:row.dataset.a,q:1,who:ME(),at:defMealTime(dd.meals.length)});save();toast('Logged for '+MENAME());};});}
  draw('');$('#mpq',m).oninput=function(){draw(this.value);};
}
function tmplEditor(colId,dayIdx){
  var c=tmplCol(colId); if(!c) return;
  var m=modal('Every '+DOW[dayIdx]+' — '+c.name,
    form([{id:'tw',l:'Who',t:'select',o:whoOpts(),v:ME()},
      {id:'tx',l:'What',v:'',ph:'Church, work, class, gym'},
      {id:'tl',l:'Where',v:'',ph:'The shop, CSU, home'},
      {id:'tf',l:'From',t:'time',v:'09:00'},{id:'tt',l:'To',t:'time',v:'17:00'}]),
    '<button class="b o" data-close>Cancel</button><button class="b" id="tSave2">Add</button>');
  $('#tSave2',m).onclick=function(){
    if(!c.days) c.days={};
    if(!c.days[dayIdx]) c.days[dayIdx]=[];
    c.days[dayIdx].push({id:uid(),who:$('#tw',m).value,what:$('#tx',m).value.trim()||'Busy',
      where:$('#tl',m).value.trim(),from:$('#tf',m).value,to:$('#tt',m).value});
    save();m.remove();route();};
}
function tmplColEditor(id){
  var isNew=!id, c=isNew?{name:'',note:'',repeat:'weekly',anchor:today(),fav:false,
    active:false,days:{}}:tmplCol(id);
  if(!c) return;
  var m=modal(isNew?'New template':'Template settings',
    form([{id:'kn',l:'Name',v:c.name,ph:'The ordinary week'},
      {id:'kr',l:'How often',t:'select',o:REPEATS,v:c.repeat||'weekly'},
      {id:'ka',l:'Counting from',t:'date',v:c.anchor||today()},
      {id:'ko',l:'Note',t:'area',v:c.note||''}])+
    '<p class="sm muted">"Counting from" only matters for every other week and once a month: '+
    'it is the date the pattern lines up with. Weekly ignores it.</p>',
    (isNew?'':'<button class="b o dz" id="kDel">Delete</button>')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="kSave">Save</button>');
  var d=$('#kDel',m); if(d)d.onclick=function(){
    if(!confirm('Delete "'+c.name+'"? Days it already wrote onto the calendar stay.'))return;
    S.sched.cols=tmplCols().filter(function(x){return x.id!==id;});
    save();m.remove();nav('schedule/templates');};
  $('#kSave',m).onclick=function(){
    var n=$('#kn',m).value.trim(); if(!n){toast('Give it a name');return;}
    if(isNew){
      S.sched.cols=tmplCols();
      S.sched.cols.push({id:uid(),name:n,note:$('#ko',m).value.trim(),
        repeat:$('#kr',m).value,anchor:$('#ka',m).value||today(),
        fav:false,active:false,days:{}});
    }else{
      c.name=n; c.note=$('#ko',m).value.trim();
      c.repeat=$('#kr',m).value; c.anchor=$('#ka',m).value||today();
    }
    save();m.remove();route();};
}
function tmplApplyModal(id){
  var c=tmplCol(id); if(!c) return;
  if(!tmplCount(c)){toast('Nothing in this template yet');return;}
  var m=modal('Apply "'+c.name+'"',
    form([{id:'as',l:'How far',t:'select',o:SCOPES,v:'week'}])+
    '<p class="sm muted">This copies the items onto real days, so you can then change any one of '+
    'them without touching the template. Days that already have the same item are skipped, so '+
    'applying twice is safe.</p>'+
    (c.active?'<div class="note good"><b>Note.</b> This one is already running, so it shows on '+
      'matching days anyway. Applying is only worth it if you want to edit individual days.</div>':''),
    '<button class="b o" data-close>Cancel</button><button class="b" id="aGo">Apply</button>');
  $('#aGo',m).onclick=function(){
    var n=applyCollection(id,$('#as',m).value);
    m.remove();route();
    toast(n?n+' item'+(n===1?'':'s')+' added':'Nothing new to add');};
}

/* ============================ global events ============================ */
document.addEventListener('click',function(e){
  var el, t=e.target;
  if(!t||!t.closest) return;
  try{
  if((el=t.closest('[data-nav]'))){nav(el.dataset.nav);return;}
  if((el=t.closest('[data-w]'))){S.who=el.dataset.w;save();route();return;}
  if((el=t.closest('[data-fav]'))){e.stopPropagation();
    var id=el.dataset.fav,i=S.fav.indexOf(id);
    if(i>=0)S.fav.splice(i,1);else S.fav.push(id); save();route();return;}
  if((el=t.closest('[data-go]'))){nav('r/'+el.dataset.go);return;}
  if((el=t.closest('[data-log]'))){var dt=dayLog(today());
    dt.meals.push({id:el.dataset.log,q:1,who:ME(),at:defMealTime(dt.meals.length)});
    save();toast('Logged to today for '+MENAME());return;}
  if((el=t.closest('[data-groc]'))){addRecipeToShop(byId(el.dataset.groc));
    toast('Added to '+S.shop.active);return;}
  if((el=t.closest('[data-tolist]'))){listModal(el.dataset.tolist);return;}
  if((el=t.closest('[data-rlrm]'))){var rr=el.dataset.rlrm.split('|');
    var arr=S.lists[rr[0]]||[]; var ri=arr.indexOf(rr[1]);
    if(ri>=0){arr.splice(ri,1);save();route();} return;}
  if((el=t.closest('[data-rle]'))){var on_=el.dataset.rle;
    var nn=prompt('Rename the list',on_); if(!nn||nn===on_)return;
    if(S.lists[nn]){toast('"'+nn+'" already exists');return;}
    if(!renameKey(S.lists,on_,nn))return; save();route();return;}
  if((el=t.closest('[data-rld]'))){
    if(confirm('Delete the list "'+el.dataset.rld+'"? The recipes themselves stay.')){
      delete S.lists[el.dataset.rld];save();route();} return;}
  if((el=t.closest('[data-rlgroc]'))){
    var added=0;
    (S.lists[el.dataset.rlgroc]||[]).map(byId).filter(Boolean).forEach(function(r){
      addRecipeToShop(r);added++;});
    toast(added?added+' recipe'+(added===1?'':'s')+' added to '+S.shop.active:'Nothing to add');
    return;}
  if((el=t.closest('[data-photo]'))){pickPhoto(el.dataset.photo);return;}
  if((el=t.closest('[data-card]'))){cardPNG(byId(el.dataset.card));return;}
  if((el=t.closest('[data-list]'))){S.shop.active=el.dataset.list;save();route();return;}
  if((el=t.closest('[data-gt]'))){var L=curList();
    L.items[+el.dataset.gt].done=el.checked;save();route();return;}
  if((el=t.closest('[data-gd]'))){curList().items.splice(+el.dataset.gd,1);save();route();return;}
  if((el=t.closest('[data-ge]'))){shopItemEditor(+el.dataset.ge);return;}
  if((el=t.closest('[data-ie]'))){ingEditor(el.dataset.ie);return;}
  if((el=t.closest('[data-sess]'))){sessModal(+el.dataset.sess);return;}
  if((el=t.closest('[data-jobe]'))){jobEditor(el.dataset.jobe);return;}
  if((el=t.closest('[data-coste]'))){costEditor(el.dataset.coste);return;}

  /* switches: one line, a whole cost section, one earner, or everything */
  if((el=t.closest('[data-jobtog]'))){var jid=el.dataset.jobtog;
    finToggle('jobs',function(x){return x.id===jid;},null);return;}
  if((el=t.closest('[data-costtog]'))){var cid=el.dataset.costtog;
    finToggle('costs',function(x){return x.id===cid;},null);return;}
  if((el=t.closest('[data-secttog]'))){
    var sect=el.dataset.secttog, pth=S.fin.path||'rent';
    var anyOn=S.fin.costs.some(function(c){
      return c.section===sect&&costInPath(c,pth)&&finLive(c);});
    finToggle('costs',function(c){return c.section===sect&&costInPath(c,pth);},!anyOn);
    return;}
  if((el=t.closest('[data-whotog]'))){
    var wk=el.dataset.whotog;
    var onNow=S.fin.jobs.some(function(j){return j.who===wk&&finLive(j);});
    finToggle('jobs',function(j){return j.who===wk;},!onNow);
    return;}
  if((el=t.closest('[data-alltog]'))){
    var ap=el.dataset.alltog.split('|'), want=ap[1]==='1';
    var pth2=S.fin.path||'rent';
    var moved=finToggle(ap[0],ap[0]==='costs'
      ?function(c){return costInPath(c,pth2);}
      :function(){return true;},want);
    if(!moved) toast(want?'Everything was already counted':'Everything was already off');
    return;}
  if((el=t.closest('[data-shd]'))){S.fin.shifts=S.fin.shifts.filter(function(x){
    return x.id!==el.dataset.shd;});save();route();return;}
  if((el=t.closest('[data-scload]'))){
    if(scenDirty()&&!confirm('Unsaved changes will be lost. Continue?')){return;}
    scenLoad(el.dataset.scload);route();toast('Opened '+el.dataset.scload);return;}
  if((el=t.closest('[data-scdel]'))){
    if(confirm('Delete scenario "'+el.dataset.scdel+'"?')){
      delete S.fin.scenarios[el.dataset.scdel];
      if(S.fin.activeScenario===el.dataset.scdel)S.fin.activeScenario=null;
      save();route();}return;}
  if((el=t.closest('[data-bpadd]'))){bpItemEditor(el.dataset.bpadd,null);return;}
  if((el=t.closest('[data-bple]'))){bpListEditor(el.dataset.bple);return;}
  if((el=t.closest('[data-bpdel]'))){var bn=el.dataset.bpdel;
    if(confirm('Delete the list "'+bn+'" and everything on it?')){
      delete S.fin.purchases[bn];save();route();}return;}
  if((el=t.closest('[data-bpie]'))){var pe=el.dataset.bpie.split('|');
    bpItemEditor(pe[0],+pe[1]);return;}
  if((el=t.closest('[data-bpi]'))){var p=el.dataset.bpi.split('|');
    S.fin.purchases[p[0]].items.splice(+p[1],1);save();route();return;}

  /* strategies */
  if((el=t.closest('[data-stadd]'))){stratEditor(el.dataset.stadd,null);return;}
  if((el=t.closest('[data-stle]'))){stratListEditor(el.dataset.stle);return;}
  if((el=t.closest('[data-stdel]'))){var sn=el.dataset.stdel;
    if(confirm('Delete the list "'+sn+'" and every strategy on it?')){
      delete S.fin.strategies[sn];save();route();}return;}
  if((el=t.closest('[data-stie]'))){var se=el.dataset.stie.split('|');
    stratEditor(se[0],+se[1]);return;}
  if((el=t.closest('[data-stid]'))){var sd=el.dataset.stid.split('|');
    if(confirm('Delete this strategy?')){
      S.fin.strategies[sd[0]].items.splice(+sd[1],1);save();route();}return;}

  /* planning */
  if((el=t.closest('[data-plgo]'))){nav('planning/'+el.dataset.plgo);return;}
  if((el=t.closest('[data-ple]'))){planColEditor(el.dataset.ple);return;}
  if((el=t.closest('[data-pld]'))){var pc=planCol(el.dataset.pld);
    if(pc&&confirm('Delete "'+pc.name+'" and every section in it?')){
      S.plan.cols=S.plan.cols.filter(function(x){return x.id!==el.dataset.pld;});
      save();nav('planning');}return;}
  if((el=t.closest('[data-plsadd]'))){planSubEditor(el.dataset.plsadd,null);return;}
  if((el=t.closest('[data-plse]'))){var q=el.dataset.plse.split('|');
    planSubEditor(q[0],q[1]);return;}
  if((el=t.closest('[data-plsd]'))){var qd=el.dataset.plsd.split('|');
    var pcol=planCol(qd[0]), psub=planSub(qd[0],qd[1]);
    if(pcol&&psub&&confirm('Delete the section "'+psub.name+'"?')){
      pcol.subs=pcol.subs.filter(function(x){return x.id!==qd[1];});save();route();}return;}
  if((el=t.closest('[data-pliadd]'))){var ia=el.dataset.pliadd.split('|');
    planItemEditor(ia[0],ia[1],null);return;}
  if((el=t.closest('[data-plie]'))){var ie=el.dataset.plie.split('|');
    planItemEditor(ie[0],ie[1],ie[2]);return;}
  if((el=t.closest('[data-plid]'))){var idl=el.dataset.plid.split('|');
    var dsub=planSub(idl[0],idl[1]);
    if(dsub){dsub.items=dsub.items.filter(function(x){return x.id!==idl[2];});save();route();}
    return;}
  if((el=t.closest('[data-plck]'))){var ck=el.dataset.plck.split('|');
    var csub=planSub(ck[0],ck[1]);
    if(csub){csub.items.forEach(function(x){ if(x.id===ck[2]) x.done=el.checked; });
      save();
      /* Repaint just this row and the counters, so ticking a box does not
         scroll the page back to the top mid-list. */
      var row=el.closest('.pitem'); if(row) row.classList.toggle('done',el.checked);
      var c2=planCol(ck[0]);
      if(c2){var n2=planCount(c2);
        $$('.stat b').forEach(function(b,i){ if(i===0)b.textContent=n2.pct+'%';
          if(i===1)b.textContent=n2.done; if(i===2)b.textContent=n2.total-n2.done; });
        var sd2=(csub.items||[]).filter(function(x){return x.done;}).length;
        var chip=row&&row.closest('.sec')&&row.closest('.sec').querySelector('.chip.p');
        if(chip) chip.textContent=sd2+' / '+csub.items.length;}}
    return;}
  if((el=t.closest('[data-d]'))){calSel=el.dataset.d;route();return;}
  if((el=t.closest('[data-evd]'))){dayLog(calSel).sched.splice(+el.dataset.evd,1);save();route();return;}
  if((el=t.closest('[data-spd]'))){dayLog(calSel).spend.splice(+el.dataset.spd,1);save();route();return;}
  if((el=t.closest('[data-mld]'))){dayLog(calSel).meals.splice(+el.dataset.mld,1);save();route();return;}
  if((el=t.closest('[data-tadd]'))){var ta=el.dataset.tadd.split('|');
    tmplEditor(ta[0],+ta[1]);return;}
  if((el=t.closest('[data-td]'))){var q=el.dataset.td.split('|');
    var tc=tmplCol(q[0]);
    if(tc&&tc.days&&tc.days[q[1]]){tc.days[q[1]].splice(+q[2],1);save();route();}
    return;}
  /* template collections */
  if((el=t.closest('[data-tcopen]'))){nav('schedule/templates/'+el.dataset.tcopen);return;}
  if((el=t.closest('[data-tcedit]'))){tmplColEditor(el.dataset.tcedit);return;}
  if((el=t.closest('[data-tcapply]'))){tmplApplyModal(el.dataset.tcapply);return;}
  if((el=t.closest('[data-tctoggle]'))){var tt=tmplCol(el.dataset.tctoggle);
    if(tt){ if(!tt.active&&(tt.repeat||'weekly')==='once'){
        toast('Set it to repeat before it can run'); tmplColEditor(tt.id); return; }
      tt.active=!tt.active; save(); route();
      toast(tt.active?'"'+tt.name+'" is running':'"'+tt.name+'" stopped'); }
    return;}
  if((el=t.closest('[data-tcfav]'))){var tf=tmplCol(el.dataset.tcfav);
    if(tf){tf.fav=!tf.fav;save();route();} return;}
  if((el=t.closest('[data-tcdel]'))){var tdc=tmplCol(el.dataset.tcdel);
    if(tdc&&confirm('Delete "'+tdc.name+'"? Days it already wrote onto the calendar stay.')){
      S.sched.cols=tmplCols().filter(function(x){return x.id!==el.dataset.tcdel;});
      save();nav('schedule/templates');}
    return;}
  if(t.closest('#syncPill')){
    if(syncOn){syncFlush();syncPull();toast('Syncing');} else settingsModal(); return;}
  if(t.closest('#settings')){settingsModal();return;}
  }catch(err){ if(window.console&&console.error)console.error('click',err);
    toast('Something went wrong: '+(err.message||err)); }
});
function settingsModal(){
  var when=S.savedAt?new Date(S.savedAt).toLocaleString():'never';
  var size=0; try{size=(localStorage.getItem(KEY)||'').length;}catch(e){}
  var body=
   '<h4 class="lbl">Appearance</h4>'+
   '<div class="row" style="margin:10px 0 18px">'+
   ['dark','light','auto'].map(function(t){
     return '<button class="pill'+((S.theme||'dark')===t?' on':'')+'" data-theme="'+t+'">'+
     (t==='auto'?'Match device':t.charAt(0).toUpperCase()+t.slice(1))+'</button>';}).join('')+
   '</div><div class="hr"></div>'+
   '<h4 class="lbl">Your data</h4>'+
   '<p class="sm muted" style="margin:8px 0 14px">Everything lives in this browser on this device. '+
   'Nothing is uploaded. Save to a file to move it, back it up, or hand it over for changes.</p>'+
   '<div class="stats gap-b">'+
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
   '<button class="b o s" id="stFin">Budget CSV</button>'+
   '<button class="b o s" id="stPlan">Plans CSV</button></div>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Sync</h4>'+
   '<p class="sm muted" style="margin:8px 0 12px">'+
   (syncOn
     ? 'Shared with every device that knows the code. Changes push a moment after you '+
       'make them and pull when a device comes back to the front.'
     : 'Not syncing right now. Everything still saves on this device.')+
   (syncMsg?' <b>'+E(syncMsg)+'</b>':'')+'</p>'+
   '<div class="stats gap-b">'+
   '<div class="stat"><b>'+E({off:'Local',idle:'On',pull:'On',push:'On',
      offline:'Offline',error:'Error'}[syncState]||syncState)+'</b><span>State</span></div>'+
   '<div class="stat"><b>'+(S.__v||0)+'</b><span>Version</span></div>'+
   '<div class="stat"><b>'+E(syncAt?new Date(syncAt).toLocaleTimeString():'never')+'</b>'+
   '<span>Last synced</span></div></div>'+
   '<div class="row"><button class="b o" id="stSync">Sync now</button></div>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Lock</h4>'+
   '<p class="sm muted" style="margin:8px 0 12px">This device remembers the code so it does not '+
   'ask every time. Locking forgets it. Your data is not touched either way.</p>'+
   '<button class="b o" id="stLock">Lock this device</button>'+
   '<div class="hr"></div>'+
   '<h4 class="lbl">Danger</h4>'+
   '<p class="sm muted" style="margin:8px 0 12px">This wipes everything on this device. '+
   'Save a file first.</p>'+
   '<button class="b dz" id="stReset">Erase all data</button>';
  var m=modal('Settings',body,'<button class="b o" data-close>Close</button>');
  $$('[data-theme]',m).forEach(function(b){b.onclick=function(){
    S.theme=b.dataset.theme; save(); applyTheme();
    $$('[data-theme]',m).forEach(function(x){x.classList.remove('on');});
    b.classList.add('on'); chrome();};});
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
        (r.sched||[]).map(function(x){return WHO(x.who)+':'+x.what;}).join('; '),r.notes||'']);});
    dl('daily-log-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stShift',m).onclick=function(){
    var rows=[['Date','Who','Job','Hours','Gross','Net','Note']];
    S.fin.shifts.forEach(function(s){var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
      rows.push([s.date,j?WHO(j.who):'',j?j.name:'',s.hours,s.gross,s.net,s.note||'']);});
    dl('shifts-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stFin',m).onclick=function(){
    var rows=[['Type','Section','Name','Who','Low','Realistic','High','Actual']];
    S.fin.jobs.forEach(function(j){rows.push(['Income','',j.name,WHO(j.who),j.low,j.real,j.high,j.actual||'']);});
    S.fin.costs.forEach(function(c){rows.push(['Cost',c.section,c.name,WHO(c.who),c.low,c.real,c.high,c.actual||'']);});
    dl('budget-'+today()+'.csv',toCSV(rows),'text/csv');};
  $('#stPlan',m).onclick=function(){
    var rows=[['Plan','Section','Item','Done','Note']];
    planCols().forEach(function(c){(c.subs||[]).forEach(function(s){
      (s.items||[]).forEach(function(i){
        rows.push([c.name,s.name,i.text,i.done?'yes':'',i.note||'']);});});});
    dl('plans-'+today()+'.csv',toCSV(rows),'text/csv');};
  var sy=$('#stSync',m); if(sy) sy.onclick=function(){
    if(!syncOn){toast('Sync is not available on this host');return;}
    syncFlush(); syncPull(); toast('Syncing');};
  $('#stLock',m).onclick=function(){
    if(confirm('Ask for the code again next time this device opens the Handbook?')) lock();};
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
    ' style="width:18px;height:18px;accent-color:var(--brass)"><div><b>'+E(n)+'</b>'+
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

try{ applyTheme(); }catch(e){}
try{ chrome(); }catch(e){ if(window.console)console.error('chrome',e); }
if(!location.hash)location.hash='#/meals';
route();
/* Take a baseline of every branch before anything can change, so the first
   save does not stamp the whole document as freshly edited. */
try{ syncTouch(); }catch(e){}
try{ if(SEED.__token) syncInit(SEED.__token); else syncSet('off','No sync token in this build.'); }
catch(e){ if(window.console)console.error('sync',e); }
window.onerror=function(msg,src,ln,col,err){
  var v=$('#view');
  if(v&&!v.innerHTML){ v.innerHTML=errPanel('The app',err||{message:msg}); }
  return false;
};
"""
