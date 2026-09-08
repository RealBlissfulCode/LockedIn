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
T=tok(sub="stale1",email="stale@x.com",name="Jaron")

def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(1900)

with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])

    # A: set the account up properly and get the real data onto it.
    A=b.new_context(viewport={"width":1280,"height":900}); pa=A.new_page()
    ea=[]; pa.on("pageerror",lambda e:ea.append(str(e))); pa.on("dialog",lambda d:d.accept())
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2200)
    with pa.expect_file_chooser() as fc:
        pa.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pa.wait_for_timeout(600)
        pa.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
        pa.wait_for_timeout(200); pa.click("#stLoad")
    fc.value.set_files("/tmp/lockedin-my-data.json"); pa.wait_for_timeout(4000)
    srv=pa.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return {v:j.version,c:j.body.fin.costs.length};}""")
    ck("account has the real data", srv["c"]==39, srv)

    # B: a second device that already has an older, smaller copy in local storage
    #    and has NOT touched anything this session. This is the returning device:
    #    it loads, pulls, and must take the account's copy.
    B=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
    pb=B.new_page()
    eb=[]; pb.on("pageerror",lambda e:eb.append(str(e))); pb.on("dialog",lambda d:d.accept())
    signin(pb)
    for _ in range(8):
        if pb.query_selector("#suNext"): pb.click("#suNext"); pb.wait_for_timeout(220)
        else: break
    if pb.query_selector("#suDone"): pb.click("#suDone"); pb.wait_for_timeout(2200)
    pb.wait_for_timeout(3000)
    # plant a stale copy, exactly what a device that fell behind is holding
    pb.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      s.fin.costs=s.fin.costs.slice(0,2);
      s.fin.purchases={};
      s.household='STALE COPY';
      localStorage.setItem('lockedin.v7',JSON.stringify(s));}""")
    ck("stale copy planted", pb.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")==2)

    # the returning device loads fresh. no edits made. it must take the account.
    pb.reload(); pb.wait_for_timeout(4000)
    n=pb.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    h=pb.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).household")
    ck("returning device takes the account copy", n==39, n)
    ck("and does not keep its stale household name", h!="STALE COPY", h)

    # and it must NOT have pushed its stale copy over the account
    pb.wait_for_timeout(4000)
    srv2=pa.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return {v:j.version,c:j.body.fin.costs.length,h:j.body.household};}""")
    ck("the account was not overwritten by the stale device", srv2["c"]==39, srv2)

    # and A, on its next look, still has everything
    pa.reload(); pa.wait_for_timeout(4000)
    ck("the good device still has it after a reload",
       pa.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")==39,
       pa.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length"))

    # both devices reloading repeatedly must converge, not ping pong
    for i in range(3):
        pa.reload(); pa.wait_for_timeout(2600)
        pb.reload(); pb.wait_for_timeout(2600)
    na=pa.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    nb=pb.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    ck("they agree after three rounds of reloads", na==39 and nb==39, [na,nb])
    print("   A errors:", ea[:3] or "none"); print("   B errors:", eb[:3] or "none")
    if ea: F.append("js A")
    if eb: F.append("js B")
    b.close()
print("\nFAILURES:", F or "none")
