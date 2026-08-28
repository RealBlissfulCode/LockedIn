# -*- coding: utf-8 -*-
APP_CSS = """
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
--navy:#0A1A2F;--deep:#0F2947;--steel:#164272;--azure:#2680EB;--sky:#7FC4FF;
--ice:#EAF2FB;--mist:#F6F9FC;--line:#D3E0EE;--ink:#0D1826;--mut:#5D7186;
--good:#1B8A5A;--warn:#C4562F;--gold:#E0A80D;
--r:12px;--sh:0 1px 3px rgba(10,26,47,.07),0 6px 18px rgba(10,26,47,.05);
--shL:0 8px 30px rgba(10,26,47,.14);
--ease:cubic-bezier(.22,.61,.36,1);
}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--mist);padding-bottom:78px}
a{color:var(--azure);text-decoration:none}
h1,h2,h3,h4{margin:0;line-height:1.2;letter-spacing:-.4px}
button,input,select,textarea{font:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 18px}

/* ---------- top bar ---------- */
.top{position:sticky;top:0;z-index:60;background:rgba(10,26,47,.97);
backdrop-filter:saturate(180%) blur(10px);color:#fff}
.topin{max-width:1240px;margin:0 auto;padding:11px 18px;display:flex;align-items:center;gap:16px}
.brand{font-weight:800;font-size:16px;letter-spacing:-.5px;color:#fff;white-space:nowrap}
.brand em{font-style:normal;color:var(--sky)}
.tabs{display:flex;gap:3px;margin-left:auto;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{background:none;border:0;color:#A9C6E4;font-weight:600;font-size:13px;padding:8px 14px;
border-radius:999px;cursor:pointer;white-space:nowrap;transition:.2s var(--ease)}
.tab:hover{color:#fff;background:rgba(255,255,255,.09)}
.tab.on{background:var(--azure);color:#fff}
.whoswitch{display:flex;background:rgba(255,255,255,.1);border-radius:999px;padding:3px;gap:2px}
.whoswitch button{background:none;border:0;color:#A9C6E4;font-weight:700;font-size:12px;
padding:6px 12px;border-radius:999px;cursor:pointer;transition:.2s var(--ease)}
.whoswitch button.on{background:#fff;color:var(--navy)}

/* ---------- bottom bar (phone) ---------- */
.btmnav{display:none;position:fixed;bottom:0;left:0;right:0;z-index:70;background:#fff;
border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom))}
.btmnav button{flex:1;background:none;border:0;padding:7px 2px;color:var(--mut);font-size:10px;
font-weight:700;letter-spacing:.2px;cursor:pointer;display:flex;flex-direction:column;
align-items:center;gap:3px}
.btmnav button.on{color:var(--azure)}
.btmnav svg{width:21px;height:21px}

/* ---------- page ---------- */
.page{animation:fade .34s var(--ease)}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.phead{padding:26px 0 16px}
.phead h1{font-size:30px}
.phead p{color:var(--mut);margin:7px 0 0;max-width:70ch}
.sec{margin:26px 0}
.sec>h2{font-size:19px;margin-bottom:4px}
.sec>.sub{color:var(--mut);font-size:13.5px;margin:0 0 13px}

.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh)}
.pad{padding:18px 20px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.spread{display:flex;justify-content:space-between;align-items:center;gap:10px}
.muted{color:var(--mut)}.sm{font-size:13px}.xs{font-size:11.5px}
.right{margin-left:auto}

/* ---------- buttons ---------- */
.b{border:1px solid var(--azure);background:var(--azure);color:#fff;font-weight:600;font-size:13.5px;
padding:9px 16px;border-radius:9px;cursor:pointer;transition:.2s var(--ease);display:inline-flex;
align-items:center;gap:7px;justify-content:center}
.b:hover{background:#1668C8;border-color:#1668C8;transform:translateY(-1px)}
.b:active{transform:none}
.b.o{background:#fff;color:var(--steel);border-color:var(--line)}
.b.o:hover{background:var(--ice);border-color:var(--azure);color:var(--navy)}
.b.s{padding:6px 11px;font-size:12px;border-radius:7px}
.b.dz{border-color:#E5B4A4;color:var(--warn);background:#fff}
.b:disabled{opacity:.45;cursor:not-allowed;transform:none}

/* ---------- fields ---------- */
.f{display:block;margin-bottom:12px}
.f>span{display:block;font-size:10px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase;
color:var(--mut);margin-bottom:5px}
.f input,.f select,.f textarea{width:100%;padding:10px 12px;border:1px solid var(--line);
border-radius:9px;background:#fff;color:var(--ink);font-weight:500;transition:.15s var(--ease)}
.f input:focus,.f select:focus,.f textarea:focus{outline:0;border-color:var(--azure);
box-shadow:0 0 0 3px rgba(38,128,235,.15)}
.f textarea{resize:vertical;line-height:1.5}
.fr{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}

/* ---------- stat tiles ---------- */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:1px;
background:var(--line);border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.stat{background:#fff;padding:14px 12px;text-align:center}
.stat b{display:block;font-size:22px;letter-spacing:-.8px;color:var(--navy);line-height:1.05}
.stat span{display:block;font-size:9.5px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase;
color:var(--mut);margin-top:5px}
.stat.hero{background:var(--navy)}.stat.hero b{color:#fff;font-size:27px}.stat.hero span{color:var(--sky)}
.stat.acc{background:var(--azure)}.stat.acc b{color:#fff;font-size:27px}.stat.acc span{color:#D3E7FF}

/* ---------- progress ---------- */
.bar{height:8px;background:var(--ice);border-radius:99px;overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;border-radius:99px;transition:width .5s var(--ease)}
.pk{background:var(--azure)}.pp{background:var(--good)}.pc{background:var(--gold)}.pf{background:#8B6FD4}
.mrow{margin-bottom:11px}
.mrow .spread{font-size:12.5px;font-weight:700}
.mrow .spread em{font-style:normal;color:var(--mut);font-weight:600}

/* ---------- recipe card ---------- */
.rc{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;
cursor:pointer;transition:.24s var(--ease);display:flex;flex-direction:column;box-shadow:var(--sh)}
.rc:hover{transform:translateY(-3px);box-shadow:var(--shL);border-color:#B9D2EA}
.rcart{height:126px;position:relative;display:flex;align-items:center;justify-content:center;
overflow:hidden}
.rcart img{width:100%;height:100%;object-fit:cover}
.rcart .ring{position:absolute;right:11px;bottom:9px}
.rcbadge{position:absolute;left:10px;top:10px;background:rgba(10,26,47,.82);color:#fff;
font-size:10px;font-weight:800;letter-spacing:.9px;padding:3px 8px;border-radius:5px}
.rcb{padding:12px 13px 13px;display:flex;flex-direction:column;flex:1}
.rcn{font-size:14.5px;font-weight:700;color:var(--navy);line-height:1.28;margin-bottom:6px}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:9px}
.chip{font-size:10px;font-weight:700;padding:3px 7px;border-radius:5px;background:var(--ice);
color:var(--steel);letter-spacing:.2px;white-space:nowrap}
.chip.t{background:#EAF6EF;color:var(--good)}
.chip.d1{background:#E8F5EC;color:var(--good)}
.chip.d2{background:#FDF3E0;color:#96690B}
.chip.d3{background:#FBECE7;color:var(--warn)}
.chip.p{background:#F0F4F8;color:var(--mut);font-family:ui-monospace,Menlo,monospace}
.rcm{display:grid;grid-template-columns:repeat(4,1fr);gap:3px;margin-top:auto}
.rcm div{background:var(--mist);border-radius:6px;padding:6px 2px;text-align:center}
.rcm b{display:block;font-size:12.5px;color:var(--navy)}
.rcm span{font-size:8.5px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:var(--mut)}
.fav{position:absolute;right:9px;top:8px;width:30px;height:30px;border-radius:50%;border:0;
background:rgba(255,255,255,.93);color:#B9C8D8;font-size:15px;cursor:pointer;line-height:1;
display:flex;align-items:center;justify-content:center;transition:.2s var(--ease);z-index:2}
.fav:hover{transform:scale(1.12)}.fav.on{color:var(--gold)}

/* ---------- detail ---------- */
.dhero{border-radius:var(--r);overflow:hidden;position:relative;min-height:190px;
display:flex;align-items:flex-end;color:#fff;padding:22px;box-shadow:var(--sh)}
.dhero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dhero .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,26,47,.93),rgba(10,26,47,.28))}
.dhero .in{position:relative}
.dhero h1{font-size:27px;margin-bottom:8px}
.ing{list-style:none;margin:0;padding:0}
.ing li{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--ice);font-size:14px;
align-items:baseline}
.ing b{color:var(--navy);min-width:74px;font-variant-numeric:tabular-nums}
.ing .c{margin-left:auto;color:var(--mut);font-size:12px;font-variant-numeric:tabular-nums}
ol.stp{margin:0;padding-left:20px}
ol.stp li{margin-bottom:11px;line-height:1.6}
ol.stp li::marker{color:var(--azure);font-weight:800}

/* ---------- table ---------- */
table{border-collapse:collapse;width:100%;font-size:13.5px}
th{background:var(--navy);color:#fff;text-align:left;font-size:10.5px;letter-spacing:.9px;
text-transform:uppercase;padding:9px 10px;font-weight:700}
td{padding:8px 10px;border-bottom:1px solid var(--ice)}
tbody tr:hover td{background:var(--mist)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--r);border:1px solid var(--line);background:#fff}

/* ---------- calendar ---------- */
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:5px}
.cal .dow{text-align:center;font-size:10px;font-weight:800;color:var(--mut);letter-spacing:.8px;padding:5px 0}
.day{aspect-ratio:1;border:1px solid var(--line);border-radius:9px;background:#fff;padding:5px;
cursor:pointer;display:flex;flex-direction:column;transition:.18s var(--ease);position:relative}
.day:hover{border-color:var(--azure);transform:translateY(-2px)}
.day.out{opacity:.32}
.day.today{border-color:var(--azure);border-width:2px}
.day.sel{background:var(--navy);border-color:var(--navy)}
.day.sel .dn,.day.sel .dk{color:#fff}
.dn{font-size:12px;font-weight:700;color:var(--navy)}
.dk{font-size:9.5px;color:var(--mut);margin-top:auto;font-weight:700}
.dots{display:flex;gap:2px;margin-top:2px}
.dot{width:5px;height:5px;border-radius:50%;background:var(--azure)}
.dot.w{background:var(--good)}

/* ---------- grocery ---------- */
.gitem{display:flex;align-items:center;gap:11px;padding:9px 12px;border-bottom:1px solid var(--ice)}
.gitem:last-child{border-bottom:0}
.gitem.done{opacity:.45}
.gitem.done .gn{text-decoration:line-through}
.gitem input[type=checkbox]{width:19px;height:19px;accent-color:var(--azure);flex:none;cursor:pointer}
.gn{flex:1;min-width:0;font-size:14px;font-weight:600;color:var(--navy)}
.gq{font-size:12px;color:var(--mut)}
.gp{font-variant-numeric:tabular-nums;font-weight:700;color:var(--good);font-size:13px}
.aisle{background:var(--navy);color:#fff;padding:9px 14px;font-size:11px;font-weight:800;
letter-spacing:1.1px;text-transform:uppercase;display:flex;justify-content:space-between}
.aisle span{color:var(--sky)}

/* ---------- modal ---------- */
.mask{position:fixed;inset:0;background:rgba(10,26,47,.55);backdrop-filter:blur(3px);z-index:200;
display:flex;align-items:center;justify-content:center;padding:18px;animation:fade .2s var(--ease)}
.modal{background:#fff;border-radius:16px;max-width:560px;width:100%;max-height:86vh;
display:flex;flex-direction:column;box-shadow:0 24px 60px rgba(0,0,0,.3);
animation:pop .28s var(--ease)}
@keyframes pop{from{opacity:0;transform:scale(.95) translateY(14px)}to{opacity:1;transform:none}}
.mhead{padding:17px 20px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;
align-items:center}
.mhead h3{font-size:17px}
.mbody{padding:18px 20px;overflow-y:auto}
.mfoot{padding:14px 20px;border-top:1px solid var(--line);display:flex;gap:9px;justify-content:flex-end}
.x{border:0;background:var(--ice);width:31px;height:31px;border-radius:50%;cursor:pointer;
color:var(--mut);font-size:17px;line-height:1}
.pickrow{display:flex;align-items:center;gap:11px;padding:10px;border-radius:9px;cursor:pointer;
border:1px solid transparent}
.pickrow:hover{background:var(--ice);border-color:var(--line)}
.toast{position:fixed;left:50%;bottom:88px;transform:translateX(-50%);background:var(--navy);
color:#fff;padding:11px 20px;border-radius:99px;font-size:13.5px;font-weight:600;z-index:300;
box-shadow:var(--shL);animation:pop .25s var(--ease)}

/* ---------- misc ---------- */
.pill{display:inline-block;background:var(--ice);color:var(--steel);border-radius:99px;
padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer;border:1px solid transparent;
transition:.18s var(--ease)}
.pill:hover{border-color:var(--azure)}
.pill.on{background:var(--azure);color:#fff}
.note{background:var(--ice);border-left:3px solid var(--azure);border-radius:0 9px 9px 0;
padding:13px 16px;font-size:13.5px;margin:13px 0}
.note b{color:var(--navy)}
.empty{text-align:center;padding:38px 18px;color:var(--mut)}
details{background:#fff;border:1px solid var(--line);border-radius:var(--r);margin-bottom:9px;
overflow:hidden}
summary{padding:14px 18px;cursor:pointer;font-weight:700;color:var(--navy);list-style:none;
display:flex;justify-content:space-between;align-items:center}
summary::-webkit-details-marker{display:none}
summary:after{content:"+";color:var(--azure);font-size:19px;font-weight:400}
details[open] summary:after{content:"\\2212"}
details .dc{padding:0 18px 18px;border-top:1px solid var(--ice);padding-top:14px}
details p{margin:0 0 10px}

@media (max-width:820px){
  .wrap{padding:0 14px}
  body{padding-bottom:74px}
  .tabs{display:none}
  .btmnav{display:flex}
  .phead h1{font-size:24px}
  .phead{padding:18px 0 12px}
  .g2,.g3{grid-template-columns:1fr}
  .grid>*{flex:1 1 100%}
  .fr>*{flex:1 1 100%}
  .g4{grid-template-columns:1fr 1fr}
  .stats{grid-template-columns:repeat(3,1fr)}
  .dhero h1{font-size:21px}
  .cal{gap:3px}
  .day{padding:3px;border-radius:7px}
  .topin{padding:9px 14px;gap:10px}
  .brand{font-size:14px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

/* ---------- flex fallbacks for engines without CSS grid ---------- */
.stats{display:flex;flex-wrap:wrap}
.stat{flex:1 1 96px}
.grid{display:flex;flex-wrap:wrap}
.grid>*{flex:1 1 300px;min-width:0}
.g3>*{flex:1 1 240px}.g4>*{flex:1 1 190px}
.cal{display:flex;flex-wrap:wrap}
.cal>*{flex:0 0 14.28%;max-width:14.28%}
.fr{display:flex;flex-wrap:wrap}
.fr>*{flex:1 1 150px}
@supports (display:grid){
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr))}
  .grid{display:grid}
  .grid>*{min-width:0}
  .g2{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
  .g3{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
  .g4{grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
  .cal{display:grid;grid-template-columns:repeat(7,1fr)}
  .cal>*{max-width:none}
  .fr{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
}
</style>
"""
