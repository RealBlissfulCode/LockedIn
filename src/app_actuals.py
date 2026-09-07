# -*- coding: utf-8 -*-
"""What actually happened, and what that says a month really costs.

The plan holds four guesses per line. This holds facts: individual amounts, on
dates, with notes, against the income or cost line they belong to. Once there
are enough of them the Actual column stops being something you type and becomes
something measured.

The estimator is arithmetic, not a language model. Working out a monthly figure
from dated amounts is a maths problem with a right answer, and the interesting
part is picking the right method per line rather than generating prose about
it. A rent that arrives on the first at the same amount every month wants the
most recent value. Groceries bought eleven times at random want the total over
the elapsed period. Getting that choice right is what makes the number good.
"""

APP_ACTUALS = r"""
/* ============================ the ledger ============================
   One list for everything real. kind 'in' points at an income line, 'out' at a
   cost line, and lineId is that row's id. Keeping both in one list means the
   estimator, the editor and the totals are written once. */
function actuals(){
  if(!S.fin.actuals) S.fin.actuals=[];
  return S.fin.actuals;
}
/* Shifts predate this. Fold them in the first time so nothing logged before is
   stranded, and leave the old array alone in case an older device is still
   writing to it. */
function migrateShifts(){
  var sh=S.fin.shifts||[];
  if(!sh.length||S.fin.shiftsMoved) return;
  var seen={};
  actuals().forEach(function(a){ if(a.from) seen[a.from]=1; });
  sh.forEach(function(s){
    if(seen[s.id]) return;
    actuals().push({id:uid(),from:s.id,date:s.date,kind:'in',lineId:s.jobId,
      amount:s.net||0,gross:s.gross||0,hours:s.hours||0,note:s.note||''});
  });
  S.fin.shiftsMoved=true;
  save();
}

function actualsFor(lineId){
  return actuals().filter(function(a){return a.lineId===lineId;})
    .sort(function(a,b){return a.date<b.date?1:-1;});
}
function lineById(id){
  var j=S.fin.jobs.filter(function(x){return x.id===id;})[0];
  if(j) return {line:j,kind:'in'};
  var c=S.fin.costs.filter(function(x){return x.id===id;})[0];
  if(c) return {line:c,kind:'out'};
  return null;
}
function daysBetween(a,b){
  return Math.round((dOf(b)-dOf(a))/86400000);
}

/* ---------------- the estimator ----------------
   Two shapes of thing get logged and they want opposite treatment.

   A fixed recurring charge arrives about once a month for about the same
   amount. Averaging it over the elapsed window is wrong: miss a month's entry
   and the estimate drops even though the bill did not. The most recent
   value is what you will pay next month.

   Everything else is irregular. Eleven grocery runs in seven weeks tell you a
   weekly rate, and the only honest monthly figure is the total divided by how
   long you have been watching.

   Anything under two entries is not an estimate and does not pretend to be. */
function estimateLine(lineId){
  var e=actualsFor(lineId);
  var n=e.length;
  if(!n) return {n:0,monthly:0,method:'none',confidence:'none',months:0};
  if(n===1) return {n:1,monthly:e[0].amount,method:'single',confidence:'low',
                    months:0,total:e[0].amount};

  var oldest=e[n-1].date, newest=e[0].date;
  /* Measured to today, not to the last entry. Stopping at the last entry makes
     a line you gave up logging look like it is still running at full rate. */
  var spanDays=Math.max(1,daysBetween(oldest,today()));
  var months=Math.max(spanDays/30.44,0.5);
  var total=e.reduce(function(a,x){return a+(x.amount||0);},0);

  /* Does it look like a monthly bill. Gaps clustered near 30 days, and amounts
     that do not wander far from their own middle. */
  var gaps=[],i;
  for(i=0;i<n-1;i++) gaps.push(daysBetween(e[i+1].date,e[i].date));
  var amounts=e.map(function(x){return x.amount||0;}).slice().sort(function(a,b){return a-b;});
  var mid=amounts[Math.floor(amounts.length/2)]||0;
  var spread=mid?Math.max.apply(null,amounts.map(function(v){
    return Math.abs(v-mid)/mid;})):1;
  var monthlyGaps=gaps.length&&gaps.every(function(g){return g>=24&&g<=38;});
  var steady=spread<=0.15;

  if(monthlyGaps&&steady){
    /* Median of the last three, so one odd month does not move it. */
    var recent=e.slice(0,3).map(function(x){return x.amount||0;})
      .sort(function(a,b){return a-b;});
    return {n:n,monthly:recent[Math.floor(recent.length/2)],method:'recurring',
            confidence:n>=3?'good':'fair',months:months,total:total,
            oldest:oldest,newest:newest};
  }

  var conf = (spanDays>=75&&n>=6) ? 'good'
           : (spanDays>=30||n>=4) ? 'fair' : 'low';
  return {n:n,monthly:total/months,method:'rate',confidence:conf,
          months:months,total:total,oldest:oldest,newest:newest};
}

function methodWords(est){
  if(est.method==='none') return 'Nothing logged';
  if(est.method==='single') return 'One entry, so this is that amount and not an estimate';
  if(est.method==='recurring')
    return 'Arrives about monthly for about the same amount, so this is the middle of the '+
           'last '+Math.min(3,est.n)+'';
  return est.n+' entries over '+(Math.round(est.months*10)/10)+' months, so this is the '+
         'total spread across that';
}
function confChip(c){
  var cls={good:'t',fair:'d2',low:'d3',none:''}[c]||'';
  var word={good:'solid',fair:'rough',low:'thin',none:'none'}[c]||c;
  return '<span class="chip '+cls+'">'+word+'</span>';
}

/* What the whole month looks like once every line that has been logged uses
   its measured figure and everything else falls back to the plan. */
function measuredMonth(mode,path){
  var inc=0,cost=0,measuredIn=0,measuredOut=0;
  S.fin.jobs.forEach(function(j){
    if(!finLive(j)) return;
    var e=estimateLine(j.id);
    if(e.n>=2){ inc+=e.monthly; measuredIn++; } else { inc+=(j[mode]||0); }
  });
  S.fin.costs.forEach(function(c){
    if(!finLive(c)||!costInPath(c,path)) return;
    var e=estimateLine(c.id);
    if(e.n>=2){ cost+=e.monthly; measuredOut++; } else { cost+=(c[mode]||0); }
  });
  return {inc:inc,cost:cost,gap:inc-cost,measuredIn:measuredIn,measuredOut:measuredOut,
          totalIn:S.fin.jobs.filter(finLive).length,
          totalOut:S.fin.costs.filter(function(c){return finLive(c)&&costInPath(c,path);}).length};
}

/* ============================ the page ============================ */
var actTab='out';

function vActuals(){
  migrateShifts();
  var mode=S.fin.costMode||'real', path=S.fin.path||'rent';
  var m=measuredMonth(mode,path);
  var lines=actTab==='in'
    ? S.fin.jobs.slice()
    : S.fin.costs.filter(function(c){return costInPath(c,path);});
  var covered=actTab==='in'?m.measuredIn:m.measuredOut;
  var totalLines=actTab==='in'?m.totalIn:m.totalOut;

  var rows=lines.map(function(l){
    var e=estimateLine(l.id);
    var planned=l[mode]||0;
    var diff=e.n>=1?e.monthly-planned:0;
    return '<tr'+(finLive(l)?'':' class="offrow"')+'>'+
      '<td><b>'+E(l.name)+'</b>'+
        (actTab==='out'?'<div class="xs muted">'+E(l.section)+'</div>':
          (l.employer?'<div class="xs muted">'+E(l.employer)+'</div>':''))+'</td>'+
      '<td class="num sm muted">'+M(planned)+'</td>'+
      '<td class="num">'+(e.n?'<b>'+M(e.monthly)+'</b>':'<span class="muted">-</span>')+'</td>'+
      '<td class="num sm '+(e.n?(diff>0?'up':'down'):'muted')+'">'+
        (e.n?(diff>0?'+':'')+M(diff):'-')+'</td>'+
      '<td class="sm">'+(e.n?e.n+' '+confChip(e.confidence):'<span class="muted">none</span>')+'</td>'+
      '<td><button class="b o s" data-actline="'+E(l.id)+'">'+
        (e.n?'Entries':'Add')+'</button></td></tr>';
  }).join('');

  return '<div class="page"><div class="phead"><h1>Actuals</h1>'+
   '<p>What really happened, line by line. Log the amounts as they land and the monthly '+
   'figure stops being a guess. Nothing here touches the plan until you tell it to.</p></div>'+

   '<div class="row toolbar">'+
   '<button class="b" id="actAdd">Log an amount</button>'+
   '<button class="b o" id="actApply">Fill the Actual column</button>'+
   '<button class="b o" id="actCsv">Export</button>'+
   '<button class="b o" data-nav="financial">&larr; Plan</button></div>'+

   '<div class="stats gap-b">'+
   '<div class="stat"><b data-cv="'+m.inc+'">'+M(m.inc)+'</b><span>Income / mo</span></div>'+
   '<div class="stat"><b data-cv="'+m.cost+'">'+M(m.cost)+'</b><span>Costs / mo</span></div>'+
   '<div class="stat '+(m.gap>=0?'good':'bad')+'"><b data-cv="'+m.gap+'">'+M(m.gap)+'</b>'+
     '<span>'+(m.gap>=0?'Surplus':'Shortfall')+'</span></div>'+
   '<div class="stat"><b>'+(m.measuredIn+m.measuredOut)+' of '+(m.totalIn+m.totalOut)+'</b>'+
     '<span>Lines measured</span></div></div>'+

   '<div class="note"><b>How this is worked out.</b> Any line with two or more entries uses '+
   'what you logged. Everything else falls back to its '+modeLabel(mode).toLowerCase()+
   ' guess, so the total gets more real as you log more and never has a hole in it.</div>'+

   '<div class="sec"><div class="spread"><h2>Line by line</h2>'+
   '<div class="row"><button class="pill'+(actTab==='out'?' on':'')+'" data-acttab="out">Costs</button>'+
   '<button class="pill'+(actTab==='in'?' on':'')+'" data-acttab="in">Income</button></div></div>'+
   '<p class="sub">'+covered+' of '+totalLines+' lines have enough logged to be measured.</p>'+
   (lines.length?'<div class="tw wide"><table><thead><tr><th>Line</th>'+
     '<th class="num">Planned</th><th class="num">Measured</th><th class="num">Difference</th>'+
     '<th>Entries</th><th></th></tr></thead><tbody>'+rows+'</tbody></table></div>'
    :'<div class="empty">No '+(actTab==='in'?'income':'cost')+' lines yet.</div>')+
   '</div>'+

   monthsChart()+
   recentEntries()+
   '</div>';
}

/* Six calendar months of what actually moved. A month with nothing logged
   stays as a zero rather than being dropped, otherwise the gaps close up and a
   quiet month looks like it never happened. */
function ledgerMonths(n){
  var out=[],d=new Date(),i;
  d.setDate(1);
  for(i=n-1;i>=0;i--){
    var mm=new Date(d.getFullYear(),d.getMonth()-i,1);
    out.push({key:mm.getFullYear()+'-'+p2(mm.getMonth()+1),
              label:mm.toLocaleDateString(undefined,{month:'short'}),inc:0,out:0});
  }
  actuals().forEach(function(a){
    var k=String(a.date||'').slice(0,7);
    for(var j=0;j<out.length;j++) if(out[j].key===k){
      if(a.kind==='in') out[j].inc+=(a.amount||0); else out[j].out+=(a.amount||0);
    }
  });
  return out;
}

function monthsChart(){
  var mons=ledgerMonths(6);
  var any=mons.some(function(x){return x.inc||x.out;});
  if(!any) return '';
  var max=Math.max.apply(null,mons.map(function(x){return Math.max(x.inc,x.out);}).concat([1]));
  return '<div class="sec"><h2>Six months of real money</h2>'+
   '<p class="sub">Only what you logged. A month sitting at nothing means nothing was '+
   'entered for it, which is not the same as nothing having happened.</p>'+
   '<div class="card pad">'+
   chartCols({max:max,h:160,cols:mons.map(function(x){
     return {label:x.label,sub:M(x.inc-x.out),subCls:(x.inc-x.out)>=0?'good':'bad',
       bars:[{v:x.inc,cls:'ct2',tip:'In '+M(x.inc)},{v:x.out,cls:'ct5',tip:'Out '+M(x.out)}]};})})+
   '<div class="ckey"><span><i class="ct2"></i>Came in</span>'+
   '<span><i class="ct5"></i>Went out</span>'+
   '<span class="muted">Number under each month is what was left</span></div>'+
   '</div></div>';
}

function recentEntries(){
  var all=actuals().slice().sort(function(a,b){return a.date<b.date?1:-1;}).slice(0,25);
  if(!all.length) return '<div class="sec"><h2>Recent</h2>'+
    '<div class="empty"><p>Nothing logged yet.</p>'+
    '<p class="sm">Press Log an amount, or open any line above.</p></div></div>';
  return '<div class="sec"><h2>Recent</h2><div class="tw"><table>'+
    '<thead><tr><th>Date</th><th>Line</th><th class="num">Amount</th><th>Note</th><th></th></tr></thead>'+
    '<tbody>'+all.map(function(a){
      var l=lineById(a.lineId);
      return '<tr><td class="sm">'+E(shortD(a.date))+'</td>'+
        '<td><b>'+E(l?l.line.name:'(deleted line)')+'</b>'+
          '<span class="chip" style="margin-left:6px">'+(a.kind==='in'?'in':'out')+'</span></td>'+
        '<td class="num">'+M(a.amount)+'</td>'+
        '<td class="sm muted">'+E(a.note||'')+'</td>'+
        '<td><button class="b o s" data-acte="'+E(a.id)+'">Edit</button></td></tr>';
    }).join('')+'</tbody></table></div></div>';
}

/* Every entry on one line, with the estimate it produces spelled out. */
function lineEntries(lineId){
  var got=lineById(lineId); if(!got) return;
  var l=got.line, e=estimateLine(lineId);
  var rows=actualsFor(lineId);
  var body=
    '<div class="stats gap-b">'+
    '<div class="stat"><b>'+(e.n?M(e.monthly):'-')+'</b><span>Measured / mo</span></div>'+
    '<div class="stat"><b>'+M(l[S.fin.costMode||'real']||0)+'</b><span>Planned</span></div>'+
    '<div class="stat"><b>'+e.n+'</b><span>Entries</span></div></div>'+
    '<p class="sm muted">'+E(methodWords(e))+'.</p>'+
    (rows.length?'<div class="tw" style="margin-top:12px"><table>'+
      '<thead><tr><th>Date</th><th class="num">Amount</th><th>Note</th><th></th></tr></thead><tbody>'+
      rows.map(function(a){
        return '<tr><td class="sm">'+E(shortD(a.date))+'</td>'+
        '<td class="num">'+M(a.amount)+'</td>'+
        '<td class="sm muted">'+E(a.note||'')+'</td>'+
        '<td><button class="b o s" data-acte="'+E(a.id)+'">Edit</button> '+
        '<button class="x" data-actd="'+E(a.id)+'">&times;</button></td></tr>';
      }).join('')+'</tbody></table></div>'
     :'<div class="empty sm" style="margin-top:12px">Nothing logged against this line yet.</div>');
  var m=modal(l.name,body,
    '<button class="b o" data-close>Close</button>'+
    '<button class="b" data-actadd="'+E(lineId)+'">Log an amount</button>');
  return m;
}

/* One editor for adding and for changing. Income lines that carry an hourly
   rate get the hours and gross fields as well, because working out take-home
   from them is the whole reason the old shift log existed. */
function actualEditor(id,presetLine){
  var a=id?actuals().filter(function(x){return x.id===id;})[0]:null;
  if(id&&!a) return;
  var lineId=a?a.lineId:(presetLine||'');
  var opts=[];
  S.fin.jobs.forEach(function(j){opts.push([j.id,'In: '+j.name]);});
  S.fin.costs.forEach(function(c){opts.push([c.id,'Out: '+c.section+' / '+c.name]);});
  if(!opts.length){toast('Add an income or cost line first');return;}
  if(!lineId) lineId=opts[0][0];

  var got=lineById(lineId);
  var hourly=got&&got.kind==='in'&&got.line.rate>0;

  var fields=[
    {id:'aL',l:'Which line',t:'select',o:opts,v:lineId},
    {id:'aD',l:'Date',t:'date',v:a?a.date:today()},
    {id:'aA',l:'Amount that landed',t:'number',step:'0.01',v:a?a.amount:''}
  ];
  if(hourly||(a&&(a.hours||a.gross))){
    fields.push({id:'aH',l:'Hours',t:'number',step:'0.25',v:a?a.hours:''});
    fields.push({id:'aG',l:'Gross before tax',t:'number',step:'0.01',v:a?a.gross:''});
  }
  fields.push({id:'aN',l:'Note',v:a?a.note:'',ph:'What this was'});

  var m=modal(id?'Edit entry':'Log an amount',
    form(fields)+
    '<p class="sm muted">Amount is what actually moved. For income that is what landed after '+
    'tax, for a cost it is what you paid.</p>',
    (id?'<button class="b o dz" id="aDel">Delete</button>':'')+
    '<button class="b o" data-close>Cancel</button><button class="b" id="aSave">Save</button>');

  var d=$('#aDel',m);
  if(d) d.onclick=function(){
    S.fin.actuals=actuals().filter(function(x){return x.id!==id;});
    save(); m.remove(); route(); toast('Deleted');
  };
  $('#aSave',m).onclick=function(){
    var lid=$('#aL',m).value, g=lineById(lid);
    var amt=num($('#aA',m).value);
    var hrs=$('#aH',m)?num($('#aH',m).value):0;
    var gross=$('#aG',m)?num($('#aG',m).value):0;
    /* Nothing typed in the amount but hours and a rate present is the shift
       case, so work it out rather than saving a zero. */
    if(!amt&&hrs&&g&&g.line.rate) { gross=gross||hrs*g.line.rate; amt=Math.round(gross*0.8*100)/100; }
    if(!amt&&gross) amt=Math.round(gross*0.8*100)/100;
    if(!amt){toast('Put an amount in');return;}
    var o={id:id||uid(),date:$('#aD',m).value||today(),
           kind:g?g.kind:'out',lineId:lid,amount:amt,
           gross:gross||0,hours:hrs||0,note:$('#aN',m).value.trim()};
    if(id) S.fin.actuals=actuals().map(function(x){return x.id===id?o:x;});
    else actuals().push(o);
    save(); m.remove(); route(); toast(id?'Saved':'Logged');
  };
}

/* Writing the measured figures into the plan's Actual column. Only lines with
   enough behind them, and it says how many it moved rather than claiming to
   have done the lot. */
function applyMeasured(){
  var n=0;
  S.fin.jobs.forEach(function(j){
    var e=estimateLine(j.id);
    if(e.n>=2){ j.actual=Math.round(e.monthly); n++; }
  });
  S.fin.costs.forEach(function(c){
    var e=estimateLine(c.id);
    if(e.n>=2){ c.actual=Math.round(e.monthly); n++; }
  });
  if(!n){ toast('No line has two entries yet'); return; }
  save(); route();
  toast(n+' line'+(n===1?'':'s')+' updated from what you logged');
}

function bindActuals(){
  on('#actAdd','click',function(){actualEditor(null,null);});
  on('#actApply','click',function(){
    if(confirm('Overwrite the Actual column on every line that has two or more entries?'))
      applyMeasured();
  });
  on('#actCsv','click',function(){
    var rows=[['Date','Direction','Line','Section','Amount','Gross','Hours','Note']];
    actuals().slice().sort(function(a,b){return a.date<b.date?-1:1;}).forEach(function(a){
      var l=lineById(a.lineId);
      rows.push([a.date,a.kind==='in'?'income':'cost',l?l.line.name:'(deleted)',
                 (l&&l.line.section)||'',a.amount,a.gross||'',a.hours||'',a.note||'']);
    });
    dl('actuals-'+today()+'.csv',toCSV(rows),'text/csv');
  });
  countUp($('#view'));
}
"""
