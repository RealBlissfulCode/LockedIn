#!/usr/bin/env node
/* Smoke tests for The Handbook.
 *
 *   node test/run.js            static checks only
 *   node test/run.js --browser  also drive a real Chromium through every route
 *
 * The static half needs nothing installed. The browser half uses Playwright if
 * it happens to be present, which is what CI runs; without it the suite still
 * passes and says it skipped.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
let failures = 0;
let checks = 0;

function ok(name, cond, detail) {
  checks++;
  if (cond) {
    console.log('  \x1b[32m✓\x1b[0m ' + name);
  } else {
    failures++;
    console.log('  \x1b[31m✗\x1b[0m ' + name + (detail ? '\n      ' + detail : ''));
  }
}

function group(name) { console.log('\n' + name); }

/* Poll a page-side predicate instead of guessing at a timeout. Every assertion
   that follows a click goes through this, so the suite is deterministic. */
async function okEventually(page, name, fn, arg, detail) {
  try {
    await page.waitForFunction(fn, arg, { timeout: 4000, polling: 60 });
    ok(name, true);
  } catch (e) {
    ok(name, false, detail || 'still false after 4s');
  }
}
function read(rel) { return fs.readFileSync(path.join(ROOT, rel), 'utf8'); }

/* ---------------------------------------------------------- static */

group('Files');
const REQUIRED = ['index.html', 'sw.js', 'manifest.webmanifest', 'netlify.toml',
  'assets/app.css', 'assets/core.js', 'assets/ui.js', 'assets/views.js',
  'assets/app.js', 'assets/data.js', 'src/build_data.py'];
REQUIRED.forEach(f => ok(f + ' exists', fs.existsSync(path.join(ROOT, f))));

group('Cache version is consistent');
const html = read('index.html');
const sw = read('sw.js');
const versions = new Set([...html.matchAll(/\?v=([0-9a-f]{8})/g)].map(m => m[1]));
ok('index.html uses a single version', versions.size === 1,
  'found: ' + [...versions].join(', '));
const version = [...versions][0];
const swVersions = new Set([...sw.matchAll(/\?v=([0-9a-f]{8})/g)].map(m => m[1]));
ok('sw.js matches index.html', swVersions.size === 1 && swVersions.has(version),
  'sw: ' + [...swVersions].join(', ') + ' vs ' + version);
ok('sw.js cache name carries the version', sw.includes("handbook-" + version));

group('Every script index.html loads exists');
[...html.matchAll(/<script src="([^"]+)"/g)].forEach(m => {
  const p = m[1].split('?')[0].replace(/^\//, '');
  ok(p, fs.existsSync(path.join(ROOT, p)));
});

group('Data file');
const dataSrc = read('assets/data.js');
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(dataSrc, sandbox);
const D = sandbox.window._DATA;
ok('data.js parses', !!D);
ok('has recipes', Array.isArray(D.recipes) && D.recipes.length > 200,
  'got ' + (D.recipes || []).length);
ok('has ingredients', Object.keys(D.ing).length > 100);
ok('has exercises', D.exercises.length > 200);
ok('has sessions', D.sessions.length > 10);
ok('every recipe has an id, name and macros', D.recipes.every(r =>
  r.id && r.n && typeof r.k === 'number' && typeof r.p === 'number'));
ok('no duplicate recipe ids',
  new Set(D.recipes.map(r => r.id)).size === D.recipes.length);
const aisleKeys = new Set(D.aisles.flatMap(a => a[1]));
const unplaced = Object.keys(D.ing).filter(k => !aisleKeys.has(k));
ok('every ingredient has an aisle', unplaced.length === 0,
  'unplaced: ' + unplaced.slice(0, 5).join(', '));
const missingIng = [];
D.recipes.forEach(r => (r.ing || []).forEach(i => {
  if (i[1] && !D.ing[i[1]]) missingIng.push(r.id + ':' + i[1]);
}));
ok('every recipe ingredient resolves', missingIng.length === 0,
  missingIng.slice(0, 5).join(', '));

