# LockedIn

Meals, training, shopping, money, plans and schedule for two people. One HTML
file, no framework, no backend, no database, no accounts.

- 251 recipes, gluten-free, macros computed from gram weights
- 168 ingredients priced at whichever of Walmart or Costco is cheaper
- 211 exercises, 32 sessions, and a session suggested from what has not been trained lately
- Financial planning with scenario snapshots, real earnings tracking, strategy
  lists and big-purchase comparisons
- Every income and cost line has a switch, so a plan can be re-cut without
  deleting anything, and charts that redraw as you flip them
- Planning: collections, subsections and checklists for anything that is not money or food
- Schedule templates: as many as you like, each repeating weekly, every other
  week or once a month, either left running or applied over a stretch of dates
- Recipe lists, shopping lists, strategy lists, plans, big-purchase comparisons
- Dark and light themes, and it installs to a phone home screen

## The passcode

The app is behind a four digit code. It is **2121**, set in `PASSCODE` at the top
of `src/build.py`. Change it there and rebuild and it changes everywhere.

**Be clear about what this protects.** Everything personal is encrypted into the
page at build time. What we earn, what we owe, where we might live, the strategy
lists, the plans, and the application code itself, which carries our names and the
placeholder text in every editor. Until the right code is entered, View
Source shows a lock screen, the recipe database and a block of base64. There is
no readable copy of any of it anywhere in the file.

What it does **not** do is survive someone determined. Four digits is ten thousand
guesses. The key derivation is deliberately slow (200,000 PBKDF2 rounds, about
80 ms per guess) so a full sweep costs hours rather than seconds, but that is the
ceiling of what a four digit code can buy. It stops anyone who finds the URL. It
would not stop somebody who wanted in.

The recipe and exercise database ships **unencrypted**, because it is generic and
because base64 does not compress: sealing it would turn ~150 KB over the wire into
~1.3 MB. That trade only holds while nothing personal is in it, so `src/build.py`
keeps a `FORBIDDEN` list and **refuses to build** if one of our names, employers,
towns or diagnoses reaches the unencrypted half. If it stops you, either reword
the text or move it into `src/private_seed.py`.

The browser remembers the code so it does not ask every time. Settings has a
**Lock this device** button that forgets it. The data itself is never touched
by locking.

Decryption needs `crypto.subtle`, which browsers only expose over **https or
localhost**. The gate says so if it is opened over plain http.

## Time and mobile

Times are stored as 24h `HH:MM`, because that is what `<input type="time">`
speaks and what sorts correctly, and never shown that way. Everything on screen
goes through `t12()` / `range12()`: "8am", "8am – 5pm".

On a phone the editors rise from the bottom as a sheet with a sticky header and
a full-width Save, rather than floating in the middle where the keyboard covers
them. Fields are 16px, which is the threshold below which iOS zooms the page on
focus and leaves it zoomed. Buttons and close targets are sized for a thumb.
Under 560px a calendar cell is about 45px wide, so instead of 8px event text
ellipsised to nothing, each day carries one dot per kind of thing on it and the
day panel underneath holds the detail.

## Schedule templates

A template is a named set of things that repeat, keyed by weekday. There can be
as many as you want; star the ones you use most and they sort to the top.

Each one repeats **every week**, **every other week**, **once a month in the same
week**, or **only when you apply it**. Every other week and once a month line up
against the "counting from" date, so an every-other-Monday shift stays on the
right Mondays and a first-Sunday thing stays on the first Sunday.

There are two ways to use one:

- **Keep it running.** Its items appear on every matching day on their own.
  Nothing is copied into a day, so turning it off clears it everywhere at once
  and there are never stale duplicates to hunt down. Running items show with the
  template's name next to them.
- **Apply it.** Copies the items onto real days over **this week**, **this
  month**, **the next 4 weeks** or **the next 3 months**, so individual days can
  then be edited without touching the template. Days that already have the same
  item are skipped, so applying twice is safe.

