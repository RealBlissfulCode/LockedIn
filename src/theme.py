# -*- coding: utf-8 -*-
"""Blue design system for the handbook. Replaces the old neutral CSS."""

CSS = """
<style>
:root{
  --navy:#0B1F3A;      /* deepest, headers and rules */
  --steel:#12365F;     /* primary blue */
  --azure:#1E6FD9;     /* accent, links, active */
  --ice:#EAF1FA;       /* pale fill */
  --mist:#F5F8FC;      /* page-level fill */
  --line:#C9D8EC;      /* borders */
  --ink:#0E1A26;       /* body text */
  --mut:#5A6B80;       /* secondary text */
  --warn:#B4442A;      /* the one non-blue: celiac and hard warnings */
}
*{box-sizing:border-box}
body{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  color:var(--ink);line-height:1.58;margin:0 auto;padding:0 24px 90px;
  max-width:1040px;font-size:15px;background:#fff;
}

/* ---------- masthead ---------- */
.masthead{
  background:linear-gradient(160deg,var(--navy) 0%,var(--steel) 62%,#1B4B85 100%);
  color:#fff;margin:0 -24px 30px;padding:44px 34px 34px;
}
.masthead h1{color:#fff;font-size:38px;line-height:1.1;letter-spacing:-1px;margin:0 0 8px;border:0}
.masthead .lead{color:#BBD3F0;font-size:16px;margin:0}
.masthead .rule{height:3px;width:64px;background:var(--azure);margin:18px 0 0;border-radius:2px}
.statline{display:flex;flex-wrap:wrap;gap:0;margin:26px 0 0;border-top:1px solid rgba(255,255,255,.18);padding-top:20px}
.statline div{flex:1;min-width:96px;padding-right:14px}
.statline b{display:block;font-size:24px;color:#fff;letter-spacing:-.5px;line-height:1.1}
.statline span{font-size:10.5px;text-transform:uppercase;letter-spacing:1px;color:#8FB4E0}

/* ---------- headings ---------- */
h1{font-size:30px;letter-spacing:-.5px;margin:34px 0 6px;color:var(--navy)}
h2{font-size:23px;margin:52px 0 14px;padding:0 0 9px;color:var(--navy);
   border-bottom:3px solid var(--steel);letter-spacing:-.3px;font-weight:700}
h3{font-size:17.5px;margin:28px 0 8px;color:var(--steel);font-weight:650}
h4{font-size:12px;text-transform:uppercase;letter-spacing:1.1px;color:var(--azure);
   margin:18px 0 6px;font-weight:700}
p,li{font-size:14.5px}
a{color:var(--azure);text-decoration:none}
a:hover{text-decoration:underline}
.lead{font-size:16px;color:var(--mut)}
.small{font-size:13px;color:var(--mut)}
.hh{color:var(--mut);font-weight:400;font-size:12.5px}
.meta{color:var(--mut);font-size:12.5px;margin:2px 0 10px}
.printnote{font-size:12.5px;color:var(--mut);font-style:italic}

/* ---------- tables ---------- */
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13px}
th{background:var(--steel);color:#fff;text-align:left;font-weight:600;font-size:11px;
   text-transform:uppercase;letter-spacing:.7px;border:1px solid var(--steel)}
th,td{border:1px solid var(--line);padding:7px 9px;vertical-align:top}
tbody tr:nth-child(even) td{background:var(--mist)}
table.idx td{padding:5px 7px;font-size:12.5px}
table.idx td.tg{font-size:10px;color:var(--mut);letter-spacing:.2px}
table.idx tbody tr:hover td{background:var(--ice)}
table.idx td b{color:var(--navy)}
table.micro td{font-size:12.5px}
table.scale{width:auto;font-size:12px}
td.w{background:#FCEDE9}
table.targets td:first-child{font-weight:600;color:var(--navy)}
table.track td,table.blank td.fill{height:27px;background:#fff}

/* ---------- callouts ---------- */
.banner{background:var(--ice);border:1px solid var(--line);border-left:4px solid var(--steel);
  padding:14px 18px;margin:20px 0;font-size:13.5px;border-radius:0 4px 4px 0}
.callout{background:var(--mist);border:1px solid var(--line);border-left:4px solid var(--azure);
  padding:16px 20px;margin:22px 0;border-radius:0 4px 4px 0}
.callout h4{margin-top:0}
.callout.warn{background:#FDF1EE;border-color:#EFC9BE;border-left-color:var(--warn)}
.callout.warn h4{color:var(--warn)}
.formula{background:var(--ice);border-left:4px solid var(--azure);padding:11px 16px;
  font-weight:600;color:var(--navy);border-radius:0 4px 4px 0}

/* ---------- table of contents ---------- */
.toc{columns:2;column-gap:34px;font-size:13.5px;background:var(--mist);
  border:1px solid var(--line);border-radius:5px;padding:18px 22px;margin:20px 0}
.toc a{display:block;padding:3.5px 0;border-bottom:1px solid rgba(201,216,236,.5);
  break-inside:avoid;color:var(--steel)}

/* ---------- tags ---------- */
.tags{margin:0 0 12px;line-height:2.1}
.tag{display:inline-block;font-size:9.5px;letter-spacing:.6px;padding:2.5px 8px;border-radius:11px;
  border:1px solid var(--line);background:var(--mist);color:var(--steel);margin-right:4px;
  white-space:nowrap;font-weight:600;text-transform:uppercase}
.t-prot{background:#DCE9FA;border-color:#9EC0EA;color:#0F3F7D}
.t-leu{background:#0B1F3A;border-color:#0B1F3A;color:#7FD4FF}
.t-cal{background:#E4EDF9;border-color:#A9C6E8;color:#144A87}
.t-lowcal{background:#EDF4FC;border-color:#C2D8EF;color:#3F6B99}
.t-fib{background:#DFF0F6;border-color:#A5CFDE;color:#0F5570}
.t-fat{background:#E6EEF7;border-color:#B0C8E0;color:#274B70}
.t-mus{background:#1E6FD9;border-color:#1E6FD9;color:#fff}
.t-rec{background:#D9F0F8;border-color:#9FD2E5;color:#0D5772}
.t-fast{background:#E7E9F8;border-color:#BEC4EA;color:#33409C}
.t-budget{background:#EFF3F7;border-color:#C6D2DE;color:#405568}
.t-carb,.t-bal,.t-sat,.t-quick,.t-veg,.t-gf,.t-micro,.t-def{
  background:#F2F5F9;border-color:#D3DFEC;color:#4C6076}
.d-E{color:#1B6FA8;font-weight:700}
.d-M{color:#2E5C8A;font-weight:700}
.d-A{color:#0B1F3A;font-weight:700}

/* ---------- recipe block ---------- */
.recipe{border-top:2px solid var(--line);padding:24px 0 10px;page-break-inside:avoid}
.recipe h3{margin-top:0}
.recipe h3 .rid{display:inline-block;background:var(--steel);color:#fff;font-size:11px;
  font-weight:700;letter-spacing:.8px;padding:3px 9px;border-radius:3px;margin-right:9px;
  vertical-align:middle;font-family:ui-monospace,Menlo,Consolas,monospace}
.macrobar{display:flex;gap:7px;margin:12px 0 16px;flex-wrap:wrap}
.macrobar div{flex:1;min-width:84px;background:var(--mist);border:1px solid var(--line);
  border-top:3px solid var(--steel);border-radius:4px;padding:9px 4px;text-align:center;
  font-size:10px;text-transform:uppercase;letter-spacing:.7px;color:var(--mut);font-weight:600}
.macrobar div:first-child{border-top-color:var(--azure)}
.macrobar span{display:block;font-size:19px;color:var(--navy);font-weight:700;letter-spacing:-.5px}
.cols{display:flex;gap:30px;flex-wrap:wrap}
.cols>div{flex:1;min-width:270px}
ul.ing{padding-left:19px}
ul.ing li{margin-bottom:3px}
ul.ing b{color:var(--navy)}
ol.steps{padding-left:21px;counter-reset:none}
ol.steps li{margin-bottom:8px}
.back{font-size:11.5px;color:var(--mut);margin-top:14px}
.back a{color:var(--mut)}
code{background:var(--ice);padding:1px 6px;border-radius:3px;font-size:13px;color:var(--navy)}

@media print{
  body{font-size:10pt;max-width:none;padding:0}
  .masthead{margin:0 0 18pt;padding:26pt 22pt;background:var(--navy)!important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact}
  .masthead h1{font-size:26pt}
  th{background:var(--steel)!important;color:#fff!important;
    -webkit-print-color-adjust:exact;print-color-adjust:exact}
  .recipe{page-break-inside:avoid}
  h2{page-break-after:avoid;page-break-before:always}
  h2#howto,h2#toc{page-break-before:auto}
  .macrobar{display:block}
  .macrobar div{display:inline-block;width:15%;margin-right:4px;vertical-align:top}
  .cols{display:block}
  .cols>div{display:inline-block;width:47%;vertical-align:top;margin-right:2%}
  .toc{columns:auto}
  table.idx td{font-size:8.5pt}
  table.idx td.tg{font-size:7pt}
  a{color:var(--navy)}
}
</style>"""


