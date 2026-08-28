/* ============================================================
   The Handbook - views

   Every view is a function that returns an HTML string for the
   main region. They read state and never write it; app.js owns
   the wiring and the writes.
   ============================================================ */
(function (global) {
  'use strict';

  var H = global.Handbook;
  var E = H.E, money = H.money, money0 = H.money0;
  var V = H.views = {};

  function S() { return H.state(); }

  /* ---------------------------------------------------------- card art */
  var CATC = {
    'Breakfast': ['#D89A3C', '#B0651F'],
    'Lunch/Dinner': ['#2C6B50', '#173C2C'],
    'Snack': ['#4E8C7A', '#28584A'],
    'Drink': ['#6E5AA8', '#3F3168'],
    'SDA Meat/Fish': ['#C4614B', '#8A3826'],
    'My recipe': ['#6B6B5E', '#3E3E36']
  };
  H.CATC = CATC;

  function art(r) {
    var ph = S().photos[r.id];
    if (ph) return '<div class="rcart"><img src="' + ph + '" alt="" loading="lazy"></div>';
    var c = CATC[r.cat] || CATC['My recipe'];
    return '<div class="rcart" style="background:linear-gradient(135deg,' + c[0] + ',' + c[1] + ')">' +
      '<svg class="plate" viewBox="0 0 120 70" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
      '<circle cx="45" cy="35" r="21" fill="none" stroke="rgba(255,255,255,.30)" stroke-width="3"/>' +
      '<circle cx="45" cy="35" r="12" fill="none" stroke="rgba(255,255,255,.20)" stroke-width="2"/>' +
      '<path d="M78 18v34M86 18v12a4 4 0 004 4h0v18M96 18v34" stroke="rgba(255,255,255,.28)" ' +
      'stroke-width="3" fill="none" stroke-linecap="round"/></svg>' +
      H.ringSVG(r) + '</div>';
  }

  function heroPlate() {
    return '<svg class="heroart" viewBox="0 0 240 140" preserveAspectRatio="xMaxYMid slice" ' +
      'aria-hidden="true"><g fill="none" stroke="rgba(255,255,255,.16)">' +
      '<circle cx="176" cy="58" r="46" stroke-width="4"/>' +
      '<circle cx="176" cy="58" r="26" stroke-width="3"/>' +
      '<path d="M214 22v78M226 22v26a9 9 0 009 9v43" stroke-width="4" stroke-linecap="round"/>' +
      '</g></svg>';
  }

  function pscale(v) { return v < 1.6 ? '$' : v < 3.2 ? '$$' : '$$$'; }

  function rcard(r) {
    var fav = S().fav.indexOf(r.id) >= 0;
    var dc = r.diff === 'EASY' ? 'd1' : r.diff === 'MODERATE' ? 'd2' : 'd3';
    var diff = (r.diff || 'EASY');
    return '<article class="rc" data-go="' + r.id + '" tabindex="0" role="link" ' +
      'aria-label="' + E(r.n) + ', ' + Math.round(r.k) + ' calories">' + art(r) +
      '<button class="fav' + (fav ? ' on' : '') + '" data-fav="' + r.id + '" ' +
      'aria-pressed="' + fav + '" aria-label="' + (fav ? 'Remove from' : 'Add to') + ' favourites">' +
      (fav ? '★' : '☆') + '</button>' +
      '<div class="rcbadge">' + E(r.id) + '</div><div class="rcb">' +
      '<div class="rcn">' + E(r.n) + '</div>' +
      '<div class="chips"><span class="chip">' + r.t + ' min</span>' +
      '<span class="chip ' + dc + '">' + diff.charAt(0) + diff.slice(1).toLowerCase() + '</span>' +
      '<span class="chip p">' + pscale(H.cps(r)) + ' ' + money(H.cps(r)) + '</span>' +
      '<span class="chip t">' + E(H.bestFor(r)) + '</span></div>' +
      '<div class="rcm"><div><b>' + Math.round(r.k) + '</b><span>kcal</span></div>' +
      '<div><b>' + Math.round(r.p) + '</b><span>prot</span></div>' +
      '<div><b>' + Math.round(r.c) + '</b><span>carb</span></div>' +
      '<div><b>' + Math.round(r.f) + '</b><span>fat</span></div></div></div></article>';
  }
  H.rcard = rcard;

  /* ============================================================ MEALS */
  H.flt = { q: '', cat: '', tag: '', sort: 'rec', page: 1 };
  var PAGE = 48;

  V.meals = function () {
    var st = S(), ds = H.today(), d = H.dayLog(ds);
    var tgt = H.dayTarget(st.who, d.workout), got = H.eaten(ds);
    var left = { k: Math.max(150, tgt.kcal - got.kcal), p: Math.max(10, tgt.p - got.p) };
    var rec = H.rank(left, d.workout).slice(0, 8);
    var est = H.estDayCost(tgt, st.prefs.costMode);
    var planned = H.planFor(ds);

    return '<div class="page"><div class="phead"><h1>Meals</h1>' +
      '<p>' + H.all().length + ' recipes, all gluten-free. Average ' + money(H.avgCost()) +
      ' a serving at the cheaper of Walmart or Costco.</p></div>' +

      '<div class="sec"><div class="spread"><h2>What ' + E(H.P().name) + ' needs today</h2>' +
      '<button class="b o s" data-nav="plan">Plan the week</button></div>' +
      '<p class="sub">Adjusted for ' + E(H.TRAIN[d.workout].n.toLowerCase()) +
      '. Change it on the Training tab.</p>' +
      '<div class="grid g2"><div class="card pad">' + H.statRow(tgt) +
      '<div style="height:16px"></div>' +
      H.bar('Calories', got.kcal, tgt.kcal, 'pk') +
      H.bar('Protein', got.p, tgt.p, 'pp') +
      H.bar('Carbs', got.c, tgt.c, 'pc') +
      H.bar('Fat', got.f, tgt.f, 'pf') +
      '<p class="sm muted" style="margin-top:12px">Left today: <b>' + Math.round(left.k) +
      ' kcal</b>, <b>' + Math.round(left.p) + ' g protein</b> &middot; spent ' +
      money(got.cost) + '</p>' +
      (planned.length
        ? '<div class="note" style="margin-bottom:0"><b>Planned for today.</b> ' +
        planned.map(function (m) {
          var r = H.byId(m.id);
          return r ? E(r.n) : '';
        }).filter(Boolean).join(', ') +
        '. <button class="b o s" id="logPlanned" style="margin-left:6px">Log all of it</button></div>'
        : '') +
      '</div>' +

      '<div class="card pad"><h3 style="font-size:15px">What that costs</h3>' +
      '<p class="sub sm">Estimated food cost to actually hit today\'s numbers.</p>' +
      '<label class="f"><span>Base the estimate on</span><select id="costMode">' +
      H.opt([['all', 'Every recipe (average)'], ['cheap', 'The cheapest 40 per calorie'],
      ['fav', 'My favourites only'], ['logged', 'What we actually logged']], st.prefs.costMode) +
      '</select></label>' +
      '<div class="stats">' +
      H.stat(money(est.byKcal), 'Today', 'acc') +
      (est.byProt ? H.stat(money(est.byProt), 'By protein') : '') +
      H.stat(money(est.byKcal * 7), 'Per week') +
      H.stat(money(est.byKcal * 30), 'Per month') + '</div>' +
      '<p class="xs muted" style="margin-top:10px">From ' + E(est.src) + '. ' +
      (est.byProt ? 'The two figures differ because protein is the expensive macro; if they are ' +
        'far apart the day is protein-heavy relative to its calories.' : '') + '</p>' +
      '<div class="row" style="margin-top:12px">' +
      '<button class="b o s" id="bothCost">Cost for both of us</button></div>' +
      '<div id="bothOut"></div></div></div></div>' +

      '<div class="sec"><h2>For today</h2>' +
      '<p class="sub">Ranked for the session and what is left.</p>' +
      '<div class="grid g3" data-stagger>' + rec.map(rcard).join('') + '</div></div>' +

      (st.fav.length
        ? '<div class="sec"><h2>Favourites</h2><div class="grid g3" data-stagger>' +
        st.fav.map(H.byId).filter(Boolean).map(rcard).join('') + '</div></div>'
        : '') +

      '<div class="sec"><h2>Everything</h2>' +
      '<div class="card pad filterbar"><div class="fr">' +
      '<label class="f"><span>Search</span><input id="fq" type="search" ' +
      'placeholder="tofu, oats, burger..." value="' + E(H.flt.q) + '"></label>' +
      '<label class="f"><span>Category</span><select id="fcat">' +
      H.opt([['', 'All'], ['Breakfast', 'Breakfast'], ['Lunch/Dinner', 'Mains'], ['Snack', 'Snacks'],
      ['Drink', 'Drinks'], ['SDA Meat/Fish', 'Meat and fish'], ['My recipe', 'Mine']], H.flt.cat) +
      '</select></label>' +
      '<label class="f"><span>Best for</span><select id="ftag">' +
      H.opt([['', 'Any'], ['LEUCINE PRIORITY', 'High protein'], ['CHEAT MEAL', 'Cheat meal'],
      ['HEALTHY DESSERT', 'Dessert'], ['BUDGET FRIENDLY', 'Cheap'], ['NO-COOK', 'No cooking'],
      ['MEAL PREP', 'Meal prep'], ['HIGH FIBER', 'High fiber'], ['QUICK', 'Under ten minutes']],
        H.flt.tag) + '</select></label>' +
      '<label class="f"><span>Sort</span><select id="fsort">' +
      H.opt([['rec', 'Protein'], ['cheap', 'Cheapest'], ['kcal_cheap', 'Cheapest per calorie'],
      ['t', 'Fastest'], ['k', 'Most calories'], ['az', 'A to Z']], H.flt.sort) +
      '</select></label></div>' +
      '<div class="row"><button class="b o s" id="addOwn">Add my own recipe</button>' +
      '<button class="b o s" id="clearFlt">Clear filters</button>' +
      '<span class="right sm muted" id="fcount"></span></div></div>' +
      '<div class="grid g3" id="fgrid"></div>' +
      '<div class="row" style="justify-content:center;margin-top:20px" id="fmore"></div>' +
      '</div></div>';
  };

  H.filtered = function () {
    var q = H.flt.q.toLowerCase().trim();
    var L = H.all().filter(function (r) {
      if (H.flt.cat && r.cat !== H.flt.cat) return false;
      if (H.flt.tag && r.tg.indexOf(H.flt.tag) < 0) return false;
      if (q) {
        var hay = (r.n + ' ' + r.cat + ' ' + r.tg.join(' ') + ' ' +
          (r.ing || []).map(function (i) {
            var m = H.ING(i[1]);
            return m ? m.n : '';
          }).join(' ')).toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });
    var s = H.flt.sort;
    L.sort(function (a, b) {
      if (s === 'cheap') return H.cps(a) - H.cps(b);
      if (s === 'kcal_cheap') return (H.cps(a) / Math.max(a.k, 1)) - (H.cps(b) / Math.max(b.k, 1));
      if (s === 't') return a.t - b.t;
      if (s === 'k') return b.k - a.k;
      if (s === 'az') return a.n.localeCompare(b.n);
      return b.p - a.p;
    });
    return L;
  };

  /* ============================================================ RECIPE */
  V.recipe = function (id) {
    var r = H.byId(id);
    if (!r) {
      return '<div class="page">' + H.empty('That recipe is not here.',
        'It may have been a custom one that was removed.',
        '<button class="b" data-nav="meals">Back to meals</button>') + '</div>';
    }
    var st = S(), sv = r.sv || 1;
    var fav = st.fav.indexOf(id) >= 0, ph = st.photos[id];
    var c = CATC[r.cat] || CATC['My recipe'];

    return '<div class="page">' +
      '<div class="row" style="margin:16px 0 14px">' +
      '<button class="b o s" data-nav="meals">&larr; Meals</button>' +
      '<span class="chip">' + E(r.id) + '</span>' +
      '<span class="chip">' + E(r.cat) + '</span></div>' +

      '<div class="dhero" style="background:linear-gradient(135deg,' + c[0] + ',' + c[1] + ')">' +
      (ph ? '<img src="' + ph + '" alt="">' : heroPlate()) +
      '<div class="scrim"></div><div class="in">' +
      '<div class="chips"><span class="chip">' + E(r.diff) + '</span>' +
      '<span class="chip">' + r.t + ' min</span>' +
      '<span class="chip">' + E(H.bestFor(r)) + '</span></div>' +
      '<h1>' + E(r.n) + '</h1>' +
      '<div class="sm" style="color:rgba(255,255,255,.85)">makes <span id="svHero">' + sv +
      '</span> &middot; ' + money(H.cps(r)) + ' per serving, <span id="totHero">' +
      money(H.ctot(r)) + '</span> total</div></div></div>' +

      '<div class="row" style="margin:16px 0">' +
      '<button class="b" data-log="' + id + '">Log to today</button>' +
      '<button class="b o" data-fav="' + id + '">' + (fav ? '★ Favourited' : '☆ Favourite') + '</button>' +
      '<button class="b o" data-plan="' + id + '">Put on a day</button>' +
      '<button class="b o" data-groc="' + id + '">Add to shopping</button>' +
      '<button class="b o" data-tolist="' + id + '">Add to a list</button>' +
      '<button class="b o" data-photo="' + id + '">' + (ph ? 'Change photo' : 'Add photo') + '</button>' +
      '<button class="b o" data-card="' + id + '">Save card</button>' +
      (ph ? '<button class="b o dz" data-rmphoto="' + id + '">Remove photo</button>' : '') +
      '</div>' +

      '<div class="sec"><div class="stats s6">' +
      H.stat(Math.round(r.k), 'Calories', 'acc') +
      H.stat(Math.round(r.p) + 'g', 'Protein') +
      H.stat(Math.round(r.c) + 'g', 'Carbs') +
      H.stat(Math.round(r.f) + 'g', 'Fat') +
      H.stat(Math.round(r.fib || 0) + 'g', 'Fiber') +
      H.stat((r.leu || 0).toFixed(1) + 'g', 'Leucine') + '</div>' +
      '<p class="muted sm" style="margin-top:9px">Every number above is <b>one plated serving</b>. ' +
      'Making <span id="batchSv">' + sv + '</span> total: <span id="batchAll">' +
      Math.round(r.k * sv) + ' kcal, ' + Math.round(r.p * sv) + ' g protein, ' +
      Math.round(r.c * sv) + ' g carbs, ' + Math.round(r.f * sv) + ' g fat, ' +
      money(H.ctot(r)) + '</span>.</p></div>' +

      '<div class="grid g2"><div class="card pad">' +
      '<div class="spread" style="margin-bottom:10px"><h3 style="font-size:16px">Ingredients ' +
      '<span class="muted sm" id="svLabel">for ' + sv + '</span></h3></div>' +
      '<div class="row" style="margin-bottom:12px"><span class="muted sm">Scale</span>' +
      [0.5, 1, 1.5, 2, 3, 4].map(function (x) {
        return '<button class="pill' + (x === 1 ? ' on' : '') + '" data-scale="' + x + '">' + x + 'x</button>';
      }).join('') + '</div>' +
      '<ul class="ing" id="ingList"></ul>' +
      '<p class="xs muted" style="margin-top:10px">Prices come from the ingredient list. ' +
      '<a href="#/shopping/ingredients">Edit an ingredient</a> and every recipe using it updates.</p>' +
      '</div>' +

      '<div class="card pad"><div class="spread" style="margin-bottom:12px">' +
      '<h3 style="font-size:16px">Method</h3>' +
      '<span class="xs muted">Tap a step to tick it off</span></div>' +
      '<ol class="stp" id="stepList">' +
      (r.st || []).map(function (s, i) {
        return '<li data-step="' + i + '">' + E(s) + '</li>';
      }).join('') + '</ol></div></div>' +

      (r.prep ? '<div class="note"><b>Note.</b> ' + E(r.prep) + '</div>' : '') +
      '<div class="grid g2" style="margin-top:14px">' +
      (r.storage ? '<div class="card pad"><h4 class="lbl">Storage</h4>' +
        '<p class="sm" style="margin:8px 0 0">' + E(r.storage) + '</p></div>' : '') +
      ((r.subs || []).length ? '<div class="card pad"><h4 class="lbl">Substitutions</h4>' +
        '<ul class="sm" style="margin:8px 0 0;padding-left:18px">' +
        r.subs.map(function (s) { return '<li>' + E(s) + '</li>'; }).join('') + '</ul></div>' : '') +
      ((r.vars || []).length ? '<div class="card pad"><h4 class="lbl">Variations</h4>' +
        '<ul class="sm" style="margin:8px 0 0;padding-left:18px">' +
        r.vars.map(function (s) { return '<li>' + E(s) + '</li>'; }).join('') + '</ul></div>' : '') +
      '</div></div>';
  };

  /* ============================================================ PLAN */
  H.planOpts = { days: 7, slots: 4, budget: '', favOnly: false, maxMinutes: '', variety: 3 };

  V.plan = function () {
    var st = S(), from = H.planCursor || H.today();
    var days = H.planOpts.days;
    var rows = H.planRange(from, days);
    var anyPlanned = rows.some(function (r) { return r.meals.length; });

    var totals = { kcal: 0, p: 0, cost: 0, tk: 0, tp: 0 };
    rows.forEach(function (row) {
      var sum = H.sumMeals(row.meals);
      var workout = (st.days[row.date] && st.days[row.date].workout) || 'rest';
      var t = H.dayTarget(st.who, workout);
      totals.kcal += sum.kcal; totals.p += sum.p; totals.cost += sum.cost;
      totals.tk += t.kcal; totals.tp += t.p;
    });

    return '<div class="page"><div class="phead"><h1>Meal plan</h1>' +
      '<p>Generate a run of days that lands on ' + E(H.P().name) +
      '’s macro targets without going over budget, then turn the whole thing ' +
      'into one shopping list.</p></div>' +

      '<div class="card pad filterbar"><div class="fr">' +
      '<label class="f"><span>Start</span><input id="pFrom" type="date" value="' + from + '"></label>' +
      '<label class="f"><span>How many days</span><select id="pDays">' +
      H.opt([[3, '3 days'], [5, '5 days'], [7, 'A week'], [14, 'Two weeks'], [28, 'Four weeks']],
        H.planOpts.days) + '</select></label>' +
      '<label class="f"><span>Meals a day</span><select id="pSlots">' +
      H.opt([[2, '2'], [3, '3'], [4, '4']], H.planOpts.slots) + '</select></label>' +
      '<label class="f"><span>Budget a day</span>' +
      '<input id="pBudget" type="number" step="0.5" min="0" placeholder="no limit" value="' +
      E(H.planOpts.budget) + '"></label>' +
      '<label class="f"><span>Nothing longer than</span><select id="pMax">' +
      H.opt([['', 'Any length'], [10, '10 minutes'], [20, '20 minutes'], [35, '35 minutes']],
        H.planOpts.maxMinutes) + '</select></label>' +
      '<label class="f"><span>Repeat a meal after</span><select id="pVar">' +
      H.opt([[1, 'Any time'], [2, '2 days'], [3, '3 days'], [5, '5 days'], [7, 'A week']],
        H.planOpts.variety) + '</select></label>' +
      '</div><div class="row">' +
      '<button class="b" id="pGen">Generate the plan</button>' +
      '<button class="pill' + (H.planOpts.favOnly ? ' on' : '') + '" id="pFav">Favourites only</button>' +
      (anyPlanned ? '<button class="b o" id="pShop">Build the shopping list</button>' +
        '<button class="b o" id="pCsv">Export</button>' +
        '<button class="b o dz right" id="pClear">Clear the plan</button>' : '') +
      '</div></div>' +

      (anyPlanned ? '<div class="stats" style="margin:16px 0">' +
        H.stat(money(totals.cost), 'Food for ' + days + ' days', 'acc') +
        H.stat(money(totals.cost / days), 'A day') +
        H.stat(Math.round(totals.kcal / days).toLocaleString(), 'Avg kcal') +
        H.stat(Math.round(totals.p / days) + 'g', 'Avg protein') +
        H.stat(pct(totals.kcal, totals.tk), 'Of kcal target') +
        H.stat(pct(totals.p, totals.tp), 'Of protein target') + '</div>' : '') +

      (anyPlanned
        ? '<div class="sec"><div class="plan" data-stagger>' + rows.map(planDay).join('') + '</div>' +
        '<p class="sm muted" style="margin-top:14px">Tap any meal to swap it, or open the day ' +
        'on the schedule to log what actually happened.</p></div>'
        : '<div class="sec">' + H.empty(
          'No plan yet for these days.',
          'Generating one picks real recipes so the week lands on the targets, then the ' +
          'shopping list falls out of it.',
          '<button class="b" id="pGen2">Generate the plan</button>') + '</div>') +
      '</div>';
  };

  function pct(a, b) { return b ? Math.round(a / b * 100) + '%' : '—'; }

  function planDay(row) {
    var st = S();
    var workout = (st.days[row.date] && st.days[row.date].workout) || 'rest';
    var t = H.dayTarget(st.who, workout);
    var sum = H.sumMeals(row.meals);
    var kOk = Math.abs(sum.kcal - t.kcal) / Math.max(t.kcal, 1) <= 0.1;
    var pOk = sum.p >= t.p * 0.92;
    var d = H.dOf(row.date);

    return '<div class="pday' + (row.date === H.today() ? ' today' : '') + '">' +
      '<h4>' + E(H.DOW[d.getDay()]) + ' <span>' + E(H.shortD(row.date)) + '</span></h4>' +
      '<div class="xs muted" style="margin-top:-4px">' + E(H.TRAIN[workout].n) + '</div>' +
      (row.meals.length
        ? row.meals.map(function (m, i) {
          var r = H.byId(m.id);
          if (!r) return '';
          return '<button class="pmeal" data-swap="' + row.date + '|' + i + '">' +
            '<span class="nm">' + E(r.n) + (m.q !== 1 ? ' <span class="kc">×' + m.q + '</span>' : '') + '</span>' +
            '<span class="kc">' + Math.round(r.k * (m.q || 1)) + '</span></button>';
        }).join('')
        : '<p class="xs muted">Nothing planned.</p>') +
      '<div class="pfoot">' +
      '<span class="' + (kOk ? 'hit' : 'miss') + '">' + Math.round(sum.kcal) + ' / ' + t.kcal + ' kcal</span>' +
      '<span class="' + (pOk ? 'hit' : 'miss') + '">' + Math.round(sum.p) + 'g P</span>' +
      '<span>' + money(sum.cost) + '</span></div></div>';
  }

  /* ============================================================ SHOPPING */
  V.shopping = function (sub) {
    if (sub === 'ingredients') return V.ingredients();
    if (sub === 'pantry') return V.pantry();

    var st = S(), L = H.shopLists(), names = Object.keys(L);
    var cur = H.curList(), items = cur.items || [];
    var byAisle = {};
    items.forEach(function (it, i) {
      (byAisle[it.aisle] = byAisle[it.aisle] || []).push([it, i]);
    });
    var order = H.AISLES.map(function (a) { return a[0]; }).concat(['Other']);
    var tot = H.listTotals(items);
    var cats = {};
    names.forEach(function (n) {
      var c = L[n].cat || 'Lists';
      (cats[c] = cats[c] || []).push(n);
    });

    return '<div class="page"><div class="phead"><h1>Shopping</h1>' +
      '<p>Every item priced at whichever of Walmart Fort Collins or Costco Timnath is ' +
      'cheaper for that item.</p></div>' +

      '<div class="sec"><div class="spread"><h2>Lists</h2>' +
      '<div class="row"><button class="b o s" id="newList">New list</button>' +
      '<button class="b o s" data-nav="shopping/pantry">Pantry</button>' +
      '<button class="b o s" data-nav="shopping/ingredients">Ingredient list</button></div></div>' +
      Object.keys(cats).sort().map(function (c) {
        return '<div style="margin:10px 0"><div class="lbl" style="margin-bottom:7px">' + E(c) + '</div>' +
          '<div class="row">' + cats[c].map(function (n) {
            return '<button class="pill' + (n === st.shop.active ? ' on' : '') +
              '" data-list="' + E(n) + '">' + (L[n].fav ? '★ ' : '') + E(n) +
              ' <span class="muted">' + L[n].items.length + '</span></button>';
          }).join('') + '</div></div>';
      }).join('') + '</div>' +

      '<div class="sec"><div class="spread"><h2>' + E(st.shop.active) + '</h2>' +
      '<div class="row"><button class="b o s" id="listFav">' +
      (cur.fav ? '★ Favourite' : '☆ Favourite') + '</button>' +
      '<button class="b o s" id="listRename">Rename</button>' +
      '<button class="b o s" id="listDup">Duplicate</button>' +
      '<button class="b o s dz" id="listDel">Delete</button></div></div>' +

      '<div class="stats" style="margin:12px 0">' +
      H.stat(money0(tot.todo), 'Still to buy', 'acc', 'shopTodo') +
      H.stat(tot.n, 'Items', '', 'shopCount') +
      H.stat(money0(tot.got), 'In the cart', '', 'shopGot') +
      H.stat(tot.aisles, 'Aisles') + '</div>' +

      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b" id="gAdd">Add item</button>' +
      '<button class="b o" id="gRecipe">Add from a recipe</button>' +
      '<button class="b o" id="gPlan">Build from the meal plan</button>' +
      '<button class="b o" id="gTxt">Checklist</button>' +
      '<button class="b o" id="gCsv">CSV</button>' +
      '<button class="b o" id="gSave">Save to file</button>' +
      '<button class="b o" id="gLoad">Load</button></div>' +
      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b o" id="gStock">Move checked into the pantry</button>' +
      '<button class="b o dz right" id="gClear">Clear checked</button></div>' +

      (items.length
        ? '<div id="shopBody">' + order.filter(function (a) { return byAisle[a]; }).map(function (a) {
          var rows = byAisle[a];
          var st2 = rows.reduce(function (x, p) { return x + (p[0].done ? 0 : p[0].price * p[0].qty); }, 0);
          return '<div class="card" style="margin-bottom:12px;overflow:hidden">' +
            '<div class="aisle">' + E(a) + '<span>' + money0(st2) + '</span></div>' +
            rows.map(function (p) {
              var it = p[0], i = p[1];
              return '<div class="gitem' + (it.done ? ' done' : '') + '">' +
                '<input type="checkbox" data-gt="' + i + '"' + (it.done ? ' checked' : '') +
                ' aria-label="' + E(it.name) + '">' +
                '<div style="flex:1;min-width:0"><div class="gn">' + E(it.name) + '</div>' +
                '<div class="gq">' + (it.qty > 1 ? it.qty + ' × ' : '') + E(it.note || '') +
                (it.key ? ' &middot; ' + E(H.bestStore(H.ING(it.key))) : '') + '</div></div>' +
                '<span class="gp">' + money(it.price * it.qty) + '</span>' +
                '<button class="b o s" data-ge="' + i + '">Edit</button>' +
                '<button class="x" data-gd="' + i + '" aria-label="Remove">&times;</button></div>';
            }).join('') + '</div>';
        }).join('') + '</div>'
        : H.empty('Nothing on this list.',
          'Add an item, open a recipe and hit Add to shopping, or build the whole list ' +
          'straight off the meal plan.',
          '<button class="b" id="gPlan2">Build from the meal plan</button>')) +
      '</div></div>';
  };

  V.pantry = function () {
    var st = S();
    var keys = Object.keys(st.pantry).filter(function (k) { return H.ING(k); });
    keys.sort(function (a, b) { return H.ING(a).n.localeCompare(H.ING(b).n); });
    var value = keys.reduce(function (a, k) {
      return a + (st.pantry[k].g / 100) * H.best(H.ING(k));
    }, 0);

    return '<div class="page"><div class="phead"><h1>Pantry</h1>' +
      '<p>What is already in the cupboard. A generated shopping list subtracts this ' +
      'first, and logging a meal draws it back down.</p></div>' +

      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b" id="panAdd">Add something</button>' +
      '<button class="b o" data-nav="shopping">&larr; Lists</button>' +
      '<button class="b o" id="panCsv">Export</button>' +
      (keys.length ? '<button class="b o dz right" id="panClear">Empty the pantry</button>' : '') +
      '</div>' +

      (keys.length
        ? '<div class="stats" style="margin-bottom:16px">' +
        H.stat(keys.length, 'Things in stock', 'acc') +
        H.stat(money0(value), 'Roughly worth') + '</div>' +
        '<div class="tw"><table><thead><tr><th>Ingredient</th><th>Aisle</th>' +
        '<th>In stock</th><th>Value</th><th></th></tr></thead><tbody>' +
        keys.map(function (k) {
          var g = H.ING(k), grams = st.pantry[k].g;
          return '<tr><td><b>' + E(g.n) + '</b></td>' +
            '<td class="sm muted">' + E(g.a || 'Other') + '</td>' +
            '<td class="num">' + Math.round(grams) + ' g</td>' +
            '<td class="num">' + money(grams / 100 * H.best(g)) + '</td>' +
            '<td><button class="b o s" data-pane="' + E(k) + '">Edit</button> ' +
            '<button class="x" data-pand="' + E(k) + '" aria-label="Remove">&times;</button></td></tr>';
        }).join('') + '</tbody></table></div>'
        : H.empty('The pantry is empty.',
          'Tick things off a shopping list and hit "Move checked into the pantry", or add ' +
          'what is already in the cupboard by hand.',
          '<button class="b" id="panAdd2">Add something</button>')) +
      '</div>';
  };

  V.ingredients = function () {
    var st = S();
    var count = H.allIngKeys().length;
    var edited = Object.keys(st.ingOv).length;
    return '<div class="page"><div class="phead"><h1>Ingredient list</h1>' +
      '<p>The master list every recipe price comes from. Edit a price here and all ' +
      H.all().length + ' recipes recost instantly. ' + edited + ' edited or added so far.</p></div>' +
      '<div class="card pad filterbar"><div class="row">' +
      '<button class="b" id="ingNew">Add an ingredient</button>' +
      '<button class="b o" data-nav="shopping">&larr; Back to lists</button>' +
      '<button class="b o" id="ingCsv">Export list</button>' +
      '<input class="inp right" id="ingQ" type="search" style="max-width:260px" ' +
      'placeholder="Search ' + count + ' ingredients" aria-label="Search ingredients">' +
      '</div></div>' +
      '<div class="tw"><table><thead><tr><th>Ingredient</th><th>Aisle</th>' +
      '<th>Walmart /100g</th><th>Costco /100g</th><th>Best</th><th>Used in</th><th></th></tr></thead>' +
      '<tbody id="ingBody"></tbody></table></div>' +
      '<p class="sm muted" id="ingCount" style="margin-top:10px"></p></div>';
  };

  /* ============================================================ TRAINING */
  H.exFlt = { q: '', mg: '', eq: '', hero: false };

  V.training = function (sub) {
    if (sub === 'exercises') return V.exercises();
    var st = S(), ds = H.today(), d = H.dayLog(ds);
    var t = H.dayTarget(st.who, d.workout);

    var week = [];
    for (var i = 6; i >= 0; i--) {
      var k = H.addDays(ds, -i);
      week.push([k, st.days[k] ? st.days[k].workout : null]);
    }
    var trained = week.filter(function (x) { return x[1] && x[1] !== 'rest'; }).length;
    var wSeries = H.weightSeries(90);
    var suggested = H.sessionsFor(d.workout);

    var rows = Object.keys(H.TRAIN).map(function (k) {
      var tt = H.dayTarget(st.who, k);
      return '<tr' + (d.workout === k ? ' class="hl"' : '') + '>' +
        '<td><b>' + E(H.TRAIN[k].n) + '</b></td>' +
        '<td class="num">' + tt.kcal + '</td><td class="num">' + tt.p + ' g</td>' +
        '<td class="num">' + tt.c + ' g</td><td class="num">' + tt.f + ' g</td>' +
        '<td class="sm muted">' + E(H.TRAIN[k].why.split('.')[0]) + '.</td></tr>';
    }).join('');

    return '<div class="page"><div class="phead"><h1>Training</h1>' +
      '<p>' + H.EX.length + ' exercises, ' + H.SESS.length + ' prebuilt sessions, and the ' +
      'macro shift each session type causes.</p></div>' +

      '<div class="sec"><div class="spread"><h2>Today</h2>' +
      '<button class="b o s" id="splitBtn">Generate a split</button></div>' +
      '<div class="grid g2"><div class="card pad">' +
      '<label class="f"><span>Session</span><select id="tWorkout">' +
      Object.keys(H.TRAIN).map(function (k) {
        return '<option value="' + k + '"' + (d.workout === k ? ' selected' : '') + '>' +
          E(H.TRAIN[k].n) + '</option>';
      }).join('') + '</select></label>' +
      '<label class="f"><span>Notes, lifts, PRs</span>' +
      '<textarea id="tNotes" rows="3" placeholder="Weighted pull-up 3x5 +25 lb">' +
      E(d.notes || '') + '</textarea></label>' +
      '<label class="f"><span>Bodyweight this morning</span>' +
      '<input id="tW" type="number" step="0.1" value="' + (d.w || '') + '"></label>' +
      '<button class="b" id="tSave">Save</button></div>' +

      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:10px">Targets for this session</h3>' +
      H.statRow(t) +
      '<div class="note" style="margin-top:12px">' + E(H.TRAIN[d.workout].why) + '</div>' +
      '<div class="lbl" style="margin-top:14px">Last 7 days &middot; ' + trained + ' sessions</div>' +
      '<div class="row" style="margin-top:8px">' +
      week.map(function (x) {
        var isTrain = x[1] && x[1] !== 'rest';
        return '<span class="pill flat' + (isTrain ? ' on' : '') + '">' +
          E(H.shortD(x[0]).split(' ')[1]) + ' ' +
          E(x[1] ? H.TRAIN[x[1]].n.split(' ')[0] : '—') + '</span>';
      }).join('') + '</div>' +
      (suggested.length
        ? '<div class="lbl" style="margin-top:16px">Sessions for today</div><div class="row" style="margin-top:8px">' +
        suggested.slice(0, 4).map(function (s) {
          return '<button class="pill" data-sess="' + H.SESS.indexOf(s) + '">' + E(s.name) + '</button>';
        }).join('') + '</div>'
        : '') +
      '</div></div></div>' +

      (wSeries.length > 1
        ? '<div class="sec"><h2>Bodyweight</h2>' +
        '<p class="sub">Every morning weigh-in logged in the last 90 days.</p>' +
        '<div class="card pad">' +
        H.lineChart(wSeries, {
          label: 'Bodyweight over the last 90 days', uid: 'w', px: 170,
          fmt: function (p) { return p.y.toFixed(1) + ' lb'; }
        }) + '</div></div>'
        : '') +

      '<div class="sec"><div class="spread"><h2>Sessions</h2>' +
      '<button class="b o s" data-nav="training/exercises">Exercise database</button></div>' +
      '<p class="sub">From the printable guide. Tap one to see the full session.</p>' +
      '<div class="grid g3" data-stagger>' + H.SESS.map(function (s, i) {
        return '<button class="card pad" data-sess="' + i + '" style="text-align:left;cursor:pointer">' +
          '<div style="font-weight:700;color:var(--ink);font-family:var(--fd);font-size:16px">' +
          E(s.name) + '</div>' +
          '<div class="xs muted" style="margin-top:5px">' + s.ex.length + ' exercises</div></button>';
      }).join('') + '</div></div>' +

      '<div class="sec"><h2>Macro shift by session</h2>' +
      '<div class="tw"><table><thead><tr><th>Session</th><th>Kcal</th><th>Protein</th>' +
      '<th>Carbs</th><th>Fat</th><th>Why</th></tr></thead><tbody>' + rows +
      '</tbody></table></div></div></div>';
  };

  V.exercises = function () {
    var mgs = [];
    H.EX.forEach(function (e) { if (mgs.indexOf(e.mg) < 0) mgs.push(e.mg); });
    mgs.sort();
    return '<div class="page"><div class="phead"><h1>Exercise database</h1>' +
      '<p>' + H.EX.length + ' exercises with technique, mistakes, progressions and regressions.</p></div>' +
      '<div class="card pad filterbar"><div class="fr">' +
      '<label class="f"><span>Search</span><input id="exq" type="search" ' +
      'placeholder="pull-up, planche..." value="' + E(H.exFlt.q) + '"></label>' +
      '<label class="f"><span>Muscle group</span><select id="exmg">' +
      H.opt([['', 'All']].concat(mgs.map(function (m) { return [m, m]; })), H.exFlt.mg) +
      '</select></label>' +
      '<label class="f"><span>Equipment</span><select id="exeq">' +
      H.opt([['', 'Anything'], ['Bodyweight', 'Bodyweight'], ['Dumbbell', 'Dumbbells'],
      ['Pull-up', 'Pull-up bar'], ['Dip', 'Dip station'], ['Parallettes', 'Parallettes'],
      ['vest', 'Weighted vest'], ['Band', 'Bands'], ['Rings', 'Rings']], H.exFlt.eq) +
      '</select></label></div>' +
      '<div class="row"><button class="pill' + (H.exFlt.hero ? ' on' : '') +
      '" id="exhero">Hero lifts only</button>' +
      '<span class="right sm muted" id="excount"></span></div></div>' +
      '<div id="exList"></div>' +
      '<button class="b o" data-nav="training" style="margin-top:16px">&larr; Training</button></div>';
  };

  /* ============================================================ FINANCIAL */
  V.financial = function (sub) {
    if (sub === 'purchases') return V.purchases();
    if (sub === 'actual') return V.actual();

    var st = S();
    var mode = st.fin.costMode || 'real', path = st.fin.path || 'rent';
    var inc = H.finIncome('both', mode), cost = H.finCost(mode, path);
    var gap = inc - cost;

    var bySection = {};
    st.fin.costs.forEach(function (c) {
      if (c.section === 'Housing (rent)' && path === 'buy') return;
      if (c.section === 'Housing (buy)' && path !== 'buy') return;
      bySection[c.section] = (bySection[c.section] || 0) + (c[mode] || 0);
    });
    var scen = Object.keys(st.fin.scenarios || {});

    return '<div class="page"><div class="phead"><h1>Financial</h1>' +
      '<p>Planning on the left, what actually happened on the right. Seeded from the ' +
      'Moving In workbook.</p></div>' +

      '<div class="sec"><div class="spread"><h2>The plan</h2>' +
      '<div class="row"><button class="b o s" data-nav="financial/actual">Actual earnings</button>' +
      '<button class="b o s" data-nav="financial/purchases">Big purchases</button></div></div>' +
      '<div class="card pad"><div class="fr">' +
      '<label class="f"><span>Scenario</span><select id="finMode">' +
      H.opt([['low', 'Lean (low estimates)'], ['real', 'Realistic'],
      ['high', 'Good month (high)'], ['actual', 'Actual / researched']], mode) + '</select></label>' +
      '<label class="f"><span>Housing path</span><select id="finPath">' +
      H.opt([['rent', 'Renting'], ['buy', 'Buying']], path) + '</select></label>' +
      '<label class="f"><span>Saved scenarios</span><select id="finScen">' +
      H.opt([['', '— pick —']].concat(scen.map(function (s) { return [s, s]; })), '') +
      '</select></label></div>' +
      '<div class="row"><button class="b o s" id="scenSave">Save this as a scenario</button>' +
      (scen.length ? '<button class="b o s dz" id="scenDel">Delete selected</button>' : '') +
      '</div></div>' +

      '<div class="stats" style="margin-top:14px">' +
      H.stat(money0(inc), 'Income / mo') +
      H.stat(money0(cost), 'Costs / mo') +
      H.stat(money0(gap), gap >= 0 ? 'Surplus' : 'Shortfall', gap >= 0 ? 'acc' : 'bad') +
      H.stat(money0(gap * 12), 'Per year') + '</div>' +
      (gap < 0
        ? '<div class="note bad"><b>The gap is real.</b> At these numbers we are ' +
        money0(-gap) + ' short every month. Either income has to rise by that, or costs ' +
        'have to fall.</div>'
        : '') + '</div>' +

      '<div class="sec"><h2>Where the money goes</h2><div class="grid g2">' +
      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">By section</h3>' +
      Object.keys(bySection).sort(function (a, b) { return bySection[b] - bySection[a]; })
        .map(function (k) {
          var p = cost ? bySection[k] / cost * 100 : 0;
          return '<div class="mrow"><div class="spread"><span>' + E(k) + '</span>' +
            '<em>' + money0(bySection[k]) + '</em></div>' +
            '<div class="bar"><i class="pk" data-w="' + p.toFixed(1) + '"></i></div></div>';
        }).join('') + '</div>' +

      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:12px">Income by person</h3>' +
      ['Jaron', 'Aaliyah', 'Both'].map(function (w) {
        var v = st.fin.jobs.filter(function (j) { return j.who === w; })
          .reduce(function (a, j) { return a + (j[mode] || 0); }, 0);
        if (!v) return '';
        var p = inc ? v / inc * 100 : 0;
        return '<div class="mrow"><div class="spread">' +
          '<span>' + E(w === 'Both' ? 'Shared / gig' : H.nameOf(w)) + '</span>' +
          '<em>' + money0(v) + '</em></div>' +
          '<div class="bar"><i class="pp" data-w="' + p.toFixed(1) + '"></i></div></div>';
      }).join('') +
      '<button class="b o s" id="jobAdd" style="margin-top:10px">Add a job or income</button>' +
      '</div></div></div>' +

      '<div class="sec"><div class="spread"><h2>Income lines</h2>' +
      '<button class="b o s" id="jobAdd2">Add</button></div><div class="tw"><table>' +
      '<thead><tr><th>Who</th><th>Name</th><th>Employer</th><th>Low</th><th>Realistic</th>' +
      '<th>High</th><th></th></tr></thead><tbody>' +
      st.fin.jobs.map(function (j) {
        return '<tr><td><span class="chip">' + E(H.nameOf(j.who)) + '</span></td>' +
          '<td><b>' + E(j.name) + '</b></td><td class="sm muted">' + E(j.employer || '') + '</td>' +
          '<td class="num">' + money0(j.low) + '</td><td class="num"><b>' + money0(j.real) + '</b></td>' +
          '<td class="num">' + money0(j.high) + '</td>' +
          '<td><button class="b o s" data-jobe="' + E(j.id) + '">Edit</button></td></tr>';
      }).join('') + '</tbody></table></div></div>' +

      '<div class="sec"><div class="spread"><h2>Cost lines</h2>' +
      '<button class="b o s" id="costAdd">Add</button></div><div class="tw"><table>' +
      '<thead><tr><th>Section</th><th>Cost</th><th>Who</th><th>Low</th><th>Realistic</th>' +
      '<th>High</th><th>Actual</th><th></th></tr></thead><tbody>' +
      st.fin.costs.map(function (c) {
        return '<tr><td class="sm muted">' + E(c.section) + '</td>' +
          '<td><b>' + E(c.name) + '</b></td>' +
          '<td><span class="chip">' + E(H.nameOf(c.who)) + '</span></td>' +
          '<td class="num">' + money0(c.low) + '</td><td class="num"><b>' + money0(c.real) + '</b></td>' +
          '<td class="num">' + money0(c.high) + '</td>' +
          '<td class="num">' + (c.actual ? money0(c.actual) : '—') + '</td>' +
          '<td><button class="b o s" data-coste="' + E(c.id) + '">Edit</button></td></tr>';
      }).join('') + '</tbody></table></div></div></div>';
  };

  V.actual = function () {
    var st = S();
    var from = H.addDays(H.today(), -90);
    var shifts = st.fin.shifts.slice().sort(function (a, b) { return b.date < a.date ? -1 : 1; });
    function tot(who, field) {
      return H.shiftsFor(who, from).reduce(function (a, s) { return a + (s[field] || 0); }, 0);
    }
    var months = 90 / 30.4;
    var months6 = H.monthlyEarnings(6);
    var anyEarnings = months6.some(function (m) { return m.net > 0; });

    return '<div class="page"><div class="phead"><h1>Actual earnings</h1>' +
      '<p>Log real shifts. Averages, effective hourly and after-tax rate all come from ' +
      'what actually landed, not the plan.</p></div>' +
      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b" id="shAdd">Log a shift</button>' +
      '<button class="b o" id="shCsv">Export shifts</button>' +
      '<button class="b o" data-nav="financial">&larr; Plan</button></div>' +

      '<div class="sec"><h2>Last 90 days</h2><div class="grid g2">' +
      ['Jaron', 'Aaliyah'].map(function (w) {
        var h = tot(w, 'hours'), g = tot(w, 'gross'), n = tot(w, 'net');
        return '<div class="card pad"><h3 style="font-size:16px;margin-bottom:12px">' +
          E(H.nameOf(w)) + '</h3><div class="stats">' +
          H.stat(money0(n / months), 'Net / mo', 'acc') +
          H.stat(h.toFixed(0), 'Hours') +
          H.stat(money(h > 0 ? g / h : 0), 'Gross / hr') +
          H.stat(money(h > 0 ? n / h : 0), 'Net / hr') + '</div>' +
          '<p class="sm muted" style="margin-top:10px">' +
          (g > 0 ? 'Take-home is ' + Math.round(n / g * 100) + '% of gross.' : 'No shifts logged yet.') +
          '</p></div>';
      }).join('') + '</div>' +
      '<div class="note" style="margin-top:14px"><b>Auto scenario.</b> Combined that is <b>' +
      money0((tot('Jaron', 'net') + tot('Aaliyah', 'net')) / months) +
      '</b> net a month from real data, against a plan of <b>' +
      money0(H.finIncome('both', 'real')) + '</b>. ' +
      '<button class="b o s" id="scenFromActual" style="margin-left:8px">Save that as a scenario</button>' +
      '</div></div>' +

      (anyEarnings
        ? '<div class="sec"><h2>Month by month</h2>' +
        '<p class="sub">Gross against what actually landed after tax. The table below carries ' +
        'the same numbers.</p>' +
        '<div class="card pad">' +
        H.barChart(months6.map(function (m) {
          return { label: m.label, v: { gross: m.gross, net: m.net } };
        }), [
          { key: 'gross', label: 'Gross', color: 'var(--s2)' },
          { key: 'net', label: 'Net', color: 'var(--s1)' }
        ], { label: 'Gross and net earnings by month', fmt: function (v) { return money0(v); } }) +
        '</div></div>'
        : '') +

      '<div class="sec"><h2>Shifts</h2>' +
      (shifts.length
        ? '<div class="tw"><table><thead><tr><th>Date</th><th>Job</th><th>Hours</th>' +
        '<th>Gross</th><th>Net</th><th>Note</th><th></th></tr></thead><tbody>' +
        shifts.slice(0, 80).map(function (s) {
          var j = null;
          st.fin.jobs.forEach(function (x) { if (x.id === s.jobId) j = x; });
          return '<tr><td>' + E(H.shortD(s.date)) + '</td>' +
            '<td>' + E(j ? j.name : '?') + '</td><td class="num">' + s.hours + '</td>' +
            '<td class="num">' + money0(s.gross) + '</td><td class="num">' + money0(s.net) + '</td>' +
            '<td class="sm muted">' + E(s.note || '') + '</td>' +
            '<td><button class="x" data-shd="' + E(s.id) + '" aria-label="Delete">&times;</button></td></tr>';
        }).join('') + '</tbody></table></div>'
        : H.empty('No shifts logged.', 'Log one and the numbers above start coming from real data.',
          '<button class="b" id="shAdd2">Log a shift</button>')) +
      '</div></div>';
  };

  V.purchases = function () {
    var P_ = S().fin.purchases || {}, names = Object.keys(P_);
    return '<div class="page"><div class="phead"><h1>Big purchases</h1>' +
      '<p>Houses, cars, anything worth comparing side by side before committing.</p></div>' +
      '<div class="row" style="margin-bottom:14px"><button class="b" id="bpNew">New list</button>' +
      '<button class="b o" data-nav="financial">&larr; Financial</button></div>' +
      (names.length
        ? names.map(function (n) {
          var L = P_[n];
          var cheapest = L.items.length
            ? L.items.reduce(function (a, b) { return (a.price || 0) <= (b.price || 0) ? a : b; })
            : null;
          return '<div class="sec"><div class="spread"><h2>' + E(n) +
            ' <span class="chip">' + E(L.cat || '') + '</span></h2>' +
            '<div class="row"><button class="b o s" data-bpadd="' + E(n) + '">Add item</button>' +
            '<button class="b o s dz" data-bpdel="' + E(n) + '">Delete list</button></div></div>' +
            (L.items.length
              ? '<div class="grid g3" data-stagger>' + L.items.map(function (it, i) {
                var isBest = cheapest && cheapest === it && L.items.length > 1;
                return '<div class="card pad"><div class="spread">' +
                  '<b style="font-family:var(--fd);font-size:16px">' + E(it.name) + '</b>' +
                  '<button class="x" data-bpi="' + E(n) + '|' + i + '" aria-label="Remove">&times;</button></div>' +
                  '<div style="font-size:22px;font-weight:700;color:var(--forest);margin:6px 0" class="num">' +
                  money0(it.price) + (isBest ? ' <span class="chip t">cheapest</span>' : '') + '</div>' +
                  (it.fields ? Object.keys(it.fields).map(function (k) {
                    return '<div class="spread sm" style="border-bottom:1px solid var(--line);padding:5px 0">' +
                      '<span class="muted">' + E(k) + '</span><b>' + E(it.fields[k]) + '</b></div>';
                  }).join('') : '') +
                  (it.notes ? '<p class="sm muted" style="margin-top:8px">' + E(it.notes) + '</p>' : '') +
                  (it.link ? '<a class="b o s" href="' + E(it.link) + '" target="_blank" ' +
                    'rel="noopener" style="margin-top:10px">Open link</a>' : '') +
                  '</div>';
              }).join('') + '</div>'
              : '<div class="empty sm">Nothing on this list yet.</div>') + '</div>';
        }).join('')
        : H.empty('No lists yet.',
          'Make one for apartments, or cars, or anything you are comparing.',
          '<button class="b" id="bpNew2">New list</button>')) +
      '</div>';
  };

  /* ============================================================ SCHEDULE */
  V.schedule = function (sub) {
    if (sub === 'week') return V.weekTemplate();
    var st = S();
    var first = new Date(H.calY, H.calM, 1);
    var start = first.getDay();
    var days = new Date(H.calY, H.calM + 1, 0).getDate();

    var cells = '';
    for (var i = 0; i < start; i++) cells += '<div class="day out"></div>';
    for (var dn = 1; dn <= days; dn++) {
      var ds = H.calY + '-' + H.p2(H.calM + 1) + '-' + H.p2(dn);
      var rec = st.days[ds];
      var ev = rec && rec.sched ? rec.sched.length : 0;
      var planned = (st.plan[ds] || []).length;
      cells += '<button class="day' + (ds === H.today() ? ' today' : '') +
        (ds === H.calSel ? ' sel' : '') + '" data-d="' + ds + '" ' +
        'aria-label="' + E(H.pretty(ds)) + '">' +
        '<span class="dn">' + dn + '</span><span class="dots">' +
        (rec && rec.meals.length ? '<i class="dot"></i>' : '') +
        (rec && rec.workout && rec.workout !== 'rest' ? '<i class="dot w"></i>' : '') +
        (ev ? '<i class="dot e"></i>' : '') + '</span>' +
        '<span class="dk">' + (planned ? planned + ' pl' : ev ? ev + ' ev' : '') + '</span></button>';
    }

    var d = H.dayLog(H.calSel);
    var t = H.dayTarget(st.who, d.workout);
    var got = H.eaten(H.calSel);
    var spend = H.daySpend(H.calSel);
    var blocks = H.freeBlocks(d, 60);
    var planned2 = st.plan[H.calSel] || [];
    var spendData = H.spendSeries(30);
    var anySpend = spendData.some(function (x) { return x.food || x.other; });

    return '<div class="page"><div class="phead"><h1>Schedule</h1>' +
      '<p>What each of us is doing, when we are both free, and what the day cost.</p></div>' +
      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b o" data-nav="schedule/week">Weekly template</button>' +
      '<button class="b o" id="applyTmpl">Apply template to this week</button>' +
      '<button class="b o" id="calCsv">Export the log</button></div>' +

      '<div class="card pad"><div class="spread" style="margin-bottom:12px">' +
      '<button class="b o s" id="cPrev" aria-label="Previous month">&larr;</button>' +
      '<h3>' + E(new Date(H.calY, H.calM, 1)
        .toLocaleDateString(undefined, { month: 'long', year: 'numeric' })) + '</h3>' +
      '<button class="b o s" id="cNext" aria-label="Next month">&rarr;</button></div>' +
      '<div class="cal">' + H.DOW.map(function (x) {
        return '<div class="dow">' + x + '</div>';
      }).join('') + cells + '</div>' +
      '<div class="row sm muted" style="margin-top:12px">' +
      '<span><i class="dot"></i> meals</span>' +
      '<span><i class="dot w"></i> training</span>' +
      '<span><i class="dot e"></i> plans</span></div></div>' +

      '<div class="sec"><h2>' + E(H.pretty(H.calSel)) + '</h2><div class="grid g2">' +
      '<div class="card pad"><div class="spread"><h3 style="font-size:15px">Plans</h3>' +
      '<button class="b o s" id="evAdd">Add</button></div>' +
      ((d.sched || []).length
        ? '<div style="margin-top:10px">' + d.sched.map(function (ev, i) {
          return '<div class="gitem"><span class="chip' + (ev.who === 'Aaliyah' ? ' t' : '') + '">' +
            E(H.nameOf(ev.who)) + '</span>' +
            '<div style="flex:1"><div class="gn">' + E(ev.what) + '</div>' +
            '<div class="gq">' + E(ev.from || '') + (ev.to ? ' – ' + E(ev.to) : '') +
            (ev.where ? ' &middot; ' + E(ev.where) : '') + '</div></div>' +
            '<button class="x" data-evd="' + i + '" aria-label="Remove">&times;</button></div>';
        }).join('') + '</div>'
        : '<div class="empty sm">Nothing planned.</div>') +
      (blocks === null ? ''
        : blocks.length
          ? '<div class="note" style="margin-top:12px"><b>Both free.</b> ' +
          blocks.map(function (b) { return H.fmtMin(b[0]) + ' to ' + H.fmtMin(b[1]); }).join(', ') +
          '</div>'
          : '<div class="note warn" style="margin-top:12px">No overlapping free time today.</div>') +
      '</div>' +

      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:10px">The day</h3>' +
      '<label class="f"><span>Training</span><select id="schWorkout">' +
      Object.keys(H.TRAIN).map(function (k) {
        return '<option value="' + k + '"' + (d.workout === k ? ' selected' : '') + '>' +
          E(H.TRAIN[k].n) + '</option>';
      }).join('') + '</select></label>' +
      H.bar('Calories', got.kcal, t.kcal, 'pk') +
      H.bar('Protein', got.p, t.p, 'pp') +
      (planned2.length
        ? '<div class="note" style="margin:12px 0"><b>Planned.</b> ' +
        planned2.map(function (m) {
          var r = H.byId(m.id);
          return r ? E(r.n) : '';
        }).filter(Boolean).join(', ') +
        ' <button class="b o s" id="logPlannedDay" style="margin-left:6px">Log it</button></div>'
        : '') +
      '<div class="spread sm" style="margin-top:12px"><span class="muted">Food logged</span>' +
      '<b class="num">' + money(spend.food) + '</b></div>' +
      '<div class="spread sm"><span class="muted">Other spend</span>' +
      '<b class="num">' + money(spend.other) + '</b></div>' +
      '<div class="spread" style="margin-top:6px;padding-top:8px;border-top:1px solid var(--line)">' +
      '<span><b>Day total</b></span>' +
      '<b class="num" style="color:var(--forest)">' + money(spend.total) + '</b></div>' +
      '<div class="row" style="margin-top:12px">' +
      '<button class="b o s" id="spAdd">Log a spend</button>' +
      '<button class="b o s" id="mealAdd">Log a meal</button></div>' +
      ((d.meals || []).length
        ? '<div style="margin-top:10px">' + d.meals.map(function (m, i) {
          var r = H.byId(m.id);
          if (!r) return '';
          return '<div class="spread sm" style="padding:5px 0;border-bottom:1px solid var(--line)">' +
            '<span>' + E(r.n) + (m.q !== 1 ? ' ×' + m.q : '') + '</span>' +
            '<span><b class="num">' + Math.round(r.k * (m.q || 1)) + '</b> ' +
            '<button class="x" data-mld="' + i + '" aria-label="Remove">&times;</button></span></div>';
        }).join('') + '</div>'
        : '') +
      ((d.spend || []).length
        ? '<div style="margin-top:10px">' + d.spend.map(function (x, i) {
          return '<div class="spread sm" style="padding:5px 0;border-bottom:1px solid var(--line)">' +
            '<span>' + E(x.what) + ' <span class="chip">' + E(H.nameOf(x.who || 'Both')) + '</span></span>' +
            '<span><b class="num">' + money(x.amt) + '</b> ' +
            '<button class="x" data-spd="' + i + '" aria-label="Remove">&times;</button></span></div>';
        }).join('') + '</div>'
        : '') +
      '</div></div></div>' +

      (anySpend
        ? '<div class="sec"><h2>Spending, last 30 days</h2>' +
        '<p class="sub">Food comes from the meals logged that day; other spend is what was ' +
        'entered by hand.</p><div class="card pad">' +
        H.barChart(spendData.filter(function (_, i) { return i % 2 === 0; }).map(function (x) {
          return { label: H.shortD(x.x).split(' ')[1], v: { food: x.food, other: x.other } };
        }), [
          { key: 'food', label: 'Food', color: 'var(--s1)' },
          { key: 'other', label: 'Other', color: 'var(--s3)' }
        ], { label: 'Daily spending over the last 30 days', fmt: function (v) { return money(v); } }) +
        '</div></div>'
        : '') +
      '</div>';
  };

  V.weekTemplate = function () {
    var t = S().sched.tmpl || {};
    return '<div class="page"><div class="phead"><h1>Weekly template</h1>' +
      '<p>The normal week. Put the regular stuff here once, then push it onto the ' +
      'calendar whenever.</p></div>' +
      '<div class="row" style="margin-bottom:14px">' +
      '<button class="b o" data-nav="schedule">&larr; Calendar</button>' +
      '<button class="b" id="applyTmpl2">Apply to this week</button></div>' +
      '<div class="grid g3" data-stagger>' + H.DOW.map(function (dn, i) {
        var items = t[i] || [];
        return '<div class="card pad"><div class="spread"><h3 style="font-size:16px">' + dn + '</h3>' +
          '<button class="b o s" data-tadd="' + i + '">Add</button></div>' +
          (items.length
            ? '<div style="margin-top:10px">' + items.map(function (x, j) {
              return '<div class="gitem" style="padding:8px 0">' +
                '<span class="chip' + (x.who === 'Aaliyah' ? ' t' : '') + '">' +
                E(H.nameOf(x.who)) + '</span>' +
                '<div style="flex:1"><div class="gn" style="font-size:13.5px">' + E(x.what) + '</div>' +
                '<div class="gq">' + E(x.from || '') + (x.to ? ' – ' + E(x.to) : '') + '</div></div>' +
                '<button class="x" data-td="' + i + '|' + j + '" aria-label="Remove">&times;</button></div>';
            }).join('') + '</div>'
            : '<p class="empty sm" style="padding:16px 0">Nothing regular.</p>') + '</div>';
      }).join('') + '</div></div>';
  };

  /* ============================================================ SETTINGS */
  V.settings = function () {
    var st = S();
    var use = H.storageUsed();
    var since = H.daysSinceExport();

    return '<div class="page"><div class="phead"><h1>Profile and settings</h1>' +
      '<p>The numbers every target in the app is calculated from, and where the data lives.</p></div>' +

      '<div class="sec"><h2>Profiles</h2>' +
      '<p class="sub">Calories, protein and water targets all come from these. Change one and ' +
      'every page updates.</p>' +
      '<div class="grid g2">' + ['j', 'a'].map(function (k) {
        var p = st.prof[k], c = H.calc(p);
        return '<div class="card pad"><div class="spread" style="margin-bottom:12px">' +
          '<h3 style="font-size:17px">' + E(p.name) + '</h3>' +
          '<button class="b o s" data-prof="' + k + '">Edit</button></div>' +
          '<div class="stats">' +
          H.stat(c.kcal.toLocaleString(), 'Kcal / day', 'acc') +
          H.stat(c.p + 'g', 'Protein') +
          H.stat(c.tdee.toLocaleString(), 'TDEE') +
          H.stat(c.ffmi, 'FFMI') + '</div>' +
          '<div class="sm muted" style="margin-top:12px">' +
          p.w + ' lb &middot; ' + Math.floor(p.h / 12) + '′' + (p.h % 12) + '″ &middot; ' +
          p.age + ' &middot; ' + p.bf + '% body fat &middot; ' + p.pf + ' g protein per lb</div>' +
          '<div class="sm muted">Resting ' + c.rmr.toLocaleString() + ' kcal, Katch-McArdle ' +
          c.katch.toLocaleString() + '. At this intake, about <b>' +
          (c.rate >= 0 ? '+' : '') + c.rate.toFixed(1) + ' lb a week</b>.</div></div>';
      }).join('') + '</div></div>' +

      '<div class="sec"><h2>Your data</h2><div class="grid g2">' +
      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:6px">Backup</h3>' +
      '<p class="sm muted">Everything lives in this browser on this device. Nothing is uploaded ' +
      'and there is no account, so the save file is the only copy that survives clearing ' +
      'site data.</p>' +
      '<div class="row" style="margin-top:12px">' +
      '<button class="b" id="setExport">Save to file</button>' +
      '<button class="b o" id="setImport">Load a file</button></div>' +
      '<p class="sm muted" style="margin-top:12px">' +
      (since == null ? 'Never exported.'
        : since === 0 ? 'Last exported today.'
          : 'Last exported ' + since + ' day' + (since === 1 ? '' : 's') + ' ago.') + '</p>' +
      H.switchRow('setRemind', 'Remind me to back up',
        'A nudge once a week if the save file is getting stale.', st.prefs.remindBackup) +
      '</div>' +

      '<div class="card pad"><h3 style="font-size:15px;margin-bottom:6px">Storage</h3>' +
      '<p class="sm muted">Browsers cap this at roughly 5 MB. Photos are the only thing big ' +
      'enough to matter; they are downscaled to 900 px on the way in.</p>' +
      '<div class="mrow" style="margin-top:14px"><div class="spread">' +
      '<span>Used</span><em>' + use.mb.toFixed(2) + ' MB of about 5</em></div>' +
      '<div class="bar"><i class="' + (use.pct > 80 ? 'pbad' : 'pk') +
      '" data-w="' + use.pct.toFixed(1) + '"></i></div></div>' +
      '<div class="stats" style="margin-top:14px">' +
      H.stat(Object.keys(st.photos).length, 'Photos') +
      H.stat(Object.keys(st.days).length, 'Logged days') +
      H.stat(st.mine.length, 'My recipes') +
      H.stat(Object.keys(st.ingOv).length, 'Price edits') + '</div>' +
      '<div class="row" style="margin-top:14px">' +
      (Object.keys(st.photos).length ? '<button class="b o dz" id="setDropPhotos">Remove all photos</button>' : '') +
      '<button class="b o dz" id="setReset">Start over</button></div></div></div></div>' +

      '<div class="sec"><h2>Appearance and behaviour</h2><div class="card pad">' +
      '<label class="f"><span>Theme</span><select id="setTheme">' +
      H.opt([['auto', 'Match the system'], ['light', 'Always light'], ['dark', 'Always dark']],
        st.theme) + '</select></label>' +
      '<label class="f"><span>Default meals a day when planning</span><select id="setSlots">' +
      H.opt([[2, '2'], [3, '3'], [4, '4']], st.prefs.planSlots) + '</select></label>' +
      '<label class="f"><span>Daily food budget for planning</span>' +
      '<input id="setBudget" type="number" step="0.5" min="0" placeholder="no limit" value="' +
      E(st.prefs.dayBudget == null ? '' : st.prefs.dayBudget) + '">' +
      '<span class="hint">Used as the default when a plan is generated.</span></label>' +
      '</div></div>' +

      '<div class="sec"><h2>Recipe lists</h2>' +
      '<p class="sub">Saved groups of recipes — a Sunday prep set, a rotation, whatever is ' +
      'worth keeping together.</p>' +
      (Object.keys(st.lists).length
        ? '<div class="grid g3" data-stagger>' + Object.keys(st.lists).sort().map(function (n) {
          var ids = st.lists[n];
          var recipes = ids.map(H.byId).filter(Boolean);
          var kcal = recipes.reduce(function (a, r) { return a + r.k; }, 0);
          var cost = recipes.reduce(function (a, r) { return a + H.cps(r); }, 0);
          return '<div class="card pad"><div class="spread">' +
            '<h3 style="font-size:16px">' + E(n) + '</h3>' +
            '<button class="x" data-listdel="' + E(n) + '" aria-label="Delete list">&times;</button></div>' +
            '<div class="sm muted" style="margin:6px 0 10px">' + recipes.length + ' recipes &middot; ' +
            Math.round(kcal) + ' kcal &middot; ' + money(cost) + '</div>' +
            recipes.slice(0, 6).map(function (r) {
              return '<div class="spread sm" style="padding:4px 0"><a href="#/r/' + E(r.id) + '">' +
                E(r.n) + '</a><span class="muted num">' + Math.round(r.k) + '</span></div>';
            }).join('') +
            (recipes.length > 6 ? '<div class="xs muted" style="margin-top:6px">and ' +
              (recipes.length - 6) + ' more</div>' : '') +
            '<div class="row" style="margin-top:12px">' +
            '<button class="b o s" data-listshop="' + E(n) + '">Add all to shopping</button></div>' +
            '</div>';
        }).join('') + '</div>'
        : H.empty('No recipe lists yet.',
          'Open a recipe and use "Add to a list" to start one.')) +
      '</div>' +

      '<div class="sec"><h2>Keyboard</h2><div class="card pad">' +
      '<div class="swrow"><div class="t"><b>Search everything</b>' +
      '<span>Recipes, exercises, pages and actions in one box.</span></div>' +
      '<span><kbd>Ctrl</kbd> <kbd>K</kbd></span></div>' +
      '<div class="swrow"><div class="t"><b>Switch person</b>' +
      '<span>Flip between the two profiles.</span></div><span><kbd>Ctrl</kbd> <kbd>⇧</kbd> <kbd>P</kbd></span></div>' +
      '<div class="swrow"><div class="t"><b>Sections</b>' +
      '<span>Jump straight to a tab.</span></div>' +
      '<span><kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> <kbd>4</kbd> <kbd>5</kbd></span></div>' +
      '<div class="swrow"><div class="t"><b>Close a dialog</b><span>Anywhere.</span></div>' +
      '<span><kbd>Esc</kbd></span></div></div></div>' +
      '</div>';
  };

})(typeof window !== 'undefined' ? window : globalThis);
