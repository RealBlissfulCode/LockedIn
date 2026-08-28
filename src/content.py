# -*- coding: utf-8 -*-
"""Written content for the handbook. HTML fragments."""

ASSUMPTIONS = """
<h2 id="assumptions">1. The ground rules</h2>
<p class="lead">Four things govern every page that follows. Worth two minutes before I cook anything.</p>

<h3>Everything is gluten-free</h3>
<p>Celiac since around age 11 is an autoimmune condition, not a preference, and cross-contamination
counts. So there is no wheat pasta, no ordinary bread, no seitan, no standard oats and no regular
soy sauce anywhere in here. Where a product is commonly contaminated rather than inherently unsafe,
it is called out at the ingredient: oats must say <strong>certified gluten-free</strong>, soy sauce
becomes <strong>gluten-free tamari</strong>, and protein powder needs a certification on the tub
because whey is frequently processed on shared lines.</p>

<h3>The numbers run off my current stats</h3>
<p>20 years old, 150 lb, 5'8", measured May 2026. Nothing is hard-coded to those figures though.
Every target comes out of a formula, so when my weight moves I recalculate rather than needing
a new document. The calculator does it for me.</p>

<h3>Vegetarian by default, meat kept separate</h3>
<p>The main catalog is lacto-ovo vegetarian, which reflects how I grew up rather than a rule me
are bound to. Clean meat and fish live in their own section. Nothing in the main catalog depends on
anything in that section, so I can ignore it entirely or lean on it as I go.</p>

<h3>How exact the macros are</h3>
<p>Every calorie and macro is calculated from gram weights against per-100 g values from USDA
FoodData Central, which is why quantities are given in grams first and cups second. Cups are for
cooking, grams are for the math. Leucine is the one soft number: USDA publishes full amino acid
profiles for many foods but not all, so where one is missing, leucine comes from protein multiplied
by a food-group fraction. Treat leucine as accurate to roughly plus or minus 10 percent. Branded
items vary between manufacturers, so check my own labels on anything I eat daily.</p>
"""


TARGETS = """
<h2 id="targets">2. My numbers</h2>

<h3>The starting point</h3>
<p>Mifflin-St Jeor is the most accurate of the common BMR equations for people in my range.
For a male: <code>BMR = (10 x kg) + (6.25 x cm) - (5 x age) + 5</code>.</p>
<p>At 66.7 kg, 172.7 cm, age 20, that gives <strong>1,635 kcal/day BMR</strong>. My Hume Pod
reported 1,718, which is close enough that the two methods agree. Multiply by an activity factor
to get maintenance:</p>
<table>
<tr><th>Activity factor</th><th>Describes</th><th>Estimated maintenance</th></tr>
<tr><td>1.55</td><td>Desk job, training 4 to 5x/week</td><td>2,530 kcal</td></tr>
<tr><td>1.725</td><td>Physical job, daily training</td><td><strong>2,820 kcal</strong></td></tr>
<tr><td>1.9</td><td>Heavy manual labor plus daily hard training</td><td>3,105 kcal</td></tr>
</table>
<p>Laser engraving work plus daily training puts me between 1.725 and 1.9. My working maintenance
estimate is <strong>2,800 to 2,800 kcal</strong>.</p>

<h3>Targets by goal</h3>
<table>
<tr><th>Goal</th><th>Calories</th><th>Protein</th><th>Fat</th><th>Carbs</th><th>Rate</th></tr>
<tr><td><strong>Lean gain (my current goal)</strong></td><td>3,050 to 3,250</td><td>150 to 165 g</td><td>85 to 95 g</td><td>420 to 460 g</td><td>+0.25 to 0.5 lb/week</td></tr>
<tr><td>Maintenance / recomp</td><td>2,800 to 2,800</td><td>150 to 175 g</td><td>80 to 90 g</td><td>370 to 420 g</td><td>Flat</td></tr>
<tr><td>Cut</td><td>2,300 to 2,500</td><td>165 to 185 g</td><td>65 to 80 g</td><td>260 to 300 g</td><td>-0.5 to 0.75 lb/week</td></tr>
</table>

<h3>The formulas, so I can recalculate</h3>
<ul>
<li><strong>Protein:</strong> bodyweight in lb x 1.0 to 1.1 during a gain, x 1.1 to 1.25 during a cut.
At 150 lb that is 147 to 162 g gaining, 162 to 184 g cutting. Cross-check against lean mass:
1.0 to 1.2 g per lb of lean mass, and at 120 lb lean that gives 115 to 138 g. The higher of the
two is the safer target while gaining. <strong>Call it 155 g/day.</strong></li>
<li><strong>Fat:</strong> minimum 0.35 g per lb of bodyweight, so 51 g is the floor, never go under
it. Target 0.55 to 0.65 g/lb, which is 80 to 95 g. Fat below about 20 percent of calories for
extended periods is associated with lower testosterone in trained men.</li>
<li><strong>Carbs:</strong> whatever is left. <code>(total kcal - (protein x 4) - (fat x 9)) / 4</code>.
At 3,150 kcal with 155 g protein and 90 g fat: (3,150 - 620 - 810) / 4 = <strong>430 g.</strong></li>
<li><strong>Fiber:</strong> 14 g per 1,000 kcal. At 3,150 kcal that is <strong>44 g/day.</strong></li>
<li><strong>Water:</strong> 35 ml per kg baseline (2.3 L), plus 500 to 1,000 ml per hour of training or
hot work. Realistically <strong>3.5 to 4.5 L/day</strong> on a work-plus-training day.</li>
</ul>

<h3>The honest part</h3>
<p>My file says I skip breakfast every day, sometimes skip lunch, eat one or two dinners, and
deliberately try to eat as little as possible to keep my abs visible. On a physical job with
daily training, that pattern probably puts me somewhere between 1,600 and 2,200 kcal. If that
is accurate, I have been running a 800 to 1,400 calorie daily deficit against my actual
expenditure while trying to build muscle. That is the ceiling on my progress, and no
programming change fixes it.</p>
<p>Do not jump from 1,800 to 3,150 overnight. I will feel bloated, sluggish, and convinced it
is fat gain, and I will quit. <strong>Add 250 kcal per week</strong> until I reach the target.
That is roughly one of the D-series shakes, or one extra meal-sized snack. Six weeks to get
there. Track the trend, not the day.</p>

<h3>Adjustment rules</h3>
<ul>
<li>Weigh myself daily, same conditions: fasted, after the bathroom, before food or water. Use
the <strong>7-day average</strong>, never a single day.</li>
<li>Compare this week's average to the average from two weeks ago. One week is noise.</li>
<li>Gaining and the average has not moved in 3 weeks: add 200 kcal/day.</li>
<li>Gaining faster than 0.75 lb/week for 3 weeks: subtract 200 kcal/day.</li>
<li>Cutting and the average has not moved in 3 weeks: subtract 200 kcal/day or add 2,000 steps.</li>
<li>Daily swings of 3 to 4 lb are water, glycogen, sodium and gut contents. Every 1 g of stored
glycogen holds roughly 3 g of water. A high-carb day can put 2 lb on the scale with zero fat gain.</li>
</ul>
"""

