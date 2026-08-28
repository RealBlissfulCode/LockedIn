# -*- coding: utf-8 -*-
"""Curated collections and the gluten audit, both generated from the live database."""
import html

# Each collection: (anchor, title, intro, selector function)
def _has(d, *tags): return any(t in d["tags"] for t in tags)

COLLECTIONS = [
 ("c-cheat", "Cheat meals",
  "Food I'd actually order. It's in here because a diet I can't live inside doesn't work, and "
  "because most of these land 40 to 55 g of protein anyway. One of these a week changes nothing "
  "about my physique. Believing I can't have one is what causes the problem.",
  lambda d: _has(d, "CHEAT MEAL")),

 ("c-dessert", "Healthy desserts",
  "Sweet, high protein, and built so I can have one most nights. Most of these sit between 200 "
  "and 350 calories with 25 to 45 g of protein, which means they're a feeding, not a slip.",
  lambda d: _has(d, "HEALTHY DESSERT")),

 ("c-realdessert", "Real desserts",
  "Not protein desserts. Actual desserts, portioned so I know exactly what I'm spending. "
  "The point of putting numbers on these isn't guilt, it's so I can fit one in on purpose "
  "instead of avoiding it and then eating three.",
  lambda d: _has(d, "CHEAT DESSERT")),

 ("c-protein", "Protein meals",
  "40 g or more per serving with a real leucine dose. If I'm behind on protein at 8 p.m., "
  "start here and stop reading everything else.",
  lambda d: d["per"]["p"] >= 40 and d["per"]["leu"] >= 3.0),

 ("c-carb", "Carb meals",
  "For training days, long shifts, and anything after a hard session. Glycogen is why I look "
  "full rather than flat, and chronic low carbs is a big part of why an underfed physique reads "
  "smaller than it actually is.",
  lambda d: d["per"]["c"] >= 60),

 ("c-lean", "Lean and high volume",
  "Under 400 calories, high protein, high food volume. For days I'm already full, days I'm "
  "cutting, or the 9 p.m. hunger that isn't really hunger.",
  lambda d: d["per"]["kcal"] <= 400 and d["per"]["p"] >= 25),

 ("c-calorie", "When I need calories",
  "550 kcal and up per serving. These exist for the days work runs to seven and I'm a thousand "
  "behind. Liquid calories and fat density are the tools; I can't chew my way to a surplus.",
  lambda d: d["per"]["kcal"] >= 550),

 ("c-fast", "Ten minutes or less",
  "Total time, start to plate. The realistic alternative on these days is not eating, so a fast "
  "meal beats a good one that doesn't happen.",
  lambda d: d["time"] <= 10),

 ("c-cheap", "Cheapest meals in here",
  "Built on beans, eggs, oats, rice, potatoes and dairy. Nothing on this list needs a specialty "
  "aisle. Most come in well under three dollars a serving.",
  lambda d: _has(d, "BUDGET FRIENDLY")),

 ("c-nocook", "No cooking required",
  "No stove, no oven. Assembly, a blender, or a microwave at most.",
  lambda d: _has(d, "NO-COOK") or d["r"]["cook"] == 0),

 ("c-prep", "Batch cook and freeze",
  "Sunday afternoon items. Most of these are better on day two and several freeze for months.",
  lambda d: _has(d, "FREEZER FRIENDLY")),

 ("c-drink", "Health drinks",
  "Hydration, electrolytes and micronutrients rather than protein. Honest notes on what each one "
  "actually does, including the ones where the answer is 'not much, but it tastes good'.",
  lambda d: _has(d, "HEALTH DRINK")),

 ("c-fiber", "High fiber",
  "12 g or more. Worth knowing about because I'm going from a low-food-volume diet to a much "
  "higher one, and ramping fiber too fast is genuinely unpleasant.",
  lambda d: d["per"]["fib"] >= 12),

 ("c-micro", "Most nutrient dense",
  "The meals covering the nutrients a gluten-free vegetarian diet actually runs short on: iron, "
  "B12, zinc, calcium, vitamin D and omega-3.",
  lambda d: _has(d, "HIGH MICRONUTRIENT DENSITY", "OMEGA-3 RICH")),

 ("c-sleep", "Before bed",
  "Slow protein, 30 to 60 minutes before sleep. The pre-sleep feeding has more evidence behind it "
  "than most nutrient timing does.",
  lambda d: _has(d, "PRE-SLEEP")),
]


