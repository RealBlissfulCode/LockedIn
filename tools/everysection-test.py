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
T=tok(sub="eb1",email="eb@x.com",name="Jaron")
def signin(pg):
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", T)
    pg.goto(URL); pg.wait_for_timeout(2000)

with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    A=b.new_context(); pa=A.new_page(); pa.on("dialog",lambda d:d.accept())
    signin(pa)
    for _ in range(8):
        if pa.query_selector("#suNext"): pa.click("#suNext"); pa.wait_for_timeout(220)
        else: break
    if pa.query_selector("#suDone"): pa.click("#suDone"); pa.wait_for_timeout(2500)

    # Put a marker into every branch, on the account, the way another device would.
    res=pa.evaluate("""async()=>{
      const get=async()=>{const r=await fetch('api/doc.php?scope=shared',
        {credentials:'same-origin',headers:{'X-LockedIn':'1'}});return await r.json();};
      const cur=await get();
      const b=cur.body||{};
      b.household='HOUSE_MARK';
      b.members=[{id:'m1',name:'MEMBER_MARK',sex:'m'}];
      b.ingOv={ING_MARK:{n:'x'}};
      b.fav=['FAV_MARK'];
      b.lists={LIST_MARK:{n:'x',items:[]}};
      b.mine={MINE_MARK:1};
      b.photos={PHOTO_MARK:'x'};
      b.shop={active:'SHOP_MARK',lists:{SHOP_MARK:{cat:'x',items:[]}}};
      b.fin=b.fin||{}; b.fin.costs=[{id:'c1',name:'COST_MARK',section:'Food',real:1}];
      b.fin.jobs=[{id:'j1',name:'JOB_MARK',real:1}];
      b.fin.purchases={PURCHASE_MARK:{cat:'x',items:[]}};
      b.fin.scenarios={SCENARIO_MARK:{jobs:[],costs:[],mode:'real',path:'rent'}};
      b.fin.strategies={STRATEGY_MARK:{items:[]}};
      b.fin.actuals=[{id:'a1',note:'ACTUAL_MARK'}];
      b.plan={cols:[{id:'p1',name:'PLAN_MARK',items:[]}]};
      b.sched={cols:[{id:'s1',name:'SCHED_MARK'}],tmpl:{TMPL_MARK:[]}};
      b.exLog=[{id:'e1',note:'EXLOG_MARK'}];
      b.prefs={diet:['DIET_MARK'],goals:[],train:[]};
      b.days=b.days||{};
      b.days['2026-01-05']={workout:'rest',meals:[],notes:'DAY_MARK',w:null,
        sched:[{who:'all',what:'DAYSCHED_MARK'}],spend:[]};
      const w=await fetch('api/doc.php?scope=shared',{method:'POST',credentials:'same-origin',
        headers:{'Content-Type':'application/json','X-LockedIn':'1'},
        body:JSON.stringify({version:cur.version,body:b})});
      return await w.json();}""")
    ck("the account was seeded with a marker in every section", bool(res.get("ok")), res)

    # A fresh device signs in. Every marker must arrive.
    B=b.new_context(); pb=B.new_page(); pb.on("dialog",lambda d:d.accept())
    eb=[]; pb.on("pageerror",lambda e:eb.append(str(e)))
    signin(pb); pb.wait_for_timeout(4500)
    raw=pb.evaluate("()=>localStorage.getItem('lockedin.v7')||''")
    MARKS=["HOUSE_MARK","MEMBER_MARK","ING_MARK","FAV_MARK","LIST_MARK","MINE_MARK","PHOTO_MARK",
           "SHOP_MARK","COST_MARK","JOB_MARK","PURCHASE_MARK","SCENARIO_MARK","STRATEGY_MARK",
           "ACTUAL_MARK","PLAN_MARK","SCHED_MARK","TMPL_MARK","EXLOG_MARK","DIET_MARK",
           "DAY_MARK","DAYSCHED_MARK"]
    missing=[m for m in MARKS if m not in raw]
    ck("a new device receives every section", not missing, missing)

    # And the already-open device must pick them all up live, no refresh.
    for _ in range(14):
        r2=pa.evaluate("()=>localStorage.getItem('lockedin.v7')||''")
        if not [m for m in MARKS if m not in r2]: break
        pa.wait_for_timeout(1000)
    r2=pa.evaluate("()=>localStorage.getItem('lockedin.v7')||''")
    missing2=[m for m in MARKS if m not in r2]
    ck("an open device picks every section up live", not missing2, missing2)

    # And it survives a reload on both.
    pa.reload(); pa.wait_for_timeout(3500)
    pb.reload(); pb.wait_for_timeout(3500)
    r3=pa.evaluate("()=>localStorage.getItem('lockedin.v7')||''")
    r4=pb.evaluate("()=>localStorage.getItem('lockedin.v7')||''")
    ck("still all there after a reload on A", not [m for m in MARKS if m not in r3],
       [m for m in MARKS if m not in r3])
    ck("still all there after a reload on B", not [m for m in MARKS if m not in r4],
       [m for m in MARKS if m not in r4])
    print("   B errors:", eb[:3] or "none")
    if eb: F.append("js B")
    b.close()
print("\nFAILURES:", F or "none")