PROTEIN = """
<h2 id="protein">3. Protein, essential amino acids, and leucine</h2>

<h3>Why protein is listed as grams and not as a percentage</h3>
<p>Percentage targets move when my calories move, which makes them useless. Protein
requirements scale with body mass and training, not with how much I happen to be eating.</p>

<h3>The essential amino acids</h3>
<p>Nine amino acids cannot be synthesized by the body and must come from food. Everything my
body builds, including contractile muscle protein, needs all nine present at the same time.
Running short on any one caps the rate at which the rest can be used, which is why protein
"quality" is a real concept rather than marketing.</p>
<table>
<tr><th>Amino acid</th><th>Main roles</th><th>Notably rich sources</th></tr>
<tr><td><strong>Leucine</strong></td><td>The primary trigger for muscle protein synthesis via mTORC1 signaling; also oxidized for energy</td><td>Whey, dairy, eggs, soy</td></tr>
<tr><td>Isoleucine</td><td>Glucose uptake into muscle, energy metabolism</td><td>Dairy, eggs, legumes</td></tr>
<tr><td>Valine</td><td>Energy substrate, tissue repair</td><td>Dairy, soy, seeds</td></tr>
<tr><td>Lysine</td><td>Collagen crosslinking, calcium absorption, carnitine synthesis. The limiting amino acid in most grains.</td><td>Dairy, legumes, quinoa</td></tr>
<tr><td>Methionine</td><td>Methyl donor, sulfur source. The limiting amino acid in most legumes.</td><td>Eggs, dairy, grains, seeds</td></tr>
<tr><td>Phenylalanine</td><td>Precursor to tyrosine, dopamine, adrenaline</td><td>Dairy, soy, nuts</td></tr>
<tr><td>Threonine</td><td>Collagen and elastin, gut mucosal protein</td><td>Dairy, eggs, lentils</td></tr>
<tr><td>Tryptophan</td><td>Serotonin and melatonin precursor</td><td>Dairy, oats, seeds</td></tr>
<tr><td>Histidine</td><td>Carnosine synthesis (muscle buffering), histamine</td><td>Dairy, eggs, beans</td></tr>
</table>
<p>Note the pattern in the last two columns: <strong>grains are low in lysine, legumes are low in
methionine.</strong> Eaten across the same day they complement each other completely. This is why
rice and beans, or oats and dairy, are nutritionally robust combinations rather than folk wisdom.
They do not need to be in the same meal; the free amino acid pool persists for hours.</p>

<h3>Leucine, without the oversimplification</h3>
<p>Leucine concentration in a meal is the strongest single predictor of whether that meal
maximally stimulates muscle protein synthesis. The commonly cited threshold is roughly 2.5 to 3 g
of leucine per feeding for a young trained male. But three qualifications matter:</p>
<ol>
<li><strong>Leucine triggers the response; the other eight essential amino acids build the tissue.</strong>
Free leucine on its own raises signaling and does very little for actual accretion. This is why
BCAA supplements are largely pointless if I am already eating enough protein.</li>
<li><strong>Total daily protein dominates.</strong> Hitting the leucine threshold four times a day while
eating 90 g of total protein will not outperform 155 g spread carelessly.</li>
<li><strong>Energy availability gates everything.</strong> In a large deficit, muscle protein synthesis is
suppressed regardless of leucine. This is the specific reason my under-eating matters more than
my programming.</li>
</ol>
<p>Practically: aim for <strong>4 feedings of 35 to 45 g protein</strong> across the day, each landing
above 2.5 g leucine. The <span class="tag t-leu">LEUCINE PRIORITY</span> tag marks meals that
clear 3.0 g on their own.</p>

<h3>Protein source comparison</h3>
<table>
<tr><th>Source</th><th>Protein per 100 g</th><th>Leucine % of protein</th><th>Digestibility</th><th>Practical read</th></tr>
<tr><td>Whey isolate</td><td>85 g</td><td>~10.5%</td><td>Very high, fast</td><td>The most leucine-dense option that exists. 30 g scoop delivers ~2.7 g leucine.</td></tr>
<tr><td>Casein</td><td>78 g</td><td>~9.3%</td><td>High, slow</td><td>Clots in the stomach, releases over 5 to 7 hours. Useful pre-bed.</td></tr>
<tr><td>Whole egg</td><td>12.6 g</td><td>~8.6%</td><td>Very high</td><td>Reference-standard amino acid profile. The yolk contains the choline and vitamin D.</td></tr>
<tr><td>Greek yogurt / cottage cheese</td><td>10 to 11 g</td><td>~9.6%</td><td>High</td><td>Best food-based protein per dollar available to me.</td></tr>
<tr><td>Soy (tofu, tempeh, isolate)</td><td>17 to 20 g</td><td>~7.8%</td><td>High</td><td>The only plant protein with a genuinely complete profile and no meaningful limiting amino acid.</td></tr>
<tr><td>Legumes (beans, lentils, chickpeas)</td><td>9 g</td><td>~7.2%</td><td>Moderate</td><td>Low in methionine, high in fiber. Excellent as part of a mixed diet, weak as a sole source.</td></tr>
<tr><td>Pea/rice blend powder</td><td>75 g</td><td>~8.0%</td><td>Moderate to high</td><td>The rice covers pea's methionine gap. Needs ~20% more grams than whey for equal leucine.</td></tr>
<tr><td>Grains (oats, rice, quinoa)</td><td>2.7 to 13 g</td><td>~7.4%</td><td>Moderate</td><td>Contribute meaningfully at volume. Quinoa is the only common one that is close to complete.</td></tr>
<tr><td>Nuts and seeds</td><td>15 to 31 g</td><td>~6.7%</td><td>Moderate</td><td>Treat as a fat source that happens to contain protein, not as a protein source.</td></tr>
</table>

<h3>Reading a label properly</h3>
<p>A tub advertising "47% protein" means 47 g of protein per 100 g of powder. It says nothing
about amino acid profile, and nothing about how much of that protein my body can actually use.
Three things to check, in order:</p>
<ol>
<li><strong>Protein per serving, then serving size.</strong> A 40 g scoop with 24 g protein is 60% protein.
A 30 g scoop with 25 g protein is 83%. The second is better value even at a higher price per tub.</li>
<li><strong>Ingredient order.</strong> If maltodextrin or glycine appears high on the list on a product
claiming high protein, be suspicious. Glycine and taurine are cheap nitrogen sources that inflate
crude protein readings without contributing usefully to muscle protein synthesis.</li>
<li><strong>Third-party testing and gluten-free certification.</strong> For me the second is not optional.</li>
</ol>

<h3>How much protein is too much</h3>
<p>Above roughly 1.1 g per lb of bodyweight the additional muscle-building return is close to
zero in healthy trained individuals. Protein is not harmful at higher intakes in people with
normal kidney function, but it is expensive, filling, and displaces carbohydrate that would
otherwise fuel training. Once I am at 155 g, put further calories into carbohydrate first,
then fat. Going from 155 g to 220 g of protein buys me nothing except a smaller food budget.</p>

<h3>Meal distribution</h3>
<table>
<tr><th>Pattern</th><th>Per-meal protein</th><th>Works if</th></tr>
<tr><td>2 meals</td><td>75 to 80 g</td><td>I am willing to add one shake. Per-meal utilization is not a hard cap, but 75 g in one sitting is less efficient than 40 g twice.</td></tr>
<tr><td>2 meals + 1 shake</td><td>50 / 50 / 35 g</td><td>Realistic for my schedule. This is the pattern to default to.</td></tr>
<tr><td>3 meals + 1 snack</td><td>40 g each</td><td>The textbook optimum. Slightly better than the above, but only if I actually do it.</td></tr>
<tr><td>4+ meals</td><td>35 to 40 g</td><td>Marginal further benefit. Not worth the logistics on a job site.</td></tr>
</table>
"""

