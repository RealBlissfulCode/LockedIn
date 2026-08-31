# -*- coding: utf-8 -*-
"""Builds the deployable repo for the five-section Handbook.

    python3 repo2.py    ->  /home/claude/repo  (zipped into outputs)
"""
import json, os, shutil, sys, hashlib

ROOT = "/home/claude/repo"

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>The Handbook</title>
<meta name="description" content="Meals, training, shopping, money and schedule for two people. Everything stays on the device.">
<meta name="theme-color" content="#FBFAF7">
<meta name="color-scheme" content="light">

<link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Handbook">
<link rel="apple-touch-icon" href="/icons/icon-192.png">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="icon" href="/icons/icon-192.png" sizes="192x192">

<meta property="og:title" content="The Handbook">
<meta property="og:description" content="251 recipes, 211 exercises, shopping, budget and schedule in one app.">
<meta property="og:type" content="website">
<meta property="og:image" content="/icons/icon-512.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/app.css">
</head>
<body>
<header class="top"><div class="topin">
  <div class="brand">The <em>Handbook</em></div>
  <div class="whoswitch" id="who"></div>
  <nav class="tabs" id="tabs"></nav>
  <button class="iconbtn" id="settings" title="Settings"></button>
</div></header>

<main class="wrap" id="view">
  <noscript><div style="padding:44px 0">
    <h1>JavaScript is off</h1>
    <p>This is an app rather than a page, so it needs JavaScript switched on.</p>
  </div></noscript>
</main>
<nav class="btmnav" id="btm"></nav>

<script src="/assets/data.js"></script>
<script src="/assets/app.js"></script>
<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});
}
</script>
</body>
</html>
"""

NETLIFY = """# Static site. No build step, no dependencies.
[build]
  publish = "."
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=(self)"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/icons/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/index.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[headers]]
  for = "/sw.js"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"
"""

MANIFEST = {
  "name": "The Handbook",
  "short_name": "Handbook",
  "description": "Meals, training, shopping, money and schedule.",
  "start_url": "/", "scope": "/", "display": "standalone",
  "background_color": "#FBFAF7", "theme_color": "#1F4D3A",
  "icons": [
    {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
  "shortcuts": [
    {"name": "Meals", "url": "/#/meals"},
    {"name": "Shopping", "url": "/#/shopping"},
    {"name": "Financial", "url": "/#/financial"},
    {"name": "Schedule", "url": "/#/schedule"}],
}

SW = """/* Network first, cache as fallback. A redeploy always wins; the cache only
   exists so the app still opens with no signal. */
var CACHE='handbook-__V__';
var CORE=['/','/index.html','/assets/app.css','/assets/app.js','/assets/data.js',
          '/manifest.webmanifest','/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];
self.addEventListener('install',function(e){self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(CORE).catch(function(){});}));});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(k){
    return Promise.all(k.map(function(x){if(x!==CACHE)return caches.delete(x);}));
  }).then(function(){return self.clients.claim();}));});
self.addEventListener('message',function(e){ if(e.data==='skipWaiting') self.skipWaiting(); });
self.addEventListener('fetch',function(e){
  var req=e.request; if(req.method!=='GET')return;
  var u; try{u=new URL(req.url);}catch(err){return;}
  if(u.origin!==location.origin)return;
  e.respondWith(
    fetch(req).then(function(res){
      if(res&&res.status===200){
        var copy=res.clone();
        caches.open(CACHE).then(function(c){c.put(req,copy);});
      }
      return res;
    }).catch(function(){
      return caches.match(req).then(function(hit){
        return hit || caches.match('/index.html');
      });
    })
  );
});
"""

README = """# The Handbook

Meals, training, shopping, money and schedule for two people, in one static site.
No framework, no build step, no backend, no accounts.

- **251 recipes**, all gluten-free, macros computed from gram weights
- **168 ingredients** with Walmart Fort Collins and Costco Timnath prices, fully editable
- **211 exercises** and 32 prebuilt sessions
- **Financial** planning and real earnings tracking, seeded from the Moving In workbook
- **Schedule** with a weekly template and a shared calendar

## Deploy to Netlify

**Drag and drop.** Drop this folder onto app.netlify.com. Live in seconds.

**From the repo.** Better, because every push redeploys.

```
git init
git add .
git commit -m "Handbook"
git branch -M main
git remote add origin https://github.com/YOURNAME/Meal-App.git
git push -u origin main
```

Then Netlify: Add new site, Import an existing project, pick the repo.
Build command **empty**, publish directory `.` — `netlify.toml` already sets headers,
caching and the SPA fallback.

## Layout

```
index.html               shell and meta
assets/app.css           the design system
assets/app.js            state, router, all five sections
assets/data.js           recipes, ingredients, exercises, sessions, seed budget
manifest.webmanifest     installable on a phone
sw.js                    offline cache
icons/                   app icons
netlify.toml             headers, caching, redirects
src/                     Python that regenerates assets/data.js
```

## Your data

Everything lives in this browser's localStorage on this device. Nothing is uploaded,
there is no backend and no analytics.

**Save** in the top bar downloads the whole state as `handbook-data-YYYY-MM-DD.json`:
profiles, ingredient edits, every shopping list, favourites, custom recipes, photos,
every logged day, shifts, costs, scenarios and the schedule. **Load** restores it.

That file is also how you hand the data back for changes. Send the JSON and the next
version can be built on top of exactly what is in it, rather than starting clean.