The old single weekly template is folded into a collection called "My week" the
first time the app opens, so nothing already entered is lost.

## Syncing between devices

One JSON file on the server holds the shared state. Every device pulls it when it
opens, when it comes back to the front, and on a slow timer, and pushes a
debounced copy about a second after you change something. Add a plan on a phone
and it is on the laptop the next time that tab is looked at.

The pill in the header says which it is: **Synced**, **Saving**, **Checking**,
**Offline**, or **Local only**. Tap it to force a sync. Settings has the version
number and the last sync time.

`api/sync.php` is generated by the build. It needs PHP, which Hostinger has by
default. If the endpoint is missing the app notices, says **Local only**, and
keeps working exactly as it did before, saving to that browser.

**Where the file lives.** `handbook-data/state.json`, one level above the web
root where the host allows it, otherwise `api/data/` with a deny rule written
next to it. `.htaccess` blocks `.json` either way. One previous version is kept
as `state.json.bak`.

**Merging.** Two devices editing at once do not overwrite each other. Every
top-level part of the state carries the time it last actually changed, and a
push that arrives against a moved version comes back 409 with the server's copy
so the two get merged instead. Edit the budget on a laptop while the shopping
list changes on a phone and both survive. The calendar merges one date at a
time, since that is the part two people are most likely to touch together.

What it will not do is merge two edits to the *same* list in the same moment.
The later one wins. Fixing that properly needs per-field history, which is a lot
of machinery for two people who are rarely in the same list at the same second.

`who` and `theme` are deliberately not synced. Which of you is selected, and
whether it is dark, belong to the device.

**Who can read it.** The endpoint takes a token derived from the passcode, so it
is exactly as private as the app: anyone with the code and the URL can read the
file. That is the same boundary as the app itself, not a weaker one, but it does
mean the sync file is not a second layer of protection.

## Rebuilding

The app is generated from the Python in `src/`. Nothing is typed by hand into
`index.html`.

```
python3 src/build.py
```

That rewrites `index.html`. Commit it and push.

```
python3 src/build.py --check
```

Rebuilds in memory and exits non-zero if the committed `index.html` is stale or
if a recipe fails validation. Worth running before a deploy.

| Where | What is in it |
| --- | --- |
| `src/build.py` | The only build script. Recipe maths, the encryption, the HTML shell. |
| `src/private_seed.py` | Everything personal. The only file that knows where we might live. |
| `src/gate.py` | The lock screen and the decryption client. |
| `src/app_sync.py` | Pull, push, and the per-branch merge. |
| `src/sync_php.py` | The server endpoint, written out to `api/sync.php`. |
| `src/app_core.py` | State, storage, scenarios, the one-time seed. |
| `src/app_charts.py` | The chart kit: columns, waterfall, donut, line, count-up. |
| `src/app_views1.py` | Meals, recipe detail, shopping, ingredients. |
| `src/app_views2.py` | Training, financial, strategies, purchases, planning, schedule, templates. |
| `src/app_wire.py` | Router, event wiring, every editor modal. |
| `src/spa_css.py` | The whole stylesheet. |
| `src/recipes_1..6.py`, `ingredients.py`, `prices.py` | The food database. |
| `src/exercises.json`, `sessions.json` | The training database. |
| `src/costs.json`, `jobs.json` | Seed budget lines. Encrypted into the page. |

Prices are in `src/prices.py` as dollars per 100 g, two columns. Editing a price
inside the app is easier and updates every recipe that uses it.

## Switching a money line off

Every income line and every cost line carries an `off` flag, and the Financial
page puts a switch on each one. Off does not mean deleted. The row stays where it
is, keeps all four of its estimates, and stops counting anywhere: the totals, the
charts, the section splits and the twelve month projection. Switch it back and
every number goes back to exactly what it was.

