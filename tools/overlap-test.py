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
  const bad = [];
  const vis = e => { const s=getComputedStyle(e);
    return s.display!=='none' && s.visibility!=='hidden' && +s.opacity>0.05; };
  const painted = e => { const s=getComputedStyle(e);
    const bg=s.backgroundColor;
    return bg && bg!=='rgba(0, 0, 0, 0)' && bg!=='transparent'; };
  const textOf = e => {
    let t='';
    for (const n of e.childNodes) if (n.nodeType===3) t+=n.textContent.trim();
    return t;
  };
  const all=[...document.querySelectorAll('.page *, .mask *')].filter(vis);
  const texts=all.filter(e=>textOf(e).length>1);
  const boxes=all.filter(e=>painted(e)&&textOf(e).length===0&&e.getBoundingClientRect().height>6);
  const inter=(a,b)=>!(a.right<=b.left+1||b.right<=a.left+1||a.bottom<=b.top+1||b.bottom<=a.top+1);
  for (const t of texts) {
    const tr=t.getBoundingClientRect();
    if (tr.width<4||tr.height<4) continue;
    for (const b of boxes) {
      if (b===t||b.contains(t)||t.contains(b)) continue;
      const br=b.getBoundingClientRect();
      if (br.width<4||br.height<4) continue;
      if (!inter(tr,br)) continue;
      /* only a real problem if the box paints on top of the text */
      const mx=Math.round((Math.max(tr.left,br.left)+Math.min(tr.right,br.right))/2);
      const my=Math.round((Math.max(tr.top,br.top)+Math.min(tr.bottom,br.bottom))/2);
      if (mx<0||my<0||mx>innerWidth||my>innerHeight) continue;
      const hit=document.elementFromPoint(mx,my);
      if (hit===b||b.contains(hit)) {
        bad.push({text:textOf(t).slice(0,34), over:(b.className||b.tagName)+''});
      }
      break;
    }
  }
  /* sideways scrollbars where there is nothing to scroll to */
  const scrolls=[];
  document.querySelectorAll('.page .tw, .mask .tw').forEach(e=>{
    if (e.scrollWidth>e.clientWidth+2) scrolls.push((e.className||'')+' '+e.scrollWidth+'>'+e.clientWidth);
  });
  return {bad:bad.slice(0,8), scrolls:scrolls.slice(0,6)};
}"""
BAD=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    for W,H,mob in [(1512,950,False),(1280,800,False),(390,844,True)]:
        ctx=b.new_context(viewport={"width":W,"height":H},is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
        pg.goto(URL); pg.wait_for_timeout(1000)
        pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
          headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
          body:JSON.stringify({credential:t})});}""", tok(sub="ov%d"%W,email="ov%d@x.com"%W,name="Jaron"))
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
            r=pg.evaluate(AUDIT)
            for x in r["bad"]: BAD.append((W,v,"'%s' covered by %s"%(x["text"],x["over"])))
            for x in r["scrolls"]: BAD.append((W,v,"sideways scroll: "+x))
        # and the two modals
        pg.evaluate("()=>{const p=document.getElementById('syncPill');if(p)p.click();}")
        pg.wait_for_timeout(800)
        r=pg.evaluate(AUDIT)
        for x in r["bad"]: BAD.append((W,"sync panel","'%s' covered by %s"%(x["text"],x["over"])))
        for x in r["scrolls"]: BAD.append((W,"sync panel","sideways scroll: "+x))
        pg.evaluate("()=>{const b=document.getElementById('syTest');if(b)b.click();}")
        pg.wait_for_timeout(3000)
        r=pg.evaluate(AUDIT)
        for x in r["bad"]: BAD.append((W,"sync test","'%s' covered by %s"%(x["text"],x["over"])))
        for x in r["scrolls"]: BAD.append((W,"sync test","sideways scroll: "+x))
        print("%dpx done"%W)
        ctx.close()
    b.close()
seen=set(); out=[]
for x in BAD:
    k=(x[0],x[2])
    if k in seen: continue
    seen.add(k); out.append(x)
print("\nPROBLEMS:", len(out))
for x in out[:30]: print("  ",x)
