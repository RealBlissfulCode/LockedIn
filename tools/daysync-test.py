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
T=tok(sub="dy1",email="dy@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)
def days(pg):
    return pg.evaluate("()=>JSON.stringify(JSON.parse(localStorage.getItem('lockedin.v7')).days||{})")
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    A=b.new_context(); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    ea=[]; pa.on("pageerror",lambda e:ea.append(str(e)))
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2200)
    B=b.new_context(); pb=B.new_page(); pb.on("dialog",lambda d:d.accept())
    eb=[]; pb.on("pageerror",lambda e:eb.append(str(e)))
    signin(pb); pb.wait_for_timeout(4000)

    # A writes a real note on today, through the UI
    pa.evaluate("location.hash='#/training'"); pa.wait_for_timeout(1800)
    # write today's note through the real field and its Save button
    wrote = pa.evaluate("""()=>{const t=document.querySelector('#tNotes');
      if(!t) return false; t.value='REAL NOTE FROM A';
      t.dispatchEvent(new Event('input',{bubbles:true}));
      const b=document.querySelector('#tSave'); if(!b) return false; b.click(); return true;}""")
    pa.wait_for_timeout(3000)
    ck("wrote today's note through the UI", wrote)
    ck("A stored the note", "REAL NOTE FROM A" in days(pa), days(pa)[:120])
    pb.wait_for_timeout(9000)
    ck("the note reached the other device", "REAL NOTE FROM A" in days(pb), days(pb)[:160])
    # and it survives a reload on both
    pa.reload(); pa.wait_for_timeout(3000)
    pb.reload(); pb.wait_for_timeout(3000)
    ck("survives a reload on A", "REAL NOTE FROM A" in days(pa))
    ck("survives a reload on B", "REAL NOTE FROM A" in days(pb))
    print("   A errors:", ea[:3] or "none"); print("   B errors:", eb[:3] or "none")
    if ea: F.append("js A")
    if eb: F.append("js B")
    b.close()
print("\nFAILURES:", F or "none")
