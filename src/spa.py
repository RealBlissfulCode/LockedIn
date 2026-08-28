# -*- coding: utf-8 -*-
"""Builds the app HTML. Run after build.py has computed DATA."""
import json, os

from spa_css import APP_CSS
from spa_js import APP_JS
from ingredient_list import AISLES
import prices as PR

OUT = "/mnt/user-data/outputs"

DIFF_ORDER = {"EASY": "EASY", "MODERATE": "MODERATE", "ADVANCED": "ADVANCED"}


def aisle_of(key):
    for name, keys in AISLES:
        if key in keys:
            return name
    return "Other"


def build_recipes(DATA, ING):
    out = []
    for d in DATA:
        r = d["r"]; p = d["per"]
        w, ws, _ = PR.cost_of(r, r["servings"], "walmart")
        c, cs, _ = PR.cost_of(r, r["servings"], "costco")
        out.append({
            "id": r["id"], "n": r["name"], "cat": r["cat"], "sv": r["servings"],
            "t": d["time"], "diff": d["diff"],
            "k": round(p["kcal"]), "p": round(p["p"], 1), "c": round(p["c"], 1),
            "f": round(p["f"], 1), "fib": round(p["fib"], 1), "leu": round(p["leu"], 2),
            "tg": d["tags"],
            "cw": round(w, 2), "cws": round(ws, 2), "cc": round(c, 2), "ccs": round(cs, 2),
            "ing": [[i[2], i[0], i[1]] for i in r["ing"]],
            "st": r["steps"],
            "storage": r.get("storage", ""), "prep": r.get("prep_notes", ""),
            "subs": r.get("subs", []), "vars": r.get("variations", []),
        })
    return out


def build_ing(ING):
    out = {}
    for k, v in ING.items():
        pr = PR.PRICE.get(k)
        if not pr:
            continue
        out[k] = {"n": v["name"], "aisle": aisle_of(k), "w": pr[0],
                  "c": pr[1] if pr[1] else 0, "kcal": v["kcal"], "p": v["p"]}
    return out


