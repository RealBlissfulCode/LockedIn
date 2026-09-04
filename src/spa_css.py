# -*- coding: utf-8 -*-
APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
/* Palette follows jaronnorris.com: near-black ground, purple accent, monospace
   for anything numeric or structural. --brass is kept as the accent variable
   name so every existing rule picks the new colour up for free. */
:root{
--bg:#0A0A0C;--bg-2:#0E0E12;--panel:#131318;--panel-2:#1A1A21;--raise:#22222B;
--line:#26262F;--line-2:#33333F;
--ink:#EDEAF2;--ink-2:#B4B0BE;--ink-3:#8B8796;--ink-4:#5D5A68;
--brass:#A855F7;--brass-2:#C084FC;--amber:#E879C4;
--sage:#4ADE80;--steel:#60A5FA;--clay:#F87171;
--on-accent:#0A0A0C;
--r:10px;--r-s:7px;--r-l:16px;
--sh:0 1px 2px rgba(0,0,0,.5);
--sh-2:0 4px 16px rgba(0,0,0,.5);
--sh-3:0 18px 48px rgba(0,0,0,.65);
--glow:0 0 0 3px rgba(168,85,247,.16);
--ez:cubic-bezier(.2,.7,.3,1);
--f-body:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
--f-disp:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
--f-mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
html[data-theme="light"]{
--bg:#FBFAFC;--bg-2:#F4F2F8;--panel:#FFFFFF;--panel-2:#F5F3F9;--raise:#EBE7F2;
--line:#E5E2EC;--line-2:#D2CDE0;
--ink:#17151C;--ink-2:#3D3948;--ink-3:#655F73;--ink-4:#918B9E;
--brass:#7E22CE;--brass-2:#9333EA;--amber:#BE1D8B;
--sage:#177245;--steel:#1D5FBF;--clay:#B91C1C;
--on-accent:#FFFFFF;
--sh:0 1px 2px rgba(23,21,28,.06);
--sh-2:0 4px 14px rgba(23,21,28,.10);
--sh-3:0 18px 48px rgba(23,21,28,.20);
--glow:0 0 0 3px rgba(126,34,206,.15);}
html[data-theme="light"] body{
background-image:radial-gradient(ellipse 900px 500px at 12% -6%,rgba(126,34,206,.07),transparent 60%),
radial-gradient(ellipse 700px 400px at 92% 2%,rgba(29,95,191,.05),transparent 60%);}
html[data-theme="light"] .top{background:rgba(251,250,252,.88)}
html[data-theme="light"] .btmnav{background:rgba(251,250,252,.96)}
html[data-theme="light"] .tab.on{color:#fff}
html[data-theme="light"] .b{color:#fff}
html[data-theme="light"] .b.o{color:var(--ink)}
html[data-theme="light"] .b.dz{color:var(--clay)}
html[data-theme="light"] .b.o:hover{color:var(--brass-2)}
html[data-theme="light"] .day.sel{background:rgba(126,34,206,.09)}
html[data-theme="light"] .day.sel .dev{color:var(--ink-2)}
html[data-theme="light"] .toast{color:#fff}
html[data-theme="light"] .pill.on{color:#fff}
html[data-theme="light"] .rcbadge{background:rgba(255,255,255,.9);color:var(--ink-2)}
html[data-theme="light"] .fav{background:rgba(255,255,255,.92)}
html[data-theme="light"] .aisle{background:var(--ink);color:#fff}
html[data-theme="light"] .aisle span{color:var(--brass-2)}
html[data-theme="light"] .stat.acc{background:linear-gradient(150deg,#F3E8FF,#EDE4FA)}
html[data-theme="light"] .dhero .scrim{
background:linear-gradient(to top,rgba(14,12,18,.92),rgba(14,12,18,.45) 55%,rgba(14,12,18,.2))}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;background:var(--bg);transition:background .3s var(--ez)}
body{transition:background-color .3s var(--ez),color .3s var(--ez)}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.6 var(--f-body);padding-bottom:88px;
background-image:radial-gradient(ellipse 900px 500px at 12% -6%,rgba(168,85,247,.07),transparent 60%),
radial-gradient(ellipse 700px 400px at 92% 2%,rgba(96,165,250,.055),transparent 60%);
background-attachment:fixed}
a{color:var(--brass);text-decoration:none}
button,input,select,textarea{font:inherit;color:inherit}
h1,h2,h3,h4{margin:0;font-family:var(--f-disp);font-weight:600;letter-spacing:-.02em;line-height:1.14}
.wrap{max-width:1200px;margin:0 auto;padding:0 22px}
.lbl,.eyebrow{font:700 9.5px/1 var(--f-body);letter-spacing:.2em;text-transform:uppercase;color:var(--ink-4)}
.mono{font-family:var(--f-mono);font-variant-numeric:tabular-nums}

/* top bar */
.top{position:sticky;top:0;z-index:60;background:rgba(10,10,12,.86);
backdrop-filter:saturate(150%) blur(16px);-webkit-backdrop-filter:saturate(150%) blur(16px);
border-bottom:1px solid var(--line)}
.topin{max-width:1200px;margin:0 auto;padding:12px 22px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;min-width:0}
.brand{flex:0 0 auto}
.tabs{flex:1 1 auto;justify-content:flex-end;flex-wrap:wrap}
.whoswitch{flex:0 0 auto}
.brand{font-family:var(--f-disp);font-weight:700;font-size:18px;letter-spacing:-.03em;color:var(--ink);
white-space:nowrap;display:flex;align-items:center;gap:9px}
.brand:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--brass);
box-shadow:var(--glow),0 0 14px rgba(168,85,247,.5)}
.brand em{font-style:normal;color:var(--ink-3);font-weight:500}
.brand>span{display:inline-flex;letter-spacing:-.03em}
.tabs{display:flex;gap:2px;margin-left:auto}
.tab{background:none;border:0;color:var(--ink-3);font-weight:600;font-size:13px;padding:8px 14px;
border-radius:999px;cursor:pointer;transition:.2s var(--ez);white-space:nowrap}
.tab:hover{color:var(--ink);background:var(--panel-2)}
.tab.on{color:var(--bg);background:var(--brass)}
.iconbtn{background:var(--panel-2);border:1px solid var(--line);color:var(--ink-2);width:34px;height:34px;
border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s var(--ez)}
.iconbtn:hover{border-color:var(--brass);color:var(--brass)}
.iconbtn svg{width:17px;height:17px}
.whoswitch{display:flex;background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:3px;gap:2px}
.whoswitch button{background:none;border:0;color:var(--ink-3);font-weight:600;font-size:12.5px;
padding:6px 15px;border-radius:999px;cursor:pointer;transition:.22s var(--ez);white-space:nowrap}
.whoswitch button:hover{color:var(--ink)}
.whoswitch button.on{background:var(--raise);color:var(--ink);box-shadow:var(--sh);font-weight:700}
.whoswitch button.on:before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;
background:var(--sage);margin-right:7px;vertical-align:middle}

/* bottom bar */
.btmnav{display:none;position:fixed;left:0;right:0;bottom:0;z-index:70;background:rgba(10,10,12,.95);
backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-top:1px solid var(--line);
padding:7px 4px calc(7px + env(safe-area-inset-bottom))}
.btmnav button{flex:1;background:none;border:0;padding:5px 2px;color:var(--ink-4);cursor:pointer;
display:flex;flex-direction:column;align-items:center;gap:4px;font:700 9px/1 var(--f-body);
letter-spacing:.08em;transition:.18s var(--ez);text-transform:uppercase}
.btmnav svg{width:20px;height:20px;stroke-width:1.6}
.btmnav button.on{color:var(--brass)}
.btmnav button.on svg{stroke-width:2}

/* page */
.page{animation:rise .4s var(--ez)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.phead{padding:38px 0 22px;border-bottom:1px solid var(--line);margin-bottom:30px}
.phead h1,.phead p{max-width:68ch}
.phead h1{font-size:clamp(28px,4.2vw,44px);letter-spacing:-.035em}
.phead p{color:var(--ink-3);margin:10px 0 0;font-size:16px;line-height:1.55}
.sec{margin:40px 0}
.sec:first-child{margin-top:0}
/* Section header rhythm. A header always leaves the same gap before its
   content, whether or not it carries a subtitle or a row of buttons. Getting
   this wrong is what had action buttons sitting a few pixels off the card
   below them. */
.sec>h2,.sec>.spread{margin-bottom:18px}
.sec>h2+.sub,.sec>.spread+.sub{margin-top:-12px;margin-bottom:18px}
.sec>h2{font-size:21px;letter-spacing:-.028em;min-width:0;overflow-wrap:break-word}
.sec>.sub{color:var(--ink-3);font-size:13.5px;max-width:72ch}
.sec>.spread{align-items:center;gap:12px 18px}
/* Buttons in a section header answer to the heading, so they sit a step down
   from a primary action rather than competing with it. */
.sec>.spread .row{gap:8px}
.sec>.spread .b{padding:7px 14px;font-size:12.5px}
/* A toolbar under the page head, above the first block of content. */
.toolbar{margin-bottom:24px}
/* Card headings, instead of a hand-set font-size at every call site. */
.ctitle{font-size:15px;letter-spacing:-.01em;margin-bottom:14px;color:var(--ink)}
.stats+.note,.note+.stats{margin-top:16px}
.gap-b{margin-bottom:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh)}
.pad{padding:20px 22px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(196px,1fr))}
.row{display:flex;gap:9px;flex-wrap:wrap;align-items:center;min-width:0}
.row>*{min-width:0}
.spread{flex-wrap:wrap}
.spread{display:flex;justify-content:space-between;align-items:center;gap:12px}
.muted{color:var(--ink-3)}.sm{font-size:13px}.xs{font-size:11.5px}
.right{margin-left:auto}
.hr{height:1px;background:var(--line);margin:26px 0}

/* stats */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));
background:var(--panel);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.stat{padding:16px 15px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-family:var(--f-mono);font-size:24px;font-weight:700;letter-spacing:-.03em;
line-height:1;color:var(--ink)}
.stat span{display:block;font:700 9px/1 var(--f-body);letter-spacing:.18em;text-transform:uppercase;
color:var(--ink-4);margin-top:8px}
.stat.acc{background:linear-gradient(150deg,#1E1330,#14101C)}
.stat.acc b{color:var(--brass);font-size:29px}
.stat.acc span{color:rgba(168,85,247,.62)}
.stat.good b{color:var(--sage)}
.stat.bad b{color:var(--clay)}

/* progress */
.mrow{margin-bottom:13px}.mrow:last-child{margin-bottom:0}
.mrow .spread{font-size:12.5px;font-weight:600;margin-bottom:6px}
.mrow .spread em{font-style:normal;color:var(--ink-3);font-weight:500;font-family:var(--f-mono)}
.bar{height:4px;background:var(--panel-2);border-radius:99px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:99px;transition:width .7s var(--ez)}
.pk{background:var(--brass)}.pp{background:var(--sage)}.pc{background:var(--amber)}.pf{background:var(--steel)}

/* buttons */
.b{border:1px solid var(--brass);background:var(--brass);color:var(--on-accent);font-weight:700;font-size:13.5px;
padding:9px 17px;border-radius:999px;cursor:pointer;transition:.2s var(--ez);display:inline-flex;
align-items:center;gap:7px;justify-content:center}
.b:hover{background:var(--brass-2);border-color:var(--brass-2);transform:translateY(-1px);box-shadow:var(--sh-2)}
.b:active{transform:none}
.b.o{background:transparent;color:var(--ink-2);border-color:var(--line-2);font-weight:600}
.b.o:hover{background:var(--panel-2);border-color:var(--brass);color:var(--brass)}
.b.s{padding:6px 12px;font-size:12px}
.b.dz{background:transparent;color:var(--clay);border-color:#4A2530}
.b.dz:hover{background:rgba(248,113,113,.12);border-color:var(--clay);color:var(--clay)}
.b:disabled{opacity:.4;cursor:not-allowed;transform:none}

/* fields */
.f{display:block;margin-bottom:13px}
.f>span{display:block;font:700 9.5px/1 var(--f-body);letter-spacing:.18em;text-transform:uppercase;
color:var(--ink-4);margin-bottom:6px}
.f input,.f select,.f textarea{width:100%;padding:10px 12px;border:1px solid var(--line-2);
border-radius:var(--r-s);background:var(--bg-2);color:var(--ink);font-weight:500;transition:.16s var(--ez)}
.f input:focus,.f select:focus,.f textarea:focus{outline:0;border-color:var(--brass);
box-shadow:var(--glow)}
.f textarea{resize:vertical;line-height:1.55}
.fr{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(155px,1fr))}

/* recipe cards */
.rc{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:var(--r);
overflow:hidden;cursor:pointer;transition:.26s var(--ez);display:flex;flex-direction:column;box-shadow:var(--sh)}
.rc:hover{transform:translateY(-3px);box-shadow:var(--sh-2);border-color:var(--line-2)}
.rcart{height:126px;position:relative;overflow:hidden;background:var(--panel-2)}
.rcart img{width:100%;height:100%;object-fit:cover;display:block;transition:.5s var(--ez)}
.rc:hover .rcart img{transform:scale(1.05)}
.rcart .plate{position:absolute;inset:0;width:100%;height:100%;opacity:.5}
.rcart .ring{position:absolute;right:11px;bottom:10px}
.rcbadge{position:absolute;left:11px;top:11px;background:rgba(10,10,12,.72);color:var(--ink-2);
font:700 9px/1 var(--f-mono);letter-spacing:.1em;padding:5px 8px;border-radius:4px;
border:1px solid rgba(255,255,255,.1)}
.rcb{padding:14px 15px 15px;display:flex;flex-direction:column;flex:1}
.rcn{font-family:var(--f-disp);font-size:16px;font-weight:600;letter-spacing:-.02em;line-height:1.24;
color:var(--ink);margin-bottom:9px}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:11px}
.chip{font:600 10.5px/1 var(--f-body);padding:5px 8px;border-radius:5px;background:var(--panel-2);
color:var(--ink-2);white-space:nowrap;border:1px solid var(--line)}
.chip.t{background:rgba(74,222,128,.14);color:var(--sage);border-color:rgba(74,222,128,.28)}
.chip.d1{background:rgba(74,222,128,.14);color:var(--sage);border-color:rgba(74,222,128,.28)}
.chip.d2{background:rgba(168,85,247,.13);color:var(--brass);border-color:rgba(168,85,247,.28)}
.chip.d3{background:rgba(248,113,113,.14);color:var(--clay);border-color:rgba(248,113,113,.3)}
.chip.p{font-family:var(--f-mono)}
.rcm{display:grid;grid-template-columns:repeat(4,1fr);margin-top:auto;border-top:1px solid var(--line);padding-top:11px}
.rcm div{text-align:center;border-right:1px solid var(--line)}
.rcm div:last-child{border-right:0}
.rcm b{display:block;font-family:var(--f-mono);font-size:15px;font-weight:700;color:var(--ink)}
.rcm span{font:700 8px/1 var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-4);
display:block;margin-top:4px}
.fav{position:absolute;right:10px;top:10px;width:30px;height:30px;border-radius:50%;border:1px solid var(--line);
background:rgba(10,10,12,.72);color:var(--ink-4);font-size:14px;cursor:pointer;line-height:1;
display:flex;align-items:center;justify-content:center;transition:.22s var(--ez);z-index:2}
.fav:hover{transform:scale(1.12);border-color:var(--brass)}
.fav.on{color:var(--brass);border-color:var(--brass)}

