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
T=tok(sub="fail1",email="fail@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    ctx=b.new_context(); pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    signin(pg)
    for _ in range(8):
        if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
        else: break
    if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2200)

    # the host starts refusing writes, the way a shared host does: an HTML error page
    blocked=[0]
    def route(r):
        blocked[0]+=1
        r.fulfill(status=500, content_type="text/html",
                  body="<html><body>Internal Server Error</body></html>")
    ctx.route("**/api/doc.php?scope=shared", lambda r,_r=None: route(r) if r.request.method=="POST" else r.continue_())
    pg.evaluate("location.hash='#/financial/purchases'"); pg.wait_for_timeout(1200)
    pg.click("#bpNew"); pg.wait_for_timeout(400)
    pg.fill("#ln","MADE WHILE THE SERVER WAS DOWN"); pg.click("#lSave"); pg.wait_for_timeout(2000)
    n1=blocked[0]
    pg.wait_for_timeout(9000)
    ck("it keeps trying instead of giving up", blocked[0]>n1, "%d tries then %d"%(n1,blocked[0]))
    pill=pg.evaluate("()=>{const e=document.getElementById('syncPill');return e?e.innerText+' | '+e.title:''}")
    ck("and says so on the pill", "Not saved yet" in pill, pill)

    # the self test names the failure
    pg.evaluate("()=>{const e=document.getElementById('syncPill');if(e)e.click();}")
    pg.wait_for_timeout(700)
    pg.evaluate("()=>{const b=document.getElementById('syTest');if(b)b.click();}")
    pg.wait_for_timeout(3500)
    txt=pg.evaluate("()=>{const m=document.querySelector('.mask');return m?m.innerText:''}")
    ck("the test says writing is what failed", "cannot save to your account" in txt.lower(), txt[:200])
    ck("and it says reading worked", "Reading your account" in txt, txt[:200])

    # the server comes back, and the edit that was stuck must land on its own
    ctx.unroute("**/api/doc.php?scope=shared")
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
    pg.wait_for_timeout(22000)
    srv=pg.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return Object.keys((j.body&&j.body.fin&&j.body.fin.purchases)||{}).join(', ');}""")
    ck("the stuck edit reaches the account once the server is back",
       "MADE WHILE THE SERVER WAS DOWN" in srv, srv[:120])
    pill2=pg.evaluate("()=>{const e=document.getElementById('syncPill');return e?e.innerText:''}")
    ck("and it goes back to saved", "Saved" in pill2, pill2)
    print("   errors:", errs[:3] or "none")
    if errs: F.append("js errors")
    b.close()
print("\nFAILURES:", F or "none")
