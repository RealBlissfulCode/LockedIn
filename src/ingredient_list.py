# -*- coding: utf-8 -*-
"""Master ingredient list generator.

Reads every recipe, works out which ingredients are actually used, how often, and in what
typical quantity, then emits:
  - an HTML section for the handbook (grouped by supermarket aisle)
  - ingredient_list.csv
  - an extra sheet in the workbook

Nothing here is typed by hand. Usage counts and gram totals come from the recipes themselves.
"""
import csv, html
from collections import defaultdict

# Aisle assignment. Every ingredient key must land in exactly one aisle.
AISLES = [
 ("Dairy and eggs", ["greek_yogurt_nonfat","greek_yogurt_2","greek_yogurt_whole","skyr",
   "cottage_cheese_2","cottage_cheese_4","milk_skim","milk_2","milk_whole","kefir_plain",
   "egg_whole","egg_white","cheddar","mozzarella_ps","parmesan","feta","ricotta_ps","butter",
   "sour_cream","cream_cheese_whipped","whipped_cream","string_cheese_light"]),
 ("Protein powders and shelf protein", ["whey_isolate","whey_concentrate","casein_powder",
   "plant_protein","soy_protein_isolate","pb_powder"]),
 ("Soy, legumes and beans", ["tofu_firm","tofu_extrafirm","tofu_silken","tempeh","edamame_shelled",
   "soy_milk_unsw","lentils","black_beans","chickpeas","kidney_beans","pinto_beans",
   "refried_beans_ff","peas_frozen","hummus","impossible_patty","bean_sprouts"]),
 ("Grains, starch and GF baking", ["oats_gf_dry","gf_oat_flour","rice_white_cooked",
   "rice_brown_cooked","quinoa_cooked","gf_pasta_dry","chickpea_pasta_dry","lentil_pasta_dry",
   "mung_bean_pasta_dry","gf_lasagna_noodle_dry","gf_ravioli_cheese","rice_noodles_dry",
   "corn_tortilla","gf_bread","gf_wrap","gf_english_muffin","rice_cake","cornmeal_polenta",
   "tapioca_pearls_dry","baking_powder","cornstarch","popcorn_popped","gf_sandwich_cookie",
   "sf_pudding_mix","gf_burger_bun","gf_breadcrumbs"]),
 ("Produce", ["banana","blueberries","strawberries","raspberries","apple","orange","pineapple",
   "dates_medjool","spinach","kale","broccoli_cooked","bell_pepper","onion","tomato",
   "cherry_tomatoes","cucumber","romaine","zucchini","mushrooms","carrot","cauliflower_rice",
   "potato","sweet_potato","avocado","garlic","lemon_juice","green_onion","coleslaw_mix",
   "sweet_corn"]),
 ("Frozen", ["mixed_berries_frozen","mango_frozen","hash_brown_patty","frozen_fries","vanilla_ice_cream"]),
 ("Nuts, seeds and oils", ["peanut_butter","almond_butter","almonds","walnuts","cashews",
   "pumpkin_seeds","sunflower_seeds","chia","flax_ground","hemp_hearts","tahini","olive_oil",
   "coconut_oil","almond_milk_unsw","peanuts_roasted"]),
 ("Pantry, sauces and condiments", ["marinara","salsa","salsa_verde","soy_sauce_gf","sriracha",
   "cholula","buffalo_sauce","curry_paste","ketchup","mustard_yellow","mayo","honey","maple_syrup",
   "sugar","brown_sugar","sugar_free_syrup","cocoa_powder","dark_chocolate_70","choc_chips_mini",
   "nutritional_yeast","vanilla_extract","cinnamon","spice_generic","salt","matcha","cold_brew",
   "black_tea_brewed","raisins","coconut_milk_light","coconut_milk_full","acv","applesauce_unsw",
   "artichoke_hearts","green_chilies","greek_dressing_lite","roasted_red_pepper","pickled_jalapeno",
   "pumpkin_puree","shrimp_NOT"]),
 ("Optional: clean meat and fish (M section only)", ["chicken_breast","chicken_thigh",
   "turkey_breast","ground_turkey_93","salmon","canned_salmon","canned_tuna","sardines","cod","tilapia"]),
]

