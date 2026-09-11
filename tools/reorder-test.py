"""Moving an income or cost line and having it stay moved.

Drags with real pointer events at desktop and phone size, checks the list came
back in the new order, checks it survived a reload, and checks the keyboard
does the same job without a mouse.
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

NAMES = """(k)=>[...document.querySelectorAll('[data-grip="'+k+'"]')]
  .map(g=>g.closest('tr').querySelector('td.hd b').textContent)"""

def boot(pg, sub):
    pg.goto(URL); pg.wait_for_timeout(800)
    pg.evaluate("""async(t)=>{await fetch('api/auth.php?do=google',{method:'POST',
      headers:{'Content-Type':'application/json','X-LockedIn':'1'},credentials:'same-origin',
      body:JSON.stringify({credential:t})});}""", tok(sub=sub, email=sub + "@x.com", name="Jaron"))
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
    pg.evaluate("location.hash='#/financial'"); pg.wait_for_timeout(1400)

def drag(pg, kind, frm, to):
    """Pick a grip up and put it down where another one started.

    The destination is fixed before anything moves. Rows slide out of the way
    as you drag, so aiming at where the target sits right now chases a moving
    goalpost and stops short. Aiming at where it began is what a hand does.

    The target is often off screen, which is the normal case with two dozen
    cost lines on a phone, so the pointer parks near the edge and lets the page
    come to it, exactly as a thumb would.
    """
    sel = '[data-grip="%s"]' % kind
    scroll = lambda: pg.evaluate("()=>window.pageYOffset||0")
    pg.query_selector_all(sel)[frm].scroll_into_view_if_needed()
    pg.wait_for_timeout(200)

    # Put the grip somewhere a pointer can actually reach it. Scrolling it into
    # view can leave it hard against an edge, and a press aimed at an edge
    # lands on the page behind instead of on the grip.
    h = pg.evaluate("()=>window.innerHeight")
    for _ in range(6):
        b = pg.query_selector_all(sel)[frm].bounding_box()
        mid = b["y"] + b["height"] / 2
        if 90 < mid < h - 90:
            break
        pg.evaluate("(d)=>window.scrollBy(0,d)", int(mid - h / 2))
        pg.wait_for_timeout(160)
    grips = pg.query_selector_all(sel)
    a = grips[frm].bounding_box()
    b = grips[to].bounding_box()
    y0 = scroll()
    x = a["x"] + a["width"] / 2
    doc_from = a["y"] + a["height"] / 2 + y0
    doc_to = b["y"] + b["height"] / 2 + y0

    pg.mouse.move(x, doc_from - y0)
    pg.mouse.down()
    pg.wait_for_timeout(60)

    for _ in range(120):
        want = doc_to - scroll()
        if 34 < want < h - 34:
            pg.mouse.move(x, want)
            pg.wait_for_timeout(70)
            if abs((doc_to - scroll()) - want) < 2:
                break
        else:
            pg.mouse.move(x, 26 if want <= 34 else h - 26)
            pg.wait_for_timeout(70)
    # Land on the spot and let the last frame paint before letting go. Without
    # this the release can be read against a position the page has not drawn
    # yet, and the line quietly goes back where it came from.
    if not pg.query_selector("tr.lift"):
        raise AssertionError("the drag never started: nothing was picked up")
    want = doc_to - scroll()
    if 0 < want < h:
        pg.mouse.move(x, want)
    pg.wait_for_timeout(160)
    pg.mouse.up()
    pg.wait_for_timeout(400)
    settle(pg)


def settle(pg):
    """Wait for the account to actually have it, not just the screen."""
    pg.wait_for_function(
        "()=>{const p=document.getElementById('syncPill');"
        "return p && /Saved|Offline/.test(p.textContent);}", timeout=15000)
    pg.wait_for_timeout(250)

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                            args=["--no-sandbox"])
    for tag, W, H, mob in [("desk", 1512, 950, False), ("phone", 390, 844, True)]:
        ctx = br.new_context(viewport={"width": W, "height": H}, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); pg.on("dialog", lambda d: d.accept())
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        boot(pg, "ro" + tag)

        for kind in ("jobs", "costs"):
            before = pg.evaluate(NAMES, kind)
            ck("%s: %s has lines to move" % (tag, kind), len(before) >= 4, len(before))
            if len(before) < 4: continue

            drag(pg, kind, 0, 2)
            after = pg.evaluate(NAMES, kind)
            want = [before[1], before[2], before[0]] + before[3:]
            ck("%s: %s first line dragged down to third" % (tag, kind), after == want,
               (before[:4], after[:4]))

            pg.reload(); pg.wait_for_timeout(2600)
            pg.evaluate("location.hash='#/financial'"); pg.wait_for_timeout(1200)
            ck("%s: %s order survived a reload" % (tag, kind),
               pg.evaluate(NAMES, kind) == want, pg.evaluate(NAMES, kind)[:4])

            drag(pg, kind, 3, 0)
            now = pg.evaluate(NAMES, kind)
            ck("%s: %s fourth line dragged up to first" % (tag, kind),
               now[0] == want[3], (want[:5], now[:5]))

            pg.focus('[data-grip="%s"][data-ord="0"]' % kind)
            pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(450); settle(pg)
            kb = pg.evaluate(NAMES, kind)
            ck("%s: %s arrow key moves a line down" % (tag, kind),
               kb[1] == now[0] and kb[0] == now[1], (now[:3], kb[:3]))
            ck("%s: %s keeps hold of the grip it moved" % (tag, kind),
               pg.evaluate("()=>document.activeElement.dataset.ord") == "1",
               pg.evaluate("()=>document.activeElement.className"))

            pg.select_option('[data-finsort="%s"]' % kind, "big")
            pg.wait_for_timeout(700)
            vals = pg.evaluate("""(k)=>[...document.querySelectorAll('[data-grip="'+k+'"]')]
              .map(g=>{const r=g.closest('tr');
                const c=[...r.querySelectorAll('td')].filter(x=>x.dataset.l==='Realistic')[0];
                return parseFloat((c?c.textContent:'0').replace(/[^0-9.]/g,''))||0;})""", kind)
            ck("%s: %s sorted biggest first" % (tag, kind),
               all(vals[i] >= vals[i+1] for i in range(len(vals)-1)), vals[:6])
            ck("%s: %s reorder select went back to its label" % (tag, kind),
               pg.evaluate("(k)=>document.querySelector('[data-finsort=\\''+k+'\\']').value", kind) == "")

        ck(tag + ": nothing threw", not errs, errs[:2])
        ctx.close()
    br.close()

print("\nFAILURES:", F or "none")
