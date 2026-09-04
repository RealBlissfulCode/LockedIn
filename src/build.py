# -*- coding: utf-8 -*-
"""Builds index.html. This is the only build script.

    python3 src/build.py              rebuild index.html
    python3 src/build.py --check      rebuild in memory, fail if index.html is stale

Everything the app knows about food and training comes from here: the recipes in
recipes_1..6, the nutrition table in ingredients.py, the shelf prices in prices.py,
the aisle map in ingredient_list.py, and the JSON files next to this script.
Macros are computed from gram weights, costs from the price table, tags from the
macros. Nothing is typed by hand into index.html.

Nothing personal is in here any more. The page ships the recipe book, the
exercise database and the application code, all of it generic. Everything about
a person arrives from the API after they sign in, which is the only way it can
work when the person is not us.
"""
import argparse
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from ingredients import ING                      # noqa: E402
from ingredient_list import AISLES               # noqa: E402
import prices as PR                              # noqa: E402
from recipes_1 import RECIPES_1                  # noqa: E402
from recipes_2 import RECIPES_2                  # noqa: E402
from recipes_3 import RECIPES_3                  # noqa: E402
from recipes_4 import RECIPES_4                  # noqa: E402
from recipes_5 import RECIPES_5                  # noqa: E402
from recipes_6 import RECIPES_6                  # noqa: E402
from app_core import APP_CORE                    # noqa: E402
from app_auth import APP_AUTH                    # noqa: E402
from app_state import APP_STATE                  # noqa: E402
from app_setup import APP_SETUP, APP_PLANNER, APP_HOUSEHOLD  # noqa: E402
from app_charts import APP_CHARTS                # noqa: E402
from app_views1 import APP_VIEWS1                # noqa: E402
from app_views2 import APP_VIEWS2                # noqa: E402
from app_wire import APP_WIRE                    # noqa: E402
from spa_css import APP_CSS                      # noqa: E402
from gate import GATE_HTML                       # noqa: E402

RECIPES = RECIPES_1 + RECIPES_2 + RECIPES_3 + RECIPES_4 + RECIPES_5 + RECIPES_6

NUTS = ["kcal", "p", "c", "f", "fib", "leu", "ca", "fe", "mg", "k", "zn", "na",
        "b12", "vitd", "ala", "epadha"]

DV = {"ca": 1300, "fe": 18, "mg": 420, "k": 4700, "zn": 11, "b12": 2.4, "vitd": 20}
MICRO_NAME = {"ca": "CALCIUM", "fe": "IRON", "mg": "MAGNESIUM",
              "k": "POTASSIUM", "zn": "ZINC"}

def compute(r):
    """Per-serving nutrition, summed from the gram weights of the ingredients."""
    tot = {n: 0.0 for n in NUTS}
    grams = 0.0
    for key, g, _measure in r["ing"]:
        if key not in ING:
            raise KeyError("%s: unknown ingredient %r" % (r["id"], key))
        item = ING[key]
        grams += g
        for n in NUTS:
            tot[n] += item[n] * g / 100.0
    s = max(r["servings"], 1)
    per = {n: tot[n] / s for n in NUTS}
    per["grams"] = grams / s
    return per


def satiety(per, cat):
    sc = 0.30 * per["p"] + 0.60 * per["fib"] + 0.01 * per["grams"] - (6 if cat == "Drink" else 0)
    lvl = "HIGH" if sc >= 16 else ("MEDIUM" if sc >= 9 else "LOWER")
    return round(sc, 1), lvl


def difficulty(r):
    t = r["prep"] + r["cook"]
    return ("EASY" if t <= 10 else ("MODERATE" if t <= 25 else "ADVANCED")), t


# Diet flags, worked out from the ingredient keys rather than typed per recipe.
# The signup questionnaire filters on these, so getting one wrong means somebody
# with an allergy gets shown food they cannot eat. Anything not clearly safe is
# treated as containing the thing.
DAIRY = {"milk_2", "milk_skim", "whey_isolate", "casein_powder", "greek_yogurt_0",
         "greek_yogurt_2", "cottage_cheese_2", "cottage_cheese_4", "cheddar", "feta",
         "mozzarella_part_skim", "parmesan", "cream_cheese_whipped", "butter",
         "ricotta_part_skim", "sour_cream_light", "string_cheese", "kefir_plain",
         "heavy_cream", "half_and_half", "ice_cream_vanilla", "milk_choc"}
