# -*- coding: utf-8 -*-
APP_WIRE = r"""
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
function route(){
  var h=(location.hash||'#/meals').slice(2).split('/'), v=h[0]||'meals', sub=h[1]||'';
  var m=$('#view'); if(!m) return;
  var html;
  try{
    html = v==='r'?vRecipe(sub) : v==='training'?vTraining(sub) : v==='shopping'?vShopping(sub)
      : v==='financial'?vFinancial(sub) : v==='schedule'?vSchedule(sub) : vMeals();
  }catch(e){ html=errPanel(v.charAt(0).toUpperCase()+v.slice(1),e);
    if(window.console&&console.error)console.error(e); }
  m.innerHTML=html;
  try{window.scrollTo(0,0);}catch(e){}
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
    save();toast('Logged to today for '+ME());return;}
  if((el=t.closest('[data-groc]'))){addRecipeToShop(byId(el.dataset.groc));
    toast('Added to '+S.shop.active);return;}
  if((el=t.closest('[data-tolist]'))){listModal(el.dataset.tolist);return;}
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
  if((el=t.closest('[data-bpadd]'))){bpItemEditor(el.dataset.bpadd);return;}
  if((el=t.closest('[data-bpdel]'))){if(confirm('Delete list?')){
    delete S.fin.purchases[el.dataset.bpdel];save();route();}return;}
  if((el=t.closest('[data-bpi]'))){var p=el.dataset.bpi.split('|');
    S.fin.purchases[p[0]].items.splice(+p[1],1);save();route();return;}
  if((el=t.closest('[data-d]'))){calSel=el.dataset.d;route();return;}
  if((el=t.closest('[data-evd]'))){dayLog(calSel).sched.splice(+el.dataset.evd,1);save();route();return;}
  if((el=t.closest('[data-spd]'))){dayLog(calSel).spend.splice(+el.dataset.spd,1);save();route();return;}
  if((el=t.closest('[data-mld]'))){dayLog(calSel).meals.splice(+el.dataset.mld,1);save();route();return;}
  if((el=t.closest('[data-tadd]'))){tmplEditor(+el.dataset.tadd);return;}
  if((el=t.closest('[data-td]'))){var q=el.dataset.td.split('|');
    S.sched.tmpl[q[0]].splice(+q[1],1);save();route();return;}
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

try{ applyTheme(); }catch(e){}
try{ chrome(); }catch(e){ if(window.console)console.error('chrome',e); }
if(!location.hash)location.hash='#/meals';
route();
window.onerror=function(msg,src,ln,col,err){
  var v=$('#view');
  if(v&&!v.innerHTML){ v.innerHTML=errPanel('The app',err||{message:msg}); }
  return false;
};
"""
