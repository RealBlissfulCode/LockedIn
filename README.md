# The Handbook

Meals, training, shopping, money and schedule for two people, in one static site.
No framework, no bundler, no backend, no accounts. Open `index.html` and it runs.

- **251 recipes**, all gluten-free, macros computed from gram weights rather than typed in
- **168 ingredients** with Walmart Fort Collins and Costco Timnath prices, editable in the app
- **211 exercises** and 32 prebuilt sessions
- **A meal planner** that fills a week with real recipes hitting the macro targets under a budget
- **Financial** planning and real earnings tracking, seeded from the Moving In workbook
- **Schedule** with a weekly template, a shared calendar and "when are we both free"

Everything lives in the browser's localStorage on the device it was entered on.
Nothing is uploaded, there is no analytics, and the save file is the only copy
that survives clearing site data.

## Running it

```
make serve        # http://localhost:8080
make build        # regenerate assets/data.js and stamp the cache version
make check        # fail if anything checked in is stale or invalid
make test         # static checks, core logic, and a real browser pass
make all          # check + test, exactly what CI runs
```

Nothing needs installing for `build`, `check` or `serve` beyond Python 3. `make
test` runs its browser pass only if Playwright happens to be present; without it
the static and logic halves still run and the suite says it skipped.

## What is generated and what is written by hand

`assets/data.js` is **generated**. Do not edit it. It comes from:

| Source | What it holds |
|---|---|
| `src/recipes_1.py` … `recipes_6.py` | the recipes, as ingredient keys and gram weights |
| `src/ingredients.py` | nutrition per 100 g for every ingredient |
| `src/prices.py` | shelf prices per 100 g at each store |
| `src/ingredient_list.py` | which supermarket aisle each ingredient sits in |
| `src/exercises.json`, `sessions.json` | the training database |
| `src/costs.json`, `jobs.json` | the financial seed |

`src/build_data.py` reads those, computes per-serving macros, costs and tags,
validates the result, writes `assets/data.js`, and stamps a content hash into
`index.html` and `sw.js` so a deploy never serves a half-updated cache.

```
python3 src/build_data.py            rebuild
python3 src/build_data.py --check    verify without writing
```

It reports anything suspicious rather than shipping it: a recipe whose stated
calories disagree with its macros by more than 15%, an implausible leucine
fraction, an ingredient with no price, an ingredient with no aisle, a duplicate
recipe id, a recipe with no steps.

Everything under `assets/` other than `data.js` is written by hand and is the
only copy — there is no second source to keep in sync.

## Layout

```
index.html            the shell, the meta tags, and the pre-paint theme stamp
assets/app.css        the design system: tokens, components, motion, both themes
assets/core.js        state, storage, and every calculation. No DOM in this file
assets/ui.js          modals, toasts, charts, the command palette
assets/views.js       one function per page, each returning an HTML string
assets/app.js         the router, and all the wiring and writes
assets/data.js        generated. Edit the Python, not this
sw.js                 offline cache
manifest.webmanifest  installable on a phone
netlify.toml          headers, caching, SPA fallback
src/                  the Python the data file is generated from
test/run.js           the test suite
tools/serve.py        preview server that mirrors the Netlify redirects
```

The four scripts load in order and share one global, `Handbook`. Adding a page
means writing a function in `views.js`, a case in `viewHTML` and a `bind*` in
`app.js`.

## What the app does on its own

- **Plan a week.** Meals → *Plan the week* → *Generate*. It picks real recipes
  for each slot, aiming at that day's targets for whichever person is selected.
  *Change the settings* opens the daily budget, maximum cook time,
  favourites-only and how soon a meal may repeat; the defaults are enough to
  press Generate straight away. Each day shows how close it landed.
- **Turn the plan into a shopping list.** Aggregates every ingredient across the
  planned days, subtracts what is in the pantry, prices each line at the cheaper
  store, and groups it by aisle.
- **Keep the pantry current.** Ticking a shopping list off and hitting *Move
  checked into the pantry* (under More) stocks it; logging a meal draws it back
  down. Aisles collapse as you finish them, and the ones you closed stay closed.