CARBS_FAT_FIBER = """
<h2 id="cfw">4. Carbohydrate, fat, fiber, water</h2>

<h3>Carbohydrate</h3>
<p>Carbohydrate is stored as glycogen in muscle and liver, roughly 400 to 500 g total in a trained
male my size. Glycogen is the dominant fuel for the 6 to 20 rep range where most of my
hypertrophy work sits. Depleted glycogen shows up as reps disappearing off the back end of sets,
which reads like a recovery problem but is a fueling problem.</p>
<p>Carbohydrate is also protein-sparing: adequate carbohydrate means amino acids get used for
tissue rather than oxidized for energy. Nothing about carbohydrates makes me fat except eating
more total calories than I burn. Ranges by context, in g per lb of bodyweight:</p>
<table>
<tr><th>Context</th><th>g/lb</th><th>At 150 lb</th></tr>
<tr><td>Lean gain, high-volume training</td><td>2.5 to 3.2</td><td>370 to 470 g</td></tr>
<tr><td>Maintenance / recomp</td><td>2.2 to 2.8</td><td>325 to 410 g</td></tr>
<tr><td>Cut</td><td>1.5 to 2.2</td><td>220 to 325 g</td></tr>
<tr><td>Rest day</td><td>Drop 10 to 15% from training day, or leave it flat</td><td>Either is fine</td></tr>
</table>
<p>Do not cut carbs on rest days as a reflex. Glycogen resynthesis after a hard session takes 24
hours or more, and a rest day is when it happens.</p>

<h3>Fat</h3>
<p>Dietary fat provides the two essential fatty acids (linoleic and alpha-linolenic), builds cell
membranes, carries vitamins A, D, E and K, and supplies the cholesterol backbone for steroid
hormone synthesis. The last point is the one that matters for me specifically: sustained
low-fat, low-calorie intake in lean young men reliably lowers testosterone.</p>
<p><strong>Absolute floor: 0.35 g/lb, or 51 g/day. Target 80 to 95 g.</strong> Saturated fat is not
something to eliminate, but keeping it under roughly 10% of total calories (about 35 g at 3,150
kcal) is the sensible default. Priority sources: olive oil, avocado, nuts and seeds, whole eggs,
full-fat dairy where it fits, and fatty fish if I eat it.</p>

<h3>Fiber</h3>
<p>Fiber feeds gut bacteria that produce short-chain fatty acids, slows gastric emptying (which
drives satiety), blunts post-meal glucose swings, and is independently associated with lower
cardiovascular risk. My target is <strong>44 g/day</strong>.</p>
<p>One caution specific to me: celiac disease damages the intestinal villi, and even in
well-managed cases the gut can be more sensitive than average. Going from a low-fiber intake to
44 g in a week will produce gas, bloating and cramping that I may misread as a gluten exposure.
<strong>Increase by about 5 g per week</strong> and increase water at the same time.</p>

<h3>Hydration</h3>
<p>Baseline: 35 ml per kg, so 2.3 L for me. Add 500 to 1,000 ml per hour of training. Add more
again for hot work, and Colorado's altitude and dry air increase respiratory water loss
noticeably compared to sea level.</p>
<p>A 2% loss of bodyweight in fluid measurably reduces strength output and time to fatigue. For
me that is 3 lb. Practical check: urine should be pale straw, not clear and not dark yellow.
Clear all day means I am over-drinking and diluting sodium. If I sweat heavily on the job,
I am losing 500 to 1,500 mg of sodium per liter of sweat; salt my food, and on a hot
outdoor day an electrolyte tab is legitimate rather than a supplement gimmick.</p>
"""