/* detail */
.dhero{border-radius:var(--r-l);overflow:hidden;position:relative;min-height:250px;display:flex;
align-items:flex-end;color:var(--ink);padding:30px;border:1px solid var(--line)}
.dhero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dhero .scrim{position:absolute;inset:0;
background:linear-gradient(to top,rgba(8,9,10,.94),rgba(8,9,10,.45) 55%,rgba(8,9,10,.2))}
.dhero .in{position:relative;max-width:64ch}
.dhero h1{font-size:clamp(25px,3.8vw,38px);letter-spacing:-.032em;margin:8px 0 9px}
.ing{list-style:none;margin:0;padding:0}
.ing li{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);font-size:14px;align-items:baseline}
.ing li:last-child{border-bottom:0}
.ing b{color:var(--ink);min-width:76px;font-family:var(--f-mono);font-weight:700}
.ing .c{margin-left:auto;color:var(--ink-4);font-size:12px;font-family:var(--f-mono)}
ol.stp{margin:0;padding:0;list-style:none;counter-reset:s}
ol.stp li{counter-increment:s;position:relative;padding:0 0 18px 44px;line-height:1.66;font-size:15px}
ol.stp li:before{content:counter(s);position:absolute;left:0;top:-1px;width:28px;height:28px;border-radius:50%;
background:var(--panel-2);border:1px solid var(--line-2);color:var(--brass);
font:700 12px/26px var(--f-mono);text-align:center}
ol.stp li:after{content:"";position:absolute;left:13.5px;top:32px;bottom:5px;width:1px;background:var(--line)}
ol.stp li:last-child{padding-bottom:0}ol.stp li:last-child:after{display:none}

