# -*- coding: utf-8 -*-
"""Regenerates assets/data.js from the Python sources.

    python3 src/build_data.py            rebuild and write
    python3 src/build_data.py --check    rebuild in memory, fail if the repo is stale

Everything the app knows about food and training comes from here: the recipes in
recipes_1..6, the nutrition table in ingredients.py, the shelf prices in prices.py,
the aisle map in ingredient_list.py, and the four JSON files next to this script.

Nothing is typed by hand into assets/data.js. Macros are computed from gram weights,
costs from the price table, tags from the macros. The script also stamps a content
hash into index.html and sw.js so a deploy never serves a half-updated cache.
"""
import argparse
import hashlib
import json
import os
import re
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

RECIPES = RECIPES_1 + RECIPES_2 + RECIPES_3 + RECIPES_4 + RECIPES_5 + RECIPES_6

NUTS = ["kcal", "p", "c", "f", "fib", "leu", "ca", "fe", "mg", "k", "zn", "na",
        "b12", "vitd", "ala", "epadha"]

# Daily values used to decide whether a recipe counts as rich in a micronutrient.
DV = {"ca": 1300, "fe": 18, "mg": 420, "k": 4700, "zn": 11, "b12": 2.4, "vitd": 20}
MICRO_NAME = {"ca": "CALCIUM", "fe": "IRON", "mg": "MAGNESIUM",
              "k": "POTASSIUM", "zn": "ZINC"}


# ---------------------------------------------------------------- computation

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


# ---------------------------------------------------------------- assembly

def load_json(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def build_blob():
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

    exercises = load_json("exercises.json")
    sessions = load_json("sessions.json")
    for s in sessions:
        for x in s["ex"]:
            pass  # sessions carry their own copy of name/sets/reps, nothing to resolve

    blob = {
        "recipes": recipes,
        "ing": ings,
        "aisles": [[a, k] for a, k in AISLES],
        "exercises": exercises,
        "sessions": sessions,
        "costs": load_json("costs.json"),
        "jobs": load_json("jobs.json"),
    }
    return blob, issues


BANNER = "/* Generated by src/build_data.py. Edit the Python, not this file. */\n"


def render(blob):
    return BANNER + "window._DATA=" + json.dumps(blob, separators=(",", ":")) + ";\n"


def version_of(data_js):
    """Content hash over everything the browser caches."""
    h = hashlib.sha1()
    h.update(data_js.encode("utf-8"))
    for rel in ("assets/core.js", "assets/ui.js", "assets/views.js",
                "assets/app.js", "assets/app.css"):
        with open(os.path.join(ROOT, rel), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


def stamp(path, version):
    """Rewrite the ?v= / cache-name markers in a file. Returns True if it changed."""
    full = os.path.join(ROOT, path)
    with open(full, encoding="utf-8") as fh:
        before = fh.read()
    after = re.sub(r"(\?v=)[0-9a-f]{6,12}", r"\g<1>" + version, before)
    after = re.sub(r"(handbook-)[0-9a-f]{6,12}(')", r"\g<1>" + version + r"\g<2>", after)
    if after != before:
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(after)
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit non-zero if the checked-in files are stale")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    blob, issues = build_blob()
    data_js = render(blob)
    version = version_of(data_js)

    data_path = os.path.join(ROOT, "assets", "data.js")
    current = ""
    if os.path.exists(data_path):
        with open(data_path, encoding="utf-8") as fh:
            current = fh.read()

    if args.check:
        stale = []
        if current != data_js:
            stale.append("assets/data.js")
        for path in ("index.html", "sw.js"):
            with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
                text = fh.read()
            if version not in text:
                stale.append(path + " (cache version)")
        if issues:
            print("VALIDATION ISSUES: %d" % len(issues))
            for i in issues:
                print("  -", i)
        if stale:
            print("STALE: %s" % ", ".join(stale))
            print("Run: python3 src/build_data.py")
            return 1
        if not args.quiet:
            print("up to date | %d recipes | %d ingredients | version %s"
                  % (len(blob["recipes"]), len(blob["ing"]), version))
        return 1 if issues else 0

    with open(data_path, "w", encoding="utf-8") as fh:
        fh.write(data_js)
    stamp("index.html", version)
    stamp("sw.js", version)

    if not args.quiet:
        print("assets/data.js  %.0f KB" % (len(data_js) / 1024.0))
        print("recipes %d | ingredients %d | exercises %d | sessions %d"
              % (len(blob["recipes"]), len(blob["ing"]),
                 len(blob["exercises"]), len(blob["sessions"])))
        print(dict(Counter(r["cat"] for r in blob["recipes"])))
        print("cache version %s" % version)
        if issues:
            print("VALIDATION ISSUES: %d" % len(issues))
            for i in issues:
                print("  -", i)
        else:
            print("no validation issues")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