EXTRA = """
<style>
/* ---------- cover ---------- */
.cover{background:linear-gradient(155deg,#050F1E 0%,var(--navy) 40%,var(--steel) 78%,#215691 100%);
  color:#fff;margin:0 -24px 0;padding:0;min-height:96vh;display:flex;align-items:center;
  position:relative;overflow:hidden}
.cover:before{content:"";position:absolute;right:-14%;top:-18%;width:62%;height:78%;
  background:radial-gradient(circle at 50% 50%,rgba(30,111,217,.42),transparent 62%)}
.cover:after{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;
  background:linear-gradient(90deg,var(--azure),#7FD4FF,var(--azure))}
.coverinner{position:relative;padding:0 44px;max-width:860px}
.eyebrow{font-size:11px;letter-spacing:3.2px;text-transform:uppercase;color:#79A7DE;margin:0 0 26px}
.cover h1{font-size:78px;line-height:.94;letter-spacing:-3px;color:#fff;margin:0 0 22px;
  font-weight:800;border:0}
.subtitle{font-size:18px;line-height:1.5;color:#C4DAF3;max-width:560px;margin:0 0 40px}
.coverstats{display:flex;gap:0;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.2);
  border-bottom:1px solid rgba(255,255,255,.2);padding:22px 0;margin:0 0 26px;max-width:620px}
.coverstats div{flex:1;min-width:110px}
.coverstats b{display:block;font-size:36px;letter-spacing:-1.5px;line-height:1;color:#fff}
.coverstats span{font-size:10px;letter-spacing:1.6px;text-transform:uppercase;color:#79A7DE}
.coverfoot{font-size:12.5px;color:#8FB4E0;max-width:540px;line-height:1.6;margin:0}

/* ---------- sticky nav ---------- */
.topnav{position:sticky;top:0;z-index:50;background:rgba(11,31,58,.97);
  backdrop-filter:saturate(160%) blur(8px);margin:0 -24px 0;padding:9px 24px;
  border-bottom:1px solid rgba(255,255,255,.12);white-space:nowrap;overflow-x:auto}
.topnav a{color:#BBD3F0;font-size:11.5px;letter-spacing:.5px;text-transform:uppercase;
  font-weight:600;padding:6px 13px;border-radius:20px;display:inline-block}
.topnav a:hover{background:rgba(30,111,217,.30);color:#fff;text-decoration:none}

/* ---------- calculator ---------- */
.calcwrap{border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:22px 0;
  box-shadow:0 2px 14px rgba(11,31,58,.07)}
.calcinputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;
  background:var(--mist);padding:20px 22px;border-bottom:1px solid var(--line)}
.calcinputs label{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:1px;
  color:var(--mut);font-weight:700}
.calcinputs input,.calcinputs select{display:block;width:100%;margin-top:5px;padding:8px 10px;
  border:1px solid var(--line);border-radius:5px;font-size:14px;font-family:inherit;
  color:var(--navy);background:#fff;font-weight:600}
.calcinputs input:focus,.calcinputs select:focus{outline:2px solid var(--azure);border-color:var(--azure)}
.calcout{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:0;
  background:var(--navy)}
.cocard{padding:20px 14px;text-align:center;border-right:1px solid rgba(255,255,255,.10)}
.cocard:last-child{border-right:0}
.cocard span{display:block;font-size:27px;font-weight:800;color:#fff;letter-spacing:-1px;line-height:1}
.cocard em{display:block;font-style:normal;font-size:9.5px;letter-spacing:1.4px;
  text-transform:uppercase;color:#79A7DE;margin-top:7px}
.cocard.big{background:var(--azure)}
.cocard.big span{font-size:36px}
.cocard.big em{color:#D6E8FF}
table.calcdetail{margin:0;font-size:12.5px}
table.calcdetail th{border-radius:0}
table.calcdetail td:nth-child(2){font-weight:700;color:var(--navy);white-space:nowrap}
table.calcdetail td:nth-child(3){color:var(--mut);font-size:11.5px}

/* ---------- highlighted rows ---------- */
tr.hl td{background:#DCE9FA !important;border-color:#9EC0EA}
tr.hl td:first-child{box-shadow:inset 4px 0 0 var(--azure)}

@media print{
  .cover{min-height:auto;padding:60pt 0;page-break-after:always;
    background:var(--navy)!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .cover h1{font-size:52pt}
  .topnav{display:none}
  .calcout{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .calcinputs{display:block}
  .calcinputs label{display:inline-block;width:30%;margin:0 2% 8pt 0;vertical-align:top}
  tr.hl td{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>"""