MICROS = """
<h2 id="micros">5. Micronutrients</h2>
<p>Percentages below are against the FDA Daily Value for an adult male. The "Watch" column flags
where my specific diet pattern creates risk: a vegetarian-leaning, gluten-free, historically
under-eating diet has three predictable gaps, which are <strong>B12, iron, and vitamin D</strong>,
with zinc and iodine as secondary concerns.</p>
<table class="micro">
<tr><th>Nutrient</th><th>DV</th><th>What it does</th><th>Best sources here</th><th>Watch</th></tr>
<tr><td><strong>Vitamin B12</strong></td><td>2.4 mcg</td><td>Red blood cell formation, myelin, DNA synthesis. Deficiency causes fatigue and, if prolonged, irreversible nerve damage.</td><td>Nutritional yeast (fortified), dairy, eggs, sardines, salmon</td><td class="w">HIGH RISK. Found only in animal foods and fortified products. Get it tested. Supplementing 250 to 500 mcg/day is cheap and reasonable on a vegetarian-leaning diet.</td></tr>
<tr><td><strong>Iron</strong></td><td>18 mg</td><td>Oxygen transport, energy production in the mitochondria. Low ferritin causes fatigue and poor training tolerance long before anemia shows.</td><td>Lentils, tofu, pumpkin seeds, spinach, cocoa, fortified GF grains</td><td class="w">HIGH RISK. Plant (non-heme) iron absorbs at 2 to 20% versus 15 to 35% for heme iron. Celiac impairs absorption further. Pair iron foods with vitamin C; keep coffee and tea away from those meals by an hour. Test ferritin.</td></tr>
<tr><td><strong>Vitamin D</strong></td><td>20 mcg (800 IU)</td><td>Calcium absorption, bone mineralization, immune function, muscle function.</td><td>Egg yolks, fortified milk, salmon, sardines</td><td class="w">HIGH RISK, and it matters more for me than most. CRMO is a bone inflammatory condition. Colorado has high UV but I work in winter and indoors. Test 25-OH-D; 2,000 to 4,000 IU/day is a common and safe corrective dose.</td></tr>
<tr><td>Zinc</td><td>11 mg</td><td>Testosterone synthesis, immune function, wound healing, protein synthesis</td><td>Pumpkin seeds, hemp hearts, oats, dairy, legumes</td><td class="w">Moderate risk. Phytates in legumes and grains reduce absorption. Soaking and sprouting helps.</td></tr>
<tr><td>Calcium</td><td>1,300 mg</td><td>Bone mineralization, muscle contraction, nerve signaling</td><td>Dairy (the dominant source), fortified plant milks, tofu set with calcium sulfate, canned salmon with bones, kale</td><td>Low risk given my dairy intake. Directly relevant to CRMO.</td></tr>
<tr><td>Magnesium</td><td>420 mg</td><td>Over 300 enzyme reactions, ATP production, muscle relaxation, sleep quality</td><td>Pumpkin seeds, cocoa, oats, spinach, almonds, black beans</td><td>Moderate risk. Commonly low in athletes. Glycinate or citrate forms if supplementing; oxide is poorly absorbed.</td></tr>
<tr><td>Potassium</td><td>4,700 mg</td><td>Fluid balance, blood pressure, muscle contraction</td><td>Potato, sweet potato, banana, beans, spinach, yogurt</td><td>Most people fall short. The catalog is potassium-heavy by design.</td></tr>
<tr><td>Sodium</td><td>~2,300 mg guideline</td><td>Fluid balance, nerve conduction, muscle contraction</td><td>Salt, tamari, cheese</td><td>I likely need <em>more</em>, not less, given sweat losses on the job. The standard guideline assumes a sedentary person.</td></tr>
<tr><td>Phosphorus</td><td>1,250 mg</td><td>Bone, ATP, cell membranes</td><td>Dairy, legumes, nuts, whole grains</td><td>Adequacy is near automatic on a high-protein diet.</td></tr>
<tr><td>Selenium</td><td>55 mcg</td><td>Thyroid hormone conversion, antioxidant enzymes</td><td>Brazil nuts (one nut covers a day), eggs, fish</td><td>Do not eat more than 2 Brazil nuts a day. Selenium toxicity is real.</td></tr>
<tr><td>Iodine</td><td>150 mcg</td><td>Thyroid hormone synthesis, which sets metabolic rate</td><td>Iodized salt, dairy, fish</td><td class="w">Moderate risk. Sea salt and kosher salt are usually <em>not</em> iodized. If I avoid fish and use non-iodized salt, dairy is my only real source.</td></tr>
<tr><td>Vitamin A</td><td>900 mcg RAE</td><td>Vision, immune function, skin cell turnover</td><td>Sweet potato, carrot, kale, spinach, eggs, dairy</td><td>Low risk. Relevant to skin quality.</td></tr>
<tr><td>Vitamin C</td><td>90 mg</td><td>Collagen synthesis, antioxidant, dramatically increases non-heme iron absorption</td><td>Bell pepper, strawberries, orange, broccoli, tomato</td><td>Low risk. Use it deliberately alongside iron-rich meals.</td></tr>
<tr><td>Vitamin E</td><td>15 mg</td><td>Membrane antioxidant</td><td>Almonds, sunflower seeds, olive oil, avocado</td><td>Low risk.</td></tr>
<tr><td>Vitamin K</td><td>120 mcg</td><td>Blood clotting, directs calcium into bone rather than soft tissue</td><td>Kale, spinach, broccoli</td><td>Low risk. K2 works alongside vitamin D for bone, which is worth knowing given CRMO.</td></tr>
<tr><td>B1 Thiamin</td><td>1.2 mg</td><td>Carbohydrate metabolism</td><td>Legumes, oats, sunflower seeds</td><td>Note: gluten-free grain products are usually <em>not</em> enriched with B vitamins the way wheat flour is. This is a real and under-discussed gap in long-term GF diets.</td></tr>
<tr><td>B2 Riboflavin</td><td>1.3 mg</td><td>Energy metabolism, works with B6 and folate</td><td>Dairy, eggs, nutritional yeast, almonds</td><td>Low risk with dairy.</td></tr>
<tr><td>B3 Niacin</td><td>16 mg</td><td>NAD production, energy metabolism</td><td>Nutritional yeast, legumes, fish, poultry</td><td>Low risk.</td></tr>
<tr><td>B5 Pantothenic acid</td><td>5 mg</td><td>Coenzyme A, fat and carb metabolism</td><td>Nearly everything</td><td>Very low risk.</td></tr>
<tr><td>B6</td><td>1.7 mg</td><td>Amino acid metabolism, neurotransmitter synthesis</td><td>Potato, banana, chickpeas, nutritional yeast</td><td>Low risk. Do not megadose; chronic high-dose B6 causes peripheral neuropathy.</td></tr>
<tr><td>Biotin</td><td>30 mcg</td><td>Fatty acid synthesis, keratin infrastructure</td><td>Eggs, nuts, seeds, oats</td><td>Very low risk. Biotin hair supplements do nothing unless I am deficient, which is rare.</td></tr>
<tr><td>Folate</td><td>400 mcg</td><td>DNA synthesis, red blood cell formation</td><td>Lentils, spinach, chickpeas, avocado</td><td>Low risk. Again, GF grains are usually not folate-fortified.</td></tr>
<tr><td>Choline</td><td>550 mg</td><td>Cell membranes, acetylcholine, liver fat transport</td><td>Egg yolks (the dominant source), soy, dairy</td><td>Moderate risk if I eat only whites. Two whole eggs cover about half a day.</td></tr>
</table>

<h3 id="omega3">Omega-3</h3>
<p>Three forms matter and they are not interchangeable.</p>
<ul>
<li><strong>ALA</strong> is the plant form, in flax, chia, walnuts and hemp. It is essential, but the body
converts it to the useful long-chain forms at roughly <strong>5 to 8% for EPA and under 1 to 4% for
DHA</strong>. Eating flax is not equivalent to eating fish.</li>
<li><strong>EPA</strong> is the primarily anti-inflammatory form. Given CRMO, this one is specifically
relevant to me.</li>
<li><strong>DHA</strong> is structural, concentrated in brain and retinal membranes.</li>
</ul>
<p>Marine sources are the only direct dietary route: salmon (about 2.0 g EPA+DHA per 100 g),
sardines (about 1.0 g), canned salmon (about 1.5 g), tuna (about 0.27 g). Two servings of fatty
fish per week covers it. If I am not eating fish, <strong>algae oil</strong> is the one supplement
that genuinely substitutes, since it is the original source that fish get theirs from. 500 to
1,000 mg combined EPA+DHA per day is a reasonable target.</p>
"""

TIMING = """
<h2 id="timing">6. Meal timing, fasting, and the two-meal day</h2>

<h3>Pre-workout</h3>
<table>
<tr><th>Time before training</th><th>What to eat</th><th>What to reach for</th></tr>
<tr><td>2 to 3 hours</td><td>A full mixed meal. Fat and fiber are fine at this distance.</td><td>L-02, L-03, L-06, M-02</td></tr>
<tr><td>1 to 2 hours</td><td>Moderate carb, moderate protein, keep fat under 15 g and fiber under 6 g.</td><td>B-04, B-10, S-08, D-01</td></tr>
<tr><td>30 to 60 minutes</td><td>Fast carbs plus easily digested protein. Liquid is easier than solid.</td><td>D-01, D-04, S-02, a banana with whey</td></tr>
<tr><td>Under 30 minutes</td><td>Liquid only, or nothing. Fructose and fat are the two things most likely to cause GI distress at this range.</td><td>D-04, or just water</td></tr>
</table>
<p>If I train fasted first thing, I am not sabotaging myself, but I will do more total work
with something in me. Around 30 g of carbs is enough to make a difference.</p>

<h3>Post-workout</h3>
<p>The "anabolic window" as sold, a 30-minute panic sprint to a shake, is not supported. Elevated
muscle protein synthesis after a training session lasts <strong>24 to 48 hours</strong> in trained
individuals. What actually matters:</p>
<ul>
<li>Total daily protein and calories. This is 90% of it.</li>
<li>Getting a 35 to 45 g protein feeding within a few hours, mostly because it keeps my daily
total on track.</li>
<li>Carbohydrate for glycogen resynthesis. This becomes genuinely time-sensitive only if I am
training hard twice in under 8 hours, which I am not.</li>
<li>Fluid and sodium replacement, which is the most neglected part and the one I will feel.</li>
</ul>
<p>The exception worth knowing: if I trained fasted, protein soon after does matter more, simply
because I have gone longer without amino acids.</p>

<h3>Intermittent fasting and the two-meal day</h3>
<p>Fasting is a meal-timing preference. It has no independent muscle-building advantage when
calories and protein are matched, and the research on that is fairly settled. What it does offer
is simplicity, and for some people better appetite control. What it costs me, in my specific
situation, is real: <strong>compressing 3,150 kcal and 155 g of protein into two meals is difficult,
and I am already under-eating.</strong> A shorter eating window makes under-eating easier, not
harder.</p>
<p>If I want to run two meals, run it deliberately:</p>
<table>
<tr><th>Template</th><th>Structure</th><th>Works for</th></tr>
<tr><td>Two meals</td><td>Meal 1: 1,500 kcal / 75 g P. Meal 2: 1,665 kcal / 80 g P.</td><td>Days I genuinely cannot eat at work. Hard to hit at these numbers.</td></tr>
<tr><td><strong>Two meals + shake</strong></td><td>Shake 700 kcal / 45 g P (D-03 or D-10). Meal 1: 1,200 / 55 g. Meal 2: 1,250 / 55 g.</td><td><strong>The version that actually fits my week.</strong> The shake solves the calorie gap without needing an eating break on site.</td></tr>
<tr><td>Two meals + snack</td><td>Meal 1: 1,300. S-05 or S-14 mid-shift: 450. Meal 2: 1,400.</td><td>No blender access. Protein balls and trail mix travel.</td></tr>
<tr><td>Three or four meals</td><td>4 x 40 g protein spread evenly</td><td>Days off, or once I move out and control my kitchen.</td></tr>
</table>
<p>Meals above 1,200 kcal are marked <span class="tag t-fast">TWO-MEAL-DAY FRIENDLY</span>. On a
two-meal day, build both meals from the L or M sections and add a D-series drink rather than
trying to make a single meal enormous.</p>
"""

