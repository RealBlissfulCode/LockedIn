from playwright.sync_api import sync_playwright
import subprocess, json
AUD="417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com"
def tok(**kw):
    kw.setdefault("aud",AUD)
    return subprocess.run(["php","/home/user/lockedin/tools/fakegoogle.php",json.dumps(kw)],
                          capture_output=True,text=True).stdout.strip()
F=[]
def ck(n,c,x=""):
    print(("PASS " if c else "FAIL ")+n+((" :: "+str(x)) if x else ""),flush=True)
    if not c: F.append(n)
URL="http://127.0.0.1:8080/index.html"
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    for W,mob,tag in [(1400,False,"desk"),(390,True,"phone")]:
        ctx=b.new_context(viewport={"width":W,"height":950},is_mobile=mob,has_touch=mob)
        pg=ctx.new_page(); pg.on("dialog",lambda d:d.accept())
        errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(1000)
        pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
          headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
          body:JSON.stringify({credential:t})});}""", tok(sub="dg%d"%W,email="dg%d@x.com"%W,name="Jaron"))
        pg.goto(URL); pg.wait_for_timeout(1900)
        for _ in range(8):
            if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(220)
            else: break
        if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2500)
        with pg.expect_file_chooser() as fc:
            pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
            pg.wait_for_timeout(200); pg.click("#stLoad")
        fc.value.set_files("/tmp/his.json"); pg.wait_for_timeout(4000)
        pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove());location.hash='#/financial'}")
        pg.wait_for_timeout(1500)
        pg.evaluate("""()=>{const r=[...document.querySelectorAll('tr')].find(x=>/Feminine/i.test(x.innerText));
          r.querySelector('[data-coste]').click();}""")
        pg.wait_for_timeout(800)
        pg.fill("#cn","Feminine Products")

        # THE BUG: press inside a field, drag out past the panel, release on the backdrop
        # a point that is genuinely on the backdrop, not on the panel
        box=pg.evaluate("""()=>{const i=document.querySelector('.mask #cn');
          const r=i.getBoundingClientRect();
          const d=document.querySelector('.mask .modal').getBoundingClientRect();
          let ox,oy;
          if(d.top>60){ ox=innerWidth/2; oy=d.top/2; }
          else if(d.left>60){ ox=d.left/2; oy=innerHeight/2; }
          else { ox=innerWidth/2; oy=Math.max(4,d.top-10); }
          return {x:r.x+20,y:r.y+r.height/2,ox:ox,oy:oy};}""")
        pg.mouse.move(box["x"],box["y"]); pg.mouse.down()
        pg.mouse.move(box["x"]-40,box["y"],steps=6)
        pg.mouse.move(box["ox"],box["oy"],steps=10)
        pg.mouse.up(); pg.wait_for_timeout(500)
        ck(tag+": dragging a selection out does not close it", pg.query_selector(".mask") is not None)
        ck(tag+": and what was typed is still there",
           (pg.input_value("#cn") if pg.query_selector("#cn") else None)=="Feminine Products")

        # a real click on the backdrop still closes it
        pg.mouse.click(box["ox"],box["oy"]); pg.wait_for_timeout(500)
        ck(tag+": a real click outside still closes it", pg.query_selector(".mask") is None)

        # the breakdown design
        pg.evaluate("""()=>{const r=[...document.querySelectorAll('tr')].find(x=>/Feminine/i.test(x.innerText));
          r.querySelector('[data-coste]').click();}""")
        pg.wait_for_timeout(700)
        for n,q,e in [("Bin bags","2","4"),("Washing up liquid","1","3")]:
            pg.click("#pAdd"); pg.wait_for_timeout(200)
            pg.evaluate("""(v)=>{const r=[...document.querySelectorAll('.prow')].pop();
              const set=(s,x)=>{const el=r.querySelector(s);el.value=x;
                el.dispatchEvent(new Event('input',{bubbles:true}));};
              set('.pn',v[0]);set('.pq',v[1]);set('.pe',v[2]);}""",[n,q,e])
            pg.wait_for_timeout(250)
        ck(tag+": no tampons anywhere in the breakdown",
           "tampon" not in pg.inner_html(".pbox").lower(),
           pg.get_attribute(".pn","placeholder"))
        sums=pg.evaluate("()=>[...document.querySelectorAll('.psum')].map(x=>x.textContent)")
        ck(tag+": each row shows what it comes to", sums==["$8","$3"], sums)
        ck(tag+": and the total adds up", pg.inner_text("#pTot")=="$11", pg.inner_text("#pTot"))
        hdr=pg.evaluate("()=>{const h=document.querySelector('.phead2');return h?getComputedStyle(h).display:'none'}")
        if mob: ck(tag+": no header row, labels on each card", hdr=="none")
        else:   ck(tag+": labels said once at the top", hdr!="none", hdr)
        lbl=pg.evaluate("()=>{const s=document.querySelector('.prow .pfld>span');return s?getComputedStyle(s).display:'?'}")
        if mob: ck(tag+": each field is labelled on a phone", lbl!="none", lbl)
        else:   ck(tag+": no repeated labels on a desk", lbl=="none", lbl)
        over=pg.evaluate("""()=>{const vw=document.documentElement.clientWidth;let n=0;
          document.querySelectorAll('.mask *').forEach(e=>{const b=e.getBoundingClientRect();
            if(b.width>0&&b.right>vw+0.5)n++;});return n;}""")
        ck(tag+": nothing over the edge", over==0, over)
        pg.query_selector(".pbox").screenshot(path="/tmp/pbox-%s.png"%tag)
        print("   errors:", errs[:3] or "none")
        if errs: F.append(tag+" js")
        ctx.close()
    b.close()
print("\nFAILURES:", F or "none")
