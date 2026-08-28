# -*- coding: utf-8 -*-
"""Price table. USD per 100 g of the ingredient as used.

Walmart = Great Value / store brand, Fort Collins supercenter shelf pricing, Aug 2026.
Costco  = Kirkland or bulk equivalent, Timnath warehouse. None means not worth buying there
          in a size two people will get through.

Anchors used: eggs 18ct $2.47, cottage cheese 48oz $5.46, butter 16oz $3.44, shredded
cheddar 32oz $6.92, whole milk gal $3.28, chicken breast $3.79/lb, jasmine rice 5lb $6.22,
tuna 5oz $0.96. Cooked-weight items are converted from raw at typical yield, so cooked rice
is a third the price per 100 g of dry rice, and cooked chicken is 1.4x raw.

Edit these in the app if a price moves. Every recipe cost recalculates from here.
"""

# key: (walmart_per_100g, costco_per_100g or None)
PRICE = {
# ---------- dairy and egg ----------
"greek_yogurt_nonfat":(0.49,0.42), "greek_yogurt_2":(0.52,0.45), "greek_yogurt_whole":(0.55,0.47),
"skyr":(0.79,None), "cottage_cheese_2":(0.40,0.34), "cottage_cheese_4":(0.40,0.34),
"milk_skim":(0.08,0.07), "milk_2":(0.084,0.072), "milk_whole":(0.086,0.074),
"kefir_plain":(0.62,None), "egg_whole":(0.28,0.22), "egg_white":(0.49,0.41),
"cheddar":(0.76,0.62), "mozzarella_ps":(0.72,0.58), "parmesan":(1.85,1.32),
"feta":(1.28,0.95), "ricotta_ps":(0.68,None), "butter":(0.76,0.62),
"sour_cream":(0.42,0.33), "cream_cheese_whipped":(0.95,0.72), "whipped_cream":(0.88,None),
"string_cheese_light":(1.35,0.98),
# ---------- powders ----------
"whey_isolate":(2.42,2.17), "whey_concentrate":(1.95,1.72), "casein_powder":(2.85,None),
"plant_protein":(2.75,2.30), "soy_protein_isolate":(2.10,None), "pb_powder":(1.30,0.98),
"cocoa_powder":(1.05,0.72), "nutritional_yeast":(2.20,1.55), "matcha":(9.50,6.80),
"sf_pudding_mix":(1.75,None),
# ---------- soy, legume, plant protein ----------
"tofu_firm":(0.57,0.42), "tofu_extrafirm":(0.60,0.44), "tofu_silken":(0.62,None),
"tempeh":(1.15,None), "edamame_shelled":(0.55,0.38), "soy_milk_unsw":(0.16,0.13),
"lentils":(0.18,0.13), "black_beans":(0.39,0.28), "chickpeas":(0.41,0.30),
"kidney_beans":(0.39,0.28), "pinto_beans":(0.22,0.16), "refried_beans_ff":(0.35,0.27),
"peas_frozen":(0.31,0.22), "hummus":(0.88,0.62), "impossible_patty":(1.55,1.24),
"bean_sprouts":(0.42,None),
# ---------- grains and starch ----------
"oats_gf_dry":(0.60,0.44), "gf_oat_flour":(0.85,None),
"rice_white_cooked":(0.091,0.068), "rice_brown_cooked":(0.11,0.082),
"quinoa_cooked":(0.24,0.17), "gf_pasta_dry":(0.62,0.48), "chickpea_pasta_dry":(1.05,0.78),
"lentil_pasta_dry":(1.00,0.75), "mung_bean_pasta_dry":(1.95,None),
"gf_lasagna_noodle_dry":(0.88,None), "gf_ravioli_cheese":(1.60,None),
"rice_noodles_dry":(0.55,None), "corn_tortilla":(0.28,0.19), "gf_bread":(1.05,0.82),
"gf_wrap":(1.25,None), "gf_english_muffin":(1.30,None), "gf_burger_bun":(1.35,None),
"rice_cake":(0.85,0.60), "cornmeal_polenta":(0.28,None), "tapioca_pearls_dry":(0.95,None),
"baking_powder":(0.45,None), "cornstarch":(0.28,None), "popcorn_popped":(0.42,0.26),
"gf_sandwich_cookie":(1.75,None), "gf_breadcrumbs":(1.10,None), "frozen_fries":(0.30,0.21),
"hash_brown_patty":(0.38,0.27),
# ---------- produce ----------
"banana":(0.14,0.11), "blueberries":(0.88,0.52), "strawberries":(0.62,0.40),
"raspberries":(1.25,0.78), "apple":(0.36,0.26), "orange":(0.33,0.24),
"pineapple":(0.31,0.22), "mango_frozen":(0.44,0.30), "mixed_berries_frozen":(0.52,0.35),
"dates_medjool":(1.15,0.78), "raisins":(0.55,0.36),
"spinach":(0.72,0.48), "kale":(0.55,0.38), "broccoli_cooked":(0.42,0.30),
"bell_pepper":(0.48,0.33), "onion":(0.20,0.14), "tomato":(0.42,0.30),
"cherry_tomatoes":(0.68,0.46), "cucumber":(0.28,0.20), "romaine":(0.35,0.24),
"zucchini":(0.35,0.25), "mushrooms":(0.62,0.42), "carrot":(0.17,0.12),
"cauliflower_rice":(0.55,0.38), "potato":(0.16,0.11), "sweet_potato":(0.22,0.16),
"avocado":(0.72,0.48), "garlic":(0.85,0.55), "lemon_juice":(0.42,0.30),
"green_onion":(0.75,None), "coleslaw_mix":(0.30,0.21), "sweet_corn":(0.33,0.23),
"pumpkin_puree":(0.30,0.22), "artichoke_hearts":(0.72,0.52), "green_chilies":(0.62,None),
# ---------- nuts, seeds, fats ----------
"peanut_butter":(0.52,0.36), "almond_butter":(1.45,1.02), "almonds":(1.05,0.72),
"walnuts":(1.35,0.92), "cashews":(1.30,0.88), "pumpkin_seeds":(1.20,0.82),
"sunflower_seeds":(0.62,0.42), "chia":(1.05,0.68), "flax_ground":(0.62,0.42),
"hemp_hearts":(2.10,1.42), "tahini":(1.35,0.95), "olive_oil":(0.85,0.55),
"coconut_oil":(0.68,0.46), "almond_milk_unsw":(0.15,0.11), "peanuts_roasted":(0.62,0.40),
"dark_chocolate_70":(1.55,1.05), "choc_chips_mini":(0.95,0.68),
"vanilla_ice_cream":(0.52,0.36),
# ---------- pantry, sauces, condiments ----------
"marinara":(0.32,0.22), "salsa":(0.38,0.26), "salsa_verde":(0.42,None),
"soy_sauce_gf":(0.95,0.68), "sriracha":(0.62,0.42), "cholula":(0.85,None),
"buffalo_sauce":(0.58,0.40), "curry_paste":(2.10,None), "ketchup":(0.30,0.20),
"mustard_yellow":(0.32,0.22), "mayo":(0.45,0.32), "honey":(0.95,0.62),
"maple_syrup":(1.55,0.98), "sugar":(0.16,0.11), "brown_sugar":(0.22,0.15),
"sugar_free_syrup":(0.62,None), "vanilla_extract":(4.50,2.80), "cinnamon":(1.85,0.95),
"spice_generic":(2.50,1.40), "salt":(0.12,0.08), "cold_brew":(0.32,0.22),
"black_tea_brewed":(0.04,0.03), "coconut_milk_light":(0.32,0.24),
"coconut_milk_full":(0.38,0.28), "acv":(0.22,0.15), "applesauce_unsw":(0.32,0.22),
"greek_dressing_lite":(0.62,None), "roasted_red_pepper":(0.75,0.52),
"pickled_jalapeno":(0.48,0.32),
# ---------- clean meat and fish ----------
"chicken_breast":(1.19,0.92), "chicken_thigh":(0.85,0.65), "turkey_breast":(1.45,1.10),
"ground_turkey_93":(1.05,0.82), "salmon":(2.85,2.10), "canned_salmon":(1.55,1.15),
"canned_tuna":(0.68,0.48), "sardines":(1.35,0.95), "cod":(1.95,1.45), "tilapia":(1.25,0.92),
}

# Ingredients used in trace amounts where the per-100g price is misleading.
TRACE = {"spice_generic","salt","cinnamon","vanilla_extract","baking_powder","garlic"}

STORE_NOTE = ("Walmart column is Great Value or store brand at the Fort Collins supercenter. "
              "Costco column is Kirkland or the bulk equivalent at Timnath, and is blank where "
              "the pack size is more than two people will get through before it turns. Prices "
              "are Aug 2026 and move weekly, so treat them as a planning number rather than a "
              "receipt. Anything can be edited in the app and every recipe recosts instantly.")


def cost_of(recipe, servings, store="walmart"):
    """Returns (total_cost, cost_per_serving, missing_keys)."""
    idx = 0 if store == "walmart" else 1
    total = 0.0; missing = []
    for k, g, _m in recipe["ing"]:
        p = PRICE.get(k)
        if not p:
            missing.append(k); continue
        v = p[idx]
        if v is None: v = p[0]          # fall back to Walmart if no Costco size
        total += (g / 100.0) * v
    return total, total / max(servings, 1), missing