EXTRA2 = """
<style>
/* ================= density pass ================= */
body{max-width:1220px;padding:0 26px 70px;font-size:15.5px;line-height:1.52;
  background:#fff;
  background-image:radial-gradient(circle at 1px 1px, rgba(18,54,95,.055) 1px, transparent 0);
  background-size:26px 26px;background-attachment:fixed}
.cover,.topnav{margin-left:-26px;margin-right:-26px}

/* section headers become bands, not floating text */
h2{position:relative;font-size:25px;margin:0 -26px 20px;padding:26px 26px 20px;
  border-bottom:0;background:linear-gradient(100deg,var(--navy) 0%,var(--steel) 58%,#1B4B85 100%);
  color:#fff;letter-spacing:-.4px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h2:after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;
  background:linear-gradient(90deg,var(--azure) 0%,#7FD4FF 45%,rgba(127,212,255,0) 100%)}
h3{font-size:18px;margin:30px 0 9px;padding-left:12px;border-left:4px solid var(--azure);
  line-height:1.25}
h4{margin:16px 0 5px}
p{margin:0 0 11px}
table{margin:10px 0 16px}
th,td{padding:6px 9px}

/* prose in two columns on wide screens kills the white gutter */
.twocol{columns:2;column-gap:38px;column-rule:1px solid var(--line)}
.twocol p{break-inside:avoid}

/* ================= content cards ================= */
.callout,.banner{border-radius:6px;box-shadow:0 1px 6px rgba(11,31,58,.06);margin:16px 0}
.formula{border-radius:6px;font-size:14.5px}

/* pull quotes / key numbers between sections */
.stripe{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:20px 0}
.stripe div{background:var(--mist);padding:15px 14px}
.stripe b{display:block;font-size:23px;color:var(--navy);letter-spacing:-.7px;line-height:1.1}
.stripe span{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:var(--mut);
  display:block;margin-top:5px}

/* ================= index tables ================= */
table.idx{font-size:12.5px}
table.idx thead th{position:sticky;top:44px;z-index:5}
table.idx td{padding:4px 7px}
table.idx tbody tr:nth-child(even) td{background:#F7FAFD}
table.idx tbody tr:hover td{background:var(--ice)}

/* ================= recipe grid ================= */
@media screen and (min-width:1000px){
  .rgrid{column-count:2;column-gap:30px}
  .rgrid .recipe{break-inside:avoid;display:inline-block;width:100%}
}
.recipe{border-top:0;border:1px solid var(--line);border-radius:7px;padding:16px 18px 10px;
  margin:0 0 20px;background:#fff;box-shadow:0 1px 5px rgba(11,31,58,.05)}
.recipe h3{border-left:0;padding-left:0;margin:0 0 4px;font-size:16.5px}
.recipe .meta{font-size:11.5px;margin:0 0 7px}
.recipe .tags{line-height:1.9;margin-bottom:9px}
.recipe h4{font-size:10.5px;margin:13px 0 4px}
.macrobar{gap:5px;margin:9px 0 12px}
.macrobar div{min-width:62px;padding:7px 3px;font-size:9px;border-radius:3px}
.macrobar span{font-size:16px}
.cols{gap:20px}
.cols>div{min-width:190px}
ul.ing li,ol.steps li{font-size:13px;margin-bottom:3px}
.recipe .small{font-size:12.5px}
.recipe ul.small{padding-left:17px;margin:3px 0 0}

/* category dividers inside the library */
.catrule{margin:34px 0 18px;padding:12px 18px;background:var(--navy);color:#fff;border-radius:6px;
  font-size:15px;font-weight:700;letter-spacing:.4px;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.catrule span{float:right;color:#79A7DE;font-weight:600;font-size:12px;letter-spacing:1px;
  text-transform:uppercase;padding-top:3px}

/* toc denser */
.toc{columns:3;column-gap:26px;padding:16px 20px;font-size:13px}

@media print{
  body{background-image:none;font-size:9.5pt}
  h2{margin:0 0 12pt;padding:14pt 12pt 11pt;font-size:17pt}
  .twocol{columns:2}
  .rgrid{column-count:2;column-gap:16pt}
  .rgrid .recipe{break-inside:avoid}
  .recipe{box-shadow:none;padding:8pt 9pt 4pt;margin-bottom:9pt}
  .recipe h3{font-size:11.5pt}
  ul.ing li,ol.steps li{font-size:8.5pt}
  .toc{columns:3}
  table.idx thead th{position:static}
  .catrule{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style>"""


