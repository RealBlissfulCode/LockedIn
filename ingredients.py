# -*- coding: utf-8 -*-
"""
INGREDIENT NUTRIENT DATABASE
All values are per 100 g EDIBLE PORTION unless the key says otherwise.

Fields: kcal, p (protein g), c (carb g), f (fat g), fib (fiber g), leu (leucine g),
        ca (mg), fe (mg), mg (mg), k (mg), zn (mg), na (mg), b12 (mcg),
        vitd (mcg), ala (g omega-3 ALA), epadha (g EPA+DHA)

SOURCE METHOD:
 - Macronutrients, fiber and minerals are taken from USDA FoodData Central
   SR Legacy / Foundation Foods entries for the generic food named, rounded.
 - Leucine is taken from the USDA amino-acid profile where published; where it is
   not, it is estimated as protein x a food-group leucine fraction
   (whey 0.105, casein 0.093, dairy 0.096, egg 0.086, poultry/fish 0.077,
   soy 0.078, legume 0.072, oat/grain 0.074, nut/seed 0.067).
   Every leucine number in this handbook is therefore an ESTIMATE to +/- ~10%.
 - Branded items (protein powder, GF bread, GF tortillas, protein pasta) vary a lot
   between brands. Values used here are typical-label averages and are flagged
   as BRAND-DEPENDENT in the handbook. Check your own labels.
"""

F = ["kcal", "p", "c", "f", "fib", "leu", "ca", "fe", "mg", "k", "zn", "na", "b12", "vitd", "ala", "epadha"]


def _ing(name, *vals, **kw):
    d = dict(zip(F, list(vals) + [0] * (len(F) - len(vals))))
    d["name"] = name
    d.update(kw)
    return d


