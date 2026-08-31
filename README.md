# The Handbook

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