LEARN = [
 ["The macros", [
  ["Protein, and why mine is set higher than most calculators say",
   "<p>Protein is a delivery vehicle for amino acids, nine of which the body cannot make. Muscle protein "
   "synthesis is limited by whichever essential amino acid is shortest, so total grams is a crude measure.</p>"
   "<p>My target is 1.1 g per lb of bodyweight rather than the 0.8 most calculators land on. Two reasons. "
   "Dairy and plant proteins have lower digestibility than meat, so a day reading 160 g on paper is "
   "realistically 135 to 145 g usable. And protein requirement rises in a deficit or during hard training. "
   "The correction is real, not padding.</p>"
   "<p>Above about 1.5 g/lb the extra is oxidised. Past that point, calories are better spent on carbs.</p>"],
  ["Leucine, the part everyone oversimplifies",
   "<p>Leucine is the amino acid that acts as a signal rather than just a building block. It flips on mTORC1, "
   "which starts muscle protein synthesis. The response saturates around 2.5 to 3 g per feeding.</p>"
   "<p>What matters: hitting that threshold does not build muscle, it starts a signal. Whether the signal "
   "becomes tissue depends on the other amino acids being present, on energy balance, and on having trained. "
   "Leucine is the ignition, not the fuel and not the engine. This is exactly why isolated BCAA supplements "
   "do nothing once total protein is controlled for.</p>"
   "<p>Order of importance: total daily protein, then progressive training, then adequate calories, then "
   "distribution across three to five feedings, and only then leucine per feeding.</p>"],
  ["Carbs, and why cutting them makes me look smaller",
   "<p>Carbs fuel training and refill muscle glycogen. Muscle glycogen capacity is roughly 15 g per kg of "
   "bodyweight, so around 1,000 g stored, and each gram pulls roughly 3 g of water into the muscle with it.</p>"
   "<p>That is why chronic low carbs makes a physique read flat. Full glycogen is the difference between "
   "looking like the muscle mass I have and looking smaller than it. It is also the fastest visible change "
   "from eating properly, showing up inside two weeks before any real tissue is built.</p>"
   "<p>Target is 2.5 to 3 g per lb on a gaining phase. Carbs take whatever calories are left after protein "
   "and fat are set.</p>"],
  ["Fat, and the floor I should not go under",
   "<p>Fat runs hormone production, builds cell membranes, and carries vitamins A, D, E and K. The floor is "
   "0.3 g per lb of bodyweight. Below that, testosterone and fat-soluble vitamin absorption both suffer.</p>"
   "<p>Practical setting is 25% of calories. It is also the easiest lever for adding calories without volume, "
   "at 9 kcal per gram against 4 for protein and carbs. A tablespoon of olive oil over a finished dish is "
   "120 calories that take no effort to eat.</p>"],
  ["Fiber, and why ramping it too fast is miserable",
   "<p>Target is 14 g per 1,000 calories, so around 39 g a day. Fiber does digestion, satiety, blood glucose "
   "control and feeds gut bacteria.</p>"
   "<p>The catch: going from a low-food-volume diet to a much higher one raises fiber fast, and a sudden jump "
   "causes real bloating and discomfort. Ramp it over a few weeks alongside the calories, and drink more "
   "water as it climbs.</p>"],
 ]],
 ["How the numbers are worked out", [
  ["RMR, the starting point",
   "<p>Mifflin-St Jeor is the default: (10 x kg) + (6.25 x cm) - (5 x age), then +5 for men or -161 for women. "
   "That last term is most of the 660-calorie gap between my target and Aaliyah's.</p>"
   "<p>Katch-McArdle, 370 + (21.6 x lean kg), is more accurate but only if the body fat number is real. "
   "From a BIA scale it is not, so Mifflin stays the default until a DEXA says otherwise. The calculator "
   "shows both so the spread is visible.</p>"],
  ["Activity factor, where most of the error lives",
   "<p>The honest test is not how hard the session felt, it is how many hours a day I am on my feet. "
   "Engraving work is 1.55. Electrical was 1.75, and that difference alone is about 330 calories a day.</p>"
   "<p>Most people overestimate by one full step. It is also not one number all year: a week of overtime "
   "pushes it up, a flare week pushes it down.</p>"],
  ["Goal multiplier",
   "<p>Maintenance is RMR x activity. Then: cut is 0.78x, maintain 1.0x, recomp 1.03x, lean gain 1.09x, "
   "bulk 1.15x. Lean gain targets 0.3 to 0.5 lb a week, which at my training age gives the best "
   "muscle-to-fat ratio.</p>"
   "<p>Coming off a long stretch of underfeeding, recomp is the unusual case worth knowing about: muscle "
   "gain and fat loss at the same time, which normally only happens to beginners. It lasts three to four "
   "months and then the window closes.</p>"],
  ["Why the scale is not the judge",
   "<p>The calculator produces a starting guess. The weight trend produces the truth. Weigh every morning "
   "after the bathroom, average the seven days, and compare this week's average to the one from three weeks "
   "ago. Never compare single days.</p>"
   "<p>Daily swings of 2 to 4 lb come from sodium, glycogen, training inflammation, gut contents and sleep. "
   "With celiac there is one more: an accidental gluten exposure causes days of inflammatory water retention "
   "that looks exactly like fat gain.</p>"],
 ]],
 ["Training and food", [
  ["Why the day's target changes with the session",
   "<p>Legs empty far more glycogen than arms do, so leg day carries the highest carb and calorie target of "
   "the week. Pull day weights protein, leucine and iron-rich options, because pulling volume on a "
   "plant-heavy diet is where iron runs thin. Rest days hold protein steady and ease carbs back, because "
   "repair happens on rest days.</p>"
   "<p>The adjustments are deliberately modest, between 3 and 30 percent depending on the macro. Anything "
   "larger is guesswork dressed up as precision.</p>"],
  ["Nutrient timing, honestly",
   "<p>The anabolic window is not thirty minutes. Elevated sensitivity to protein lasts something like "
   "24 hours after training, biggest in the first few hours. If I ate within a couple of hours beforehand, "
   "there is no urgency at all.</p>"
   "<p>Where timing earns its keep: training fasted, training twice in a day, or a work shift straight after "
   "training. Then 40 g protein and 60 to 80 g carbs within an hour or two is worth doing.</p>"
   "<p>Pre-sleep protein has better evidence than most timing claims. 40 g of casein or cottage cheese "
   "before bed measurably raises overnight synthesis.</p>"],
  ["Meal distribution",
   "<p>Total daily protein is roughly 80% of the result. Distribution is worth maybe 5 to 10% more in "
   "controlled studies, which is small but free.</p>"
   "<p>Per feeding target is 40 to 55 g with at least 2.5 g leucine. Two meals works and is not a disaster, "
   "it is just slightly less efficient. Two meals plus a shake is the pattern that actually fits my week.</p>"],
 ]],
 ["Celiac, and what actually goes wrong", [
  ["Where the real risk is",
   "<p>The food itself is the easy part. Every recipe here is built from ingredients that are gluten-free by "
   "nature. What catches people is the brand: uncertified oats, soy sauce instead of tamari, frozen fries "
   "with a flour anti-stick coating, cajun seasoning with wheat as an anti-caking agent, Thai curry paste.</p>"
   "<p>Cross-contamination at home matters too. Shared toasters, shared colanders, butter and condiment jars "
   "with crumbs in them, wooden boards, flour dust in the air. Squeeze bottles over jars, and a separate "
   "toaster or toaster bags.</p>"],
  ["The nutrients that run short",
   "<p>Celiac damages the duodenum, which is exactly where iron is absorbed. Add a plant-heavy diet, where "
   "non-heme iron absorbs at 2 to 10% versus 15 to 35% for heme, and iron is the top risk. Pair iron foods "
   "with vitamin C, and keep tea and coffee away from those meals.</p>"
   "<p>Then B12 (animal foods and fortified products only), vitamin D (fat-soluble, malabsorbed, and Colorado "
   "gives almost nothing usable October through March), calcium (matters more with CRMO), and zinc "
   "(phytates in legumes bind it).</p>"
   "<p>Worth testing annually: ferritin, CBC, B12, 25-OH vitamin D, and tTG-IgA to confirm the diet is "
   "actually controlling the disease.</p>"],
  ["Why gluten-free eating gets more expensive, and how to dodge it",
   "<p>GF bread, wraps, pasta and snacks run two to four times their wheat equivalents. The way around it is "
   "to build meals on food that is naturally gluten-free rather than on replacement products: rice, potatoes, "
   "corn tortillas, beans, certified GF oats, dairy, eggs.</p>"
   "<p>Corn tortillas in particular are cheap, naturally safe, and higher in leucine than most grains. Mexican "
   "food is one of the few cuisines where celiac barely restricts anything.</p>"],
 ]],
 ["Money and food", [
  ["What a serving means here",
   "<p>One serving is one plated portion for one person. A recipe that makes 4 makes four meals, not four "
   "spoonfuls. Median main is 675 kcal and 45 g protein at about $2.59.</p>"
   "<p>This is a different unit from the MyPlate style 'eat 15 to 22 servings a day', where a serving is one "
   "slice of bread or half a cup of rice. A single plate of dal is five of those on its own.</p>"
   "<p>A normal day is four to six servings: breakfast, lunch, dinner, a shake, a snack or two.</p>"],
  ["The real cost, worked from cost per calorie",
   "<p>Median across the catalog is $3.92 per 1,000 kcal at Walmart. From that: me at 2,800 kcal is $11 a "
   "day, Aaliyah at 1,900 is $7.45, so about $18.44 a day or $553 a month for both of us. Costco pulls it to "
   "roughly $417, and leaning on the cheap list gets under $300.</p>"
   "<p>Average US household of two spends $800 to $900 a month including eating out, so cooking from here "
   "lands well under that before any budgeting.</p>"
   "<p>That $285 to $553 spread is the lever, and it is not about eating less. It is which recipes get used "
   "in a given week.</p>"],
  ["Protein per dollar",
   "<p>Cost per 25 g of protein is the only supermarket metric worth tracking. Cheapest first: dried lentils "
   "and beans, cottage cheese, milk, eggs, tofu, then Greek yogurt in large tubs, bulk whey, canned tuna, "
   "chicken.</p>"
   "<p>Protein bars are four to six times the cost per gram of any of those, with fewer calories, at exactly "
   "the point where calories are the thing in short supply. A jar of overnight oats plus a shaker of whey is "
   "about a dollar fifty and takes four minutes the night before.</p>"],
 ]],
 ["Supplements, sorted honestly", [
  ["Worth the money",
   "<p><b>Creatine monohydrate, 5 g daily.</b> The most evidence-backed legal ergogenic there is. It works by "
   "saturating muscle stores over three to four weeks, so consistency is the entire mechanism. Every day, "
   "including rest days. Anything labelled HCl or buffered is monohydrate with a markup.</p>"
   "<p><b>Whey or casein.</b> Food, not a supplement. Verify certified gluten-free.</p>"
   "<p><b>Vitamin D3, 2,000 to 4,000 IU with a fat meal.</b> Colorado winter plus celiac malabsorption plus "
   "CRMO. Test 25-OH-D and aim for 40 to 60 ng/mL.</p>"
   "<p><b>EPA and DHA, 1 to 2 g.</b> Algae oil keeps it vegetarian and works as well as fish oil. Directly "
   "relevant to CRMO inflammation.</p>"],
  ["Situational, overrated, and skip",
   "<p><b>Situational:</b> magnesium glycinate 200 to 400 mg if sleep or cramping is a problem. Caffeine at "
   "3 to 6 mg/kg, but starting low given a resting heart rate around 94. Iron only if ferritin is actually "
   "low, because excess iron is genuinely harmful.</p>"
   "<p><b>Overrated:</b> pre-workouts are caffeine plus filler at a large premium. Nitric oxide and pump "
   "products produce a cosmetic, transient effect.</p>"
   "<p><b>Skip:</b> turkesterone has essentially no human evidence and third-party testing repeatedly finds "
   "products containing little or none of the labelled compound. BCAAs are pointless once total protein is "
   "adequate. Glutamine does nothing in healthy people. Test boosters do not raise testosterone in men with "
   "normal levels. Mass gainers are sugar at four times the price of oats and milk.</p>"
   "<p>Supplements are a rounding error against the calorie gap. Eating 2,800 consistently would out-progress "
   "any stack money can buy.</p>"],
 ]],
]


def build(DATA, ING):
    recipes = build_recipes(DATA, ING)
    ings = build_ing(ING)
    js = (APP_JS
          .replace("__RECIPES__", json.dumps(recipes, separators=(",", ":")))
          .replace("__ING__", json.dumps(ings, separators=(",", ":")))
          .replace("__AISLES__", json.dumps([[a, k] for a, k in AISLES], separators=(",", ":")))
          .replace("__LEARN__", json.dumps(LEARN, separators=(",", ":"))))
    html = (
      '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<meta name="theme-color" content="#0A1A2F">'
      '<title>The Meal Handbook</title>' + APP_CSS + '</head><body>'
      '<header class="top"><div class="topin">'
      '<div class="brand">The Meal <em>Handbook</em></div>'
      '<div class="whoswitch" id="who"></div>'
      '<nav class="tabs" id="tabs"></nav></div></header>'
      '<main class="wrap" id="view"></main>'
      '<nav class="btmnav" id="btm"></nav>'
      + js + '</body></html>')
    with open(f"{OUT}/meal_app.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    return len(html), len(recipes), len(ings)