/* table */
table{border-collapse:collapse;width:100%;font-size:13.5px}
th{background:var(--panel-2);color:var(--ink-3);text-align:left;font:700 9px/1 var(--f-body);
letter-spacing:.18em;text-transform:uppercase;padding:12px 13px;border-bottom:1px solid var(--line)}
td{padding:11px 13px;border-bottom:1px solid var(--line);color:var(--ink-2)}
td b{color:var(--ink)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--panel-2)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:var(--r);
background:var(--panel)}
.num{font-family:var(--f-mono);text-align:right}

/* calendar */
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}
.cal .dow{text-align:center;font:700 9px/1 var(--f-body);letter-spacing:.18em;color:var(--ink-4);padding:7px 0}
.day{min-height:82px;border:1px solid var(--line);border-radius:var(--r-s);background:var(--panel);
padding:6px 7px;cursor:pointer;display:flex;flex-direction:column;transition:.18s var(--ez);
position:relative;overflow:hidden;text-align:left}
.day:hover{border-color:var(--brass);transform:translateY(-2px)}
.day.out{opacity:0;pointer-events:none}
.day.today{border-color:var(--line-2)}
.day.today .dn{color:var(--brass)}
.day.sel{background:rgba(168,85,247,.13);border-color:var(--brass);
box-shadow:inset 0 0 0 1px var(--brass)}
.day.sel .dn{color:var(--brass)}
.day.sel .dk{color:var(--brass-2)}
.dn{font-family:var(--f-mono);font-size:13px;font-weight:700;color:var(--ink)}
.dk{font:600 9px/1 var(--f-mono);color:var(--ink-4);margin-top:auto}
.devs{margin-top:5px;display:flex;flex-direction:column;gap:2px;overflow:hidden}
.dev{font:600 9.5px/1.25 var(--f-body);color:var(--ink-2);white-space:nowrap;overflow:hidden;
text-overflow:ellipsis;padding-left:8px;position:relative}
.dev:before{content:"";position:absolute;left:0;top:4px;width:4px;height:4px;border-radius:50%;background:var(--steel)}
.dev.w:before{background:var(--sage)}.dev.m:before{background:var(--amber)}
.day.sel .dev{color:var(--ink-2)}
.day.sel .dev:before{background:var(--brass)}
.dmore{font:600 9px/1 var(--f-body);color:var(--ink-4);padding-left:8px}
.dots{display:none;gap:3px;margin-top:4px;flex-wrap:wrap}
.dot{width:4px;height:4px;border-radius:50%;background:var(--brass)}
.dot.w{background:var(--sage)}.dot.e{background:var(--steel)}.dot.m{background:var(--amber)}