GOALS = """
<h2 id="goals">7. Goal guides</h2>

<h3>Lean gain, my current situation</h3>
<p>Surplus of 250 to 350 kcal above maintenance. Faster than that and I gain fat at a ratio that
is not worth it; a natural trainee at my stage builds roughly 1 to 1.5 lb of muscle per month
at best, and there is no calorie surplus that outruns that ceiling. Target
<strong>+0.25 to 0.5 lb per week</strong>, which is 1 to 2 lb per month.</p>
<p>Adding calories without garbage: the cleanest additions are 200 to 300 kcal blocks bolted onto
meals I already eat. One tbsp of olive oil into whatever I cook is +120. Two tbsp of peanut
butter is +190. 60 g of dry oats into a shake is +230. 200 ml of whole milk instead of water in a
shake is +120. Half an avocado is +160. Doing three of those every day is +500 without a single
extra meal.</p>
<p>Expect the first 3 to 5 lb to arrive fast. That is glycogen and the water bound to it, plus
increased gut contents. It is not fat. Given the note in my file about how I see my
midsection, I should decide now that I am going to judge this on the 7-day weight average
and on lift progression, not on how I look in the mirror at 9 p.m. under bad lighting.</p>

<h3>Cutting</h3>
<p>Deficit of 400 to 600 kcal, protein up to 1.1 to 1.25 g/lb, fiber up to 45 to 50 g, and keep
training volume where it is rather than adding cardio to accelerate it. Target 0.5 to 0.75 lb per
week. Below about 8% body fat, sustained, hormonal and mood costs start to outweigh the aesthetic
return, and my file already flags stress and a physical job. Filter for
<span class="tag t-prot">HIGH PROTEIN</span> plus <span class="tag t-fib">HIGH FIBER</span> plus
<span class="tag t-lowcal">LOW CALORIE</span>.</p>

<h3>Recomposition</h3>
<p>Gaining muscle and losing fat simultaneously. It works best in exactly three situations:
untrained beginners, people returning after a layoff, and people who have been under-eating while
training hard. <strong>I am the third case.</strong> That is genuinely good news: raising my
calories toward maintenance while keeping protein at 155 g and training hard is likely to add
muscle and lose fat at the same time for the next few months, which is not available to most
intermediate lifters. Run maintenance calories, high protein, and judge it by lift numbers,
photographs in fixed lighting every 4 weeks, and tape measurements, not by the scale, which will
barely move.</p>

<h3>Training-specific priorities</h3>
<table>
<tr><th>Training focus</th><th>Nutritional priority</th></tr>
<tr><td>Hypertrophy</td><td>Calorie sufficiency first, 155 g protein spread over 4 feedings, carbs at 2.5 to 3.2 g/lb to support volume.</td></tr>
<tr><td>Strength / low rep</td><td>Same protein, slightly less total carbohydrate needed, more attention to hydration and sodium before heavy sessions.</td></tr>
<tr><td>Calisthenics skill work (my planche progression)</td><td>Skill work is neurological, not metabolic. Do it fresh and early in the session. Fueling matters less than being non-fatigued, so train it after a normal meal rather than fasted.</td></tr>
<tr><td>Conditioning / zone 2</td><td>Little acute fueling needed under 60 minutes. Beyond that, 30 to 60 g carbs per hour.</td></tr>
<tr><td>Rest day</td><td>Keep protein identical. Drop calories by 10% or leave them flat. Do not cut carbs; that is when glycogen is being replaced.</td></tr>
</table>

<h3>Aesthetic physique</h3>
<p>Nutrition cannot grow a specific muscle or remove fat from a specific place. Spot reduction is
not real, and where I store and lose fat is genetic and mostly fixed. What nutrition does is
make the training that shapes me possible.</p>
<p>My file lists back, lats, legs and side delts as lagging, and abs and jawline as the visual
priorities. The relevant translation is: <strong>jawline definition is a body fat function below
about 12%, and abs are a body fat function combined with actual abdominal muscle thickness.</strong>
Under-eating gets me low body fat with nothing underneath it, which is the exact position I am
in now. The V-taper that makes I read as taller and more built is built from delts and lats,
and those are the two things that need calories and volume most. Eat to build the frame, then
reveal it later. That order is not negotiable, and doing it in the other order is the single most
common reason lean 20-year-olds spend three years looking identical.</p>
"""

