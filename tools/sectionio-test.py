from playwright.sync_api import sync_playwright
import subprocess, json, os, glob
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
DL="/tmp/dls"; os.makedirs(DL,exist_ok=True)
for f in glob.glob(DL+"/*"): os.remove(f)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1400,"height":950},accept_downloads=True)
    pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1000)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", tok(sub="io1",email="io@x.com",name="Jaron"))
    pg.goto(URL); pg.wait_for_timeout(1900)
    for _ in range(8):
        if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
        else: break
    if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2500)

    # load HIS real account file through the app
    with pg.expect_file_chooser() as fc:
        pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
        pg.wait_for_timeout(200); pg.click("#stLoad")
    fc.value.set_files("/tmp/his.json"); pg.wait_for_timeout(4000)
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
    st=pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));return {c:s.fin.costs.length,d:Object.keys(s.days).length,p:s.plan.cols.length,pur:Object.keys(s.fin.purchases).length,str:Object.keys(s.fin.strategies).length};}")
    ck("his real file loads whole", st["c"]==39 and st["d"]==22 and st["p"]==2, st)

    # every section exports a spreadsheet, and it has rows
    def openIO(k):
        pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
        pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
        pg.wait_for_timeout(500)
        pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"exp\"]');if(d)d.open=true;}")
        pg.wait_for_timeout(200)
        pg.click('[data-io="%s"]'%k); pg.wait_for_timeout(500)
    keys=pg.evaluate("""()=>{const x=document.querySelector('[data-a="settings"],#settings');if(x)x.click();
      return null;}""")
    pg.wait_for_timeout(500)
    pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"exp\"]');if(d)d.open=true;}")
    pg.wait_for_timeout(250)
    keys=pg.evaluate("()=>[...document.querySelectorAll('.mask [data-io]')].map(b=>b.dataset.io)")
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
    ck("every section is registered", len(keys)==20, keys)
    # nothing in the account may be missing from the section files
    missing=pg.evaluate("""()=>{
      const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      const device=['v','who','savedAt','theme','onboarded','seeded','seeded6','__sections7',
                    '__t','__td','__bv','__dv','__migrated','secret'];
      const covered=new Set(%s);
      return Object.keys(s).filter(k=>device.indexOf(k)<0&&!covered.has(k));
    }""" % json.dumps(['members','household','prefs','ingOv','fav','lists','mine','photos',
                       'shop','days','fin','plan','sched','exLog']))
    ck("no part of the account is left out", not missing, missing)
    for k in keys:
        openIO(k)
        with pg.expect_download() as d:
            pg.click("#ioCsv")
        path=DL+"/"+k+".csv"; d.value.save_as(path)
        import csv as _csv
        with open(path,newline='',encoding='utf-8') as fh:
            rr=list(_csv.reader(fh))
        # counted straight out of his own file, not guessed
        want={'plans':68,'schedule':14,'income':9,'costs':40,'purchases':21,
              'strategies':65,'shopping':1,'daylog':23,'breakdown':1,
              'templates':1,'people':3,'recipelists':1,'traininglog':1,
              'shifts':1,'actuals':1,'scenarios':1,'meals':1,'spending':1,'photos':3}
        n=len(rr)
        if k in want:
            ck("%s exports every row" % k, n==want[k], "%d rows, expected %d"%(n,want[k]))
        else:
            ck("%s exports a spreadsheet" % k, n>=1, "%d rows"%n)
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")

    # round trip: export costs, wipe, import back, same count
    before=pg.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    openIO('costs')
    pg.select_option("#ioMode","replace"); pg.wait_for_timeout(150)
    with pg.expect_file_chooser() as fc:
        pg.click("#ioPick")
    fc.value.set_files(DL+"/costs.csv"); pg.wait_for_timeout(2200)
    after=pg.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.length")
    ck("cost lines survive a round trip", before==after, "%d -> %d"%(before,after))
    nm=pg.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.map(c=>c.name).join('|')")
    ck("and keep their names", "Feminine Products" in nm and "Rent" in nm, nm[:80])
    sec=pg.evaluate("()=>JSON.parse(localStorage.getItem('lockedin.v7')).fin.costs.filter(c=>c.name==='Rent')[0].section")
    ck("and their section", sec=="Home (renting)", sec)
    who=pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));const c=s.fin.costs.filter(x=>x.name==='Groceries (Jaron)')[0];const m=s.members.filter(m=>m.id===c.who)[0];return m?m.name:c.who;}")
    ck("and who they belong to", who=="Jaron", who)

    # HIS plans csv imports
    openIO('plans')
    pg.select_option("#ioMode","replace"); pg.wait_for_timeout(150)
    with pg.expect_file_chooser() as fc:
        pg.click("#ioPick")
    fc.value.set_files("/tmp/hisplans.csv"); pg.wait_for_timeout(2500)
    pl=pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      return s.plan.cols.map(c=>c.name+':'+(c.subs||[]).length+':'+(c.subs||[]).reduce((a,x)=>a+(x.items||[]).length,0)).join(' | ');}""")
    ck("his own plans CSV imports", "Moving in together" in pl and "Open questions" in pl, pl)
    tot=pg.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('lockedin.v7'));
      return s.plan.cols.reduce((a,c)=>a+(c.subs||[]).reduce((b,x)=>b+(x.items||[]).length,0),0);}""")
    ck("with every row", tot==67, tot)

    # the planning page groups by road
    pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove());location.hash='#/planning'}")
    pg.wait_for_timeout(1200)
    heads=pg.evaluate("()=>[...document.querySelectorAll('.trkhead h2')].map(h=>h.innerText.split('\\n')[0].trim())")
    ck("planning is grouped by road", len(heads)==5, heads)
    where=pg.evaluate("""()=>{const out={};document.querySelectorAll('.trk').forEach(t=>{
      const h=t.querySelector('h2').innerText.split('\\n')[0].trim();
      out[h]=[...t.querySelectorAll('.pln')].map(x=>x.innerText);});return out;}""")
    ck("moving in sits under Happening now", "Moving in together" in where.get("Happening now",[]), where)
    ck("open questions sit under Still undecided", "Open questions" in where.get("Still undecided",[]), where)
    ck("the path you are on is marked", pg.evaluate("()=>!!document.querySelector('.trk.live')"))
    pg.screenshot(path="/tmp/planning.png", full_page=False)
    print("   errors:", errs[:3] or "none")
    if errs: F.append("js errors")
    b.close()
print("\nFAILURES:", F or "none")