/* timeline */
.tl{list-style:none;margin:0;padding:0;position:relative}
.tl:before{content:"";position:absolute;left:58px;top:6px;bottom:6px;width:1px;background:var(--line)}
.tl li{display:flex;gap:16px;padding:10px 0;position:relative;align-items:flex-start}
.tl .tm{width:52px;flex:none;text-align:right;font:700 11px/1.5 var(--f-mono);color:var(--ink-3);padding-top:3px}
.tl .pip{position:absolute;left:55px;top:14px;width:7px;height:7px;border-radius:50%;
background:var(--brass);box-shadow:0 0 0 3px var(--panel)}
.tl .pip.w{background:var(--sage)}.tl .pip.e{background:var(--steel)}.tl .pip.m{background:var(--amber)}
.tl .bd{flex:1;min-width:0;padding-left:14px}
.tl .ti{font-weight:600;color:var(--ink);font-size:14px}
.tl .ts{font-size:11.5px;color:var(--ink-4);margin-top:2px}

/* grocery */
.aisle{background:var(--panel-2);color:var(--ink-2);padding:10px 16px;font:700 9px/1 var(--f-body);
letter-spacing:.2em;text-transform:uppercase;display:flex;justify-content:space-between;
border-bottom:1px solid var(--line)}
.aisle span{color:var(--brass);font-family:var(--f-mono);letter-spacing:0}
.gitem{display:flex;align-items:center;gap:12px;padding:11px 16px;border-bottom:1px solid var(--line)}
.gitem:last-child{border-bottom:0}
.gitem.done{opacity:.4}
.gitem.done .gn{text-decoration:line-through}
.gitem input[type=checkbox]{width:18px;height:18px;accent-color:var(--brass);flex:none;cursor:pointer}
.gn{flex:1;min-width:0;font-size:14px;font-weight:600;color:var(--ink)}
.gq{font-size:11.5px;color:var(--ink-4);font-weight:400;margin-top:2px}
.gp{font-family:var(--f-mono);font-weight:700;color:var(--brass);font-size:13.5px}

/* modal */
.mask{position:fixed;inset:0;background:rgba(6,5,10,.72);backdrop-filter:blur(5px);z-index:200;
display:flex;align-items:center;justify-content:center;padding:20px;animation:fadein .2s var(--ez)}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.modal{background:var(--panel);border:1px solid var(--line-2);border-radius:var(--r-l);max-width:600px;
width:100%;max-height:88vh;display:flex;flex-direction:column;box-shadow:var(--sh-3);
animation:pop .28s var(--ez);overflow:hidden}
@keyframes pop{from{opacity:0;transform:scale(.96) translateY(12px)}to{opacity:1;transform:none}}
.mhead{padding:19px 22px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;
align-items:center}
.mhead h3{font-size:18px}
.mbody{padding:20px 22px;overflow-y:auto}
.mfoot{padding:15px 22px;border-top:1px solid var(--line);display:flex;gap:9px;justify-content:flex-end;
background:var(--bg-2);flex-wrap:wrap}
.x{border:1px solid var(--line);background:var(--panel-2);width:30px;height:30px;border-radius:50%;
cursor:pointer;color:var(--ink-3);font-size:16px;line-height:1;transition:.18s var(--ez)}
.x:hover{background:var(--raise);color:var(--ink)}
.pickrow{display:flex;align-items:center;gap:12px;padding:11px;border-radius:var(--r-s);cursor:pointer;
border:1px solid transparent;transition:.16s var(--ez)}
.pickrow:hover{background:var(--panel-2);border-color:var(--line)}
.toast{position:fixed;left:50%;bottom:100px;transform:translateX(-50%);background:var(--brass);
color:var(--on-accent);padding:12px 22px;border-radius:999px;font-size:13.5px;font-weight:700;z-index:300;
box-shadow:var(--sh-3);animation:pop .26s var(--ez)}

/* error panel */
.errbox{background:rgba(248,113,113,.10);border:1px solid var(--clay);border-radius:var(--r);
padding:20px 22px;margin:24px 0}
.errbox h3{color:var(--clay);font-size:17px;margin-bottom:8px}
.errbox pre{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--r-s);
padding:12px;overflow:auto;font:500 12px/1.5 var(--f-mono);color:var(--ink-2);margin:10px 0 0}

/* misc */
.pill{display:inline-block;background:var(--panel);color:var(--ink-2);border-radius:999px;padding:6px 14px;
font-size:12.5px;font-weight:600;cursor:pointer;border:1px solid var(--line);transition:.18s var(--ez)}
.pill:hover{border-color:var(--brass);color:var(--brass)}
.pill.on{background:var(--brass);color:var(--on-accent);border-color:var(--brass)}
.note{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--brass);
border-radius:0 var(--r-s) var(--r-s) 0;padding:15px 18px;font-size:14px;margin:15px 0;color:var(--ink-2)}
.note b{color:var(--ink);font-weight:600}
.note.warn{border-left-color:var(--clay)}
.note.good{border-left-color:var(--sage)}
.empty{text-align:center;padding:50px 20px;color:var(--ink-4)}
.empty p{margin:0 0 6px}
details{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);margin-bottom:8px;
overflow:hidden;transition:.2s var(--ez)}
details[open]{border-color:var(--line-2)}
summary{padding:16px 20px;cursor:pointer;font-weight:600;font-size:15px;color:var(--ink);list-style:none;
display:flex;justify-content:space-between;align-items:center;gap:14px}
summary::-webkit-details-marker{display:none}
summary:after{content:"";width:8px;height:8px;border-right:1.6px solid var(--ink-4);
border-bottom:1.6px solid var(--ink-4);transform:rotate(45deg);flex:none;margin-top:-4px;transition:.24s var(--ez)}
details[open] summary:after{transform:rotate(-135deg);margin-top:2px}
details .dc{padding:2px 20px 18px;color:var(--ink-2)}
details .dc p{margin:0 0 11px}
details .dc p:last-child{margin-bottom:0}
details .dc ul{margin:0 0 11px;padding-left:18px}
.dirty{display:inline-flex;align-items:center;gap:6px;font:700 10px/1 var(--f-body);letter-spacing:.14em;
text-transform:uppercase;color:var(--clay);background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.3);
padding:5px 10px;border-radius:999px}
.dirty:before{content:"";width:6px;height:6px;border-radius:50%;background:var(--clay)}

/* ---------------------------------------------------------------- the gate */
/* Plain `center` clips the top of a box taller than the viewport and puts it out
   of scroll reach. flex-start is the fallback; `safe center` centres it only
   while it actually fits. */