- **Generate a training split.** Writes a repeating week onto the calendar,
  which is what every macro target keys off.
- **Apply the weekly template** to a week of the calendar in one go.
- **Nudge a backup** when the save file is more than a week behind the data.

## How the interface is put together

A few rules the views follow, so a new page fits without thinking about it.

- **One primary action per view.** Whatever you came to do is a filled button.
  Everything rare — CSV, save to a file, load, delete — goes behind a single
  **More** menu built with `H.actionBar(id, actions)`. Nine equal buttons in a
  row means none of them is the answer.
- **Tables are built with `H.table(cols, rows)`, never by hand.** Below 720px
  each row restacks into a card with every value labelled from its column
  header. A column marked `hide: true` is detail that only appears on a wider
  screen. A long table takes `limit:` and shows the rest on demand, because a
  forty-row table restacked as cards is a very long page.
- **Anything you tap is at least 38px**, and a control that is painted smaller
  than that (a switch, a checkbox) sits inside a larger hit area. On the
  shopping list the whole row is the tick target.
- **Nothing may run off the right edge**, at any width, on any route. The test
  suite walks every page at 390, 768 and 1280 and fails on an element that
  overflows or clips with no way to scroll to the rest.
- **A phone gets a different shape, not a squeezed one.** A recipe is a poster
  on a laptop and a row on a phone; a menu is a popover on a pointer device and
  a bottom sheet on a touch screen.

## Keyboard

| | |
|---|---|
| <kbd>Ctrl</kbd>/<kbd>⌘</kbd> <kbd>K</kbd> or <kbd>/</kbd> | search recipes, exercises, lists, pages and actions |
| <kbd>1</kbd>–<kbd>5</kbd> | jump to a section |
| <kbd>Ctrl</kbd>/<kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>P</kbd> | switch person |
| <kbd>Esc</kbd> | close a dialog |

## Your data

**Save to file**, on the Settings page behind the gear, downloads the whole
state as `handbook-data-YYYY-MM-DD.json`: profiles, ingredient edits, every
shopping list, the pantry, the meal plan, favourites, custom recipes, photos,
every logged day, shifts, costs, scenarios and the schedule. **Load a file**
restores it. Both are also in the Ctrl-K search.

Because storage is per browser and per device, it does not sync between a phone
and a laptop by itself. Save on one, Load on the other.

Storage caps at roughly 5 MB, and the Settings page shows how much of it is gone.
Photos are the only thing big enough to matter; they are downscaled to 900 px and
compressed on the way in.

A save from the previous version loads without losing anything — the meal plan,
the pantry and the preferences are filled in from the defaults on the way through.

## Downloads

Recipe cards as PNG, shopping checklists as TXT, shopping lists as CSV, a single
shopping list as JSON that can be loaded back, the ingredient list as CSV, the
pantry as CSV, the meal plan as CSV, shifts as CSV, the daily log as CSV, and the
whole state as JSON.

## Deploying

Netlify, publish directory `.`, build command empty. `netlify.toml` already sets
the headers, the immutable caching for hashed assets, and the SPA fallback.
Every push redeploys.

Anything static works — the app makes no network requests of its own beyond the
webfont, and falls back to system fonts without it.

## Design notes

The palette is warm paper and forest green in light, and a warm near-black in
dark. Dark is a separately chosen palette rather than an inverted one, so the
paper never turns blue-grey. The theme is stamped onto `<html>` by a small
inline script before first paint, so a reload in dark mode does not flash white.

Chart series colours (`--s1` … `--s4`) were validated for colour-blind separation
and contrast against both surfaces. Do not nudge them by eye; re-validate if they
need to change.

## Known limits

- No sync between devices. By design, since there is no server.
- Prices are Aug 2026 estimates for Fort Collins and drift. Edit them in the app,
  which recosts every recipe using that ingredient immediately.
- Leucine is an estimate within about 10 percent where USDA has no amino acid
  profile.
- The planner works from the recipe catalogue's macros, so a day it calls "on
  target" is on target for the recipes as written, at the servings shown.
- Recipe photos are yours to add. No stock imagery is bundled.