EXTRA3 = """
<style>
/* ============ full-bleed layout ============ */
html{overflow-x:hidden}
body{max-width:none;width:100%;padding:0 var(--gut) 70px;margin:0;
  --gut:clamp(20px,3.2vw,64px)}

/* anything that should touch both edges of the window */
.cover,.topnav,h2,.catrule{
  width:100vw;
  margin-left:calc(50% - 50vw);
  margin-right:calc(50% - 50vw);
}

/* re-inset their inner text so it lines up with the body column */
.topnav{padding-left:var(--gut);padding-right:var(--gut)}
h2{padding-left:var(--gut);padding-right:var(--gut);margin-top:0;margin-bottom:22px}
.catrule{padding-left:var(--gut);padding-right:var(--gut);border-radius:0}
.catrule span{padding-right:0}

.cover{min-height:100vh;padding:0}
.coverinner{max-width:1500px;margin:0 auto;padding:0 var(--gut);width:100%}
.cover h1{font-size:clamp(54px,7.4vw,116px);line-height:.92;letter-spacing:-4px;margin-bottom:26px}
.subtitle{font-size:clamp(16px,1.35vw,22px);max-width:720px}
.coverstats{max-width:900px;padding:26px 0}
.coverstats b{font-size:clamp(32px,3.4vw,52px)}
.coverfoot{max-width:760px;font-size:13.5px}
.eyebrow{font-size:clamp(11px,.9vw,14px);letter-spacing:4px}

/* ============ use the extra width ============ */
@media screen and (min-width:1450px){
  .rgrid{column-count:3;column-gap:26px}
  .toc{columns:4}
  .calcinputs{grid-template-columns:repeat(9,1fr)}
}
@media screen and (min-width:1900px){
  .rgrid{column-count:4}
  .toc{columns:5}
}
.calcwrap{max-width:none}
.stripe{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}
table.idx thead th{top:44px}

/* keep running prose readable without leaving a dead right margin */
.twocol{columns:2;column-gap:44px}
@media screen and (min-width:1500px){.twocol{columns:3}}

@media print{
  html,body{overflow-x:visible}
  body{max-width:none;padding:0;--gut:10pt}
  .cover,h2,.catrule{width:auto;margin-left:0;margin-right:0}
  .cover{min-height:auto}
  .cover h1{font-size:54pt;letter-spacing:-2pt}
  .coverinner{padding:0 26pt}
  .rgrid{column-count:2 !important}
  .toc{columns:3 !important}
  h2{padding-left:12pt;padding-right:12pt}
  .catrule{padding-left:12pt;padding-right:12pt}
}
</style>"""


