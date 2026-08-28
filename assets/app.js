/* ============================================================
   The Handbook - router and wiring

   Owns the URL, decides which view renders, and binds every
   control on it. All the writes to state happen here.
   ============================================================ */
(function (global) {
  'use strict';

  var H = global.Handbook;
  var $ = H.$, $$ = H.$$, on = H.on, E = H.E, money = H.money, money0 = H.money0;
  var toast = H.toast, modal = H.modal, form = H.form, opt = H.opt;
  var V = H.views;

  function S() { return H.state(); }

  /* ---------------------------------------------------------- chrome */
  var NAV = [
    ['meals', 'Meals'], ['training', 'Training'], ['shopping', 'Shopping'],
    ['financial', 'Financial'], ['schedule', 'Schedule']
  ];
  H.NAV = NAV;

  var ICO = {
    meals: '<path d="M4 3v8a3 3 0 006 0V3M7 11v10M16 3c-1.5 2-2 4-2 6s.5 3 2 3 2-1 2-3-.5-4-2-6zM16 12v9"/>',
    training: '<path d="M6 8v8M18 8v8M3 10v4M21 10v4M6 12h12"/>',
    shopping: '<path d="M3 4h2l2 12h11M7 8h14l-2 6H8"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/>',
    financial: '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>',
    schedule: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'
  };

  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg>';
  var AUTO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 3v18" /><path d="M12 3a9 9 0 010 18z" fill="currentColor" stroke="none"/></svg>';

  function chrome() {
    $('#tabs').innerHTML = NAV.map(function (t) {
      return '<button class="tab" data-v="' + t[0] + '" data-nav="' + t[0] + '">' + t[1] + '</button>';
    }).join('');
    $('#btm').innerHTML = NAV.map(function (t) {
      return '<button data-v="' + t[0] + '" data-nav="' + t[0] + '" aria-label="' + t[1] + '">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" ' +
        'stroke-linejoin="round" aria-hidden="true">' + ICO[t[0]] + '</svg>' +
        '<span>' + t[1] + '</span></button>';
    }).join('');
    drawWho();
    drawTheme();
  }

  function drawWho() {
    $('#who').innerHTML = ['j', 'a'].map(function (k) {
      return '<button data-w="' + k + '"' + (S().who === k ? ' class="on"' : '') +
        ' aria-pressed="' + (S().who === k) + '">' + E(S().prof[k].name) + '</button>';
    }).join('');
  }

  /* ---------------------------------------------------------- theme */
  function applyTheme() {
    var pref = S().theme || 'auto';
    var dark = pref === 'dark' || (pref === 'auto' && global.matchMedia &&
      global.matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    var meta = document.querySelector('meta[name="theme-color"]:not([media])');
    if (!meta) {
      meta = document.createElement('meta');
      meta.name = 'theme-color';
      document.head.appendChild(meta);
    }
    meta.content = dark ? '#16160F' : '#FBFAF7';
    drawTheme();
  }
  H.applyTheme = applyTheme;

  function drawTheme() {
    var btn = $('#themeBtn');
    if (!btn) return;
    var pref = S().theme || 'auto';
    btn.innerHTML = pref === 'dark' ? MOON : pref === 'light' ? SUN : AUTO;
    btn.title = 'Theme: ' + (pref === 'auto' ? 'matching the system' : pref);
  }

  if (global.matchMedia) {
    var mq = global.matchMedia('(prefers-color-scheme: dark)');
    var onScheme = function () { if ((S().theme || 'auto') === 'auto') applyTheme(); };
    if (mq.addEventListener) mq.addEventListener('change', onScheme);
    else if (mq.addListener) mq.addListener(onScheme);
  }

  /* ---------------------------------------------------------- router */
  H.calY = new Date().getFullYear();
  H.calM = new Date().getMonth();
  H.calSel = H.today();
  H.planCursor = H.today();

  var scrollByRoute = {};
  var lastRoute = null;

  function parse() {
    var h = (location.hash || '#/meals').slice(2).split('/');
    return { v: h[0] || 'meals', sub: h[1] || '', rest: h.slice(2) };
  }

  function viewHTML(r) {
    switch (r.v) {
      case 'r': return V.recipe(r.sub);
      case 'plan': return V.plan();
      case 'training': return V.training(r.sub);
      case 'shopping': return V.shopping(r.sub);
      case 'financial': return V.financial(r.sub);
      case 'schedule': return V.schedule(r.sub);
      case 'settings': return V.settings();
      default: return V.meals();
    }
  }

  /* scroll-behavior:smooth makes programmatic scrolling animate, which turns a
     "stay exactly where you are" repaint into a visible drift. These jumps are
     always instant. */
  function jump(y) {
    try { global.scrollTo({ top: y, left: 0, behavior: 'instant' }); }
    catch (e) { global.scrollTo(0, y); }
  }

  function paint(r, keepScroll) {
    var main = $('#view');
    var y = global.scrollY || 0;
    main.innerHTML = viewHTML(r);

    $$('.tab,.btmnav button').forEach(function (b) {
      var active = b.dataset.v === (r.v === 'r' || r.v === 'plan' ? 'meals' : r.v);
      b.classList.toggle('on', active);
      if (active) b.setAttribute('aria-current', 'page');
      else b.removeAttribute('aria-current');
    });
    $$('#who button').forEach(function (b) {
      b.classList.toggle('on', b.dataset.w === S().who);
      b.setAttribute('aria-pressed', b.dataset.w === S().who);
    });
    $$('[data-stagger]').forEach(H.stagger);
    H.fillBars(main);

    if (keepScroll) jump(y);
    bind(r);
  }

  /* A fresh route scrolls to the top and restores where you were if you are
     going back; a refresh in place must not move the page at all, which is what
     made ticking a shopping item so annoying before. */
  function route() {
    var r = parse();
    var key = r.v + '/' + r.sub;
    if (lastRoute && lastRoute !== key) scrollByRoute[lastRoute] = global.scrollY || 0;

    var render = function () { paint(r, false); };
    if (document.startViewTransition && lastRoute !== key) {
      document.startViewTransition(render);
    } else {
      render();
    }

    if (lastRoute !== key) {
      var restore = scrollByRoute[key] || 0;
      requestAnimationFrame(function () { jump(restore); });
    }
    lastRoute = key;
  }

  function refresh() { paint(parse(), true); }
  H.refresh = refresh;

  function nav(p) {
    if (('#/' + p) === location.hash) { refresh(); return; }
    location.hash = '#/' + p;
  }
  H.nav = nav;

  global.addEventListener('hashchange', route);

  /* ---------------------------------------------------------- per-view */
  function bind(r) {
    if (r.v === 'meals') bindMeals();
    else if (r.v === 'r') bindRecipe(r.sub);
    else if (r.v === 'plan') bindPlan();
    else if (r.v === 'shopping') {
      if (r.sub === 'ingredients') bindIngredients();
      else if (r.sub === 'pantry') bindPantry();
      else bindShop();
    }
    else if (r.v === 'training') {
      if (r.sub === 'exercises') bindExercises();
      else bindTraining();
    }
    else if (r.v === 'financial') bindFin(r.sub);
    else if (r.v === 'schedule') bindSched(r.sub);
    else if (r.v === 'settings') bindSettings();
  }

  function debounce(fn, ms) {
    var t = null;
    return function () {
      var a = arguments, self = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, a); }, ms);
    };
  }

  /* ---------------------------------------------------------- meals */
  function drawGrid() {
    var g = $('#fgrid');
    if (!g) return;
    var L = H.filtered();
    var shown = L.slice(0, H.flt.page * 48);
    g.innerHTML = shown.length
      ? shown.map(H.rcard).join('')
      : '<p class="empty">Nothing matches those filters.</p>';
    H.stagger(g);
    H.setText('#fcount', L.length + ' recipe' + (L.length === 1 ? '' : 's'));
    var more = $('#fmore');
    if (more) {
      more.innerHTML = shown.length < L.length
        ? '<button class="b o" id="fmoreBtn">Show ' +
        Math.min(48, L.length - shown.length) + ' more of ' + L.length + '</button>'
        : '';
      var b = $('#fmoreBtn');
      if (b) b.onclick = function () { H.flt.page++; drawGrid(); };
    }
  }

  function bindMeals() {
    drawGrid();
    on('#fq', 'input', debounce(function () {
      H.flt.q = this.value; H.flt.page = 1; drawGrid();
    }, 140));
    ['fcat', 'ftag', 'fsort'].forEach(function (id) {
      on('#' + id, 'change', function () {
        H.flt[id.slice(1)] = this.value; H.flt.page = 1; drawGrid();
      });
    });
    on('#clearFlt', 'click', function () {
      H.flt = { q: '', cat: '', tag: '', sort: 'rec', page: 1 };
      refresh();
    });
    on('#costMode', 'change', function () {
      S().prefs.costMode = this.value; H.save(); refresh();
    });
    on('#bothCost', 'click', function () {
      var w = H.dayLog(H.today()).workout;
      var a = H.estDayCost(H.dayTarget('j', w), S().prefs.costMode);
      var b = H.estDayCost(H.dayTarget('a', w), S().prefs.costMode);
      $('#bothOut').innerHTML = '<div class="note" style="margin-bottom:0"><b>Both of us.</b> ' +
        money(a.byKcal) + ' for ' + E(S().prof.j.name) + ' plus ' + money(b.byKcal) + ' for ' +
        E(S().prof.a.name) + ' is <b>' + money(a.byKcal + b.byKcal) + ' a day</b>, ' +
        money((a.byKcal + b.byKcal) * 30) + ' a month.</div>';
    });
    on('#addOwn', 'click', ownRecipe);
    on('#logPlanned', 'click', function () { logPlanned(H.today()); });
  }

  function logPlanned(ds) {
    var planned = H.planFor(ds);
    if (!planned.length) return;
    var log = H.dayLog(ds);
    planned.forEach(function (m) {
      log.meals.push({ id: m.id, q: m.q || 1 });
      H.consumeFromPantry(m.id, m.q || 1);
    });
    H.save(true);
    refresh();
    toast(planned.length + ' meals logged');
  }

  /* ---------------------------------------------------------- recipe */
  function drawIng(r, mult) {
    var el = $('#ingList');
    if (!el) return;
    el.innerHTML = (r.ing || []).map(function (i) {
      var meas = i[0], key = i[1], g = i[2] || 0, q = H.ING(key);
      var nm = q ? q.n : meas;
      var pr = q ? (g * mult / 100) * H.best(q) : 0;
      var gs = g ? Math.round(g * mult) + ' g' : '';
      var sub = (q && meas) ? ' <span class="muted xs">(' + E(meas) + ')</span>' : '';
      return '<li><b>' + gs + '</b><span>' + E(nm) + sub + '</span>' +
        (pr ? '<span class="c">' + money(pr) + '</span>' : '') + '</li>';
    }).join('');

    var sv = (r.sv || 1) * mult;
    var nice = function (x) { return Math.round(x * 10) / 10; };
    var t = H.ctot(r) * mult;
    H.setText('#svLabel', 'for ' + nice(sv) + ' serving' + (sv === 1 ? '' : 's'));
    H.setText('#svHero', nice(sv));
    H.setText('#totHero', money(t));
    H.setText('#batchSv', nice(sv));
    var a = $('#batchAll');
    if (a) {
      a.textContent = Math.round(r.k * sv) + ' kcal, ' + Math.round(r.p * sv) +
        ' g protein, ' + Math.round(r.c * sv) + ' g carbs, ' + Math.round(r.f * sv) +
        ' g fat, ' + money(t);
    }
  }

  function bindRecipe(id) {
    var r = H.byId(id);
    if (!r) return;
    drawIng(r, 1);
    $$('[data-scale]').forEach(function (b) {
      b.onclick = function () {
        $$('[data-scale]').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        drawIng(r, parseFloat(b.dataset.scale));
      };
    });
    // Ticking steps is per-visit rather than stored: it is a cooking aid, not data.
    var list = $('#stepList');
    if (list) {
      list.addEventListener('click', function (e) {
        var li = e.target.closest('li[data-step]');
        if (li) li.classList.toggle('done');
      });
    }
  }

  /* ---------------------------------------------------------- plan */
  function readPlanOpts() {
    var o = H.planOpts;
    if ($('#pFrom')) H.planCursor = $('#pFrom').value || H.today();
    if ($('#pDays')) o.days = +$('#pDays').value;
    if ($('#pSlots')) o.slots = +$('#pSlots').value;
    if ($('#pBudget')) o.budget = $('#pBudget').value;
    if ($('#pMax')) o.maxMinutes = $('#pMax').value;
    if ($('#pVar')) o.variety = +$('#pVar').value;
    return o;
  }

  function generate() {
    var o = readPlanOpts();
    var res = H.generatePlan({
      from: H.planCursor,
      days: o.days,
      slots: o.slots,
      who: S().who,
      budget: o.budget === '' ? null : H.num(o.budget),
      maxMinutes: o.maxMinutes === '' ? null : H.num(o.maxMinutes),
      favOnly: o.favOnly,
      variety: o.variety,
      seed: Date.now() & 0xffff
    });
    Object.keys(res.plan).forEach(function (ds) { S().plan[ds] = res.plan[ds]; });
    H.save(true);
    refresh();

    var missed = res.report.filter(function (d) { return d.err > 55; }).length;
    var over = res.report.filter(function (d) { return d.overBudget; }).length;
    var msg = o.days + ' days planned';
    if (over) msg += ', ' + over + ' over budget';
    else if (missed) msg += ', ' + missed + ' a way off target';
    else msg += ', all on target';
    toast(msg);
  }

  function bindPlan() {
    on('#pGen', 'click', generate);
    on('#pGen2', 'click', generate);
    on('#pFav', 'click', function () {
      H.planOpts.favOnly = !H.planOpts.favOnly;
      this.classList.toggle('on');
    });
    ['#pFrom', '#pDays', '#pSlots', '#pBudget', '#pMax', '#pVar'].forEach(function (s) {
      on(s, 'change', function () { readPlanOpts(); refresh(); });
    });
    on('#pClear', 'click', function () {
      H.confirmDanger({
        title: 'Clear the plan?',
        text: 'This removes the planned meals for these ' + H.planOpts.days +
          ' days. Anything already logged stays.',
        ok: 'Clear'
      }).then(function (ok) {
        if (!ok) return;
        for (var i = 0; i < H.planOpts.days; i++) delete S().plan[H.addDays(H.planCursor, i)];
        H.save(true);
        refresh();
        toast('Plan cleared');
      });
    });
    on('#pShop', 'click', buildListFromPlan);
    on('#pCsv', 'click', function () {
      var rows = [['Date', 'Slot', 'Recipe', 'Servings', 'Kcal', 'Protein', 'Cost']];
      H.planRange(H.planCursor, H.planOpts.days).forEach(function (d) {
        d.meals.forEach(function (m) {
          var rec = H.byId(m.id);
          if (!rec) return;
          rows.push([d.date, m.slot || '', rec.n, m.q || 1,
          Math.round(rec.k * (m.q || 1)), Math.round(rec.p * (m.q || 1)),
          (H.cps(rec) * (m.q || 1)).toFixed(2)]);
        });
      });
      H.dl('meal-plan-' + H.planCursor + '.csv', H.toCSV(rows), 'text/csv');
      toast('Plan exported');
    });

    $$('[data-swap]').forEach(function (b) {
      b.onclick = function () {
        var p = b.dataset.swap.split('|');
        swapMeal(p[0], +p[1]);
      };
    });
  }

  function swapMeal(ds, idx) {
    var meals = S().plan[ds] || [];
    var cur = meals[idx];
    if (!cur) return;
    var r = H.byId(cur.id);

    var m = modal('Swap ' + (r ? r.n : 'this meal'),
      '<div class="row" style="margin-bottom:12px">' +
      '<span class="muted sm">Servings</span>' +
      [0.5, 1, 1.5, 2].map(function (q) {
        return '<button class="pill' + ((cur.q || 1) === q ? ' on' : '') +
          '" data-q="' + q + '">' + q + '×</button>';
      }).join('') + '</div>' +
      '<label class="f"><span>Pick a different recipe</span>' +
      '<input id="swq" type="search" placeholder="Filter recipes..." autocomplete="off"></label>' +
      '<div class="picklist" id="swlist"></div>',
      '<button class="b o dz" id="swDel">Remove from the day</button>' +
      '<button class="b o" data-close>Done</button>', { focus: '#swq' });

    function draw(q) {
      q = (q || '').toLowerCase();
      var hits = H.all().filter(function (x) {
        return x.n.toLowerCase().indexOf(q) >= 0;
      }).slice(0, 60);
      $('#swlist', m).innerHTML = hits.map(function (x) {
        return '<button class="pickrow" data-r="' + E(x.id) + '">' +
          '<div style="flex:1"><b>' + E(x.n) + '</b>' +
          '<div class="xs muted">' + Math.round(x.k) + ' kcal &middot; ' + Math.round(x.p) +
          'g protein &middot; ' + money(H.cps(x)) + '</div></div>' +
          '<span class="b s">Use</span></button>';
      }).join('') || '<p class="empty sm">No match.</p>';
      $$('[data-r]', m).forEach(function (row) {
        row.onclick = function () {
          meals[idx] = { id: row.dataset.r, q: cur.q || 1, slot: cur.slot };
          H.save(true); m.close(); refresh(); toast('Swapped');
        };
      });
    }

    $$('[data-q]', m).forEach(function (b) {
      b.onclick = function () {
        cur.q = parseFloat(b.dataset.q);
        H.save(true); m.close(); refresh();
      };
    });
    $('#swDel', m).onclick = function () {
      meals.splice(idx, 1);
      H.save(true); m.close(); refresh(); toast('Removed');
    };
    $('#swq', m).oninput = function () { draw(this.value); };
    draw('');
  }

  function buildListFromPlan() {
    var res = H.shoppingFromPlan(H.planCursor, H.planOpts.days, { usePantry: true });
    if (!res.items.length) {
      toast('Nothing to buy — the pantry already covers this plan');
      return;
    }
    var total = res.items.reduce(function (a, i) { return a + i.price; }, 0);
    var name = 'Plan ' + H.shortD(H.planCursor);

    var m = modal('Build the shopping list',
      '<p class="sm muted" style="margin-top:0">' + res.items.length + ' ingredients across ' +
      H.planOpts.days + ' planned days, priced at the cheaper store, worth <b>' +
      money(total) + '</b>.' +
      (res.skipped.length ? ' ' + res.skipped.length + ' already covered by the pantry.' : '') +
      '</p>' +
      '<label class="f"><span>List name</span><input id="blName" value="' + E(name) + '"></label>' +
      '<label class="f"><span>What to do with what is already on that list</span>' +
      '<select id="blMode">' +
      opt([['replace', 'Replace it'], ['merge', 'Add to it']], 'replace') + '</select></label>' +
      (res.skipped.length
        ? '<div class="note"><b>Skipped.</b> ' +
        res.skipped.slice(0, 8).map(function (s) { return E(s.name); }).join(', ') +
        (res.skipped.length > 8 ? ' and ' + (res.skipped.length - 8) + ' more' : '') +
        ' — already in the pantry.</div>'
        : ''),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="blGo">Build it</button>', { focus: '#blName' });

    $('#blGo', m).onclick = function () {
      var nm = $('#blName', m).value.trim() || name;
      var mode = $('#blMode', m).value;
      var lists = H.shopLists();
      if (!lists[nm] || mode === 'replace') {
        lists[nm] = { cat: 'Groceries', fav: false, items: res.items };
      } else {
        res.items.forEach(function (it) {
          var ex = null;
          lists[nm].items.forEach(function (x) { if (x.key === it.key) ex = x; });
          if (ex) {
            ex.grams = (ex.grams || 0) + it.grams;
            ex.price = (ex.grams / 100) * H.best(H.ING(it.key));
            ex.note = Math.round(ex.grams) + ' g';
          } else lists[nm].items.push(it);
        });
      }
      S().shop.active = nm;
      H.save(true);
      m.close();
      nav('shopping');
      toast(res.items.length + ' items on "' + nm + '"');
    };
  }

  /* ---------------------------------------------------------- shopping */
  function bindShop() {
    on('#newList', 'click', function () {
      H.ask({ title: 'New list', label: 'Name', placeholder: 'Costco run' }).then(function (n) {
        if (!n) return;
        H.ask({
          title: 'Category', label: 'Category', value: 'Groceries',
          text: 'Lists are grouped by this on the Shopping page.'
        }).then(function (c) {
          S().shop.lists[n] = { cat: c || 'Lists', fav: false, items: [] };
          S().shop.active = n;
          H.save(true); refresh();
        });
      });
    });
    on('#listRename', 'click', function () {
      H.ask({ title: 'Rename list', label: 'Name', value: S().shop.active }).then(function (n) {
        if (!n || n === S().shop.active) return;
        var L = S().shop.lists;
        L[n] = L[S().shop.active];
        delete L[S().shop.active];
        S().shop.active = n;
        H.save(true); refresh();
      });
    });
    on('#listDup', 'click', function () {
      var n = S().shop.active + ' copy';
      while (S().shop.lists[n]) n += ' 2';
      S().shop.lists[n] = JSON.parse(JSON.stringify(H.curList()));
      S().shop.active = n;
      H.save(true); refresh();
      toast('Duplicated');
    });
    on('#listFav', 'click', function () {
      H.curList().fav = !H.curList().fav;
      H.save(); refresh();
    });
    on('#listDel', 'click', function () {
      if (Object.keys(S().shop.lists).length < 2) { toast('Keep at least one list'); return; }
      var name = S().shop.active;
      H.confirmDanger({
        title: 'Delete "' + name + '"?',
        text: 'The ' + H.curList().items.length + ' items on it go too.'
      }).then(function (ok) {
        if (!ok) return;
        var backup = S().shop.lists[name];
        delete S().shop.lists[name];
        S().shop.active = Object.keys(S().shop.lists)[0];
        H.save(true); refresh();
        toast('Deleted "' + name + '"', {
          action: 'Undo',
          onAction: function () {
            S().shop.lists[name] = backup;
            S().shop.active = name;
            H.save(true); refresh();
          }
        });
      });
    });
    on('#gClear', 'click', function () {
      var L = H.curList();
      var removed = L.items.filter(function (i) { return i.done; });
      if (!removed.length) { toast('Nothing checked'); return; }
      var before = L.items.slice();
      L.items = L.items.filter(function (i) { return !i.done; });
      H.save(true); refresh();
      toast(removed.length + ' cleared', {
        action: 'Undo',
        onAction: function () { H.curList().items = before; H.save(true); refresh(); }
      });
    });
    on('#gStock', 'click', function () {
      var n = H.stockFromList();
      if (!n) { toast('Nothing checked to move'); return; }
      toast(n + ' moved into the pantry');
      refresh();
    });
    on('#gAdd', 'click', function () {
      ingPicker(function (it) { H.curList().items.push(it); H.save(true); refresh(); });
    });
    on('#gRecipe', 'click', recipePicker);
    on('#gPlan', 'click', buildListFromPlan);
    on('#gPlan2', 'click', buildListFromPlan);
    on('#gTxt', 'click', shopTxt);
    on('#gCsv', 'click', shopCsv);
    on('#gSave', 'click', function () {
      H.dl('list-' + S().shop.active.replace(/[^a-z0-9]+/gi, '-').toLowerCase() + '.json',
        JSON.stringify({ app: 'handbook-list', name: S().shop.active, list: H.curList() }, null, 1),
        'application/json');
      toast('List saved');
    });
    on('#gLoad', 'click', function () {
      H.pickFile('.json', function (f) {
        var fr = new FileReader();
        fr.onload = function () {
          try {
            var o = JSON.parse(fr.result);
            var nm = o.name || 'Imported list';
            while (S().shop.lists[nm]) nm += ' 2';
            S().shop.lists[nm] = o.list || o;
            S().shop.active = nm;
            H.save(true); refresh();
            toast('List loaded');
          } catch (e) {
            toast('That is not a saved list file');
          }
        };
        fr.readAsText(f);
      });
    });
  }

  function shopTxt() {
    var L = H.curList(), byA = {};
    L.items.forEach(function (i) { (byA[i.aisle] = byA[i.aisle] || []).push(i); });
    var out = ['SHOPPING LIST  -  ' + S().shop.active, H.pretty(H.today()),
      'Best price of Walmart Fort Collins / Costco Timnath', ''];
    var tot = 0;
    H.AISLES.map(function (a) { return a[0]; }).concat(['Other']).forEach(function (a) {
      if (!byA[a]) return;
      out.push(a.toUpperCase());
      byA[a].forEach(function (i) {
        tot += i.price * i.qty;
        out.push('  [' + (i.done ? 'x' : ' ') + '] ' + i.name + '  -  ' +
          (i.note || '') + '   ' + money(i.price * i.qty));
      });
      out.push('');
    });
    out.push('TOTAL  ' + money(tot));
    H.dl('shopping-' + H.today() + '.txt', out.join('\n'));
  }

  function shopCsv() {
    var rows = [['List', 'Aisle', 'Item', 'Qty', 'Grams', 'Price', 'Store', 'Done']];
    H.curList().items.forEach(function (i) {
      rows.push([S().shop.active, i.aisle, i.name, i.qty, i.grams || '',
      i.price.toFixed(2), i.key ? H.bestStore(H.ING(i.key)) : '', i.done ? 'yes' : '']);
    });
    H.dl('shopping-' + H.today() + '.csv', H.toCSV(rows), 'text/csv');
  }

  function ingPicker(cb) {
    var keys = H.allIngKeys().sort(function (a, b) {
      return H.ING(a).n.localeCompare(H.ING(b).n);
    });
    var m = modal('Add to ' + S().shop.active,
      '<label class="f"><span>Search the ' + keys.length + ' ingredients we already have</span>' +
      '<input id="ipq" type="search" placeholder="Type to filter..." autocomplete="off"></label>' +
      '<div class="picklist" id="iplist" style="max-height:300px"></div>' +
      '<div class="note"><b>Not there?</b> Adding it below puts it in the master ingredient ' +
      'list permanently, not just this shop.</div>',
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="ipNew">Add a new ingredient</button>', { focus: '#ipq' });

    function draw(q) {
      q = (q || '').toLowerCase();
      var hits = keys.filter(function (k) {
        return H.ING(k).n.toLowerCase().indexOf(q) >= 0;
      }).slice(0, 60);
      $('#iplist', m).innerHTML = hits.map(function (k) {
        var g = H.ING(k);
        return '<button class="pickrow" data-k="' + E(k) + '"><div style="flex:1">' +
          '<b>' + E(g.n) + '</b><div class="xs muted">' + E(g.a || 'Other') + ' &middot; ' +
          money(H.best(g)) + '/100g at ' + E(H.bestStore(g)) + '</div></div>' +
          '<span class="b s">Add</span></button>';
      }).join('') || '<p class="empty sm">No match. Nothing by that name exists yet.</p>';
      $$('[data-k]', m).forEach(function (row) {
        row.onclick = function () {
          var k = row.dataset.k, g = H.ING(k);
          cb({
            key: k, name: g.n, qty: 1, price: H.best(g) * 2, grams: 200,
            note: 'about 200 g', aisle: g.a || 'Other', done: false
          });
          m.close();
          toast('Added ' + g.n);
        };
      });
    }
    $('#ipq', m).oninput = function () { draw(this.value); };
    $('#ipNew', m).onclick = function () { m.close(); ingEditor(null); };
    draw('');
  }

  function recipePicker() {
    var m = modal('Add a recipe to ' + S().shop.active,
      '<label class="f"><span>Search</span>' +
      '<input id="rpq" type="search" placeholder="Filter recipes..." autocomplete="off"></label>' +
      '<div class="picklist" id="rplist"></div>',
      '<button class="b" data-close>Done</button>',
      { focus: '#rpq', onClose: refresh });

    function draw(q) {
      q = (q || '').toLowerCase();
      var hits = H.all().filter(function (r) {
        return r.n.toLowerCase().indexOf(q) >= 0;
      }).slice(0, 70);
      $('#rplist', m).innerHTML = hits.map(function (r) {
        return '<button class="pickrow" data-r="' + E(r.id) + '"><div style="flex:1">' +
          '<b>' + E(r.n) + '</b><div class="xs muted">' + E(r.id) + ' &middot; makes ' + r.sv +
          ' &middot; ' + money(H.ctot(r)) + '</div></div><span class="b s">Add</span></button>';
      }).join('');
      $$('[data-r]', m).forEach(function (row) {
        row.onclick = function () {
          var n = H.addRecipeToShop(H.byId(row.dataset.r));
          toast(n + ' ingredients added');
        };
      });
    }
    $('#rpq', m).oninput = function () { draw(this.value); };
    draw('');
  }

  function shopItemEditor(idx) {
    var it = H.curList().items[idx];
    if (!it) return;
    var m = modal('Edit ' + it.name,
      form([{ id: 'sen', l: 'Name', v: it.name },
      { id: 'seq', l: 'Qty', t: 'number', step: '0.5', v: it.qty },
      { id: 'sep', l: 'Price each', t: 'number', step: '0.01', v: it.price },
      {
        id: 'sea', l: 'Aisle', t: 'select',
        o: H.AISLES.map(function (a) { return [a[0], a[0]]; }).concat([['Other', 'Other']]),
        v: it.aisle
      },
      { id: 'sen2', l: 'Note', v: it.note || '' }]) +
      (it.key ? '<p class="sm muted">Changing the price here only affects this list. To change ' +
        'it everywhere, edit it in the <a href="#/shopping/ingredients">ingredient list</a>.</p>' : ''),
      '<button class="b o dz" id="seDel">Remove</button>' +
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="seSave">Save</button>', { focus: '#sen' });

    $('#seDel', m).onclick = function () {
      H.curList().items.splice(idx, 1);
      H.save(true); m.close(); refresh();
    };
    $('#seSave', m).onclick = function () {
      it.name = $('#sen', m).value;
      it.qty = H.num($('#seq', m).value, 1);
      it.price = H.num($('#sep', m).value);
      it.aisle = $('#sea', m).value;
      it.note = $('#sen2', m).value;
      H.save(true); m.close(); refresh();
    };
  }

  /* ---------------------------------------------------------- pantry */
  function bindPantry() {
    var add = function () {
      ingPicker(function (it) {
        H.ask({
          title: 'How much of ' + it.name + '?',
          label: 'Grams', value: '500',
          text: 'Roughly is fine. This is only used to skip things when a list is generated.'
        }).then(function (v) {
          if (v == null) return;
          H.pantryAdd(it.key, H.num(v));
          refresh();
          toast(it.name + ' in the pantry');
        });
      });
    };
    on('#panAdd', 'click', add);
    on('#panAdd2', 'click', add);
    on('#panClear', 'click', function () {
      H.confirmDanger({
        title: 'Empty the pantry?',
        text: 'Generated shopping lists will stop skipping anything.'
      }).then(function (ok) {
        if (!ok) return;
        var backup = S().pantry;
        S().pantry = {};
        H.save(true); refresh();
        toast('Pantry emptied', {
          action: 'Undo',
          onAction: function () { S().pantry = backup; H.save(true); refresh(); }
        });
      });
    });
    on('#panCsv', 'click', function () {
      var rows = [['Ingredient', 'Aisle', 'Grams', 'Value']];
      Object.keys(S().pantry).forEach(function (k) {
        var g = H.ING(k);
        if (!g) return;
        rows.push([g.n, g.a || '', Math.round(S().pantry[k].g),
        (S().pantry[k].g / 100 * H.best(g)).toFixed(2)]);
      });
      H.dl('pantry-' + H.today() + '.csv', H.toCSV(rows), 'text/csv');
    });
  }

  /* ---------------------------------------------------------- ingredients */
  function drawIngTable(q) {
    var body = $('#ingBody');
    if (!body) return;
    q = (q || '').toLowerCase();
    var keys = H.allIngKeys().filter(function (k) {
      return H.ING(k).n.toLowerCase().indexOf(q) >= 0;
    }).sort(function (a, b) { return H.ING(a).n.localeCompare(H.ING(b).n); });

    body.innerHTML = keys.slice(0, 400).map(function (k) {
      var g = H.ING(k), ov = S().ingOv[k];
      return '<tr><td><b>' + E(g.n) + '</b>' +
        (ov ? ' <span class="chip t">edited</span>' : '') + '</td>' +
        '<td class="sm muted">' + E(g.a || 'Other') + '</td>' +
        '<td class="num">' + (g.w != null ? money(g.w) : '—') + '</td>' +
        '<td class="num">' + (g.c != null && g.c > 0 ? money(g.c) : '—') + '</td>' +
        '<td class="num"><b>' + money(H.best(g)) + '</b> ' +
        '<span class="xs muted">' + E(H.bestStore(g)) + '</span></td>' +
        '<td class="sm num">' + H.ingUsage(k) + '</td>' +
        '<td><button class="b o s" data-ie="' + E(k) + '">Edit</button></td></tr>';
    }).join('');
    H.setText('#ingCount', keys.length + ' shown' +
      (keys.length > 400 ? ' (first 400 — narrow the search)' : ''));
  }

  function bindIngredients() {
    drawIngTable('');
    on('#ingQ', 'input', debounce(function () { drawIngTable(this.value); }, 120));
    on('#ingNew', 'click', function () { ingEditor(null); });
    on('#ingCsv', 'click', function () {
      var rows = [['Ingredient', 'Aisle', 'Walmart/100g', 'Costco/100g', 'Best',
        'BestStore', 'UsedIn', 'Edited']];
      H.allIngKeys().forEach(function (k) {
        var g = H.ING(k);
        rows.push([g.n, g.a || '', g.w, g.c, H.best(g).toFixed(3),
        H.bestStore(g), H.ingUsage(k), S().ingOv[k] ? 'yes' : '']);
      });
      H.dl('ingredients-' + H.today() + '.csv', H.toCSV(rows), 'text/csv');
    });
  }

  function ingEditor(k) {
    var g = k ? H.ING(k) : { n: '', a: 'Other', w: null, c: null };
    var isNew = !k;
    var aisles = H.AISLES.map(function (a) { return a[0]; }).concat(['Other']);

    var body = '<div class="fr">' +
      '<label class="f"><span>Name</span><input id="ieN" value="' + E(g.n) + '"></label>' +
      '<label class="f"><span>Aisle</span><select id="ieA">' +
      aisles.map(function (a) {
        return '<option' + (a === (g.a || 'Other') ? ' selected' : '') + '>' + E(a) + '</option>';
      }).join('') + '</select></label></div>' +
      '<div class="fr">' +
      '<label class="f"><span>Walmart $ per 100 g</span>' +
      '<input id="ieW" type="number" step="0.01" min="0" value="' + (g.w != null ? g.w : '') + '"></label>' +
      '<label class="f"><span>Costco $ per 100 g</span>' +
      '<input id="ieC" type="number" step="0.01" min="0" value="' +
      (g.c != null && g.c > 0 ? g.c : '') + '"></label></div>' +
      (isNew ? '<div class="fr">' +
        '<label class="f"><span>kcal /100g</span><input id="ieK" type="number"></label>' +
        '<label class="f"><span>Protein</span><input id="ieP" type="number" step="0.1"></label>' +
        '<label class="f"><span>Carbs</span><input id="ieCb" type="number" step="0.1"></label>' +
        '<label class="f"><span>Fat</span><input id="ieF" type="number" step="0.1"></label></div>' : '') +
      '<p class="sm muted">Leave a price blank if that store does not stock a sensible size. ' +
      'The cheaper of the two is always what gets used.</p>' +
      (k ? '<p class="sm muted">Used in <b>' + H.ingUsage(k) + '</b> recipes. Changing the price ' +
        'updates all of them.</p>' : '');

    var m = modal(isNew ? 'Add an ingredient' : 'Edit ' + g.n, body,
      (k && S().ingOv[k] ? '<button class="b o dz" id="ieReset">Reset to default</button>' : '') +
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="ieSave">Save</button>', { focus: '#ieN' });

    var reset = $('#ieReset', m);
    if (reset) {
      reset.onclick = function () {
        delete S().ingOv[k];
        H.save(true); H.bumpCosts(); m.close(); refresh();
        toast('Reset to the default price');
      };
    }
    $('#ieSave', m).onclick = function () {
      var nm = $('#ieN', m).value.trim();
      if (!nm) { toast('It needs a name'); $('#ieN', m).focus(); return; }
      var key = k || ('u_' + nm.toLowerCase().replace(/[^a-z0-9]+/g, '_').slice(0, 28));
      var w = $('#ieW', m).value, c = $('#ieC', m).value;
      var o = S().ingOv[key] || {};
      o.n = nm;
      o.a = $('#ieA', m).value;
      o.w = w === '' ? null : H.num(w);
      o.c = c === '' ? null : H.num(c);
      if (isNew) {
        o.k = H.num($('#ieK', m).value);
        o.p = H.num($('#ieP', m).value);
        o.cb = H.num($('#ieCb', m).value);
        o.f = H.num($('#ieF', m).value);
        o.userAdded = true;
      }
      S().ingOv[key] = o;
      H.save(true); H.bumpCosts(); m.close(); refresh();
      toast(isNew ? 'Ingredient added' : 'Updated. ' + H.ingUsage(key) + ' recipes recosted.');
    };
  }

  /* ---------------------------------------------------------- training */
  function bindTraining() {
    on('#tWorkout', 'change', function () {
      H.dayLog(H.today()).workout = this.value;
      H.save(true); refresh();
    });
    on('#tSave', 'click', function () {
      var d = H.dayLog(H.today());
      d.notes = $('#tNotes').value;
      var w = parseFloat($('#tW').value);
      d.w = isNaN(w) ? null : w;
      H.save(true); refresh();
      toast('Saved');
    });
    on('#splitBtn', 'click', splitModal);
  }

  function splitModal() {
    var keys = Object.keys(H.SPLITS);
    var m = modal('Generate a training split',
      '<p class="sm muted" style="margin-top:0">Writes a repeating week onto the calendar, ' +
      'which is what the macro targets key off. Anything already logged on those days keeps ' +
      'its meals and notes.</p>' +
      form([
        {
          id: 'spK', l: 'Split', t: 'select', wide: true,
          o: keys.map(function (k) { return [k, H.SPLITS[k].n]; }), v: 'ppl'
        },
        { id: 'spFrom', l: 'Starting', t: 'date', v: H.today() },
        {
          id: 'spWeeks', l: 'For how long', t: 'select',
          o: [[1, 'One week'], [2, 'Two weeks'], [4, 'A month'], [12, 'Three months']], v: 4
        }
      ]) + '<div id="spPreview"></div>',
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="spGo">Write it to the calendar</button>', { focus: '#spK' });

    function preview() {
      var s = H.SPLITS[$('#spK', m).value];
      var from = $('#spFrom', m).value || H.today();
      var startDow = H.dOf(from).getDay();
      $('#spPreview', m).innerHTML = '<div class="lbl" style="margin-bottom:8px">The week</div>' +
        '<div class="row">' + H.DOW.map(function (d, i) {
          var w = s.d[(i - startDow + 7 * 7) % 7];
          // Show the week as it will land on real weekdays.
          var wk = s.d[((i - startDow) % 7 + 7) % 7];
          return '<span class="pill flat' + (wk !== 'rest' ? ' on' : '') + '">' + d + ' ' +
            E(H.TRAIN[wk].n.split(' ')[0]) + '</span>';
        }).join('') + '</div>';
    }
    $('#spK', m).onchange = preview;
    $('#spFrom', m).onchange = preview;
    preview();

    $('#spGo', m).onclick = function () {
      var from = $('#spFrom', m).value || H.today();
      var n = H.applySplit($('#spK', m).value, from, +$('#spWeeks', m).value, 0);
      m.close(); refresh();
      toast(n + ' days scheduled');
    };
  }

  function drawEx() {
    var el = $('#exList');
    if (!el) return;
    var q = H.exFlt.q.toLowerCase();
    var L = H.EX.filter(function (e) {
      if (H.exFlt.mg && e.mg !== H.exFlt.mg) return false;
      if (H.exFlt.hero && !e.hero) return false;
      if (H.exFlt.eq && e.eq.toLowerCase().indexOf(H.exFlt.eq.toLowerCase()) < 0) return false;
      if (q && (e.n + ' ' + e.pri + ' ' + e.tags).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    H.setText('#excount', L.length + ' exercise' + (L.length === 1 ? '' : 's'));
    el.innerHTML = L.slice(0, 120).map(function (e) {
      return '<details data-ex="' + E(e.n) + '"><summary>' + E(e.n) +
        ' <span class="chip">' + E(e.mg) + '</span>' +
        (e.hero ? ' <span class="chip t">Hero</span>' : '') + '</summary><div class="dc">' +
        '<div class="chips"><span class="chip">' + E(e.eq) + '</span>' +
        '<span class="chip">' + E(e.df) + '</span>' +
        '<span class="chip">' + E(e.sets) + ' × ' + E(e.reps) + '</span>' +
        '<span class="chip">RIR ' + E(e.rir) + '</span>' +
        '<span class="chip">' + E(e.rest) + '</span></div>' +
        '<p><b>Technique.</b> ' + E(e.tech) + '</p>' +
        (e.mist ? '<p><b>Common mistakes.</b> ' + E(e.mist) + '</p>' : '') +
        (e.prog ? '<p><b>Progress it.</b> ' + E(e.prog) + '</p>' : '') +
        (e.reg ? '<p><b>Regress it.</b> ' + E(e.reg) + '</p>' : '') +
        (e.use ? '<p><b>Best use.</b> ' + E(e.use) + '</p>' : '') +
        '<p class="sm muted">Primary: ' + E(e.pri) +
        (e.sec ? '. Secondary: ' + E(e.sec) : '') + '</p></div></details>';
    }).join('') || '<p class="empty">Nothing matches.</p>';
    if (L.length > 120) {
      el.innerHTML += '<p class="sm muted" style="text-align:center">Showing the first 120 of ' +
        L.length + '. Narrow the search to see the rest.</p>';
    }
  }

  H.focusExercise = function (name) {
    H.exFlt = { q: name, mg: '', eq: '', hero: false };
    refresh();
    var d = $('[data-ex]');
    if (d) { d.open = true; d.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  };

  function bindExercises() {
    drawEx();
    on('#exq', 'input', debounce(function () { H.exFlt.q = this.value; drawEx(); }, 130));
    on('#exmg', 'change', function () { H.exFlt.mg = this.value; drawEx(); });
    on('#exeq', 'change', function () { H.exFlt.eq = this.value; drawEx(); });
    on('#exhero', 'click', function () {
      H.exFlt.hero = !H.exFlt.hero;
      this.classList.toggle('on');
      drawEx();
    });
  }

  function sessModal(i) {
    var s = H.SESS[i];
    if (!s) return;
    var m = modal(s.name,
      '<div class="tw"><table><thead><tr><th>Exercise</th><th>Sets</th><th>Reps</th>' +
      '<th>Note</th></tr></thead><tbody>' +
      s.ex.map(function (x) {
        return '<tr><td><b>' + E(x.n) + '</b></td><td>' + E(x.sets) + '</td>' +
          '<td>' + E(x.reps) + '</td><td class="sm muted">' + E(x.note) + '</td></tr>';
      }).join('') + '</tbody></table></div>',
      '<button class="b o" id="sessCopy">Copy to today\'s notes</button>' +
      '<button class="b" data-close>Close</button>', { wide: true });

    $('#sessCopy', m).onclick = function () {
      var d = H.dayLog(H.today());
      var text = s.name + '\n' + s.ex.map(function (x) {
        return '- ' + x.n + ' ' + x.sets + '×' + x.reps;
      }).join('\n');
      d.notes = d.notes ? d.notes + '\n\n' + text : text;
      H.save(true); m.close(); refresh();
      toast('Copied into today');
    };
  }

  /* ---------------------------------------------------------- financial */
  function bindFin(sub) {
    on('#finMode', 'change', function () { S().fin.costMode = this.value; H.save(); refresh(); });
    on('#finPath', 'change', function () { S().fin.path = this.value; H.save(); refresh(); });
    on('#finScen', 'change', function () {
      var s = S().fin.scenarios[this.value];
      if (!s) return;
      S().fin.costMode = s.mode;
      S().fin.path = s.path;
      H.save(true); refresh();
      toast('Loaded ' + this.value);
    });
    on('#scenSave', 'click', function () {
      H.ask({
        title: 'Save this scenario', label: 'Name',
        placeholder: 'Renting, both grinding'
      }).then(function (n) {
        if (!n) return;
        var mode = S().fin.costMode || 'real', path = S().fin.path || 'rent';
        S().fin.scenarios[n] = {
          mode: mode, path: path,
          inc: H.finIncome('both', mode), cost: H.finCost(mode, path), saved: H.today()
        };
        H.save(true); refresh();
        toast('Scenario saved');
      });
    });
    on('#scenDel', 'click', function () {
      var v = $('#finScen').value;
      if (!v) { toast('Pick one first'); return; }
      H.confirmDanger({ title: 'Delete "' + v + '"?', text: 'The scenario goes.' })
        .then(function (ok) {
          if (!ok) return;
          delete S().fin.scenarios[v];
          H.save(true); refresh();
        });
    });
    ['#jobAdd', '#jobAdd2'].forEach(function (s) {
      on(s, 'click', function () { jobEditor(null); });
    });
    on('#costAdd', 'click', function () { costEditor(null); });
    ['#shAdd', '#shAdd2'].forEach(function (s) { on(s, 'click', shiftEditor); });
    on('#shCsv', 'click', function () {
      var rows = [['Date', 'Who', 'Job', 'Hours', 'Gross', 'Net', 'Note']];
      S().fin.shifts.forEach(function (sh) {
        var j = null;
        S().fin.jobs.forEach(function (x) { if (x.id === sh.jobId) j = x; });
        rows.push([sh.date, j ? H.nameOf(j.who) : '', j ? j.name : '',
        sh.hours, sh.gross, sh.net, sh.note || '']);
      });
      H.dl('shifts-' + H.today() + '.csv', H.toCSV(rows), 'text/csv');
    });
    on('#scenFromActual', 'click', function () {
      var from = H.addDays(H.today(), -90);
      var net = H.shiftsFor(null, from).reduce(function (a, s) { return a + (s.net || 0); }, 0) / (90 / 30.4);
      S().fin.scenarios['From actual earnings'] = {
        mode: 'actual', path: S().fin.path || 'rent',
        inc: Math.round(net), cost: H.finCost('real', S().fin.path || 'rent'),
        saved: H.today(), auto: true
      };
      H.save(true); refresh();
      toast('Saved from real data');
    });
    ['#bpNew', '#bpNew2'].forEach(function (s) {
      on(s, 'click', function () {
        H.ask({ title: 'New comparison list', label: 'Name', value: 'Apartments' })
          .then(function (n) {
            if (!n) return;
            H.ask({ title: 'What kind?', label: 'Category', value: 'Housing' }).then(function (c) {
              S().fin.purchases[n] = { cat: c || 'Other', items: [] };
              H.save(true); refresh();
            });
          });
      });
    });
  }

  var JOB_FIELDS = function (j) {
    return [
      {
        id: 'jw', l: 'Who', t: 'select',
        o: [['Jaron', S().prof.j.name], ['Aaliyah', S().prof.a.name], ['Both', 'Shared / gig']],
        v: j.who
      },
      { id: 'jn', l: 'Name', v: j.name, ph: 'Ritchey day job' },
      { id: 'je', l: 'Employer', v: j.employer },
      { id: 'jt', l: 'Title', v: j.title },
      { id: 'jr', l: 'Hourly rate', t: 'number', step: '0.01', v: j.rate },
      { id: 'jl', l: 'Low / mo', t: 'number', v: j.low },
      { id: 'jm', l: 'Realistic / mo', t: 'number', v: j.real },
      { id: 'jh', l: 'High / mo', t: 'number', v: j.high }
    ];
  };

  function jobEditor(id) {
    var j = null;
    if (id) S().fin.jobs.forEach(function (x) { if (x.id === id) j = x; });
    if (!j) j = { who: 'Jaron', name: '', employer: '', title: '', rate: '', low: '', real: '', high: '' };

    var m = modal(id ? 'Edit income' : 'Add income', form(JOB_FIELDS(j)),
      (id ? '<button class="b o dz" id="jDel">Delete</button>' : '') +
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="jSave">Save</button>', { focus: '#jn' });

    var del = $('#jDel', m);
    if (del) {
      del.onclick = function () {
        S().fin.jobs = S().fin.jobs.filter(function (x) { return x.id !== id; });
        H.save(true); m.close(); refresh();
      };
    }
    $('#jSave', m).onclick = function () {
      var o = {
        id: id || H.uid(), who: $('#jw', m).value,
        name: $('#jn', m).value.trim() || 'Income',
        employer: $('#je', m).value, title: $('#jt', m).value,
        rate: H.num($('#jr', m).value) || null,
        low: H.num($('#jl', m).value), real: H.num($('#jm', m).value),
        high: H.num($('#jh', m).value)
      };
      if (id) S().fin.jobs = S().fin.jobs.map(function (x) { return x.id === id ? o : x; });
      else S().fin.jobs.push(o);
      H.save(true); m.close(); refresh();
    };
  }

  function costEditor(id) {
    var c = null;
    if (id) S().fin.costs.forEach(function (x) { if (x.id === id) c = x; });
    if (!c) c = { name: '', section: 'Living', who: 'Both', low: '', real: '', high: '', actual: '' };

    var m = modal(id ? 'Edit cost' : 'Add cost',
      form([{ id: 'cn', l: 'Cost', v: c.name },
      {
        id: 'cs', l: 'Section', t: 'select',
        o: [['Living', 'Living'], ['Utilities', 'Utilities'], ['Health', 'Health'],
        ['Housing (rent)', 'Housing (rent)'], ['Housing (buy)', 'Housing (buy)'],
        ['Debt', 'Debt'], ['Savings', 'Savings']], v: c.section
      },
      {
        id: 'cw', l: 'Who', t: 'select',
        o: [['Both', 'Both'], ['Jaron', S().prof.j.name], ['Aaliyah', S().prof.a.name]], v: c.who
      },
      { id: 'cl', l: 'Low', t: 'number', v: c.low },
      { id: 'cr', l: 'Realistic', t: 'number', v: c.real },
      { id: 'ch', l: 'High', t: 'number', v: c.high },
      { id: 'ca', l: 'Actual', t: 'number', v: c.actual }]),
      (id ? '<button class="b o dz" id="cDel">Delete</button>' : '') +
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="cSave">Save</button>', { focus: '#cn' });

    var del = $('#cDel', m);
    if (del) {
      del.onclick = function () {
        S().fin.costs = S().fin.costs.filter(function (x) { return x.id !== id; });
        H.save(true); m.close(); refresh();
      };
    }
    $('#cSave', m).onclick = function () {
      var o = {
        id: id || H.uid(), name: $('#cn', m).value.trim() || 'Cost',
        section: $('#cs', m).value, who: $('#cw', m).value,
        low: H.num($('#cl', m).value), real: H.num($('#cr', m).value),
        high: H.num($('#ch', m).value), actual: H.num($('#ca', m).value) || null
      };
      if (id) S().fin.costs = S().fin.costs.map(function (x) { return x.id === id ? o : x; });
      else S().fin.costs.push(o);
      H.save(true); m.close(); refresh();
    };
  }

  function shiftEditor() {
    if (!S().fin.jobs.length) { toast('Add a job first'); return; }
    var m = modal('Log a shift',
      form([{ id: 'sd', l: 'Date', t: 'date', v: H.today() },
      {
        id: 'sj', l: 'Job', t: 'select',
        o: S().fin.jobs.map(function (j) { return [j.id, H.nameOf(j.who) + ' — ' + j.name]; }),
        v: S().fin.jobs[0].id
      },
      { id: 'sh', l: 'Hours', t: 'number', step: '0.25', v: 8 },
      { id: 'sg', l: 'Gross $', t: 'number', step: '0.01', v: '' },
      { id: 'sn', l: 'Net (after tax) $', t: 'number', step: '0.01', v: '' },
      { id: 'sx', l: 'Note', v: '', wide: true }]) +
      '<p class="sm muted">Leave gross blank and it uses the job hourly rate. Leave net blank ' +
      'and it estimates 80% of gross.</p>',
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="sSave">Save</button>', { focus: '#sd' });

    $('#sSave', m).onclick = function () {
      var jid = $('#sj', m).value, j = null;
      S().fin.jobs.forEach(function (x) { if (x.id === jid) j = x; });
      var hrs = H.num($('#sh', m).value);
      var g = H.num($('#sg', m).value), n = H.num($('#sn', m).value);
      if (!g && j && j.rate) g = hrs * j.rate;
      if (!n && g) n = g * 0.8;
      S().fin.shifts.push({
        id: H.uid(), date: $('#sd', m).value || H.today(), jobId: jid, hours: hrs,
        gross: Math.round(g * 100) / 100, net: Math.round(n * 100) / 100,
        note: $('#sx', m).value
      });
      H.save(true); m.close(); refresh();
      toast('Shift logged');
    };
  }

  function bpItemEditor(listName) {
    var L = S().fin.purchases[listName];
    if (!L) return;
    var cat = (L.cat || '').toLowerCase();
    var extra = cat.indexOf('hous') >= 0
      ? [{ id: 'f1', l: 'Beds' }, { id: 'f2', l: 'Baths' }, { id: 'f3', l: 'Sq ft' }, { id: 'f4', l: 'To CSU (min)' }]
      : cat.indexOf('car') >= 0
        ? [{ id: 'f1', l: 'Year' }, { id: 'f2', l: 'Miles' }, { id: 'f3', l: 'MPG' }, { id: 'f4', l: 'Condition' }]
        : [{ id: 'f1', l: 'Detail 1' }, { id: 'f2', l: 'Detail 2' }];

    var m = modal('Add to ' + listName,
      form([{ id: 'bn', l: 'Name', v: '' },
      { id: 'bp', l: 'Price / rent', t: 'number', v: '' },
      { id: 'bl', l: 'Link', v: '' }]
        .concat(extra)
        .concat([{ id: 'bo', l: 'Notes', t: 'area', v: '' }])),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="bSave">Save</button>', { focus: '#bn' });

    $('#bSave', m).onclick = function () {
      var f = {};
      extra.forEach(function (x) {
        var v = $('#' + x.id, m).value;
        if (v) f[x.l] = v;
      });
      L.items.push({
        name: $('#bn', m).value.trim() || 'Item', price: H.num($('#bp', m).value),
        link: $('#bl', m).value, notes: $('#bo', m).value, fields: f
      });
      H.save(true); m.close(); refresh();
    };
  }

  /* ---------------------------------------------------------- schedule */
  function bindSched() {
    on('#cPrev', 'click', function () {
      H.calM--;
      if (H.calM < 0) { H.calM = 11; H.calY--; }
      refresh();
    });
    on('#cNext', 'click', function () {
      H.calM++;
      if (H.calM > 11) { H.calM = 0; H.calY++; }
      refresh();
    });
    on('#schWorkout', 'change', function () {
      H.dayLog(H.calSel).workout = this.value;
      H.save(true); refresh();
    });
    on('#evAdd', 'click', function () { evEditor(H.calSel); });
    on('#spAdd', 'click', function () { spendEditor(H.calSel); });
    on('#mealAdd', 'click', function () { mealPicker(H.calSel); });
    on('#logPlannedDay', 'click', function () { logPlanned(H.calSel); });
    ['#applyTmpl', '#applyTmpl2'].forEach(function (s) {
      on(s, 'click', function () {
        var n = H.applyTemplate(H.calSel);
        refresh();
        toast(n ? n + ' items added to that week' : 'Already applied');
      });
    });
    on('#calCsv', 'click', function () {
      var rows = [['Date', 'Training', 'Kcal', 'Protein', 'FoodCost', 'OtherSpend',
        'Plans', 'Bodyweight', 'Notes']];
      Object.keys(S().days).sort().forEach(function (d) {
        var rec = S().days[d], e = H.eaten(d);
        var sp = (rec.spend || []).reduce(function (a, x) { return a + (x.amt || 0); }, 0);
        rows.push([d, H.TRAIN[rec.workout] ? H.TRAIN[rec.workout].n : rec.workout,
        Math.round(e.kcal), Math.round(e.p), e.cost.toFixed(2), sp.toFixed(2),
        (rec.sched || []).map(function (x) { return H.nameOf(x.who) + ':' + x.what; }).join('; '),
        rec.w || '', rec.notes || '']);
      });
      H.dl('log-' + H.today() + '.csv', H.toCSV(rows), 'text/csv');
    });
  }

  function whoOptions() {
    return [['Jaron', S().prof.j.name], ['Aaliyah', S().prof.a.name], ['Both', 'Both of us']];
  }

  function evEditor(ds) {
    var m = modal('Add to ' + H.shortD(ds),
      form([{ id: 'ew', l: 'Who', t: 'select', o: whoOptions(), v: H.label(S().who) },
      { id: 'ex', l: 'What', v: '', ph: 'Class, shift, gym' },
      { id: 'ef', l: 'From', t: 'time', v: '09:00' },
      { id: 'et', l: 'To', t: 'time', v: '17:00' },
      { id: 'el', l: 'Where', v: '' }]),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="eSave">Add</button>', { focus: '#ex' });

    $('#eSave', m).onclick = function () {
      H.dayLog(ds).sched.push({
        who: $('#ew', m).value, what: $('#ex', m).value.trim() || 'Busy',
        from: $('#ef', m).value, to: $('#et', m).value, where: $('#el', m).value
      });
      H.save(true); m.close(); refresh();
    };
  }

  function spendEditor(ds) {
    var m = modal('Log a spend',
      form([{ id: 'sw', l: 'Who', t: 'select', o: whoOptions(), v: 'Both' },
      { id: 'sx', l: 'What', v: '', ph: 'Gas, coffee, parts' },
      { id: 'sa', l: 'Amount', t: 'number', step: '0.01', v: '' }]),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="spSave">Add</button>', { focus: '#sx' });

    $('#spSave', m).onclick = function () {
      H.dayLog(ds).spend.push({
        who: $('#sw', m).value, what: $('#sx', m).value.trim() || 'Spend',
        amt: H.num($('#sa', m).value)
      });
      H.save(true); m.close(); refresh();
    };
  }

  function mealPicker(ds) {
    var m = modal('Log a meal on ' + H.shortD(ds),
      '<label class="f"><span>Search</span>' +
      '<input id="mpq" type="search" placeholder="What did we eat?" autocomplete="off"></label>' +
      '<div class="picklist" id="mplist"></div>',
      '<button class="b" data-close>Done</button>',
      { focus: '#mpq', onClose: refresh });

    function draw(q) {
      q = (q || '').toLowerCase();
      var hits = H.all().filter(function (r) {
        return r.n.toLowerCase().indexOf(q) >= 0;
      }).slice(0, 60);
      $('#mplist', m).innerHTML = hits.map(function (r) {
        return '<button class="pickrow" data-a="' + E(r.id) + '"><div style="flex:1">' +
          '<b>' + E(r.n) + '</b><div class="xs muted">' + Math.round(r.k) + ' kcal &middot; ' +
          Math.round(r.p) + 'g protein &middot; ' + money(H.cps(r)) + '</div></div>' +
          '<span class="b s">Add</span></button>';
      }).join('');
      $$('[data-a]', m).forEach(function (row) {
        row.onclick = function () {
          H.dayLog(ds).meals.push({ id: row.dataset.a, q: 1 });
          H.consumeFromPantry(row.dataset.a, 1);
          H.save(true);
          toast('Logged');
        };
      });
    }
    $('#mpq', m).oninput = function () { draw(this.value); };
    draw('');
  }

  function tmplEditor(dayIdx) {
    var m = modal('Regular ' + H.DOW[dayIdx],
      form([{ id: 'tw', l: 'Who', t: 'select', o: whoOptions(), v: H.label(S().who) },
      { id: 'tx', l: 'What', v: '', ph: 'Work, class, gym' },
      { id: 'tf', l: 'From', t: 'time', v: '09:00' },
      { id: 'tt', l: 'To', t: 'time', v: '17:00' }]),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="tSave2">Add</button>', { focus: '#tx' });

    $('#tSave2', m).onclick = function () {
      if (!S().sched.tmpl[dayIdx]) S().sched.tmpl[dayIdx] = [];
      S().sched.tmpl[dayIdx].push({
        who: $('#tw', m).value, what: $('#tx', m).value.trim() || 'Busy',
        from: $('#tf', m).value, to: $('#tt', m).value
      });
      H.save(true); m.close(); refresh();
    };
  }

  /* ---------------------------------------------------------- settings */
  function bindSettings() {
    on('#setTheme', 'change', function () {
      S().theme = this.value;
      H.save(true);
      applyTheme();
    });
    on('#setSlots', 'change', function () {
      S().prefs.planSlots = +this.value;
      H.planOpts.slots = +this.value;
      H.save();
    });
    on('#setBudget', 'change', function () {
      S().prefs.dayBudget = this.value === '' ? null : H.num(this.value);
      H.planOpts.budget = this.value;
      H.save();
    });
    on('#setRemind', 'click', function () {
      var next = this.getAttribute('aria-checked') !== 'true';
      this.setAttribute('aria-checked', next);
      S().prefs.remindBackup = next;
      H.save(true);
    });
    on('#setExport', 'click', exportAll);
    on('#setImport', 'click', importAll);
    on('#setDropPhotos', 'click', function () {
      H.confirmDanger({
        title: 'Remove every photo?',
        text: 'This frees the most storage by a wide margin. The recipes themselves are untouched.'
      }).then(function (ok) {
        if (!ok) return;
        S().photos = {};
        H.save(true); refresh();
        toast('Photos removed');
      });
    });
    on('#setReset', 'click', function () {
      H.confirmDanger({
        title: 'Start over?',
        text: 'Every profile, log, list, price edit and photo on this device goes. ' +
          'Save to a file first if there is any doubt.',
        ok: 'Wipe it'
      }).then(function (ok) {
        if (!ok) return;
        H.setState(H.DEF());
        H.save(true);
        H.invalidate();
        applyTheme();
        chrome();
        nav('meals');
        toast('Back to a clean slate');
      });
    });
    $$('[data-prof]').forEach(function (b) {
      b.onclick = function () { profileEditor(b.dataset.prof); };
    });
    $$('[data-listdel]').forEach(function (b) {
      b.onclick = function () {
        var n = b.dataset.listdel;
        var backup = S().lists[n];
        delete S().lists[n];
        H.save(true); refresh();
        toast('Deleted "' + n + '"', {
          action: 'Undo',
          onAction: function () { S().lists[n] = backup; H.save(true); refresh(); }
        });
      };
    });
    $$('[data-listshop]').forEach(function (b) {
      b.onclick = function () {
        var ids = S().lists[b.dataset.listshop] || [];
        var n = 0;
        ids.forEach(function (id) { n += H.addRecipeToShop(H.byId(id)); });
        toast(n + ' ingredients added to "' + S().shop.active + '"');
      };
    });
  }

  function profileEditor(k) {
    var p = S().prof[k];
    var fields = [
      { id: 'pfN', l: 'Name', v: p.name, wide: true },
      { id: 'pfS', l: 'Sex', t: 'select', o: [['m', 'Male'], ['f', 'Female']], v: p.sex },
      { id: 'pfA', l: 'Age', t: 'number', v: p.age, min: 12, max: 100 },
      { id: 'pfW', l: 'Weight (lb)', t: 'number', step: '0.1', v: p.w },
      { id: 'pfH', l: 'Height (in)', t: 'number', step: '0.5', v: p.h },
      { id: 'pfB', l: 'Body fat %', t: 'number', step: '0.5', v: p.bf },
      {
        id: 'pfAc', l: 'Activity', t: 'select', v: p.act,
        o: [[1.2, 'Sedentary'], [1.375, 'Light, 1–3 days'], [1.45, 'Moderate, 3–4 days'],
        [1.55, 'Active, 4–5 days'], [1.725, 'Very active, 6–7 days'], [1.9, 'Athlete / physical job']]
      },
      {
        id: 'pfG', l: 'Goal', t: 'select', v: p.goal,
        o: [[0.8, 'Cut hard (−20%)'], [0.9, 'Cut (−10%)'], [1.0, 'Maintain'],
        [1.09, 'Lean bulk (+9%)'], [1.2, 'Bulk (+20%)']]
      },
      {
        id: 'pfP', l: 'Protein g per lb', t: 'number', step: '0.05', v: p.pf,
        hint: '0.8 to 1.2 covers almost everyone lifting.'
      }
    ];

    var m = modal('Edit ' + p.name, form(fields) + '<div id="pfPreview"></div>',
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="pfSave">Save</button>', { focus: '#pfN' });

    function read() {
      return {
        name: $('#pfN', m).value.trim() || p.name,
        sex: $('#pfS', m).value,
        age: H.num($('#pfA', m).value, p.age),
        w: H.num($('#pfW', m).value, p.w),
        h: H.num($('#pfH', m).value, p.h),
        bf: H.num($('#pfB', m).value, p.bf),
        act: H.num($('#pfAc', m).value, p.act),
        goal: H.num($('#pfG', m).value, p.goal),
        pf: H.num($('#pfP', m).value, p.pf)
      };
    }
    function preview() {
      var c = H.calc(read());
      $('#pfPreview', m).innerHTML = '<div class="stats" style="margin-top:6px">' +
        H.stat(c.kcal.toLocaleString(), 'Kcal / day', 'acc') +
        H.stat(c.p + 'g', 'Protein') +
        H.stat(c.c + 'g', 'Carbs') +
        H.stat(c.f + 'g', 'Fat') +
        H.stat(c.w + 'oz', 'Water') + '</div>' +
        '<p class="sm muted" style="margin:10px 0 0">TDEE ' + c.tdee.toLocaleString() +
        ', resting ' + c.rmr.toLocaleString() + ', FFMI ' + c.ffmi + '. About <b>' +
        (c.rate >= 0 ? '+' : '') + c.rate.toFixed(1) + ' lb a week</b> at this intake.</p>';
    }
    $$('input,select', m).forEach(function (n) {
      n.addEventListener('input', preview);
      n.addEventListener('change', preview);
    });
    preview();

    $('#pfSave', m).onclick = function () {
      var next = read();
      Object.keys(next).forEach(function (key) { p[key] = next[key]; });
      H.save(true);
      m.close();
      chrome();
      refresh();
      toast('Profile updated');
    };
  }

  /* ---------------------------------------------------------- own recipe */
  function ownRecipe() {
    var fields = [
      { id: 'on', l: 'Name', v: '', wide: true },
      {
        id: 'oc', l: 'Category', t: 'select', v: 'Lunch/Dinner',
        o: [['Breakfast', 'Breakfast'], ['Lunch/Dinner', 'Mains'], ['Snack', 'Snack'],
        ['Drink', 'Drink'], ['SDA Meat/Fish', 'Meat and fish']]
      },
      { id: 'osv', l: 'Servings', t: 'number', v: 2, min: 1 },
      { id: 'ot', l: 'Minutes', t: 'number', v: 20, min: 0 },
      { id: 'ok', l: 'Kcal / serving', t: 'number', v: '' },
      { id: 'op', l: 'Protein g', t: 'number', v: '' },
      { id: 'ocb', l: 'Carbs g', t: 'number', v: '' },
      { id: 'of', l: 'Fat g', t: 'number', v: '' },
      { id: 'ofib', l: 'Fiber g', t: 'number', v: '' },
      { id: 'ocost', l: 'Cost / serving', t: 'number', step: '0.01', v: '' },
      { id: 'oi', l: 'Ingredients, one per line', t: 'area', rows: 5, v: '' },
      { id: 'os', l: 'Method, one step per line', t: 'area', rows: 5, v: '' }
    ];
    var m = modal('Add my own recipe', form(fields),
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="oSave">Save</button>', { focus: '#on', wide: true });

    $('#oSave', m).onclick = function () {
      var n = $('#on', m).value.trim();
      if (!n) { toast('It needs a name'); $('#on', m).focus(); return; }
      var sv = H.num($('#osv', m).value, 1);
      var c = H.num($('#ocost', m).value);
      S().mine.push({
        id: 'X-' + (S().mine.length + 1), n: n, cat: $('#oc', m).value, sv: sv,
        t: H.num($('#ot', m).value, 20), diff: 'MODERATE',
        k: H.num($('#ok', m).value), p: H.num($('#op', m).value),
        c: H.num($('#ocb', m).value), f: H.num($('#of', m).value),
        fib: H.num($('#ofib', m).value), leu: 0, tg: ['MY RECIPE'],
        cw: c * sv, cws: c, cc: c * sv, ccs: c,
        ing: $('#oi', m).value.split('\n').filter(Boolean).map(function (l) {
          return [l.trim(), '', 0];
        }),
        st: $('#os', m).value.split('\n').filter(Boolean),
        storage: '', prep: '', subs: [], vars: []
      });
      H.save(true);
      H.invalidate();
      m.close();
      refresh();
      toast('Recipe saved');
    };
  }

  function listModal(id) {
    var names = Object.keys(S().lists);
    var body = (names.length
      ? names.map(function (n) {
        var has = S().lists[n].indexOf(id) >= 0;
        return '<label class="pickrow" data-l="' + E(n) + '">' +
          '<input type="checkbox"' + (has ? ' checked' : '') +
          ' style="width:18px;height:18px;accent-color:var(--forest)">' +
          '<div><b>' + E(n) + '</b><div class="xs muted">' +
          S().lists[n].length + ' recipes</div></div></label>';
      }).join('')
      : '<p class="sm muted">No recipe lists yet.</p>') +
      '<label class="f" style="margin-top:14px"><span>Or make a new one</span>' +
      '<input id="nl" placeholder="Sunday prep"></label>';

    var m = modal('Add to a recipe list', body,
      '<button class="b o" data-close>Cancel</button>' +
      '<button class="b" id="lS">Save</button>', { focus: '#nl' });

    $('#lS', m).onclick = function () {
      $$('.pickrow', m).forEach(function (row) {
        var n = row.dataset.l;
        if (!n) return;
        var checked = row.querySelector('input').checked;
        var i = S().lists[n].indexOf(id);
        if (checked && i < 0) S().lists[n].push(id);
        if (!checked && i >= 0) S().lists[n].splice(i, 1);
      });
      var nl = $('#nl', m).value.trim();
      if (nl) {
        if (!S().lists[nl]) S().lists[nl] = [];
        if (S().lists[nl].indexOf(id) < 0) S().lists[nl].push(id);
      }
      H.save(true); m.close();
      toast('Saved to your lists');
    };
  }

  function planPicker(id) {
    var r = H.byId(id);
    var days = [];
    for (var i = 0; i < 14; i++) days.push(H.addDays(H.today(), i));
    var m = modal('Put ' + (r ? r.n : 'this') + ' on a day',
      '<div class="picklist">' + days.map(function (ds) {
        var n = (S().plan[ds] || []).length;
        return '<button class="pickrow" data-d="' + ds + '"><div style="flex:1">' +
          '<b>' + E(H.pretty(ds)) + '</b><div class="xs muted">' +
          (n ? n + ' meals planned' : 'nothing planned') + '</div></div>' +
          '<span class="b s">Add</span></button>';
      }).join('') + '</div>',
      '<button class="b" data-close>Done</button>');

    $$('[data-d]', m).forEach(function (row) {
      row.onclick = function () {
        var ds = row.dataset.d;
        if (!S().plan[ds]) S().plan[ds] = [];
        S().plan[ds].push({ id: id, q: 1, slot: 'snack' });
        H.save(true);
        m.close();
        toast('Added to ' + H.shortD(ds));
      };
    });
  }

  /* ---------------------------------------------------------- photos */
  function pickPhoto(id) {
    H.pickFile('image/*', function (f) {
      var fr = new FileReader();
      fr.onload = function () {
        var img = new Image();
        img.onload = function () {
          var sc = Math.min(1, 900 / Math.max(img.width, img.height));
          var cv = document.createElement('canvas');
          cv.width = img.width * sc | 0;
          cv.height = img.height * sc | 0;
          cv.getContext('2d').drawImage(img, 0, 0, cv.width, cv.height);
          S().photos[id] = cv.toDataURL('image/jpeg', 0.72);
          if (!H.save(true)) { delete S().photos[id]; return; }
          refresh();
          toast('Photo saved');
        };
        img.onerror = function () { toast('That image would not open'); };
        img.src = fr.result;
      };
      fr.readAsDataURL(f);
    });
  }

  function cardPNG(r) {
    if (!r) return;
    var W = 900, Hh = 1280;
    var cv = document.createElement('canvas');
    cv.width = W; cv.height = Hh;
    var x = cv.getContext('2d');
    var col = H.CATC[r.cat] || H.CATC['My recipe'];
    var g = x.createLinearGradient(0, 0, W, Hh);
    g.addColorStop(0, '#14140F'); g.addColorStop(.58, '#1F3A2C'); g.addColorStop(1, col[1]);
    x.fillStyle = g; x.fillRect(0, 0, W, Hh);
    x.fillStyle = col[0]; x.fillRect(0, 0, W, 9);
    x.fillStyle = '#A8CDB8'; x.font = '700 19px Helvetica,Arial';
    x.fillText(r.id + '   ·   ' + r.cat.toUpperCase() + '   ·   ' + r.diff, 56, 80);
    x.fillStyle = '#fff'; x.font = '800 52px Helvetica,Arial';
    var y = 142 + wrapT(x, r.n, 56, 142, 780, 56);

    var mac = [[Math.round(r.k), 'KCAL'], [Math.round(r.p) + 'g', 'PROTEIN'],
    [Math.round(r.c) + 'g', 'CARBS'], [Math.round(r.f) + 'g', 'FAT'],
    [Math.round(r.fib || 0) + 'g', 'FIBER'], [(r.leu || 0).toFixed(1) + 'g', 'LEUCINE']];
    var bw = (788 - 25) / 6;
    mac.forEach(function (mm, i) {
      var bx = 56 + i * (bw + 5);
      x.fillStyle = 'rgba(255,255,255,.10)'; x.fillRect(bx, y, bw, 90);
      x.fillStyle = '#fff'; x.font = '800 25px Helvetica,Arial'; x.textAlign = 'center';
      x.fillText(String(mm[0]), bx + bw / 2, y + 40);
      x.fillStyle = '#A8CDB8'; x.font = '700 11px Helvetica,Arial';
      x.fillText(mm[1], bx + bw / 2, y + 66);
      x.textAlign = 'left';
    });
    y += 128;

    x.fillStyle = '#1F4D3A'; x.fillRect(56, y, 788, 62);
    x.fillStyle = '#fff'; x.font = '700 23px Helvetica,Arial';
    x.fillText(r.t + ' min   ·   makes ' + r.sv + '   ·   ' + money(H.cps(r)) +
      '/serving   ·   ' + money(H.ctot(r)) + ' batch', 78, y + 39);
    y += 100;

    x.fillStyle = '#A8CDB8'; x.font = '700 16px Helvetica,Arial';
    x.fillText('INGREDIENTS', 56, y); y += 28;
    x.fillStyle = '#E6EDE7'; x.font = '400 18px Helvetica,Arial';
    (r.ing || []).slice(0, 15).forEach(function (i) {
      var q = H.ING(i[1]);
      x.fillText('•  ' + (i[2] ? Math.round(i[2]) + ' g  ' : '') + (q ? q.n : i[0]), 56, y);
      y += 26;
    });

    y += 20;
    x.fillStyle = '#A8CDB8'; x.font = '700 16px Helvetica,Arial';
    x.fillText('METHOD', 56, y); y += 28;
    x.fillStyle = '#C9D6CB'; x.font = '400 16px Helvetica,Arial';
    (r.st || []).slice(0, 6).forEach(function (s, i) {
      y += wrapT(x, (i + 1) + '. ' + s, 56, y, 788, 23) + 7;
    });
    x.fillStyle = '#6E8A76'; x.font = '700 13px Helvetica,Arial';
    x.fillText('The Handbook', 56, Hh - 40);

    var a = document.createElement('a');
    a.download = r.id + '-' + r.n.replace(/[^a-z0-9]+/gi, '-').toLowerCase() + '.png';
    a.href = cv.toDataURL('image/png');
    a.click();
    toast('Card saved');
  }

  function wrapT(x, t, px, py, mw, lh) {
    var words = String(t).split(' '), line = '', yy = py, used = 0;
    for (var i = 0; i < words.length; i++) {
      var test = line + words[i] + ' ';
      if (x.measureText(test).width > mw && line) {
        x.fillText(line, px, yy);
        line = words[i] + ' ';
        yy += lh;
        used += lh;
      } else line = test;
    }
    x.fillText(line, px, yy);
    return used + lh;
  }

  /* ---------------------------------------------------------- save / load */
  function exportAll() {
    H.dl('handbook-data-' + H.today() + '.json',
      JSON.stringify(H.exportBlob(), null, 1), 'application/json');
    H.markExported();
    toast('Saved to file');
  }

  function importAll() {
    H.pickFile('.json', function (f) {
      var fr = new FileReader();
      fr.onload = function () {
        try {
          H.importState(fr.result);
          applyTheme();
          chrome();
          refresh();
          toast('Loaded');
        } catch (e) {
          modal('That file would not load',
            '<p style="margin:0">' + E(e.message) + '</p>' +
            '<p class="sm muted">A handbook save is the JSON file the Save button produces. ' +
            'A shopping-list export is a different shape and loads from the Shopping page.</p>',
            '<button class="b" data-close>OK</button>');
        }
      };
      fr.readAsText(f);
    });
  }

  H.PALETTE_ACTIONS = [
    { k: 'Do', nm: 'Save everything to a file', run: exportAll },
    { k: 'Do', nm: 'Load a saved file', run: importAll },
    { k: 'Do', nm: 'Generate a meal plan', run: function () { nav('plan'); setTimeout(generate, 120); } },
    { k: 'Do', nm: 'Build a shopping list from the plan', run: buildListFromPlan },
    { k: 'Do', nm: 'Generate a training split', run: function () { nav('training'); setTimeout(splitModal, 120); } },
    { k: 'Do', nm: 'Add my own recipe', run: ownRecipe },
    { k: 'Do', nm: 'Log a shift', run: function () { nav('financial/actual'); setTimeout(shiftEditor, 120); } },
    { k: 'Do', nm: 'Switch theme', run: cycleTheme }
  ];

  function cycleTheme() {
    var order = ['auto', 'light', 'dark'];
    var i = order.indexOf(S().theme || 'auto');
    S().theme = order[(i + 1) % order.length];
    H.save(true);
    applyTheme();
    if (parse().v === 'settings') refresh();
    toast('Theme: ' + (S().theme === 'auto' ? 'matching the system' : S().theme));
  }

  /* ---------------------------------------------------------- global events */
  document.addEventListener('click', function (e) {
    var el;
    function hit(sel) { return (el = e.target.closest(sel)); }

    if (hit('[data-nav]')) { nav(el.dataset.nav); return; }
    if (hit('[data-w]')) { S().who = el.dataset.w; H.save(true); refresh(); return; }

    if (hit('[data-fav]')) {
      e.stopPropagation();
      var id = el.dataset.fav, i = S().fav.indexOf(id);
      if (i >= 0) S().fav.splice(i, 1); else S().fav.push(id);
      H.save(true);
      // Toggle in place so the grid does not rebuild under the cursor.
      $$('[data-fav="' + id + '"]').forEach(function (b) {
        var isOn = S().fav.indexOf(id) >= 0;
        if (!b.classList.contains('fav')) return;
        b.classList.toggle('on', isOn);
        b.setAttribute('aria-pressed', isOn);
        b.textContent = isOn ? '★' : '☆';
        b.classList.remove('pop');
        void b.offsetWidth;
        b.classList.add('pop');
      });
      if (parse().v === 'r') refresh();
      return;
    }

    if (hit('[data-go]')) { nav('r/' + el.dataset.go); return; }
    if (hit('[data-log]')) {
      H.dayLog(H.today()).meals.push({ id: el.dataset.log, q: 1 });
      H.consumeFromPantry(el.dataset.log, 1);
      H.save(true);
      var mealId = el.dataset.log;
      toast('Logged to today', {
        action: 'Undo',
        onAction: function () {
          var meals = H.dayLog(H.today()).meals;
          for (var k = meals.length - 1; k >= 0; k--) {
            if (meals[k].id === mealId) { meals.splice(k, 1); break; }
          }
          H.save(true); refresh();
        }
      });
      return;
    }
    if (hit('[data-groc]')) {
      var n = H.addRecipeToShop(H.byId(el.dataset.groc));
      toast(n + ' ingredients added to ' + S().shop.active);
      return;
    }
    if (hit('[data-tolist]')) { listModal(el.dataset.tolist); return; }
    if (hit('[data-plan]')) { planPicker(el.dataset.plan); return; }
    if (hit('[data-photo]')) { pickPhoto(el.dataset.photo); return; }
    if (hit('[data-rmphoto]')) {
      delete S().photos[el.dataset.rmphoto];
      H.save(true); refresh();
      toast('Photo removed');
      return;
    }
    if (hit('[data-card]')) { cardPNG(H.byId(el.dataset.card)); return; }
    if (hit('[data-list]')) { S().shop.active = el.dataset.list; H.save(true); refresh(); return; }

    if (hit('[data-gt]')) {
      var idx = +el.dataset.gt;
      var item = H.curList().items[idx];
      if (item) {
        item.done = el.checked;
        H.save();
        // Update just this row rather than repainting the list.
        var row = el.closest('.gitem');
        if (row) row.classList.toggle('done', item.done);
        updateShopTotals();
      }
      return;
    }
    if (hit('[data-gd]')) {
      var gi = +el.dataset.gd;
      var removed = H.curList().items[gi];
      H.curList().items.splice(gi, 1);
      H.save(true); refresh();
      toast('Removed ' + (removed ? removed.name : 'item'), {
        action: 'Undo',
        onAction: function () {
          H.curList().items.splice(gi, 0, removed);
          H.save(true); refresh();
        }
      });
      return;
    }
    if (hit('[data-ge]')) { shopItemEditor(+el.dataset.ge); return; }
    if (hit('[data-ie]')) { ingEditor(el.dataset.ie); return; }
    if (hit('[data-pane]')) {
      var pk = el.dataset.pane, pg = H.ING(pk);
      H.ask({
        title: pg ? pg.n : 'Pantry item', label: 'Grams in stock',
        value: String(Math.round(S().pantry[pk].g))
      }).then(function (v) {
        if (v == null) return;
        S().pantry[pk].g = Math.max(0, H.num(v));
        if (!S().pantry[pk].g) delete S().pantry[pk];
        H.save(true); refresh();
      });
      return;
    }
    if (hit('[data-pand]')) {
      var dk = el.dataset.pand, back = S().pantry[dk];
      delete S().pantry[dk];
      H.save(true); refresh();
      toast('Removed', {
        action: 'Undo',
        onAction: function () { S().pantry[dk] = back; H.save(true); refresh(); }
      });
      return;
    }
    if (hit('[data-sess]')) { sessModal(+el.dataset.sess); return; }
    if (hit('[data-jobe]')) { jobEditor(el.dataset.jobe); return; }
    if (hit('[data-coste]')) { costEditor(el.dataset.coste); return; }
    if (hit('[data-shd]')) {
      S().fin.shifts = S().fin.shifts.filter(function (x) { return x.id !== el.dataset.shd; });
      H.save(true); refresh();
      return;
    }
    if (hit('[data-bpadd]')) { bpItemEditor(el.dataset.bpadd); return; }
    if (hit('[data-bpdel]')) {
      var bn = el.dataset.bpdel;
      H.confirmDanger({ title: 'Delete "' + bn + '"?', text: 'Every item on it goes too.' })
        .then(function (ok) {
          if (!ok) return;
          delete S().fin.purchases[bn];
          H.save(true); refresh();
        });
      return;
    }
    if (hit('[data-bpi]')) {
      var p = el.dataset.bpi.split('|');
      S().fin.purchases[p[0]].items.splice(+p[1], 1);
      H.save(true); refresh();
      return;
    }
    if (hit('[data-d]')) { H.calSel = el.dataset.d; refresh(); return; }
    if (hit('[data-evd]')) { H.dayLog(H.calSel).sched.splice(+el.dataset.evd, 1); H.save(true); refresh(); return; }
    if (hit('[data-spd]')) { H.dayLog(H.calSel).spend.splice(+el.dataset.spd, 1); H.save(true); refresh(); return; }
    if (hit('[data-mld]')) { H.dayLog(H.calSel).meals.splice(+el.dataset.mld, 1); H.save(true); refresh(); return; }
    if (hit('[data-tadd]')) { tmplEditor(+el.dataset.tadd); return; }
    if (hit('[data-td]')) {
      var q = el.dataset.td.split('|');
      S().sched.tmpl[q[0]].splice(+q[1], 1);
      H.save(true); refresh();
      return;
    }

    if (hit('#home')) { nav('meals'); return; }
    if (hit('#cmdBtn')) { H.openPalette(); return; }
    if (hit('#themeBtn')) { cycleTheme(); return; }
    if (hit('#menuBtn')) { nav('settings'); return; }
  });

  function updateShopTotals() {
    var tot = H.listTotals(H.curList().items);
    H.setText('#shopTodo', money0(tot.todo));
    H.setText('#shopGot', money0(tot.got));
    H.setText('#shopCount', tot.n);
  }

  /* Recipe cards are links, so they answer to Enter and Space as well as a click. */
  document.addEventListener('keydown', function (e) {
    var card = e.target.closest && e.target.closest('.rc');
    if (card && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      nav('r/' + card.dataset.go);
    }
  });

  /* ---------------------------------------------------------- shortcuts */
  document.addEventListener('keydown', function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable;

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      H.openPalette();
      return;
    }
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'p') {
      e.preventDefault();
      S().who = H.otherKey();
      H.save(true);
      refresh();
      toast('Showing ' + H.P().name);
      return;
    }
    if (typing || e.ctrlKey || e.metaKey || e.altKey) return;

    if (e.key === '/') { e.preventDefault(); H.openPalette(); return; }
    var i = ['1', '2', '3', '4', '5'].indexOf(e.key);
    if (i >= 0) { e.preventDefault(); nav(NAV[i][0]); }
  });

  /* ---------------------------------------------------------- boot */
  H.onSaveFail(function () {
    var use = H.storageUsed();
    toast('Storage is full (' + use.mb.toFixed(1) + ' MB). Save to a file, then remove some photos.', {
      action: 'Settings',
      onAction: function () { nav('settings'); },
      ms: 9000
    });
  });

  function backupNudge() {
    if (!S().prefs.remindBackup) return;
    var since = H.daysSinceExport();
    var hasData = Object.keys(S().days).length > 3 || S().mine.length || Object.keys(S().photos).length;
    if (!hasData) return;
    if (since !== null && since < 7) return;
    setTimeout(function () {
      toast(since === null
        ? 'Nothing is backed up yet. This all lives in one browser.'
        : 'Last backup was ' + since + ' days ago.', {
        action: 'Save now',
        onAction: exportAll,
        ms: 9000
      });
    }, 2500);
  }

  H.planOpts.slots = S().prefs.planSlots || 4;
  if (S().prefs.dayBudget != null) H.planOpts.budget = String(S().prefs.dayBudget);

  applyTheme();
  chrome();
  if (!location.hash) location.hash = '#/meals';
  route();
  backupNudge();

})(typeof window !== 'undefined' ? window : globalThis);
