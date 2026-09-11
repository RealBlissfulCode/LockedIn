# -*- coding: utf-8 -*-
APP_REORDER = r"""
/* ============================================================
   PUTTING THE MONEY LINES IN ORDER

   The order of the income and cost lines is the order they are stored in, so
   moving one is a real edit. It saves, it syncs, and the other device sees the
   same list in the same order. Nothing here sorts on the way to the screen,
   which means what you arranged is what stays arranged.

   Dragging runs on pointer events rather than the HTML5 drag API, because that
   one does not fire on a phone at all. The grip is also a real button, so the
   same move is one arrow key away without touching a mouse.
   ============================================================ */

function finList(kind){return kind==='jobs'?S.fin.jobs:S.fin.costs;}

/* Pull one line out and put it back somewhere else. Everything between the two
   places closes up behind it, which is what a list does when you move an item
   in it by hand. */
function finMove(kind,from,to){
  var a=finList(kind);
  if(!a||from<0||from>=a.length) return false;
  to=Math.max(0,Math.min(a.length-1,to));
  if(to===from) return false;
  a.splice(to,0,a.splice(from,1)[0]);
  save();
  return true;
}

/* The grip. Six dots is the oldest sign in the business for "this moves", and
   it earns its place in the row because it is also the keyboard control. */
function finGrip(kind,i,label){
  var d='',x,y;
  for(y=0;y<3;y++) for(x=0;x<2;x++)
    d+='<circle cx="'+(2+x*5)+'" cy="'+(3+y*5)+'" r="1.35"></circle>';
  return '<button type="button" class="grip" data-grip="'+E(kind)+'" data-ord="'+i+'" '+
    'aria-label="Move '+E(label)+' up or down the list" '+
    'title="Drag to move it, or use the arrow keys">'+
    '<svg viewBox="0 0 9 14" width="9" height="14" aria-hidden="true">'+d+'</svg></button>';
}

/* ---- the drag itself ----
   Measurements are taken once, in page coordinates rather than screen ones, so
   the sums still hold while the page scrolls underneath a dragging finger. */
var _drag=null;

function finUnits(kind,tbody){
  /* A line can be two rows: itself, and its breakdown underneath if that is
     open. They travel together or the breakdown detaches from the thing it
     belongs to. */
  var out=[];
  $$('[data-grip="'+kind+'"]',tbody).forEach(function(g){
    var tr=g.closest('tr'); if(!tr) return;
    var rows=[tr], nx=tr.nextElementSibling;
    if(nx&&nx.classList.contains('prow2')) rows.push(nx);
    var top=tr.getBoundingClientRect().top+(window.pageYOffset||0);
    var last=rows[rows.length-1].getBoundingClientRect();
    out.push({idx:+g.dataset.ord, rows:rows, grip:g, top:top,
              h:last.top+(window.pageYOffset||0)+last.height-top});
  });
  return out;
}

function finDragStart(e){
  if(_drag||e.button>0) return;
  var g=e.currentTarget, kind=g.dataset.grip, tbody=g.closest('tbody');
  if(!tbody) return;
  var units=finUnits(kind,tbody);
  var me=null,i;
  for(i=0;i<units.length;i++) if(units[i].grip===g) me=units[i];
  if(!me||units.length<2) return;
  e.preventDefault();
  try{g.setPointerCapture(e.pointerId);}catch(err){}
  _drag={kind:kind,g:g,me:me,units:units,from:me.idx,to:me.idx,
         startY:e.clientY+(window.pageYOffset||0),clientY:e.clientY,raf:0};
  me.rows.forEach(function(r){r.classList.add('lift');});
  document.body.classList.add('dragging');
  g.addEventListener('pointermove',finDragMove);
  g.addEventListener('pointerup',finDragEnd);
  g.addEventListener('pointercancel',finDragCancel);
  window.addEventListener('keydown',finDragKey,true);
  finDragPaint();
}

/* Near the top or bottom of the screen the page comes to the finger. Without
   it a line on a phone can only ever move as far as one screenful. */
function finDragScroll(){
  if(!_drag) return;
  var y=_drag.clientY, h=window.innerHeight||0, edge=74, step=0;
  if(y<edge) step=-Math.ceil((edge-y)/5);
  else if(y>h-edge) step=Math.ceil((y-(h-edge))/5);
  if(step){
    var before=window.pageYOffset||0;
    window.scrollBy(0,step);
    if((window.pageYOffset||0)!==before) finDragPaint();
  }
  _drag.raf=requestAnimationFrame(finDragScroll);
}

function finDragPaint(){
  var d=_drag; if(!d) return;
  var dy=(d.clientY+(window.pageYOffset||0))-d.startY;
  var top=d.me.top+dy, bot=top+d.me.h, to=d.from;
  d.units.forEach(function(u){
    if(u.idx===d.from) return;
    var mid=u.top+u.h/2;
    if(u.idx<d.from&&top<mid) to=Math.min(to,u.idx);
    else if(u.idx>d.from&&bot>mid) to=Math.max(to,u.idx);
  });
  d.to=to;
  d.units.forEach(function(u){
    var shift=0;
    if(u.idx===d.from) shift=dy;
    else if(u.idx>=to&&u.idx<d.from) shift=d.me.h;
    else if(u.idx>d.from&&u.idx<=to) shift=-d.me.h;
    u.rows.forEach(function(r){
      r.style.transform=shift?'translateY('+shift+'px)':'';
      r.classList.toggle('slid',!!shift&&u.idx!==d.from);
    });
  });
}

function finDragMove(e){
  if(!_drag) return;
  e.preventDefault();
  _drag.clientY=e.clientY;
  if(!_drag.raf) _drag.raf=requestAnimationFrame(finDragScroll);
  finDragPaint();
}

function finDragClear(){
  var d=_drag; if(!d) return;
  if(d.raf) cancelAnimationFrame(d.raf);
  d.units.forEach(function(u){u.rows.forEach(function(r){
    r.style.transform=''; r.classList.remove('lift','slid');});});
  document.body.classList.remove('dragging');
  d.g.removeEventListener('pointermove',finDragMove);
  d.g.removeEventListener('pointerup',finDragEnd);
  d.g.removeEventListener('pointercancel',finDragCancel);
  window.removeEventListener('keydown',finDragKey,true);
  _drag=null;
}

function finDragEnd(){
  var d=_drag; if(!d) return;
  var kind=d.kind, from=d.from, to=d.to;
  finDragClear();
  if(to!==from&&finMove(kind,from,to)) finAfterMove(kind,to);
}

function finDragCancel(){finDragClear();}

function finDragKey(e){
  if(e.key==='Escape'&&_drag){e.preventDefault();finDragCancel();}
}

/* ---- keyboard ----
   Arrows move it a step, Home and End take it to the ends. Focus follows the
   line to where it landed, so holding an arrow down walks it up the list. */
function finGripKey(e){
  var g=e.currentTarget, kind=g.dataset.grip, i=+g.dataset.ord;
  var n=finList(kind).length, to=null;
  if(e.key==='ArrowUp') to=i-1;
  else if(e.key==='ArrowDown') to=i+1;
  else if(e.key==='Home') to=0;
  else if(e.key==='End') to=n-1;
  else return;
  e.preventDefault();
  if(finMove(kind,i,Math.max(0,Math.min(n-1,to)))) finAfterMove(kind,Math.max(0,Math.min(n-1,to)));
}

/* Redraw, then put the caret back on the line that moved rather than at the
   top of the page, and say where it ended up for anyone listening. */
function finAfterMove(kind,to){
  reroute();
  var g=$('[data-grip="'+kind+'"][data-ord="'+to+'"]');
  if(g){
    try{g.focus({preventScroll:true});}catch(e){try{g.focus();}catch(e2){}}
    var r=g.getBoundingClientRect();
    if(r.top<80||r.bottom>(window.innerHeight||0)-80)
      try{g.scrollIntoView({block:'center',behavior:'smooth'});}catch(e3){}
  }
  finSay((kind==='jobs'?'Income line':'Cost line')+' moved to number '+(to+1));
}

/* A quiet line for a screen reader. It says what just happened without
   putting a toast over the table you are working in. */
function finSay(msg){
  var n=$('#finsay');
  if(!n){n=document.createElement('div');n.id='finsay';n.className='sr';
    n.setAttribute('aria-live','polite');document.body.appendChild(n);}
  n.textContent=msg;
}

/* ---- sorting ----
   A sort writes the order into the list and then gets out of the way. It is a
   starting point you can drag from, not a setting that keeps reasserting
   itself over whatever you arrange by hand. */
var FINSORTS=[
  ['big','Biggest first'],
  ['small','Smallest first'],
  ['az','Name, A to Z'],
  ['who','By person, then biggest'],
  ['sect','By section, then biggest'],
  ['on','Counted ones first']
];
function finSortOpts(kind){
  return FINSORTS.filter(function(o){return o[0]!=='sect'||kind==='costs';});
}
/* It reads "Reorder" rather than "Sort by" because it does the move once and
   then hands the list back. There is nothing left switched on afterwards. */
function finSortSel(kind){
  return '<label class="ssel"><span class="sr">Reorder the '+
    (kind==='jobs'?'income':'cost')+' lines</span><select data-finsort="'+E(kind)+'">'+
    '<option value="">Reorder...</option>'+
    finSortOpts(kind).map(function(o){
      return '<option value="'+E(o[0])+'">'+E(o[1])+'</option>';}).join('')+
    '</select></label>';
}
function finSortBy(kind,how){
  var a=finList(kind), mode=S.fin.mode||'real';
  if(!a||a.length<2) return false;
  var amt=function(x){return Math.abs(Number(x[mode])||0);};
  var nm=function(x){return String(x.name||'').toLowerCase();};
  var who=function(x){return String(x.who===EVERYONE?'￿':WHO(x.who)).toLowerCase();};
  var sect=function(x){return String(x.section||'￿').toLowerCase();};
  var cmp={
    big:function(x,y){return amt(y)-amt(x)||nm(x).localeCompare(nm(y));},
    small:function(x,y){return amt(x)-amt(y)||nm(x).localeCompare(nm(y));},
    az:function(x,y){return nm(x).localeCompare(nm(y));},
    who:function(x,y){return who(x).localeCompare(who(y))||amt(y)-amt(x);},
    sect:function(x,y){return sect(x).localeCompare(sect(y))||amt(y)-amt(x);},
    on:function(x,y){return (finLive(y)?1:0)-(finLive(x)?1:0)||amt(y)-amt(x);}
  }[how];
  if(!cmp) return false;
  var was=a.map(function(x){return x.id;}).join('|');
  a.sort(cmp);
  if(a.map(function(x){return x.id;}).join('|')===was) return false;
  save();
  return true;
}

/* ---- wiring ---- */
function wireReorder(){
  $$('[data-grip]').forEach(function(g){
    g.addEventListener('pointerdown',finDragStart);
    g.addEventListener('keydown',finGripKey);
    /* A grip is for grabbing, not for following a link somewhere. */
    g.addEventListener('click',function(e){e.preventDefault();});
  });
  $$('[data-finsort]').forEach(function(sel){
    sel.addEventListener('change',function(){
      var kind=this.dataset.finsort, how=this.value;
      this.value='';
      if(!how) return;
      if(finSortBy(kind,how)){
        reroute();
        var lbl='';
        FINSORTS.forEach(function(o){if(o[0]===how)lbl=o[1].toLowerCase();});
        toast((kind==='jobs'?'Income':'Costs')+' now in order: '+lbl);
      } else toast('Already in that order');
    });
  });
}
"""