group('Source hygiene');
['assets/core.js', 'assets/ui.js', 'assets/views.js', 'assets/app.js'].forEach(f => {
  const src = read(f);
  ok(f + ' parses as JavaScript', (() => {
    try { new vm.Script(src, { filename: f }); return true; } catch (e) {
      ok.detail = e.message; return false;
    }
  })());
  ok(f + ' has no leftover debugging', !/\bconsole\.log\(|\bdebugger\b/.test(src));
});
const css = read('assets/app.css');
ok('css has balanced braces',
  (css.match(/\{/g) || []).length === (css.match(/\}/g) || []).length);
ok('css defines both themes',
  css.includes(':root{') && css.includes('[data-theme="dark"]'));
ok('css respects reduced motion', css.includes('prefers-reduced-motion'));

group('Manifest');
const man = JSON.parse(read('manifest.webmanifest'));
ok('manifest has a name and icons', !!man.name && man.icons.length >= 2);
man.icons.forEach(i => ok('icon ' + i.src + ' exists',
  fs.existsSync(path.join(ROOT, i.src.replace(/^\//, '')))));

/* ---------------------------------------------------------- core logic */
/* core.js has no DOM in it, so the calculations can be tested directly rather
   than through the UI. */

function loadCore() {
  const store = {};
  const ctx = {
    localStorage: {
      getItem: k => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: k => { delete store[k]; }
    },
    addEventListener() { },
    setTimeout, clearTimeout, console,
    Math, Date, JSON, Object, Array, String, Number, isNaN, parseFloat, parseInt
  };
  ctx.window = ctx;
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(dataSrc, ctx);
  vm.runInContext(read('assets/core.js'), ctx);
  return ctx.Handbook;
}

group('Core calculations');
{
  const H = loadCore();
  const S = H.state();

  ok('a fresh state seeds the workbook costs and jobs',
    S.fin.costs.length > 0 && S.fin.jobs.length > 0);

  const c = H.calc({ sex: 'm', w: 150, h: 68, age: 20, bf: 20, act: 1.55, goal: 1.09, pf: 1.1 });
  ok('calorie target is in a sane range', c.kcal > 2000 && c.kcal < 3600, 'got ' + c.kcal);
  ok('protein target follows the multiplier', c.p === Math.round(150 * 1.1), 'got ' + c.p);
  ok('TDEE sits above resting metabolic rate', c.tdee > c.rmr);

  const t = H.dayTarget('j', 'legs');
  const rest = H.dayTarget('j', 'rest');
  ok('leg day asks for more than a rest day', t.kcal > rest.kcal && t.c > rest.c);
  ok('fat never falls below the floor', t.f >= Math.round(S.prof.j.w * 0.3) - 1);

  const r = H.byId(D.recipes[0].id);
  ok('a recipe costs something', H.cps(r) > 0);
  ok('per-serving times servings is the batch cost',
    Math.abs(H.cps(r) * r.sv - H.ctot(r)) < 0.01);

  // Editing an ingredient price has to flow through to every recipe using it.
  const key = r.ing.find(i => i[1])[1];
  const before = H.cps(r);
  S.ingOv[key] = { w: H.ING(key).w * 10, c: H.ING(key).w * 10 };
  H.bumpCosts();
  ok('editing an ingredient price recosts the recipe', H.cps(r) > before,
    before + ' -> ' + H.cps(r));
  // Blanking a store price has to mean "not sold here", not "fall back to base".
  S.ingOv[key] = { w: 99, c: null };
  H.bumpCosts();
  ok('clearing a store price drops that store', H.ING(key).c === null &&
    H.bestStore(H.ING(key)) === 'Walmart');
  delete S.ingOv[key];
  H.bumpCosts();
  ok('resetting the price restores the original cost',
    Math.abs(H.cps(r) - before) < 0.001);

  ok('the cheaper store wins', H.best({ w: 2, c: 1 }) === 1 && H.best({ w: 1, c: 2 }) === 1);
  ok('a store with no size is skipped, not treated as free',
    H.best({ w: 3, c: null }) === 3 && H.bestStore({ w: 3, c: null }) === 'Walmart');

  group('Meal planner');
  const res = H.generatePlan({ from: H.today(), days: 7, slots: 4, who: 'j', seed: 7 });
  ok('plans the number of days asked for', Object.keys(res.plan).length === 7);
  ok('every day gets the number of meals asked for',
    res.report.every((_, i) => res.plan[H.addDays(H.today(), i)].length === 4));

  const worst = Math.max(...res.report.map(d => {
    const got = H.sumMeals(res.plan[d.date]);
    return Math.abs(got.p - d.target.p) / d.target.p;
  }));
  ok('protein lands within 15% every day', worst < 0.15,
    'worst day was off by ' + Math.round(worst * 100) + '%');

  const kWorst = Math.max(...res.report.map(d => {
    const got = H.sumMeals(res.plan[d.date]);
    return Math.abs(got.kcal - d.target.kcal) / d.target.kcal;
  }));
  ok('calories land within 15% every day', kWorst < 0.15,
    'worst day was off by ' + Math.round(kWorst * 100) + '%');

  const budgeted = H.generatePlan({ from: H.today(), days: 5, slots: 4, who: 'j', budget: 7, seed: 3 });
  const avgCost = budgeted.report.reduce((a, d) => a + H.sumMeals(budgeted.plan[d.date]).cost, 0) / 5;
  ok('a budget actually pulls the cost down', avgCost < 9, 'averaged ' + avgCost.toFixed(2));

  const variety = H.generatePlan({ from: H.today(), days: 7, slots: 4, who: 'j', variety: 7, seed: 5 });
  const ids = Object.values(variety.plan).flat().map(m => m.id);
  ok('a high variety setting mostly avoids repeats',
    new Set(ids).size / ids.length > 0.8,
    new Set(ids).size + ' distinct of ' + ids.length);

  group('Shopping from a plan');
  Object.keys(res.plan).forEach(ds => { S.plan[ds] = res.plan[ds]; });
  const list = H.shoppingFromPlan(H.today(), 7, { usePantry: true });
  ok('a week of meals produces a list', list.items.length > 10, list.items.length + ' items');
  ok('every line is priced and placed in an aisle',
    list.items.every(i => i.price > 0 && i.aisle && i.grams > 0));

  const first = list.items[0];
  H.pantryAdd(first.key, first.grams * 3);
  const after = H.shoppingFromPlan(H.today(), 7, { usePantry: true });
  ok('the pantry removes what is already in the cupboard',
    !after.items.some(i => i.key === first.key) &&
    after.skipped.some(s => s.key === first.key));
  ok('ignoring the pantry brings it back',
    H.shoppingFromPlan(H.today(), 7, { usePantry: false })
      .items.some(i => i.key === first.key));

  group('Training and schedule');
  ok('every training type maps to sessions that exist', ['pull', 'push', 'legs', 'arms', 'abs', 'full']
    .every(w => H.sessionsFor(w).length > 0));
  ok('"Back" does not match "Fallback"',
    H.sessionsFor('pull').every(s => !/fallback/i.test(s.name)));
  ok('rest and cardio suggest nothing',
    H.sessionsFor('rest').length === 0 && H.sessionsFor('cardio').length === 0);

  const n = H.applySplit('ppl', H.today(), 1, 0);
  ok('a split writes a week of days', n === 7);
  ok('the split lands the right sessions',
    H.dayLog(H.today()).workout === 'push' &&
    H.dayLog(H.addDays(H.today(), 2)).workout === 'legs');

  const day = { sched: [{ who: 'Jaron', what: 'Work', from: '09:00', to: '17:00' }] };
  const free = H.freeBlocks(day, 60);
  ok('free time is found around a booked block',
    free.length > 0 && free.every(b => b[0] >= 17 * 60 || b[1] <= 9 * 60),
    JSON.stringify(free));
  ok('a fully booked day reports no overlap',
    H.freeBlocks({ sched: [{ who: 'Both', what: 'x', from: '00:00', to: '23:59' }] }, 60).length === 0);
  ok('an empty day returns null rather than a block list',
    H.freeBlocks({ sched: [] }, 60) === null);

  group('Migration');
  {
    const H2 = loadCore();
    // A v5 save: no plan, no pantry, no prefs, cost mode loose on the root.
    H2.setState({
      v: 5, who: 'a', costMode: 'cheap',
      prof: { j: { name: 'Me', sex: 'm', w: 150, h: 68, age: 20, bf: 20, act: 1.55, goal: 1.09, pf: 1.1 } },
      fav: ['B-01'], days: {}, fin: { jobs: [], shifts: [], costs: [], scenarios: {}, purchases: {} },
      shop: { active: 'Weekly shop', lists: {} }, sched: {}, ingOv: {}, lists: {}, mine: [], photos: {}
    });
    const m = H2.state();
    ok('migration adds the new state', !!m.plan && !!m.pantry && !!m.prefs);
    ok('migration keeps what was there', m.who === 'a' && m.fav[0] === 'B-01');
    ok('migration moves the loose cost mode into prefs',
      m.prefs.costMode === 'cheap' && !('costMode' in m));
    ok('migration fills in the missing profile', !!m.prof.a && m.prof.a.name === 'Aaliyah');
    ok('migration renames the placeholder profile', m.prof.j.name === 'Jaron');
    ok('migration stamps the version', m.v === 6);
  }
}

/* ---------------------------------------------------------- browser */

const ROUTES = [
  ['#/meals', 'Meals'],
  ['#/plan', 'Meal plan'],
  ['#/training', 'Training'],
  ['#/training/exercises', 'Exercise database'],
  ['#/shopping', 'Shopping'],
  ['#/shopping/ingredients', 'Ingredient list'],
  ['#/shopping/pantry', 'Pantry'],
  ['#/financial', 'Financial'],
  ['#/financial/actual', 'Actual earnings'],
  ['#/financial/purchases', 'Big purchases'],
  ['#/schedule', 'Schedule'],
  ['#/schedule/week', 'Weekly template'],
  ['#/settings', 'Profile and settings'],
  ['#/r/' + D.recipes[0].id, D.recipes[0].n]
];

function serve() {
  const types = {
    '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
    '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
    '.webmanifest': 'application/manifest+json'
  };
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (p === '/') p = '/index.html';
    const file = path.join(ROOT, p);
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404); res.end('not found'); return;
    }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'text/plain' });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise(r => server.listen(0, () => r(server)));
}

async function browserTests() {
  let chromium;
  try {
    chromium = require('playwright').chromium;
  } catch (e) {
    group('Browser');
    console.log('  \x1b[33m—\x1b[0m Playwright not installed, skipping the browser pass');
    return;
  }

  group('Browser');
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port;
  // The image pins a Chromium build that may not match the Playwright version's
  // expected revision, so prefer the one that is actually installed.
  const pinned = '/opt/pw-browsers/chromium';
  const launchOpts = fs.existsSync(pinned) ? { executablePath: pinned } : {};
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage();

  // The sandbox has no outbound network, and the webfont stylesheet is the only
  // external request. Stub it so a connection reset is not reported as an app error.
  await page.route('**://fonts.googleapis.com/**', r =>
    r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  await page.route('**://fonts.gstatic.com/**', r => r.abort());

  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

  try {
    await page.goto(base + '/', { waitUntil: 'networkidle' });
    ok('app boots with no page errors', errors.length === 0, errors.slice(0, 3).join('\n      '));

    for (const [hash, expect] of ROUTES) {
      errors.length = 0;
      await page.evaluate(h => { location.hash = h; }, hash);
      let text = '';
      try {
        // View transitions defer the swap by a frame or two, so wait for the
        // content rather than guessing at a timeout.
        await page.waitForFunction(
          e => document.querySelector('#view').innerText.includes(e), expect,
          { timeout: 4000 });
        text = await page.locator('#view').innerText();
      } catch (e) {
        text = await page.locator('#view').innerText();
      }
      ok('route ' + hash + ' renders "' + expect + '"',
        text.includes(expect) && errors.length === 0,
        errors.slice(0, 2).join(' | ') || text.slice(0, 80));
    }

    // The interactions most likely to break: they all write state.
    errors.length = 0;
    await page.evaluate(h => { location.hash = h; }, '#/plan');
    await page.waitForTimeout(150);
    await page.click('#pGen');
    await page.waitForTimeout(900);
    await okEventually(page, 'generating a plan fills days',
      () => Object.keys(window.Handbook.state().plan).length >= 7);
    ok('the plan hits the protein target within 15%', await page.evaluate(() => {
      const H = window.Handbook;
      const days = Object.keys(H.state().plan).slice(0, 7);
      let got = 0, want = 0;
      days.forEach(ds => {
        got += H.sumMeals(H.state().plan[ds]).p;
        const w = (H.state().days[ds] || {}).workout || 'rest';
        want += H.dayTarget(H.state().who, w).p;
      });
      return want > 0 && Math.abs(got - want) / want < 0.15;
    }));

    await page.click('#pShop');
    await page.waitForTimeout(200);
    await page.click('#blGo');
    await okEventually(page, 'the plan builds a shopping list',
      () => window.Handbook.curList().items.length > 5);

    // Ticking an item must not scroll the page.
    const box = page.locator('[data-gt]').first();
    if (await box.count()) {
      await page.evaluate(() => window.scrollTo({ top: 400, behavior: 'instant' }));
      await page.waitForFunction(() => Math.abs(window.scrollY - 400) < 5, null,
        { timeout: 3000 }).catch(() => { });
      const before = await page.evaluate(() => window.scrollY);
      await box.check();
      await page.waitForFunction(() => !!document.querySelector('.gitem.done'), null,
        { timeout: 3000 }).catch(() => { });
      const after = await page.evaluate(() => window.scrollY);
      ok('checking a shopping item keeps the scroll position',
        Math.abs(after - before) < 40, before + ' -> ' + after);
    }

    errors.length = 0;
    await page.keyboard.press('Escape');
    await page.evaluate(() => window.Handbook.openPalette());
    await page.waitForTimeout(150);
    await page.fill('#cmdq', 'oat');
    await okEventually(page, 'the command palette finds things',
      () => document.querySelectorAll('.cmdrow').length > 0);
    await page.keyboard.press('Escape');

    await page.evaluate(() => {
      window.Handbook.state().theme = 'dark';
      window.Handbook.applyTheme();
    });
    await okEventually(page, 'dark theme applies',
      () => document.documentElement.getAttribute('data-theme') === 'dark');
    // body has a colour transition, so poll past it rather than sampling mid-fade.
    await okEventually(page, 'dark theme actually repaints the page',
      () => getComputedStyle(document.body).backgroundColor !== 'rgb(251, 250, 247)');

    // A saved file must survive a round trip.
    const roundTrip = await page.evaluate(() => {
      const H = window.Handbook;
      // savedAt is a write timestamp, so it legitimately changes on load.
      const strip = s => { const o = JSON.parse(s); delete o.savedAt; return JSON.stringify(o); };
      const before = JSON.stringify(H.exportBlob().state);
      H.importState(before);
      return strip(JSON.stringify(H.state())) === strip(before);
    });
    ok('export then import is lossless', roundTrip);

    // Every dialog in the app, opened and driven. These are the paths a route
    // walk does not touch, and the ones most likely to throw on a rename.
    group('Dialogs');
    async function dialog(name, open, drive) {
      errors.length = 0;
      try {
        await open();
        await page.waitForSelector('.mask', { timeout: 3000 });
        if (drive) await drive();
        await page.waitForTimeout(220);
        // Anything still open gets dismissed so the next case starts clean.
        while (await page.locator('.mask').count()) {
          await page.keyboard.press('Escape');
          await page.waitForTimeout(120);
        }
        ok(name, errors.length === 0, errors.slice(0, 2).join(' | '));
      } catch (e) {
        ok(name, false, e.message.split('\n')[0]);
        while (await page.locator('.mask').count()) {
          await page.keyboard.press('Escape');
          await page.waitForTimeout(120);
        }
      }
    }
    const goto = async h => {
      await page.evaluate(x => { location.hash = x; }, h);
      await page.waitForTimeout(320);
    };

    await goto('#/settings');
    await dialog('profile editor opens and saves',
      () => page.click('[data-prof="j"]'),
      async () => {
        await page.fill('#pfW', '158');
        await page.waitForTimeout(120);
        const preview = await page.locator('#pfPreview').innerText();
        ok('  profile editor previews the new targets', /Kcal/i.test(preview));
        await page.click('#pfSave');
      });
    await okEventually(page, 'saving the profile persisted the weight',
      () => window.Handbook.state().prof.j.w === 158);

    await goto('#/training');
    await dialog('split generator opens and writes the calendar',
      () => page.click('#splitBtn'),
      () => page.click('#spGo'));
    await okEventually(page, 'the split reached the calendar',
      () => window.Handbook.dayLog(window.Handbook.today()).workout !== 'rest');

    await dialog('session detail opens', () => page.click('[data-sess]'));

    await goto('#/shopping/ingredients');
    await dialog('ingredient editor opens and saves',
      () => page.click('[data-ie]'),
      () => page.click('#ieSave'));
    await dialog('new ingredient needs a name',
      () => page.click('#ingNew'),
      async () => {
        await page.click('#ieSave');
        ok('  it refuses to save a nameless ingredient',
          await page.locator('.mask').count() === 1);
        await page.fill('#ieN', 'Test ingredient');
        await page.click('#ieSave');
      });

    await goto('#/shopping/pantry');
    await dialog('pantry add opens the ingredient picker', () => page.click('#panAdd'));

    await goto('#/shopping');
    await dialog('shopping item editor opens',
      () => page.click('[data-ge]'),
      () => page.click('#seSave'));
    await dialog('recipe picker opens', () => page.click('#gRecipe'));
    await dialog('new list asks for a name', () => page.click('#newList'));

    await goto('#/financial');
    await dialog('job editor opens and saves', () => page.click('#jobAdd'), () => page.click('#jSave'));
    await dialog('cost editor opens and saves', () => page.click('#costAdd'), () => page.click('#cSave'));
    await dialog('edit an existing income line', () => page.click('[data-jobe]'));
    await dialog('edit an existing cost line', () => page.click('[data-coste]'));
    await dialog('scenario save asks for a name', () => page.click('#scenSave'));

    await goto('#/financial/actual');
    await dialog('shift editor opens and saves', () => page.click('#shAdd'), () => page.click('#sSave'));
    await okEventually(page, 'the shift was logged',
      () => window.Handbook.state().fin.shifts.length > 0);

    await goto('#/financial/purchases');
    await dialog('new comparison list asks for a name', () => page.click('#bpNew'));

    await goto('#/schedule');
    await dialog('event editor opens and saves', () => page.click('#evAdd'), () => page.click('#eSave'));
    await dialog('spend editor opens and saves', () => page.click('#spAdd'), () => page.click('#spSave'));
    await dialog('meal picker opens', () => page.click('#mealAdd'));
    await okEventually(page, 'the event reached the day', () => {
      const H = window.Handbook;
      return H.dayLog(H.calSel).sched.length > 0 && H.dayLog(H.calSel).spend.length > 0;
    });

    await goto('#/schedule/week');
    await dialog('weekly template editor opens and saves',
      () => page.click('[data-tadd="1"]'), () => page.click('#tSave2'));

    await goto('#/meals');
    await dialog('own recipe needs a name',
      () => page.click('#addOwn'),
      async () => {
        await page.fill('#on', 'Test recipe');
        await page.fill('#ok', '400');
        await page.fill('#op', '30');
        await page.click('#oSave');
      });
    await okEventually(page, 'the custom recipe is now in the catalogue',
      () => window.Handbook.all().some(r => r.n === 'Test recipe'));

    await goto('#/r/B-01');
    await dialog('recipe list picker opens', () => page.click('[data-tolist]'), () => page.click('#lS'));
    await dialog('put-on-a-day picker opens', () => page.click('[data-plan]'));

    group('Offline and motion');
    await page.context().setOffline(true);
    await page.evaluate(() => window.dispatchEvent(new Event('offline')));
    await okEventually(page, 'going offline says so without breaking anything',
      () => !!document.querySelector('.banner'));
    await page.context().setOffline(false);
    await page.evaluate(() => window.dispatchEvent(new Event('online')));
    await okEventually(page, 'coming back online clears the note',
      () => !document.querySelector('.banner'));

    await goto('#/meals');
    ok('progress bars are rendered for animation, not painted full',
      await page.evaluate(() => {
        const b = document.querySelector('.bar i[data-w]');
        return !!b && b.getAttribute('data-w') !== null;
      }));
    await okEventually(page, 'and then actually get their width',
      () => {
        const b = document.querySelector('.bar i[data-w]');
        return !!b && b.style.width !== '';
      });

    group('Accessibility');
    await goto('#/meals');
    ok('recipe cards are reachable from the keyboard',
      await page.evaluate(() => {
        const c = document.querySelector('.rc');
        return c && c.getAttribute('tabindex') === '0' && !!c.getAttribute('aria-label');
      }));
    ok('the active tab is marked for screen readers',
      await page.locator('.tab[aria-current="page"]').count() === 1);
    await page.evaluate(() => window.Handbook.openPalette());
    await page.waitForTimeout(200);
    ok('a dialog announces itself as one',
      await page.locator('.mask[role="dialog"][aria-modal="true"]').count() === 1);
    ok('focus lands inside the dialog',
      await page.evaluate(() => !!document.activeElement.closest('.mask')));
    await page.keyboard.press('Escape');
    await page.waitForTimeout(200);
    ok('Escape closes it', await page.locator('.mask').count() === 0);
    ok('toasts sit below the dialog layer, so they cannot cover its buttons',
      await page.evaluate(() => {
        const z = n => parseInt(getComputedStyle(n).zIndex, 10) || 0;
        const probe = document.createElement('div');
        probe.className = 'mask';
        document.body.appendChild(probe);
        const result = z(document.querySelector('#toasts')) < z(probe);
        probe.remove();
        return result;
      }));
    ok('focus returns to the page behind it',
      await page.evaluate(() => !document.activeElement.closest || !document.activeElement.closest('.mask')));

    ok('no errors from any of that', errors.length === 0, errors.slice(0, 3).join('\n      '));
  } finally {
    await browser.close();
    server.close();
  }
}

browserTests()
  .catch(e => { failures++; console.log('\n\x1b[31mBrowser pass threw:\x1b[0m ' + e.message); })
  .then(() => {
    console.log('\n' + (failures
      ? '\x1b[31m' + failures + ' of ' + checks + ' checks failed\x1b[0m'
      : '\x1b[32mall ' + checks + ' checks passed\x1b[0m'));
    process.exit(failures ? 1 : 0);
  });
