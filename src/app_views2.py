# -*- coding: utf-8 -*-
APP_VIEWS2 = r"""
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
  if(sub==='strategies') return vStrategies();
  if(sub==='actual') return vActual();
  var mode=S.fin.costMode||'real', path=S.fin.path||'rent';
  var inc=finIncome('both',mode), cost=finCost(mode,path), gap=inc-cost;
  var byS={}; S.fin.costs.forEach(function(c){
    if(c.section==='Housing (rent)'&&path==='buy')return;
    if(c.section==='Housing (buy)'&&path!=='buy')return;
    byS[c.section]=(byS[c.section]||0)+(c[mode]||0);});
  var pairs=scenAllFixed(), names=pairs.map(function(p){return p[0];});
  var act=S.fin.activeScenario, dirty=scenDirty();
  var cmp='';
  if(names.length){
    cmp='<div class="sec"><h2>Scenarios side by side</h2>'+
      '<p class="sub">Each one stores every income and cost line as it was when saved.</p>'+
      '<div class="tw"><table><thead><tr><th>Scenario</th><th>Basis</th><th>Housing</th>'+
      '<th class="num">Income</th><th class="num">Costs</th><th class="num">Monthly</th>'+
      '<th class="num">Yearly</th><th></th></tr></thead><tbody>'+
      pairs.map(function(pr){var n=pr[0],sc=pr[1];
        if(!sc||!sc.jobs||!sc.costs) return '';
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
   '<button class="b o s" data-nav="financial/strategies">Strategies</button>'+
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
   '<p>Places, houses, cars, anything worth comparing side by side before committing. '+
   'Every list here is yours to rename, edit or delete.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b" id="bpNew">New list</button>'+
   '<button class="b o" data-nav="financial">&larr; Financial</button></div>'+
   (names.length?names.map(function(n){var L=P_[n], its=L.items||[];
     var prices=its.map(function(i){return num(i.price);}).filter(function(x){return x>0;});
     var lo=prices.length?Math.min.apply(null,prices):0;
     var av=prices.length?prices.reduce(function(a,b){return a+b;},0)/prices.length:0;
     return '<div class="sec"><div class="spread"><h2>'+E(n)+
     (L.cat?' <span class="chip">'+E(L.cat)+'</span>':'')+'</h2>'+
     '<div class="row"><button class="b o s" data-bpadd="'+E(n)+'">Add item</button>'+
     '<button class="b o s" data-bple="'+E(n)+'">Edit list</button>'+
     '<button class="b o s dz" data-bpdel="'+E(n)+'">Delete</button></div></div>'+
     (L.note?'<p class="sub">'+E(L.note)+'</p>':'')+
     (prices.length>1?'<div class="stats" style="margin-bottom:14px">'+
       '<div class="stat"><b>'+its.length+'</b><span>Options</span></div>'+
       '<div class="stat acc"><b>'+M(lo)+'</b><span>Cheapest</span></div>'+
       '<div class="stat"><b>'+M(av)+'</b><span>Average</span></div></div>':'')+
     (its.length?'<div class="grid g3">'+its.map(function(it,i){
       var cheapest=prices.length>1&&num(it.price)===lo;
       return '<div class="card pad bpc'+(cheapest?' best':'')+'">'+
       '<div class="spread"><b class="bpn">'+E(it.name)+'</b>'+
       '<button class="x" data-bpi="'+E(n)+'|'+i+'" title="Remove">&times;</button></div>'+
       (cheapest?'<span class="chip t" style="margin-top:6px;display:inline-block">Cheapest</span>':'')+
       '<div class="bpp">'+M(it.price)+'</div>'+
       (it.fields?Object.keys(it.fields).map(function(k){
         return '<div class="spread sm bpf">'+
         '<span class="muted">'+E(k)+'</span><b>'+E(it.fields[k])+'</b></div>';}).join(''):'')+
       (it.notes?'<p class="sm muted" style="margin-top:10px">'+E(it.notes)+'</p>':'')+
       '<div class="row" style="margin-top:12px">'+
       '<button class="b o s" data-bpie="'+E(n)+'|'+i+'">Edit</button>'+
       (it.link?'<a class="b o s" href="'+E(it.link)+'" target="_blank" rel="noopener">Open link</a>':'')+
       '</div></div>';}).join('')+'</div>':'<div class="empty sm">Nothing on this list yet.</div>')+
     '</div>';}).join('')
    :'<div class="empty"><p>No lists yet.</p><p class="sm">Make one for apartments, or houses, '+
     'or anything you are comparing.</p></div>')+
   '</div>';
}

/* ---------------------------- STRATEGIES ----------------------------
   Ways to close the gap, grouped into lists you own. Same rules as every
   other list in the app: make them, rename them, delete them. */
function stratClass(st){
  var s=String(st||'').toUpperCase();
  if(s==='DEAD'||s==='BLOCKED'||s==='N/A'||s==='NEGLIGIBLE') return 'd3';
  if(s==='CRITICAL'||s==='LOCKED'||s==='KEY') return 'd2';
  if(s==='ACTIVE'||s==='READY'||s==='ON TRACK'||s==='STAGED'||s==='DONE') return 'd1';
  return '';
}
function stratDead(st){
  var s=String(st||'').toUpperCase();
  return s==='DEAD'||s==='N/A'||s==='NEGLIGIBLE'||s==='BLOCKED';
}
function stratTotal(list,mode){
  return (list.items||[]).reduce(function(a,x){
    return a+(stratDead(x.status)?0:num(x[mode]));},0);
}
function vStrategies(){
  var G=S.fin.strategies||{}, names=Object.keys(G);
  var mode=S.fin.stratMode||'real';
  var grand=names.reduce(function(a,n){return a+stratTotal(G[n],mode);},0);
  var live=names.reduce(function(a,n){return a+(G[n].items||[]).filter(function(x){
    return !stratDead(x.status);}).length;},0);
  var dead=names.reduce(function(a,n){return a+(G[n].items||[]).filter(function(x){
    return stratDead(x.status);}).length;},0);
  return '<div class="page"><div class="phead"><h1>Strategies</h1>'+
   '<p>Ways to close the gap, sorted by what they are worth against what they cost you. '+
   'Anything marked dead has been checked and is dead, so it does not get researched twice.</p></div>'+
   '<div class="row" style="margin-bottom:14px"><button class="b" id="stNew">New list</button>'+
   '<button class="b o" data-nav="financial">&larr; Financial</button>'+
   '<label class="f inline"><span>Column</span><select id="stMode">'+
   opt([['low','Lean (low)'],['real','Realistic'],['high','Good month (high)']],mode)+
   '</select></label></div>'+
   (names.length?'<div class="stats" style="margin-bottom:8px">'+
     '<div class="stat acc"><b>'+M(grand)+'</b><span>Swing / mo</span></div>'+
     '<div class="stat"><b>'+M(grand*12)+'</b><span>Per year</span></div>'+
     '<div class="stat"><b>'+live+'</b><span>Live moves</span></div>'+
     '<div class="stat"><b>'+dead+'</b><span>Ruled out</span></div></div>'+
     '<div class="note warn"><b>That total is a ceiling, not a plan.</b> It assumes every live '+
     'move runs at once, which is a 70 hour week. Pick three.</div>':'')+
   (names.length?names.map(function(n){
     var L=G[n], its=L.items||[], sub=stratTotal(L,mode);
     return '<div class="sec"><div class="spread"><h2>'+E(n)+'</h2>'+
     '<div class="row">'+(sub?'<span class="chip p">'+M(sub)+' / mo</span>':'')+
     '<button class="b o s" data-stadd="'+E(n)+'">Add</button>'+
     '<button class="b o s" data-stle="'+E(n)+'">Edit list</button>'+
     '<button class="b o s dz" data-stdel="'+E(n)+'">Delete</button></div></div>'+
     (L.note?'<p class="sub">'+E(L.note)+'</p>':'')+
     (its.length?its.map(function(it,i){
       var v=num(it[mode]);
       return '<details class="strat'+(stratDead(it.status)?' dead':'')+'"><summary>'+
       '<span class="stn">'+E(it.name)+'</span>'+
       '<span class="stmeta">'+
       (it.status?'<span class="chip '+stratClass(it.status)+'">'+E(it.status)+'</span>':'')+
       '<b class="stv'+(v<0?' neg':'')+'">'+(v?M(v)+'/mo':'&mdash;')+'</b></span></summary>'+
       '<div class="dc">'+
       '<div class="stgrid">'+
       '<div><span class="lbl">Low</span><b>'+M(it.low)+'</b></div>'+
       '<div><span class="lbl">Realistic</span><b>'+M(it.real)+'</b></div>'+
       '<div><span class="lbl">High</span><b>'+M(it.high)+'</b></div>'+
       (it.rate&&it.rate!=='n/a'?'<div><span class="lbl">Per hour</span><b>'+E(it.rate)+'</b></div>':'')+
       (it.effort?'<div><span class="lbl">Effort</span><b>'+E(it.effort)+'</b></div>':'')+
       (it.when?'<div><span class="lbl">When</span><b>'+E(it.when)+'</b></div>':'')+
       '</div>'+
       (it.how?'<p>'+E(it.how)+'</p>':'')+
       '<div class="row"><button class="b o s" data-stie="'+E(n)+'|'+i+'">Edit</button>'+
       '<button class="b o s dz" data-stid="'+E(n)+'|'+i+'">Delete</button></div>'+
       '</div></details>';}).join('')
      :'<div class="empty sm">Nothing on this list yet.</div>')+'</div>';}).join('')
    :'<div class="empty"><p>No strategy lists yet.</p>'+
     '<p class="sm">Make one for anything you are weighing: ways to earn more, bills to cut, '+
     'things to negotiate.</p></div>')+
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
    var items=rec?dayTimeline(ds):[];
    var show=items.slice(0,3).map(function(x){
      return '<span class="dev '+x.kind+'" title="'+E(x.title)+'">'+
        (x.t?'<b>'+E(x.t.slice(0,5))+'</b> ':'')+E(x.title)+'</span>';}).join('');
    var more=items.length>3?'<span class="dmore">+'+(items.length-3)+' more</span>':'';
    cells+='<div class="day'+(ds===today()?' today':'')+(ds===calSel?' sel':'')+'" data-d="'+ds+'">'+
      '<span class="dn">'+dn+'</span>'+
      (items.length?'<span class="devs">'+show+more+'</span>':'')+
      '</div>';}
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
/* ============================ PLANNING ============================
   General plans. A collection holds subsections, a subsection holds items.
   All three levels can be created, renamed and deleted. */
function planCols(){ return (S.plan&&S.plan.cols)||[]; }
function planCol(id){ var c=planCols().filter(function(x){return x.id===id;}); return c[0]||null; }
function planCount(c){
  var t=0,d=0;
  (c.subs||[]).forEach(function(s){(s.items||[]).forEach(function(i){t++; if(i.done)d++;});});
  return {total:t,done:d,pct:t?Math.round(d/t*100):0};
}
function vPlanning(sub){
  if(sub) return vPlanCol(sub);
  var cols=planCols();
  return '<div class="page"><div class="phead"><h1>Planning</h1>'+
   '<p>Plans that are not about money or food. Make a collection for anything, break it into '+
   'subsections, and tick things off as they happen.</p></div>'+
   '<div class="row" style="margin-bottom:16px"><button class="b" id="plNew">New collection</button></div>'+
   (cols.length?'<div class="grid g2">'+cols.map(function(c){
     var n=planCount(c);
     return '<button class="card pad plcard" data-plgo="'+c.id+'">'+
     '<div class="spread"><h3 class="pln">'+E(c.name)+'</h3>'+
     '<span class="chip p">'+n.done+' / '+n.total+'</span></div>'+
     (c.note?'<p class="sm muted" style="margin:8px 0 0">'+E(c.note)+'</p>':'')+
     '<div class="bar" style="margin-top:14px"><i class="pp" style="width:'+n.pct+'%"></i></div>'+
     '<div class="xs muted" style="margin-top:8px">'+
     (c.subs||[]).length+' section'+((c.subs||[]).length===1?'':'s')+
     (n.total?' &middot; '+n.pct+'% done':'')+'</div>'+
     '</button>';}).join('')+'</div>'
    :'<div class="empty"><p>No plans yet.</p><p class="sm">Start one for moving in, or a trip, '+
     'or anything with more than three steps.</p></div>')+
   '</div>';
}
function vPlanCol(id){
  var c=planCol(id);
  if(!c) return '<div class="page"><div class="empty"><p>That plan is gone.</p>'+
    '<button class="b o" data-nav="planning">Back to Planning</button></div></div>';
  var n=planCount(c);
  return '<div class="page"><div class="phead"><h1>'+E(c.name)+'</h1>'+
   (c.note?'<p>'+E(c.note)+'</p>':'')+'</div>'+
   '<div class="row" style="margin-bottom:14px">'+
   '<button class="b" data-plsadd="'+c.id+'">New section</button>'+
   '<button class="b o" data-ple="'+c.id+'">Rename</button>'+
   '<button class="b o dz" data-pld="'+c.id+'">Delete plan</button>'+
   '<button class="b o" data-nav="planning">&larr; All plans</button></div>'+
   (n.total?'<div class="stats" style="margin-bottom:18px">'+
     '<div class="stat acc"><b>'+n.pct+'%</b><span>Done</span></div>'+
     '<div class="stat"><b>'+n.done+'</b><span>Ticked off</span></div>'+
     '<div class="stat"><b>'+(n.total-n.done)+'</b><span>Left</span></div>'+
     '<div class="stat"><b>'+(c.subs||[]).length+'</b><span>Sections</span></div></div>':'')+
   ((c.subs||[]).length?(c.subs||[]).map(function(s){
     var si=s.items||[], sd=si.filter(function(i){return i.done;}).length;
     return '<div class="sec"><div class="spread"><h2>'+E(s.name)+'</h2>'+
     '<div class="row"><span class="chip p">'+sd+' / '+si.length+'</span>'+
     '<button class="b o s" data-pliadd="'+c.id+'|'+s.id+'">Add item</button>'+
     '<button class="b o s" data-plse="'+c.id+'|'+s.id+'">Edit</button>'+
     '<button class="b o s dz" data-plsd="'+c.id+'|'+s.id+'">Delete</button></div></div>'+
     (s.note?'<p class="sub">'+E(s.note)+'</p>':'')+
     (si.length?'<div class="card">'+si.map(function(i){
       return '<div class="pitem'+(i.done?' done':'')+'">'+
       '<input type="checkbox" data-plck="'+c.id+'|'+s.id+'|'+i.id+'"'+(i.done?' checked':'')+'>'+
       '<div class="pbody"><div class="pt">'+E(i.text)+'</div>'+
       (i.note?'<div class="pn">'+E(i.note)+'</div>':'')+'</div>'+
       '<button class="b o s" data-plie="'+c.id+'|'+s.id+'|'+i.id+'">Edit</button>'+
       '<button class="x" data-plid="'+c.id+'|'+s.id+'|'+i.id+'">&times;</button>'+
       '</div>';}).join('')+'</div>'
      :'<div class="empty sm">Nothing in this section yet.</div>')+'</div>';}).join('')
    :'<div class="empty"><p>No sections yet.</p>'+
     '<p class="sm">Break the plan into parts, then put the actual to-dos inside them.</p></div>')+
   '</div>';
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
"""