Because storage is per browser and per device, it does not sync between a phone and a
laptop by itself. Save on one, Load on the other.

Storage caps at roughly 5 MB. Photos are the only thing big enough to matter; they are
downscaled to 900 px and compressed on the way in.

## Editing

- **Look** -> `assets/app.css`
- **Behaviour** -> `assets/app.js`. Views are `vMeals`, `vRecipe`, `vShopping`,
  `vIngredients`, `vTraining`, `vExercises`, `vFinancial`, `vActual`, `vPurchases`,
  `vSchedule`, `vWeekTemplate`. Each returns an HTML string.
- **Recipes, prices, exercises** -> `assets/data.js` is generated. Edit the Python in
  `src/` and re-run, or edit an ingredient price directly in the app, which is easier
  and updates every recipe that uses it.

Regenerate the data file:

```
cd src && python3 repo2.py
```

## Downloads the app can produce

Recipe cards as PNG, shopping checklists as TXT, shopping lists as CSV, a single
shopping list as JSON that can be loaded back, the ingredient list as CSV, shifts as
CSV, the daily log as CSV, and the whole state as JSON.

## Known limits

- No sync between devices. By design, since there is no server.
- Prices are Aug 2026 estimates for Fort Collins and drift. Edit them in the app.
- Leucine is an estimate within about 10 percent where USDA has no amino acid profile.
- Recipe photos are yours to add. No stock imagery is bundled.
"""

GITIGNORE = """.DS_Store
Thumbs.db
node_modules/
__pycache__/
*.pyc
.netlify/
.env
"""


def icon_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#14140F"/><stop offset="0.55" stop-color="#1F4D3A"/>
<stop offset="1" stop-color="#2C6B50"/></linearGradient></defs>
<rect width="512" height="512" rx="112" fill="url(#g)"/>
<circle cx="200" cy="262" r="86" fill="none" stroke="#F2EFE8" stroke-width="16" opacity="0.55"/>
<circle cx="200" cy="262" r="46" fill="none" stroke="#F2EFE8" stroke-width="12" opacity="0.35"/>
<path d="M320 168v188M352 168v54a20 20 0 0020 20v114M384 168v188"
  stroke="#F2EFE8" stroke-width="17" stroke-linecap="round" fill="none" opacity="0.75"/>
</svg>"""


def icon_png(size):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (size, size), "#14140F")
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        r = int(0x14 + (0x2C - 0x14) * t)
        g = int(0x14 + (0x6B - 0x14) * t)
        b = int(0x0F + (0x50 - 0x0F) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b))
    s = size / 512.0
    cx, cy, R = 200 * s, 262 * s, 86 * s
    w = max(3, int(16 * s))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(242, 239, 232), width=w)
    r2 = 46 * s
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=(200, 205, 195), width=max(2, int(12 * s)))
    for x0 in (320, 352, 384):
        d.line([(x0 * s, 168 * s), (x0 * s, 356 * s)], fill=(242, 239, 232), width=max(3, int(17 * s)))
    return img


def main():
    sys.path.insert(0, "/home/claude/build")
    os.chdir("/home/claude/build")
    ns = {}
    exec(open("build.py").read().split("htm = build_html")[0], ns)
    import build_app
    out = build_app.build(ns["DATA"], ns["ING"])

    data_js = ("/* Generated by src/repo2.py. Edit the Python, not this file. */\n"
               "window._DATA=" + json.dumps(out["blob"], separators=(",", ":")) + ";\n")
    app_js = "(function(){\n'use strict';\nvar _D=window._DATA;\n" + out["js"] + "\n})();\n"
    css = out["css"]
    ver = hashlib.sha1((data_js + app_js + css).encode()).hexdigest()[:8]

    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    for p in ("assets", "icons", "src"):
        os.makedirs(f"{ROOT}/{p}", exist_ok=True)

    open(f"{ROOT}/index.html", "w").write(INDEX.replace("__V__", ver))
    open(f"{ROOT}/assets/app.css", "w").write(css)
    open(f"{ROOT}/assets/app.js", "w").write(app_js)
    open(f"{ROOT}/assets/data.js", "w").write(data_js)
    open(f"{ROOT}/netlify.toml", "w").write(NETLIFY)
    open(f"{ROOT}/manifest.webmanifest", "w").write(json.dumps(MANIFEST, indent=2))
    open(f"{ROOT}/sw.js", "w").write(SW.replace("__V__", ver))
    open(f"{ROOT}/README.md", "w").write(README)
    open(f"{ROOT}/.gitignore", "w").write(GITIGNORE)
    open(f"{ROOT}/icons/icon.svg", "w").write(icon_svg())
    for s in (192, 512):
        icon_png(s).save(f"{ROOT}/icons/icon-{s}.png")

    keep = ["ingredients.py", "prices.py", "ingredient_list.py", "build.py", "build_app.py",
            "app_core.py", "app_views1.py", "app_views2.py", "app_wire.py", "spa_css.py",
            "repo2.py", "exercises.json", "sessions.json", "costs.json", "jobs.json"] + \
           [f"recipes_{i}.py" for i in range(1, 7)]
    for f in keep:
        if os.path.exists(f):
            shutil.copy(f, f"{ROOT}/src/{f}")

    return ver, out


if __name__ == "__main__":
    v, o = main()
    print("version", v, "| recipes", o["recipes"], "| ingredients", o["ings"],
          "| exercises", o["ex"], "| sessions", o["sess"])
