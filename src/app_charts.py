# -*- coding: utf-8 -*-
APP_CHARTS = r"""
/* ============================================================
   CHARTS. Hand rolled. No library, no canvas.

   Most of them are plain HTML. A div with a percentage height is already a
   bar, it picks up the theme variables for free, and its labels are real text
   at a real size instead of glyphs that grow with the viewBox. Only the donut
   and the projection line are SVG, because HTML cannot draw an arc or a
   polyline. Neither of those two carries any text.

   Every function takes numbers and returns markup, so a view can call one in
   the middle of a template string. All the motion is in CSS. That way the
   prefers-reduced-motion rule at the bottom of the stylesheet kills the lot in
   one place, and every chart already sits at its finished state before the
   keyframes touch it.
   ============================================================ */

function chNum(n){n=Number(n);return isFinite(n)?Math.round(n*100)/100:0;}
function chPct(v,max){return max>0?Math.max(0,Math.min(100,v/max*100)):0;}
function chEmpty(msg){return '<div class="cempty">'+E(msg)+'</div>';}
/* Six accent classes on a loop. Sections will outrun them eventually and that
   is fine. What matters is that touching slices differ, not distant ones. */
function chTone(i){return 'ct'+(i%6+1);}

/* Round a scale up to something a person would actually write down, so the
   top gridline reads $7,000 rather than $6,847. */
function chNice(v){
  if(!(v>0)) return 1;
  var p=Math.pow(10,Math.floor(Math.log(v)/Math.LN10));
  var f=v/p, step=f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10;
  return step*p;
}
/* The scale down the left edge. Four lines is enough to read a bar against
   and few enough that they stay behind the bars instead of competing. */
function chAxis(max,h,fmt){
  var n=4, out='', i;
  for(i=n;i>=0;i--)
    out+='<span style="bottom:'+chNum(i/n*100)+'%">'+E((fmt||M)(max*i/n))+'</span>';
  return '<div class="cyax" style="--ch:'+h+'px">'+out+'</div>';
}

/* ---------------- columns ----------------
   spec.max     what one full height bar is worth
   spec.cols[]  {label, sub, subCls, bars:[{v, base, cls, tip}]}
   Give a bar a base and it floats that far off the floor, which is the whole
   trick behind a waterfall. Bars in one column split the width evenly.

   Bar width comes from the column count. Fix the inset and a three column
   chart draws slabs on a monitor while an eight column one draws threads.

   spec.connect adds the line a waterfall needs. Without it you see six
   floating rectangles. With it you see one balance getting cut down. The line
   sits at the top of each bar and runs back into the gutter so it lands where
   the bar before it finished. */
function chartCols(spec){
  var cols=spec.cols||[]; if(!cols.length) return chEmpty(spec.empty||'Nothing to draw yet.');
  /* Every bar at zero is not a chart, it is a tall empty box. Say so instead,
     which matters most on a phone where that box is the whole screen. */
  var anyValue=cols.some(function(c){
    return (c.bars||[]).some(function(b){return Math.abs(b.v||0)>0;});});
  if(!anyValue) return chEmpty(spec.empty||'Nothing to draw yet.');
  /* The scale is rounded up before anything is measured against it, so bars,
     gridlines and the numbers on the left are all reading off one ruler. */
  var h=spec.h||150, k=0;
  var max=spec.axis===false?(spec.max||0):chNice(spec.max||0);
  var n0=cols.length;
  var pad=n0<=2?26:n0<=3?20:n0<=4?15:n0<=6?9:n0<=9?5:3;
  var body=cols.map(function(c,ci){
    var bars=c.bars||[], n=bars.length;
    var gutter=n>1?2:0;
    var inner=bars.map(function(b,bi){
      var w=(100-pad*2)/n;
      var l=pad+w*bi+(bi?gutter:0), r=100-(pad+w*(bi+1))+(bi<n-1?gutter:0);
      var hp=chPct(Math.abs(b.v),max), bp=chPct(b.base||0,max);
      k++;
      return '<i class="cb '+(b.cls||'ct1')+'" style="--l:'+chNum(l)+'%;--r:'+chNum(r)+'%;'+
        '--h:'+chNum(Math.max(hp,hp>0?0.8:0))+'%;--b:'+chNum(bp)+'%;--d:'+(k*0.045).toFixed(3)+'s"'+
        (b.tip?' tabindex="0" role="img" data-tip="'+E(b.tip)+'" aria-label="'+E(b.tip)+'"':'')+
        '></i>';
    }).join('');
    /* The connector belongs to the column it leads into, so the first one has
       nothing to join and is skipped. */
    var conn='';
    if(spec.connect&&ci>0&&bars.length){
      var top=chPct(Math.abs(bars[0].v)+(bars[0].base||0),max);
      conn='<u class="cconn" style="--y:'+chNum(top)+'%;--r:'+chNum(100-pad)+'%;--d:'+
        (ci*0.045+0.1).toFixed(3)+'s"></u>';
    }
    return '<div class="ccol">'+
      '<div class="cstack" style="--ch:'+h+'px">'+conn+inner+'</div>'+
      '<div class="clab">'+E(c.label)+'</div>'+
      (c.sub?'<div class="csub '+(c.subCls||'')+'">'+E(c.sub)+'</div>':'')+
      '</div>';
  }).join('');
  var ax=spec.axis===false?'':chAxis(max,h,spec.fmt);
  /* Past six columns there is no room on a phone for a figure under every bar,
     and half a figure overlapping the next one is worse than none. The scale
     on the left still gives the size, and a tap still gives the exact number. */
  return '<div class="cchart'+(spec.connect?' wf':'')+(ax?' ax':'')+
    (n0>6?' many':'')+'">'+ax+body+'</div>';
}

/* ---------------- donut ----------------
   One circle per slice. The dash is as long as that slice's share and the
   offset is everything ahead of it. pathLength="100" turns the circumference
   into percent, so the radius never enters the maths. */
function chartDonut(slices,top,bottom,key){
  var live=(slices||[]).filter(function(s){return s.v>0;});
  var tot=live.reduce(function(a,s){return a+s.v;},0);
  if(!tot) return chEmpty('Nothing counted right now.');
  var acc=0; key=key||chRingKey();
  var arcs=live.map(function(s,i){
    var len=s.v/tot*100, off=-acc; acc+=len;
    var pct=Math.round(s.v/tot*100)+'%';
    return '<circle class="cdseg '+(s.cls||chTone(i))+'" cx="60" cy="60" r="47" pathLength="100" '+
      'data-donut="'+key+'" data-di="'+i+'" '+
      'data-dv="'+E(M(s.v))+'" data-dl="'+E(s.label||'')+'" data-dp="'+pct+'" '+
      'style="--len:'+chNum(len)+';--d:'+(i*0.07).toFixed(2)+'s;stroke-dashoffset:'+chNum(off)+'">'+
      (s.label?'<title>'+E(s.label)+' - '+pct+'</title>':'')+'</circle>';
  }).join('');
  /* The middle holds the total until you point at a slice, and then it holds
     that slice. Reading a share off a ring is guesswork otherwise. */
  return '<div class="cdonut" data-dring="'+key+'">'+
    '<svg viewBox="0 0 120 120" role="img" aria-label="Breakdown">'+
    '<circle class="cdtrack" cx="60" cy="60" r="47"></circle>'+
    '<g transform="rotate(-90 60 60)">'+arcs+'</g></svg>'+
    '<div class="cdmid"><b data-dtop="'+E(top)+'">'+E(top)+'</b>'+
    '<span data-dbot="'+E(bottom)+'">'+E(bottom)+'</span></div></div>';
}
/* Each ring on a page needs its own name so pointing at one does not light up
   the other, and its legend needs the same name to point back. */
var _ringN=0;
function chRingKey(){return 'r'+(++_ringN);}

/* ---------------- projection line ----------------
   pts are plain numbers. If the series crosses zero it gets a zero line, since
   where it crosses is the thing you actually want to see. */
function chartLine(pts,opts){
  opts=opts||{};
  var v=(pts||[]).map(function(x){return Number(x)||0;});
  if(v.length<2) return chEmpty('Not enough to project yet.');
  /* Room on the left for the scale, so the numbers sit in a gutter of their
     own rather than on top of the line they are describing. */
  var W=600,H=170,PL=58,PR=10,PT=12,PB=12;
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
      'tabindex="0" data-tip="'+E((opts.pt||function(k,val){
        return 'Month '+(k+1)+': '+M(val);})(j,y))+'" '+
      'style="--d:'+(0.35+j*0.045).toFixed(3)+'s"></circle>';}).join('');
  /* Three numbers up the side. Without them the line says the shape but not
     the size, and the size is the part you make decisions on. */
  var marks=[mx,(mx+mn)/2,mn].map(function(val,j){
    var gy=chNum(PT+(H-PT-PB)*j/2);
    return '<text class="clv2" x="'+(PL-9)+'" y="'+gy+'" dy="4">'+
      E((opts.fmt||M)(val))+'</text>'+
      '<line class="cgl" x1="'+PL+'" x2="'+(W-PR)+'" y1="'+gy+'" y2="'+gy+'"></line>';}).join('');
  return '<svg class="cline'+(opts.neg?' neg':'')+'" viewBox="0 0 '+W+' '+H+'" role="img" '+
    'aria-label="'+E(opts.label||'Projection')+'">'+marks+
    '<defs><linearGradient id="cgFill" x1="0" y1="0" x2="0" y2="1">'+
    '<stop class="cgs0" offset="0"></stop><stop class="cgs1" offset="1"></stop>'+
    '</linearGradient></defs>'+
    zero+'<path class="carea" d="'+area+'"></path>'+
    '<path class="cpath" pathLength="1" d="'+d+'"></path>'+dots+'</svg>';
}

/* ---------------- legend rows ----------------
   On the money pages the switches live in the legend, so a row takes raw
   markup for its control instead of building one itself. */
function chartLegend(items,ring){
  return '<div class="cleg">'+(items||[]).map(function(it,i){
    return '<div class="clrow'+(it.off?' off':'')+'"'+
      (ring?' data-dleg="'+E(ring)+'" data-di="'+i+'"':'')+'>'+
      '<span class="cdotc '+(it.cls||'ct1')+'"></span>'+
      '<span class="cln">'+E(it.label)+'</span>'+
      '<b class="clv">'+E(it.value)+'</b>'+
      (it.pct!=null?'<span class="clp">'+E(it.pct)+'</span>':'')+
      (it.ctrl||'')+'</div>';}).join('')+'</div>';
}

/* ---------------- pointing at a chart ----------------
   A title attribute is a desktop-only feature. It never appears for a thumb,
   which meant every number hidden behind one was unreachable on the device the
   charts get looked at on most. This puts the same text in a real element that
   a tap can summon and a tap elsewhere dismisses.

   One listener for every chart on the page, installed once. */
function chTipEl(){
  var t=document.getElementById('ctip');
  if(!t){t=document.createElement('div');t.id='ctip';t.className='ctip';
    t.setAttribute('role','status');document.body.appendChild(t);}
  return t;
}
function chTipShow(el,text){
  var t=chTipEl();
  t.textContent=text;
  t.classList.add('on');
  var r=el.getBoundingClientRect(), w=t.offsetWidth, h=t.offsetHeight;
  var x=r.left+r.width/2-w/2, y=r.top-h-9;
  /* Never off the edge, and never over the thing it is describing. */
  x=Math.max(8,Math.min(x,(window.innerWidth||0)-w-8));
  if(y<6) y=r.bottom+9;
  t.style.left=Math.round(x)+'px';
  t.style.top=Math.round(y+(window.pageYOffset||0))+'px';
}
function chTipHide(){
  var t=document.getElementById('ctip');
  if(t) t.classList.remove('on');
}
function chRingSet(key,i){
  var ring=document.querySelector('[data-dring="'+key+'"]');
  if(!ring) return;
  var mid=ring.querySelector('.cdmid b'), sub=ring.querySelector('.cdmid span');
  var seg=i==null?null:ring.querySelector('[data-donut="'+key+'"][data-di="'+i+'"]');
  ring.classList.toggle('picked',!!seg);
  $$('[data-donut="'+key+'"]').forEach(function(c){
    c.classList.toggle('on',!!seg&&c===seg);});
  $$('[data-dleg="'+key+'"]').forEach(function(r){
    r.classList.toggle('on',!!seg&&r.dataset.di===String(i));});
  if(mid) mid.textContent=seg?seg.dataset.dv:mid.dataset.dtop;
  if(sub) sub.textContent=seg?(seg.dataset.dl+' - '+seg.dataset.dp):sub.dataset.dbot;
}
function chartsWire(){
  var pick=function(t){return t&&t.closest?t.closest('[data-tip],[data-donut],[data-dleg]'):null;};
  var enter=function(e){
    var el=pick(e.target);
    if(!el){chTipHide();return;}
    if(el.hasAttribute('data-tip')) chTipShow(el,el.getAttribute('data-tip'));
    var key=el.getAttribute('data-donut')||el.getAttribute('data-dleg');
    if(key) chRingSet(key,+el.getAttribute('data-di'));
  };
  var leave=function(e){
    /* A finger leaves the moment it lifts. Honouring that would wipe the
       readout in the same instant it appeared, so on touch it stays until the
       next tap somewhere else puts it away. */
    if(e.pointerType&&e.pointerType!=='mouse') return;
    var el=pick(e.target);
    if(!el) return;
    chTipHide();
    var key=el.getAttribute('data-donut')||el.getAttribute('data-dleg');
    if(key) chRingSet(key,null);
  };
  document.addEventListener('pointerover',enter);
  document.addEventListener('pointerout',leave);
  document.addEventListener('focusin',enter);
  document.addEventListener('focusout',leave);
  /* A finger has no hover, so a tap does the pointing and the next tap
     anywhere else puts it back. */
  document.addEventListener('pointerdown',function(e){
    if(e.pointerType==='mouse') return;
    var el=pick(e.target);
    if(!el){chTipHide();
      $$('.cdonut[data-dring]').forEach(function(r){chRingSet(r.dataset.dring,null);});
      return;}
    enter(e);
  },true);
  window.addEventListener('scroll',chTipHide,true);
}

/* ---------------- count up ----------------
   Big money figures roll up from zero when a page draws. The element is
   already holding its final text, so this borrows it and hands it back. Drop a
   frame, or turn motion off, and what is on screen is still the real number. */
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
