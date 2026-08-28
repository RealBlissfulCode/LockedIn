/* ============================================================
   The Handbook - UI primitives

   Modals with a real focus trap, a toast stack, the charts, the
   command palette, and the small helpers views.js builds pages
   out of. Nothing here knows about recipes or money.
   ============================================================ */
(function (global) {
  'use strict';

  var H = global.Handbook;
  var E = H.E;

  /* ---------------------------------------------------------- dom */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function on(sel, ev, fn) { var e = $(sel); if (e) e.addEventListener(ev, fn); return e; }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  H.$ = $; H.$$ = $$; H.on = on;

  function setText(sel, v) { var e = $(sel); if (e) e.textContent = v; }
  H.setText = setText;

  /* ---------------------------------------------------------- toasts */
  var toastHost = null;
  function toast(msg, opts) {
    opts = opts || {};
    if (!toastHost) toastHost = $('#toasts');
    if (!toastHost) return;
    var t = el('div', 'toast');
    t.appendChild(document.createTextNode(msg));
    if (opts.action && opts.onAction) {
      var b = el('button', null, E(opts.action));
      b.onclick = function () { close(); opts.onAction(); };
      t.appendChild(b);
    }
    toastHost.appendChild(t);
    var timer = setTimeout(close, opts.ms || (opts.action ? 6000 : 2600));
    function close() {
      clearTimeout(timer);
      if (!t.parentNode) return;
      t.classList.add('out');
      setTimeout(function () { if (t.parentNode) t.remove(); }, 240);
    }
    // Never let a backlog of toasts stack past three.
    while (toastHost.children.length > 3) toastHost.firstChild.remove();
    return close;
  }
  H.toast = toast;

  /* ---------------------------------------------------------- download */
  function dl(name, text, mime) {
    var b = new Blob([text], { type: mime || 'text/plain' });
    var a = el('a');
    a.href = URL.createObjectURL(b);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1200);
  }
  H.dl = dl;

  function pickFile(accept, cb) {
    var i = el('input');
    i.type = 'file';
    i.accept = accept;
    i.style.display = 'none';
    document.body.appendChild(i);
    i.onchange = function () { if (i.files[0]) cb(i.files[0]); i.remove(); };
    i.click();
  }
  H.pickFile = pickFile;

  /* ---------------------------------------------------------- modal */
  var openModals = [];
  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),' +
    'textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  function modal(title, body, foot, opts) {
    opts = opts || {};
    var prev = document.activeElement;
    var m = el('div', 'mask' + (opts.maskClass ? ' ' + opts.maskClass : ''));
    m.setAttribute('role', 'dialog');
    m.setAttribute('aria-modal', 'true');
    m.setAttribute('aria-label', title || 'Dialog');
    m.innerHTML =
      '<div class="modal' + (opts.wide ? ' wide' : '') + (opts.cls ? ' ' + opts.cls : '') + '">' +
      (opts.bare ? '' :
        '<div class="mhead"><h3>' + E(title) + '</h3>' +
        '<button class="x" data-close aria-label="Close">&times;</button></div>') +
      '<div class="mbody">' + body + '</div>' +
      (foot ? '<div class="mfoot">' + foot + '</div>' : '') +
      '</div>';

    m.close = function () {
      var i = openModals.indexOf(m);
      if (i >= 0) openModals.splice(i, 1);
      m.remove();
      if (!openModals.length) document.body.style.removeProperty('overflow');
      if (opts.onClose) opts.onClose();
      if (prev && prev.focus) { try { prev.focus(); } catch (e) { } }
    };

    m.addEventListener('click', function (e) {
      if (e.target === m || (e.target.closest && e.target.closest('[data-close]'))) {
        e.preventDefault();
        m.close();
      }
    });

    // Focus trap: tab cycles inside the dialog instead of wandering into the
    // page behind it, which is what makes a modal usable from the keyboard.
    m.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var items = $$(FOCUSABLE, m).filter(function (n) { return n.offsetParent !== null; });
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    document.body.appendChild(m);
    document.body.style.overflow = 'hidden';
    openModals.push(m);

    var focusFirst = $(opts.focus || FOCUSABLE, m);
    if (focusFirst) setTimeout(function () { try { focusFirst.focus(); } catch (e) { } }, 30);
    return m;
  }
  H.modal = modal;

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && openModals.length) {
      e.preventDefault();
      openModals[openModals.length - 1].close();
    }
  });

  /* Promise-shaped replacements for prompt/confirm, so every dialog in the app
     looks like the app rather than like the browser. */
  function ask(opts) {
    return new Promise(function (resolve) {
      var body = (opts.text ? '<p class="sm muted" style="margin:0 0 14px">' + E(opts.text) + '</p>' : '') +
        '<label class="f"><span>' + E(opts.label || 'Value') + '</span>' +
        '<input id="askIn" value="' + E(opts.value || '') + '"' +
        (opts.placeholder ? ' placeholder="' + E(opts.placeholder) + '"' : '') + '></label>';
      var m = modal(opts.title || 'Name it', body,
        '<button class="b o" data-close>Cancel</button>' +
        '<button class="b" id="askOk">' + E(opts.ok || 'Save') + '</button>',
        { focus: '#askIn', onClose: function () { if (!done) resolve(null); } });
      var done = false;
      function submit() {
        var v = $('#askIn', m).value.trim();
        if (!v) { $('#askIn', m).focus(); return; }
        done = true; m.close(); resolve(v);
      }
      $('#askOk', m).onclick = submit;
      $('#askIn', m).addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); submit(); }
      });
    });
  }
  H.ask = ask;

  function confirmDanger(opts) {
    return new Promise(function (resolve) {
      var m = modal(opts.title || 'Are you sure?',
        '<p style="margin:0">' + E(opts.text || '') + '</p>',
        '<button class="b o" data-close>Cancel</button>' +
        '<button class="b ' + (opts.safe ? '' : 'dz') + '" id="okBtn">' +
        E(opts.ok || 'Delete') + '</button>',
        { focus: '#okBtn', onClose: function () { if (!done) resolve(false); } });
      var done = false;
      $('#okBtn', m).onclick = function () { done = true; m.close(); resolve(true); };
    });
  }
  H.confirmDanger = confirmDanger;

  /* ---------------------------------------------------------- form bits */
  function opt(list, sel) {
    return list.map(function (o) {
      return '<option value="' + E(o[0]) + '"' +
        (String(o[0]) === String(sel) ? ' selected' : '') + '>' + E(o[1]) + '</option>';
    }).join('');
  }
  H.opt = opt;

  function form(fields) {
    return '<div class="fr">' + fields.map(function (f) {
      var wide = f.wide ? ' wide' : '';
      if (f.t === 'select') {
        return '<label class="f' + wide + '"><span>' + E(f.l) + '</span>' +
          '<select id="' + f.id + '">' + opt(f.o, f.v) + '</select>' +
          (f.hint ? '<span class="hint">' + E(f.hint) + '</span>' : '') + '</label>';
      }
      if (f.t === 'area') {
        return '<label class="f wide"><span>' + E(f.l) + '</span>' +
          '<textarea id="' + f.id + '" rows="' + (f.rows || 3) + '"' +
          (f.ph ? ' placeholder="' + E(f.ph) + '"' : '') + '>' + E(f.v || '') + '</textarea>' +
          (f.hint ? '<span class="hint">' + E(f.hint) + '</span>' : '') + '</label>';
      }
      return '<label class="f' + wide + '"><span>' + E(f.l) + '</span>' +
        '<input id="' + f.id + '" type="' + (f.t || 'text') + '"' +
        (f.step ? ' step="' + f.step + '"' : '') +
        (f.min != null ? ' min="' + f.min + '"' : '') +
        (f.max != null ? ' max="' + f.max + '"' : '') +
        ' value="' + E(f.v == null ? '' : f.v) + '"' +
        (f.ph ? ' placeholder="' + E(f.ph) + '"' : '') + '>' +
        (f.hint ? '<span class="hint">' + E(f.hint) + '</span>' : '') + '</label>';
    }).join('') + '</div>';
  }
  H.form = form;


  function switchRow(id, title, sub, checked) {
    return '<div class="swrow"><div class="t"><b>' + E(title) + '</b>' +
      (sub ? '<span>' + E(sub) + '</span>' : '') + '</div>' +
      '<button class="sw" id="' + id + '" role="switch" aria-checked="' +
      (checked ? 'true' : 'false') + '" aria-label="' + E(title) + '"></button></div>';
  }
  H.switchRow = switchRow;

  /* ---------------------------------------------------------- charts */
  /* All charts are hand-built inline SVG. One y-scale, thin marks, recessive
     grid, direct labels where they fit, and a hover tooltip. Series colours come
     from the --s1..--s4 tokens, which were validated for colour-blind
     separation against both surfaces. */

  function niceMax(v) {
    if (v <= 0) return 1;
    var mag = Math.pow(10, Math.floor(Math.log(v) / Math.LN10));
    var n = v / mag;
    var step = n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10;
    return step * mag;
  }

  /* A single-series line with a soft area under it. No legend: the title names
     the series. */
  function lineChart(points, opts) {
    opts = opts || {};
    if (!points || points.length < 2) {
      return '<p class="empty sm" style="padding:28px 0">' +
        E(opts.empty || 'Not enough data yet.') + '</p>';
    }
    var W = 100, Hh = opts.height || 46;
    var pad = { t: 4, b: 12, l: 0, r: 0 };
    var ys = points.map(function (p) { return p.y; });
    var lo = Math.min.apply(null, ys), hi = Math.max.apply(null, ys);
    if (hi === lo) { hi = lo + 1; lo = lo - 1; }
    var span = hi - lo;
    lo -= span * 0.12; hi += span * 0.12;

    function X(i) { return pad.l + (i / (points.length - 1)) * (W - pad.l - pad.r); }
    function Y(v) { return pad.t + (1 - (v - lo) / (hi - lo)) * (Hh - pad.t - pad.b); }

    var d = points.map(function (p, i) { return (i ? 'L' : 'M') + X(i).toFixed(2) + ' ' + Y(p.y).toFixed(2); }).join(' ');
    var area = d + ' L' + X(points.length - 1).toFixed(2) + ' ' + (Hh - pad.b) +
      ' L' + X(0).toFixed(2) + ' ' + (Hh - pad.b) + ' Z';
    var color = opts.color || 'var(--s1)';
    var last = points[points.length - 1], first = points[0];

    return '<div class="chartwrap" data-chart="line">' +
      '<svg class="chart" viewBox="0 0 ' + W + ' ' + Hh + '" preserveAspectRatio="none" ' +
      'role="img" aria-label="' + E(opts.label || 'Trend') + '" style="height:' + (opts.px || 150) + 'px">' +
      '<defs><linearGradient id="lg' + (opts.uid || '0') + '" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="' + color + '" stop-opacity=".22"/>' +
      '<stop offset="1" stop-color="' + color + '" stop-opacity="0"/></linearGradient></defs>' +
      '<path d="' + area + '" fill="url(#lg' + (opts.uid || '0') + ')"/>' +
      '<path class="lin" d="' + d + '" stroke="' + color + '" vector-effect="non-scaling-stroke"/>' +
      points.map(function (p, i) {
        return '<circle class="dotm" cx="' + X(i).toFixed(2) + '" cy="' + Y(p.y).toFixed(2) +
          '" r="1.6" fill="' + color + '" vector-effect="non-scaling-stroke" ' +
          'data-tip="' + E((opts.fmt ? opts.fmt(p) : p.y) + ' · ' + H.shortD(p.x)) + '"/>';
      }).join('') +
      '</svg>' +
      '<div class="spread xs muted" style="margin-top:4px">' +
      '<span>' + E(H.shortD(first.x)) + '</span>' +
      '<span class="num"><b style="color:var(--ink)">' +
      E(opts.fmt ? opts.fmt(last) : last.y) + '</b> ' + E(H.shortD(last.x)) + '</span></div>' +
      '<div class="tip" data-tipbox></div></div>';
  }
  H.lineChart = lineChart;

  /* Grouped bars. Up to three series, always with a legend, and the values are
     direct-labelled on the tallest bar of each group when they fit. */
  function barChart(groups, series, opts) {
    opts = opts || {};
    if (!groups.length) {
      return '<p class="empty sm" style="padding:28px 0">' +
        E(opts.empty || 'Nothing logged yet.') + '</p>';
    }
    var maxV = 0;
    groups.forEach(function (g) {
      series.forEach(function (s) { maxV = Math.max(maxV, g.v[s.key] || 0); });
    });
    maxV = niceMax(maxV);

    var W = 100, Hh = 52, padB = 10, padT = 6;
    var gw = W / groups.length;
    var bw = Math.min(gw / (series.length + 0.8), 7);
    var plot = Hh - padB - padT;

    var ticks = [0, 0.5, 1].map(function (f) {
      var y = padT + (1 - f) * plot;
      return '<line class="gridline" x1="0" y1="' + y.toFixed(2) + '" x2="' + W +
        '" y2="' + y.toFixed(2) + '" vector-effect="non-scaling-stroke"/>';
    }).join('');

    var bars = groups.map(function (g, gi) {
      var cx = gi * gw + gw / 2;
      var startX = cx - (series.length * bw + (series.length - 1) * 1) / 2;
      return series.map(function (s, si) {
        var v = g.v[s.key] || 0;
        var h = maxV ? (v / maxV) * plot : 0;
        var x = startX + si * (bw + 1);
        return '<rect class="barm" x="' + x.toFixed(2) + '" y="' + (padT + plot - h).toFixed(2) +
          '" width="' + bw.toFixed(2) + '" height="' + Math.max(h, 0.4).toFixed(2) +
          '" fill="' + s.color + '" data-tip="' + E(s.label + ' ' + (opts.fmt ? opts.fmt(v) : v) +
          ' · ' + g.label) + '"/>';
      }).join('');
    }).join('');

    var labels = groups.map(function (g, gi) {
      return '<text x="' + (gi * gw + gw / 2).toFixed(2) + '" y="' + (Hh - 2) +
        '" text-anchor="middle" style="font-size:3.4px">' + E(g.label) + '</text>';
    }).join('');

    return '<div class="chartwrap" data-chart="bar">' +
      '<svg class="chart" viewBox="0 0 ' + W + ' ' + Hh + '" preserveAspectRatio="none" ' +
      'role="img" aria-label="' + E(opts.label || 'Comparison') + '" ' +
      'style="height:' + (opts.px || 190) + 'px">' +
      ticks + bars + labels + '</svg>' +
      '<div class="legend">' + series.map(function (s) {
        return '<span><i style="background:' + s.color + '"></i>' + E(s.label) + '</span>';
      }).join('') + '</div>' +
      '<div class="tip" data-tipbox></div></div>';
  }
  H.barChart = barChart;

  /* The macro donut on a recipe card. Segments are separated by a 2px surface
     gap so adjacent fills never blur into one another. */
  function ringSVG(r) {
    var tot = r.p * 4 + r.c * 4 + r.f * 9 || 1;
    var C = 2 * Math.PI * 15.9155;
    var segs = [[r.p * 4 / tot, '#1F4D3A'], [r.c * 4 / tot, '#C2860E'], [r.f * 9 / tot, '#5C4A78']];
    var off = 25, h = '';
    segs.forEach(function (s) {
      var L = Math.max(s[0] * C - 1.2, 0);
      h += '<circle cx="18" cy="18" r="15.9155" fill="none" stroke="' + s[1] + '" stroke-width="4.4" ' +
        'stroke-dasharray="' + L.toFixed(2) + ' ' + (C - L).toFixed(2) +
        '" stroke-dashoffset="' + off.toFixed(2) + '"/>';
      off -= s[0] * C;
    });
    return '<svg class="ring" viewBox="0 0 36 36" width="58" height="58" aria-hidden="true">' +
      '<circle cx="18" cy="18" r="15.9155" fill="rgba(255,255,255,.14)" ' +
      'stroke="rgba(255,255,255,.22)" stroke-width="4.4"/>' + h +
      '<text x="18" y="19.4" text-anchor="middle" font-size="8.2" font-weight="800" fill="#fff">' +
      Math.round(r.k) + '</text>' +
      '<text x="18" y="25" text-anchor="middle" font-size="4.2" font-weight="700" ' +
      'fill="rgba(255,255,255,.8)">KCAL</text></svg>';
  }
  H.ringSVG = ringSVG;

  /* One delegated handler drives every chart tooltip on the page. */
  document.addEventListener('mouseover', function (e) {
    var mark = e.target.closest && e.target.closest('[data-tip]');
    if (!mark) return;
    var wrap = mark.closest('.chartwrap');
    if (!wrap) return;
    var box = wrap.querySelector('[data-tipbox]');
    if (!box) return;
    var wr = wrap.getBoundingClientRect(), mr = mark.getBoundingClientRect();
    box.textContent = mark.getAttribute('data-tip');
    box.style.left = (mr.left - wr.left + mr.width / 2) + 'px';
    box.style.top = (mr.top - wr.top) + 'px';
    box.classList.add('on');
  });
  document.addEventListener('mouseout', function (e) {
    var mark = e.target.closest && e.target.closest('[data-tip]');
    if (!mark) return;
    var wrap = mark.closest('.chartwrap');
    var box = wrap && wrap.querySelector('[data-tipbox]');
    if (box) box.classList.remove('on');
  });

  /* ---------------------------------------------------------- tables */
  /* A table wider than a phone is not a table any more: the right-hand columns
     simply vanish with nothing to say they are there. Cells carry their column
     name, and below 720px CSS restacks each row as a labelled card.

     cols: [{h: 'Header', cls, hide}]  rows: [[cell, cell, ...]] */
  var tableSeq = 0;
  var tableStore = {};

  function table(cols, rows, opts) {
    opts = opts || {};
    if (!rows.length) {
      return empty(opts.emptyTitle || 'Nothing here yet.', opts.emptySub, opts.emptyAction);
    }
    /* Restacked as cards, a forty-row table becomes a very long page. Long ones
       show a first page and a button for the rest. */
    if (opts.limit && rows.length > opts.limit) {
      var id = 't' + (++tableSeq);
      tableStore[id] = { cols: cols, rows: rows, opts: opts, shown: opts.limit };
      return '<div data-tablehost="' + id + '">' +
        renderTable(cols, rows.slice(0, opts.limit), opts) +
        '<div class="row" style="justify-content:center;margin-top:14px">' +
        '<button class="b o" data-tablemore="' + id + '">Show the other ' +
        (rows.length - opts.limit) + '</button></div></div>';
    }
    return renderTable(cols, rows, opts);
  }

  function renderTable(cols, rows, opts) {
    return '<div class="tw"><table>' +
      '<thead><tr>' + cols.map(function (c) {
        return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + '>' + E(c.h || '') + '</th>';
      }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) {
        var attrs = r.attrs || '';
        var cells = r.cells || r;
        return '<tr' + (attrs ? ' ' + attrs : '') + '>' + cells.map(function (cell, i) {
          var c = cols[i] || {};
          return '<td' + (c.cls ? ' class="' + c.cls + '"' : '') +
            (c.h ? ' data-l="' + E(c.h) + '"' : '') +
            (c.hide ? ' data-hide="1"' : '') + '>' + cell + '</td>';
        }).join('') + '</tr>';
      }).join('') +
      '</tbody></table></div>';
  }
  H.table = table;

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-tablemore]');
    if (!b) return;
    var st = tableStore[b.dataset.tablemore];
    if (!st) return;
    var host = b.closest('[data-tablehost]');
    st.shown = st.rows.length;
    host.innerHTML = renderTable(st.cols, st.rows, st.opts);
  });

  /* ---------------------------------------------------------- menus */
  /* One primary button and a menu beats nine pills in a row. The menu is a
     sheet on a phone and a popover on a pointer device. */
  var openMenu = null;

  function closeMenu() {
    if (!openMenu) return;
    openMenu.remove();
    openMenu = null;
  }
  H.closeMenu = closeMenu;

  function menu(anchor, items) {
    closeMenu();
    var m = el('div', 'menumask');
    var list = el('div', 'menu');
    list.setAttribute('role', 'menu');
    items.forEach(function (it) {
      if (it.sep) { list.appendChild(el('div', 'menusep')); return; }
      var b = el('button', 'menuitem' + (it.danger ? ' danger' : ''));
      b.type = 'button';
      b.setAttribute('role', 'menuitem');
      b.innerHTML = '<span>' + E(it.label) + '</span>' +
        (it.hint ? '<em>' + E(it.hint) + '</em>' : '');
      b.onclick = function () { closeMenu(); it.run(); };
      list.appendChild(b);
    });
    m.appendChild(list);
    m.addEventListener('click', function (e) { if (e.target === m) closeMenu(); });
    document.body.appendChild(m);
    openMenu = m;

    // Popover next to the button when there is room; the CSS turns it into a
    // bottom sheet on narrow screens.
    if (anchor && global.innerWidth > 700) {
      var r = anchor.getBoundingClientRect();
      list.style.position = 'fixed';
      list.style.minWidth = Math.max(r.width, 210) + 'px';
      var top = r.bottom + 8;
      var lh = Math.min(items.length * 44 + 16, 420);
      if (top + lh > global.innerHeight - 12) top = Math.max(12, r.top - lh - 8);
      list.style.top = top + 'px';
      list.style.left = Math.min(r.left, global.innerWidth - 250) + 'px';
      list.style.maxHeight = (global.innerHeight - top - 16) + 'px';
    }
    var first = list.querySelector('.menuitem');
    if (first) setTimeout(function () { try { first.focus(); } catch (e) { } }, 20);
    return m;
  }
  H.menu = menu;

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && openMenu) { e.preventDefault(); closeMenu(); }
  });

  /* ---------------------------------------------------------- action bar */
  /* actions: [{label, id, run, primary, danger, keep}]
     Anything without `primary` or `keep` folds into the More menu. */
  var actionRegistry = {};

  function actionBar(id, actions, opts) {
    opts = opts || {};
    actionRegistry[id] = actions;
    var shown = actions.filter(function (a) { return a.primary || a.keep; });
    var rest = actions.filter(function (a) { return !a.primary && !a.keep; });
    return '<div class="actions" data-actions="' + id + '">' +
      shown.map(function (a, i) {
        return '<button class="b' + (a.primary ? '' : ' o') + (a.danger ? ' dz' : '') +
          '" data-act="' + id + '|' + actions.indexOf(a) + '">' + E(a.label) + '</button>';
      }).join('') +
      (rest.length
        ? '<button class="b o more" data-more="' + id + '" aria-haspopup="menu">' +
        E(opts.moreLabel || 'More') +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M6 9l6 6 6-6"/></svg></button>'
        : '') +
      '</div>';
  }
  H.actionBar = actionBar;

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-act]');
    if (b) {
      var p = b.dataset.act.split('|');
      var a = (actionRegistry[p[0]] || [])[+p[1]];
      if (a && a.run) a.run();
      return;
    }
    var mb = e.target.closest && e.target.closest('[data-more]');
    if (mb) {
      var list = (actionRegistry[mb.dataset.more] || [])
        .filter(function (a) { return !a.primary && !a.keep; });
      menu(mb, list.map(function (a) {
        return { label: a.label, hint: a.hint, danger: a.danger, run: a.run };
      }));
    }
  });

  /* ---------------------------------------------------------- shared bits */
  function statRow(t) {
    return '<div class="stats s6">' +
      '<div class="stat acc"><b>' + t.kcal.toLocaleString() + '</b><span>Calories</span></div>' +
      '<div class="stat"><b>' + t.p + 'g</b><span>Protein</span></div>' +
      '<div class="stat"><b>' + t.c + 'g</b><span>Carbs</span></div>' +
      '<div class="stat"><b>' + t.f + 'g</b><span>Fat</span></div>' +
      '<div class="stat"><b>' + t.fib + 'g</b><span>Fiber</span></div>' +
      '<div class="stat"><b>' + t.w + 'oz</b><span>Water</span></div></div>';
  }
  H.statRow = statRow;

  function bar(label, have, need, cls) {
    var pct = need ? have / need * 100 : 0;
    var over = pct > 108;
    return '<div class="mrow"><div class="spread"><span>' + E(label) + '</span>' +
      '<em>' + Math.round(have) + ' / ' + Math.round(need) + '</em></div>' +
      '<div class="bar" role="img" aria-label="' + E(label) + ', ' + Math.round(pct) +
      ' percent of target"><i class="' + (over ? 'pbad over' : cls) +
      '" data-w="' + Math.min(100, pct).toFixed(1) + '"></i></div></div>';
  }

  /* Bars are rendered at zero width and given their real width on the next
     frame, which is what lets the CSS transition actually run. */
  function fillBars(root) {
    var bars = $$('.bar i[data-w]', root || document);
    if (!bars.length) return;
    requestAnimationFrame(function () {
      bars.forEach(function (n) { n.style.width = n.getAttribute('data-w') + '%'; });
    });
  }
  H.fillBars = fillBars;
  H.bar = bar;

  function stat(value, label, cls, id) {
    return '<div class="stat' + (cls ? ' ' + cls : '') + '">' +
      '<b' + (id ? ' id="' + id + '"' : '') + '>' + value + '</b>' +
      '<span>' + E(label) + '</span></div>';
  }
  H.stat = stat;

  function empty(title, sub, action) {
    return '<div class="empty"><p>' + E(title) + '</p>' +
      (sub ? '<p class="sm">' + E(sub) + '</p>' : '') +
      (action || '') + '</div>';
  }
  H.empty = empty;

  /* Staggers direct children in, capped so a 251-card grid does not spend two
     seconds animating. */
  function stagger(host) {
    if (!host) return;
    host.classList.add('stag');
    [].slice.call(host.children).forEach(function (c, i) {
      c.style.setProperty('--i', Math.min(i, 14));
    });
  }
  H.stagger = stagger;

  /* ---------------------------------------------------------- palette */
  /* Ctrl/Cmd-K. Searches every recipe, exercise, shopping list and action in
     one box, so nothing in the app is more than two keystrokes away. */
  var paletteOpen = false;

  function paletteItems() {
    var S = H.state(), items = [];
    H.NAV.forEach(function (t) {
      items.push({ k: 'Go', nm: t[1], meta: '', go: t[0] });
    });
    items.push({ k: 'Go', nm: 'Profile and settings', go: 'settings' });
    items.push({ k: 'Go', nm: 'Meal plan', go: 'plan' });
    items.push({ k: 'Go', nm: 'Pantry', go: 'shopping/pantry' });
    items.push({ k: 'Go', nm: 'Ingredient list', go: 'shopping/ingredients' });
    items.push({ k: 'Go', nm: 'Exercise database', go: 'training/exercises' });
    items.push({ k: 'Go', nm: 'Actual earnings', go: 'financial/actual' });

    H.PALETTE_ACTIONS.forEach(function (a) { items.push(a); });

    H.all().forEach(function (r) {
      items.push({
        k: 'Recipe', nm: r.n, go: 'r/' + r.id,
        meta: Math.round(r.k) + ' kcal · ' + Math.round(r.p) + 'g P · ' + H.money(H.cps(r))
      });
    });
    H.EX.forEach(function (x) {
      items.push({ k: 'Exercise', nm: x.n, meta: x.mg, ex: x.n });
    });
    Object.keys(S.shop.lists).forEach(function (n) {
      items.push({ k: 'List', nm: n, meta: S.shop.lists[n].items.length + ' items', list: n });
    });
    return items;
  }

  function score(q, s) {
    s = s.toLowerCase();
    var i = s.indexOf(q);
    if (i === 0) return 100;
    if (i > 0) return 60 - Math.min(i, 30);
    // Fall back to a loose subsequence match so "chkbowl" still finds one.
    var qi = 0;
    for (var si = 0; si < s.length && qi < q.length; si++) if (s[si] === q[qi]) qi++;
    return qi === q.length ? 20 : -1;
  }

  function openPalette() {
    if (paletteOpen) return;
    paletteOpen = true;
    var all = paletteItems();
    var m = modal('Search', '', null, {
      bare: true, cls: 'cmd', maskClass: 'cmdmask',
      onClose: function () { paletteOpen = false; }
    });
    $('.mbody', m).outerHTML =
      '<input id="cmdq" placeholder="Search recipes, exercises, pages, actions..." ' +
      'autocomplete="off" spellcheck="false" aria-label="Search everything">' +
      '<div class="cmdlist" id="cmdlist" role="listbox"></div>';

    var input = $('#cmdq', m), list = $('#cmdlist', m), cursor = 0, shown = [];

    function draw() {
      var q = input.value.trim().toLowerCase();
      shown = (!q ? all.slice(0, 12) : all.map(function (it) {
        return { it: it, s: score(q, it.nm) + (it.k === 'Go' || it.k === 'Do' ? 8 : 0) };
      }).filter(function (o) { return o.s > 0; })
        .sort(function (a, b) { return b.s - a.s; })
        .slice(0, 40)
        .map(function (o) { return o.it; }));

      cursor = 0;
      list.innerHTML = shown.length ? shown.map(function (it, i) {
        return '<button class="cmdrow' + (i === 0 ? ' cursor' : '') + '" data-i="' + i + '" role="option">' +
          '<span class="k">' + E(it.k) + '</span>' +
          '<span class="nm">' + E(it.nm) + '</span>' +
          (it.meta ? '<span class="meta">' + E(it.meta) + '</span>' : '') + '</button>';
      }).join('') : '<p class="empty sm">Nothing matches.</p>';
    }

    function move(d) {
      if (!shown.length) return;
      cursor = (cursor + d + shown.length) % shown.length;
      $$('.cmdrow', list).forEach(function (n, i) { n.classList.toggle('cursor', i === cursor); });
      var node = $$('.cmdrow', list)[cursor];
      if (node) node.scrollIntoView({ block: 'nearest' });
    }

    function run(it) {
      m.close();
      if (!it) return;
      if (it.go) H.nav(it.go);
      else if (it.ex) { H.nav('training/exercises'); setTimeout(function () { H.focusExercise(it.ex); }, 60); }
      else if (it.list) { H.state().shop.active = it.list; H.save(); H.nav('shopping'); }
      else if (it.run) it.run();
    }

    input.addEventListener('input', draw);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); run(shown[cursor]); }
    });
    list.addEventListener('click', function (e) {
      var row = e.target.closest('[data-i]');
      if (row) run(shown[+row.dataset.i]);
    });

    draw();
    input.focus();
  }
  H.openPalette = openPalette;

  /* ---------------------------------------------------------- connection */
  /* The app works entirely offline, so losing the connection is worth a quiet
     note rather than an error: the only thing that stops is picking up a new
     deploy. */
  var offlineNote = null;

  function showOffline() {
    if (offlineNote || navigator.onLine !== false) return;
    offlineNote = el('div', 'banner');
    offlineNote.style.background = 'var(--ink)';
    offlineNote.style.color = 'var(--paper)';
    offlineNote.innerHTML = '<span>Offline. Everything still works — it all lives here.</span>';
    document.body.appendChild(offlineNote);
  }

  function hideOffline() {
    if (!offlineNote) return;
    offlineNote.remove();
    offlineNote = null;
  }

  global.addEventListener('offline', showOffline);
  global.addEventListener('online', function () {
    hideOffline();
    toast('Back online');
  });
  if (navigator.onLine === false) showOffline();

  /* ---------------------------------------------------------- update prompt */
  var updateBanner = null;
  H.updateReady = function (accept) {
    if (updateBanner) return;
    updateBanner = el('div', 'banner');
    updateBanner.innerHTML = '<span>A newer version is ready.</span>' +
      '<button type="button">Reload</button>';
    updateBanner.querySelector('button').onclick = function () {
      updateBanner.remove();
      accept();
    };
    document.body.appendChild(updateBanner);
    setTimeout(function () {
      if (updateBanner) { updateBanner.remove(); updateBanner = null; }
    }, 20000);
  };

})(typeof window !== 'undefined' ? window : globalThis);