The switches come in three sizes. One per line in the two tables at the bottom
of the page. One per cost section and one per earner in the legends beside the
donuts, which move a whole group at once. And All on / All off above each table.

Since `off` lives on the line, it is part of what a scenario snapshots. Saving
"Renting, both grinding" stores which lines were counted at the time, opening it
brings them back, and flipping a switch while a scenario is open marks it unsaved
the same way editing a figure does. The scenario table's **Off** column counts
what each snapshot has parked.

A line saved before any of this existed carries no flag, which counts as on, so
every scenario made earlier still totals to what it always did.

## The charts

`src/app_charts.py` holds the lot, about a hundred and fifty lines with nothing
behind it. Columns, stacks and the waterfall are plain HTML. A div with a
percentage height is already a bar, it picks up the theme variables for free, and
its labels are real text at a real size. Only the donut and the projection line
are SVG, because HTML cannot draw an arc, and neither of those carries text.

All the motion is in CSS, so the `prefers-reduced-motion` rule at the bottom of
the stylesheet kills the lot in one place. Every chart already sits at its
finished state and the keyframes only animate towards it. The one bit of motion
in JavaScript is the money figures counting up from zero, and that checks the
same media query itself and leaves the final text alone when it is set.

## The seeded lists are not templates

The apartments, the houses, the strategy tiers and the plans seed **once**, the
first time a browser unlocks the app. From that moment they are ordinary rows.
Rename them, edit them, delete them, and they stay however you left them. A
deleted list does not come back on the next deploy, and a rebuild does not
overwrite an edit. Two flags in `app_core.py`, `seeded` and `seeded6`, are the
whole mechanism.

If you want a clean re-seed, Settings has **Erase all data**.

## Accounts, households and the API

The old model was one household with a shared passcode and one JSON file on the
server. That is being replaced by real accounts. `api/` is the whole of it and
it needs PHP 8 and MySQL, both of which Hostinger has.

| File | What it does |
| --- | --- |
| `api/schema.sql` | Six tables. Run it with `php api/migrate.php`. |
| `api/config.sample.php` | Copy to `config.php` and fill in. Never committed. |
| `api/lib/google.php` | Checks the signature on a Google ID token. No library. |
| `api/lib/auth.php` | Sessions. The cookie holds the token, the table holds its hash. |
| `api/lib/store.php` | Households, seats, invite codes, the state documents. |
| `api/auth.php` | Sign in, sign out, who am I. |
| `api/household.php` | Members, invites, joining, leaving, handing over. |
| `api/doc.php` | Read and write documents, with versions. |

### Why there is no client secret anywhere

The browser asks Google for an ID token and posts it here. The server checks the
signature against Google's published keys and reads the claims off it. That is
the whole handshake. Nothing in this app has a secret that could leak, and the
client id in `config.php` is meant to be public.

`api/lib/google.php` does the checking by hand: pull the key id off the token
header, find the matching key in Google's JWKS, turn that key into a PEM, and
hand it to openssl. Then check the issuer, the audience, the expiry and that
Google says the email address is verified. Any one of those failing is a flat
refusal with no explanation, because the only person who wants to know which
check failed is someone probing it.

### Documents

`shared` is the household's copy and everybody in it reads and writes it.
`private:<accountId>` belongs to one person and the server will not hand it to
anyone else. That second one is what makes hiding a surprise on the schedule
actually hidden, rather than just not drawn.

Writes carry the version you last read. If the row moved on in the meantime the
write is refused with a 409 and the current copy comes back, so two phones
editing at once merge instead of one silently winning.

### Seats

Seats come from the plan: two on free, six on paid. A seat can sit there with
nobody in it, which is how you put someone on the meal plan and the schedule
before they have ever signed in. When they join with an invite code they claim
that waiting seat rather than getting a new one, so everything already written
against their name carries over.

Leaving is a real cleanup. The seat goes, that person's private documents go
with it, and the shared document stays because it belonged to the household.
An owner cannot walk out on other people, so they hand it over first or take
the household down with them.

