# The Meal Handbook

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
