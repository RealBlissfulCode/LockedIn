/* ============================================================
   The Handbook - core

   State, storage, and every calculation the app does. No DOM
   in this file: views.js renders it, ui.js decorates it, app.js
   wires it. Everything hangs off the single global H so the
   four files can be loaded as plain scripts with no build step.
   ============================================================ */
(function (global) {
  'use strict';

  var H = global.Handbook = global.Handbook || {};
  var _D = global._DATA;

  /* ---------------------------------------------------------- data */
  var R = _D.recipes;
  var BASEING = _D.ing;
  var AISLES = _D.aisles;
  var EX = _D.exercises;
  var SESS = _D.sessions;
  var SEEDCOST = _D.costs;
  var SEEDJOB = _D.jobs;

  H.AISLES = AISLES; H.EX = EX; H.SESS = SESS;

  var KEY = 'handbook.v6';
  var OLDKEY = 'handbook.v5';

  /* ---------------------------------------------------------- state */
  function DEF() {
    return {
      v: 6,
      who: 'j',
      theme: 'auto',
      savedAt: null,
      lastExport: null,
      prof: {
        j: { name: 'Jaron', sex: 'm', w: 150, h: 68, age: 20, bf: 20, act: 1.55, goal: 1.09, pf: 1.1 },
        a: { name: 'Aaliyah', sex: 'f', w: 120, h: 66.5, age: 20, bf: 24, act: 1.45, goal: 1.0, pf: 0.8 }
      },
      ingOv: {},
      fav: [],
      lists: {},
      mine: [],
      photos: {},
      pantry: {},
      shop: { active: 'Weekly shop', lists: { 'Weekly shop': { cat: 'Groceries', fav: true, items: [] } } },
      plan: {},
      days: {},
      fin: { jobs: [], shifts: [], costs: [], scenarios: {}, purchases: {}, costMode: 'real', path: 'rent' },
      sched: { tmpl: {} },
      prefs: {
        costMode: 'all', dayBudget: null, remindBackup: true, planSlots: 4,
        hideChecked: false, closedAisles: [], calView: null
      },
      seeded: false
    };
  }
  H.DEF = DEF;

  /* Deep-fills anything a newer version added, so an old save keeps working. */
  function migrate(o) {
    var d = DEF();
    if (!o || typeof o !== 'object') return d;
    var k;
    // v5 kept the cost mode loose on the root; read it before the defaults land.
    var legacyCostMode = (!o.prefs || !o.prefs.costMode) ? o.costMode : null;
    for (k in d) if (!(k in o)) o[k] = d[k];
    for (k in d.prof) if (!o.prof[k]) o.prof[k] = d.prof[k];
    for (k in d.fin) if (!(k in o.fin)) o.fin[k] = d.fin[k];
    for (k in d.prefs) if (!(k in o.prefs)) o.prefs[k] = d.prefs[k];
    if (!o.sched.tmpl) o.sched.tmpl = {};
    if (!Array.isArray(o.prefs.closedAisles)) o.prefs.closedAisles = [];
    if (legacyCostMode) o.prefs.costMode = legacyCostMode;
    delete o.costMode;
    if (o.prof.j && o.prof.j.name === 'Me') o.prof.j.name = 'Jaron';
    o.v = 6;
    return o;
  }

  var S = (function () {
    var raw = null;
    try { raw = localStorage.getItem(KEY) || localStorage.getItem(OLDKEY); } catch (e) { }
    if (raw) { try { return migrate(JSON.parse(raw)); } catch (e) { } }
    return DEF();
  })();
  H.state = function () { return S; };

  /* Loading a save replaces the contents of S in place rather than rebinding it,
     so every module that closed over the object keeps pointing at live state. */
  H.setState = function (next) {
    var fresh = migrate(next), k;
    for (k in S) if (Object.prototype.hasOwnProperty.call(S, k)) delete S[k];
    for (k in fresh) if (Object.prototype.hasOwnProperty.call(fresh, k)) S[k] = fresh[k];
    return S;
  };

  var saveTimer = null;
  var onSaveFail = null;
  H.onSaveFail = function (fn) { onSaveFail = fn; };

  function writeNow() {
    S.savedAt = Date.now();
    try {
      localStorage.setItem(KEY, JSON.stringify(S));
      return true;
    } catch (e) {
      if (onSaveFail) onSaveFail(e);
      return false;
    }
  }

  /* Writes are coalesced: dragging a slider or typing in a field should not
     serialise the whole state on every keystroke. Anything that must survive a
     tab close right now calls save(true). */
  function save(immediate) {
    if (immediate) {
      if (saveTimer) { clearTimeout(saveTimer); saveTimer = null; }
      return writeNow();
    }
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { saveTimer = null; writeNow(); }, 180);
    return true;
  }
  H.save = save;

  if (global.addEventListener) {
    global.addEventListener('pagehide', function () { if (saveTimer) save(true); });
    global.addEventListener('visibilitychange', function () {
      if (global.document && global.document.visibilityState === 'hidden' && saveTimer) save(true);
    });
  }

  /* Seed the financial side from the Moving In workbook, once. */
  if (!S.seeded) {
    S.fin.costs = SEEDCOST.map(function (c, i) {
      return {
        id: 'c' + i, name: c.name, section: c.section, who: c.who,
        low: c.low, real: c.real, high: c.high, actual: c.exact || null
      };
    });
    S.fin.jobs = SEEDJOB.map(function (j, i) {
      return {
        id: 'j' + i, who: j.who, name: j.name, employer: j.employer,
        title: j.title, rate: null, low: j.low, real: j.real, high: j.high
      };
    });
    S.seeded = true;
    save(true);
  }

  /* ---------------------------------------------------------- helpers */
  function E(t) {
    return String(t == null ? '' : t).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function money(v) {
    var n = Number(v) || 0;
    return (n < 0 ? '-$' : '$') + Math.abs(n).toLocaleString(undefined,
      { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function money0(v) {
    var n = Math.round(Number(v) || 0);
    return (n < 0 ? '-$' : '$') + Math.abs(n).toLocaleString();
  }
  function p2(n) { n = String(n); return n.length < 2 ? '0' + n : n; }
  function dstr(d) { return d.getFullYear() + '-' + p2(d.getMonth() + 1) + '-' + p2(d.getDate()); }
  function today() { return dstr(new Date()); }
  function dOf(ds) { var p = String(ds).split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(ds, n) { var d = dOf(ds); d.setDate(d.getDate() + n); return dstr(d); }
  function pretty(ds) {
    return dOf(ds).toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
  }
  function shortD(ds) {
    return dOf(ds).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }
  function uid() { return Math.random().toString(36).slice(2, 9) + Date.now().toString(36).slice(-3); }
  function num(x, d) { var n = parseFloat(x); return isNaN(n) ? (d || 0) : n; }
  function clamp(n, lo, hi) { return n < lo ? lo : n > hi ? hi : n; }
  function csvEsc(v) { return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"'; }
  function toCSV(rows) { return rows.map(function (r) { return r.map(csvEsc).join(','); }).join('\n'); }

  H.E = E; H.money = money; H.money0 = money0; H.p2 = p2; H.dstr = dstr;
  H.today = today; H.dOf = dOf; H.addDays = addDays; H.pretty = pretty; H.shortD = shortD;
  H.uid = uid; H.num = num; H.toCSV = toCSV;

  /* ---------------------------------------------------------- people */
  /* Records seeded from the workbook store a person's name as a literal string.
     Profiles own the display name, so everything renders through here and a
     rename in the profile editor flows through the whole app. */
  var PKEY = { Jaron: 'j', Aaliyah: 'a' };
  function personKey(label) { return PKEY[label] || null; }
  function nameOf(label) {
    if (label === 'Both') return 'Both';
    var k = personKey(label);
    return k ? S.prof[k].name : label;
  }
  function label(k) { return k === 'a' ? 'Aaliyah' : 'Jaron'; }
  function P() { return S.prof[S.who]; }
  function otherKey() { return S.who === 'j' ? 'a' : 'j'; }

  H.nameOf = nameOf; H.label = label; H.P = P; H.otherKey = otherKey;

  /* ---------------------------------------------------------- ingredients */
  /* Prices are the one field where an explicit null is meaningful: it says the
     store does not stock a sensible size. Every other field falls back to the
     base value when the override is blank. */
  var NULLABLE = { w: 1, c: 1 };

  function ING(k) {
    var b = BASEING[k], o = S.ingOv[k];
    if (!b && !o) return null;
    var m = {}, x, y;
    if (b) for (x in b) m[x] = b[x];
    if (o) {
      for (y in o) {
        if (NULLABLE[y] && Object.prototype.hasOwnProperty.call(o, y)) { m[y] = o[y]; continue; }
        if (o[y] !== null && o[y] !== undefined && o[y] !== '') m[y] = o[y];
      }
    }
    return m;
  }
  function allIngKeys() {
    var s = {}, k, j;
    for (k in BASEING) s[k] = 1;
    for (j in S.ingOv) s[j] = 1;
    return Object.keys(s).filter(function (key) {
      return !S.ingOv[key] || !S.ingOv[key].deleted;
    });
  }
  /* The cheaper of the two stores wins, and a store with no sensible size is
     simply skipped rather than counted as free. */
  function best(q) {
    if (!q) return 0;
    var w = q.w, c = q.c;
    if (c != null && c > 0 && (w == null || w <= 0 || c < w)) return c;
    return w || 0;
  }
  function bestStore(q) {
    if (!q) return '';
    var w = q.w, c = q.c;
    if (c != null && c > 0 && (w == null || w <= 0 || c < w)) return 'Costco';
    return 'Walmart';
  }
  H.ING = ING; H.allIngKeys = allIngKeys; H.best = best; H.bestStore = bestStore;

  /* Recipe cost is always recomputed from live ingredient prices, so editing one
     price flows straight through to every recipe that uses it. Memoised per
     render pass because the meal planner asks for it thousands of times. */
  var costCache = {}, costEpoch = 0;
  function bumpCosts() { costCache = {}; costEpoch++; }
  H.bumpCosts = bumpCosts;

  function rcost(r) {
    var hit = costCache[r.id];
    if (hit) return hit;
    var t = 0, any = false;
    (r.ing || []).forEach(function (i) {
      var q = ING(i[1]);
      if (!q) return;
      var p = best(q);
      if (p > 0) { any = true; t += (i[2] || 0) / 100 * p; }
    });
    var out = any
      ? { tot: t, per: t / Math.max(r.sv || 1, 1) }
      : { tot: r.cw || 0, per: r.cws || 0 };
    costCache[r.id] = out;
    return out;
  }
  function cps(r) { return rcost(r).per; }
  function ctot(r) { return rcost(r).tot; }
  H.cps = cps; H.ctot = ctot;

  var allCache = null;
  function all() {
    if (!allCache) allCache = R.concat(S.mine);
    return allCache;
  }
  function invalidate() { allCache = null; bumpCosts(); byIdCache = null; }
  H.all = all; H.invalidate = invalidate;

  var byIdCache = null;
  function byId(id) {
    if (!byIdCache) {
      byIdCache = {};
      all().forEach(function (r) { byIdCache[r.id] = r; });
    }
    return byIdCache[id] || null;
  }
  H.byId = byId;

  function ingUsage(k) {
    var n = 0;
    all().forEach(function (r) {
      (r.ing || []).forEach(function (i) { if (i[1] === k) n++; });
    });
    return n;
  }
  H.ingUsage = ingUsage;

  /* ---------------------------------------------------------- nutrition */
  function calc(p) {
    var kg = p.w * 0.45359237, cm = p.h * 2.54, m = cm / 100;
    var lbm = kg * (1 - p.bf / 100);
    var rmr = (10 * kg) + (6.25 * cm) - (5 * p.age) + (p.sex === 'f' ? -161 : 5);
    var tdee = rmr * p.act, kcal = tdee * p.goal;
    var prot = p.w * p.pf, fat = kcal * 0.25 / 9, carb = (kcal - prot * 4 - fat * 9) / 4;
    return {
      rmr: Math.round(rmr), katch: Math.round(370 + 21.6 * lbm), tdee: Math.round(tdee),
      kcal: Math.round(kcal), p: Math.round(prot), c: Math.round(carb), f: Math.round(fat),
      fib: Math.round(kcal / 1000 * 14), w: Math.round(p.w * 0.6 + 35),
      lbm: Math.round(p.w * (1 - p.bf / 100)),
      ffmi: (lbm / (m * m) + 6.1 * (1.8 - m)).toFixed(1),
      rate: (kcal - tdee) * 7 / 3500
    };
  }
  H.calc = calc;

  var TRAIN = {
    rest: { n: 'Rest day', k: 0.94, c: 0.80, p: 1.00, why: 'Repair happens on rest days, so protein holds. Carbs ease back, fiber and micronutrients come up.' },
    pull: { n: 'Back and biceps', k: 1.02, c: 1.05, p: 1.08, why: 'Biggest upper-body group. Protein and leucine lead, and iron-rich meals get weighted up.' },
    push: { n: 'Chest, shoulders, triceps', k: 1.02, c: 1.02, p: 1.08, why: 'Straight hypertrophy demand. Leucine per feeding matters most.' },
    legs: { n: 'Legs', k: 1.10, c: 1.30, p: 1.04, why: 'Legs empty the most glycogen of any session. Carbs and total calories lead.' },
    arms: { n: 'Arms', k: 0.99, c: 0.95, p: 1.05, why: 'Small group, small systemic cost. Protein holds, calories do not spike.' },
    abs: { n: 'Abs and core', k: 0.96, c: 0.88, p: 1.02, why: 'Low energy cost. Food volume and fiber over calories.' },
    cardio: { n: 'Cardio', k: 1.06, c: 1.25, p: 0.98, why: 'Carbs and fluid lead. Sodium matters more in dry Colorado air.' },
    skill: { n: 'Skill work', k: 1.01, c: 1.10, p: 1.04, why: 'Loads connective tissue more than muscle. Omega-3 and nutrient density weighted up.' },
    full: { n: 'Full body', k: 1.06, c: 1.15, p: 1.08, why: 'Everything trained, everything demanded.' }
  };
  H.TRAIN = TRAIN;

  function dayLog(ds) {
    if (!S.days[ds]) {
      S.days[ds] = { workout: 'rest', meals: [], notes: '', w: null, sched: [], spend: [] };
    }
    var d = S.days[ds];
    if (!d.sched) d.sched = [];
    if (!d.spend) d.spend = [];
    if (!d.meals) d.meals = [];
    return d;
  }
  H.dayLog = dayLog;

  function dayTarget(who, tt) {
    var b = calc(S.prof[who]), t = TRAIN[tt] || TRAIN.rest;
    var kcal = Math.round(b.kcal * t.k);
    var pr = Math.round(b.p * t.p);
    var cb = Math.round(b.c * t.c);
    var ft = Math.round((kcal - pr * 4 - cb * 4) / 9);
    var floor = Math.round(S.prof[who].w * 0.3);
    if (ft < floor) { ft = floor; cb = Math.round((kcal - pr * 4 - ft * 9) / 4); }
    return {
      kcal: kcal, p: pr, c: cb, f: ft,
      fib: Math.round(kcal / 1000 * 14), w: b.w, tr: t, base: b
    };
  }
  H.dayTarget = dayTarget;

  function sumMeals(list) {
    var o = { kcal: 0, p: 0, c: 0, f: 0, fib: 0, cost: 0, n: 0 };
    (list || []).forEach(function (m) {
      var r = byId(m.id);
      if (!r) return;
      var q = m.q || 1;
      o.kcal += r.k * q; o.p += r.p * q; o.c += r.c * q;
      o.f += r.f * q; o.fib += (r.fib || 0) * q; o.cost += cps(r) * q; o.n++;
    });
    return o;
  }
  H.sumMeals = sumMeals;
  function eaten(ds) { return sumMeals(dayLog(ds).meals); }
  H.eaten = eaten;

  function avgCost() {
    var A = all();
    if (!A.length) return 0;
    return A.reduce(function (a, r) { return a + cps(r); }, 0) / A.length;
  }
  H.avgCost = avgCost;

  /* What a day of these targets actually costs, priced off real recipes rather
     than a guess. Four bases, because "cheapest per calorie" and "what we
     actually ate" answer very different questions. */
  function estDayCost(t, mode) {
    var A = all().filter(function (r) { return r.k > 60; });
    if (mode === 'fav' && S.fav.length) {
      var f = S.fav.map(byId).filter(Boolean);
      if (f.length) A = f;
    }
    if (mode === 'cheap') {
      A = A.slice().sort(function (a, b) { return (cps(a) / a.k) - (cps(b) / b.k); }).slice(0, 40);
    }
    if (mode === 'logged') {
      var days = Object.keys(S.days).filter(function (d) { return S.days[d].meals.length; });
      if (days.length) {
        var c = 0, k = 0;
        days.forEach(function (d) { var e = eaten(d); c += e.cost; k += e.kcal; });
        if (k > 0) {
          return { byKcal: t.kcal * (c / k), byProt: null, src: days.length + ' logged days' };
        }
      }
    }
    if (!A.length) A = all();
    var pk = 0, n = 0, pp = 0, np = 0;
    A.forEach(function (r) {
      var c2 = cps(r);
      if (c2 <= 0) return;
      pk += c2 / r.k; n++;
      if (r.p > 3) { pp += c2 / r.p; np++; }
    });
    return {
      byKcal: t.kcal * (pk / Math.max(n, 1)),
      byProt: np ? t.p * (pp / np) : null,
      src: mode === 'fav' ? 'favourites'
        : mode === 'cheap' ? 'the 40 cheapest per calorie'
          : 'the average of ' + n + ' priced recipes'
    };
  }
  H.estDayCost = estDayCost;

  /* ---------------------------------------------------------- ranking */
  function bestFor(r) {
    if (r.tg.indexOf('LEUCINE PRIORITY') >= 0 || r.p >= 40) return 'Protein';
    if (r.tg.indexOf('CHEAT MEAL') >= 0) return 'Cheat';
    if (r.tg.indexOf('HEALTHY DESSERT') >= 0 || r.tg.indexOf('CHEAT DESSERT') >= 0) return 'Dessert';
    if (r.c >= 70) return 'Carbs';
    if (r.tg.indexOf('HIGH FIBER') >= 0) return 'Fiber';
    if (r.k <= 350) return 'Lean';
    if (r.k >= 600) return 'Calories';
    return 'Balanced';
  }
  H.bestFor = bestFor;

  function rank(left, tr) {
    var t = TRAIN[tr] || TRAIN.rest;
    return all().map(function (r) {
      var s = 0;
      s -= Math.abs(r.k - left.k) / 26;
      s += Math.min(r.p, left.p * 1.4) * 1.9 * t.p;
      s += Math.min(r.c, 140) * 0.15 * t.c;
      s += (r.leu || 0) * 7;
      if (S.fav.indexOf(r.id) >= 0) s += 14;
      return { r: r, s: s };
    }).sort(function (a, b) { return b.s - a.s; })
      .map(function (o) { return o.r; });
  }
  H.rank = rank;

  /* ============================================================
     Meal plan generator

     Fills a run of days with real recipes so the totals land on the
     macro targets without blowing a per-day budget. Greedy fill by
     slot, then a few improvement passes that swap one slot at a time
     for whichever candidate lowers the error most. Deterministic for
     a given seed so "generate" twice on the same inputs is stable.
     ============================================================ */

  var SLOTS = [
    { key: 'breakfast', label: 'Breakfast', cats: ['Breakfast'], share: 0.24 },
    { key: 'lunch', label: 'Lunch', cats: ['Lunch/Dinner', 'SDA Meat/Fish'], share: 0.30 },
    { key: 'dinner', label: 'Dinner', cats: ['Lunch/Dinner', 'SDA Meat/Fish'], share: 0.32 },
    { key: 'snack', label: 'Snack', cats: ['Snack', 'Drink'], share: 0.14 }
  ];

  function mulberry(seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* How badly one candidate set of meals misses a day's targets.
     Protein is weighted hardest because it is the macro that actually
     drives the training outcome; calories second; cost is a soft
     penalty that only bites past the budget. */
  function dayError(sum, target, budget) {
    var e = 0;
    e += Math.abs(sum.kcal - target.kcal) / Math.max(target.kcal, 1) * 100;
    e += Math.abs(sum.p - target.p) / Math.max(target.p, 1) * 165;
    e += Math.abs(sum.c - target.c) / Math.max(target.c, 1) * 42;
    e += Math.abs(sum.f - target.f) / Math.max(target.f, 1) * 30;
    if (sum.fib < target.fib) e += (target.fib - sum.fib) / Math.max(target.fib, 1) * 22;
    if (budget && sum.cost > budget) e += (sum.cost - budget) / budget * 120;
    return e;
  }

  function poolFor(opts) {
    var pool = all().filter(function (r) {
      if (!r.k || r.k < 40) return false;
      if (opts.favOnly && S.fav.indexOf(r.id) < 0) return false;
      if (opts.maxMinutes && r.t > opts.maxMinutes) return false;
      if (opts.noCook && r.tg.indexOf('NO-COOK') < 0) return false;
      if (opts.vegetarian && r.tg.indexOf('VEGETARIAN') < 0) return false;
      if (opts.exclude && opts.exclude.indexOf(r.id) >= 0) return false;
      return true;
    });
    return pool.length >= 8 ? pool : all().filter(function (r) { return r.k >= 40; });
  }

  function inSlot(pool, slot) {
    var hit = pool.filter(function (r) { return slot.cats.indexOf(r.cat) >= 0; });
    return hit.length ? hit : pool;
  }

  /* opts: {from, days, who, slots, budget, favOnly, maxMinutes, noCook,
            vegetarian, variety, seed} */
  function generatePlan(opts) {
    opts = opts || {};
    var from = opts.from || today();
    var days = clamp(opts.days || 7, 1, 28);
    var who = opts.who || S.who;
    var slotCount = clamp(opts.slots || 4, 2, 4);
    var slots = SLOTS.slice(0, slotCount);
    // Re-weight the shares so a 3-slot day still adds up to the whole target.
    var shareSum = slots.reduce(function (a, s) { return a + s.share; }, 0);
    var budget = opts.budget || null;
    var variety = opts.variety == null ? 3 : opts.variety;
    var rnd = mulberry(opts.seed || 1);
    var pool = poolFor(opts);
    var bySlot = slots.map(function (s) { return inSlot(pool, s); });

    var recent = {};          // recipe id -> most recent day index used
    var out = {};
    var report = [];

    function penalty(r, dayIdx) {
      var last = recent[r.id];
      if (last == null) return 0;
      var gap = dayIdx - last;
      return gap >= variety ? 0 : (variety - gap) * 55;
    }

    for (var di = 0; di < days; di++) {
      var ds = addDays(from, di);
      var workout = (S.days[ds] && S.days[ds].workout) || 'rest';
      var target = dayTarget(who, workout);
      var chosen = [];

      // Greedy first pass: fill each slot against its share of the day.
      for (var si = 0; si < slots.length; si++) {
        var slot = slots[si];
        var want = slot.share / shareSum;
        var sub = {
          kcal: target.kcal * want, p: target.p * want,
          c: target.c * want, f: target.f * want,
          fib: target.fib * want
        };
        var cands = bySlot[si];
        var bestR = null, bestS = Infinity;
        // Sample rather than scanning 251 recipes per slot per day; the
        // improvement passes below clean up anything the sample missed.
        var tries = Math.min(cands.length, 70);
        for (var t = 0; t < tries; t++) {
          var r = cands[(Math.floor(rnd() * cands.length) + t) % cands.length];
          if (chosen.some(function (m) { return m.id === r.id; })) continue;
          var s = dayError(
            { kcal: r.k, p: r.p, c: r.c, f: r.f, fib: r.fib || 0, cost: cps(r) },
            { kcal: sub.kcal, p: sub.p, c: sub.c, f: sub.f, fib: sub.fib },
            budget ? budget * want : null
          ) + penalty(r, di);
          if (s < bestS) { bestS = s; bestR = r; }
        }
        if (bestR) chosen.push({ id: bestR.id, q: 1, slot: slot.key });
      }

      // Improvement passes: swap one slot at a time for whatever lowers the
      // whole-day error most. Three passes is enough to converge in practice.
      for (var pass = 0; pass < 3; pass++) {
        var improved = false;
        for (var ci = 0; ci < chosen.length; ci++) {
          var cur = sumMeals(chosen);
          var curErr = dayError(cur, target, budget);
          var cands2 = bySlot[Math.min(ci, bySlot.length - 1)];
          var swapBest = null, swapErr = curErr;
          var scan = Math.min(cands2.length, 90);
          for (var k2 = 0; k2 < scan; k2++) {
            var cand = cands2[(k2 * 7 + di * 3 + pass) % cands2.length];
            if (cand.id === chosen[ci].id) continue;
            if (chosen.some(function (m, mi) { return mi !== ci && m.id === cand.id; })) continue;
            var trial = chosen.slice();
            trial[ci] = { id: cand.id, q: 1, slot: chosen[ci].slot };
            var err = dayError(sumMeals(trial), target, budget) + penalty(cand, di);
            if (err < swapErr - 0.4) { swapErr = err; swapBest = cand; }
          }
          if (swapBest) {
            chosen[ci] = { id: swapBest.id, q: 1, slot: chosen[ci].slot };
            improved = true;
          }
        }
        if (!improved) break;
      }

      // Portion nudge: if the day is still low on calories, bump the largest
      // main to 1.5 servings rather than adding a fifth meal.
      var got = sumMeals(chosen);
      if (got.kcal && target.kcal - got.kcal > 320) {
        var big = null, bigK = 0;
        chosen.forEach(function (m) {
          var r = byId(m.id);
          if (r && r.k > bigK) { bigK = r.k; big = m; }
        });
        if (big) {
          var step = clamp((target.kcal - got.kcal) / Math.max(bigK, 1), 0.5, 1);
          big.q = Math.round((1 + step) * 2) / 2;
        }
      }

      chosen.forEach(function (m) { recent[m.id] = di; });
      out[ds] = chosen;

      var fin = sumMeals(chosen);
      report.push({
        date: ds, workout: workout, target: target, got: fin,
        err: dayError(fin, target, budget),
        overBudget: budget ? fin.cost > budget : false
      });
    }

    return { plan: out, report: report, days: days, from: from, who: who };
  }
  H.generatePlan = generatePlan;

  function planFor(ds) { return S.plan[ds] || []; }
  H.planFor = planFor;

  function planRange(from, days) {
    var out = [];
    for (var i = 0; i < days; i++) {
      var ds = addDays(from, i);
      out.push({ date: ds, meals: planFor(ds) });
    }
    return out;
  }
  H.planRange = planRange;

  /* ---------------------------------------------------------- shopping */
  /* Rolls a run of planned days into one priced list, aisle by aisle, with
     anything already in the pantry deducted. */
  function shoppingFromPlan(from, days, opts) {
    opts = opts || {};
    var need = {};
    planRange(from, days).forEach(function (d) {
      d.meals.forEach(function (m) {
        var r = byId(m.id);
        if (!r) return;
        var portions = (m.q || 1) / Math.max(r.sv || 1, 1);
        (r.ing || []).forEach(function (i) {
          var key = i[1], g = (i[2] || 0) * portions;
          if (!key || !g) return;
          need[key] = (need[key] || 0) + g;
        });
      });
    });

    var items = [], skipped = [];
    Object.keys(need).forEach(function (key) {
      var q = ING(key);
      if (!q) return;
      var grams = need[key];
      var have = opts.usePantry === false ? 0 : ((S.pantry[key] && S.pantry[key].g) || 0);
      var buy = grams - have;
      if (buy <= 1) { skipped.push({ key: key, name: q.n, grams: grams }); return; }
      items.push({
        key: key, name: q.n, qty: 1, grams: Math.round(buy),
        price: (buy / 100) * best(q),
        note: Math.round(buy) + ' g' + (have ? ' (' + Math.round(have) + ' g in the pantry)' : ''),
        aisle: q.a || 'Other', done: false
      });
    });

    items.sort(function (a, b) { return a.name.localeCompare(b.name); });
    return { items: items, skipped: skipped };
  }
  H.shoppingFromPlan = shoppingFromPlan;

  function shopLists() { return S.shop.lists; }
  function curList() {
    var L = shopLists();
    if (!L[S.shop.active]) {
      var k = Object.keys(L)[0];
      if (!k) { L['Weekly shop'] = { cat: 'Groceries', fav: true, items: [] }; k = 'Weekly shop'; }
      S.shop.active = k;
    }
    return L[S.shop.active];
  }
  H.shopLists = shopLists; H.curList = curList;

  function addRecipeToShop(r, mult) {
    if (!r) return 0;
    mult = mult || 1;
    var L = curList(), n = 0;
    (r.ing || []).forEach(function (i) {
      var k = i[1], g = (i[2] || 0) * mult, q = ING(k);
      if (!q || !g) return;
      var ex = null;
      L.items.forEach(function (x) { if (x.key === k) ex = x; });
      if (ex) {
        ex.grams = (ex.grams || 0) + g;
        ex.price = (ex.grams / 100) * best(q);
        ex.qty = 1;
        ex.note = Math.round(ex.grams) + ' g';
      } else {
        L.items.push({
          key: k, name: q.n, qty: 1, price: (g / 100) * best(q), grams: g,
          note: Math.round(g) + ' g', aisle: q.a || 'Other', done: false
        });
      }
      n++;
    });
    save();
    return n;
  }
  H.addRecipeToShop = addRecipeToShop;

  function listTotals(items) {
    var todo = 0, got = 0, done = 0, aisles = {};
    (items || []).forEach(function (i) {
      var v = i.price * i.qty;
      if (i.done) { got += v; done++; } else todo += v;
      aisles[i.aisle] = 1;
    });
    return {
      todo: todo, got: got, done: done,
      aisles: Object.keys(aisles).length, n: (items || []).length
    };
  }
  H.listTotals = listTotals;

  /* ---------------------------------------------------------- pantry */
  function pantryAdd(key, grams) {
    if (!S.pantry[key]) S.pantry[key] = { g: 0 };
    S.pantry[key].g = Math.max(0, (S.pantry[key].g || 0) + grams);
    if (!S.pantry[key].g) delete S.pantry[key];
    save();
  }
  H.pantryAdd = pantryAdd;

  /* Everything ticked off on a list moves into the pantry, which is what makes
     the next generated list skip what is already in the cupboard. */
  function stockFromList(name) {
    var L = shopLists()[name || S.shop.active];
    if (!L) return 0;
    var n = 0;
    L.items.forEach(function (it) {
      if (it.done && it.key && it.grams) { pantryAdd(it.key, it.grams); n++; }
    });
    save();
    return n;
  }
  H.stockFromList = stockFromList;

  /* Logging a meal draws its ingredients back down out of the pantry. */
  function consumeFromPantry(recipeId, q) {
    var r = byId(recipeId);
    if (!r) return;
    var portions = (q || 1) / Math.max(r.sv || 1, 1);
    (r.ing || []).forEach(function (i) {
      var key = i[1], g = (i[2] || 0) * portions;
      if (key && g && S.pantry[key]) pantryAdd(key, -g);
    });
  }
  H.consumeFromPantry = consumeFromPantry;

  /* ---------------------------------------------------------- training */
  var SPLITS = {
    ppl: { n: 'Push / pull / legs', d: ['push', 'pull', 'legs', 'rest', 'push', 'pull', 'legs'] },
    ppl6: { n: 'Push / pull / legs, six days', d: ['push', 'pull', 'legs', 'push', 'pull', 'legs', 'rest'] },
    ul: { n: 'Upper / lower', d: ['push', 'legs', 'rest', 'pull', 'legs', 'rest', 'rest'] },
    full3: { n: 'Full body, three days', d: ['full', 'rest', 'full', 'rest', 'full', 'rest', 'rest'] },
    full4: { n: 'Full body plus cardio', d: ['full', 'cardio', 'full', 'rest', 'full', 'cardio', 'rest'] },
    arms: { n: 'Bro split', d: ['push', 'pull', 'legs', 'arms', 'abs', 'cardio', 'rest'] }
  };
  H.SPLITS = SPLITS;

  /* Writes a split onto the calendar. startDow lets a Monday-start split land on
     a Monday no matter which day it is generated. */
  function applySplit(splitKey, from, weeks, startDow) {
    var split = SPLITS[splitKey];
    if (!split) return 0;
    var n = 0, dayCount = clamp(weeks || 4, 1, 26) * 7;
    for (var i = 0; i < dayCount; i++) {
      var ds = addDays(from, i);
      var idx = (i + (startDow || 0)) % 7;
      dayLog(ds).workout = split.d[idx];
      n++;
    }
    save();
    return n;
  }
  H.applySplit = applySplit;

  /* Which prebuilt sessions suit today's training type. Matching on the muscle
     group by substring is not good enough — "Back" is inside "Fallback" — so
     each type names the session titles it actually belongs to. */
  var SESSION_MATCH = {
    pull: /pull emphasis|back width|back thickness|v-taper/i,
    push: /push emphasis|shoulders and arms/i,
    legs: /quad emphasis|hinge emphasis|athletic legs/i,
    arms: /arm day|levers, arms/i,
    abs: /core day/i,
    skill: /skill day/i,
    full: /full body|full physique/i
  };

  function sessionsFor(workout) {
    var re = SESSION_MATCH[workout];
    if (!re) return [];
    return SESS.filter(function (s) { return re.test(s.name || ''); });
  }
  H.sessionsFor = sessionsFor;

  function weightSeries(daysBack) {
    var out = [], start = addDays(today(), -(daysBack || 90));
    Object.keys(S.days).sort().forEach(function (ds) {
      if (ds < start) return;
      var w = S.days[ds].w;
      if (w) out.push({ x: ds, y: w });
    });
    return out;
  }
  H.weightSeries = weightSeries;

  /* ---------------------------------------------------------- financial */
  function finIncome(who, mode) {
    return S.fin.jobs.filter(function (j) {
      return who === 'both' || j.who === who || j.who === 'Both';
    }).reduce(function (a, j) { return a + (j[mode] || 0); }, 0);
  }
  function finCost(mode, path) {
    return S.fin.costs.filter(function (c) {
      if (c.section === 'Housing (rent)') return path !== 'buy';
      if (c.section === 'Housing (buy)') return path === 'buy';
      return true;
    }).reduce(function (a, c) { return a + (c[mode] || 0); }, 0);
  }
  function shiftsFor(who, from) {
    return S.fin.shifts.filter(function (s) {
      var j = null;
      S.fin.jobs.forEach(function (x) { if (x.id === s.jobId) j = x; });
      if (who && j && j.who !== who && j.who !== 'Both') return false;
      if (from && s.date < from) return false;
      return true;
    });
  }
  H.finIncome = finIncome; H.finCost = finCost; H.shiftsFor = shiftsFor;

  /* Earnings rolled up by calendar month, for the trend chart. */
  function monthlyEarnings(monthsBack) {
    var buckets = {}, now = new Date();
    for (var i = (monthsBack || 6) - 1; i >= 0; i--) {
      var d = new Date(now.getFullYear(), now.getMonth() - i, 1);
      buckets[d.getFullYear() + '-' + p2(d.getMonth() + 1)] = { net: 0, gross: 0, hours: 0 };
    }
    S.fin.shifts.forEach(function (s) {
      var key = String(s.date).slice(0, 7);
      if (!buckets[key]) return;
      buckets[key].net += s.net || 0;
      buckets[key].gross += s.gross || 0;
      buckets[key].hours += s.hours || 0;
    });
    return Object.keys(buckets).sort().map(function (k) {
      return {
        month: k, net: buckets[k].net, gross: buckets[k].gross, hours: buckets[k].hours,
        label: new Date(+k.slice(0, 4), +k.slice(5) - 1, 1)
          .toLocaleDateString(undefined, { month: 'short' })
      };
    });
  }
  H.monthlyEarnings = monthlyEarnings;

  /* Everything spent on a day: food actually logged plus the loose spends. */
  function daySpend(ds) {
    var d = dayLog(ds);
    var other = (d.spend || []).reduce(function (a, x) { return a + (x.amt || 0); }, 0);
    return { food: eaten(ds).cost, other: other, total: eaten(ds).cost + other };
  }
  H.daySpend = daySpend;

  function spendSeries(daysBack) {
    var out = [], n = daysBack || 30;
    for (var i = n - 1; i >= 0; i--) {
      var ds = addDays(today(), -i);
      if (!S.days[ds]) { out.push({ x: ds, food: 0, other: 0 }); continue; }
      var s = daySpend(ds);
      out.push({ x: ds, food: s.food, other: s.other });
    }
    return out;
  }
  H.spendSeries = spendSeries;

  /* ---------------------------------------------------------- schedule */
  var DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  H.DOW = DOW;

  function applyTemplate(fromDs) {
    var t = S.sched.tmpl || {}, n = 0;
    var base = fromDs ? dOf(fromDs) : new Date();
    base.setDate(base.getDate() - base.getDay());
    for (var i = 0; i < 7; i++) {
      var d = new Date(base);
      d.setDate(base.getDate() + i);
      var ds = dstr(d);
      (t[i] || []).forEach(function (x) {
        var log = dayLog(ds);
        var dupe = log.sched.some(function (e) {
          return e.what === x.what && e.who === x.who && e.from === x.from;
        });
        if (!dupe) {
          log.sched.push({ who: x.who, what: x.what, from: x.from, to: x.to, where: '' });
          n++;
        }
      });
    }
    save();
    return n;
  }
  H.applyTemplate = applyTemplate;

  function mins(t) { var p = String(t).split(':'); return (+p[0]) * 60 + (+(p[1] || 0)); }
  function fmtMin(m) {
    var h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? 'pm' : 'am', hh = h % 12 || 12;
    return hh + (mm ? ':' + p2(mm) : '') + ap;
  }
  H.fmtMin = fmtMin;

  /* Blocks where neither person has anything booked. Used for "both free". */
  function freeBlocks(d, minLen) {
    var busy = { Jaron: [], Aaliyah: [] };
    (d.sched || []).forEach(function (e) {
      if (!e.from || !e.to) return;
      if (e.who === 'Both') { busy.Jaron.push([e.from, e.to]); busy.Aaliyah.push([e.from, e.to]); }
      else if (busy[e.who]) busy[e.who].push([e.from, e.to]);
    });
    if (!busy.Jaron.length && !busy.Aaliyah.length) return null;

    var free = [], step = 30;
    for (var m = 8 * 60; m < 22 * 60; m += step) {
      var clash = false;
      ['Jaron', 'Aaliyah'].forEach(function (w) {
        busy[w].forEach(function (b) {
          if (m >= mins(b[0]) && m < mins(b[1])) clash = true;
        });
      });
      if (!clash) free.push(m);
    }
    if (!free.length) return [];

    var blocks = [], cur = [free[0], free[0] + step];
    for (var i = 1; i < free.length; i++) {
      if (free[i] === cur[1]) cur[1] = free[i] + step;
      else { blocks.push(cur); cur = [free[i], free[i] + step]; }
    }
    blocks.push(cur);
    return blocks.filter(function (b) { return b[1] - b[0] >= (minLen || 60); });
  }
  H.freeBlocks = freeBlocks;

  /* ---------------------------------------------------------- backup */
  function exportBlob() {
    return { app: 'handbook', version: 6, exported: new Date().toISOString(), state: S };
  }
  H.exportBlob = exportBlob;

  function daysSinceExport() {
    if (!S.lastExport) return null;
    return Math.floor((Date.now() - S.lastExport) / 86400000);
  }
  H.daysSinceExport = daysSinceExport;

  function markExported() { S.lastExport = Date.now(); save(true); }
  H.markExported = markExported;

  /* Rough localStorage footprint, so the storage warning can arrive before the
     write actually fails. */
  function storageUsed() {
    try {
      var bytes = JSON.stringify(S).length;
      return { bytes: bytes, mb: bytes / 1048576, pct: Math.min(100, bytes / 5242880 * 100) };
    } catch (e) {
      return { bytes: 0, mb: 0, pct: 0 };
    }
  }
  H.storageUsed = storageUsed;

  function importState(text) {
    var o = JSON.parse(text);
    var st = o.state || o;
    if (!st.prof) throw new Error('That file has no profiles in it, so it is not a handbook save.');
    H.setState(st);
    save(true);
    invalidate();
    return true;
  }
  H.importState = importState;

})(typeof window !== 'undefined' ? window : globalThis);
