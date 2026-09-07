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
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1180,"height":900}); pg=ctx.new_page()
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("dialog",lambda d:d.accept())
    pg.goto("http://127.0.0.1:8080/index.html"); pg.wait_for_timeout(1300)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", tok(sub="200",email="loss@b.com",name="Jaron"))
    pg.goto("http://127.0.0.1:8080/index.html"); pg.wait_for_timeout(1800)
    for _ in range(4): pg.click("#suNext"); pg.wait_for_timeout(280)
    pg.click("#suDone"); pg.wait_for_timeout(2500)
    base=pg.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    ck("account has data", base>30, base)
    pg.wait_for_timeout(1500)

    # ---- THE REGRESSION: a state saved under the pre-rework section names ----
    pg.evaluate("""()=>{
      const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      delete s.__sections7;
      s.fin.costs.forEach((c,i)=>{ c.section = i%3===0?'Living':(i%3===1?'Housing (rent)':'Savings'); });
      s.fin.costs[0].name='Groceries'; s.fin.costs[3].name='Fuel for the car';
      localStorage.setItem('lockedin.v7', JSON.stringify(s));
    }""")
    pg.reload(); pg.wait_for_timeout(2600)
    after=pg.evaluate("()=>{const r=localStorage.getItem('lockedin.v7');return r?JSON.parse(r).fin.costs.length:0}")
    ck("old-section data survives a reload", after==base, "%d -> %d"%(base,after))
    secs=pg.evaluate("""()=>[...new Set(JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.map(c=>c.section))]""")
    ck("old sections migrated", "Living" not in secs and "Savings" not in secs, secs)
    ck("groceries landed in Food", pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      return (s.fin.costs.filter(c=>c.name==='Groceries')[0]||{}).section;}""")=="Food")
    ck("fuel landed in Getting around", pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      return (s.fin.costs.filter(c=>c.name==='Fuel for the car')[0]||{}).section;}""")=="Getting around")
    ck("no errors on reload", not errs, errs[:2])

    # ---- the server refuses a wipe ----
    srv=pg.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});return await r.json();}""")
    ck("server still has the account", len(srv["body"]["fin"]["costs"])>30, len(srv["body"]["fin"]["costs"]))
    wipe=pg.evaluate("""async(v)=>{const r=await fetch('api/doc.php?scope=shared',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({version:v,body:{fin:{costs:[],jobs:[],actuals:[],scenarios:{},purchases:{},strategies:{}},days:{},members:[],lists:{},plan:{cols:[]},sched:{cols:[]},fav:[]}})});
      return {status:r.status, body:await r.json()};}""", srv["version"])
    ck("server refuses a write that would empty the account", wipe["body"].get("error")=="would_wipe", wipe)
    still=pg.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});return (await r.json()).body.fin.costs.length;}""")
    ck("account untouched after the refusal", still>30, still)

    # ---- history and restore ----
    h=pg.evaluate("""async()=>{const r=await fetch('api/doc.php?do=history&scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});return await r.json();}""")
    ck("earlier versions are kept", h["ok"] and len(h["versions"])>0, len(h.get("versions",[])))
    ck("install page draws", pg.evaluate("()=>{location.hash='#/install';return true}") is True)
    pg.wait_for_timeout(900)
    ck("install page has steps", "Add to Home Screen" in pg.inner_text(".page") or "Install app" in pg.inner_text(".page") or "install icon" in pg.inner_text(".page"), pg.inner_text(".page")[:120])
    ck("install page shows the address", "127.0.0.1:8080" in pg.inner_text(".addr"))
    b.close()
print("\nFAILURES:", F or "none")
