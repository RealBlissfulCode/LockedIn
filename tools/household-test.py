from playwright.sync_api import sync_playwright
import subprocess, json, re
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
TJ=tok(sub="acctJ",email="jaron@x.com",name="Jaron")
TA=tok(sub="acctA",email="aaliyah@x.com",name="Aaliyah")
def signin(pg,t):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", t)
    pg.goto(URL); pg.wait_for_timeout(2000)
def wizard(pg):
    for _ in range(8):
        if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
        else: break
    if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2200)
def pur(pg):
    return pg.evaluate("()=>{try{return Object.keys(JSON.parse(localStorage.getItem('lockedin.v7')).fin.purchases||{}).join(', ')}catch(e){return 'ERR'}}")
def addList(pg,name):
    pg.evaluate("location.hash='#/financial/purchases'"); pg.wait_for_timeout(1300)
    pg.click("#bpNew"); pg.wait_for_timeout(450)
    pg.fill("#ln",name); pg.click("#lSave"); pg.wait_for_timeout(2200)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    # Jaron sets the household up and loads the data
    J=b.new_context(); pj=J.new_page(); pj.on("dialog",lambda d:d.accept())
    ej=[]; pj.on("pageerror",lambda e:ej.append(str(e)))
    signin(pj,TJ); wizard(pj)
    with pj.expect_file_chooser() as fc:
        pj.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pj.wait_for_timeout(600)
        pj.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
        pj.wait_for_timeout(200); pj.click("#stLoad")
    fc.value.set_files("/tmp/lockedin-my-data.json"); pj.wait_for_timeout(4500)
    pj.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
    ck("Jaron has the data", pj.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")==39)

    # Jaron makes an invite code
    inv=pj.evaluate("""async()=>{const r=await fetch('api/household.php?do=invite',{method:'POST',
      credentials:'same-origin',headers:{'Content-Type':'application/json','X-LockedIn':'1'},
      body:JSON.stringify({name:'Aaliyah'})});return await r.json();}""")
    ck("an invite code was made", bool(inv.get("code")), inv)

    # Aaliyah signs in on her own account and joins with the code
    A=b.new_context(); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    ea=[]; pa.on("pageerror",lambda e:ea.append(str(e)))
    dl=[]; pa.on("console",lambda m: dl.append(m.text) if "DBG" in m.text else None)
    signin(pa,TA)
    joined=pa.evaluate("""async(c)=>{const r=await fetch('api/household.php?do=join',{method:'POST',
      credentials:'same-origin',headers:{'Content-Type':'application/json','X-LockedIn':'1'},
      body:JSON.stringify({code:c})});return await r.json();}""", inv.get("code"))
    ck("Aaliyah joined the household", bool(joined.get("ok")), joined)
    pa.reload(); pa.wait_for_timeout(4500)
    if pa.query_selector("#suNext"): wizard(pa)
    pa.wait_for_timeout(3500)
    ck("Aaliyah sees the household data", pa.evaluate("()=>{try{return JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length}catch(e){return -1}}")==39,
       pa.evaluate("()=>{try{return JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length}catch(e){return -1}}"))

    # each adds something, both must see both, live
    addList(pj,"JARON ADDED THIS")
    pa.wait_for_timeout(9000)
    ck("Aaliyah sees Jaron's, live", "JARON ADDED THIS" in pur(pa), pur(pa))
    addList(pa,"AALIYAH ADDED THIS")
    pj.wait_for_timeout(9000)
    ck("Jaron sees Aaliyah's, live", "AALIYAH ADDED THIS" in pur(pj), pur(pj))
    ck("and Jaron still has his own", "JARON ADDED THIS" in pur(pj), pur(pj))

    # both survive a reload
    pj.reload(); pj.wait_for_timeout(3500); pa.reload(); pa.wait_for_timeout(3500)
    ck("both survive a reload on Jaron", "JARON ADDED THIS" in pur(pj) and "AALIYAH ADDED THIS" in pur(pj), pur(pj))
    ck("both survive a reload on Aaliyah", "JARON ADDED THIS" in pur(pa) and "AALIYAH ADDED THIS" in pur(pa), pur(pa))
    cj=pj.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    ca=pa.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    ck("Jaron's cost lines were not replaced by hers", cj==39, cj)
    ck("Aaliyah has the household's cost lines", ca==39, ca)
    mem=pa.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).members.map(m=>m.name).join(', ')")
    ck("and both people are in the member list", "Jaron" in mem and "Aaliyah" in mem, mem)
    srv=pj.evaluate("""async()=>{const r=await fetch('api/doc.php?scope=shared',
      {credentials:'same-origin',headers:{'X-LockedIn':'1'}});const j=await r.json();
      return j.body.fin.costs.length;}""")
    ck("and the account itself still has them", srv==39, srv)
    print("   DBG:", dl[:4])
    print("   Jaron errors:", ej[:3] or "none"); print("   Aaliyah errors:", ea[:3] or "none")
    if ej: F.append("js Jaron")
    if ea: F.append("js Aaliyah")
    b.close()
print("\nFAILURES:", F or "none")
