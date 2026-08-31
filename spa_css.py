# -*- coding: utf-8 -*-
APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
--bg:#0B0C0E;--bg-2:#101216;--panel:#131518;--panel-2:#1B1E23;--raise:#22262C;
--line:#262A31;--line-2:#333942;
--ink:#EAE6DE;--ink-2:#B9B4AA;--ink-3:#8D939C;--ink-4:#5E646D;
--brass:#C2A24B;--brass-2:#D9994F;--amber:#C88A45;
--sage:#7FA87F;--steel:#6E8CA8;--clay:#B85C46;
--r:10px;--r-s:7px;--r-l:16px;
--sh:0 1px 2px rgba(0,0,0,.4);
--sh-2:0 4px 14px rgba(0,0,0,.45);
--sh-3:0 18px 48px rgba(0,0,0,.6);
--ez:cubic-bezier(.2,.7,.3,1);
--f-body:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
--f-disp:'Fraunces','Iowan Old Style',Georgia,serif;
--f-mono:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace;}
html[data-theme="light"]{
--bg:#FAF8F4;--bg-2:#F2EEE6;--panel:#FFFFFF;--panel-2:#F4F1EA;--raise:#EAE5DA;
--line:#E2DDD1;--line-2:#CFC8B8;
--ink:#1A1814;--ink-2:#413C33;--ink-3:#6E675A;--ink-4:#938C7C;
--brass:#8A6D18;--brass-2:#A2811F;--amber:#9A6B21;
--sage:#3E7A50;--steel:#3F6285;--clay:#A2432A;
--sh:0 1px 2px rgba(26,24,20,.06);
--sh-2:0 4px 14px rgba(26,24,20,.10);
--sh-3:0 18px 48px rgba(26,24,20,.20);}
html[data-theme="light"] body{
background-image:radial-gradient(ellipse 900px 500px at 12% -6%,rgba(138,109,24,.07),transparent 60%),
radial-gradient(ellipse 700px 400px at 92% 2%,rgba(63,98,133,.06),transparent 60%);}
html[data-theme="light"] .top{background:rgba(250,248,244,.88)}
html[data-theme="light"] .btmnav{background:rgba(250,248,244,.96)}
html[data-theme="light"] .tab.on{color:#fff}
html[data-theme="light"] .b{color:#fff}
html[data-theme="light"] .b.o{color:var(--ink)}
html[data-theme="light"] .b.dz{color:var(--clay)}
html[data-theme="light"] .b.o:hover{color:var(--brass-2)}
html[data-theme="light"] .day.sel .dn,html[data-theme="light"] .day.sel .dk,
html[data-theme="light"] .day.sel .dev{color:#fff}
html[data-theme="light"] .day.sel .dev:before{background:rgba(255,255,255,.7)}
html[data-theme="light"] .toast{color:#fff}
html[data-theme="light"] .pill.on{color:#fff}
html[data-theme="light"] .rcbadge{background:rgba(255,255,255,.9);color:var(--ink-2)}
html[data-theme="light"] .fav{background:rgba(255,255,255,.92)}
html[data-theme="light"] .aisle{background:var(--ink);color:#fff}
html[data-theme="light"] .aisle span{color:var(--brass-2)}
html[data-theme="light"] .stat.acc{background:linear-gradient(150deg,#FBF3DC,#F5EBD0)}
html[data-theme="light"] .dhero .scrim{
background:linear-gradient(to top,rgba(20,18,14,.92),rgba(20,18,14,.45) 55%,rgba(20,18,14,.2))}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;background:var(--bg);transition:background .3s var(--ez)}
body{transition:background-color .3s var(--ez),color .3s var(--ez)}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.6 var(--f-body);padding-bottom:88px;
background-image:radial-gradient(ellipse 900px 500px at 12% -6%,rgba(194,162,75,.07),transparent 60%),
radial-gradient(ellipse 700px 400px at 92% 2%,rgba(110,140,168,.055),transparent 60%);
background-attachment:fixed}
a{color:var(--brass);text-decoration:none}
button,input,select,textarea{font:inherit;color:inherit}
h1,h2,h3,h4{margin:0;font-family:var(--f-disp);font-weight:600;letter-spacing:-.02em;line-height:1.14}
.wrap{max-width:1200px;margin:0 auto;padding:0 22px}
.lbl,.eyebrow{font:700 9.5px/1 var(--f-body);letter-spacing:.2em;text-transform:uppercase;color:var(--ink-4)}
.mono{font-family:var(--f-mono);font-variant-numeric:tabular-nums}

/* top bar */
.top{position:sticky;top:0;z-index:60;background:rgba(11,12,14,.86);
backdrop-filter:saturate(150%) blur(16px);-webkit-backdrop-filter:saturate(150%) blur(16px);
border-bottom:1px solid var(--line)}
.topin{max-width:1200px;margin:0 auto;padding:12px 22px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;min-width:0}
.brand{flex:0 0 auto}
.tabs{flex:1 1 auto;justify-content:flex-end;flex-wrap:wrap}
.whoswitch{flex:0 0 auto}
.brand{font-family:var(--f-disp);font-weight:700;font-size:18px;letter-spacing:-.03em;color:var(--ink);
white-space:nowrap;display:flex;align-items:center;gap:9px}
.brand:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--brass);
box-shadow:0 0 0 3px rgba(194,162,75,.16),0 0 14px rgba(194,162,75,.5)}
.brand em{font-style:normal;color:var(--ink-3);font-weight:500}
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
.btmnav{display:none;position:fixed;left:0;right:0;bottom:0;z-index:70;background:rgba(11,12,14,.95);
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
.phead{padding:36px 0 20px;max-width:68ch;border-bottom:1px solid var(--line);margin-bottom:26px}
.phead h1{font-size:clamp(28px,4.2vw,44px);letter-spacing:-.035em}
.phead p{color:var(--ink-3);margin:10px 0 0;font-size:16px;line-height:1.55}
.sec{margin:34px 0}
.sec>h2{font-size:21px;letter-spacing:-.028em;margin-bottom:3px;min-width:0;overflow-wrap:break-word}
.sec>.sub{color:var(--ink-3);font-size:13.5px;margin:0 0 14px;max-width:72ch}
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
.stat.acc{background:linear-gradient(150deg,#2A2312,#1A1710)}
.stat.acc b{color:var(--brass);font-size:29px}
.stat.acc span{color:rgba(194,162,75,.62)}
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
.b{border:1px solid var(--brass);background:var(--brass);color:#15130C;font-weight:700;font-size:13.5px;
padding:9px 17px;border-radius:999px;cursor:pointer;transition:.2s var(--ez);display:inline-flex;
align-items:center;gap:7px;justify-content:center}
.b:hover{background:var(--brass-2);border-color:var(--brass-2);transform:translateY(-1px);box-shadow:var(--sh-2)}
.b:active{transform:none}
.b.o{background:transparent;color:var(--ink-2);border-color:var(--line-2);font-weight:600}
.b.o:hover{background:var(--panel-2);border-color:var(--brass);color:var(--brass)}
.b.s{padding:6px 12px;font-size:12px}
.b.dz{background:transparent;color:var(--clay);border-color:#4A2E27}
.b.dz:hover{background:rgba(184,92,70,.12);border-color:var(--clay);color:var(--clay)}
.b:disabled{opacity:.4;cursor:not-allowed;transform:none}

/* fields */
.f{display:block;margin-bottom:13px}
.f>span{display:block;font:700 9.5px/1 var(--f-body);letter-spacing:.18em;text-transform:uppercase;
color:var(--ink-4);margin-bottom:6px}
.f input,.f select,.f textarea{width:100%;padding:10px 12px;border:1px solid var(--line-2);
border-radius:var(--r-s);background:var(--bg-2);color:var(--ink);font-weight:500;transition:.16s var(--ez)}
.f input:focus,.f select:focus,.f textarea:focus{outline:0;border-color:var(--brass);
box-shadow:0 0 0 3px rgba(194,162,75,.16)}
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
.rcbadge{position:absolute;left:11px;top:11px;background:rgba(11,12,14,.72);color:var(--ink-2);
font:700 9px/1 var(--f-mono);letter-spacing:.1em;padding:5px 8px;border-radius:4px;
border:1px solid rgba(255,255,255,.1)}
.rcb{padding:14px 15px 15px;display:flex;flex-direction:column;flex:1}
.rcn{font-family:var(--f-disp);font-size:16px;font-weight:600;letter-spacing:-.02em;line-height:1.24;
color:var(--ink);margin-bottom:9px}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:11px}
.chip{font:600 10.5px/1 var(--f-body);padding:5px 8px;border-radius:5px;background:var(--panel-2);
color:var(--ink-2);white-space:nowrap;border:1px solid var(--line)}
.chip.t{background:rgba(127,168,127,.14);color:var(--sage);border-color:rgba(127,168,127,.28)}
.chip.d1{background:rgba(127,168,127,.14);color:var(--sage);border-color:rgba(127,168,127,.28)}
.chip.d2{background:rgba(194,162,75,.13);color:var(--brass);border-color:rgba(194,162,75,.28)}
.chip.d3{background:rgba(184,92,70,.14);color:var(--clay);border-color:rgba(184,92,70,.3)}
.chip.p{font-family:var(--f-mono)}
.rcm{display:grid;grid-template-columns:repeat(4,1fr);margin-top:auto;border-top:1px solid var(--line);padding-top:11px}
.rcm div{text-align:center;border-right:1px solid var(--line)}
.rcm div:last-child{border-right:0}
.rcm b{display:block;font-family:var(--f-mono);font-size:15px;font-weight:700;color:var(--ink)}
.rcm span{font:700 8px/1 var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-4);
display:block;margin-top:4px}
.fav{position:absolute;right:10px;top:10px;width:30px;height:30px;border-radius:50%;border:1px solid var(--line);
background:rgba(11,12,14,.72);color:var(--ink-4);font-size:14px;cursor:pointer;line-height:1;
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
.day{min-height:96px;border:1px solid var(--line);border-radius:var(--r-s);background:var(--panel);
padding:6px 7px;cursor:pointer;display:flex;flex-direction:column;transition:.18s var(--ez);
position:relative;overflow:hidden;text-align:left}
.day:hover{border-color:var(--brass);transform:translateY(-2px)}
.day.out{opacity:0;pointer-events:none}
.day.today{border-color:var(--brass)}
.day.sel{background:var(--brass);border-color:var(--brass)}
.day.sel .dn,.day.sel .dk{color:#15130C}
.dn{font-family:var(--f-mono);font-size:13px;font-weight:700;color:var(--ink)}
.dk{font:600 9px/1 var(--f-mono);color:var(--ink-4);margin-top:auto}
.devs{margin-top:5px;display:flex;flex-direction:column;gap:2px;overflow:hidden}
.dev{font:600 9.5px/1.25 var(--f-body);color:var(--ink-2);white-space:nowrap;overflow:hidden;
text-overflow:ellipsis;padding-left:8px;position:relative}
.dev:before{content:"";position:absolute;left:0;top:4px;width:4px;height:4px;border-radius:50%;background:var(--steel)}
.dev.w:before{background:var(--sage)}.dev.m:before{background:var(--amber)}
.day.sel .dev{color:rgba(21,19,12,.82)}
.day.sel .dev:before{background:rgba(21,19,12,.6)}
.dmore{font:600 9px/1 var(--f-body);color:var(--ink-4);padding-left:8px}
.dots{display:flex;gap:2px;margin-top:3px;flex-wrap:wrap}
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
.mask{position:fixed;inset:0;background:rgba(5,6,7,.72);backdrop-filter:blur(5px);z-index:200;
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
color:#15130C;padding:12px 22px;border-radius:999px;font-size:13.5px;font-weight:700;z-index:300;
box-shadow:var(--sh-3);animation:pop .26s var(--ez)}

/* error panel */
.errbox{background:rgba(184,92,70,.10);border:1px solid var(--clay);border-radius:var(--r);
padding:20px 22px;margin:24px 0}
.errbox h3{color:var(--clay);font-size:17px;margin-bottom:8px}
.errbox pre{background:var(--bg-2);border:1px solid var(--line);border-radius:var(--r-s);
padding:12px;overflow:auto;font:500 12px/1.5 var(--f-mono);color:var(--ink-2);margin:10px 0 0}

/* misc */
.pill{display:inline-block;background:var(--panel);color:var(--ink-2);border-radius:999px;padding:6px 14px;
font-size:12.5px;font-weight:600;cursor:pointer;border:1px solid var(--line);transition:.18s var(--ez)}
.pill:hover{border-color:var(--brass);color:var(--brass)}
.pill.on{background:var(--brass);color:#15130C;border-color:var(--brass)}
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
text-transform:uppercase;color:var(--clay);background:rgba(184,92,70,.12);border:1px solid rgba(184,92,70,.3);
padding:5px 10px;border-radius:999px}
.dirty:before{content:"";width:6px;height:6px;border-radius:50%;background:var(--clay)}

@media (max-width:860px){
.wrap{padding:0 15px}
body{padding-bottom:80px}
.tabs{display:none}
.btmnav{display:flex}
.topin{padding:10px 15px;gap:10px}
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
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
"""
