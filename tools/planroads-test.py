from playwright.sync_api import sync_playwright
import subprocess, json
AUD="417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com"
def tok(**kw):
    kw.setdefault("aud",AUD)
    return subprocess.run(["php","/home/user/lockedin/tools/fakegoogle.php",json.dumps(kw)],
                          capture_output=True,text=True).stdout.strip()
F=[]
def ck(n,c,x=""):
    print(("PASS " if c else "FAIL ")+n+((" :: "+str(x)) if x else ""))
    if not c: F.append(n)
URL="http://127.0.0.1:8080/index.html"
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1400,"height":1000},accept_downloads=True)
    pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1000)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", tok(sub="rg1",email="rg@x.com",name="Jaron"))
    pg.goto(URL); pg.wait_for_timeout(1900)
    for _ in range(8):
        if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
        else: break
    if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2500)
    # his real account first
    with pg.expect_file_chooser() as fc:
        pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
        pg.wait_for_timeout(200); pg.click("#stLoad")
    fc.value.set_files("/tmp/his.json"); pg.wait_for_timeout(4000)
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")

    # now the organised plans, replacing the old two
    pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
    pg.wait_for_timeout(500)
    pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"exp\"]');if(d)d.open=true;}")
    pg.wait_for_timeout(250)
    pg.click('[data-io="plans"]'); pg.wait_for_timeout(500)
    pg.select_option("#ioMode","replace"); pg.wait_for_timeout(150)
    with pg.expect_file_chooser() as fc:
        pg.click("#ioPick")
    fc.value.set_files("/tmp/plans-organised.csv"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove());location.hash='#/planning'}")
    pg.wait_for_timeout(1500)

    tot=pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      return s.plan.cols.reduce((a,c)=>a+(c.subs||[]).reduce((b,x)=>b+(x.items||[]).length,0),0);}""")
    ck("all 67 items came in", tot==67, tot)
    where=pg.evaluate("""()=>{const out={};document.querySelectorAll('.trk').forEach(t=>{
      const h=t.querySelector('h2').innerText.split('\\n')[0].trim();
      out[h]=[...t.querySelectorAll('.pln')].map(x=>x.innerText);});return out;}""")
    ck("moving in is on Happening now", where.get("Happening now")==["Moving in together"], where)
    ck("the lease is on Renting together", where.get("Renting together")==["Getting the lease"], where)
    ck("buying is on Buying a home", where.get("Buying a home")==["Buying"], where)
    ck("setting up is on True either way", where.get("True either way")==["Setting up the home"], where)
    ck("questions are on Still undecided", where.get("Still undecided")==["Open questions"], where)
    ck("every road has something on it", all(where.get(k) for k in where), where)
    notes=pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      let hit=null;
      s.plan.cols.forEach(c=>(c.subs||[]).forEach(x=>(x.items||[]).forEach(i=>{
        if(i.text.indexOf('soft-pull')>=0) hit=i.note;})));return hit;}""")
    ck("the notes came with them", "Ryan Lococo" in (notes or ""), (notes or "")[:70])
    pg.screenshot(path="/tmp/planning2.png", full_page=True)
    print("   errors:", errs[:3] or "none")
    if errs: F.append("js errors")
    b.close()
print("\nFAILURES:", F or "none")
