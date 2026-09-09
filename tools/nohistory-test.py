
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
T=tok(sub="nh1",email="nh@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    A=b.new_context(); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    ea=[]; pa.on("pageerror",lambda e:ea.append(str(e)))
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2500)
    ck("signup saved with no history table", pa.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return (j.version||0)>0;}"""))
    pa.evaluate("location.hash='#/financial/purchases'"); pa.wait_for_timeout(1300)
    pa.click("#bpNew"); pa.wait_for_timeout(450)
    pa.fill("#ln","SAVED WITHOUT HISTORY"); pa.click("#lSave"); pa.wait_for_timeout(2500)
    srv=pa.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return Object.keys((j.body&&j.body.fin&&j.body.fin.purchases)||{}).join(', ');}""")
    ck("an edit reaches the account", "SAVED WITHOUT HISTORY" in srv, srv[:120])
    pill=pa.evaluate("()=>{const e=document.getElementById('syncPill');return e?e.innerText:''}")
    ck("and the pill says saved", "Saved" in pill, pill)
    # a second device must see it
    B=b.new_context(); pb=B.new_page(); pb.on("dialog",lambda d:d.accept())
    signin(pb); pb.wait_for_timeout(4000)
    got=pb.evaluate("()=>Object.keys(JSON.parse(localStorage.getItem('lockedin.v7')).fin.purchases||{}).join(', ')")
    ck("and the second device gets it", "SAVED WITHOUT HISTORY" in got, got[:120])
    print("   errors:", ea[:3] or "none")
    b.close()
print("\nFAILURES:", F or "none")
