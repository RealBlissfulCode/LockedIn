# -*- coding: utf-8 -*-
"""Getting one section in or out on its own.

The whole account already saves to a file. This is for the smaller thing people
actually ask for: hand me the cost lines as a spreadsheet, let me fix forty rows
in Sheets, give them back. One section at a time, in a format a person can read.

CSV for anything with rows in it, because that opens in Sheets and Excel and
Numbers without asking. JSON alongside it for anything with structure a
spreadsheet would flatten away, so nothing is ever lost by choosing the wrong
one.
"""

APP_IO = r"""
/* ============================ import and export ============================ */

/* A CSV a spreadsheet will actually open. Quotes doubled, anything with a
   comma, a quote or a newline in it wrapped. */
function csvEsc2(v){
  v=(v===null||v===undefined)?'':String(v);
  return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;
}
function csvOut(rows){
  return rows.map(function(r){return r.map(csvEsc2).join(',');}).join('\r\n');
}
/* And one it will actually give back. Handles quoted fields with commas and
   newlines inside them, doubled quotes, and both line ending conventions,
   because a file that has been round a Windows machine should still load. */
function csvIn(text){
  var rows=[], row=[], cur='', q=false, i=0;
  text=String(text).replace(/^﻿/,'');
  while(i<text.length){
    var ch=text[i];
    if(q){
      if(ch==='"'){ if(text[i+1]==='"'){cur+='"';i+=2;continue;} q=false;i++;continue; }
      cur+=ch;i++;continue;
    }
    if(ch==='"'){ q=true;i++;continue; }
    if(ch===','){ row.push(cur);cur='';i++;continue; }
    if(ch==='\r'){ i++;continue; }
    if(ch==='\n'){ row.push(cur);rows.push(row);row=[];cur='';i++;continue; }
    cur+=ch;i++;
  }
  if(cur!==''||row.length){ row.push(cur); rows.push(row); }
  return rows.filter(function(r){ return r.some(function(c){return String(c).trim()!=='';}); });
}
/* Header row to index, so a column can move and the import still works. */
function csvCols(head){
  var m={};
  head.forEach(function(h,i){ m[String(h).trim().toLowerCase()]=i; });
  return function(name,row,dflt){
    var i=m[String(name).toLowerCase()];
    return (i===undefined||row[i]===undefined)?(dflt===undefined?'':dflt):String(row[i]).trim();
  };
}
function ynBool(v){ return /^(y|yes|true|1|done|x)$/i.test(String(v).trim()); }

/* Every section that can go in or out on its own.
   rows() gives the spreadsheet. load() takes one back, either adding to what is
   here or replacing it. json()/loadJson() carry the parts a flat table cannot,
   like a cost line's breakdown or a comparison list's own columns. */
var SECTION_IO=[
 {key:'plans', label:'Plans', page:'planning',
  head:['Plan','Section','Item','Done','Note'],
  rows:function(){
    var out=[];
    planCols().forEach(function(c){ (c.subs||[]).forEach(function(s){
      (s.items||[]).forEach(function(i){
        out.push([c.name,s.name,i.text,i.done?'yes':'',i.note||'']); }); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.plan.cols=[];
    body.forEach(function(r){
      var pn=g('Plan',r)||'Imported', sn=g('Section',r)||'Everything else';
      var c=null;
      (S.plan.cols||[]).forEach(function(x){ if(!c&&x.name===pn) c=x; });
      if(!c){ c={id:uid(),name:pn,note:'',subs:[]}; S.plan.cols.push(c); }
      var s=null;
      (c.subs=c.subs||[]).forEach(function(x){ if(!s&&x.name===sn) s=x; });
      if(!s){ s={id:uid(),name:sn,note:'',items:[]}; c.subs.push(s); }
      s.items=s.items||[];
      s.items.push({id:uid(),text:g('Item',r),note:g('Note',r),done:ynBool(g('Done',r))});
    });
  },
  json:function(){ return {plan:S.plan}; },
  loadJson:function(o){ if(o.plan) S.plan=o.plan; }},

 {key:'schedule', label:'Calendar', page:'schedule',
  head:['Date','Who','What','From','To','Where'],
  rows:function(){
    var out=[];
    Object.keys(S.days||{}).sort().forEach(function(d){
      ((S.days[d]||{}).sched||[]).forEach(function(x){
        out.push([d,WHO(x.who),x.what||'',x.from||'',x.to||'',x.where||'']); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) Object.keys(S.days||{}).forEach(function(d){ S.days[d].sched=[]; });
    body.forEach(function(r){
      var d=g('Date',r); if(!d) return;
      var day=dayLog(d);
      day.sched=day.sched||[];
      day.sched.push({who:whoIdFor(g('Who',r)),what:g('What',r),
        from:g('From',r),to:g('To',r),where:g('Where',r)});
    });
  },
  json:function(){ return {days:S.days,sched:S.sched}; },
  loadJson:function(o){ if(o.days) S.days=o.days; if(o.sched) S.sched=o.sched; }},

 {key:'income', label:'Income lines', page:'financial',
  head:['Name','Who','Employer','Title','Hourly rate','Low','Realistic','High','Actual','Counted'],
  rows:function(){
    return (S.fin.jobs||[]).map(function(j){
      return [j.name,WHO(j.who),j.employer||'',j.title||'',j.rate||'',
        j.low||0,j.real||0,j.high||0,j.actual||'',j.off?'no':'yes']; });
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.fin.jobs=[];
    body.forEach(function(r){
      if(!g('Name',r)) return;
      S.fin.jobs.push({id:uid(),name:g('Name',r),who:whoIdFor(g('Who',r)),
        employer:g('Employer',r),title:g('Title',r),rate:num(g('Hourly rate',r))||null,
        low:num(g('Low',r)),real:num(g('Realistic',r)),high:num(g('High',r)),
        actual:num(g('Actual',r))||null,off:/^(n|no|off|false)$/i.test(g('Counted',r,'yes'))});
    });
  },
  json:function(){ return {jobs:S.fin.jobs}; },
  loadJson:function(o){ if(o.jobs) S.fin.jobs=o.jobs; }},

 {key:'costs', label:'Cost lines', page:'financial',
  head:['Name','Section','Who','Low','Realistic','High','Actual','Counted','Note'],
  rows:function(){
    return (S.fin.costs||[]).map(function(c){
      return [c.name,c.section,WHO(c.who),c.low||0,c.real||0,c.high||0,
        c.actual||'',c.off?'no':'yes',c.note||'']; });
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.fin.costs=[];
    body.forEach(function(r){
      if(!g('Name',r)) return;
      S.fin.costs.push({id:uid(),name:g('Name',r),
        section:newSection(g('Section',r),g('Name',r)),who:whoIdFor(g('Who',r)),
        low:num(g('Low',r)),real:num(g('Realistic',r)),high:num(g('High',r)),
        actual:num(g('Actual',r))||null,
        off:/^(n|no|off|false)$/i.test(g('Counted',r,'yes')),
        note:g('Note',r),parts:[]});
    });
  },
  json:function(){ return {costs:S.fin.costs}; },
  loadJson:function(o){ if(o.costs) S.fin.costs=o.costs; }},

 {key:'breakdown', label:'Cost breakdowns', page:'financial',
  head:['Cost','Part','Qty','Each'],
  rows:function(){
    var out=[];
    (S.fin.costs||[]).forEach(function(c){ (c.parts||[]).forEach(function(p){
      out.push([c.name,p.n,p.qty==null?1:p.qty,p.each||0]); }); });
    (S.fin.jobs||[]).forEach(function(j){ (j.parts||[]).forEach(function(p){
      out.push([j.name,p.n,p.qty==null?1:p.qty,p.each||0]); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    var all=(S.fin.costs||[]).concat(S.fin.jobs||[]);
    if(replace) all.forEach(function(x){ x.parts=[]; });
    body.forEach(function(r){
      var nm=g('Cost',r), hit=null;
      all.forEach(function(x){ if(!hit&&x.name===nm) hit=x; });
      if(!hit) return;
      hit.parts=hit.parts||[];
      hit.parts.push({id:uid(),n:g('Part',r)||'Part',
        qty:num(g('Qty',r,'1'))||1,each:num(g('Each',r))});
    });
  }},

 {key:'purchases', label:'Comparison lists', page:'financial/purchases',
  head:['List','Item','Price','Link','Notes'],
  rows:function(){
    var out=[];
    Object.keys(S.fin.purchases||{}).forEach(function(n){
      ((S.fin.purchases[n]||{}).items||[]).forEach(function(i){
        out.push([n,i.name,i.price||'',i.link||'',i.notes||'']); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.fin.purchases={};
    body.forEach(function(r){
      var ln=g('List',r)||'Imported';
      var L=S.fin.purchases[ln]||(S.fin.purchases[ln]={cat:'',note:'',items:[]});
      L.items=L.items||[];
      L.items.push({id:uid(),name:g('Item',r),price:num(g('Price',r)),
        link:g('Link',r),notes:g('Notes',r),fields:{}});
    });
  },
  json:function(){ return {purchases:S.fin.purchases}; },
  loadJson:function(o){ if(o.purchases) S.fin.purchases=o.purchases; }},

 {key:'strategies', label:'Strategies', page:'financial/strategies',
  head:['List','Item','Low','Realistic','High','Rate','Effort','When','Status','How'],
  rows:function(){
    var out=[];
    Object.keys(S.fin.strategies||{}).forEach(function(n){
      ((S.fin.strategies[n]||{}).items||[]).forEach(function(i){
        out.push([n,i.name,i.low||0,i.real||0,i.high||0,i.rate||'',i.effort||'',
          i.when||'',i.status||'',i.how||'']); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.fin.strategies={};
    body.forEach(function(r){
      var ln=g('List',r)||'Imported';
      var L=S.fin.strategies[ln]||(S.fin.strategies[ln]={note:'',items:[]});
      L.items=L.items||[];
      L.items.push({id:uid(),name:g('Item',r),low:num(g('Low',r)),real:num(g('Realistic',r)),
        high:num(g('High',r)),rate:g('Rate',r),effort:g('Effort',r),
        when:g('When',r),status:g('Status',r),how:g('How',r)});
    });
  },
  json:function(){ return {strategies:S.fin.strategies}; },
  loadJson:function(o){ if(o.strategies) S.fin.strategies=o.strategies; }},

 {key:'shopping', label:'Shopping lists', page:'shopping',
  head:['List','Category','Item','Qty','Done'],
  rows:function(){
    var out=[], L=(S.shop||{}).lists||{};
    Object.keys(L).forEach(function(n){
      (L[n].items||[]).forEach(function(i){
        out.push([n,L[n].cat||'',i.n||i.name||'',i.q||i.qty||'',i.done?'yes':'']); }); });
    return out;
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    S.shop=S.shop||{active:'',lists:{}};
    if(replace) S.shop.lists={};
    body.forEach(function(r){
      var ln=g('List',r)||'Imported';
      var L=S.shop.lists[ln]||(S.shop.lists[ln]={cat:g('Category',r),fav:false,items:[]});
      L.items=L.items||[];
      L.items.push({id:uid(),n:g('Item',r),q:g('Qty',r),done:ynBool(g('Done',r))});
    });
    if(!S.shop.active||!S.shop.lists[S.shop.active])
      S.shop.active=Object.keys(S.shop.lists)[0]||'';
  },
  json:function(){ return {shop:S.shop}; },
  loadJson:function(o){ if(o.shop) S.shop=o.shop; }},

 {key:'ingredients', label:'Ingredient prices', page:'shopping/ingredients',
  head:['Ingredient','Aisle','Walmart per 100g','Costco per 100g'],
  rows:function(){
    return allIngKeys().map(function(k){ var g=ING(k);
      return [g.n,g.a||'',g.w==null?'':g.w,g.c==null?'':g.c]; });
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    if(replace) S.ingOv={};
    var byName={};
    allIngKeys().forEach(function(k){ byName[ING(k).n.toLowerCase()]=k; });
    body.forEach(function(r){
      var k=byName[g('Ingredient',r).toLowerCase()]; if(!k) return;
      var ov=S.ingOv[k]||{};
      var w=g('Walmart per 100g',r), c=g('Costco per 100g',r);
      if(w!=='') ov.w=num(w);
      if(c!=='') ov.c=num(c);
      if(g('Aisle',r)) ov.a=g('Aisle',r);
      S.ingOv[k]=ov;
    });
  },
  json:function(){ return {ingOv:S.ingOv}; },
  loadJson:function(o){ if(o.ingOv) S.ingOv=o.ingOv; }},

 {key:'daylog', label:'Daily log', page:'meals',
  head:['Date','Training','Weight','Notes'],
  rows:function(){
    return Object.keys(S.days||{}).sort().map(function(d){ var r=S.days[d]||{};
      return [d,r.workout||'rest',r.w==null?'':r.w,r.notes||'']; });
  },
  load:function(rows,replace){
    var g=csvCols(rows[0]), body=rows.slice(1);
    body.forEach(function(r){
      var d=g('Date',r); if(!d) return;
      var day=dayLog(d);
      if(g('Training',r)) day.workout=g('Training',r);
      if(g('Weight',r)) day.w=num(g('Weight',r));
      if(g('Notes',r)) day.notes=g('Notes',r);
    });
  },
  json:function(){ return {days:S.days}; },
  loadJson:function(o){ if(o.days) S.days=o.days; }}
];

function sectionIO(key){
  var hit=null;
  SECTION_IO.forEach(function(x){ if(!hit&&x.key===key) hit=x; });
  return hit;
}
/* A name in a spreadsheet back to the person it means. Falls back to shared,
   because a row that names somebody who left should still come in. */
function whoIdFor(name){
  name=String(name||'').trim();
  if(!name) return shared()?EVERYONE:ME();
  if(/^(both|both of us|all|shared|everyone|us)$/i.test(name)) return EVERYONE;
  var hit=null;
  MEMS().forEach(function(m){ if(!hit&&m.name.toLowerCase()===name.toLowerCase()) hit=m.id; });
  return hit||(shared()?EVERYONE:ME());
}

/* One panel, the same for every section. */
function ioModal(key){
  var d=sectionIO(key); if(!d) return;
  var n=d.rows().length;
  var m=modal(d.label+': import and export',
    '<p class="sm muted">A spreadsheet for reading and editing, a file for keeping '+
    'everything exactly as it is. Both only cover '+E(d.label.toLowerCase())+'. '+
    'To save the whole account at once use Settings.</p>'+
    '<div class="stats gap-b" style="margin-top:12px">'+
    '<div class="stat"><b>'+n+'</b><span>rows right now</span></div></div>'+
    '<div class="row"><button class="b" id="ioCsv">Export a spreadsheet</button>'+
    (d.json?'<button class="b o" id="ioJson">Export a file</button>':'')+'</div>'+
    '<div class="sec" style="margin-top:18px"><h2>Bringing some in</h2>'+
    '<p class="sm muted">A .csv with the same column headings as the export, or a '+
    'file this app wrote. Column order does not matter, only the headings.</p>'+
    '<label class="f" style="margin-top:12px"><span>What to do with what is here</span>'+
    '<select id="ioMode">'+
    '<option value="merge">Add it to what is already here</option>'+
    '<option value="replace">Replace what is here</option></select></label>'+
    '<div class="row"><button class="b o" id="ioPick">Choose a file</button></div>'+
    '<p class="xs muted" style="margin-top:10px">Headings for this one: '+
    E(d.head.join(', '))+'</p></div>',
    '<button class="b" data-close>Close</button>');

  $('#ioCsv',m).onclick=function(){
    dl(d.key+'-'+today()+'.csv',csvOut([d.head].concat(d.rows())),'text/csv');
    toast('Spreadsheet saved');
  };
  var jb=$('#ioJson',m);
  if(jb) jb.onclick=function(){
    dl(d.key+'-'+today()+'.json',
      JSON.stringify({app:'lockedin',section:d.key,exported:new Date().toISOString(),
        data:d.json()},null,1),'application/json');
    toast('File saved');
  };
  $('#ioPick',m).onclick=function(){
    var replace=$('#ioMode',m).value==='replace';
    var inp=document.createElement('input');
    inp.type='file'; inp.accept='.csv,.json,text/csv,application/json';
    inp.onchange=function(){
      var f=inp.files[0]; if(!f) return;
      var fr=new FileReader();
      fr.onload=function(){
        try{
          var txt=String(fr.result);
          var before=d.rows().length;
          if(/^\s*[\{\[]/.test(txt)){
            if(!d.loadJson) throw new Error('this section only takes a spreadsheet');
            var o=JSON.parse(txt);
            d.loadJson(o.data||o);
          }else{
            var rows=csvIn(txt);
            if(rows.length<2) throw new Error('there are no rows in that file');
            d.load(rows,replace);
          }
          save(); m.remove(); route();
          toast(d.label+': '+before+' before, '+d.rows().length+' now');
        }catch(e){
          alert('That did not load.\n\n'+(e.message||e)+
            '\n\nThe headings this section expects are:\n'+d.head.join(', '));
        }
      };
      fr.readAsText(f);
    };
    inp.click();
  };
  return m;
}
"""
