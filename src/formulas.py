# -*- coding: utf-8 -*-
"""The calculation chapter. Every formula, every activity level, every goal type."""

CALC = """
<h2 id="calc">The calculation engine</h2>

<p>Everything downstream of this page is arithmetic. My body weight changes, my job changes,
my goal changes, and the numbers change with them. This chapter is written so I never have to
come back and ask me what to do when something moves. Work through it once and I own it.</p>

<p>The order is always the same. Estimate resting metabolic rate. Multiply by an activity factor to
get maintenance. Adjust for the goal. Set protein and fat from body weight. Give carbohydrate
whatever calories are left. Then ignore all of it and follow my weight trend for three weeks,
because the calculator is a starting guess and the scale is the truth.</p>

<h3>Step 1: resting metabolic rate</h3>

<p>Six equations, ranked. They disagree by 100 to 200 calories, which sounds like a lot and does not
matter, because the activity multiplier introduces far more error than the choice of equation does.</p>

<table>
<tr><th>Equation</th><th>Formula (male)</th><th>My value</th><th>When to use it</th></tr>
<tr><td><b>Katch-McArdle</b></td><td>370 + (21.6 x LBM_kg)</td><td>1,595</td>
<td>Best equation available, but only if my body fat number is real. Mine comes from a BIA scale,
so it is not. Becomes the right choice the day I get a DEXA.</td></tr>
<tr><td><b>Cunningham</b></td><td>500 + (22 x LBM_kg)</td><td>1,747</td>
<td>Same input as Katch-McArdle, runs higher. Built on trained athletes, so it tends to fit lifters
better than the general-population equations.</td></tr>
<tr><td><b>Mifflin-St Jeor</b></td><td>(10 x kg) + (6.25 x cm) - (5 x age) + 5</td><td>1,636</td>
<td>The default. Most accurate general equation when I do not have reliable body fat data.
This is the one the handbook uses.</td></tr>
<tr><td><b>Harris-Benedict (revised)</b></td><td>88.36 + (13.4 x kg) + (4.8 x cm) - (5.68 x age)</td><td>1,678</td>
<td>Older, runs 5 to 10% high on lean people. Fine as a cross-check.</td></tr>
<tr><td><b>Owen</b></td><td>879 + (10.2 x kg)</td><td>1,560</td>
<td>Crude but hard to get wrong. Useful sanity check: if another equation is more than 200 off this,
recheck my inputs.</td></tr>
<tr><td><b>Ten Haaf</b></td><td>(11.936 x kg) + (587.728 x m) - (8.129 x age) + 191.027</td><td>1,673</td>
<td>Validated specifically on recreational athletes. Good fit for my population.</td></tr>
</table>

<p class="small">Inputs used: 68.0 kg, 172.7 cm, 20 years, 56.7 kg lean mass. The spread across all six
is 1,560 to 1,747, a range of 187 calories. Take the median, roughly <b>1,665</b>, and move on.</p>

<h3>Step 2: activity factor</h3>

<p>This is where nearly all the error lives. Most people overestimate by one full step. The honest
test is not how hard my workout felt, it is how many hours a day I spend on my feet.</p>

<table>
<tr><th>Factor</th><th>Level</th><th>What it actually looks like</th><th>Steps/day</th><th>My TDEE</th></tr>
<tr><td>1.15</td><td>Bedbound</td><td>Illness, injury, immobilised</td><td>Under 1,000</td><td>1,900</td></tr>
<tr><td>1.20</td><td>Fully sedentary</td><td>Desk job, no training, drives everywhere</td><td>2,000-3,000</td><td>1,980</td></tr>
<tr><td>1.30</td><td>Sedentary plus training</td><td>Desk job, lifts 3x/week, otherwise still</td><td>3,000-5,000</td><td>2,145</td></tr>
<tr><td>1.40</td><td>Lightly active</td><td>Desk job, lifts 4-5x/week, walks a bit</td><td>5,000-7,000</td><td>2,310</td></tr>
<tr><td>1.50</td><td>Moderately active</td><td>Some standing, lifts 4-5x/week</td><td>7,000-9,000</td><td>2,475</td></tr>
<tr><td>1.60</td><td>Active</td><td>Standing job or retail, trains 4-5x/week</td><td>9,000-11,000</td><td>2,640</td></tr>
<tr><td>1.70</td><td>Very active</td><td>Light trade work, trains near daily</td><td>11,000-13,000</td><td>2,805</td></tr>
<tr class="hl"><td><b>1.55</b></td><td><b>Physically demanding job plus daily training</b></td>
<td><b>Laser engraving work, ladders, material handling, plus training almost every day. This is me.</b></td>
<td><b>12,000-15,000</b></td><td><b>2,580</b></td></tr>
<tr><td>1.85</td><td>Heavy labour plus training</td><td>Framing, roofing, concrete, plus daily training</td><td>15,000-18,000</td><td>3,050</td></tr>
<tr><td>1.95</td><td>Very heavy labour or two-a-days</td><td>Long physical shifts plus a serious training block</td><td>18,000-22,000</td><td>3,220</td></tr>
<tr><td>2.10</td><td>Athlete in a training camp</td><td>Multiple daily sessions, professional context</td><td>22,000+</td><td>3,465</td></tr>
<tr><td>2.30-2.60</td><td>Extreme endurance</td><td>Tour-style cycling, ultra running, expedition work</td><td>Not measured in steps</td><td>3,795-4,290</td></tr>
</table>

<p><b>Seasonal correction.</b> My factor is not one number all year. A week of overtime on a
commercial job pushes me to 1.85. A week of mostly truck and paperwork drops me to 1.60. A week
off with a CRMO flare drops me to 1.35. Move the factor when the week genuinely changes, not
because one session felt hard.</p>

<p><b>The alternative method, if I want more precision.</b> Instead of multiplying, add:
TDEE = RMR + TEF + NEAT + EAT. Thermic effect of food is roughly 10% of intake, so about 310
calories at 2,800. NEAT, all non-exercise movement, is 0.04 kcal per step per kg, so 14,000 steps at
68.0 kg is roughly 375 calories. Training is roughly 5 to 8 kcal per minute of resistance work, so
75 minutes is about 450. That gives 1,665 + 310 + 375 + 450 = <b>2,785</b>, which lands within 4% of
the multiplier method. Two independent approaches agreeing is the best confidence I can get
without a metabolic ward.</p>

<h3>Step 3: goal adjustment</h3>

<p>Seventeen goal types, because "bulk or cut" is not enough resolution to run a real year.</p>

<table>
<tr><th>Goal</th><th>Adjustment</th><th>My calories</th><th>Expected weekly change</th><th>Use it when</th></tr>
<tr><td>Aggressive cut</td><td>TDEE x 0.70</td><td>2,020</td><td>-1.5 to 2.0 lb</td>
<td>Short term only, 4 weeks maximum. Muscle loss risk is real for a natural lifter near his limit.</td></tr>
<tr><td>Standard cut</td><td>TDEE x 0.78</td><td>2,255</td><td>-1.0 to 1.3 lb</td><td>The default fat loss setting.</td></tr>
<tr><td>Conservative cut</td><td>TDEE x 0.85</td><td>2,455</td><td>-0.6 to 0.8 lb</td>
<td>When I want to keep training quality and strength. Slower, better retention.</td></tr>
<tr><td>Mini cut</td><td>TDEE x 0.75</td><td>2,170</td><td>-1.2 to 1.6 lb</td>
<td>3 to 4 weeks mid-gaining phase to strip accumulated fat, then straight back to surplus.</td></tr>
<tr><td>Diet break</td><td>TDEE x 1.00</td><td>2,580</td><td>Flat</td>
<td>1 to 2 weeks at maintenance every 8 to 12 weeks of dieting. Restores leptin, thyroid and sanity.</td></tr>
<tr><td>Refeed day</td><td>TDEE x 1.15, carbs only</td><td>3,325</td><td>+2 to 4 lb water, temporary</td>
<td>One day inside a cut. Do not interpret the scale afterward.</td></tr>
<tr><td>Maintenance</td><td>TDEE x 1.00</td><td>2,580</td><td>Flat</td><td>Holding, high stress periods, life chaos.</td></tr>
<tr><td>Maingaining</td><td>TDEE x 1.02</td><td>2,950</td><td>+0.1 lb</td>
<td>Very slow gain that keeps me visibly lean year-round. Suits my abs priority.</td></tr>
<tr class="hl"><td><b>Underfed recomp</b></td><td><b>TDEE x 1.00 to 1.05</b></td><td><b>2,580-3,035</b></td>
<td><b>Flat, with strength climbing</b></td>
<td><b>Where I am right now. Coming off chronic underfeeding, I get muscle gain and fat loss
simultaneously for roughly the first three to four months. Rare window. Do not waste it.</b></td></tr>
<tr><td>Conservative lean gain</td><td>TDEE x 1.06</td><td>3,065</td><td>+0.2 to 0.3 lb</td>
<td>Minimum fat gain. Slowest muscle accrual.</td></tr>
<tr class="hl"><td><b>Standard lean gain</b></td><td><b>TDEE x 1.08 to 1.10</b></td><td><b>2,800</b></td>
<td><b>+0.3 to 0.5 lb</b></td><td><b>The handbook default. Best growth-to-fat ratio at my training age.</b></td></tr>
<tr><td>Moderate bulk</td><td>TDEE x 1.15</td><td>3,325</td><td>+0.7 to 0.9 lb</td>
<td>Faster, more fat. Reasonable in a winter block if I am willing to mini cut afterward.</td></tr>
<tr><td>Aggressive bulk</td><td>TDEE x 1.20+</td><td>3,470+</td><td>+1.0 lb or more</td>
<td>Mostly fat past a certain point. Rarely the right call and not the right call for me.</td></tr>
<tr><td>Reverse diet</td><td>+3 to 5% per week</td><td>Ramping</td><td>Flat to +0.2 lb</td>
<td>Coming out of a deficit, or out of chronic underfeeding. Rebuilds metabolic rate with minimal fat.</td></tr>
<tr><td>Performance block</td><td>TDEE x 1.05, carbs high</td><td>3,035</td><td>Flat to +0.2 lb</td>
<td>Skill work, planche progression, when the priority is session quality over composition.</td></tr>
<tr><td>Deload or flare week</td><td>TDEE x 0.92</td><td>2,660</td><td>Flat</td>
<td>CRMO flare or programmed deload. Activity drops, so calories drop with it. Hold protein.</td></tr>
<tr><td>Injury or illness</td><td>TDEE x 0.95, protein x 1.2</td><td>2,745, 190 g protein</td><td>Flat</td>
<td>Protein requirement rises during tissue repair even as energy needs fall.</td></tr>
</table>

<div class="callout"><h4>The ramp, since I am starting from underfed</h4>
<p>I do not jump from where I am to 2,800. Add 250 to 300 per week from wherever I honestly
are now. If I am at 1,700, that is week 1 at 1,975, week 2 at 2,250, week 3 at 2,525, week 4 at
2,800, week 5 at 3,050, week 6 at 2,800. Six weeks. Hold protein at 160 g from day one, that part
does not ramp. This is formally a reverse diet and it is the correct protocol for restoring
metabolic rate after a long period of restriction.</p></div>

<h3>Step 4: protein</h3>

<table>
<tr><th>Situation</th><th>Per lb bodyweight</th><th>Per kg</th><th>My grams</th><th>Reasoning</th></tr>
<tr><td>Sedentary minimum</td><td>0.36</td><td>0.8</td><td>53</td><td>The RDA. Prevents deficiency. Irrelevant to me.</td></tr>
<tr><td>Recreational lifter</td><td>0.7</td><td>1.6</td><td>105</td><td>Morton meta-analysis plateau for a mixed-protein diet.</td></tr>
<tr><td>Serious lifter, maintenance</td><td>0.8-1.0</td><td>1.8-2.2</td><td>120-150</td><td>Standard recommendation.</td></tr>
<tr class="hl"><td><b>Plant-heavy diet, lean gain</b></td><td><b>1.05-1.2</b></td><td><b>2.3-2.6</b></td>
<td><b>155-175</b></td><td><b>My setting. Raised because dairy and plant proteins have lower
digestibility and leucine density than a meat-based diet. This is a real correction, not padding.</b></td></tr>
<tr><td>In a deficit</td><td>1.1-1.4</td><td>2.4-3.1</td><td>160-205</td>
<td>Protein need rises as calories fall. Higher again the leaner I get.</td></tr>
<tr><td>Aggressive cut, very lean</td><td>1.4-1.5</td><td>3.1-3.3</td><td>205-220</td>
<td>Ceiling of useful intake. Below 10% body fat in a deficit.</td></tr>
<tr><td>Injury or illness</td><td>1.2-1.4</td><td>2.6-3.1</td><td>175-205</td><td>Tissue repair demand.</td></tr>
<tr><td>Diminishing returns above</td><td>1.5</td><td>3.3</td><td>220</td>
<td>Past here, extra protein is oxidised or stored. Spend the calories on carbs instead.</td></tr>
</table>

<p><b>Per meal.</b> 0.4 to 0.55 g per kg per feeding, so <b>27 to 37 g minimum</b> per sitting, with
40 to 55 g being my practical target across three or four feedings. Each should carry at least
2.5 g leucine.</p>

<p><b>Digestibility-adjusted protein.</b> If I want to be precise about a plant-heavy day, multiply
each source by its DIAAS score before totalling: whey 1.10, milk protein 1.18, egg 1.13, chicken
1.08, soy protein isolate 0.90, tofu 0.87, oats 0.54, peas 0.62, rice 0.59, wheat 0.45. A day
reading 160 g on paper from a mixed plant and dairy diet is realistically 135 to 145 g usable. That
gap is exactly why my target is set where it is.</p>

<h3>Step 5: fat</h3>

<table>
<tr><th>Setting</th><th>Formula</th><th>My grams</th><th>Notes</th></tr>
<tr><td>Absolute floor</td><td>0.3 g/lb</td><td>44</td><td>Below this, testosterone and fat-soluble vitamin absorption suffer.</td></tr>
<tr><td>Cutting</td><td>0.35-0.4 g/lb</td><td>51-59</td><td>Keeps hormones intact while leaving room for carbs.</td></tr>
<tr><td>Maintenance</td><td>0.4-0.5 g/lb</td><td>59-74</td><td>Comfortable middle.</td></tr>
<tr class="hl"><td><b>Lean gain</b></td><td><b>25% of calories</b></td><td><b>85</b></td>
<td><b>The handbook default. Also the easiest lever for adding calories without volume.</b></td></tr>
<tr><td>High fat preference</td><td>35% of calories</td><td>120</td><td>Fine if I prefer it. No metabolic advantage.</td></tr>
<tr><td>Omega-3 target</td><td>EPA+DHA</td><td>1-2 g</td><td>Separate from total fat. Relevant to CRMO.</td></tr>
<tr><td>Saturated fat ceiling</td><td>Under 10% of calories</td><td>Under 34 g</td><td>Cardiovascular, not physique.</td></tr>
</table>

<h3>Step 6: carbohydrate, which takes the remainder</h3>

<p class="formula">Carbs = (target calories - (protein g x 4) - (fat g x 9)) / 4</p>
<p class="small">At 2,800 with 160 g protein and 85 g fat: (2,800 - 640 - 765) / 4 = <b>365 g</b>.</p>

<table>
<tr><th>Context</th><th>Per lb</th><th>My grams</th><th>Why</th></tr>
<tr><td>Very low carb</td><td>0.5</td><td>74</td><td>No advantage for me. Kills training quality and glycogen fullness.</td></tr>
<tr><td>Cutting</td><td>1.0-1.5</td><td>147-220</td><td>Whatever is left after protein and fat floors.</td></tr>
<tr><td>Maintenance</td><td>2.0-2.5</td><td>295-370</td><td>Comfortable.</td></tr>
<tr class="hl"><td><b>Lean gain</b></td><td><b>2.5-3.0</b></td><td><b>370-440</b></td>
<td><b>My setting. Also the fastest visible change: full glycogen makes I look considerably
fuller within two weeks.</b></td></tr>
<tr><td>High volume training day</td><td>3.0-3.5</td><td>440-515</td><td>Long sessions, heavy skill work.</td></tr>
<tr><td>Refeed day</td><td>4.0-4.5</td><td>590-660</td><td>Single day, inside a cut.</td></tr>
</table>

<p><b>Muscle glycogen capacity</b> is roughly 15 g per kg body weight, so about 1,000 g stored, worth
4,000 calories and roughly 3 kg of associated water. Refilling depleted glycogen is most of what the
first two weeks of eating properly will show on the scale and in the mirror.</p>

<h3>Every other formula I will need</h3>

<table>
<tr><th>What</th><th>Formula</th><th>My number</th></tr>
<tr><td>Lean body mass</td><td>weight x (1 - body fat %)</td><td>120 lb at 20%</td></tr>
<tr><td>Fat mass</td><td>weight x body fat %</td><td>21 lb at 20%</td></tr>
<tr><td>Goal weight at target body fat</td><td>LBM / (1 - target BF%)</td><td>140 lb at 10%, holding current LBM</td></tr>
<tr><td>FFMI</td><td>LBM_kg / height_m squared</td><td>57.2 / 2.89 = <b>19.8</b></td></tr>
<tr><td>Normalised FFMI</td><td>FFMI + 6.1 x (1.8 - height_m)</td><td>19.8 + 0.61 = <b>20.4</b></td></tr>
<tr><td>Natural FFMI ceiling</td><td>~25 normalised</td><td>I have roughly 4.6 points of room, which is real</td></tr>
<tr><td>Casey Butt max lean weight</td><td>Height and wrist based</td><td>~165-170 lb at 8-10% body fat</td></tr>
<tr><td>Rate of gain, natural</td><td>0.25-0.5% bodyweight/week</td><td>0.37-0.74 lb/week</td></tr>
<tr><td>Rate of loss, safe</td><td>0.5-1.0% bodyweight/week</td><td>0.74-1.47 lb/week</td></tr>
<tr><td>Energy deficit to weight</td><td>3,500 kcal per lb of fat</td><td>Rough. Real world runs 10-20% off due to adaptation.</td></tr>
<tr><td>Adaptive thermogenesis</td><td>10-15% below predicted after a long deficit</td><td>Why TDEE falls the longer I diet</td></tr>
<tr><td>Energy availability</td><td>(intake - exercise kcal) / LBM_kg</td><td>Below 30 kcal/kg is low energy availability. At 1,700 kcal with my job, I was near or under it.</td></tr>
<tr><td>Thermic effect of food</td><td>protein 20-30%, carbs 5-10%, fat 0-3%</td><td>~310 kcal/day at 2,800</td></tr>
<tr><td>NEAT from steps</td><td>steps x 0.04 x kg / 1000</td><td>14,000 steps = ~375 kcal</td></tr>
<tr><td>Resistance training burn</td><td>5-8 kcal/min</td><td>75 min = 375-600 kcal</td></tr>
<tr><td>Fiber</td><td>14 g per 1,000 kcal</td><td>43 g</td></tr>
<tr><td>Water baseline</td><td>0.6 oz per lb</td><td>88 oz</td></tr>
<tr><td>Water, training and altitude</td><td>+25 oz/hr trained, +10 oz for dry altitude</td><td>110-135 oz total</td></tr>
<tr><td>Sweat rate</td><td>(pre_wt - post_wt + fluid_in - urine) / hours</td><td>Measure it once on a hot shift</td></tr>
<tr><td>Sodium replacement</td><td>~1 g per litre of sweat</td><td>3-5 g/day for me, more on hot days</td></tr>
<tr><td>Creatine maintenance</td><td>0.03 g/kg, or just 5 g</td><td>5 g daily, every day</td></tr>
<tr><td>Creatine loading (optional)</td><td>0.3 g/kg for 5 days</td><td>20 g/day, then 5 g. Skips 3 weeks of waiting.</td></tr>
<tr><td>Caffeine, performance dose</td><td>3-6 mg/kg</td><td>200-400 mg. Start at 100 given a 94 bpm reading.</td></tr>
<tr><td>Caffeine half-life</td><td>~5 hours</td><td>200 mg at 3 p.m. is still 100 mg at 8 p.m.</td></tr>
<tr><td>Protein per dollar</td><td>cost / (grams protein / 25)</td><td>The only supermarket metric that matters</td></tr>
<tr><td>Recipe scaling</td><td>multiply every gram weight by the same factor</td><td>Macros scale linearly</td></tr>
<tr><td>Bodyweight trend</td><td>7-day average vs the average 3 weeks ago</td><td>Never compare single days</td></tr>
</table>

<h3>Worked example: recalculating at 158 lb</h3>
<p class="small">Say I am six months in and weigh 158 lb (71.7 kg) at 20% body fat, still on the
same job.<br>
RMR (Mifflin) = (10 x 71.7) + (6.25 x 170) - (5 x 21) + 5 = 717 + 1,063 - 105 + 5 = <b>1,680</b><br>
TDEE = 1,680 x 1.55 = <b>2,940</b><br>
Lean gain = 2,940 x 1.09 = <b>3,205 kcal</b><br>
Protein = 158 x 1.1 = <b>174 g</b><br>
Fat = 25% of 3,205 / 9 = <b>89 g</b><br>
Carbs = (3,205 - 696 - 801) / 4 = <b>427 g</b><br>
Fiber = 3,205 / 1,000 x 14 = <b>45 g</b><br>
Water = (158 x 0.6) + 25 + 10 = <b>130 oz</b><br>
LBM = 158 x 0.86 = 136 lb. FFMI = 61.7 / 2.89 = 21.3, normalised 21.9. Still under the ceiling.</p>
"""
