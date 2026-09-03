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
   '<div class="card pad"><h3 class="ctitle">Today</h3>'+
   '<label class="f"><span>Session</span><select id="tWorkout">'+
   Object.keys(TRAIN).map(function(k){return '<option value="'+k+'"'+(d.workout===k?' selected':'')+'>'+TRAIN[k].n+'</option>';}).join('')+
   '</select></label>'+
   '<label class="f"><span>Notes, lifts, PRs</span><textarea id="tNotes" rows="3" placeholder="Weighted pull-up 3x5 +25 lb">'+E(d.notes||'')+'</textarea></label>'+
   '<label class="f"><span>Bodyweight this morning</span><input id="tW" type="number" step="0.1" value="'+(d.w||'')+'"></label>'+
   '<button class="b" id="tSave">Save</button>'+
   '<p class="xs muted" style="margin-top:10px">Logged as <b>'+E(MENAME())+'</b>. This appears on the schedule automatically.</p></div>'+
   '<div class="card pad"><h3 class="ctitle">What the day needs</h3>'+
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
   '<div class="card pad gap-b"><div class="fr">'+
   '<label class="f"><span>Search</span><input id="exq" placeholder="pull-up, planche..." value="'+E(exFlt.q)+'"></label>'+
   '<label class="f"><span>Muscle group</span><select id="exmg">'+
   opt([['','All']].concat(mgs.map(function(m){return [m,m];})),exFlt.mg)+'</select></label>'+
   '<label class="f"><span>Equipment</span><select id="exeq">'+
   opt([['','Anything'],['Bodyweight','Bodyweight'],['Dumbbell','Dumbbells'],['Pull-up','Pull-up bar'],
        ['Dip','Dip station'],['Parallettes','Parallettes'],['vest','Weighted vest'],
        ['Band','Bands'],['Rings','Rings']],exFlt.eq)+'</select></label></div>'+
   '<div class="row"><button class="pill'+(exFlt.hero?' on':'')+'" id="exhero">Hero lifts only</button>'+
   '<span class="right sm muted" id="excount"></span></div></div>'+
   '<div id="exList"></div><button class="b o" style="margin-top:20px" data-nav="training">&larr; Training</button></div>';
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

/* ============================ FINANCIAL ============================
   Every income line and every cost line carries an `off` flag. Off is not
   deleted: the row stays, keeps its numbers, and stops counting. That is the
   whole point — the question "what if we dropped the gym and Aaliyah's tuition
   came out" is answered by two switches and a redraw, and switching them back
   costs nothing. A line with no flag at all is on, so every scenario saved
   before this existed still reads correctly.

   Anything that totals money goes through finIncome/finCost so there is one
   place where off is honoured and the charts can never disagree with the
   tables. */
function finLive(x){return !x.off;}
function costInPath(c,path){
  if(c.section==='Housing (rent)') return path!=='buy';
  if(c.section==='Housing (buy)') return path==='buy';
  return true;
}
/* all=true counts the switched-off lines too, which is how the page can say
   what you have parked without un-parking it. */
function finIncome(who,mode,all){
  return S.fin.jobs.filter(function(j){
    if(!all&&!finLive(j)) return false;
    return who==='both'||j.who===who||j.who==='Both';})
    .reduce(function(a,j){return a+(j[mode]||0);},0);
}
function finCost(mode,path,all){
  return S.fin.costs.filter(function(c){
    if(!all&&!finLive(c)) return false;
    return costInPath(c,path);}).reduce(function(a,c){return a+(c[mode]||0);},0);
}
/* Totals for a saved snapshot, which has its own jobs, costs, mode and path. */
function scenTotals(sc){
  var si=(sc.jobs||[]).filter(finLive).reduce(function(a,j){return a+(j[sc.mode]||0);},0);
  var sc_=(sc.costs||[]).filter(function(c){return finLive(c)&&costInPath(c,sc.path);})
    .reduce(function(a,c){return a+(c[sc.mode]||0);},0);
  return {inc:si,cost:sc_,gap:si-sc_};
}
function shiftsFor(who,from){
  return S.fin.shifts.filter(function(s){
    var j=S.fin.jobs.filter(function(x){return x.id===s.jobId;})[0];
    if(who&&j&&j.who!==who&&j.who!=='Both')return false;
    if(from&&s.date<from)return false; return true;});
}
/* What actually lands per dollar earned, measured rather than assumed. Falls
   back to 80% only when there is nothing logged to measure. */
function takeHomeRate(){
  var g=0,n=0;
  S.fin.shifts.forEach(function(s){g+=(s.gross||0);n+=(s.net||0);});
  return (g>0&&n>0)?n/g:0.8;
}
function bestLiveRate(){
  var r=0;
  S.fin.jobs.forEach(function(j){if(finLive(j)&&j.rate>r)r=j.rate;});
  return r;
}
var FINMODES=[['low','Lean'],['real','Realistic'],['high','Good month'],['actual','Actual']];
function modeLabel(m){
  for(var i=0;i<FINMODES.length;i++) if(FINMODES[i][0]===m) return FINMODES[i][1];
  return m;
}
/* The switch itself. One markup shape for line rows, section rows and person
   rows, so all three behave the same and there is one CSS rule for it. */