SYSTEM = """
<h2 id="tags">8. Tag definitions and thresholds</h2>
<p>Every tag is assigned by a rule rather than by feel. The thresholds are:</p>
<table>
<tr><th>Tag</th><th>Rule (per serving)</th></tr>
<tr><td><span class="tag t-prot">HIGH PROTEIN</span></td><td>30 g or more</td></tr>
<tr><td><span class="tag t-prot">VERY HIGH PROTEIN</span></td><td>40 g or more</td></tr>
<tr><td><span class="tag t-leu">HIGH LEUCINE</span></td><td>2.5 g or more, the approximate threshold for a maximal MPS response</td></tr>
<tr><td><span class="tag t-leu">LEUCINE PRIORITY</span></td><td>3.0 g or more, genuinely among the strongest in the catalog</td></tr>
<tr><td><span class="tag t-cal">HIGH CALORIE</span></td><td>500 kcal or more</td></tr>
<tr><td><span class="tag t-lowcal">LOW CALORIE</span></td><td>300 kcal or less</td></tr>
<tr><td><span class="tag t-fib">HIGH FIBER</span></td><td>8 g or more</td></tr>
<tr><td><span class="tag t-fat">HIGH HEALTHY FAT</span></td><td>20 g or more, predominantly unsaturated</td></tr>
<tr><td><span class="tag t-carb">HIGH CARB</span></td><td>50 g or more and at least 50% of calories</td></tr>
<tr><td><span class="tag t-carb">LOW CARB</span></td><td>25 g or less</td></tr>
<tr><td><span class="tag t-bal">BALANCED MACRO</span></td><td>Protein 20 to 40%, carbs 30 to 55%, fat 20 to 40% of calories</td></tr>
<tr><td><span class="tag t-mus">MUSCLE-BUILDING PRIORITY</span></td><td>30 g protein and 2.5 g leucine or more together</td></tr>
<tr><td><span class="tag t-rec">POST-WORKOUT FRIENDLY</span></td><td>25 g protein and 40 g carbs or more</td></tr>
<tr><td><span class="tag t-rec">PRE-WORKOUT FRIENDLY</span></td><td>30 g carbs or more, fat under 15 g, fiber under 6 g</td></tr>
<tr><td><span class="tag t-sat">HIGH SATIETY</span></td><td>Computed score of 16 or more (see below)</td></tr>
<tr><td><span class="tag t-quick">QUICK</span></td><td>10 minutes total or less</td></tr>
<tr><td><span class="tag t-fast">TWO-MEAL-DAY FRIENDLY</span></td><td>600 kcal and 35 g protein or more</td></tr>
<tr><td><span class="tag t-micro">HIGH CALCIUM / IRON / MAGNESIUM / POTASSIUM / ZINC</span></td><td>20% or more of the Daily Value</td></tr>
<tr><td><span class="tag t-micro">OMEGA-3 RICH</span></td><td>0.5 g or more EPA+DHA, or 2.5 g or more ALA</td></tr>
<tr><td><span class="tag t-budget">BUDGET FRIENDLY / MEAL PREP / FREEZER FRIENDLY / PORTABLE</span></td><td>Assigned by hand, based on cost per serving and how the food actually holds up</td></tr>
</table>

<h3>Satiety score</h3>
<p>Satiety is not measurable to laboratory precision and varies between people and between days.
This is a heuristic, and it is documented so I know exactly what it means:</p>
<p><code>score = (0.30 x protein g) + (0.60 x fiber g) + (0.01 x total food grams) - 6 if liquid</code></p>
<p>16 or above is HIGH, 9 to 15.9 is MEDIUM, under 9 is LOWER. Protein and fiber are weighted
heaviest because they have the strongest evidence behind them; food volume matters because
stomach stretch is a real signal; liquid calories carry a penalty because they empty the stomach
fast and are poorly compensated for at the next meal. No claim is made that any meal keeps me
full for a specific number of hours.</p>

<h2 id="build">9. Build my own meal</h2>
<p>When nothing in the catalog appeals, use the formula:</p>
<p class="formula">PROTEIN ANCHOR (30 to 45 g) + CARB BASE + VEGETABLE OR FRUIT + FAT SOURCE + FLAVOR</p>
<table>
<tr><th>Slot</th><th>Portion</th><th>Options</th></tr>
<tr><td>Protein anchor</td><td>Enough for 30 to 45 g</td><td>200 g Greek yogurt (21 g), 200 g cottage cheese (22 g), 3 eggs (38 g with 2 whites added), 200 g tofu (35 g), 150 g tempeh (30 g), 1.5 scoops whey (38 g), 85 g dry chickpea pasta (18 g, needs help)</td></tr>
<tr><td>Carb base</td><td>150 to 300 g cooked</td><td>Rice, potato, sweet potato, quinoa, GF pasta, oats, corn tortillas</td></tr>
<tr><td>Vegetable or fruit</td><td>100 to 200 g</td><td>Anything. Two colors is a decent heuristic for micronutrient spread.</td></tr>
<tr><td>Fat</td><td>10 to 25 g</td><td>Olive oil, avocado, nuts, seeds, cheese, tahini</td></tr>
<tr><td>Flavor</td><td>Free</td><td>Salsa, tamari, lemon, garlic, spices, hot sauce, vinegar, nutritional yeast</td></tr>
</table>
<p>Adjusting it: <strong>more calories</strong>, add oil, nut butter, or a larger carb base.
<strong>Fewer calories</strong>, cut the fat slot first, it is the densest. <strong>More protein</strong>,
add a second anchor rather than doubling the first. <strong>More fiber</strong>, swap the carb base
for beans or lentils. <strong>Easier digestion pre-training</strong>, drop the fat and fiber, keep
protein and carbs.</p>

<h2 id="decide">10. What should I eat right now</h2>
<table class="decide">
<tr><th>Situation</th><th>Filter for</th></tr>
<tr><td>I need to gain and I am behind on calories</td><td>HIGH CALORIE + HIGH PROTEIN. Start with D-03, D-10, L-08, B-07.</td></tr>
<tr><td>I need protein but not many calories</td><td>HIGH PROTEIN + LOW CALORIE. S-15, S-03, D-04, M-05, S-07.</td></tr>
<tr><td>I just trained</td><td>POST-WORKOUT FRIENDLY. D-01, L-14, M-08, L-03.</td></tr>
<tr><td>I train in an hour</td><td>PRE-WORKOUT FRIENDLY. B-04, S-08, D-01.</td></tr>
<tr><td>I have 10 minutes</td><td>QUICK. B-02, B-11, L-04, L-14, S-01, all D-series.</td></tr>
<tr><td>I do not want to cook at all</td><td>B-02, B-04, B-08, S-02, S-03, S-09, S-14, M-03, M-09, all D-series.</td></tr>
<tr><td>I am very hungry</td><td>HIGH SATIETY. L-07, L-13, L-12, S-10, D-09.</td></tr>
<tr><td>I need fiber</td><td>HIGH FIBER. L-08, L-12, S-04, L-02, B-08.</td></tr>
<tr><td>I need healthy fats</td><td>S-14, B-07, L-09, M-01, D-03.</td></tr>
<tr><td>I need a big leucine hit</td><td>LEUCINE PRIORITY. D-02, D-12, B-05, L-13, M-02.</td></tr>
<tr><td>I am doing two meals today</td><td>TWO-MEAL-DAY FRIENDLY, plus one D-series shake.</td></tr>
<tr><td>I want something sweet without wrecking the day</td><td>S-07, S-01, S-12, D-02, D-07.</td></tr>
<tr><td>I have no money until Friday</td><td>BUDGET FRIENDLY. L-07, L-02, L-12, S-11, S-04, D-12.</td></tr>
</table>
"""