# Ingredients where a gluten-free certified version must be bought specifically.
GF_CRITICAL = {
 "oats_gf_dry":"Oats are cross-contaminated during harvest and milling. Certified GF only.",
 "gf_oat_flour":"Same as rolled oats. Certified GF only.",
 "soy_sauce_gf":"Standard soy sauce is a wheat product. Buy tamari labelled gluten-free.",
 "whey_isolate":"Many powders are produced in shared facilities. Look for certified GF on the tub.",
 "whey_concentrate":"Same as isolate. Check the certification.",
 "casein_powder":"Same. Check the certification.",
 "plant_protein":"Often contains barley grass or is blended in shared facilities. Check.",
 "gf_pasta_dry":"Corn and rice pasta. Read the box, some blends contain wheat starch.",
 "gf_bread":"Must be a dedicated GF loaf. Keep a separate toaster or use toaster bags.",
 "gf_wrap":"Dedicated GF only.",
 "gf_english_muffin":"Dedicated GF only. Standard English muffins are wheat.",
 "gf_lasagna_noodle_dry":"Dedicated GF only.",
 "gf_ravioli_cheese":"Dedicated GF only. Check the filling too.",
 "gf_sandwich_cookie":"Glutino, Goodie Girl or K-Toos. Oreos are wheat.",
 "corn_tortilla":"Should be 100% corn. Some brands blend in wheat flour, so read the bag.",
 "buffalo_sauce":"Most are GF but some use wheat-derived thickeners. Read the label.",
 "curry_paste":"Many Thai pastes contain wheat or shrimp paste. Read the jar.",
 "marinara":"Usually GF but check for wheat-based thickeners in cheaper brands.",
 "sf_pudding_mix":"Usually GF, but some instant mixes use wheat starch. Read the box.",
 "impossible_patty":"Gluten-free by formulation. Impossible sausage and chicken products vary, so check each.",
 "popcorn_popped":"Plain kernels are GF. Flavoured microwave bags sometimes are not.",
 "hash_brown_patty":"Some frozen potato products use wheat flour as an anti-stick coating. Read the bag.",
 "refried_beans_ff":"Check for lard as well as gluten. Buy the vegetarian version.",
}

COSTTIER = {1:"Low",2:"Moderate",3:"Higher"}


