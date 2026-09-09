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
T=tok(sub="all1",email="all@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)
def raw(pg):
    return pg.evaluate("()=>localStorage.getItem('lockedin.v7')||''")

with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    A=b.new_context(viewport={"width":1400,"height":950}); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    ea=[]; pa.on("pageerror",lambda e:ea.append(str(e)))
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2500)
    B=b.new_context(viewport={"width":1400,"height":950}); pb=B.new_page(); pb.on("dialog",lambda d:d.accept())
    eb=[]; pb.on("pageerror",lambda e:eb.append(str(e)))
    signin(pb); pb.wait_for_timeout(4000)
    ck("both devices are on the account", pb.is_visible("#app"))

    def edit(pg,name,hash_,fn):
        pg.evaluate("location.hash='#/%s'"%hash_); pg.wait_for_timeout(1300)
        ok=fn(pg)
        pg.wait_for_timeout(2500)
        return ok

    def arrives(pg,needle,secs=12):
        for _ in range(secs):
            if needle in raw(pg): return True
            pg.wait_for_timeout(1000)
        return False

    # ---- SCHEDULE: a plan on a specific day ----
    def addPlan(pg):
        pg.click("#evAdd"); pg.wait_for_timeout(500)
        f=pg.query_selector("#ex")
        if not f: return False
        pg.fill("#ex","SHIFT FROM A"); 
        btn=pg.evaluate("""()=>{const b=[...document.querySelectorAll('.mask button')]
          .find(x=>/^(Save|Add)/.test(x.innerText.trim())); if(b){b.click();return true} return false;}""")
        return bool(btn)
    ck("a plan was added on A", edit(pa,"plan","schedule",addPlan))
    ck("SCHEDULE reaches the other device", arrives(pb,"SHIFT FROM A"), "sched")

    # ---- SCHEDULE TEMPLATES ----
    def addTmpl(pg):
        b=pg.query_selector("#tmAdd") or pg.query_selector("#schTmplAdd")
        if not b: return "skip"
        b.click(); pg.wait_for_timeout(400)
        i=pg.query_selector(".mask input")
        if not i: return "skip"
        pg.evaluate("""()=>{const i=document.querySelector('.mask input');i.value='TEMPLATE FROM A';
          i.dispatchEvent(new Event('input',{bubbles:true}));
          const b=[...document.querySelectorAll('.mask button')].find(x=>/^(Save|Add)/.test(x.innerText.trim()));
          if(b)b.click();}""")
        return True
    r=edit(pa,"tmpl","schedule/templates",addTmpl)
    if r!="skip": ck("SCHEDULE TEMPLATES reach the other device", arrives(pb,"TEMPLATE FROM A"), "sched tmpl")

    # ---- PLANNING ----
    def addPlanning(pg):
        b=pg.query_selector("#plNew") or pg.query_selector("#pNew") or pg.query_selector("#planNew")
        if not b:
            b=pg.evaluate("""()=>{const x=[...document.querySelectorAll('.page button')]
              .find(e=>/New|Add/.test(e.innerText)); if(x){x.click();return true} return false;}""")
            if not b: return "skip"
        else: b.click()
        pg.wait_for_timeout(500)
        return pg.evaluate("""()=>{const i=document.querySelector('.mask input');
          if(!i)return false; i.value='PLANNING FROM A';
          i.dispatchEvent(new Event('input',{bubbles:true}));
          const b=[...document.querySelectorAll('.mask button')].find(x=>/^(Save|Add|Create)/.test(x.innerText.trim()));
          if(b){b.click();return true} return false;}""")
    r=edit(pa,"planning","planning",addPlanning)
    if r!="skip": ck("PLANNING reaches the other device", arrives(pb,"PLANNING FROM A"), "planning")

    # ---- SHOPPING ----
    def addShop(pg):
        pg.click("#newList"); pg.wait_for_timeout(500)
        pg.fill("#nlN","SHOP FROM A")
        pg.click("#akOk"); return True
    edit(pa,"shop","shopping",addShop)
    ck("the shopping list was actually created on A", "SHOP FROM A" in raw(pa))
    ck("SHOPPING reaches the other device", arrives(pb,"SHOP FROM A"), "shop")

    # ---- RECIPE LISTS ----
    def addRl(pg):
        pg.click("#rlNew"); pg.wait_for_timeout(500)
        pg.fill("#rlN","LIST FROM A")
        pg.click("#akOk"); return True
    edit(pa,"lists","lists",addRl)
    ck("the recipe list was actually created on A", "LIST FROM A" in raw(pa))
    ck("RECIPE LISTS reach the other device", arrives(pb,"LIST FROM A"), "lists")

    # ---- and back the other way, from B ----
    def addPlanB(pg):
        pg.click("#evAdd"); pg.wait_for_timeout(500)
        if not pg.query_selector("#ex"): return False
        pg.fill("#ex","SHIFT FROM B")
        return pg.evaluate("""()=>{const b=[...document.querySelectorAll('.mask button')]
          .find(x=>/^(Save|Add)/.test(x.innerText.trim())); if(b){b.click();return true} return false;}""")
    ck("a plan was added on B", edit(pb,"planB","schedule",addPlanB))
    ck("SCHEDULE comes back the other way", arrives(pa,"SHIFT FROM B"), "sched b->a")
    ck("and A kept its own", "SHIFT FROM A" in raw(pa))

    print("   A errors:", ea[:3] or "none"); print("   B errors:", eb[:3] or "none")
    if ea: F.append("js A")
    if eb: F.append("js B")
    b.close()
print("\nFAILURES:", F or "none")
