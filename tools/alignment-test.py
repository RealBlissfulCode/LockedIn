from playwright.sync_api import sync_playwright
import subprocess, json
AUD="417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com"
def tok(**kw):
    kw.setdefault("aud",AUD)
    return subprocess.run(["php","/home/user/lockedin/tools/fakegoogle.php",json.dumps(kw)],
                          capture_output=True,text=True).stdout.strip()
URL="http://127.0.0.1:8080/index.html"
PAGES=["meals","training","training/exercises","shopping","shopping/ingredients","lists",
       "financial","financial/actual","financial/strategies","financial/purchases",
       "planning","schedule","schedule/templates","mealplan","household","install"]
AUDIT = """() => {
  const out=[];
  const vis=e=>{const s=getComputedStyle(e);
    return s.display!=='none'&&s.visibility!=='hidden'&&+s.opacity>0.05;};
  /* a marker is a small square/round thing that sits beside words */
  const markers=[...document.querySelectorAll('.page i, .page .dot, .page .cdotc, .page .sw, .page .pmark, .mask i, .mask .dot')]
    .filter(vis).filter(e=>{const r=e.getBoundingClientRect();
      return r.width>2&&r.width<=26&&r.height>2&&r.height<=26;});
  for(const m of markers){
    const p=m.parentElement; if(!p) continue;
    /* the words sitting on the same line as the marker */
    let txt=''; for(const n of p.childNodes) if(n.nodeType===3) txt+=n.textContent.trim();
    let ref=null;
    if(txt){ ref=p; }
    else { const sib=[...p.children].find(c=>c!==m&&vis(c)&&(c.textContent||'').trim().length>1); if(sib) ref=sib; }
    if(!ref) continue;
    const mr=m.getBoundingClientRect(), rr=ref.getBoundingClientRect();
    if(rr.height<4||rr.height>60) continue;
    if(mr.top>rr.bottom||mr.bottom<rr.top) continue;   /* not on the same line */
    const off=((mr.top+mr.bottom)/2)-((rr.top+rr.bottom)/2);
    if(Math.abs(off)>2.5)
      out.push({el:(m.className||m.tagName)+'', inside:(ref.className||ref.tagName)+'',
                off:Math.round(off*10)/10, txt:(ref.textContent||'').trim().slice(0,26)});
  }
  const seen=new Set(), uniq=[];
  for(const o of out){const k=o.el+'|'+o.inside+'|'+o.off; if(seen.has(k))continue; seen.add(k); uniq.push(o);}
  return uniq.slice(0,10);
}"""
BAD=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    for W,H,mob in [(1512,950,False),(390,844,True)]:
        ctx=b.new_context(viewport={"width":W,"height":H},is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
        pg.goto(URL); pg.wait_for_timeout(1000)
        pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
          headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
          body:JSON.stringify({credential:t})});}""", tok(sub="al%d"%W,email="al%d@x.com"%W,name="Jaron"))
        pg.goto(URL); pg.wait_for_timeout(1900)
        for _ in range(8):
            if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
            else: break
        if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2500)
        with pg.expect_file_chooser() as fc:
            pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
            pg.wait_for_timeout(200); pg.click("#stLoad")
        fc.value.set_files("/tmp/lockedin-my-data.json"); pg.wait_for_timeout(4500)
        pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
        for v in PAGES:
            pg.evaluate("location.hash='#/%s'"%v); pg.wait_for_timeout(700)
            for x in pg.evaluate(AUDIT):
                BAD.append((W,v,"%s in %s off by %spx  (%s)"%(x["el"],x["inside"],x["off"],x["txt"])))
        print("%dpx done"%W)
        ctx.close()
    b.close()
seen=set(); out=[]
for x in BAD:
    k=(x[0],x[2])
    if k in seen: continue
    seen.add(k); out.append(x)
print("\nMISALIGNED:", len(out))
for x in out[:25]: print("  ",x)
