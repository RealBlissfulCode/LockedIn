# -*- coding: utf-8 -*-
"""Emits a deploy-ready static site repo from the same source modules.

Run:  python3 repo.py
Out:  /home/claude/repo/   (then zipped to outputs)

The app is split into cacheable assets instead of one giant file, because on a host
you want the browser to cache the 300 KB of recipe data separately from the code you
are actually editing.
"""
import json, os, re, shutil, sys, hashlib

ROOT = "/home/claude/repo"

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>The Meal Handbook</title>
<meta name="description" content="Gluten-free meal system, calculator, grocery builder and daily log for two people.">
<meta name="theme-color" content="#0A1A2F">
<meta name="color-scheme" content="light">

<!-- installable on a phone home screen -->
<link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Meal Handbook">
<link rel="apple-touch-icon" href="/icons/icon-192.png">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="icon" href="/icons/icon-192.png" sizes="192x192">

<meta property="og:title" content="The Meal Handbook">
<meta property="og:description" content="251 gluten-free recipes, live calculator, grocery builder, daily log.">
<meta property="og:type" content="website">
<meta property="og:image" content="/icons/icon-512.png">

<link rel="stylesheet" href="/assets/app.css?v=__V__">
</head>
<body>
<header class="top"><div class="topin">
  <div class="brand">The Meal <em>Handbook</em></div>
  <div class="whoswitch" id="who"></div>
  <button class="tab" id="store" title="Switch store pricing"></button>
  <nav class="tabs" id="tabs"></nav>
</div></header>

<main class="wrap" id="view">
  <noscript>
    <div style="padding:40px 0">
      <h1>JavaScript is switched off</h1>
      <p>This is an app rather than a document, so it needs JavaScript. The printable PDF
      version of the same content does not.</p>
    </div>
  </noscript>
</main>
<nav class="btmnav" id="btm"></nav>

<script src="/assets/data.js?v=__V__"></script>
<script src="/assets/app.js?v=__V__"></script>
<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',function(){
    navigator.serviceWorker.register('/sw.js').catch(function(){});
  });
}
</script>
</body>
</html>
"""

NETLIFY = """# Static site. No build step, no dependencies, nothing to install.
[build]
  publish = "."
  command = ""

# Hash routing means the SPA never requests a deep path, but this covers
# anyone hand-typing a URL.
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

# Assets are versioned with ?v= so they can cache hard.
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/icons/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

# The shell and the worker must never go stale.
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
    "name": "The Meal Handbook",
    "short_name": "Meals",
    "description": "Gluten-free meal system, calculator, grocery builder and daily log.",
    "start_url": "/",
    "scope": "/",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#F6F9FC",
    "theme_color": "#0A1A2F",
    "icons": [
        {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Today", "url": "/#/"},
        {"name": "Recipes", "url": "/#/recipes"},
        {"name": "Grocery list", "url": "/#/grocery"},
    ],
}

SW = """/* Offline shell. Bump CACHE when assets change; the version query does the rest. */
var CACHE='meal-handbook-__V__';
var CORE=['/','/index.html','/assets/app.css?v=__V__','/assets/app.js?v=__V__',
          '/assets/data.js?v=__V__','/manifest.webmanifest',
          '/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];

self.addEventListener('install',function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(CORE).catch(function(){});}));
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){ if(k!==CACHE) return caches.delete(k); }));
  }).then(function(){return self.clients.claim();}));
});

self.addEventListener('fetch',function(e){
  var req=e.request;
  if(req.method!=='GET') return;
  var url=new URL(req.url);
  if(url.origin!==location.origin) return;

  // Shell: network first so a redeploy shows up, cache as the fallback.
  if(req.mode==='navigate'){
    e.respondWith(fetch(req).then(function(res){
      var copy=res.clone(); caches.open(CACHE).then(function(c){c.put('/index.html',copy);});
      return res;
    }).catch(function(){return caches.match('/index.html');}));
    return;
  }
  // Everything else: cache first, it is all immutable and versioned.
  e.respondWith(caches.match(req).then(function(hit){
    return hit || fetch(req).then(function(res){
      if(res && res.status===200){
        var copy=res.clone(); caches.open(CACHE).then(function(c){c.put(req,copy);});
      }
      return res;
    });
  }));
});
"""