#gate{position:fixed;inset:0;z-index:500;display:flex;align-items:flex-start;
align-items:safe center;justify-content:center;
padding:24px;background:var(--bg);
background-image:radial-gradient(ellipse 700px 460px at 50% 8%,rgba(168,85,247,.13),transparent 62%),
radial-gradient(ellipse 600px 400px at 50% 100%,rgba(96,165,250,.07),transparent 60%);
overflow-y:auto}
.gatebox{width:100%;max-width:340px;text-align:center;margin:0 auto;
padding:calc(env(safe-area-inset-top) + 8px) 0 calc(env(safe-area-inset-bottom) + 8px)}
.gatemark{width:52px;height:52px;margin:0 auto 20px;border-radius:15px;background:var(--panel);
border:1px solid var(--line-2);position:relative;box-shadow:var(--sh-2)}
/* A padlock, drawn from the two pseudo elements: shackle on top, body below. */
.gatemark:after{content:"";position:absolute;left:50%;top:13px;transform:translateX(-50%);
width:14px;height:11px;border:2px solid var(--brass);border-bottom:0;border-radius:7px 7px 0 0}
.gatemark:before{content:"";position:absolute;left:50%;top:22px;transform:translateX(-50%);
width:22px;height:17px;border-radius:3px;background:var(--brass);
box-shadow:0 0 14px rgba(168,85,247,.35)}
#gate h1{font-size:23px;letter-spacing:-.02em;color:var(--ink)}
.gsub{color:var(--ink-3);font-size:13.5px;margin:8px 0 26px}
.gdots{display:flex;justify-content:center;gap:13px;margin-bottom:26px;height:13px}
.gdots i{width:11px;height:11px;border-radius:50%;border:1.5px solid var(--line-2);
background:transparent;transition:.2s var(--ez)}
.gdots i.on{background:var(--brass);border-color:var(--brass);transform:scale(1.12);
box-shadow:0 0 12px rgba(168,85,247,.5)}
/* Real field, kept off screen. The dots are the display; this takes the typing. */
#gin{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px;left:-9999px}
.gpad{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}
.gpad button{aspect-ratio:1/1;min-height:56px;border-radius:50%;border:1px solid var(--line);
background:var(--panel);color:var(--ink);font:500 21px/1 var(--f-mono);cursor:pointer;
transition:.15s var(--ez);display:flex;align-items:center;justify-content:center}
.gpad button:hover{border-color:var(--brass);color:var(--brass)}
.gpad button:active{transform:scale(.94);background:var(--panel-2)}
.gpad .gghost{background:transparent;border-color:transparent;color:var(--ink-4);
font:600 12px/1 var(--f-body);letter-spacing:.1em;text-transform:uppercase}
.gpad .gghost:hover{color:var(--ink-2);border-color:transparent}
.gerr{color:var(--clay);font-size:13px;font-weight:600;margin:18px 0 0;min-height:19px}
.gnote{color:var(--ink-4);font-size:11.5px;line-height:1.55;margin:22px 0 0}
#gate.working{pointer-events:none}
#gate.working .gdots i{animation:gpulse 1s ease-in-out infinite}
#gate.working .gpad{opacity:.45}
@keyframes gpulse{0%,100%{opacity:.3}50%{opacity:1}}
.gatebox.shake{animation:gshake .38s var(--ez)}
@keyframes gshake{0%,100%{transform:translateX(0)}20%{transform:translateX(-9px)}
40%{transform:translateX(9px)}60%{transform:translateX(-5px)}80%{transform:translateX(5px)}}
/* Landscape phones and short windows: shrink rather than scroll. */
@media (max-height:760px){
.gatemark{width:40px;height:40px;margin-bottom:12px;border-radius:12px}
.gatemark:after{top:10px;width:11px;height:9px;border-radius:6px 6px 0 0}
.gatemark:before{top:17px;width:17px;height:13px}
#gate h1{font-size:19px}
.gsub{margin:6px 0 16px;font-size:12.5px}
.gdots{margin-bottom:16px;gap:11px}
.gpad{gap:8px}
.gpad button{min-height:44px;font-size:17px}
.gnote{display:none}
.gerr{margin-top:12px}}

/* ------------------------------------------------------------- strategies */
.f.inline{display:flex;align-items:center;gap:9px;margin:0}
.f.inline>span{margin:0;white-space:nowrap}
.f.inline select{width:auto;padding:6px 10px}
details.strat{margin-bottom:7px}
details.strat summary{padding:14px 18px;gap:12px;align-items:flex-start}
details.strat .stn{flex:1;min-width:0;font-weight:600;font-size:14.5px;line-height:1.4;
font-family:var(--f-body);letter-spacing:0}
details.strat .stmeta{display:flex;align-items:center;gap:10px;flex:none;flex-wrap:wrap;
justify-content:flex-end}
details.strat .stv{font-family:var(--f-mono);font-size:14px;font-weight:700;color:var(--brass);
white-space:nowrap}
details.strat .stv.neg{color:var(--clay)}
details.strat.dead summary .stn{color:var(--ink-4);text-decoration:line-through;
text-decoration-color:var(--line-2)}
details.strat.dead .stv{color:var(--ink-4)}
.stgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(84px,1fr));gap:10px;
padding:12px 0 16px;border-bottom:1px solid var(--line);margin-bottom:14px}
.stgrid>div{min-width:0}
.stgrid b{display:block;font-family:var(--f-mono);font-size:15px;color:var(--ink);margin-top:5px;
overflow-wrap:break-word}
details.strat .dc p{line-height:1.68;color:var(--ink-2);font-size:14px}

/* ---------------------------------------------------------- big purchases */
.bpc{display:flex;flex-direction:column;transition:.22s var(--ez)}
.bpc:hover{border-color:var(--line-2);transform:translateY(-2px);box-shadow:var(--sh-2)}
.bpc.best{border-color:rgba(74,222,128,.4)}
.bpn{font-family:var(--f-body);font-size:15.5px;font-weight:600;line-height:1.32;
letter-spacing:-.01em;min-width:0;overflow-wrap:break-word}
.bpp{font-family:var(--f-mono);font-size:23px;font-weight:700;color:var(--brass);
letter-spacing:-.02em;margin:8px 0 12px}
.bpf{border-bottom:1px solid var(--line);padding:6px 0;gap:10px}
.bpf:last-of-type{border-bottom:0}
.bpf b{font-family:var(--f-mono);font-weight:600;text-align:right;min-width:0;
overflow-wrap:break-word}

/* ---------------------------------------------------------------- planning */
.plcard{text-align:left;cursor:pointer;font:inherit;color:inherit;display:block;width:100%;
transition:.22s var(--ez)}
.plcard:hover{border-color:var(--brass);transform:translateY(-2px);box-shadow:var(--sh-2)}
.pln{font-size:17px;letter-spacing:-.02em;min-width:0;overflow-wrap:break-word}
.pitem{display:flex;align-items:flex-start;gap:13px;padding:13px 16px;
border-bottom:1px solid var(--line)}
.pitem:last-child{border-bottom:0}
.pitem input[type=checkbox]{width:19px;height:19px;accent-color:var(--brass);flex:none;
cursor:pointer;margin-top:1px}
.pbody{flex:1;min-width:0}
.pt{font-size:14.5px;font-weight:600;color:var(--ink);line-height:1.45;overflow-wrap:break-word}
.pn{font-size:12.5px;color:var(--ink-3);margin-top:4px;line-height:1.55;overflow-wrap:break-word}
.pitem.done .pt{text-decoration:line-through;color:var(--ink-4)}
.pitem.done .pn{color:var(--ink-4)}
.pitem .b.s,.pitem .x{flex:none;align-self:center}