function finSw(attr,val,on,label,small){
  return '<button type="button" class="sw'+(small?' xs':'')+(on?' on':'')+'" '+
    'data-'+attr+'="'+E(val)+'" aria-pressed="'+(on?'true':'false')+'" '+
    'title="'+E((on?'Counted — click to switch off: ':'Switched off — click to count: ')+label)+'">'+
    '<i></i></button>';
}
function vFinancial(sub){
  if(sub==='purchases') return vPurchases();
  if(sub==='strategies') return vStrategies();
  if(sub==='actual') return vActual();
  var mode=S.fin.costMode||'real', path=S.fin.path||'rent';
  var inc=finIncome('both',mode), cost=finCost(mode,path), gap=inc-cost;

  /* ---- what is parked ---- */
  var offJobs=S.fin.jobs.filter(function(j){return !finLive(j);});
  var offCosts=S.fin.costs.filter(function(c){return !finLive(c)&&costInPath(c,path);});
  var offInc=finIncome('both',mode,true)-inc;
  var offCost=finCost(mode,path,true)-cost;

  /* ---- costs by section, live and parked separately ---- */
  var byS={}, bySAll={};
  S.fin.costs.forEach(function(c){
    if(!costInPath(c,path)) return;
    bySAll[c.section]=(bySAll[c.section]||0)+(c[mode]||0);
    if(finLive(c)) byS[c.section]=(byS[c.section]||0)+(c[mode]||0);
    else if(!(c.section in byS)) byS[c.section]=0;
  });
  var secNames=Object.keys(byS).sort(function(a,b){return (bySAll[b]||0)-(bySAll[a]||0);});

  /* ---- derived numbers ---- */
  var saveRate=inc>0?gap/inc*100:0;
  var toSavings=byS['Savings']||0;               /* money into savings is not spent */
  var toDebt=byS['Debt']||0;
  var building=gap+toSavings;                    /* what the month actually adds */
  var burn=cost-toSavings;                       /* what leaving the house costs */
  var rate=bestLiveRate(), th=takeHomeRate();
  var hoursToClose=(gap<0&&rate>0)?(-gap)/(rate*th):0;
  var perDollar=inc>0?secNames.map(function(k){return [k,byS[k]/inc*100];}):[];

  /* ---- headline ---- */
  var stats='<div class="stats">'+
   '<div class="stat"><b data-cv="'+inc+'">'+M(inc)+'</b><span>Income / mo</span></div>'+
   '<div class="stat"><b data-cv="'+cost+'">'+M(cost)+'</b><span>Costs / mo</span></div>'+
   '<div class="stat '+(gap>=0?'good':'bad')+'"><b data-cv="'+gap+'">'+M(gap)+'</b><span>'+
   (gap>=0?'Surplus':'Shortfall')+'</span></div>'+
   '<div class="stat"><b data-cv="'+(gap*12)+'">'+M(gap*12)+'</b><span>Per year</span></div>'+
   '<div class="stat"><b data-cv="'+saveRate+'" data-cf="pct">'+Math.round(saveRate)+'%</b>'+
   '<span>Kept of income</span></div></div>';

  var verdict='';
  if(gap<0){
    verdict='<div class="note warn"><b>The gap is real.</b> At these numbers we are '+M(-gap)+
      ' short every month'+
      (hoursToClose>0?', which is <b>'+(Math.round(hoursToClose*10)/10)+' more hours a month</b> at '+
        $$$(rate)+'/hr once '+Math.round((1-th)*100)+'% comes off for tax':'')+
      '. Income has to rise by that, or costs have to fall.</div>';
  } else if(inc>0){
    verdict='<div class="note good"><b>'+M(gap)+' clear a month.</b> That is '+
      Math.round(saveRate)+'% of everything coming in, '+M(gap*12)+' over a year'+
      (toSavings>0?', on top of the '+M(toSavings)+' a month already going into savings as a cost line':'')+
      '.</div>';
  }

  var parked='';
  if(offJobs.length||offCosts.length){
    parked='<div class="note"><b>Switched off.</b> '+
      (offJobs.length?offJobs.length+' income line'+(offJobs.length>1?'s':'')+' worth '+M(offInc)+' / mo':'')+
      (offJobs.length&&offCosts.length?' and ':'')+
      (offCosts.length?offCosts.length+' cost line'+(offCosts.length>1?'s':'')+' worth '+M(offCost)+' / mo':'')+
      ' are sitting out of these totals. Switching every one back on would put the month at <b>'+
      M(gap+offInc-offCost)+'</b>.</div>';
  }

  /* ---- waterfall: income, then each section, then what is left ---- */
  /* Three colours, three meanings: what arrives, what is taken off, what
     survives. Giving each section its own colour here made six deductions look
     like six unrelated things instead of one balance being cut down; the donut
     below is where the sections get their identity. */
  var wfMax=Math.max(inc,cost,1), run=inc;
  var wfCols=[{label:'Income',sub:M(inc),subCls:'good',
    bars:[{v:inc,base:0,cls:'ctg',tip:'Everything coming in: '+M(inc)}]}];
  secNames.forEach(function(k,i){
    var v=byS[k]; if(v<=0) return;
    var base=Math.max(0,run-v);
    wfCols.push({label:k,sub:'−'+M(v),subCls:'bad',
      bars:[{v:v,base:base,cls:'ctb',
        tip:k+': '+M(v)+' off, leaving '+M(base)}]});
    run-=v;
  });
  wfCols.push({label:gap>=0?'Left over':'Short by',sub:M(Math.abs(gap)),subCls:gap>=0?'good':'bad',
    bars:[{v:Math.abs(gap),base:0,cls:gap>=0?'ctg':'ctb',
      tip:(gap>=0?'Left over: ':'Short by: ')+M(Math.abs(gap))}]});
  var waterfall='<div class="sec"><h2>From income to what is left</h2>'+
    '<p class="sub">The first bar is everything coming in. Each one after it is a live cost '+
    'section taken off the running balance, biggest first, on the '+modeLabel(mode).toLowerCase()+
    ' column while '+(path==='buy'?'buying':'renting')+'. The last bar is what survives.</p>'+
    '<div class="card pad">'+chartCols({max:wfMax,h:180,cols:wfCols,connect:true})+
    '<div class="ckey"><span><i class="ctg"></i>Money in, and what is left of it</span>'+
    '<span><i class="ctb"></i>Taken off the balance</span>'+
    '<span class="muted">Each bar starts where the one before it ended</span></div>'+
    '</div></div>';

  /* ---- donut of live costs, with a switch per section in the legend ---- */
  var donutSlices=secNames.map(function(k,i){return {v:byS[k],label:k+' '+M(byS[k]),cls:chTone(i)};});
  var legend=chartLegend(secNames.map(function(k,i){
    var anyOn=S.fin.costs.some(function(c){return costInPath(c,path)&&c.section===k&&finLive(c);});
    return {label:k,cls:chTone(i),off:!anyOn,
      value:M(anyOn?byS[k]:bySAll[k]),
      pct:(cost&&anyOn)?Math.round(byS[k]/cost*100)+'%':'—',
      ctrl:finSw('secttog',k,anyOn,k,true)};
  }));
  var incomePeople=['Jaron','Aaliyah','Both'].filter(function(w){
    return S.fin.jobs.some(function(j){return j.who===w;});});
  var incLegend=chartLegend(incomePeople.map(function(w,i){
    var v=S.fin.jobs.filter(function(j){return j.who===w&&finLive(j);})
      .reduce(function(a,j){return a+(j[mode]||0);},0);
    var all=S.fin.jobs.filter(function(j){return j.who===w;})
      .reduce(function(a,j){return a+(j[mode]||0);},0);
    var anyOn=S.fin.jobs.some(function(j){return j.who===w&&finLive(j);});
    return {label:w==='Both'?'Shared / gig':WHO(w),cls:chTone(i+1),off:!anyOn,
      value:M(anyOn?v:all),pct:(inc&&anyOn)?Math.round(v/inc*100)+'%':'—',
      ctrl:finSw('whotog',w,anyOn,w==='Both'?'shared income':WHO(w),true)};
  }));
  var costPeople=['Jaron','Aaliyah','Both'].filter(function(w){
    return S.fin.costs.some(function(c){return c.who===w&&costInPath(c,path);});});
  var whoCost='<div class="ckey">'+costPeople.map(function(w,i){
    var v=S.fin.costs.filter(function(c){return c.who===w&&finLive(c)&&costInPath(c,path);})
      .reduce(function(a,c){return a+(c[mode]||0);},0);
    return '<span><i class="'+chTone(i+3)+'"></i>'+E(w==='Both'?'Shared':WHO(w))+' '+M(v)+'</span>';
  }).join('')+'</div>';

  var split='<div class="sec"><h2>Where the money goes</h2>'+
   '<p class="sub">Every switch here moves a whole group at once. The tables further down do it one '+
   'line at a time.</p><div class="grid g2">'+
   '<div class="card pad"><h3 class="ctitle">Costs by section</h3>'+
   chartDonut(donutSlices,M(cost),'Live costs / mo')+legend+
   (perDollar.length?'<p class="sm muted" style="margin-top:14px">Of every $100 coming in, '+
     perDollar.slice(0,3).map(function(p){return '$'+Math.round(p[1])+' goes to '+E(p[0].toLowerCase());}).join(', ')+
     '.</p>':'')+'</div>'+
   '<div class="card pad"><h3 class="ctitle">Income by person</h3>'+
   chartDonut(incomePeople.map(function(w,i){
     return {v:S.fin.jobs.filter(function(j){return j.who===w&&finLive(j);})
       .reduce(function(a,j){return a+(j[mode]||0);},0),
       label:(w==='Both'?'Shared':WHO(w)),cls:chTone(i+1)};}),M(inc),'Live income / mo')+
   incLegend+
   '<h3 class="ctitle" style="margin-top:20px">Costs carried by</h3>'+whoCost+
   '<div class="row" style="margin-top:14px"><button class="b o s" id="jobAdd">Add income</button>'+
   '<button class="b o s" id="costAdd2">Add cost</button></div></div>'+
   '</div></div>';

  /* ---- the same month read four ways ---- */
  /* The actual column only earns a place when both sides of it are filled in.
     Most cost lines carry a researched figure and almost no income line does,
     so counting it early would draw a month with real rent and no wages and
     call it a forecast. */
  var actReady=finIncome('both','actual')>0&&finCost('actual',path)>0;
  var bandModes=FINMODES.filter(function(m){return m[0]!=='actual'||actReady;});
  var bandVals=bandModes.map(function(m){
    var i2=finIncome('both',m[0]), c2=finCost(m[0],path);
    return {m:m[0],label:m[1],inc:i2,cost:c2,gap:i2-c2};});
  var bandMax=Math.max.apply(null,bandVals.map(function(b){return Math.max(b.inc,b.cost);}).concat([1]));
  var best=bandVals.slice().sort(function(a,b){return b.gap-a.gap;})[0];
  var worst=bandVals.slice().sort(function(a,b){return a.gap-b.gap;})[0];
  var band='<div class="sec"><h2>The same month, read '+
   (['','one way','two ways','three ways','four ways'][bandVals.length]||'every way')+'</h2>'+
   '<p class="sub">Identical lines, identical switches — only the estimate column changes. '+
   'The spread between the ends is what the plan actually rests on.</p>'+
   '<div class="card pad">'+
   chartCols({max:bandMax,h:160,cols:bandVals.map(function(b){
     return {label:b.label,sub:M(b.gap),subCls:b.gap>=0?'good':'bad',
       bars:[{v:b.inc,cls:'ct2',tip:'Income '+M(b.inc)},{v:b.cost,cls:'ct5',tip:'Costs '+M(b.cost)}]};})})+
   '<div class="ckey"><span><i class="ct2"></i>Income</span><span><i class="ct5"></i>Costs</span>'+
   '<span class="muted">Number under each column is that month\'s surplus</span></div>'+
   (bandVals.length>1?'<p class="sm muted" style="margin-top:12px">Best case '+
     M(best.gap)+' a month on '+E(best.label.toLowerCase())+', worst '+M(worst.gap)+' on '+
     E(worst.label.toLowerCase())+'. A '+M(best.gap-worst.gap)+' swing, '+
     M((best.gap-worst.gap)*12)+' over a year.'+
     (actReady?'':' The actual column is not drawn yet: it needs a researched figure on the '+
       'income side as well as the cost side.')+'</p>':'')+
   '</div></div>';

  /* ---- twelve months of the current month, repeated ---- */
  var proj=[],pv=0,pi;
  for(pi=1;pi<=12;pi++){pv+=gap;proj.push(pv);}
  var projection=(inc>0||cost>0)?'<div class="sec"><h2>Twelve months at this rate</h2>'+
   '<p class="sub">Nothing clever: this month repeated twelve times, so the shape is what the '+
   'current numbers compound to if neither side moves.</p>'+
   '<div class="card pad">'+chartLine(proj,{neg:gap<0,label:'Cumulative surplus over twelve months'})+
   '<div class="caxis"><span>Month 1</span><span>Month 6</span><span>Month 12</span></div>'+
   '<div class="stats" style="margin-top:16px">'+
   '<div class="stat '+(gap>=0?'good':'bad')+'"><b data-cv="'+(gap*3)+'">'+M(gap*3)+'</b><span>After 3 months</span></div>'+
   '<div class="stat '+(gap>=0?'good':'bad')+'"><b data-cv="'+(gap*6)+'">'+M(gap*6)+'</b><span>After 6 months</span></div>'+
   '<div class="stat '+(gap>=0?'good':'bad')+'"><b data-cv="'+(gap*12)+'">'+M(gap*12)+'</b><span>After a year</span></div>'+
   '<div class="stat"><b data-cv="'+building+'">'+M(building)+'</b><span>Built / mo</span></div>'+
   '<div class="stat"><b data-cv="'+burn+'">'+M(burn)+'</b><span>Spent / mo</span></div></div>'+
   '<p class="sm muted" style="margin-top:12px">Built counts the surplus plus the '+M(toSavings)+
   ' a month sitting in the Savings section, because money moved into savings was never spent. '+
   'Spent is everything else'+(toDebt>0?', including '+M(toDebt)+' a month servicing debt':'')+'.</p>'+
   '</div></div>':'';

  /* ---- saved scenarios ---- */
  var pairs=scenAllFixed(), names=pairs.map(function(p){return p[0];});
  var act=S.fin.activeScenario, dirty=scenDirty();
  var cmp='';
  if(names.length){
    var scRows=pairs.map(function(pr){var n=pr[0],sc=pr[1];
      if(!sc||!sc.jobs||!sc.costs) return null;
      var t=scenTotals(sc);
      var offN=(sc.jobs.filter(function(j){return !finLive(j);}).length)+
               (sc.costs.filter(function(c){return !finLive(c);}).length);
      return {n:n,sc:sc,t:t,off:offN};}).filter(Boolean);
    var scMax=Math.max.apply(null,scRows.map(function(r){
      return Math.max(r.t.inc,r.t.cost);}).concat([Math.max(inc,cost),1]));
    cmp='<div class="sec"><h2>Scenarios side by side</h2>'+
      '<p class="sub">Each one stores every income and cost line, and which of them were switched '+
      'on, exactly as they were when saved.</p>'+
      '<div class="card pad gap-b">'+chartCols({max:scMax,h:150,cols:
        [{label:'Now'+(act?' ('+act+')':''),sub:M(gap),subCls:gap>=0?'good':'bad',
          bars:[{v:inc,cls:'ct2',tip:'Income '+M(inc)},{v:cost,cls:'ct5',tip:'Costs '+M(cost)}]}]
        .concat(scRows.map(function(r){
          return {label:r.n,sub:M(r.t.gap),subCls:r.t.gap>=0?'good':'bad',
            bars:[{v:r.t.inc,cls:'ct2',tip:'Income '+M(r.t.inc)},
                  {v:r.t.cost,cls:'ct5',tip:'Costs '+M(r.t.cost)}]};}))})+
      '<div class="ckey"><span><i class="ct2"></i>Income</span><span><i class="ct5"></i>Costs</span>'+
      '<span class="muted">Number under each column is the surplus</span></div></div>'+
      '<div class="tw"><table><thead><tr><th>Scenario</th><th>Basis</th><th>Housing</th>'+
      '<th class="num">Income</th><th class="num">Costs</th><th class="num">Monthly</th>'+
      '<th class="num">Yearly</th><th class="num">Off</th><th></th></tr></thead><tbody>'+
      scRows.map(function(r){
        return '<tr'+(r.n===act?' style="background:var(--panel-2)"':'')+'>'+
        '<td><b>'+E(r.n)+'</b>'+(r.n===act?' <span class="chip t">open</span>':'')+'</td>'+
        '<td class="sm muted">'+E(modeLabel(r.sc.mode))+'</td><td class="sm muted">'+E(r.sc.path)+'</td>'+
        '<td class="num">'+M(r.t.inc)+'</td><td class="num">'+M(r.t.cost)+'</td>'+
        '<td class="num" style="color:'+(r.t.gap>=0?'var(--sage)':'var(--clay)')+'"><b>'+M(r.t.gap)+'</b></td>'+
        '<td class="num">'+M(r.t.gap*12)+'</td>'+
        '<td class="num sm muted">'+(r.off||'—')+'</td>'+
        '<td><button class="b o s" data-scload="'+E(r.n)+'">Open</button> '+
        '<button class="x" data-scdel="'+E(r.n)+'">&times;</button></td></tr>';}).join('')+
      '</tbody></table></div></div>';
  }

  /* ---- the lines themselves ---- */
  var jobsOn=S.fin.jobs.filter(finLive).length;
  var costsOn=S.fin.costs.filter(function(c){return finLive(c)&&costInPath(c,path);}).length;
  var costsInPath=S.fin.costs.filter(function(c){return costInPath(c,path);}).length;

  var incTable='<div class="sec"><div class="spread"><h2>Income lines</h2>'+
   '<div class="row"><span class="chip p">'+jobsOn+' of '+S.fin.jobs.length+' on</span>'+
   '<button class="b o s" data-alltog="jobs|1">All on</button>'+
   '<button class="b o s" data-alltog="jobs|0">All off</button>'+
   '<button class="b o s" id="jobAdd2">Add</button></div></div><div class="tw wide"><table>'+
   '<thead><tr><th>On</th><th>Who</th><th>Name</th><th>Employer</th><th class="num">Low</th>'+
   '<th class="num">Realistic</th><th class="num">High</th><th class="num">Actual</th><th></th></tr></thead><tbody>'+
   (S.fin.jobs.length?S.fin.jobs.map(function(j){
     var on=finLive(j);
     return '<tr'+(on?'':' class="offrow"')+'>'+
     '<td>'+finSw('jobtog',j.id,on,j.name||'this income line')+'</td>'+
     '<td><span class="chip">'+E(WHO(j.who))+'</span></td><td><b>'+E(j.name)+'</b>'+
     (on?'':'<span class="offtag">off</span>')+
     (j.rate?'<div class="xs muted">'+$$$(j.rate)+'/hr</div>':'')+'</td>'+
     '<td class="sm muted">'+E(j.employer||'')+'</td>'+
     '<td class="num">'+M(j.low)+'</td><td class="num"><b>'+M(j.real)+'</b></td>'+
     '<td class="num">'+M(j.high)+'</td>'+
     '<td class="num">'+(j.actual?M(j.actual):'<span class="muted">-</span>')+'</td>'+
     '<td><button class="b o s" data-jobe="'+j.id+'">Edit</button></td></tr>';}).join('')
    :'<tr><td colspan="9" class="sm muted" style="text-align:center;padding:22px">No income lines yet.</td></tr>')+
   '<tr style="background:var(--panel-2)"><td colspan="4"><b>Counted total</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','low'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','real'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','high'))+'</b></td>'+
   '<td class="num"><b>'+M(finIncome('both','actual'))+'</b></td><td></td></tr>'+
   (offJobs.length?'<tr><td colspan="4" class="sm muted">Switched off</td>'+
     '<td class="num sm muted">'+M(finIncome('both','low',true)-finIncome('both','low'))+'</td>'+
     '<td class="num sm muted">'+M(finIncome('both','real',true)-finIncome('both','real'))+'</td>'+
     '<td class="num sm muted">'+M(finIncome('both','high',true)-finIncome('both','high'))+'</td>'+
     '<td class="num sm muted">'+M(finIncome('both','actual',true)-finIncome('both','actual'))+'</td>'+
     '<td></td></tr>':'')+
   '</tbody></table></div></div>';

  var costTable='<div class="sec"><div class="spread"><h2>Cost lines</h2>'+
   '<div class="row"><span class="chip p">'+costsOn+' of '+costsInPath+' on</span>'+
   '<button class="b o s" data-alltog="costs|1">All on</button>'+
   '<button class="b o s" data-alltog="costs|0">All off</button>'+
   '<button class="b o s" id="costAdd">Add</button></div></div><div class="tw wide"><table>'+
   '<thead><tr><th>On</th><th>Section</th><th>Cost</th><th>Who</th><th class="num">Low</th>'+
   '<th class="num">Realistic</th><th class="num">High</th><th class="num">Actual</th><th></th></tr></thead><tbody>'+
   (S.fin.costs.length?S.fin.costs.map(function(c){
     var on=finLive(c), inPath=costInPath(c,path);
     return '<tr'+(on&&inPath?'':' class="offrow"')+'>'+
     '<td>'+finSw('costtog',c.id,on,c.name||'this cost line')+'</td>'+
     '<td class="sm muted">'+E(c.section)+'</td>'+
     '<td><b>'+E(c.name)+'</b>'+(on?(inPath?'':'<span class="offtag">other path</span>')
       :'<span class="offtag">off</span>')+'</td>'+
     '<td><span class="chip">'+E(WHO(c.who))+'</span></td>'+
     '<td class="num">'+M(c.low)+'</td><td class="num"><b>'+M(c.real)+'</b></td>'+
     '<td class="num">'+M(c.high)+'</td>'+
     '<td class="num">'+(c.actual?M(c.actual):'<span class="muted">-</span>')+'</td>'+
     '<td><button class="b o s" data-coste="'+c.id+'">Edit</button></td></tr>';}).join('')
    :'<tr><td colspan="9" class="sm muted" style="text-align:center;padding:22px">No cost lines yet.</td></tr>')+
   '<tr style="background:var(--panel-2)"><td colspan="4"><b>Counted total</b></td>'+
   '<td class="num"><b>'+M(finCost('low',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('real',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('high',path))+'</b></td>'+
   '<td class="num"><b>'+M(finCost('actual',path))+'</b></td><td></td></tr>'+
   (offCosts.length?'<tr><td colspan="4" class="sm muted">Switched off</td>'+
     '<td class="num sm muted">'+M(finCost('low',path,true)-finCost('low',path))+'</td>'+
     '<td class="num sm muted">'+M(finCost('real',path,true)-finCost('real',path))+'</td>'+
     '<td class="num sm muted">'+M(finCost('high',path,true)-finCost('high',path))+'</td>'+
     '<td class="num sm muted">'+M(finCost('actual',path,true)-finCost('actual',path))+'</td>'+
     '<td></td></tr>':'')+
   '</tbody></table></div></div>';

  return '<div class="page"><div class="phead"><h1>Financial</h1>'+
   '<p>Every income and cost line, each one switchable, saved into scenarios you can compare. '+
   'Nothing overwrites a saved scenario until you press Save.</p></div>'+

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
     'Changes to income or cost lines — switches included — are live on screen but "'+E(act)+
     '" still holds the old figures. Save to keep them, or Revert to throw them away.</div>':'')+
   '</div>'+

   stats+verdict+parked+'</div>'+
   waterfall+split+band+projection+cmp+incTable+costTable+'</div>';
}
/* Six calendar months of logged shifts, oldest first, so the chart reads left
   to right the way a year does. A month with nothing logged stays in the list
   as a zero rather than being dropped, otherwise the gaps close up and a slow
   month looks like it never happened. */
