from playwright.sync_api import sync_playwright
import subprocess, json
AUD="417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com"
def tok(**kw):
    kw.setdefault("aud",AUD)
    return subprocess.run(["php","/home/user/lockedin/tools/fakegoogle.php",json.dumps(kw)],
                          capture_output=True,text=True).stdout.strip()
URL="http://127.0.0.1:8080/index.html"
T=tok(sub="f2",email="f2@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)
def ver(pg):
    return pg.evaluate("""async()=>{const r=await fetch('api/doc.php?do=ver',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});return (await r.json()).shared;}""")
def pur(pg):
    return pg.evaluate("()=>{try{return Object.keys(JSON.parse(localStorage.getItem('lockedin.v7')).fin.purchases||{}).length}catch(e){return -1}}")
def cst(pg):
    return pg.evaluate("()=>{try{return JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length}catch(e){return -1}}")
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    A=b.new_context(); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    npa=[0]; pa.on("request", lambda r: npa.__setitem__(0,npa[0]+1) if r.method=="POST" and "doc.php" in r.url else None)
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2200)
    print("after wizard: v%s A costs=%d" % (ver(pa), cst(pa)))
    with pa.expect_file_chooser() as fc:
        pa.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pa.wait_for_timeout(600)
        pa.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
        pa.wait_for_timeout(200); pa.click("#stLoad")
    fc.value.set_files("/tmp/lockedin-my-data.json"); pa.wait_for_timeout(5000)
    pa.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
    pa.wait_for_timeout(2000)
    print("after import: v%s A costs=%d purchases=%d" % (ver(pa), cst(pa), pur(pa)))

    B=b.new_context(); pb=B.new_page(); pb.on("dialog",lambda d:d.accept())
    npb=[0]; pb.on("request", lambda r: npb.__setitem__(0,npb[0]+1) if r.method=="POST" and "doc.php" in r.url else None)
    signin(pb); pb.wait_for_timeout(5000)
    print("B signed in: v%s B costs=%d purchases=%d" % (ver(pa), cst(pb), pur(pb)))

    npa[0]=0; npb[0]=0
    v1=ver(pa); pa.wait_for_timeout(30000); v2=ver(pa)
    print("idle 30s: v%s -> v%s, A posts=%d B posts=%d" % (v1,v2,npa[0],npb[0]))

    pa.evaluate("location.hash='#/financial/purchases'"); pa.wait_for_timeout(1200)
    pa.click("#bpNew"); pa.wait_for_timeout(500)
    pa.fill("#ln","FROM A"); pa.click("#lSave"); pa.wait_for_timeout(3000)
    print("A added a list: v%s" % ver(pa))
    pb.wait_for_timeout(9000)
    print("B sees it: %s" % pb.evaluate("()=>Object.keys(JSON.parse(localStorage.getItem('lockedin.v7')).fin.purchases||{}).join(', ')"))

    pb.evaluate("location.hash='#/financial/purchases'"); pb.wait_for_timeout(1200)
    pb.click("#bpNew"); pb.wait_for_timeout(500)
    pb.fill("#ln","FROM B"); pb.click("#lSave"); pb.wait_for_timeout(3000)
    pa.wait_for_timeout(9000)
    print("A sees B's: %s" % pa.evaluate("()=>Object.keys(JSON.parse(localStorage.getItem('lockedin.v7')).fin.purchases||{}).join(', ')"))
    print("final: v%s A costs=%d B costs=%d" % (ver(pa), cst(pa), cst(pb)))
    b.close()