EXTRA4 = """
<style>
/* float-based cover columns: works in modern browsers and the PDF engine alike */
.coverinner:after{content:"";display:table;clear:both}
.coverleft,.coverright{min-width:0}
@media screen and (min-width:1050px){
  .coverleft{float:left;width:57%}
  .coverright{float:right;width:37%;
    border-left:1px solid rgba(255,255,255,.18);padding-left:36px}
}
@media screen and (max-width:1049px){
  .coverright{border-top:1px solid rgba(255,255,255,.18);padding-top:26px;margin-top:30px}
}
.subtitle{max-width:640px}
.coverstats{max-width:none}

.panelhead{font-size:10.5px;letter-spacing:3.4px;text-transform:uppercase;color:#79A7DE;
  margin:0 0 12px}
ol.panel{list-style:none;margin:0 0 26px;padding:0}
ol.panel li{border-bottom:1px solid rgba(255,255,255,.10)}
ol.panel a{display:block;padding:7px 0;color:#DCE9FA;font-size:14.5px;font-weight:500}
ol.panel a:hover{color:#fff;text-decoration:none}
ol.panel em{font-style:normal;font-size:10.5px;letter-spacing:1.4px;color:#5C8CC4;
  font-weight:700;margin-right:12px}
.panelnums{overflow:hidden;border:1px solid rgba(255,255,255,.14);border-radius:6px}
.panelnums div{float:left;width:50%;background:rgba(11,31,58,.5);padding:12px 15px;
  border-bottom:1px solid rgba(255,255,255,.12);border-right:1px solid rgba(255,255,255,.12);
  box-sizing:border-box}
.panelnums b{display:block;font-size:21px;color:#fff;letter-spacing:-.6px;line-height:1}
.panelnums span{font-size:9.5px;letter-spacing:1.4px;text-transform:uppercase;color:#79A7DE;
  display:block;margin-top:4px}

@media print{
  .coverleft{float:left;width:57%}
  .coverright{float:right;width:38%;border-left:1px solid rgba(255,255,255,.2);
    padding-left:20pt;border-top:0;margin-top:0;padding-top:0}
  ol.panel a{color:#DCE9FA;font-size:9.5pt;padding:4pt 0}
  .panelnums{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .panelnums b{font-size:14pt}
}
</style>"""


