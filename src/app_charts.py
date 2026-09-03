# -*- coding: utf-8 -*-
APP_CHARTS = r"""
/* ============================================================
   CHARTS  -  hand rolled, no library, no canvas.

   Two techniques, picked per chart rather than uniformly:

   * Columns, stacks and waterfalls are plain HTML. A div with a percentage
     height is already a bar; it inherits the theme variables, rounds its
     corners properly, and its labels are real text at a real font size
     instead of glyphs that grow with the viewBox.
   * The donut and the projection line are SVG, because HTML cannot draw an
     arc or a polyline. Neither carries text, so nothing scales badly.

   Every function is pure: numbers in, markup out, so a view can call one in
   the middle of a template string. Motion is entirely in CSS, which means the
   one prefers-reduced-motion rule at the bottom of the stylesheet switches all
   of it off, and the static state of every chart is already its final state.
   ============================================================ */

function chNum(n){n=Number(n);return isFinite(n)?Math.round(n*100)/100:0;}
function chPct(v,max){return max>0?Math.max(0,Math.min(100,v/max*100)):0;}
function chEmpty(msg){return '<div class="cempty">'+E(msg)+'</div>';}
/* Six accent classes, cycled. Sections outnumber them eventually and that is
   fine: adjacent slices are what have to differ, not distant ones. */
function chTone(i){return 'ct'+(i%6+1);}

/* ---------------- columns ----------------
   spec.max     the value one full-height bar represents
   spec.cols[]  {label, sub, subCls, bars:[{v, base, cls, tip}]}
   A bar with a base sits that far off the floor, which is all a waterfall is.
   Bars inside one column share the width evenly unless one asks to be wide. */
function chartCols(spec){
  var cols=spec.cols||[]; if(!cols.length) return chEmpty(spec.empty||'Nothing to draw yet.');
  var max=spec.max||0, h=spec.h||150, k=0;
  var body=cols.map(function(c,ci){
    var bars=c.bars||[], n=bars.length;
    var inner=bars.map(function(b,bi){
      var w=100/n, l=w*bi+(n>1?2:8), r=100-(w*(bi+1))+(n>1?2:8);
      var hp=chPct(Math.abs(b.v),max), bp=chPct(b.base||0,max);
      k++;
      return '<i class="cb '+(b.cls||'ct1')+'" style="--l:'+chNum(l)+'%;--r:'+chNum(r)+'%;'+
        '--h:'+chNum(Math.max(hp,hp>0?0.8:0))+'%;--b:'+chNum(bp)+'%;--d:'+(k*0.045).toFixed(3)+'s"'+
        (b.tip?' title="'+E(b.tip)+'"':'')+'></i>';
    }).join('');
    return '<div class="ccol">'+
      '<div class="cstack" style="--ch:'+h+'px">'+inner+'</div>'+
      '<div class="clab">'+E(c.label)+'</div>'+
      (c.sub?'<div class="csub '+(c.subCls||'')+'">'+E(c.sub)+'</div>':'')+
      '</div>';
  }).join('');
  return '<div class="cchart">'+body+'</div>';
}

/* ---------------- donut ----------------
   Each slice is one circle with a dash the length of its share and an offset
   equal to everything before it. pathLength="100" turns the circumference into
   percent so none of that needs the radius. */
function chartDonut(slices,top,bottom){
  var live=(slices||[]).filter(function(s){return s.v>0;});
  var tot=live.reduce(function(a,s){return a+s.v;},0);
  if(!tot) return chEmpty('Nothing counted right now.');
  var acc=0;
  var arcs=live.map(function(s,i){
    var len=s.v/tot*100, off=-acc; acc+=len;
    return '<circle class="cdseg '+(s.cls||chTone(i))+'" cx="60" cy="60" r="47" pathLength="100" '+
      'style="--len:'+chNum(len)+';--d:'+(i*0.07).toFixed(2)+'s;stroke-dashoffset:'+chNum(off)+'">'+
      (s.label?'<title>'+E(s.label)+'</title>':'')+'</circle>';
  }).join('');
  return '<div class="cdonut"><svg viewBox="0 0 120 120" role="img" aria-label="Breakdown">'+
    '<circle class="cdtrack" cx="60" cy="60" r="47"></circle>'+
    '<g transform="rotate(-90 60 60)">'+arcs+'</g></svg>'+
    '<div class="cdmid"><b>'+E(top)+'</b><span>'+E(bottom)+'</span></div></div>';
}

/* ---------------- projection line ----------------
   pts are plain numbers. A zero line is drawn whenever the series crosses it,
   because the whole point of the chart is where that crossing happens. */
function chartLine(pts,opts){
  opts=opts||{};
  var v=(pts||[]).map(function(x){return Number(x)||0;});
  if(v.length<2) return chEmpty('Not enough to project yet.');
  var W=600,H=170,PL=10,PR=10,PT=12,PB=12;
  var mn=Math.min.apply(null,v), mx=Math.max.apply(null,v);
  if(opts.zero!==false){mn=Math.min(mn,0);mx=Math.max(mx,0);}
  if(mx===mn){mx=mn+1;}
  var pad=(mx-mn)*0.08; mn-=pad; mx+=pad;
  var X=function(i){return PL+(W-PL-PR)*(v.length<2?0:i/(v.length-1));};
  var Y=function(y){return PT+(H-PT-PB)*(1-(y-mn)/(mx-mn));};
  var d='',i;
  for(i=0;i<v.length;i++){d+=(i?' L':'M')+chNum(X(i))+' '+chNum(Y(v[i]));}
  var area=d+' L'+chNum(X(v.length-1))+' '+chNum(Y(Math.max(mn,0)))+
           ' L'+chNum(X(0))+' '+chNum(Y(Math.max(mn,0)))+' Z';
  var zero=(mn<0&&mx>0)?'<line class="czero" x1="'+PL+'" x2="'+(W-PR)+'" y1="'+chNum(Y(0))+
    '" y2="'+chNum(Y(0))+'"></line>':'';
  var dots=v.map(function(y,j){
    return '<circle class="cdot" cx="'+chNum(X(j))+'" cy="'+chNum(Y(y))+'" r="3.4" '+
      'style="--d:'+(0.35+j*0.045).toFixed(3)+'s"></circle>';}).join('');
  return '<svg class="cline'+(opts.neg?' neg':'')+'" viewBox="0 0 '+W+' '+H+'" role="img" '+
    'aria-label="'+E(opts.label||'Projection')+'">'+
    '<defs><linearGradient id="cgFill" x1="0" y1="0" x2="0" y2="1">'+
    '<stop class="cgs0" offset="0"></stop><stop class="cgs1" offset="1"></stop>'+
    '</linearGradient></defs>'+
    zero+'<path class="carea" d="'+area+'"></path>'+
    '<path class="cpath" pathLength="1" d="'+d+'"></path>'+dots+'</svg>';
}

/* ---------------- legend rows ----------------
   The legend is where the toggles live on the money pages, so it takes raw
   markup for the control rather than owning one. */
function chartLegend(items){
  return '<div class="cleg">'+(items||[]).map(function(it){
    return '<div class="clrow'+(it.off?' off':'')+'">'+
      '<span class="cdotc '+(it.cls||'ct1')+'"></span>'+
      '<span class="cln">'+E(it.label)+'</span>'+
      '<b class="clv">'+E(it.value)+'</b>'+
      (it.pct!=null?'<span class="clp">'+E(it.pct)+'</span>':'')+
      (it.ctrl||'')+'</div>';}).join('')+'</div>';
}

/* ---------------- count up ----------------
   Big money numbers roll from zero on the way in. The element already holds
   its final text, so the animation only ever borrows it and hands it back;
   if motion is off, or a frame is dropped, what is on screen is the truth. */
function chReduced(){
  try{return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);}
  catch(e){return false;}
}
function countUp(root){
  var els=$$('[data-cv]',root||document);
  if(!els.length||chReduced()||!window.requestAnimationFrame) return;
  var fin=els.map(function(el){return el.textContent;});
  var t0=null, DUR=680;
  function frame(ts){
    if(t0===null)t0=ts;
    var k=Math.min(1,(ts-t0)/DUR), e=1-Math.pow(1-k,3);
    for(var i=0;i<els.length;i++){
      if(k>=1){els[i].textContent=fin[i];continue;}
      var to=parseFloat(els[i].getAttribute('data-cv'));
      if(!isFinite(to)){els[i].textContent=fin[i];continue;}
      var f=els[i].getAttribute('data-cf')||'M', val=to*e;
      els[i].textContent = f==='pct' ? Math.round(val)+'%'
        : f==='n' ? N(val)
        : f==='h' ? (Math.round(val*10)/10)+'h'
        : M(val);
    }
    if(k<1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
"""