PRACTICAL = """
<h2 id="grocery">11. Groceries</h2>

<h3>Always keep these in the house</h3>
<p>If these eleven things are stocked, I can build a compliant meal at any time without a plan:
eggs, nonfat Greek yogurt or cottage cheese, certified GF rolled oats, GF-certified whey, canned
black beans and chickpeas, rice, potatoes, frozen mixed berries, frozen vegetables, olive oil,
peanut butter.</p>

<h3>Core weekly list, one person, roughly a week of the catalog</h3>
<table>
<tr><th>Category</th><th>Items and quantities</th></tr>
<tr><td>Dairy and eggs</td><td>2 dozen eggs; 1.5 kg nonfat Greek yogurt; 900 g cottage cheese; 4 L milk; 200 g shredded cheddar; 200 g part-skim mozzarella; 100 g feta or parmesan</td></tr>
<tr><td>Plant protein</td><td>2 blocks extra-firm tofu; 1 pack tempeh; 400 g frozen shelled edamame; 3 cans black beans; 2 cans chickpeas; 500 g dry lentils</td></tr>
<tr><td>Powders</td><td>GF-certified whey isolate (2 kg lasts a month); powdered peanut butter; nutritional yeast</td></tr>
<tr><td>Grains and starch (all GF)</td><td>1 kg certified GF rolled oats; 1 kg rice; 2 kg potatoes; 1 kg sweet potatoes; 500 g chickpea or lentil pasta; corn tortillas; GF bread or wraps</td></tr>
<tr><td>Produce</td><td>Spinach or kale (large bag); 4 bell peppers; onions; garlic; carrots; cucumber; cherry tomatoes; broccoli; 6 bananas; 3 apples; lemons</td></tr>
<tr><td>Frozen</td><td>1 kg mixed berries; 1 kg mixed vegetables; peas; mango</td></tr>
<tr><td>Fats</td><td>Olive oil; natural peanut butter; almonds; walnuts; pumpkin seeds; chia or ground flax; 2 avocados</td></tr>
<tr><td>Pantry and flavor</td><td>Marinara; salsa; GF tamari; sriracha; honey; unsweetened cocoa; cinnamon; cumin; chili powder; smoked paprika; iodized salt; baking powder</td></tr>
<tr><td>Optional, separate</td><td>1 kg chicken breast; 2 salmon fillets; 4 cans tuna or salmon; 1 pack ground turkey; sardines</td></tr>
</table>

<h3>Budget list</h3>
<p>Eggs, cottage cheese, milk, oats, rice, dried lentils, dried or canned beans, potatoes, frozen
vegetables, frozen berries, bananas, peanut butter, tofu, whey bought in bulk. That list alone can
run the entire handbook's core and hit 155 g of protein a day.</p>

<h3>Protein per dollar</h3>
<p>I do not have current Colorado prices, so calculate it myself with:
<code>cost per 25 g protein = (price of package / grams of protein in package) x 25</code>.
Run it once and write the numbers in. The ordering rarely changes: <strong>eggs, milk, cottage
cheese, dried lentils and beans, tofu, and bulk whey are consistently at the top; protein bars,
ready-made shakes, and any product marketed as a snack are consistently at the bottom</strong>,
usually by a factor of three or more. My file lists protein bars as a work-lunch staple. They
are the single most expensive protein I am buying.</p>

<h2 id="prep">12. Meal prep</h2>
<h3>The one-hour version</h3>
<ol>
<li>Rice or quinoa on, large batch (0 active minutes after starting it).</li>
<li>Oven to 425F: sheet pan of sweet potato and broccoli, second pan of tofu (25 min, unattended).</li>
<li>While those run: boil a dozen eggs, chop vegetables for the week into one container.</li>
<li>Assemble 4 jars of overnight oats (B-01) and one batch of protein balls (S-05).</li>
<li>Portion everything into containers.</li>
</ol>
<p>That yields roughly 5 assembled lunches, 4 breakfasts, a week of snacks and a stocked fridge.</p>

<h3>The two-hour version</h3>
<p>Add: a double batch of soup (L-12) portioned and frozen, 5 breakfast burritos (B-09) wrapped in
foil and frozen, a double batch of waffles (B-13) frozen flat, and a large batch of curry (L-08).
That is 3 weeks of frozen depth.</p>

<h3>The minimal version, for a week I am drowning</h3>
<p>Boil a dozen eggs. Buy pre-cooked rice pouches, bagged salad, and canned beans. Keep whey and
milk on hand. Nothing else. It is not optimal and it will keep me at target.</p>

<h3>Avoiding meal-prep burnout</h3>
<p>Do not prep 5 identical meals. Prep <strong>components</strong>: one protein, one starch, one
roasted vegetable, two sauces. Rice and tofu with tamari is a different meal from rice and tofu
with salsa and avocado, and the second takes ten seconds longer.</p>

<h2 id="safety">13. Food safety</h2>
<ul>
<li><strong>Cooked rice</strong> is the one people get wrong. Bacillus cereus spores survive cooking and
produce heat-stable toxin at room temperature. Cool it fast, refrigerate within one hour, use
within 3 days, reheat until steaming throughout.</li>
<li><strong>Cooked food generally:</strong> the 40 to 140F range is where bacteria multiply fastest. Do not
leave a lunch container in a hot truck.</li>
<li><strong>Eggs:</strong> cook to firm whites. Refrigerated in shell, 3 to 5 weeks; hard-boiled in shell,
1 week.</li>
<li><strong>Tofu:</strong> once opened, submerge in fresh water, change daily, use within 4 days.</li>
<li><strong>Fish:</strong> cook to 145F. Thaw in the refrigerator, never on the counter.</li>
<li><strong>Poultry:</strong> 165F, or 160F with a rest, measured at the thickest part.</li>
<li><strong>Cross-contamination, celiac-specific:</strong> a dedicated toaster, a separate colander, separate
condiment jars, and separate butter and peanut butter. Shared toasters and double-dipped knives
are the most common real-world exposure routes, far more than the food itself.</li>
</ul>

<h2 id="relationship">14. Relationship with food</h2>
<p>Macros are accounting tools. They are not a moral scoring system, and a meal that misses them
does not undo a week. Consistency across a month is what produces results; no single day matters
in either direction.</p>
<p>Two things in my file are worth naming here directly, because a nutrition handbook that
ignores them would be dishonest. The first is that I described deliberately eating as little as
possible to keep my abs visible. The second is that I flagged possible body dysmorphia around
my midsection. Those two things reinforce each other, and together they are the actual limiting
factor on everything I am trying to build, more than programming, more than supplements.</p>
<p>The practical guard rails: judge progress on <strong>lift numbers, the 7-day weight average, and
photos taken every 4 weeks under identical lighting</strong>. Do not judge it in the mirror at
night, and do not judge it on a day I am stressed. If eating to my actual target starts
producing real distress rather than just discomfort, that is worth talking to someone about, and
it is not a failure of discipline. Tracking is a tool I should be able to put down. If me
cannot put it down, that is information.</p>
"""

