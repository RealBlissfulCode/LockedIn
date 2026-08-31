# The Handbook

Meals, training, shopping, money and schedule for two people. One HTML file,
no framework, no build step, no backend, no accounts.

- 251 recipes, gluten-free, macros computed from gram weights
- 168 ingredients priced at whichever of Walmart Fort Collins or Costco Timnath is cheaper
- 211 exercises and 32 prebuilt sessions
- Financial planning with scenarios, plus real earnings tracking
- Schedule with a weekly template and a shared time-ordered calendar
- Dark and light themes

## Deploy

Netlify: **Add new site, Import an existing project**, pick the repo.
Build command **empty**, publish directory `.`

Or drag this folder onto app.netlify.com.

## Files

```
index.html               the entire app, self-contained
manifest.webmanifest     lets it install to a phone home screen
icons/                   app icons
netlify.toml             headers and the SPA redirect
src/                     Python that regenerates index.html (not deployed)
```

There is deliberately **no service worker**. Earlier versions cached assets and a
partial upload could leave a new page running old code. With one file and no cache,
what you upload is exactly what loads.

## Your data

Everything saves to this browser on this device. Nothing is uploaded, there is no
backend and no analytics.

The gear icon opens Settings. **Save to a file** downloads everything as
`handbook-data-YYYY-MM-DD.json`: profiles, ingredient edits, shopping lists,
favourites, custom recipes, photos, every logged day, shifts, costs, scenarios and
the schedule. **Load a file** restores it. That file is also how to hand the data
over for changes, so a new version can be built on top of real entries.

Because storage is per browser and per device, it does not sync between a phone and
a laptop. Save on one, Load on the other.

Storage caps around 5 MB. Photos are the only thing large enough to matter; they are
downscaled to 900 px on the way in.

## Rebuilding index.html

```
cd src && python3 build.py && python3 -c "import build_app"
```

Prices live in `src/prices.py` as dollars per 100 g, two columns. Editing an
ingredient price inside the app is easier and updates every recipe that uses it.

## Known limits

- No sync between devices, by design, since there is no server.
- Prices are Aug 2026 estimates for Fort Collins and drift.
- Leucine is an estimate within about 10 percent where USDA has no amino acid profile.
- Recipe photos are yours to add. No stock imagery is bundled.