def build(ING, DATA, OUT):
    use = defaultdict(lambda: {"n":0,"g":0.0,"ids":[]})
    for d in DATA:
        r = d["r"]
        for k,g,_m in r["ing"]:
            u = use[k]; u["n"] += 1; u["g"] += g/max(r["servings"],1); u["ids"].append(r["id"])

    placed = {k for _t,keys in AISLES for k in keys}
    unplaced = sorted(set(use) - placed)

    # ---------- CSV ----------
    rows = []
    for aisle, keys in AISLES:
        for k in keys:
            if k not in use: continue
            u = use[k]; ig = ING[k]
            rows.append([aisle, ig["name"], k, u["n"], round(u["g"]),
                         round(u["g"]/u["n"]), ig["kcal"], ig["p"], ig["c"], ig["f"], ig["fib"],
                         round(ig["leu"],2),
                         round(ig["p"]*4/ig["kcal"]*100) if ig["kcal"] else 0,
                         "YES" if k in GF_CRITICAL else "",
                         GF_CRITICAL.get(k,""), ", ".join(u["ids"][:12])])
    for k in unplaced:
        u = use[k]; ig = ING[k]
        rows.append(["Unsorted", ig["name"], k, u["n"], round(u["g"]), round(u["g"]/u["n"]),
                     ig["kcal"], ig["p"], ig["c"], ig["f"], ig["fib"], round(ig["leu"],2),
                     round(ig["p"]*4/ig["kcal"]*100) if ig["kcal"] else 0, "", "",
                     ", ".join(u["ids"][:12])])

    head = ["Aisle","Ingredient","Key","RecipesUsingIt","TotalGramsPerServingAcrossRecipes",
            "TypicalGramsPerServing","kcal_per100g","Protein_per100g","Carbs_per100g","Fat_per100g",
            "Fiber_per100g","Leucine_per100g","ProteinDensity_pct","GF_CHECK_REQUIRED",
            "GF_Note","ExampleRecipeIDs"]
    with open(f"{OUT}/ingredient_list.csv","w",newline="") as fh:
        w = csv.writer(fh); w.writerow(head); w.writerows(rows)

    # ---------- HTML ----------
    top = sorted(use.items(), key=lambda kv:-kv[1]["n"])[:20]
    h = ['<h2 id="ingredients">Master ingredient list</h2>',
     '<p>Everything the catalog actually draws on, grouped by where I find it in the '
     'store. The "used in" column counts how many recipes call for it, so the items at '
     'the top of each group are the ones worth always having. Protein density is protein calories '
     'as a share of total calories, which is the number that tells me whether something is a '
     'protein source or a carb or fat source wearing a protein label.</p>']

    h.append('<div class="callout warn"><h4>The gluten-free checklist</h4><p>These are the '
     'ingredients where the specific product matters, not just the food. Everything else on this '
     'list is gluten-free by nature.</p><table><tr><th>Ingredient</th><th>What to check</th></tr>')
    for k,note in sorted(GF_CRITICAL.items(), key=lambda kv: ING[kv[0]]["name"] if kv[0] in ING else kv[0]):
        if k in use:
            h.append(f'<tr><td>{html.escape(ING[k]["name"])}</td><td>{html.escape(note)}</td></tr>')
    h.append('</table></div>')

    h.append('<h3>The twenty ingredients that carry the whole catalog</h3>')
    h.append('<p class="small">Ranked by how many recipes use them. With these in the house me '
             'can cook most of what follows without another trip.</p><table><tr><th>#</th>'
             '<th>Ingredient</th><th>Recipes</th><th>Typical serving</th><th>Protein density</th></tr>')
    for i,(k,u) in enumerate(top,1):
        ig = ING[k]; pd_ = round(ig["p"]*4/ig["kcal"]*100) if ig["kcal"] else 0
        h.append(f'<tr><td>{i}</td><td>{html.escape(ig["name"])}</td><td>{u["n"]}</td>'
                 f'<td>{round(u["g"]/u["n"])} g</td><td>{pd_}%</td></tr>')
    h.append('</table>')

    for aisle, keys in AISLES:
        present = [k for k in keys if k in use]
        if not present: continue
        present.sort(key=lambda k:-use[k]["n"])
        h.append(f'<h3>{html.escape(aisle)}</h3>')
        h.append('<table><tr><th>Ingredient</th><th>Used in</th><th>Typical per serving</th>'
                 '<th>kcal /100g</th><th>P</th><th>C</th><th>F</th><th>Fib</th>'
                 '<th>Protein density</th><th>Cost</th><th>GF check</th></tr>')
        for k in present:
            ig = ING[k]; u = use[k]
            pd_ = round(ig["p"]*4/ig["kcal"]*100) if ig["kcal"] else 0
            flag = '<b style="color:#B4442A">CHECK</b>' if k in GF_CRITICAL else ''
            cost = COSTTIER.get(ig.get("cost",2),"")
            h.append(f'<tr><td>{html.escape(ig["name"])}</td><td>{u["n"]}</td>'
                     f'<td>{round(u["g"]/u["n"])} g</td><td>{ig["kcal"]}</td><td>{ig["p"]}</td>'
                     f'<td>{ig["c"]}</td><td>{ig["f"]}</td><td>{ig["fib"]}</td>'
                     f'<td>{pd_}%</td><td>{cost}</td><td>{flag}</td></tr>')
        h.append('</table>')

    if unplaced:
        h.append('<h3>Unsorted</h3><p class="small">' +
                 html.escape(", ".join(ING[k]["name"] for k in unplaced)) + '</p>')

    h.append('<p class="back"><a href="#top">Top</a></p>')
    return "\n".join(h), rows, head