### Setting it up

1. Hostinger, Databases, MySQL Databases. Make a database and a user, tick all
   privileges. Note the four values.
2. Copy `api/config.sample.php` to `api/config.php` and fill them in, plus the
   Google client id.
3. `php api/migrate.php` over SSH. No SSH: put a random string in
   `api/.migrate-key`, hit `/api/migrate.php?key=thatstring`, delete the file.
4. Check `/api/config.php` returns 403 or 404 in a browser. `api/.htaccess`
   should see to it, but check.

### Running the tests

Nothing here talks to Google. `tools/fakegoogle.php` makes its own keypair,
drops the public half where the app caches Google's signing keys, and signs
tokens with it, so the real signature checking runs against them.

    php api/migrate.php
    php -S 127.0.0.1:8080 -t .
    tools/apitest.sh

Forty six checks covering token verification, tampered and expired and wrongly
addressed tokens, the CSRF header, document versions and conflicts, one
person's private scope against another's, seat limits, invites, joining and
leaving.

## Deploying to a subdomain with Hostinger

Hostinger pulls straight from the repo, so a push becomes a deploy.

1. hPanel, then **Websites**, then create the subdomain (e.g. `handbook.jaronnorris.com`).
   Note the folder it makes, usually `public_html/handbook` or a separate
   `domains/handbook.jaronnorris.com/public_html`.
2. hPanel, then **GIT**. Repository: this repo's URL. Branch: `main`.
   Directory: the subdomain folder from step 1.
3. **Create**. Hostinger clones it.
4. Every push after that: hit **Deploy**, or paste Hostinger's webhook URL into
   GitHub under Settings, Webhooks, and a push deploys on its own.

There is no build step on the server. The build runs here, `index.html` is
committed, and Hostinger serves the files exactly as they sit in the repo.

If the repo is private, Hostinger shows an SSH key on the GIT page. Copy it into
GitHub under Settings, Deploy keys. Read access is enough.

### What ends up in the web root

```
index.html               the entire app, self-contained
api/sync.php             the sync endpoint, generated by the build
.htaccess                gzip, caching, https redirect, security headers, noindex
robots.txt               keeps it out of search results
manifest.webmanifest     lets it install to a phone home screen
icons/                   app icons
src/                     the Python that regenerates index.html, never served
```

`.htaccess` blocks `.py`, `.json` and `.md`, and `src/.htaccess` denies that
directory outright, so the Python is in the repo but not reachable from the web.
Both are hidden files that git tracks normally, so confirm they made it with
`git ls-files` before deploying, because without the top one you lose gzip, the
https redirect and the noindex header.

Paths are all relative, so a subfolder deploy works without changing anything.

There is no service worker. One file with no cache means what you push is exactly
what loads, and `.htaccess` sets `max-age=0` on HTML so a deploy is live at once.

## Your data

Everything saves to that browser on that device. Nothing is uploaded, there is no
backend and no analytics. Hostinger only ever serves the file.

The gear icon opens Settings. **Save to a file** downloads everything as
`handbook-data-YYYY-MM-DD.json`: profiles, ingredient edits, shopping lists,
favourites, custom recipes, photos, every logged day, shifts, costs, scenarios,
strategies, purchases, plans and the schedule. **Load a file** restores it.

Because storage is per browser and per device, it does not sync between a phone
and a laptop on its own. Save on one, Load on the other. Storage caps around
5 MB, and photos are the only thing large enough to matter.

## Local preview

```
python3 tools/serve.py 8080
```

`localhost` counts as a secure context, so the gate works there.

## Known limits

- Two edits to the same list in the same moment: the later one wins.
- A four digit passcode is a speed bump, not security. See above.
- Prices are Aug 2026 estimates for Northern Colorado and drift.
- Leucine is an estimate within about 10 percent where USDA has no amino acid profile.
- Recipe photos are yours to add. No stock imagery is bundled.