EGG = {"egg_whole", "egg_white", "mayo_olive", "mayo_light"}
PEANUT = {"pb_powder", "peanut_butter", "peanuts", "pb2_choc"}
TREENUT = {"almonds", "almond_butter", "almond_milk_unsw", "cashews", "walnuts",
           "pecans", "pistachios", "almond_flour", "coconut_flour"}
SOY = {"edamame_shelled", "tofu_firm", "tempeh", "soy_sauce_gf", "soy_milk",
       "miso_paste", "tamari"}
FISH = {"canned_salmon", "canned_tuna", "cod", "salmon_fillet", "shrimp", "tilapia",
        "sardines", "fish_sauce", "worcestershire"}
MEAT = {"chicken_breast", "chicken_thigh", "ground_turkey_93", "ground_beef_90",
        "ground_beef_93", "steak_sirloin", "pork_tenderloin", "bacon_turkey",
        "deli_turkey", "rotisserie_chicken", "beef_jerky", "ham_deli", "sausage_chicken"}
CORN = {"corn_tortilla", "cornmeal_polenta", "cornstarch", "corn_kernels", "popcorn",
        "tortilla_chips", "corn_flour"}


def diet_flags(keys):
    """What a recipe is free of, from the ingredient keys it uses."""
    ks = set(keys)
    has_dairy = bool(ks & DAIRY)
    has_egg = bool(ks & EGG)
    has_fish = bool(ks & FISH)
    has_meat = bool(ks & MEAT)
    out = []
    if not (has_meat or has_fish):
        out.append("vegetarian")
        if not (has_dairy or has_egg):
            out.append("vegan")
    if not has_dairy:
        out.append("dairyfree")
    if not (ks & PEANUT):
        out.append("peanutfree")
    if not (ks & TREENUT):
        out.append("treenutfree")
    if not (ks & SOY):
        out.append("soyfree")
    if not has_egg:
        out.append("eggfree")
    if not (ks & CORN):
        out.append("cornfree")
    if not has_fish:
        out.append("fishfree")
    # Every recipe in the book is gluten free by construction, which is the
    # whole premise of the set, so it is asserted rather than derived.
    out.append("glutenfree")
    return out


def autotags(r, per, sat_lvl):
    t = []
    kcal, p, c, f = per["kcal"], per["p"], per["c"], per["f"]
    fib, leu = per["fib"], per["leu"]
    if p >= 40:
        t.append("VERY HIGH PROTEIN")
    elif p >= 30:
        t.append("HIGH PROTEIN")
    if leu >= 3.0:
        t.append("LEUCINE PRIORITY")
    elif leu >= 2.5:
        t.append("HIGH LEUCINE")
    if kcal >= 500:
        t.append("HIGH CALORIE")
    if kcal <= 300:
        t.append("LOW CALORIE")
    if fib >= 8:
        t.append("HIGH FIBER")
    if f >= 20:
        t.append("HIGH HEALTHY FAT")
    if c >= 50 and kcal > 0 and (c * 4) / kcal >= 0.50:
        t.append("HIGH CARB")
    if c <= 25:
        t.append("LOW CARB")
    if kcal > 0:
        pp, cp, fp = p * 4 / kcal, c * 4 / kcal, f * 9 / kcal
        if 0.20 <= pp <= 0.40 and 0.30 <= cp <= 0.55 and 0.20 <= fp <= 0.40:
            t.append("BALANCED MACRO")
    if p >= 30 and leu >= 2.5:
        t.append("MUSCLE-BUILDING PRIORITY")
    if p >= 25 and c >= 40:
        t.append("POST-WORKOUT FRIENDLY")
    if c >= 30 and f < 15 and fib < 6:
        t.append("PRE-WORKOUT FRIENDLY")
    if sat_lvl == "HIGH":
        t.append("HIGH SATIETY")
    diff, total_min = difficulty(r)
    if diff == "EASY" and total_min <= 10:
        t.append("QUICK")
    if kcal >= 600 and p >= 35:
        t.append("TWO-MEAL-DAY FRIENDLY")
    for k in ("ca", "fe", "mg", "k", "zn"):
        if per[k] / DV[k] >= 0.20:
            t.append("HIGH " + MICRO_NAME[k])
    if per["epadha"] >= 0.5 or per["ala"] >= 2.5:
        t.append("OMEGA-3 RICH")
    if sum(1 for k in DV if per[k] / DV[k] >= 0.20) >= 4:
        t.append("HIGH MICRONUTRIENT DENSITY")
    if r["cat"] != "SDA Meat/Fish":
        t.append("VEGETARIAN")
    t.append("SDA-COMPATIBLE")
    t.append("GLUTEN-FREE")
    for m in r.get("manual_tags", []):
        t.append(m)
    seen, out = set(), []
    for x in t:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def validate(r, per):
    """Sanity checks that would otherwise ship silently wrong numbers."""
    issues = []
    atwater = per["p"] * 4 + per["c"] * 4 + per["f"] * 9 - per["fib"] * 2
    if per["kcal"] > 0:
        dev = abs(per["kcal"] - atwater) / per["kcal"]
        if dev > 0.15:
            issues.append("%s Atwater deviation %.0f%% (kcal %.0f vs %.0f)"
                          % (r["id"], dev * 100, per["kcal"], atwater))
    if per["p"] > 0 and per["leu"] / per["p"] > 0.13:
        issues.append("%s leucine fraction implausible" % r["id"])
    if not r["steps"]:
        issues.append("%s missing steps" % r["id"])
    if not r["ing"]:
        issues.append("%s missing ingredients" % r["id"])
    if r["servings"] < 1:
        issues.append("%s servings below one" % r["id"])
    return issues