EXTRA5 = """
<style>
/* ============ motion ============ */
html{scroll-behavior:smooth}
.rev{opacity:0;transform:translateY(16px);
  transition:opacity .55s cubic-bezier(.22,.61,.36,1),transform .55s cubic-bezier(.22,.61,.36,1)}
.rev.vis{opacity:1;transform:none}
a,.btn,.tag,.who,.store,.rcard,.fav,ol.panel a{transition:all .22s cubic-bezier(.22,.61,.36,1)}
.rcard:hover{transform:translateY(-3px);box-shadow:0 8px 26px rgba(11,31,58,.14)}
table.idx tbody tr{transition:background .18s ease}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rev{opacity:1;transform:none;transition:none}
  *{animation:none!important}
}

/* ============ app bar ============ */
.appbar{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end;background:var(--navy);
  border-radius:9px;padding:18px 20px;margin:18px 0 8px;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.whoblock.grow{flex:1;min-width:280px}
.wholabel{display:block;font-size:9.5px;letter-spacing:1.6px;text-transform:uppercase;
  color:#79A7DE;margin-bottom:7px;font-weight:700}
.whotoggle{display:inline-flex;background:rgba(255,255,255,.08);border-radius:7px;padding:3px;gap:3px}
.whotoggle button{border:0;background:transparent;color:#BBD3F0;font:600 13px inherit;
  padding:7px 15px;border-radius:5px;cursor:pointer;white-space:nowrap}
.whotoggle button.on{background:var(--azure);color:#fff;box-shadow:0 2px 8px rgba(30,111,217,.4)}
.targetrow{display:flex;flex-wrap:wrap;gap:20px}
.targetrow span{display:block}
.targetrow b{display:block;font-size:19px;color:#fff;letter-spacing:-.5px;line-height:1}
.targetrow i{font-style:normal;font-size:9px;letter-spacing:1.3px;text-transform:uppercase;
  color:#79A7DE;display:block;margin-top:4px}

/* ============ recommender ============ */
.recbox{border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:14px 0 8px}
.recinputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:13px;
  background:var(--mist);padding:18px 20px}
.recinputs label{display:block;font-size:10px;letter-spacing:1.1px;text-transform:uppercase;
  color:var(--mut);font-weight:700}
.recinputs select{display:block;width:100%;margin-top:5px;padding:8px 10px;border:1px solid var(--line);
  border-radius:5px;font:600 14px inherit;color:var(--navy);background:#fff}
.recinputs select:focus{outline:2px solid var(--azure);border-color:var(--azure)}
.recwhy{margin:0;padding:12px 20px;background:var(--ice);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);font-size:13px;color:var(--steel)}
.reccards{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:14px;padding:16px}

/* ============ recipe cards ============ */
.rcard{border:1px solid var(--line);border-radius:8px;background:#fff;padding:13px 14px 11px;
  display:flex;flex-direction:column}
.rcphoto{margin:-13px -14px 10px;height:118px;overflow:hidden;border-radius:8px 8px 0 0}
.rcphoto img{width:100%;height:100%;object-fit:cover;display:block}
.rchead{display:flex;justify-content:space-between;align-items:center}
.rcid{font:700 10px ui-monospace,Menlo,monospace;letter-spacing:1px;background:var(--steel);
  color:#fff;padding:2px 7px;border-radius:3px}
.fav{border:0;background:none;font-size:19px;color:#C9D8EC;cursor:pointer;line-height:1;padding:0}
.fav.on{color:#F2B01E}
.rcname{font-size:14.5px;margin:7px 0 3px;color:var(--navy);line-height:1.25;
  text-transform:none;letter-spacing:0}
.rcmeta{font-size:11.5px;color:var(--mut);margin-bottom:9px}
.rcmeta b{color:var(--azure)}
.rcmac{display:grid;grid-template-columns:repeat(6,1fr);gap:3px;margin-bottom:10px}
.rcmac span{background:var(--mist);border-radius:4px;padding:6px 2px;text-align:center;
  font-size:8px;letter-spacing:.4px;text-transform:uppercase;color:var(--mut);font-weight:700}
.rcmac b{display:block;font-size:13px;color:var(--navy);letter-spacing:-.3px}
.rcacts{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto}
.btn{border:1px solid var(--azure);background:var(--azure);color:#fff;font:600 13px inherit;
  padding:8px 15px;border-radius:6px;cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{background:#1558AE;border-color:#1558AE;text-decoration:none;color:#fff}
.btn.ghost{background:#fff;color:var(--steel);border-color:var(--line)}
.btn.ghost:hover{background:var(--ice);color:var(--navy);border-color:var(--azure)}
.btn.tiny{font-size:11px;padding:5px 10px;border-radius:5px}

/* ============ lists ============ */
.listbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0}
.listgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin:10px 0}
.listcard{border:1px solid var(--line);border-radius:8px;padding:14px 16px;background:#fff}
.listcard header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.listcard h4{margin:0;color:var(--navy);font-size:12px}
.dellist{border:0;background:none;color:var(--mut);font-size:11px;cursor:pointer;text-decoration:underline}
.listcard ul{list-style:none;margin:0;padding:0}
.listcard li{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:13px;
  border-bottom:1px solid var(--mist)}
.listcard li a{flex:1;min-width:0}
.li-meta{font-size:10.5px;color:var(--mut);white-space:nowrap}
.rmitem{border:0;background:none;color:#B4442A;font-size:15px;cursor:pointer;line-height:1;padding:0 2px}
.listtot{margin:9px 0 0;font-size:12px;font-weight:700;color:var(--azure)}

/* ============ my recipes form ============ */
.mineform{border:1px solid var(--line);border-radius:9px;padding:18px 20px;background:var(--mist);margin:12px 0}
.mfrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px}
.mineform label{display:block;font-size:10px;letter-spacing:1.1px;text-transform:uppercase;
  color:var(--mut);font-weight:700;margin-bottom:12px}
.mineform input,.mineform textarea{display:block;width:100%;margin-top:5px;padding:8px 10px;
  border:1px solid var(--line);border-radius:5px;font:400 14px inherit;color:var(--navy);background:#fff}
.mineform textarea{font-size:13.5px;line-height:1.45;resize:vertical}
.mfrow .btn{margin-top:0}
.photoprev{max-width:220px;border-radius:7px;margin:0 0 12px;display:block}

/* ============ price tag in the library ============ */
.pricetag{display:inline-block;background:#E8F5EC;border:1px solid #A9D9BC;color:#14603A;
  border-radius:5px;padding:3px 9px;font-size:11.5px;font-weight:700;margin:0 0 9px}
.pricetag em{font-style:normal;font-weight:600;color:#3E7F5D}

/* ============ phone ============ */
@media screen and (max-width:820px){
  body{font-size:16px;--gut:15px}
  .cover{min-height:auto;padding:52px 0 44px}
  .cover h1{font-size:clamp(42px,12vw,64px);letter-spacing:-2px}
  .subtitle{font-size:16px}
  .coverstats{padding:18px 0}
  .coverstats div{min-width:50%;margin-bottom:14px}
  .coverstats b{font-size:30px}
  .coverleft,.coverright{float:none;width:auto}
  .coverright{border-left:0;padding-left:0;border-top:1px solid rgba(255,255,255,.18);
    padding-top:22px;margin-top:26px}
  .topnav{padding:7px 15px}
  .topnav a{font-size:11px;padding:6px 10px}
  h2{font-size:20px;padding:18px 15px 15px}
  h3{font-size:16.5px}
  .rgrid,.twocol,.toc{column-count:1!important;columns:auto!important}
  .reccards,.listgrid{grid-template-columns:1fr}
  .recinputs,.calcinputs,.mfrow{grid-template-columns:1fr 1fr}
  .calcout{grid-template-columns:repeat(3,1fr)}
  .cocard.big{grid-column:1/-1}
  .appbar{padding:15px}
  .targetrow{gap:14px}
  .whotoggle button{padding:8px 12px;font-size:12.5px}
  table{font-size:12px}
  th,td{padding:5px 6px}
  /* wide data tables scroll instead of squashing */
  table.idx,table.targets,table.calcdetail,table.micro{display:block;overflow-x:auto;
    white-space:nowrap;-webkit-overflow-scrolling:touch}
  table.idx thead th{position:static}
  .stripe{grid-template-columns:1fr 1fr}
  .macrobar div{min-width:0;flex:1 1 30%}
  .cols>div{min-width:0}
  .btn{padding:10px 16px}
}
@media screen and (max-width:430px){
  .recinputs,.calcinputs,.mfrow{grid-template-columns:1fr}
  .rcmac{grid-template-columns:repeat(3,1fr)}
  .calcout{grid-template-columns:repeat(2,1fr)}
}
@media print{
  .appbar,.recbox,.listbar,.mineform,.listgrid,.reccards{display:none!important}
  .rev{opacity:1;transform:none}
}
</style>"""


EXTRA6 = """
<style>
/* phone fixes: explicit sizes, no clamp() so older engines honour them too */
@media screen and (max-width:820px){
  .cover h1{font-size:52px;line-height:.95;letter-spacing:-1.5px;
    overflow-wrap:break-word;word-wrap:break-word;hyphens:auto}
  .coverstats{display:block}
  .coverstats div{display:inline-block;width:48%;vertical-align:top;margin:0 0 16px;min-width:0}
  .coverstats b{font-size:28px}
  .eyebrow{font-size:10px;letter-spacing:2.4px}
  .subtitle{font-size:16px;line-height:1.45}
  .coverfoot{font-size:12.5px}
  .stripe{display:block}
  .stripe div{display:inline-block;width:50%;box-sizing:border-box;
    border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
  .targetrow{gap:12px}
  .targetrow b{font-size:17px}
  .rcphoto{height:150px}
}
@media screen and (max-width:480px){
  .cover h1{font-size:42px;letter-spacing:-1px}
  .coverstats div{width:47%}
  .stripe div{width:100%}
}
/* never let anything push the page sideways */
img,canvas,pre{max-width:100%}
table{max-width:100%}
.recipe,.rcard,.listcard{overflow-wrap:break-word}
</style>"""