/* ----------------------------------------------------- schedule templates */
.tcard{transition:.22s var(--ez)}
.tcard:hover{border-color:var(--line-2);transform:translateY(-2px);box-shadow:var(--sh-2)}
.tcard.live{border-color:rgba(74,222,128,.35)}
.favstar{color:var(--brass);font-size:14px;line-height:1}

/* --------------------------------------------------------- recipe lists */
.rlwrap{position:relative;min-width:0}
.rlwrap .rlrm{position:absolute;right:10px;top:46px;z-index:3;
background:rgba(10,10,12,.78);backdrop-filter:blur(4px)}
.rlwrap .rlrm:hover{background:var(--clay);color:var(--on-accent);border-color:var(--clay)}
html[data-theme="light"] .rlwrap .rlrm{background:rgba(255,255,255,.9)}

/* ------------------------------------------------------- sync status pill */
.syncpill{display:inline-flex;align-items:center;gap:7px;background:var(--panel);
border:1px solid var(--line);border-radius:999px;padding:5px 12px 5px 10px;cursor:pointer;
color:var(--ink-3);font:600 11.5px/1 var(--f-body);white-space:nowrap;
transition:.18s var(--ez)}
.syncpill:hover{border-color:var(--line-2);color:var(--ink-2)}
.syncpill i{width:6px;height:6px;border-radius:50%;background:var(--ink-4);flex:none}
.syncpill.ok i{background:var(--sage);box-shadow:0 0 8px rgba(74,222,128,.5)}
.syncpill.busy i{background:var(--brass);animation:syncblink 1s ease-in-out infinite}
.syncpill.warn i{background:var(--amber)}
.syncpill.bad i{background:var(--clay)}
.syncpill.warn,.syncpill.bad{color:var(--ink-2)}
@keyframes syncblink{0%,100%{opacity:.35}50%{opacity:1}}

/* ------------------------------------------------------------ misc polish */
:focus-visible{outline:2px solid var(--brass);outline-offset:2px;border-radius:3px}
.tw table{min-width:560px}
/* The money tables carry a switch column on top of their own eight. */
.tw.wide table{min-width:700px}
.chip{overflow-wrap:break-word}

@media (max-width:860px){
.wrap{padding:0 15px}
/* Six things have to share 375px: brand, who, sync, theme, settings. Every one
   of them gives up a little so the bar stays a single row instead of eating
   twice the height on every screen. */
.syncpill span{display:none}
.syncpill{padding:0;width:26px;height:26px;justify-content:center}
/* The wordmark is the one thing here the phone does not need: the icon, the
   bottom bar and the page title all say what this is. Dropping to the mark
   alone buys about 100px and keeps the bar one row even with longer names. */
.brand{font-size:0;gap:0;flex:0 0 auto}
.brand:before{width:9px;height:9px}
.whoswitch button{padding:5px 12px;font-size:12px}
.whoswitch button.on:before{width:5px;height:5px;margin-right:5px}
.iconbtn{width:31px;height:31px}
.iconbtn svg{width:15px;height:15px}
.gatebox{max-width:300px}
.gpad button{min-height:52px;font-size:19px}
#gate h1{font-size:20px}
details.strat summary{flex-wrap:wrap;padding:13px 15px}
details.strat .stn{flex:1 1 100%}
details.strat .stmeta{flex:1 1 100%;justify-content:flex-start;margin-top:8px}
details.strat .dc{padding:2px 15px 16px}
.bpp{font-size:21px}
.pitem{padding:12px 14px;flex-wrap:wrap}
.pitem .b.s{margin-left:auto}
.stgrid{grid-template-columns:repeat(3,1fr)}

body{padding-bottom:80px}
.tabs{display:none}
.btmnav{display:flex}
.topin{padding:10px 15px;gap:9px;flex-wrap:nowrap}
.whoswitch{margin-left:auto}
.phead{padding:22px 0 14px;margin-bottom:20px}
.g2,.g3{grid-template-columns:1fr}
.g4{grid-template-columns:1fr 1fr}
.stats{grid-template-columns:repeat(2,1fr)}
.stat{border-bottom:1px solid var(--line)}
.stat:nth-child(odd){border-right:1px solid var(--line)}
.stat:nth-child(even){border-right:0}
.dhero{min-height:200px;padding:20px;border-radius:var(--r)}
.cal{gap:3px}.day{padding:4px;border-radius:6px;min-height:64px}
.dev{font-size:8.5px}
.pad{padding:16px}
ol.stp li{padding-left:38px}
.tl:before{left:46px}.tl .tm{width:42px}.tl .pip{left:43px}

/* ------------------------------------------------------ mobile usability */
/* iOS zooms the entire page when a focused field is under 16px, and then
   leaves it zoomed. This is the whole fix. */
.f input,.f select,.f textarea,input,select,textarea{font-size:16px}
/* Sized for thumbs. 28px targets are a cursor size, not a finger size. */
.b{padding:11px 18px;font-size:14px}
.b.s,.sec>.spread .b{padding:9px 15px;font-size:13px}
.x{width:36px;height:36px;font-size:18px}
.pill{padding:9px 16px}
.gitem input[type=checkbox],.pitem input[type=checkbox]{width:22px;height:22px}
.iconbtn,.syncpill{flex:0 0 auto}
.fav{width:34px;height:34px}

/* Editors rise from the bottom instead of floating in the middle, so the
   fields sit above the keyboard and Save is always within reach. */
.mask{padding:0;align-items:flex-end}
.modal{max-width:none;width:100%;max-height:92vh;
border-radius:var(--r-l) var(--r-l) 0 0;animation:sheet .26s var(--ez)}
@keyframes sheet{from{transform:translateY(100%)}to{transform:none}}
.modal:before{content:"";position:absolute;left:50%;top:7px;transform:translateX(-50%);
width:36px;height:4px;border-radius:99px;background:var(--line-2);opacity:.9}
.mhead{position:sticky;top:0;z-index:2;background:var(--panel);padding:20px 18px 14px}
.mbody{padding:16px 18px}
.mfoot{position:sticky;bottom:0;z-index:2;
padding:14px 18px calc(14px + env(safe-area-inset-bottom));
flex-direction:column-reverse;align-items:stretch;gap:8px}
.mfoot .b{width:100%}

/* One card per screen is a lot of thumb. Two fits and still reads. */
.g3{grid-template-columns:repeat(2,minmax(0,1fr))}
.rcart{height:104px}
.rcn{font-size:14px}
.rcm b{font-size:13px}
.rcm span{font-size:7px;letter-spacing:.1em}
.chip{font-size:10px;padding:4px 7px}

/* Wide tables scroll; say so rather than letting the edge look like the end. */
.tw{position:relative}
.tw:after{content:"";position:absolute;top:0;right:0;bottom:0;width:26px;
pointer-events:none;border-radius:0 var(--r) var(--r) 0;
background:linear-gradient(to right,transparent,var(--panel))}
}

