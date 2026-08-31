# The Handbook

Meals, training, shopping, money and schedule for two people. One HTML file,
no framework, no build step, no backend, no database, no accounts.

- 251 recipes, gluten-free, macros computed from gram weights
- 168 ingredients priced at whichever of Walmart Fort Collins or Costco Timnath is cheaper
- 211 exercises, 32 sessions, and a session suggested from what has not been trained lately
- Financial planning with full scenario snapshots, plus real earnings tracking
- Schedule with recurring weekly rules and a time-ordered shared calendar
- Dark and light themes

## Deploying with Hostinger + GitHub

Hostinger can pull straight from a repo, so a push becomes a deploy.

**Once, to set it up:**

1. Push this folder to GitHub.
   ```
   git init
   git add .
   git commit -m "Handbook"
   git branch -M main
   git remote add origin https://github.com/YOURNAME/Meal-App.git
   git push -u origin main
   ```
2. hPanel, then **Website**, then **GIT**.
3. Repository: your repo URL. Branch: `main`. Directory: leave blank for
   `public_html`, or type a subfolder name to serve it from
   `yourdomain.com/thatname`.
4. **Create**. Hostinger clones it.

**Every time after:** push, then hit **Deploy** in hPanel. If you want it automatic,
copy the webhook URL Hostinger shows you and paste it into GitHub under
Settings, Webhooks. Then a push deploys on its own.

There is **no build step**. Build command stays empty. Hostinger serves the files
exactly as they sit in the repo.

### If the repo is private

Hostinger shows an SSH key on the GIT page. Copy it into GitHub under
Settings, Deploy keys, read access is enough.

## What ends up in the web root

Hostinger clones everything, `src` and `README.md` included. That is harmless:
`.htaccess` blocks `.py`, `.json` and `.md` from being served, so the Python and
this file are in the repo but not reachable from the web.

```
index.html               the entire app, self-contained
.htaccess                gzip, caching, https redirect, security headers, blocks src
manifest.webmanifest     lets it install to a phone home screen
icons/                   app icons
src/                     Python that regenerates index.html, never served
```

`.htaccess` is a hidden file but git tracks it normally. Confirm it made it with
`git ls-files` before deploying, because without it you lose gzip and the https
redirect.

Paths are all relative, so a subfolder deploy works without changing anything.

There is no service worker. One file with no cache means what you push is exactly
what loads, and `.htaccess` sets `max-age=0` on HTML so a deploy is live at once.

## Your data

Everything saves to that browser on that device. Nothing is uploaded, there is no
backend and no analytics. Hostinger only ever serves the file.

The gear icon opens Settings. **Save to a file** downloads everything as
`handbook-data-YYYY-MM-DD.json`: profiles, ingredient edits, shopping lists,
favourites, custom recipes, photos, every logged day, shifts, costs, scenarios and
the schedule. **Load a file** restores it. That file is also how to hand the data
over for changes, so a new version can be built on top of real entries.

Because storage is per browser and per device, it does not sync between a phone and
a laptop on its own. Save on one, Load on the other. Storage caps around 5 MB, and
photos are the only thing large enough to matter.

## Rebuilding index.html

The app is generated from the Python in `src`. Recipes, prices, the exercise
database and the seed budget all live there.

```
cd src
python3 -c "import build, build_app"
```

That rewrites `index.html`. Commit it and push.

Prices are in `src/prices.py` as dollars per 100 g, two columns. Editing an
ingredient price inside the app is easier and updates every recipe that uses it.

## Known limits

- No sync between devices, by design, since there is no server.
- Prices are Aug 2026 estimates for Fort Collins and drift.
- Leucine is an estimate within about 10 percent where USDA has no amino acid profile.
- Recipe photos are yours to add. No stock imagery is bundled.
