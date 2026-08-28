# -*- coding: utf-8 -*-
APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
--ink:#14140F;--ink-2:#3E3E36;--ink-3:#6B6B5E;--ink-4:#9A9A8C;
--paper:#FBFAF7;--card:#FFFFFF;--sand:#F2EFE8;--line:#E3DFD5;--line-2:#D2CDBF;
--forest:#1F4D3A;--forest-2:#2C6B50;--moss:#E7EFE9;--clay:#B4522F;--amber:#C2860E;--plum:#5C4A78;
--r:14px;--r-s:9px;--r-l:22px;
--sh-1:0 1px 2px rgba(20,20,15,.05);
--sh-2:0 2px 6px rgba(20,20,15,.05),0 12px 28px -12px rgba(20,20,15,.16);
--sh-3:0 4px 12px rgba(20,20,15,.07),0 28px 56px -20px rgba(20,20,15,.26);
--ez:cubic-bezier(.2,.7,.3,1);
--ff:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
--fd:'Fraunces','Iowan Old Style',Georgia,serif;}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 15.5px/1.6 var(--ff);padding-bottom:84px;
background-image:radial-gradient(circle at 12% -8%,rgba(31,77,58,.055),transparent 46%),radial-gradient(circle at 92% 4%,rgba(194,134,14,.05),transparent 42%);
background-attachment:fixed}
a{color:var(--forest);text-decoration:none}
button,input,select,textarea{font:inherit;color:inherit}
h1,h2,h3,h4{margin:0;font-family:var(--fd);font-weight:600;letter-spacing:-.02em;line-height:1.12}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.lbl{font:700 10px/1 var(--ff);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-4)}
.top{position:sticky;top:0;z-index:60;background:rgba(251,250,247,.82);backdrop-filter:saturate(180%) blur(14px);-webkit-backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line)}
.topin{max-width:1180px;margin:0 auto;padding:13px 22px;display:flex;align-items:center;gap:20px}
.brand{font-family:var(--fd);font-weight:700;font-size:19px;letter-spacing:-.03em;color:var(--ink);white-space:nowrap;display:flex;align-items:center;gap:9px}
.brand:before{content:"";width:9px;height:9px;border-radius:50%;background:var(--forest);box-shadow:0 0 0 3px rgba(31,77,58,.14)}
.brand em{font-style:normal;color:var(--ink-3);font-weight:500}
.tabs{display:flex;gap:2px;margin-left:auto}
.tab{background:none;border:0;color:var(--ink-3);font-weight:600;font-size:13.5px;padding:8px 14px;border-radius:999px;cursor:pointer;transition:.2s var(--ez);white-space:nowrap}
.tab:hover{color:var(--ink);background:var(--sand)}
.tab.on{color:var(--forest);background:var(--moss)}
.whoswitch{display:flex;background:var(--sand);border:1px solid var(--line);border-radius:999px;padding:3px;gap:2px}
.whoswitch button{background:none;border:0;color:var(--ink-3);font-weight:600;font-size:12.5px;padding:6px 15px;border-radius:999px;cursor:pointer;transition:.22s var(--ez);white-space:nowrap}
.whoswitch button:hover{color:var(--ink)}
.whoswitch button.on{background:var(--card);color:var(--ink);box-shadow:var(--sh-1);font-weight:700}
.btmnav{display:none;position:fixed;left:0;right:0;bottom:0;z-index:70;background:rgba(251,250,247,.94);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:1px solid var(--line);padding:7px 4px calc(7px + env(safe-area-inset-bottom))}
.btmnav button{flex:1;background:none;border:0;padding:5px 2px;color:var(--ink-4);cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;font:700 9.5px/1 var(--ff);letter-spacing:.05em;transition:.18s var(--ez)}
.btmnav svg{width:21px;height:21px;stroke-width:1.7}
.btmnav button.on{color:var(--forest)}
.btmnav button.on svg{stroke-width:2.1}
.page{animation:rise .42s var(--ez)}
@keyframes rise{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
.phead{padding:38px 0 22px;max-width:66ch}
.phead h1{font-size:clamp(30px,4.4vw,46px);letter-spacing:-.035em}
.phead p{color:var(--ink-3);margin:11px 0 0;font-size:16.5px;line-height:1.55}
.sec{margin:38px 0}
.sec>h2{font-size:23px;letter-spacing:-.028em;margin-bottom:3px}
.sec>.sub{color:var(--ink-3);font-size:14px;margin:0 0 16px;max-width:70ch}
.rule{height:1px;background:var(--line);margin:34px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh-1)}
.pad{padding:22px 24px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.spread{display:flex;justify-content:space-between;align-items:center;gap:12px}
.muted{color:var(--ink-3)}.sm{font-size:13.5px}.xs{font-size:12px}
.right{margin-left:auto}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.stat{padding:18px 16px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-family:var(--fd);font-size:28px;font-weight:600;letter-spacing:-.035em;line-height:1;color:var(--ink);font-variant-numeric:tabular-nums}
.stat span{display:block;font:700 9.5px/1 var(--ff);letter-spacing:.15em;text-transform:uppercase;color:var(--ink-4);margin-top:8px}
.stat.acc{background:var(--forest)}
.stat.acc b{color:#fff;font-size:34px}
.stat.acc span{color:rgba(255,255,255,.62)}
.mrow{margin-bottom:15px}
.mrow:last-child{margin-bottom:0}
.mrow .spread{font-size:13px;font-weight:600;margin-bottom:7px}
.mrow .spread em{font-style:normal;color:var(--ink-3);font-weight:500;font-variant-numeric:tabular-nums}
.bar{height:5px;background:var(--sand);border-radius:99px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:99px;transition:width .7s var(--ez)}
.pk{background:var(--forest)}.pp{background:var(--forest-2)}.pc{background:var(--amber)}.pf{background:var(--plum)}
.b{border:1px solid var(--forest);background:var(--forest);color:#fff;font-weight:600;font-size:14px;padding:10px 19px;border-radius:999px;cursor:pointer;transition:.2s var(--ez);display:inline-flex;align-items:center;gap:8px;justify-content:center;box-shadow:var(--sh-1)}
.b:hover{background:var(--forest-2);border-color:var(--forest-2);transform:translateY(-1px);box-shadow:var(--sh-2)}
.b:active{transform:translateY(0)}
.b.o{background:var(--card);color:var(--ink);border-color:var(--line-2);box-shadow:none}
.b.o:hover{background:var(--sand);border-color:var(--ink-4)}
.b.s{padding:7px 13px;font-size:12.5px}
.b.dz{background:var(--card);color:var(--clay);border-color:#E5C7BB}
.b.dz:hover{background:#FBF0EB;border-color:var(--clay)}
.b:disabled{opacity:.42;cursor:not-allowed;transform:none}
.f{display:block;margin-bottom:15px}
.f>span{display:block;font:700 10px/1 var(--ff);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-4);margin-bottom:7px}
.f input,.f select,.f textarea{width:100%;padding:11px 13px;border:1px solid var(--line-2);border-radius:var(--r-s);background:var(--card);font-weight:500;transition:.16s var(--ez)}
.f input:focus,.f select:focus,.f textarea:focus{outline:0;border-color:var(--forest);box-shadow:0 0 0 3px rgba(31,77,58,.13)}
.f textarea{resize:vertical;line-height:1.55}
.fr{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(158px,1fr))}
.rc{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;cursor:pointer;transition:.28s var(--ez);display:flex;flex-direction:column;box-shadow:var(--sh-1)}
.rc:hover{transform:translateY(-4px);box-shadow:var(--sh-3);border-color:var(--line-2)}
.rcart{height:132px;position:relative;overflow:hidden;background:var(--sand)}
.rcart img{width:100%;height:100%;object-fit:cover;display:block;transition:.5s var(--ez)}
.rc:hover .rcart img{transform:scale(1.05)}
.rcart .ring{position:absolute;right:12px;bottom:11px}
.rcbadge{position:absolute;left:12px;top:12px;background:rgba(255,255,255,.94);color:var(--ink);font:700 9px/1 var(--ff);letter-spacing:.14em;padding:5px 9px;border-radius:5px;box-shadow:var(--sh-1)}
.rcb{padding:15px 16px 16px;display:flex;flex-direction:column;flex:1}
.rcn{font-family:var(--fd);font-size:17px;font-weight:600;letter-spacing:-.02em;line-height:1.22;color:var(--ink);margin-bottom:9px}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px}
.chip{font:600 11px/1 var(--ff);padding:5px 9px;border-radius:6px;background:var(--sand);color:var(--ink-2);white-space:nowrap;border:1px solid transparent}
.chip.t{background:var(--moss);color:var(--forest)}
.chip.d1{background:var(--moss);color:var(--forest)}
.chip.d2{background:#FBF2DE;color:#8A5F09}
.chip.d3{background:#F9EAE4;color:var(--clay)}
.chip.p{font-variant-numeric:tabular-nums}
.rcm{display:grid;grid-template-columns:repeat(4,1fr);margin-top:auto;border-top:1px solid var(--line);padding-top:12px}
.rcm div{text-align:center;border-right:1px solid var(--line)}
.rcm div:last-child{border-right:0}
.rcm b{display:block;font-family:var(--fd);font-size:16px;font-weight:600;color:var(--ink);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.rcm span{font:700 8.5px/1 var(--ff);letter-spacing:.13em;text-transform:uppercase;color:var(--ink-4);display:block;margin-top:4px}
.fav{position:absolute;right:11px;top:11px;width:32px;height:32px;border-radius:50%;border:0;background:rgba(255,255,255,.94);color:var(--ink-4);font-size:15px;cursor:pointer;line-height:1;display:flex;align-items:center;justify-content:center;transition:.22s var(--ez);z-index:2;box-shadow:var(--sh-1)}
.fav:hover{transform:scale(1.13)}
.fav.on{color:var(--amber)}
.dhero{border-radius:var(--r-l);overflow:hidden;position:relative;min-height:260px;display:flex;align-items:flex-end;color:#fff;padding:32px;box-shadow:var(--sh-2)}
.dhero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dhero .scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(14,14,10,.90) 0%,rgba(14,14,10,.42) 52%,rgba(14,14,10,.15) 100%)}
.dhero .in{position:relative;max-width:64ch}
.dhero h1{font-size:clamp(27px,4vw,41px);letter-spacing:-.032em;color:#fff;margin:9px 0 10px}
.dhero .chip,.dhero .chip.d1,.dhero .chip.d2,.dhero .chip.d3{background:rgba(255,255,255,.17);color:#fff}
.ing{list-style:none;margin:0;padding:0}
.ing li{display:flex;gap:13px;padding:11px 0;border-bottom:1px solid var(--line);font-size:14.5px;align-items:baseline}
.ing li:last-child{border-bottom:0}
.ing b{color:var(--ink);min-width:78px;font-variant-numeric:tabular-nums;font-weight:600}
.ing .c{margin-left:auto;color:var(--ink-4);font-size:12.5px;font-variant-numeric:tabular-nums}
ol.stp{margin:0;padding:0;list-style:none;counter-reset:s}
ol.stp li{counter-increment:s;position:relative;padding:0 0 20px 46px;line-height:1.68;font-size:15.5px}
ol.stp li:before{content:counter(s);position:absolute;left:0;top:-1px;width:29px;height:29px;border-radius:50%;background:var(--moss);color:var(--forest);font:700 13px/29px var(--ff);text-align:center}
ol.stp li:after{content:"";position:absolute;left:14px;top:33px;bottom:6px;width:1px;background:var(--line)}
ol.stp li:last-child{padding-bottom:0}
ol.stp li:last-child:after{display:none}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:var(--sand);color:var(--ink-3);text-align:left;font:700 9.5px/1 var(--ff);letter-spacing:.15em;text-transform:uppercase;padding:12px 14px;border-bottom:1px solid var(--line)}
td{padding:11px 14px;border-bottom:1px solid var(--line)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--paper)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:var(--r);background:var(--card)}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:7px}
.cal .dow{text-align:center;font:700 9.5px/1 var(--ff);letter-spacing:.14em;color:var(--ink-4);padding:7px 0}
.day{aspect-ratio:1;border:1px solid var(--line);border-radius:var(--r-s);background:var(--card);padding:8px;cursor:pointer;display:flex;flex-direction:column;transition:.2s var(--ez);position:relative}
.day:hover{border-color:var(--forest);transform:translateY(-2px);box-shadow:var(--sh-2)}
.day.out{opacity:0;pointer-events:none}
.day.today{border-color:var(--forest);box-shadow:inset 0 0 0 1px var(--forest)}
.day.sel{background:var(--forest);border-color:var(--forest)}
.day.sel .dn,.day.sel .dk{color:#fff}
.dn{font-family:var(--fd);font-size:15px;font-weight:600;color:var(--ink)}
.dk{font:600 10px/1 var(--ff);color:var(--ink-4);margin-top:auto;font-variant-numeric:tabular-nums}
.dots{display:flex;gap:3px;margin-top:4px}
.dot{width:5px;height:5px;border-radius:50%;background:var(--forest)}
.dot.w{background:var(--amber)}
.aisle{background:var(--ink);color:#fff;padding:11px 18px;font:700 10px/1 var(--ff);letter-spacing:.16em;text-transform:uppercase;display:flex;justify-content:space-between}
.aisle span{color:rgba(255,255,255,.6);font-variant-numeric:tabular-nums}
.gitem{display:flex;align-items:center;gap:13px;padding:12px 18px;border-bottom:1px solid var(--line)}
.gitem:last-child{border-bottom:0}
.gitem.done{opacity:.42}
.gitem.done .gn{text-decoration:line-through}
.gitem input[type=checkbox]{width:19px;height:19px;accent-color:var(--forest);flex:none;cursor:pointer}
.gn{flex:1;min-width:0;font-size:14.5px;font-weight:600;color:var(--ink)}
.gq{font-size:12px;color:var(--ink-4);font-weight:400;margin-top:2px}
.gp{font-variant-numeric:tabular-nums;font-weight:600;color:var(--forest);font-size:14px}
.mask{position:fixed;inset:0;background:rgba(20,20,15,.42);backdrop-filter:blur(5px);z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;animation:fadein .22s var(--ez)}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.modal{background:var(--card);border-radius:var(--r-l);max-width:580px;width:100%;max-height:86vh;display:flex;flex-direction:column;box-shadow:var(--sh-3);animation:pop .3s var(--ez);overflow:hidden}
@keyframes pop{from{opacity:0;transform:scale(.96) translateY(12px)}to{opacity:1;transform:none}}
.mhead{padding:20px 24px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
.mhead h3{font-size:19px}
.mbody{padding:22px 24px;overflow-y:auto}
.mfoot{padding:16px 24px;border-top:1px solid var(--line);display:flex;gap:10px;justify-content:flex-end;background:var(--paper)}
.x{border:0;background:var(--sand);width:32px;height:32px;border-radius:50%;cursor:pointer;color:var(--ink-3);font-size:17px;line-height:1;transition:.18s var(--ez)}
.x:hover{background:var(--line);color:var(--ink)}
.pickrow{display:flex;align-items:center;gap:13px;padding:12px;border-radius:var(--r-s);cursor:pointer;border:1px solid transparent;transition:.16s var(--ez)}
.pickrow:hover{background:var(--sand);border-color:var(--line)}
.toast{position:fixed;left:50%;bottom:96px;transform:translateX(-50%);background:var(--ink);color:var(--paper);padding:13px 22px;border-radius:999px;font-size:14px;font-weight:600;z-index:300;box-shadow:var(--sh-3);animation:pop .28s var(--ez)}
.pill{display:inline-block;background:var(--card);color:var(--ink-2);border-radius:999px;padding:7px 15px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid var(--line-2);transition:.18s var(--ez)}
.pill:hover{border-color:var(--forest);color:var(--forest)}
.pill.on{background:var(--forest);color:#fff;border-color:var(--forest)}
.note{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--forest);border-radius:0 var(--r-s) var(--r-s) 0;padding:16px 20px;font-size:14.5px;margin:16px 0;color:var(--ink-2)}
.note b{color:var(--ink);font-weight:600}
.empty{text-align:center;padding:56px 20px;color:var(--ink-4)}
.empty p{margin:0 0 6px}
details{background:var(--card);border:1px solid var(--line);border-radius:var(--r);margin-bottom:10px;overflow:hidden;transition:.2s var(--ez)}
details[open]{box-shadow:var(--sh-1)}
summary{padding:17px 22px;cursor:pointer;font-weight:600;font-size:15.5px;color:var(--ink);list-style:none;display:flex;justify-content:space-between;align-items:center;gap:14px}
summary::-webkit-details-marker{display:none}
summary:after{content:"";width:9px;height:9px;border-right:1.8px solid var(--ink-4);border-bottom:1.8px solid var(--ink-4);transform:rotate(45deg);flex:none;margin-top:-4px;transition:.24s var(--ez)}
details[open] summary:after{transform:rotate(-135deg);margin-top:2px}
details .dc{padding:2px 22px 20px;color:var(--ink-2)}
details .dc p{margin:0 0 12px}
details .dc p:last-child{margin-bottom:0}
details .dc ul{margin:0 0 12px;padding-left:20px}
@media (max-width:860px){
.wrap{padding:0 16px}
body{padding-bottom:78px}
.tabs{display:none}
.btmnav{display:flex}
.topin{padding:11px 16px;gap:12px}
.whoswitch{margin-left:auto}
.phead{padding:24px 0 14px}
.g2,.g3{grid-template-columns:1fr}
.g4{grid-template-columns:1fr 1fr}
.stats{grid-template-columns:repeat(2,1fr)}
.stat{border-bottom:1px solid var(--line)}
.stat:nth-child(odd){border-right:1px solid var(--line)}
.stat:nth-child(even){border-right:0}
.dhero{min-height:210px;padding:22px;border-radius:var(--r)}
.cal{gap:4px}
.day{padding:5px;border-radius:7px}
.pad{padding:18px}
ol.stp li{padding-left:40px}
}
@media (max-width:440px){.g4{grid-template-columns:1fr}.rcm b{font-size:14px}}
.stats{display:flex;flex-wrap:wrap}
.stat{flex:1 1 112px}
.grid{display:flex;flex-wrap:wrap}
.grid>*{flex:1 1 300px;min-width:0}
.g3>*{flex:1 1 250px}.g4>*{flex:1 1 200px}
.grid{align-items:stretch}
.cal{display:flex;flex-wrap:wrap}
.cal>*{flex:0 0 14.28%;max-width:14.28%}
.fr{display:flex;flex-wrap:wrap}
.fr>*{flex:1 1 158px}
.rcm{display:flex}
.rcm>*{flex:1}
@supports (display:grid){
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr))}
.grid{display:grid}.grid>*{min-width:0}
.g2{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
.cal{display:grid;grid-template-columns:repeat(7,1fr)}.cal>*{max-width:none}
.fr{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr))}
.rcm{display:grid;grid-template-columns:repeat(4,1fr)}
@media (max-width:860px){
.g2,.g3{grid-template-columns:1fr}
.grid>*{flex:1 1 100%}
.fr>*{flex:1 1 100%}
.stats{grid-template-columns:repeat(2,1fr)}}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
"""