/* At this width a calendar cell is about 45px. Event text was 8.5px and
   ellipsised to nothing, so show what KIND of thing is on each day and let the
   day panel below carry the detail. */
@media (max-width:560px){
.cal{gap:2px}
.day{min-height:56px;padding:4px 3px;border-radius:5px}
.devs{display:none}
.dots{display:flex;justify-content:center;margin-top:auto}
.dot{width:6px;height:6px}
.dn{font-size:12px}
.dk{display:none}
.tl .tm{width:38px;font-size:10.5px}
.tl:before{left:42px}.tl .pip{left:39px}
.tl .bd{padding-left:11px}
.stgrid{grid-template-columns:repeat(2,1fr)}
.phead h1{font-size:26px}
.sec{margin:30px 0}
}

@media (max-width:440px){.g4{grid-template-columns:1fr}}
.stats{display:flex;flex-wrap:wrap}.stat{flex:1 1 110px}
.grid{display:flex;flex-wrap:wrap}.grid>*{flex:1 1 300px;min-width:0}
.g3>*{flex:1 1 250px}.g4>*{flex:1 1 196px}
.cal{display:flex;flex-wrap:wrap}.cal>*{flex:0 0 14.28%;max-width:14.28%}
.fr{display:flex;flex-wrap:wrap}.fr>*{flex:1 1 155px}
.rcm{display:flex}.rcm>*{flex:1}
@supports (display:grid){
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr))}
.grid{display:grid}.grid>*{min-width:0}
.g2{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.g3{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(196px,1fr))}
.cal{display:grid;grid-template-columns:repeat(7,1fr)}.cal>*{max-width:none}
.fr{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr))}
.rcm{display:grid;grid-template-columns:repeat(4,1fr)}
@media (max-width:860px){.g2,.g3{grid-template-columns:1fr}.grid>*{flex:1 1 100%}
.fr>*{flex:1 1 100%}.stats{grid-template-columns:repeat(2,1fr)}}
}

/* ---------------- switches ----------------
   A line can drop out of the totals without being deleted, so its row has to
   read as "still here, not counted" instead of as an empty slot. The switch is
   a real button so it is keyboard reachable, and aria-pressed says what state
   it is in. */
.sw{position:relative;flex:none;width:36px;height:20px;padding:0;border:1px solid var(--line-2);
background:var(--panel-2);border-radius:999px;cursor:pointer;transition:.24s var(--ez)}
.sw i{position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
background:var(--ink-4);transition:.24s var(--ez)}
.sw.on{background:var(--brass);border-color:var(--brass)}
.sw.on i{transform:translateX(16px);background:var(--on-accent)}
.sw:hover{border-color:var(--brass)}
.sw:focus-visible{outline:0;box-shadow:var(--glow)}
.sw.xs{width:30px;height:17px}
.sw.xs i{width:11px;height:11px}
.sw.xs.on i{transform:translateX(13px)}
/* A switched off row keeps its numbers readable. Fade it to nothing and you
   have hidden the figure you were trying to decide about. */
tr.offrow{transition:opacity .24s var(--ez)}
tr.offrow>td{opacity:.44}
tr.offrow>td:first-child{opacity:1}
tr.offrow .chip{opacity:.75}
.offtag{font:700 9px/1 var(--f-body);letter-spacing:.14em;text-transform:uppercase;
color:var(--ink-4);margin-left:7px;vertical-align:1px}

/* ---------------- charts ---------------- */
.cempty{padding:26px 4px;text-align:center;color:var(--ink-4);font-size:12.5px}
.cchart{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:8px;align-items:end}
.ccol{min-width:0;text-align:center}
.cstack{position:relative;height:var(--ch,150px);border-bottom:1px solid var(--line)}
.cb{position:absolute;left:var(--l,8%);right:var(--r,8%);bottom:var(--b,0);height:var(--h,0);
border-radius:4px 4px 0 0;transform-origin:bottom;
animation:cgrow .58s var(--ez) both;animation-delay:var(--d,0s)}
@keyframes cgrow{from{transform:scaleY(0);opacity:.3}to{transform:scaleY(1);opacity:1}}
/* The waterfall connector. It reaches back past the column's own edge into
   the grid gap so the run from one bar top to the next is unbroken. It is
   written before the bars, so a bar always covers the stretch of line that
   would otherwise show underneath it. */
.cconn{position:absolute;left:-13px;right:var(--r,8%);bottom:var(--y,0);height:0;
border-top:1px dashed var(--line-2);
animation:cfade .45s var(--ez) both;animation-delay:var(--d,0s)}
.cchart.wf .cstack{overflow:visible}
.clab{margin-top:9px;font:600 10.5px/1.3 var(--f-body);color:var(--ink-3);
overflow-wrap:break-word;hyphens:auto}
.csub{margin-top:4px;font:700 12px/1 var(--f-mono);color:var(--ink)}
.csub.good{color:var(--sage)}.csub.bad{color:var(--clay)}
.ct1{background:var(--brass)}.ct2{background:var(--sage)}.ct3{background:var(--steel)}
.ct4{background:var(--amber)}.ct5{background:var(--clay)}.ct6{background:var(--ink-4)}
.ctg{background:var(--sage)}.ctb{background:var(--clay)}.ctm{background:var(--line-2)}

.cdonut{position:relative;width:100%;max-width:210px;margin:0 auto}
.cdonut svg{display:block;width:100%;height:auto}
.cdonut circle{fill:none;stroke-width:13}
.cdtrack{stroke:var(--panel-2)}
.cdseg{stroke-linecap:butt;stroke-dasharray:var(--len) 100;
animation:cdsweep .78s var(--ez) both;animation-delay:var(--d,0s)}
@keyframes cdsweep{from{stroke-dasharray:0 100}to{stroke-dasharray:var(--len) 100}}
.cdseg.ct1{stroke:var(--brass)}.cdseg.ct2{stroke:var(--sage)}.cdseg.ct3{stroke:var(--steel)}
.cdseg.ct4{stroke:var(--amber)}.cdseg.ct5{stroke:var(--clay)}.cdseg.ct6{stroke:var(--ink-4)}
.cdmid{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
justify-content:center;pointer-events:none;text-align:center;padding:0 22px}
.cdmid b{font:700 21px/1 var(--f-mono);letter-spacing:-.03em;color:var(--ink)}
.cdmid span{margin-top:6px;font:700 8.5px/1 var(--f-body);letter-spacing:.18em;
text-transform:uppercase;color:var(--ink-4)}