def aisle_of(key):
    for name, keys in AISLES:
        if key in keys:
            return name
    return "Other"


# ------------------------------------------------------------------ assembly

def load_json(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def build_public():
    """Recipes, ingredients, exercises, sessions. Nothing personal in here."""
    recipes, issues = [], []
    for r in RECIPES:
        per = compute(r)
        _score, lvl = satiety(per, r["cat"])
        diff, total_min = difficulty(r)
        issues += validate(r, per)
        w, ws, missing_w = PR.cost_of(r, r["servings"], "walmart")
        c, cs, _missing_c = PR.cost_of(r, r["servings"], "costco")
        for key in missing_w:
            issues.append("%s no price for %s" % (r["id"], key))
        recipes.append({
            "id": r["id"], "n": r["name"], "cat": r["cat"], "sv": r["servings"],
            "t": total_min, "diff": diff,
            "k": round(per["kcal"]), "p": round(per["p"], 1), "c": round(per["c"], 1),
            "f": round(per["f"], 1), "fib": round(per["fib"], 1), "leu": round(per["leu"], 2),
            "tg": autotags(r, per, lvl),
            "df": diet_flags([i[0] for i in r["ing"]]),
            "cw": round(w, 2), "cws": round(ws, 2), "cc": round(c, 2), "ccs": round(cs, 2),
            "ing": [[m, k, g] for k, g, m in r["ing"]],
            "st": r["steps"], "storage": r.get("storage", ""), "prep": r.get("prep_notes", ""),
            "subs": r.get("subs", []), "vars": r.get("variations", []),
        })

    ids = [x["id"] for x in recipes]
    dupes = [k for k, n in Counter(ids).items() if n > 1]
    if dupes:
        issues.append("duplicate recipe ids: %s" % ", ".join(sorted(dupes)))

    ings = {}
    for key, v in ING.items():
        w, c = PR.PRICE.get(key, (None, None))
        ings[key] = {"n": v["name"], "a": aisle_of(key), "w": w, "c": c,
                     "k": v["kcal"], "p": v["p"], "cb": v["c"], "f": v["f"], "fib": v["fib"]}

    used = {i[1] for r in recipes for i in r["ing"]}
    for key in sorted(used - set(ings)):
        issues.append("recipes use %s but it is not in the ingredient table" % key)

    blob = {
        "recipes": recipes,
        "ing": ings,
        "aisles": [[a, k] for a, k in AISLES],
        "learn": [],
        "exercises": load_json("exercises.json"),
        "sessions": load_json("sessions.json"),
    }
    return blob, issues


# The whole page is public now, so this guard matters more than it used to, not
# less. If one of these reaches a build it means somebody typed something real
# into a file that is meant to hold nothing but examples.
FORBIDDEN = ["Aaliyah", "Jaron", "Ritchey", "CRMO", "Timnath", "Zoup", "MysticNoob",
             "CHFA", "Windsor", "Loveland", "Larimer", "Blissful", "Fort Collins"]


def check_public(public):
    """Fail loudly if anything identifying reached the unencrypted blob."""
    text = json.dumps(public)
    hits = []
    for word in FORBIDDEN:
        n = text.count(word)
        if n:
            i = text.find(word)
            hits.append("%s x%d  ...%s..." % (word, n, text[max(0, i - 70):i + 70]))
    return hits


SHELL_HEAD = (
    '<!DOCTYPE html><html lang="en" data-theme="dark"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<meta name="theme-color" content="#0A0A0C">'
    '<meta name="robots" content="noindex,nofollow">'
    '<title>LockedIn</title>'
    '<meta name="description" content="Private.">'
    '<meta name="apple-mobile-web-app-capable" content="yes">'
    '<meta name="apple-mobile-web-app-title" content="LockedIn">'
    '<link rel="manifest" href="manifest.webmanifest">'
    '<link rel="apple-touch-icon" href="icons/icon-192.png">'
    '<link rel="icon" href="icons/icon.svg" type="image/svg+xml">'
    '<link rel="icon" href="icons/icon-192.png" sizes="192x192">'
)

SHELL_BODY = (
    '</head><body>'
    + GATE_HTML +
    '<div id="app" hidden>'
    '<header class="top"><div class="topin">'
    '<div class="brand"><span>Locked<em>In</em></span></div>'
    '<div class="whoswitch" id="who"></div>'
    '<div id="syncSlot"></div>'
    '<nav class="tabs" id="tabs"></nav>'
    '<button class="iconbtn" id="themeBtn" title="Theme"></button>'
    '<button class="iconbtn" id="settings" title="Settings"></button>'
    '</div></header><main class="wrap" id="view"></main>'
    '<nav class="btmnav" id="btm"></nav>'
    '</div>'
)


def render_html():
    public, issues = build_public()

    leaks = check_public(public)
    if leaks:
        raise SystemExit("REFUSING TO BUILD: personal text in the shipped data\n  "
                         + "\n  ".join(leaks)
                         + "\n\nReword it in src/. Nothing personal belongs in a build now.")

    # Nothing is encrypted any more and nothing needs to be. Everything the page
    # carries is generic, and everything about a person arrives from the API
    # after they sign in.
    app_js = ("(function(){\n'use strict';\nvar _D=window._DATA;\n"
              + APP_CORE + APP_CHARTS + APP_AUTH + APP_STATE + APP_SETUP + APP_PLANNER + APP_HOUSEHOLD
              + APP_VIEWS1 + APP_VIEWS2 + APP_WIRE
              + "\nboot();\n})();\n")

    data_js = "window._DATA=" + json.dumps(public, separators=(",", ":")) + ";\n"

    html = (SHELL_HEAD + APP_CSS + SHELL_BODY
            + '<script>' + data_js + '</script>'
            + '<script>' + app_js + '</script>'
            + '</body></html>')
    return html, public, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit non-zero if index.html is stale")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    html, public, issues = render_html()
    out = os.path.join(ROOT, "index.html")

    if args.check:
        current = ""
        if os.path.exists(out):
            # newline="" so a CRLF copy does not silently compare equal to the
            # LF one we write. The check should notice that.
            with open(out, encoding="utf-8", newline="") as fh:
                current = fh.read()
        if issues:
            print("VALIDATION ISSUES: %d" % len(issues))
            for i in issues:
                print("  -", i)
        stale = []
        if current != html:
            stale.append("index.html")
        if stale:
            print("STALE: %s" % ", ".join(stale))
            print("Run: python3 src/build.py")
            return 1
        if not args.quiet:
            print("up to date | %d recipes | %d ingredients"
                  % (len(public["recipes"]), len(public["ing"])))
        return 1 if issues else 0

    # Windows would otherwise turn every newline into CRLF. The build has to be
    # byte-identical on every platform or --check means nothing.
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    if not args.quiet:
        print("index.html  %.0f KB" % (len(html) / 1024.0))
        print("recipes %d | ingredients %d | exercises %d | sessions %d"
              % (len(public["recipes"]), len(public["ing"]),
                 len(public["exercises"]), len(public["sessions"])))
        print(dict(Counter(r["cat"] for r in public["recipes"])))
        if issues:
            print("VALIDATION ISSUES: %d" % len(issues))
            for i in issues:
                print("  -", i)
        else:
            print("no validation issues")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