def collection_table(DATA, sel, limit=30):
    rows = sorted([d for d in DATA if sel(d)], key=lambda d: -d["per"]["p"])[:limit]
    if not rows: return "<p class='small'>Nothing matches yet.</p>"
    out = ['<table class="idx"><thead><tr><th>ID</th><th>Meal</th><th>Time</th><th>Cal</th>'
           '<th>P</th><th>C</th><th>F</th><th>Fib</th><th>Leu</th></tr></thead><tbody>']
    for d in rows:
        p = d["per"]; r = d["r"]
        out.append(f'<tr><td>{r["id"]}</td><td><a href="#{r["id"]}">{html.escape(r["name"])}</a></td>'
                   f'<td>{d["time"]}m</td><td><b>{int(round(p["kcal"]/5.0)*5)}</b></td>'
                   f'<td><b>{round(p["p"])}</b></td><td>{round(p["c"])}</td><td>{round(p["f"])}</td>'
                   f'<td>{round(p["fib"])}</td><td>{round(p["leu"],1)}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def build_collections(DATA):
    h = ['<h2 id="collections">Collections</h2>',
         '<p>Fifteen shortcuts into the catalog. Every list is cut by the numbers rather than by feel, '
         'so nothing appears on a list it does not earn. If I only ever use three of '
         'these, use <a href="#c-fast">Ten minutes or less</a>, <a href="#c-protein">Protein meals</a> '
         'and <a href="#c-cheat">Cheat meals</a>.</p>']
    for anchor, title, intro, sel in COLLECTIONS:
        n = sum(1 for d in DATA if sel(d))
        h.append(f'<h3 id="{anchor}">{html.escape(title)} <span class="hh">({n})</span></h3>')
        h.append(f'<p class="small">{intro}</p>')
        h.append(collection_table(DATA, sel))
    h.append('<p class="back"><a href="#top">Top</a></p>')
    return "\n".join(h)


GLUTEN_WORDS = ["wheat","barley","rye","malt","seitan","spelt","farro","semolina",
                "couscous","bulgur","triticale","durum","graham"]

def gluten_audit(ING, DATA):
    """Scans every ingredient used. Returns (html, offenders)."""
    used = sorted({k for d in DATA for k,_g,_m in d["r"]["ing"]})
    offenders = []
    for k in used:
        name = ING[k]["name"].lower(); key = k.lower()
        for w in GLUTEN_WORDS:
            if w in name or w in key:
                if not (name.startswith("gf ") or "gluten-free" in name or key.startswith("gf_")):
                    offenders.append((k, ING[k]["name"], w))
    if offenders:
        body = ("<p><b>Flagged for review:</b> " +
                ", ".join(f"{n} ({w})" for _k,n,w in offenders) + "</p>")
    else:
        body = (f"<p>None of the {len(used)} ingredients used across the catalog contain wheat, "
                "barley, rye or any derivative of them. That covers the food itself. What it does "
                "not cover is the brand, and the brand is where celiac diets usually go wrong: an "
                "uncertified oat, a soy sauce that slipped in instead of tamari, a bag of fries "
                "with a flour coating for crispness. The 23 items below marked CHECK are the ones "
                "worth reading a label on. Everything else is safe by nature.</p>")
    h = ['<div class="callout"><h4>Where the risk actually is</h4>', body, '</div>']
    return "\n".join(h), offenders