.cline{display:block;width:100%;height:auto;overflow:visible}
.cpath{fill:none;stroke:var(--brass);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;
stroke-dasharray:1;animation:cdraw 1s var(--ez) both}
@keyframes cdraw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.carea{fill:url(#cgFill);stroke:none;animation:cfade .9s var(--ez) both;animation-delay:.25s}
@keyframes cfade{from{opacity:0}to{opacity:1}}
.cgs0{stop-color:var(--brass);stop-opacity:.28}
.cgs1{stop-color:var(--brass);stop-opacity:0}
.cline.neg .cpath{stroke:var(--clay)}
.cline.neg .cgs0{stop-color:var(--clay)}
.cline.neg .cgs1{stop-color:var(--clay)}
.czero{stroke:var(--line-2);stroke-width:1;stroke-dasharray:4 4}
.cdot{fill:var(--brass);stroke:var(--panel);stroke-width:1.6;
animation:cpop .3s var(--ez) both;animation-delay:var(--d,0s)}
.cline.neg .cdot{fill:var(--clay)}
@keyframes cpop{from{transform:scale(0);opacity:0}to{transform:scale(1);opacity:1}}
.caxis{display:flex;justify-content:space-between;margin-top:8px;
font:600 10.5px/1 var(--f-body);color:var(--ink-4)}

.cleg{margin-top:16px}
.clrow{display:flex;align-items:center;gap:9px;padding:7px 0;border-top:1px solid var(--line);
font-size:13px;transition:opacity .24s var(--ez)}
.clrow:first-child{border-top:0}
.clrow.off{opacity:.45}
.cdotc{width:9px;height:9px;border-radius:2.5px;flex:none}
.cln{flex:1 1 auto;min-width:0;overflow-wrap:break-word}
.clv{font-family:var(--f-mono);font-weight:700;font-size:12.5px}
.clp{font-family:var(--f-mono);font-size:11px;color:var(--ink-4);width:38px;text-align:right}
.ckey{display:flex;flex-wrap:wrap;gap:7px 15px;margin-top:14px;
font:600 11px/1 var(--f-body);color:var(--ink-3)}
.ckey span{display:inline-flex;align-items:center;gap:6px}
.ckey i{width:9px;height:9px;border-radius:2.5px;display:block}
/* Redrawing because a switch moved should not slide the page in again. The
   charts still replay, and that is the part carrying the change. */
.page.noanim{animation:none}
@media (max-width:560px){
.cchart{gap:5px}
.clab{font-size:9.5px}
.csub{font-size:11px}
}


/* ---------------- sign in ----------------
   The gate box was built for a keypad. It now holds a Google button, an invite
   code, or an error, so it needs to breathe a bit more than it did. */
.gbtn{display:flex;justify-content:center;margin:22px 0 6px;min-height:44px}
.gwait{font:600 13px/1 var(--f-body);color:var(--ink-3);padding:13px}
.glink{background:none;border:0;color:var(--ink-3);font:600 12.5px/1 var(--f-body);
cursor:pointer;padding:10px;margin-top:6px;text-decoration:underline;
text-underline-offset:3px}
.glink:hover{color:var(--brass)}
.gcode{width:100%;margin:18px 0 4px;padding:14px;text-align:center;
font:700 22px/1 var(--f-mono);letter-spacing:.32em;text-indent:.32em;
border:1px solid var(--line-2);border-radius:var(--r);background:var(--bg-2);color:var(--ink)}
.gcode:focus{outline:0;border-color:var(--brass);box-shadow:var(--glow)}
.gfound{padding:13px;border:1px solid var(--line);border-radius:var(--r);
background:var(--panel-2);margin-top:12px}
.gfound b{display:block;font-size:15px}
.gfound span{display:block;font-size:12px;color:var(--ink-3);margin-top:3px}

/* An invite code is read out loud and typed on a phone, so it gets spacing. */
.invcode{font-family:var(--f-mono);letter-spacing:.14em}
.invbig{font:700 30px/1 var(--f-mono);letter-spacing:.22em;text-align:center;
padding:22px 10px;margin:16px 0;border:1px dashed var(--line-2);border-radius:var(--r);
background:var(--panel-2);color:var(--brass);word-break:break-all}

/* Signing up is the one screen with no app behind it yet, so everything that
   navigates gets out of the way. */
body.signup .tabs,body.signup .btmnav,body.signup .whoswitch,
body.signup #syncSlot,body.signup #settings{display:none}
body.signup{padding-bottom:20px}
body.signup .wrap{padding-top:34px}

/* ---------------- signup wizard ----------------
   Same components as the rest of the app, just given room. Somebody is doing
   this once and every question has to look answerable. */
.setup{max-width:720px;margin:0 auto}
.setuphead{margin-bottom:26px}
.setuphead h1{font-size:29px;letter-spacing:-.03em;margin:0 0 8px}
.setuphead p{color:var(--ink-3);margin:0;max-width:62ch}
.setupbar{height:3px;background:var(--panel-2);border-radius:99px;overflow:hidden;margin-bottom:16px}
.setupbar i{display:block;height:100%;background:var(--brass);border-radius:99px;
transition:width .45s var(--ez)}
.setupstep{font:700 9.5px/1 var(--f-body);letter-spacing:.2em;text-transform:uppercase;
color:var(--ink-4);margin:0 0 10px}
.setupfoot{display:flex;gap:10px;justify-content:flex-end;margin-top:30px;
padding-top:20px;border-top:1px solid var(--line)}
.picks{display:grid;gap:9px;grid-template-columns:repeat(auto-fit,minmax(216px,1fr))}
.pick{text-align:left;padding:14px 16px;border:1px solid var(--line-2);border-radius:var(--r);
background:var(--panel);cursor:pointer;transition:.18s var(--ez);color:var(--ink)}
.pick:hover{border-color:var(--brass);transform:translateY(-1px)}
.pick b{display:block;font-size:14px;font-weight:600}
.pick span{display:block;font-size:12px;color:var(--ink-3);margin-top:4px;line-height:1.45}
.pick.on{border-color:var(--brass);background:var(--panel-2);box-shadow:var(--glow)}
.pick.on b{color:var(--brass)}
@media (max-width:560px){
.setuphead h1{font-size:23px}
.picks{grid-template-columns:1fr}
}

@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
"""