TRACKING = """
<h2 id="tracking">15. Daily target page</h2>
<p class="printnote">Print this page. One per day, or one per week with seven columns.</p>
<table class="blank">
<tr><td>Date</td><td class="fill"></td><td>Bodyweight</td><td class="fill"></td></tr>
<tr><td>Goal today</td><td class="fill">gain / maintain / cut</td><td>Training</td><td class="fill">upper / lower / skill / rest</td></tr>
<tr><td>Calorie target</td><td class="fill"></td><td>Actual</td><td class="fill"></td></tr>
<tr><td>Protein target</td><td class="fill"></td><td>Actual</td><td class="fill"></td></tr>
<tr><td>Carb target</td><td class="fill"></td><td>Actual</td><td class="fill"></td></tr>
<tr><td>Fat target</td><td class="fill"></td><td>Actual</td><td class="fill"></td></tr>
<tr><td>Fiber target</td><td class="fill"></td><td>Actual</td><td class="fill"></td></tr>
<tr><td>Water</td><td class="fill"></td><td>Steps</td><td class="fill"></td></tr>
<tr><td>Sleep hours</td><td class="fill"></td><td>Sleep quality 1 to 5</td><td class="fill"></td></tr>
<tr><td>Hunger 1 to 5</td><td class="fill"></td><td>Energy 1 to 5</td><td class="fill"></td></tr>
<tr><td>Digestion 1 to 5</td><td class="fill"></td><td>CRMO pain 1 to 5</td><td class="fill"></td></tr>
<tr><td>Notes</td><td class="fill" colspan="3"></td></tr>
</table>
<p><strong>Formula reminders:</strong> protein = bodyweight lb x 1.05. Fat = bodyweight lb x 0.6.
Carbs = (calories - protein x 4 - fat x 9) / 4. Fiber = calories / 1000 x 14.
Water = 35 ml x kg + 750 ml per training hour.</p>

<h2 id="weekly">16. Weekly tracking sheet</h2>
<p class="printnote">Print one per week. The weekly average column is the only number that means anything.</p>
<table class="blank">
<tr><th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th><th>AVG</th></tr>
<tr><td>Bodyweight</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
<tr><td>Calories</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
<tr><td>Protein</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
<tr><td>Fiber</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
<tr><td>Sleep</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
<tr><td>Energy 1-5</td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td><td class="fill"></td></tr>
</table>
<p><strong>Monthly, not weekly:</strong> waist at navel, chest, arms, thighs, calves, shoulders at the
widest point. Photos front, back, side, same spot, same light, same time of day, same state
(fasted, morning). Best three lifts and best planche progression hold.</p>
<p>Why multiple metrics: bodyweight alone cannot distinguish muscle from water from fat.
Weight plus tape plus lift numbers plus photos can. If weight is up, waist is flat, and lifts are
climbing, the gain is going where I want it regardless of what the mirror tells me on a given
evening.</p>

<h2 id="supps">17. Supplements</h2>
<p>Sorted honestly. Food first; nothing here substitutes for hitting 3,150 kcal.</p>
<table>
<tr><th>Supplement</th><th>Verdict</th><th>Dose and notes</th></tr>
<tr><td>Creatine monohydrate</td><td><strong>Worth it.</strong> The most well-supported ergogenic aid that is legal and over the counter.</td><td>5 g/day, every day, timing irrelevant. No loading needed. Expect 2 to 4 lb of intracellular water weight in the first weeks; that is the mechanism working, not fat. My file says I use it inconsistently. Consistency is the entire point.</td></tr>
<tr><td>Whey or plant protein</td><td><strong>Worth it</strong> as a convenience tool, not a magic powder.</td><td>Whatever closes the gap between food protein and 155 g. Must be GF-certified.</td></tr>
<tr><td>Vitamin D3</td><td><strong>Worth it, and test first.</strong> Directly relevant given CRMO and bone health.</td><td>2,000 to 4,000 IU/day with a fat-containing meal. Pair with K2 (100 to 200 mcg) which directs calcium into bone.</td></tr>
<tr><td>Omega-3 (fish or algae oil)</td><td><strong>Worth it</strong> if I am not eating fatty fish twice a week.</td><td>500 to 1,000 mg combined EPA+DHA. Algae oil if I avoid fish entirely.</td></tr>
<tr><td>Vitamin B12</td><td><strong>Worth it</strong> on a vegetarian-leaning diet.</td><td>250 to 500 mcg/day, or 2,000 mcg weekly. Cheap, no toxicity concern.</td></tr>
<tr><td>Magnesium glycinate</td><td>Situational.</td><td>200 to 400 mg in the evening. Helps if intake is low or sleep is poor. Oxide form is poorly absorbed and mostly a laxative.</td></tr>
<tr><td>Caffeine</td><td>Worth it, used deliberately.</td><td>3 to 6 mg/kg pre-training, so 200 to 400 mg for me. Not within 8 hours of sleep; it has a 5 to 6 hour half-life and cuts deep sleep even when I fall asleep fine. I currently have almost no tolerance, so start at 100 mg.</td></tr>
<tr><td>Turkesterone / ecdysteroids (my Turk Plex)</td><td><strong>Not worth it.</strong></td><td>Human evidence is essentially absent. The one frequently cited trial is not convincing, and third-party testing has repeatedly found products containing little or none of the labeled compound. Stop buying it.</td></tr>
<tr><td>Nitric oxide / pump products (my G O2 Max)</td><td>Overrated.</td><td>Citrulline malate at 6 to 8 g has modest evidence for training volume. Most pump blends underdose it. Buy bulk citrulline if I want the effect.</td></tr>
<tr><td>Pre-workout blends (my Alpha Lion)</td><td>Mostly caffeine plus filler.</td><td>Check the label for actual caffeine content so I am not stacking it unknowingly. Proprietary blends that do not disclose per-ingredient doses are not worth paying for.</td></tr>
<tr><td>BCAAs</td><td><strong>Skip.</strong></td><td>Pointless if total protein is adequate. I get all nine essential amino acids from food; three of them in isolation does nothing extra.</td></tr>
<tr><td>Unidentified "supplement from the coach"</td><td>Unknown.</td><td>Do not take anything I cannot name and look up. Photograph the label and we will go through it.</td></tr>
</table>
<p>Bloodwork worth requesting given my history: full CBC, ferritin, 25-OH vitamin D, B12, a
full thyroid panel, lipids, and total plus free testosterone. Ferritin and B12 especially, given
vegetarian intake plus celiac malabsorption. A doctor has to order these; that is a genuine
limitation, not a deflection.</p>

<h2 id="refs">18. References</h2>
<p><strong>Nutrition data:</strong> USDA FoodData Central (SR Legacy and Foundation Foods) for all
macronutrient, fiber, mineral and amino acid values.</p>
<p><strong>Protein and amino acids:</strong> Morton et al. 2018 systematic review and meta-analysis on
protein supplementation and resistance training (the 1.6 g/kg plateau finding); Schoenfeld and
Aragon 2018 on per-meal protein dose; Phillips and Van Loon on protein requirements for athletes;
Witard et al. on dose-response of muscle protein synthesis.</p>
<p><strong>Sports nutrition position stands:</strong> International Society of Sports Nutrition position
stands on protein, creatine, and nutrient timing; ACSM/AND/DC joint position stand on nutrition
and athletic performance.</p>
<p><strong>Programming and evidence interpretation:</strong> Schoenfeld on hypertrophy; Helms on natural
bodybuilding nutrition and the Muscle and Strength Pyramid; Israetel on volume landmarks;
Nuckols and Stronger by Science on evidence quality; Lyle McDonald on body composition and
energy partitioning; Norton and Henselmans on applied nutrition.</p>
<p><strong>Sleep and recovery:</strong> Walker, Why We Sleep, on sleep architecture and caffeine
half-life effects.</p>
<p><strong>Food safety:</strong> USDA FSIS and FDA guidance on cooking temperatures and cooling times.</p>
<p><strong>Recipes:</strong> all recipes here are original constructions built from the
ingredient database, not reproductions of published recipes.</p>
"""

HOWTO = """
<h2 id="howto">How to use this handbook</h2>
<p>This is not a seven-day meal plan. It is a decision tool. The intended use is:</p>
<ol>
<li>Check <a href="#targets">my numbers</a> once, and again whenever my bodyweight moves 5 lb.</li>
<li>During the day, know roughly what I have already eaten.</li>
<li>Open the relevant index, scan the calorie, protein, carb, fat, fiber and leucine columns,
and pick something that fits the gap.</li>
<li>If nothing appeals, use <a href="#build">Build my own meal</a>.</li>
<li>If I am pressed, go straight to <a href="#decide">What should I eat right now</a>.</li>
</ol>
<p><strong>Structure:</strong> sections 1 through 18 are the reference and education material.
The indexes are compact and designed to print in grayscale. The full recipe library sits after the
indexes; every meal name in an index links directly to its recipe, and every recipe links back.</p>
<p><strong>Every recipe here is gluten-free.</strong> The main catalog is vegetarian.
The meat and fish section is separate, optional, and SDA-compatible: no pork, no shellfish, no
biblically unclean animals. Nothing in the main catalog depends on it.</p>
"""