function shiftMonths(n){
  var out=[],d=new Date(),i;
  d.setDate(1);
  for(i=n-1;i>=0;i--){
    var m=new Date(d.getFullYear(),d.getMonth()-i,1);
    var key=m.getFullYear()+'-'+p2(m.getMonth()+1);
    out.push({key:key,label:m.toLocaleDateString(undefined,{month:'short'}),
      net:0,gross:0,hours:0});
  }
  S.fin.shifts.forEach(function(s){
    var k=String(s.date||'').slice(0,7);
    for(var j=0;j<out.length;j++) if(out[j].key===k){
      out[j].net+=(s.net||0); out[j].gross+=(s.gross||0); out[j].hours+=(s.hours||0);}
  });
  return out;
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
  var mons=shiftMonths(6), plan=finIncome('both','real');
  var monMax=Math.max.apply(null,mons.map(function(m){return m.net;}).concat([plan,1]));
  var logged=mons.filter(function(m){return m.net>0;});
  var monAvg=logged.length?logged.reduce(function(a,m){return a+m.net;},0)/logged.length:0;
  var monBest=logged.length?Math.max.apply(null,logged.map(function(m){return m.net;})):0;
  var real=(jN+aN)/months, vsPlan=plan?real/plan*100:0;
  var costNow=finCost(S.fin.costMode||'real',S.fin.path||'rent');
  var realGap=real-costNow;
  return '<div class="page"><div class="phead"><h1>Actual earnings</h1>'+
   '<p>Log real shifts. Averages, effective hourly and after-tax rate all come from what actually landed, not the plan.</p></div>'+
   '<div class="row toolbar"><button class="b" id="shAdd">Log a shift</button>'+
   '<button class="b o" id="shCsv">Export shifts</button>'+
   '<button class="b o" data-nav="financial">&larr; Plan</button></div>'+
   '<div class="sec"><h2>Last 90 days</h2><div class="grid g2">'+
   ['Jaron','Aaliyah'].map(function(w){
     var h=w==='Jaron'?jH:aH,g=w==='Jaron'?jG:aG,n=w==='Jaron'?jN:aN;
     return '<div class="card pad"><h3 class="ctitle">'+E(WHO(w))+'</h3>'+
     '<div class="stats"><div class="stat acc"><b>'+M(n/months)+'</b><span>Net / mo</span></div>'+
     '<div class="stat"><b>'+h.toFixed(0)+'</b><span>Hours</span></div>'+
     '<div class="stat"><b>'+$$$(eff(g,h))+'</b><span>Gross / hr</span></div>'+
     '<div class="stat"><b>'+$$$(eff(n,h))+'</b><span>Net / hr</span></div></div>'+
     '<p class="sm muted" style="margin-top:10px">'+(g>0?'Take-home is '+Math.round(n/g*100)+'% of gross.':'No shifts logged yet.')+'</p>'+
     '</div>';}).join('')+'</div>'+
   /* With nothing logged there is no comparison to make, and drawing one
      anyway would put a -100% against the plan on the strength of no data. */
   (logged.length
     ?'<div class="note'+(vsPlan<90?' warn':(vsPlan>=100?' good':''))+'" style="margin-top:14px">'+
      '<b>Real against plan.</b> '+
      'Combined that is <b>'+M(real)+'</b> net a month from logged shifts, against a plan of <b>'+
      M(plan)+'</b>'+(plan?' — '+Math.round(vsPlan)+'% of it':'')+'. '+
      'Set against the '+M(costNow)+' of live costs, the months that actually happened leave <b>'+
      M(realGap)+'</b>. '+
      '<button class="b o s" id="scenFromActual" style="margin-left:8px">Save that as a scenario</button></div>'
     :'<div class="note" style="margin-top:14px"><b>Nothing logged yet.</b> '+
      'The plan says '+M(plan)+' a month against '+M(costNow)+' of live costs. Log a few shifts and '+
      'this page starts checking that against what actually landed.</div>')+'</div>'+

   '<div class="sec"><h2>Six months of real money</h2>'+
   '<p class="sub">Net, by calendar month, against the planned income line. Only the switched-on '+
   'income lines make up that plan, so parking a job on the Financial page moves the bar here too.</p>'+
   '<div class="card pad">'+
   (logged.length
     ?chartCols({max:monMax,h:160,cols:mons.map(function(m){
        return {label:m.label,sub:m.net?M(m.net):'—',
          bars:[{v:m.net,cls:m.net>=plan?'ct2':'ct1',
            tip:m.label+': '+M(m.net)+' net over '+Math.round(m.hours)+' hours'},
           {v:plan,cls:'ctm',tip:'Plan '+M(plan)}]};})})+
      '<div class="ckey"><span><i class="ct2"></i>Beat the plan</span>'+
      '<span><i class="ct1"></i>Under the plan</span><span><i class="ctm"></i>Plan</span></div>'+
      '<div class="stats" style="margin-top:16px">'+
      '<div class="stat"><b data-cv="'+monAvg+'">'+M(monAvg)+'</b><span>Avg logged month</span></div>'+
      '<div class="stat"><b data-cv="'+monBest+'">'+M(monBest)+'</b><span>Best month</span></div>'+
      '<div class="stat '+(monAvg>=plan?'good':'bad')+'"><b data-cv="'+(monAvg-plan)+'">'+
        M(monAvg-plan)+'</b><span>Against plan</span></div>'+
      '<div class="stat"><b data-cv="'+Math.round(takeHomeRate()*100)+'" data-cf="pct">'+
        Math.round(takeHomeRate()*100)+'%</b><span>Take home</span></div>'+
      '<div class="stat"><b data-cv="'+(jH+aH)+'" data-cf="h">'+(Math.round((jH+aH)*10)/10)+'h</b>'+
        '<span>Hours / 90 days</span></div></div>'
     :chEmpty('Nothing logged in the last six months. One shift is enough to start the chart.'))+
   '</div></div>'+
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
   '<div class="row toolbar"><button class="b" id="bpNew">New list</button>'+
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
     (prices.length>1?'<div class="stats gap-b">'+
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
   '<div class="row toolbar"><button class="b" id="stNew">New list</button>'+
   '<button class="b o" data-nav="financial">&larr; Financial</button>'+
   '<label class="f inline"><span>Column</span><select id="stMode">'+
   opt([['low','Lean (low)'],['real','Realistic'],['high','Good month (high)']],mode)+
   '</select></label></div>'+
   (names.length?'<div class="stats gap-b">'+
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
  /* Read-only on purpose: dayLog() would create an entry for every cell the
     calendar draws. Standing template items have to be visible on days that
     have nothing saved at all, so this must not write. */
  var d=S.days[ds]||{workout:'rest',meals:[],sched:[],spend:[]}, out=[];
  (d.sched||[]).forEach(function(e,i){
    out.push({t:e.from||'',kind:'e',who:e.who,title:e.what,
      sub:[range12(e.from,e.to),e.where||''].filter(Boolean).join('  \u00B7  '),
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
  /* Anything from a running template, worked out now rather than copied in. */
  tmplItemsFor(ds).forEach(function(x){
    out.push({t:x.from||'',kind:'e',who:x.who,title:x.what,
      sub:[range12(x.from,x.to),x.where||''].filter(Boolean).join('  ·  '),
      tmpl:x.col});});
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
    return '<li><div class="tm">'+(x.t?E(t12(x.t)):'&mdash;')+'</div>'+
    '<span class="pip '+x.kind+'"></span><div class="bd">'+
    '<div class="ti">'+E(x.title)+' <span class="chip">'+E(WHO(x.who)||'Both of us')+'</span>'+
    (x.tmpl?' <span class="chip t" title="From a running template">'+E(x.tmpl)+'</span>':'')+'</div>'+
    (x.sub?'<div class="ts">'+E(x.sub)+'</div>':'')+'</div>'+
    (x.rm!=null?'<button class="x" data-evd="'+x.rm+'">&times;</button>':'')+
    (x.mi!=null?'<button class="x" data-mld="'+x.mi+'">&times;</button>':'')+
    (x.si!=null?'<button class="x" data-spd="'+x.si+'">&times;</button>':'')+
    '</li>';}).join('')+'</ul>';
}
function vSchedule(sub){
  if(sub==='week'||sub==='templates'){
    var parts=(location.hash||'').slice(2).split('/');
    return parts[2]?vTemplateEdit(parts[2]):vWeekTemplate();
  }
  var first=new Date(calY,calM,1), start=first.getDay(), days=new Date(calY,calM+1,0).getDate();
  var cells='';
  for(var i=0;i<start;i++)cells+='<div class="day out"></div>';
  for(var dn=1;dn<=days;dn++){
    var ds=calY+'-'+p2(calM+1)+'-'+p2(dn);
    var items=dayTimeline(ds);
    var show=items.slice(0,3).map(function(x){
      return '<span class="dev '+x.kind+'" title="'+E(x.title)+'">'+
        (x.t?'<b>'+E(t12(x.t))+'</b> ':'')+E(x.title)+'</span>';}).join('');
    var more=items.length>3?'<span class="dmore">+'+(items.length-3)+' more</span>':'';
    /* On a narrow screen the cell is too small for text, so the same
       information is carried as one dot per kind of thing on that day. */
    var kinds={}, dots='';
    items.forEach(function(x){kinds[x.kind]=1;});
    ['e','w','m','s'].forEach(function(k){ if(kinds[k]) dots+='<i class="dot '+k+'"></i>'; });
    cells+='<div class="day'+(ds===today()?' today':'')+(ds===calSel?' sel':'')+'" data-d="'+ds+'"'+
      (items.length?' aria-label="'+E(shortD(ds)+', '+items.length+' item'+(items.length===1?'':'s'))+'"':'')+'>'+
      '<span class="dn">'+dn+'</span>'+
      (items.length?'<span class="devs">'+show+more+'</span><span class="dots">'+dots+'</span>':'')+
      '</div>';}
  var d=dayLog(calSel), t=dayTarget(S.who,d.workout), got=eaten(calSel);
  var spend=(d.spend||[]).reduce(function(a,x){return a+(x.amt||0);},0);
  return '<div class="page"><div class="phead"><h1>Schedule</h1>'+
   '<p>Everything either of us is doing that day, in time order. Training and meals appear here on '+
   'their own from the other tabs.</p></div>'+
   '<div class="row toolbar"><button class="b o" data-nav="schedule/templates">Templates</button>'+
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
   '<div class="card pad"><h3 class="ctitle">The day</h3>'+
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
  var fmt=t12m;
  return '<div class="note" style="margin-top:12px"><b>Both free.</b> '+
    blocks.filter(function(b){return b[1]-b[0]>=60;}).map(function(b){return fmt(b[0])+' to '+fmt(b[1]);}).join(', ')+'</div>';
}
function repeatLabel(c){
  var r=(REPEATS.filter(function(x){return x[0]===(c.repeat||'weekly');})[0]||REPEATS[0]);
  return r[1];
}
function vWeekTemplate(){
  var cols=tmplCols().slice().sort(function(a,b){
    if(!!b.fav!==!!a.fav) return b.fav?1:-1;
    return (a.name||'').localeCompare(b.name||'');});
  var live=cols.filter(function(c){return c.active;}).length;
  return '<div class="page"><div class="phead"><h1>Templates</h1>'+
   '<p>The parts of a week that repeat: work, class, church, gym. Build one once, then either '+
   'leave it running or push it onto a stretch of the calendar.</p></div>'+
   '<div class="row toolbar"><button class="b" id="tcNew">New template</button>'+
   '<button class="b o" data-nav="schedule">&larr; Calendar</button></div>'+
   (cols.length?'<div class="stats gap-b">'+
     '<div class="stat acc"><b>'+live+'</b><span>Running now</span></div>'+
     '<div class="stat"><b>'+cols.length+'</b><span>Templates</span></div>'+
     '<div class="stat"><b>'+cols.reduce(function(a,c){return a+tmplCount(c);},0)+'</b>'+
     '<span>Items</span></div></div>':'')+
   (cols.length?'<div class="grid g2">'+cols.map(function(c){
     var days=[];for(var i=0;i<7;i++) if(((c.days||{})[i]||[]).length) days.push(DOW[i]);
     return '<div class="card pad tcard'+(c.active?' live':'')+'">'+
     '<div class="spread"><h3 class="pln">'+
     (c.fav?'<span class="favstar on">\u2605</span> ':'')+E(c.name)+'</h3>'+
     '<span class="chip'+(c.active?' t':'')+'">'+(c.active?'Running':'Off')+'</span></div>'+
     (c.note?'<p class="sm muted" style="margin:8px 0 0">'+E(c.note)+'</p>':'')+
     '<div class="chips" style="margin-top:12px"><span class="chip">'+E(repeatLabel(c))+'</span>'+
     '<span class="chip">'+tmplCount(c)+' item'+(tmplCount(c)===1?'':'s')+'</span>'+
     (days.length?'<span class="chip">'+days.join(', ')+'</span>':'')+'</div>'+
     '<div class="row" style="margin-top:14px">'+
     '<button class="b o s" data-tcopen="'+c.id+'">Edit</button>'+
     '<button class="b o s" data-tcapply="'+c.id+'">Apply to&hellip;</button>'+
     '<button class="b o s" data-tctoggle="'+c.id+'">'+(c.active?'Stop':'Keep running')+'</button>'+
     '<button class="b o s" data-tcfav="'+c.id+'">'+(c.fav?'\u2605':'\u2606')+'</button>'+
     '</div></div>';}).join('')+'</div>'
    :'<div class="empty"><p>No templates yet.</p>'+
     '<p class="sm">Make one for the ordinary week, another for the weeks she has class, '+
     'whatever repeats.</p></div>')+
   '</div>';
}
function vTemplateEdit(id){
  var c=tmplCol(id);
  if(!c) return '<div class="page"><div class="empty"><p>That template is gone.</p>'+
    '<button class="b o" data-nav="schedule/templates">Back to templates</button></div></div>';
  return '<div class="page"><div class="phead"><h1>'+E(c.name)+'</h1>'+
   (c.note?'<p>'+E(c.note)+'</p>':'')+'</div>'+
   '<div class="row toolbar">'+
   '<button class="b" data-tcapply="'+c.id+'">Apply to&hellip;</button>'+
   '<button class="b o" data-tctoggle="'+c.id+'">'+(c.active?'Stop running':'Keep running')+'</button>'+
   '<button class="b o" data-tcedit="'+c.id+'">Settings</button>'+
   '<button class="b o dz" data-tcdel="'+c.id+'">Delete</button>'+
   '<button class="b o" data-nav="schedule/templates">&larr; Templates</button></div>'+
   '<div class="note'+(c.active?' good':'')+'">'+
   (c.active
     ? '<b>Running.</b> '+E(repeatLabel(c))+'. These show on the calendar on their own, and '+
       'stop showing the moment you turn this off. Nothing is copied into a day.'
     : '<b>Not running.</b> '+E(repeatLabel(c))+'. Use Apply to copy it onto real days, or '+
       'keep it running to have it appear on its own.')+'</div>'+
   '<div class="grid g3">'+DOW.map(function(dn,i){
     var items=((c.days||{})[i]||[]).slice().sort(function(a,b){
       return (a.from||'')<(b.from||'')?-1:1;});
     return '<div class="card pad"><div class="spread"><h3 class="ctitle" style="margin:0">'+dn+'</h3>'+
     '<button class="b o s" data-tadd="'+c.id+'|'+i+'">Add</button></div>'+
     (items.length?'<ul class="tl" style="margin-top:14px">'+items.map(function(x,j){
       return '<li><div class="tm">'+E(t12(x.from))+'</div><span class="pip e"></span>'+
       '<div class="bd"><div class="ti">'+E(x.what)+' <span class="chip">'+E(WHO(x.who))+'</span></div>'+
       '<div class="ts">'+E([range12(x.from,x.to),x.where||'']
         .filter(Boolean).join('  \u00B7  '))+'</div></div>'+
       '<button class="x" data-td="'+c.id+'|'+i+'|'+j+'">&times;</button></li>';}).join('')+'</ul>'
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
   '<div class="row toolbar"><button class="b" id="plNew">New collection</button></div>'+
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
   '<div class="row toolbar">'+
   '<button class="b" data-plsadd="'+c.id+'">New section</button>'+
   '<button class="b o" data-ple="'+c.id+'">Rename</button>'+
   '<button class="b o dz" data-pld="'+c.id+'">Delete plan</button>'+
   '<button class="b o" data-nav="planning">&larr; All plans</button></div>'+
   (n.total?'<div class="stats gap-b">'+
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