ING = {
    # ---------- DAIRY / EGGS ----------
    "greek_yogurt_nonfat": _ing("Nonfat plain Greek yogurt", 59, 10.3, 3.6, 0.4, 0, 0.99, 110, 0.07, 11, 141, 0.5, 36, 0.75, 0),
    "greek_yogurt_2": _ing("2% plain Greek yogurt", 73, 9.9, 3.9, 1.9, 0, 0.95, 111, 0.05, 11, 141, 0.5, 34, 0.6, 0),
    "greek_yogurt_whole": _ing("Whole-milk plain Greek yogurt", 97, 9.0, 4.0, 5.0, 0, 0.86, 100, 0.04, 11, 141, 0.5, 35, 0.5, 0.1),
    "skyr": _ing("Plain nonfat skyr", 63, 11.0, 4.0, 0.2, 0, 1.06, 120, 0.05, 11, 150, 0.5, 39, 0.8, 0),
    "cottage_cheese_2": _ing("2% cottage cheese", 84, 11.0, 4.3, 2.3, 0, 1.06, 91, 0.07, 8, 92, 0.4, 330, 0.6, 0),
    "cottage_cheese_4": _ing("4% cottage cheese", 98, 11.1, 3.4, 4.3, 0, 1.07, 83, 0.07, 8, 104, 0.4, 364, 0.6, 0.1),
    "milk_skim": _ing("Skim milk", 34, 3.4, 5.0, 0.2, 0, 0.33, 122, 0.03, 11, 156, 0.4, 42, 0.5, 1.2),
    "milk_2": _ing("2% milk", 50, 3.4, 4.8, 2.0, 0, 0.33, 120, 0.03, 11, 150, 0.4, 47, 0.5, 1.2),
    "milk_whole": _ing("Whole milk", 61, 3.2, 4.8, 3.3, 0, 0.31, 113, 0.03, 10, 143, 0.4, 43, 0.5, 1.3),
    "kefir_plain": _ing("Plain low-fat kefir", 41, 3.8, 4.7, 1.0, 0, 0.37, 120, 0.04, 12, 164, 0.4, 40, 0.3, 1.0),
    "egg_whole": _ing("Whole egg", 143, 12.6, 0.7, 9.5, 0, 1.08, 56, 1.75, 12, 138, 1.3, 142, 0.89, 2.0, 0.05),
    "egg_white": _ing("Egg white", 52, 10.9, 0.7, 0.2, 0, 0.92, 7, 0.08, 11, 163, 0.03, 166, 0.09, 0),
    "cheddar": _ing("Cheddar cheese", 403, 23.0, 3.4, 33.0, 0, 2.14, 710, 0.14, 28, 76, 3.1, 653, 1.1, 0.6),
    "mozzarella_ps": _ing("Part-skim mozzarella", 254, 24.3, 2.8, 15.9, 0, 2.26, 782, 0.22, 23, 84, 2.9, 619, 0.9, 0.3),
    "parmesan": _ing("Grated Parmesan", 392, 35.8, 3.2, 25.8, 0, 3.45, 1184, 0.82, 38, 125, 2.8, 1529, 1.2, 0.5),
    "feta": _ing("Feta cheese", 264, 14.2, 4.1, 21.3, 0, 1.40, 493, 0.65, 19, 62, 2.9, 917, 1.7, 0.4),
    "ricotta_ps": _ing("Part-skim ricotta", 138, 11.4, 5.1, 8.0, 0, 1.10, 272, 0.44, 15, 125, 1.2, 125, 0.3, 0.2),
    "butter": _ing("Butter", 717, 0.9, 0.1, 81.1, 0, 0.08, 24, 0.02, 2, 24, 0.1, 11, 0.2, 1.5),

    # ---------- PROTEIN POWDERS (BRAND-DEPENDENT) ----------
    "whey_isolate": _ing("Whey protein isolate powder", 370, 85.0, 5.0, 1.0, 0, 8.93, 500, 1.0, 50, 500, 2.0, 600, 0, 0),
    "whey_concentrate": _ing("Whey protein concentrate powder", 400, 75.0, 10.0, 6.0, 0, 7.88, 500, 1.0, 50, 550, 2.0, 400, 0, 0),
    "casein_powder": _ing("Micellar casein powder", 360, 78.0, 8.0, 2.0, 0, 7.25, 1500, 1.0, 60, 400, 2.0, 700, 0, 0),
    "plant_protein": _ing("Pea/rice blend plant protein powder", 380, 75.0, 8.0, 6.0, 4.0, 6.00, 200, 8.0, 90, 400, 3.0, 500, 0, 0),
    "soy_protein_isolate": _ing("Soy protein isolate powder", 335, 88.0, 0.0, 3.4, 1.6, 6.86, 178, 14.5, 39, 81, 4.0, 1005, 0, 0),

    # ---------- SOY / LEGUMES ----------
    "tofu_firm": _ing("Firm tofu", 144, 17.3, 2.8, 8.7, 2.3, 1.35, 683, 2.7, 58, 237, 1.6, 14, 0, 0.2),
    "tofu_extrafirm": _ing("Extra-firm tofu", 150, 18.0, 3.0, 8.0, 2.0, 1.40, 350, 2.7, 60, 240, 1.6, 20, 0, 0.2),
    "tofu_silken": _ing("Silken tofu", 55, 5.7, 2.4, 2.7, 0.2, 0.44, 30, 1.0, 26, 150, 0.6, 8, 0, 0.1),
    "tempeh": _ing("Tempeh", 192, 20.3, 7.6, 10.8, 5.0, 1.58, 111, 2.7, 81, 412, 1.1, 9, 0, 0.3),
    "edamame_shelled": _ing("Shelled edamame, cooked", 122, 11.9, 9.9, 5.2, 5.2, 0.93, 63, 2.3, 64, 436, 1.4, 6, 0, 0.4),
    "soy_milk_unsw": _ing("Unsweetened soy milk", 33, 2.9, 1.8, 1.6, 0.4, 0.23, 123, 0.4, 15, 118, 0.3, 39, 1.2, 1.0, 0.06),
    "black_beans": _ing("Black beans, cooked", 132, 8.9, 23.7, 0.5, 8.7, 0.71, 27, 2.1, 70, 355, 1.0, 2, 0, 0),
    "pinto_beans": _ing("Pinto beans, cooked", 143, 9.0, 26.2, 0.7, 9.0, 0.73, 46, 2.1, 50, 436, 1.0, 1, 0, 0),
    "kidney_beans": _ing("Kidney beans, cooked", 127, 8.7, 22.8, 0.5, 6.4, 0.70, 28, 2.2, 45, 405, 1.0, 1, 0, 0),
    "chickpeas": _ing("Chickpeas, cooked", 164, 8.9, 27.4, 2.6, 7.6, 0.63, 49, 2.9, 48, 291, 1.5, 7, 0, 0),
    "lentils": _ing("Lentils, cooked", 116, 9.0, 20.1, 0.4, 7.9, 0.65, 19, 3.3, 36, 369, 1.3, 2, 0, 0),
    "hummus": _ing("Hummus", 166, 7.9, 14.3, 9.6, 6.0, 0.56, 38, 2.4, 71, 228, 1.6, 379, 0, 0),
    "refried_beans_ff": _ing("Fat-free refried beans", 90, 6.0, 15.0, 0.5, 5.0, 0.48, 40, 1.8, 40, 350, 0.8, 400, 0, 0),
    "peanut_butter": _ing("Natural peanut butter", 588, 25.1, 20.0, 50.4, 6.0, 1.67, 43, 1.9, 154, 649, 2.9, 17, 0, 0),
    "pb_powder": _ing("Powdered peanut butter", 400, 50.0, 30.0, 8.0, 15.0, 3.35, 90, 3.0, 250, 1200, 4.0, 500, 0, 0),

    # ---------- NUTS / SEEDS / FATS ----------
    "almonds": _ing("Almonds", 579, 21.2, 21.6, 49.9, 12.5, 1.49, 269, 3.7, 270, 733, 3.1, 1, 0, 0),
    "almond_butter": _ing("Almond butter", 614, 20.9, 18.8, 55.5, 10.3, 1.47, 347, 3.5, 279, 748, 3.3, 7, 0, 0),
    "walnuts": _ing("Walnuts", 654, 15.2, 13.7, 65.2, 6.7, 1.17, 98, 2.9, 158, 441, 3.1, 2, 0, 9.08),
    "cashews": _ing("Cashews", 553, 18.2, 30.2, 43.9, 3.3, 1.47, 37, 6.7, 292, 660, 5.8, 12, 0, 0.06),
    "pumpkin_seeds": _ing("Pumpkin seeds", 559, 30.2, 10.7, 49.1, 6.0, 2.42, 46, 8.8, 592, 809, 7.8, 7, 0, 0.12),
    "sunflower_seeds": _ing("Sunflower seeds", 584, 20.8, 20.0, 51.5, 8.6, 1.66, 78, 5.3, 325, 645, 5.0, 9, 0, 0.07),
    "chia": _ing("Chia seeds", 486, 16.5, 42.1, 30.7, 34.4, 1.37, 631, 7.7, 335, 407, 4.6, 16, 0, 0, 17.8),
    "flax_ground": _ing("Ground flaxseed", 534, 18.3, 28.9, 42.2, 27.3, 1.24, 255, 5.7, 392, 813, 4.3, 30, 0, 0, 22.8),
    "hemp_hearts": _ing("Hemp hearts", 553, 31.6, 8.7, 48.8, 4.0, 2.16, 70, 7.9, 700, 1200, 9.9, 5, 0, 0, 8.7),
    "olive_oil": _ing("Extra-virgin olive oil", 884, 0, 0, 100, 0, 0, 1, 0.6, 0, 1, 0, 2, 0, 0, 0.76),
    "avocado": _ing("Avocado", 160, 2.0, 8.5, 14.7, 6.7, 0.14, 12, 0.6, 29, 485, 0.6, 7, 0, 0, 0.11),
    "tahini": _ing("Tahini", 595, 17.0, 21.2, 53.8, 9.3, 1.14, 426, 8.9, 95, 414, 4.6, 115, 0, 0),
    "coconut_oil": _ing("Coconut oil", 862, 0, 0, 100, 0, 0, 1, 0.1, 0, 0, 0, 0, 0, 0),

    # ---------- GRAINS / STARCHES (ALL GLUTEN-FREE CHOICES) ----------
    "oats_gf_dry": _ing("Certified GF rolled oats, dry", 379, 13.2, 67.7, 6.5, 10.1, 0.98, 52, 4.3, 138, 362, 3.6, 6, 0, 0, 0.11),
    "rice_white_cooked": _ing("White rice, cooked", 130, 2.7, 28.2, 0.3, 0.4, 0.22, 10, 0.2, 12, 35, 0.5, 1, 0, 0),
    "rice_brown_cooked": _ing("Brown rice, cooked", 123, 2.7, 25.6, 1.0, 1.6, 0.22, 3, 0.6, 39, 86, 0.7, 4, 0, 0),
    "quinoa_cooked": _ing("Quinoa, cooked", 120, 4.4, 21.3, 1.9, 2.8, 0.26, 17, 1.5, 64, 172, 1.1, 7, 0, 0, 0.04),
    "potato": _ing("Potato, cooked", 87, 2.0, 20.0, 0.1, 1.8, 0.11, 8, 0.3, 22, 379, 0.3, 5, 0, 0),
    "sweet_potato": _ing("Sweet potato, baked", 90, 2.0, 20.7, 0.2, 3.3, 0.09, 38, 0.7, 27, 475, 0.3, 36, 0, 0),
    "corn_tortilla": _ing("Corn tortilla", 218, 5.7, 44.6, 2.9, 6.3, 0.42, 81, 1.2, 72, 186, 0.9, 45, 0, 0),
    "gf_bread": _ing("Gluten-free sandwich bread (BRAND-DEPENDENT)", 265, 5.0, 47.0, 5.5, 3.5, 0.30, 90, 1.5, 20, 90, 0.5, 480, 0, 0),
    "gf_wrap": _ing("Gluten-free tortilla wrap (BRAND-DEPENDENT)", 290, 5.0, 50.0, 8.0, 4.0, 0.30, 60, 1.2, 20, 80, 0.5, 500, 0, 0),
    "chickpea_pasta_dry": _ing("Chickpea pasta, dry (BRAND-DEPENDENT)", 350, 21.0, 58.0, 5.0, 11.0, 1.51, 60, 6.0, 90, 700, 2.5, 40, 0, 0),
    "lentil_pasta_dry": _ing("Red lentil pasta, dry (BRAND-DEPENDENT)", 350, 24.0, 55.0, 2.0, 8.0, 1.73, 50, 6.5, 80, 900, 3.0, 20, 0, 0),
    "gf_pasta_dry": _ing("Brown rice pasta, dry (BRAND-DEPENDENT)", 360, 7.0, 78.0, 1.5, 3.0, 0.52, 20, 1.3, 60, 130, 1.0, 10, 0, 0),
    "rice_cake": _ing("Plain brown rice cake", 387, 8.2, 81.5, 2.8, 4.2, 0.66, 11, 1.4, 111, 283, 1.9, 26, 0, 0),
    "gf_oat_flour": _ing("GF oat flour", 404, 14.7, 65.7, 9.1, 6.5, 1.09, 55, 4.0, 144, 371, 3.6, 19, 0, 0),
    "cornmeal_polenta": _ing("Polenta, cooked", 70, 1.6, 15.0, 0.3, 0.8, 0.18, 2, 0.4, 14, 26, 0.3, 5, 0, 0),
    "popcorn_popped": _ing("Air-popped popcorn", 387, 12.9, 77.8, 4.5, 14.5, 1.13, 7, 3.2, 144, 329, 3.1, 8, 0, 0),

    # ---------- FRUIT ----------
    "banana": _ing("Banana", 89, 1.1, 22.8, 0.3, 2.6, 0.07, 5, 0.3, 27, 358, 0.2, 1, 0, 0),
    "blueberries": _ing("Blueberries", 57, 0.7, 14.5, 0.3, 2.4, 0.04, 6, 0.3, 6, 77, 0.2, 1, 0, 0),
    "strawberries": _ing("Strawberries", 32, 0.7, 7.7, 0.3, 2.0, 0.03, 16, 0.4, 13, 153, 0.1, 1, 0, 0),
    "raspberries": _ing("Raspberries", 52, 1.2, 11.9, 0.7, 6.5, 0.07, 25, 0.7, 22, 151, 0.4, 1, 0, 0),
    "mixed_berries_frozen": _ing("Frozen mixed berries", 50, 0.8, 12.0, 0.3, 3.0, 0.05, 20, 0.5, 12, 110, 0.2, 2, 0, 0),
    "mango_frozen": _ing("Frozen mango", 60, 0.8, 15.0, 0.4, 1.6, 0.04, 11, 0.2, 10, 168, 0.1, 1, 0, 0),
    "pineapple": _ing("Pineapple", 50, 0.5, 13.1, 0.1, 1.4, 0.02, 13, 0.3, 12, 109, 0.1, 1, 0, 0),
    "apple": _ing("Apple", 52, 0.3, 13.8, 0.2, 2.4, 0.02, 6, 0.1, 5, 107, 0.04, 1, 0, 0),
    "orange": _ing("Orange", 47, 0.9, 11.8, 0.1, 2.4, 0.02, 40, 0.1, 10, 181, 0.07, 0, 0, 0),
    "dates_medjool": _ing("Medjool dates", 277, 1.8, 75.0, 0.2, 6.7, 0.06, 64, 0.9, 54, 696, 0.4, 1, 0, 0),
    "raisins": _ing("Raisins", 299, 3.1, 79.2, 0.5, 3.7, 0.09, 50, 1.9, 32, 749, 0.2, 11, 0, 0),
    "lemon_juice": _ing("Lemon juice", 22, 0.4, 6.9, 0.2, 0.3, 0.01, 6, 0.1, 6, 103, 0.1, 1, 0, 0),

    # ---------- VEGETABLES ----------
    "spinach": _ing("Raw spinach", 23, 2.9, 3.6, 0.4, 2.2, 0.22, 99, 2.7, 79, 558, 0.5, 79, 0, 0, 0.14),
    "kale": _ing("Raw kale", 35, 2.9, 4.4, 1.5, 4.1, 0.21, 254, 1.6, 33, 348, 0.4, 53, 0, 0, 0.18),
    "broccoli_cooked": _ing("Broccoli, cooked", 35, 2.4, 7.2, 0.4, 3.3, 0.13, 40, 0.7, 21, 293, 0.5, 41, 0, 0, 0.06),
    "bell_pepper": _ing("Bell pepper", 26, 1.0, 6.0, 0.3, 2.1, 0.03, 7, 0.4, 12, 211, 0.1, 4, 0, 0),
    "onion": _ing("Onion", 40, 1.1, 9.3, 0.1, 1.7, 0.03, 23, 0.2, 10, 146, 0.2, 4, 0, 0),
    "garlic": _ing("Garlic", 149, 6.4, 33.1, 0.5, 2.1, 0.31, 181, 1.7, 25, 401, 1.2, 17, 0, 0),
    "tomato": _ing("Tomato", 18, 0.9, 3.9, 0.2, 1.2, 0.03, 10, 0.3, 11, 237, 0.2, 5, 0, 0),
    "cherry_tomatoes": _ing("Cherry tomatoes", 18, 0.9, 3.9, 0.2, 1.2, 0.03, 10, 0.3, 11, 237, 0.2, 5, 0, 0),
    "zucchini": _ing("Zucchini", 17, 1.2, 3.1, 0.3, 1.0, 0.06, 16, 0.4, 18, 261, 0.3, 8, 0, 0),
    "mushrooms": _ing("White mushrooms", 22, 3.1, 3.3, 0.3, 1.0, 0.12, 3, 0.5, 9, 318, 0.5, 5, 0.04, 0.2),
    "cucumber": _ing("Cucumber", 15, 0.7, 3.6, 0.1, 0.5, 0.02, 16, 0.3, 13, 147, 0.2, 2, 0, 0),
    "carrot": _ing("Carrot", 41, 0.9, 9.6, 0.2, 2.8, 0.04, 33, 0.3, 12, 320, 0.2, 69, 0, 0),
    "cauliflower_rice": _ing("Riced cauliflower", 25, 1.9, 5.0, 0.3, 2.0, 0.11, 22, 0.4, 15, 299, 0.3, 30, 0, 0),
    "sweet_corn": _ing("Sweet corn kernels", 86, 3.3, 19.0, 1.4, 2.0, 0.35, 2, 0.5, 37, 270, 0.5, 15, 0, 0),
    "peas_frozen": _ing("Frozen green peas", 77, 5.2, 13.6, 0.4, 4.5, 0.32, 25, 1.5, 33, 240, 1.2, 108, 0, 0),
    "salsa": _ing("Jarred salsa", 29, 1.5, 6.6, 0.2, 1.8, 0.04, 25, 0.6, 15, 275, 0.2, 430, 0, 0),
    "marinara": _ing("Marinara sauce", 60, 1.6, 8.5, 2.0, 2.0, 0.05, 25, 0.9, 20, 350, 0.3, 400, 0, 0),
    "coleslaw_mix": _ing("Shredded cabbage/carrot slaw mix", 27, 1.3, 6.0, 0.1, 2.3, 0.04, 42, 0.5, 13, 200, 0.2, 20, 0, 0),
    "roasted_red_pepper": _ing("Jarred roasted red pepper", 25, 1.0, 5.0, 0.2, 1.5, 0.03, 10, 0.5, 12, 200, 0.1, 350, 0, 0),
    "pickled_jalapeno": _ing("Pickled jalapeno", 27, 0.9, 5.0, 0.9, 2.6, 0.03, 23, 1.9, 15, 193, 0.1, 1500, 0, 0),

    # ---------- CLEAN POULTRY / FISH (SDA-COMPATIBLE SECTION ONLY) ----------
    "chicken_breast": _ing("Chicken breast, cooked", 165, 31.0, 0, 3.6, 0, 2.33, 15, 1.0, 29, 256, 1.0, 74, 0.3, 0.1, 0, 0.03),
    "chicken_thigh": _ing("Chicken thigh, skinless, cooked", 209, 26.0, 0, 10.9, 0, 1.95, 12, 1.3, 25, 240, 2.2, 88, 0.6, 0.1, 0, 0.05),
    "turkey_breast": _ing("Turkey breast, cooked", 135, 30.1, 0, 1.0, 0, 2.26, 12, 1.1, 30, 300, 1.7, 60, 0.4, 0.1, 0, 0.02),
    "ground_turkey_93": _ing("93% lean ground turkey, cooked", 176, 27.0, 0, 7.5, 0, 2.03, 25, 1.6, 28, 300, 3.0, 80, 1.2, 0.1, 0, 0.05),
    "salmon": _ing("Atlantic salmon, cooked", 206, 22.1, 0, 12.4, 0, 1.70, 15, 0.3, 30, 384, 0.4, 61, 3.2, 13.1, 0.1, 2.02),
    "canned_tuna": _ing("Canned light tuna in water, drained", 116, 25.5, 0, 0.8, 0, 1.96, 11, 1.0, 27, 237, 0.7, 247, 2.2, 1.7, 0, 0.27),
    "canned_salmon": _ing("Canned pink salmon, drained", 139, 19.8, 0, 6.0, 0, 1.52, 213, 0.7, 29, 326, 0.8, 397, 4.4, 12.0, 0, 1.5),
    "cod": _ing("Cod, cooked", 105, 22.8, 0, 0.9, 0, 1.75, 14, 0.5, 36, 244, 0.6, 78, 1.0, 1.2, 0, 0.19),
    "tilapia": _ing("Tilapia, cooked", 129, 26.2, 0, 2.7, 0, 2.02, 14, 0.7, 34, 380, 0.4, 56, 1.9, 3.1, 0, 0.19),
    "shrimp_NOT": _ing("Shrimp (NOT SDA-compatible; listed only as an exclusion marker)", 0, 0, 0, 0, 0, 0),
    "sardines": _ing("Canned sardines in water, drained", 208, 24.6, 0, 11.5, 0, 1.89, 382, 2.9, 39, 397, 1.3, 307, 8.9, 4.8, 0, 0.98),

    # ---------- FLAVOR / MISC ----------
    "honey": _ing("Honey", 304, 0.3, 82.4, 0, 0.2, 0.01, 6, 0.4, 2, 52, 0.2, 4, 0, 0),
    "maple_syrup": _ing("Maple syrup", 260, 0, 67.0, 0.1, 0, 0, 102, 0.1, 21, 212, 1.5, 12, 0, 0),
    "cocoa_powder": _ing("Unsweetened cocoa powder", 228, 19.6, 57.9, 13.7, 33.2, 1.13, 128, 13.9, 499, 1524, 6.8, 21, 0, 0),
    "dark_chocolate_70": _ing("70% dark chocolate", 598, 7.8, 45.9, 42.6, 10.9, 0.45, 73, 11.9, 228, 715, 3.3, 20, 0, 0),
    "choc_chips_mini": _ing("Semisweet chocolate chips", 480, 4.2, 63.9, 24.2, 5.9, 0.24, 32, 3.1, 115, 365, 1.6, 11, 0, 0),
    "nutritional_yeast": _ing("Nutritional yeast (fortified)", 350, 50.0, 36.0, 5.0, 20.0, 3.60, 40, 5.0, 130, 2000, 8.0, 30, 40.0, 0),
    "soy_sauce_gf": _ing("Gluten-free tamari", 60, 10.5, 5.6, 0.1, 0.8, 0.62, 20, 2.4, 40, 217, 0.4, 5586, 0, 0),
    "sriracha": _ing("Sriracha", 93, 1.9, 19.2, 0.9, 2.2, 0.05, 18, 1.3, 20, 320, 0.2, 2124, 0, 0),
    "salsa_verde": _ing("Salsa verde", 36, 1.0, 7.0, 0.5, 1.5, 0.03, 20, 0.5, 12, 250, 0.2, 500, 0, 0),
    "greek_dressing_lite": _ing("Light vinaigrette", 120, 0.3, 6.0, 10.0, 0, 0.01, 5, 0.2, 3, 20, 0.05, 700, 0, 0),
    "coconut_milk_light": _ing("Light canned coconut milk", 73, 0.7, 2.8, 7.0, 0.4, 0.05, 8, 1.0, 20, 180, 0.2, 15, 0, 0),
    "curry_paste": _ing("Thai red curry paste", 100, 2.0, 16.0, 3.0, 4.0, 0.10, 40, 2.0, 25, 300, 0.3, 2500, 0, 0),
    "almond_milk_unsw": _ing("Unsweetened almond milk", 15, 0.6, 0.6, 1.2, 0.3, 0.04, 188, 0.3, 7, 67, 0.1, 72, 0, 1.0),
    "cold_brew": _ing("Unsweetened cold brew coffee", 2, 0.2, 0, 0, 0, 0.01, 3, 0.02, 4, 60, 0.02, 3, 0, 0),
    "matcha": _ing("Matcha powder", 324, 29.0, 39.0, 5.0, 32.0, 1.80, 420, 17.0, 230, 2100, 6.0, 6, 0, 0),
    "tapioca_pearls_dry": _ing("Dry tapioca (boba) pearls", 358, 0.2, 89.0, 0.02, 0.9, 0.01, 20, 1.6, 1, 11, 0.1, 1, 0, 0),
    "black_tea_brewed": _ing("Brewed black tea", 1, 0, 0.3, 0, 0, 0, 0, 0.02, 3, 37, 0.02, 3, 0, 0),
    "sugar": _ing("Granulated sugar", 387, 0, 100.0, 0, 0, 0, 1, 0.05, 0, 2, 0, 1, 0, 0),
    "brown_sugar": _ing("Brown sugar", 380, 0.1, 98.1, 0, 0, 0, 83, 0.7, 9, 133, 0.03, 28, 0, 0),
    "sugar_free_syrup": _ing("Sugar-free pancake syrup", 40, 0, 10.0, 0, 4.0, 0, 0, 0, 0, 0, 0, 100, 0, 0),
    "baking_powder": _ing("Baking powder", 53, 0, 27.7, 0, 0.2, 0, 5876, 8.6, 29, 20500, 0.1, 10600, 0, 0),
    "cinnamon": _ing("Ground cinnamon", 247, 4.0, 80.6, 1.2, 53.1, 0.17, 1002, 8.3, 60, 431, 1.8, 10, 0, 0),
    "vanilla_extract": _ing("Vanilla extract", 288, 0.1, 12.7, 0.1, 0, 0, 11, 0.1, 12, 148, 0.1, 9, 0, 0),
    "salt": _ing("Table salt", 0, 0, 0, 0, 0, 0, 24, 0.3, 1, 8, 0.1, 38758, 0, 0),
    "spice_generic": _ing("Dried spices/herbs blend", 250, 10.0, 50.0, 5.0, 25.0, 0.30, 500, 15.0, 200, 1500, 2.0, 50, 0, 0),
    "ketchup": _ing("Ketchup", 101, 1.0, 25.8, 0.1, 0.3, 0.03, 15, 0.35, 13, 281, 0.1, 907, 0, 0),
    "mustard_yellow": _ing("Yellow mustard", 60, 3.7, 5.8, 3.4, 3.3, 0.25, 63, 1.6, 48, 152, 0.6, 1135, 0, 0),
    # ---------- ADDED FROM JARON'S OWN RECIPE COLLECTION ----------
    "impossible_patty": _ing("Impossible burger patty (GF)", 231, 19.2, 9.2, 13.8, 3.1, 1.50, 31, 4.2, 30, 610, 5.5, 370, 2.4, 0),
    "gf_english_muffin": _ing("GF English muffin", 245, 4.5, 47.0, 4.0, 3.5, 0.37, 60, 1.2, 20, 90, 0.4, 420, 0, 0),
    "hash_brown_patty": _ing("Frozen hash brown patty", 195, 2.3, 24.0, 10.5, 2.2, 0.13, 12, 0.6, 22, 380, 0.3, 350, 0, 0),
    "mayo": _ing("Mayonnaise", 680, 1.0, 0.6, 75.0, 0, 0.09, 8, 0.2, 1, 20, 0.1, 635, 0.1, 0.1),
    "sour_cream": _ing("Sour cream", 198, 2.4, 4.6, 19.4, 0, 0.23, 101, 0.06, 10, 141, 0.3, 40, 0.3, 0.1),
    "cream_cheese_whipped": _ing("Whipped cream cheese", 318, 5.9, 5.0, 30.6, 0, 0.57, 98, 0.11, 9, 138, 0.5, 320, 0.3, 0.1),
    "whipped_cream": _ing("Whipped cream, aerosol", 257, 3.2, 12.5, 22.2, 0, 0.31, 101, 0.04, 9, 147, 0.3, 130, 0.3, 0.2),
    "artichoke_hearts": _ing("Canned artichoke hearts in water", 47, 2.6, 10.5, 0.3, 5.4, 0.15, 44, 0.6, 42, 286, 0.4, 380, 0, 0),
    "green_chilies": _ing("Canned diced green chilies", 20, 0.9, 4.3, 0.1, 1.5, 0.05, 15, 0.4, 12, 130, 0.1, 550, 0, 0),
    "mung_bean_pasta_dry": _ing("Mung bean fettuccine, dry", 340, 45.0, 40.0, 2.0, 20.0, 3.40, 90, 8.5, 130, 900, 3.0, 25, 0, 0),
    "gf_lasagna_noodle_dry": _ing("GF lasagna noodles, dry", 357, 6.3, 78.0, 1.3, 2.5, 0.52, 12, 1.3, 30, 90, 0.5, 8, 0, 0),
    "gf_ravioli_cheese": _ing("GF cheese ravioli", 245, 10.0, 32.0, 8.5, 2.0, 0.90, 160, 1.1, 22, 110, 1.0, 480, 0.3, 0),
    "rice_noodles_dry": _ing("Rice noodles, dry", 364, 3.4, 83.0, 0.6, 1.6, 0.28, 18, 0.7, 12, 30, 0.5, 20, 0, 0),
    "buffalo_sauce": _ing("Buffalo wing sauce", 60, 0.5, 5.0, 4.5, 0.5, 0.02, 10, 0.3, 5, 80, 0.1, 2200, 0, 0),
    "acv": _ing("Apple cider vinegar", 21, 0, 0.9, 0, 0, 0, 7, 0.2, 5, 73, 0, 5, 0, 0),
    "applesauce_unsw": _ing("Unsweetened applesauce", 42, 0.2, 11.3, 0.1, 1.1, 0.01, 4, 0.2, 3, 75, 0, 2, 0, 0),
    "gf_sandwich_cookie": _ing("GF chocolate sandwich cookie", 468, 4.0, 71.0, 19.0, 3.0, 0.28, 20, 3.0, 30, 100, 0.4, 380, 0, 0),
    "string_cheese_light": _ing("Light mozzarella string cheese", 250, 30.0, 5.0, 12.5, 0, 2.90, 750, 0.2, 25, 90, 3.0, 950, 1.0, 0.2),
    "bean_sprouts": _ing("Mung bean sprouts", 30, 3.0, 5.9, 0.2, 1.8, 0.20, 13, 0.9, 21, 149, 0.4, 6, 0, 0),
    "peanuts_roasted": _ing("Roasted peanuts", 587, 24.4, 21.5, 49.7, 8.4, 1.59, 54, 2.3, 176, 634, 3.3, 6, 0, 0),
    "green_onion": _ing("Green onion / scallion", 32, 1.8, 7.3, 0.2, 2.6, 0.09, 72, 1.5, 20, 276, 0.4, 16, 0, 0),
    "cornstarch": _ing("Cornstarch", 381, 0.3, 91.3, 0.1, 0.9, 0.02, 2, 0.5, 3, 3, 0.1, 9, 0, 0),
    "coconut_milk_full": _ing("Full-fat coconut milk, canned", 197, 2.0, 2.8, 21.3, 0, 0.15, 16, 3.3, 37, 220, 0.6, 13, 0, 0),
    "sf_pudding_mix": _ing("Sugar-free instant pudding mix", 350, 0, 87.5, 0, 0, 0, 30, 0, 5, 20, 0, 3000, 0, 0),
    "cholula": _ing("Cholula-style hot sauce", 15, 0.5, 2.5, 0.2, 0.5, 0.02, 10, 0.3, 5, 60, 0, 3400, 0, 0),
    "romaine": _ing("Romaine lettuce", 17, 1.2, 3.3, 0.3, 2.1, 0.07, 33, 0.97, 14, 247, 0.2, 8, 0, 0),
    "gf_burger_bun": _ing("GF burger bun", 270, 4.5, 48.0, 6.5, 3.0, 0.37, 70, 1.3, 22, 95, 0.5, 400, 0, 0),
    "vanilla_ice_cream": _ing("Vanilla ice cream", 207, 3.5, 23.6, 11.0, 0.7, 0.34, 128, 0.09, 14, 199, 0.7, 80, 0.4, 0.1),
    "frozen_fries": _ing("Frozen oven fries", 165, 2.4, 26.0, 5.5, 2.5, 0.14, 12, 0.7, 24, 420, 0.3, 320, 0, 0),
    "gf_breadcrumbs": _ing("GF breadcrumbs / panko", 380, 7.0, 78.0, 3.0, 3.0, 0.58, 30, 1.5, 25, 100, 0.5, 500, 0, 0),
    "pumpkin_puree": _ing("Canned pumpkin puree", 34, 1.1, 8.1, 0.3, 2.9, 0.05, 26, 1.4, 23, 206, 0.2, 5, 0, 0),
}

# Household measure conversions used in recipe write-ups (grams).
MEASURES = {
    "greek_yogurt_nonfat": (170, "3/4 cup (one 6 oz container)"),
    "cottage_cheese_2": (226, "1 cup"),
    "milk_2": (244, "1 cup"),
    "milk_skim": (245, "1 cup"),
    "soy_milk_unsw": (243, "1 cup"),
    "almond_milk_unsw": (240, "1 cup"),
    "egg_whole": (50, "1 large egg"),
    "egg_white": (33, "1 large egg white"),
    "oats_gf_dry": (40, "1/2 cup dry"),
    "whey_isolate": (30, "1 scoop"),
    "peanut_butter": (32, "2 tbsp"),
    "pb_powder": (12, "2 tbsp"),
    "olive_oil": (14, "1 tbsp"),
    "chia": (12, "1 tbsp"),
    "flax_ground": (7, "1 tbsp"),
    "honey": (21, "1 tbsp"),
    "rice_white_cooked": (158, "1 cup cooked"),
    "black_beans": (172, "1 cup cooked"),
    "banana": (118, "1 medium"),
    "avocado": (100, "1/2 large"),
    "cocoa_powder": (5, "1 tbsp"),
    "corn_tortilla": (26, "1 small tortilla"),
}