README = """# The Meal Handbook

A gluten-free meal system for two people. 251 recipes with computed macros and Fort Collins
pricing, a live calculator, a training-aware recommender, a grocery list builder, and a daily log.

Static site. No framework, no build step, no dependencies. Three files do the work.

## Deploy to Netlify

**Option A, drag and drop.** Go to app.netlify.com, drag this folder onto the deploy area. Live in
about ten seconds. Fine for a first look, but you lose git history.

**Option B, connect the repo.** This is the one worth doing.

1. Create an empty repo on GitHub, then from this folder:
   ```
   git init
   git add .
   git commit -m "Meal handbook"
   git branch -M main
   git remote add origin git@github.com:YOURNAME/meal-handbook.git
   git push -u origin main
   ```
2. In Netlify: Add new site, Import an existing project, pick the repo.
3. Build command: leave empty. Publish directory: `.`
4. Deploy.

Every push to `main` redeploys automatically. `netlify.toml` already sets the caching and
security headers, so there is nothing to configure in the dashboard.

## Repository layout

```
index.html               shell, meta tags, service worker registration
assets/app.css           the whole design system
assets/app.js            router, views, calculator, recommender, downloads
assets/data.js           251 recipes + 167 ingredients as window.MH_DATA
manifest.webmanifest     makes it installable on a phone
sw.js                    offline cache
icons/                   app icons
netlify.toml             headers, caching, SPA fallback
src/                     Python that generates assets/data.js (optional)
```

## Editing

**Change how it looks** -> `assets/app.css`.
**Change how it behaves** -> `assets/app.js`. Views are `vHome`, `vRecipes`, `vRecipe`,
`vGrocery`, `vTraining`, `vCalendar`, `vLearn`. Each returns an HTML string.
**Change a recipe or a price** -> `assets/data.js` is generated, so edit the Python in `src/`
and re-run, or hand-edit the JSON if it is a one-off. Prices live in `src/prices.py` as dollars
per 100 g, two columns, Walmart and Costco.

Regenerate the data file:
```
cd src && python3 repo.py
```

## Data and privacy

Everything the app saves stays in the browser's localStorage on the device. Favourites, lists,
photos, the daily log, both profiles. Nothing is sent anywhere, there is no backend and no
analytics. That also means it does not sync between phone and laptop. Use Export backup on the
Learn page to move it.

Storage limit is around 5 MB, and photos are the only thing large enough to matter. They are
downscaled to 900 px and compressed on the way in, so a few dozen is fine.

## Installing on a phone

Open the site in Chrome or Safari, then Add to Home Screen. It runs full screen without browser
chrome and works offline after the first load.

## Known limits

- localStorage is per browser and per device. No sync by design.
- Prices are Aug 2026 estimates for Fort Collins and drift. They are one file to update.
- Leucine values are estimates within about 10 percent where USDA has no amino acid profile.
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
<stop offset="0" stop-color="#0A1A2F"/><stop offset="0.6" stop-color="#164272"/>
<stop offset="1" stop-color="#2680EB"/></linearGradient></defs>
<rect width="512" height="512" rx="112" fill="url(#g)"/>
<circle cx="256" cy="268" r="118" fill="none" stroke="#7FC4FF" stroke-width="18" opacity="0.35"/>
<circle cx="256" cy="268" r="118" fill="none" stroke="#7FE0A8" stroke-width="18"
  stroke-dasharray="278 463" stroke-linecap="round" transform="rotate(-90 256 268)"/>
<circle cx="256" cy="268" r="118" fill="none" stroke="#FFD166" stroke-width="18"
  stroke-dasharray="139 602" stroke-dashoffset="-278" stroke-linecap="round"
  transform="rotate(-90 256 268)"/>
<text x="256" y="292" text-anchor="middle" font-family="Helvetica,Arial" font-size="96"
  font-weight="800" fill="#ffffff">MH</text>
</svg>"""


