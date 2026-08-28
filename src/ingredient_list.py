# -*- coding: utf-8 -*-
"""Aisle map: which supermarket aisle every ingredient key belongs to.

Consumed by src/build_data.py, which bakes it into assets/data.js so the app can
group a shopping list the way the store is actually laid out. Every key used by a
recipe must appear in exactly one aisle; build_data.py reports the ones that do not.
"""

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
