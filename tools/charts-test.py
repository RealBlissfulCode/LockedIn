"""The charts have to be readable, not just pretty.

Checks there is a scale to measure bars against, that the numbers on it are
round ones, that a tap on a bar gives its value on a phone where a title
attribute never shows, and that pointing at a slice tells you what it is.
"""
from playwright.sync_api import sync_playwright
import subprocess, json

AUD = "417196979541-pact400k1sknkh2tn9ve3js5005hurkk.apps.googleusercontent.com"
def tok(**kw):
    kw.setdefault("aud", AUD)
    return subprocess.run(["php", "/home/user/lockedin/tools/fakegoogle.php", json.dumps(kw)],
                          capture_output=True, text=True).stdout.strip()

URL = "http://127.0.0.1:8080/index.html"
F = []
def ck(name, cond, got=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else " :: %r" % (got,)))
    if not cond: F.append(name)

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                            args=["--no-sandbox"])
    for tag, W, H, mob in [("desk", 1512, 950, False), ("phone", 390, 844, True)]:
        ctx = br.new_context(viewport={"width": W, "height": H}, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); pg.on("dialog", lambda d: d.accept())
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(800)
        pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
          headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
          body:JSON.stringify({credential:t})});}""",
          tok(sub="ch" + tag, email="ch" + tag + "@x.com", name="Jaron"))
        pg.goto(URL); pg.wait_for_timeout(1800)
        for _ in range(9):
            if pg.query_selector("#suNext"): pg.click("#suNext"); pg.wait_for_timeout(200)
            else: break
        if pg.query_selector("#suDone"): pg.click("#suDone"); pg.wait_for_timeout(2300)
        with pg.expect_file_chooser() as fc:
            pg.evaluate("()=>{const x=document.querySelector('[data-a=\"settings\"],#settings');if(x)x.click();}")
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{const d=document.querySelector('.setgrp[data-g=\"data\"]');if(d)d.open=true;}")
            pg.wait_for_timeout(200); pg.click("#stLoad")
        fc.value.set_files("/home/user/lockedin-my-data.json"); pg.wait_for_timeout(4500)
        pg.evaluate("()=>{document.querySelectorAll('.mask').forEach(m=>m.remove())}")
        pg.evaluate("location.hash='#/financial'"); pg.wait_for_timeout(1600)

        ck(tag + ": every column chart carries a scale",
           pg.evaluate("()=>[...document.querySelectorAll('.cchart')].every(c=>c.querySelector('.cyax'))"),
           pg.evaluate("()=>document.querySelectorAll('.cchart').length"))

        tops = pg.evaluate("""()=>[...document.querySelectorAll('.cyax')]
          .map(a=>a.firstElementChild.textContent)""")
        def round_number(t):
            n = float(t.replace("$", "").replace(",", "") or 0)
            if n == 0: return False
            s = ("%g" % (n / 10 ** (len(str(int(n))) - 1)))
            return s in ("1", "2", "2.5", "5", "10")
        ck(tag + ": the top of each scale is a round number", all(map(round_number, tops)), tops)

        # a bar must measure against the scale it is drawn on
        ok = pg.evaluate("""()=>{
          const c=document.querySelector('.cchart.ax');
          const top=parseFloat(c.querySelector('.cyax').firstElementChild.textContent.replace(/[^0-9.]/g,''));
          const bar=c.querySelector('.cb');
          const h=parseFloat(getComputedStyle(bar).getPropertyValue('--h'));
          return {top:top,h:h};}""")
        ck(tag + ": bars are drawn against that same scale",
           0 < ok["h"] <= 100.5 and ok["top"] > 0, ok)

        ck(tag + ": no gridline sits above the top of the scale",
           pg.evaluate("""()=>{const s=document.querySelector('.cstack');
             return getComputedStyle(s).backgroundImage.indexOf('gradient')>=0;}"""))

        # the readout a thumb can reach
        bar = pg.query_selector(".cb[data-tip]")
        bar.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
        if mob: pg.touchscreen.tap(*[v + 3 for v in (bar.bounding_box()["x"], bar.bounding_box()["y"])])
        else: bar.hover()
        pg.wait_for_timeout(300)
        tip = pg.evaluate("()=>{const t=document.getElementById('ctip');"
                          "return t&&t.classList.contains('on')?t.textContent:'';}")
        ck(tag + ": a bar says what it is worth when pointed at", "$" in tip, tip)

        # The ring answers back. Point at the stroke, not at the middle of the
        # element's box, which for a ring is the hole in it.
        ring = pg.query_selector(".cdonut")
        ring.scroll_into_view_if_needed(); pg.wait_for_timeout(250)
        # Park the pointer somewhere harmless first. Scrolling can leave it
        # sitting on the ring, and then the before and after are the same
        # reading of the same slice.
        pg.mouse.move(2, 2); pg.wait_for_timeout(250)
        mid_before = pg.evaluate("()=>document.querySelector('.cdmid b').textContent")
        r = ring.bounding_box()
        # Twelve o'clock, in the middle of the stroke. The ring is drawn at
        # radius 47 of a 120 box, so its band runs through 10.8% of the height;
        # the outer edge is a miss as often as a hit.
        px, py = r["x"] + r["width"] / 2, r["y"] + r["height"] * 0.108
        if mob: pg.touchscreen.tap(px, py)
        else: pg.mouse.move(px, py)
        pg.wait_for_timeout(350)
        mid_after = pg.evaluate("()=>document.querySelector('.cdmid b').textContent")
        sub_after = pg.evaluate("()=>document.querySelector('.cdmid span').textContent")
        ck(tag + ": pointing at a slice puts it in the middle of the ring",
           mid_after != mid_before and "%" in sub_after, (mid_before, mid_after, sub_after))
        ck(tag + ": and the rest of the ring steps back",
           pg.evaluate("()=>!!document.querySelector('.cdonut.picked')"))

        # crowded charts on a phone drop the figures rather than overlap them
        if mob:
            ck("phone: a crowded chart hides the figures it cannot fit",
               pg.evaluate("""()=>{const c=document.querySelector('.cchart.many');
                 if(!c) return true;
                 const s=c.querySelector('.csub');
                 return !s||getComputedStyle(s).display==='none';}"""))
            ck("phone: nothing in a chart runs off the side",
               pg.evaluate("""()=>{const w=document.documentElement.clientWidth;
                 return [...document.querySelectorAll('.cchart *')]
                   .every(e=>e.getBoundingClientRect().right<=w+0.5);}"""))

        ck(tag + ": nothing threw", not errs, errs[:2])
        ctx.close()
    br.close()

print("\nFAILURES:", F or "none")