def icon_png(size):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (size, size), "#0A1A2F")
    d = ImageDraw.Draw(img)
    for y in range(size):                       # diagonal-ish gradient
        t = y / size
        r = int(0x0A + (0x26 - 0x0A) * t)
        g = int(0x1A + (0x80 - 0x1A) * t)
        b = int(0x2F + (0xEB - 0x2F) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b))
    cx = cy = size / 2
    R = size * 0.30
    w = max(4, int(size * 0.035))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(127, 196, 255), width=w)
    d.arc([cx - R, cy - R, cx + R, cy + R], -90, 110, fill=(127, 224, 168), width=w)
    d.arc([cx - R, cy - R, cx + R, cy + R], 110, 190, fill=(255, 209, 102), width=w)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                               int(size * 0.20))
    except Exception:
        f = ImageFont.load_default()
    t = "MH"
    bb = d.textbbox((0, 0), t, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), t, font=f, fill="white")
    return img


def main():
    sys.path.insert(0, "/home/claude/build")
    os.chdir("/home/claude/build")
    ns = {}
    exec(open("build.py").read().split("htm = build_html")[0], ns)
    DATA, ING = ns["DATA"], ns["ING"]

    import spa, spa_css, spa_js
    recipes = spa.build_recipes(DATA, ING)
    ings = spa.build_ing(ING)
    from ingredient_list import AISLES

    blob = {"recipes": recipes, "ing": ings,
            "aisles": [[a, k] for a, k in AISLES], "learn": spa.LEARN}
    data_js = ("/* Generated. Edit src/ and re-run repo.py rather than editing here. */\n"
               "window.MH_DATA=" + json.dumps(blob, separators=(",", ":")) + ";\n")

    # app.js: read from window.MH_DATA instead of inlined literals
    js = spa_js.APP_JS
    js = js.replace("<script>", "", 1).replace("</script>", "", 1).strip()
    js = js.replace(
        "var R=__RECIPES__, ING=__ING__, AISLES=__AISLES__, LEARN=__LEARN__;",
        "var _D=window.MH_DATA||{recipes:[],ing:{},aisles:[],learn:[]};\n"
        "var R=_D.recipes, ING=_D.ing, AISLES=_D.aisles, LEARN=_D.learn;")
    css = spa_css.APP_CSS.replace("<style>", "", 1).replace("</style>", "", 1).strip()

    ver = hashlib.sha1((data_js + js + css).encode()).hexdigest()[:8]

    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    for p in ["assets", "icons", "src"]:
        os.makedirs(f"{ROOT}/{p}", exist_ok=True)

    open(f"{ROOT}/index.html", "w").write(INDEX.replace("__V__", ver))
    open(f"{ROOT}/assets/app.css", "w").write(css)
    open(f"{ROOT}/assets/app.js", "w").write(js)
    open(f"{ROOT}/assets/data.js", "w").write(data_js)
    open(f"{ROOT}/netlify.toml", "w").write(NETLIFY)
    open(f"{ROOT}/manifest.webmanifest", "w").write(json.dumps(MANIFEST, indent=2))
    open(f"{ROOT}/sw.js", "w").write(SW.replace("__V__", ver))
    open(f"{ROOT}/README.md", "w").write(README)
    open(f"{ROOT}/.gitignore", "w").write(GITIGNORE)
    open(f"{ROOT}/icons/icon.svg", "w").write(icon_svg())
    for s in (192, 512):
        icon_png(s).save(f"{ROOT}/icons/icon-{s}.png")

    for f in ["ingredients.py", "prices.py", "ingredient_list.py", "spa.py", "spa_css.py",
              "spa_js.py", "build.py", "content.py", "voice.py", "formulas.py", "calculator.py",
              "collections_page.py", "household.py", "theme.py", "app.py"] + \
             [f"recipes_{i}.py" for i in range(1, 7)]:
        if os.path.exists(f):
            shutil.copy(f, f"{ROOT}/src/{f}")
    shutil.copy("/home/claude/build/repo.py", f"{ROOT}/src/repo.py")

    return ver, len(recipes), len(ings)


if __name__ == "__main__":
    v, nr, ni = main()
    print("version", v, "| recipes", nr, "| ingredients", ni)
