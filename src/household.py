# -*- coding: utf-8 -*-
"""Two-person section. Written to be readable whether or not the toggle is on."""

HOUSEHOLD = """
<h2 id="household">Cooking for two</h2>

<p>We are moving in together, so half of this stops being a solo problem. Same kitchen, same
grocery run, same pan, wildly different calorie targets. That is the thing to design around rather
than pretending we can eat identical plates.</p>

<div class="stripe">
<div><b>2,800</b><span>My kcal</span></div>
<div><b>1,900</b><span>Her kcal</span></div>
<div><b>4,700</b><span>Household / day</span></div>
<div><b>260 g</b><span>Household protein</span></div>
<div><b>$18</b><span>Typical day, both of us</span></div>
<div><b>$129</b><span>Typical week</span></div>
</div>

<h3>The two profiles</h3>
<table>
<tr><th>Variable</th><th>Me</th><th>Aaliyah</th><th>Notes</th></tr>
<tr><td>Stats</td><td>20, 5'8", 150 lb, ~20% bf</td><td>5'6.5", 120 lb</td>
<td>Hers is a maintenance estimate. Once she tells me her actual activity and goal, the calculator
rewrites it in ten seconds.</td></tr>
<tr><td>RMR (Mifflin)</td><td>1,665</td><td>1,323</td>
<td>Female equation subtracts 161 instead of adding 5. That single term is most of the gap.</td></tr>
<tr><td>Activity factor</td><td>1.55</td><td>1.45</td>
<td>Engraving shop plus daily training for me. Campus walking plus whatever she is doing for her.</td></tr>
<tr><td>Maintenance</td><td>2,580</td><td>1,920</td><td></td></tr>
<tr><td>Target</td><td>2,800, lean gain</td><td>1,900, maintenance</td>
<td>Change hers in the app if she wants to gain, cut or recomp.</td></tr>
<tr><td>Protein</td><td>160 g</td><td>100 g</td>
<td>Hers is 0.8 g/lb, which is plenty at maintenance. Mine is raised for a plant-heavy diet.</td></tr>
<tr><td>Carbs / fat / fiber</td><td>365 / 78 / 39 g</td><td>250 / 53 / 27 g</td><td></td></tr>
<tr><td>Water</td><td>125 oz</td><td>85 oz</td><td>Colorado is dry, both numbers run higher than a sea-level guideline would say.</td></tr>
</table>

<h3>How to actually cook it</h3>

<p>The trick is not making two meals. It is making one meal and splitting it unevenly. Every recipe
here lists a serving count and per-serving macros, so a 4-serving dish that comes out to 620 kcal
and 42 g protein a portion becomes: I take 1.6 servings, she takes 1.0. Same pan, same twenty
minutes, both targets hit.</p>

<table>
<tr><th>Dish size</th><th>My share</th><th>Her share</th><th>What it covers</th></tr>
<tr><td>2 servings</td><td>1.2</td><td>0.8</td><td>One dinner each</td></tr>
<tr><td>3 servings</td><td>1.5</td><td>1.0</td><td>Dinner each plus one lunch left over</td></tr>
<tr><td>4 servings</td><td>1.6</td><td>1.0</td><td>Dinner each plus both lunches tomorrow</td></tr>
<tr><td>6 servings</td><td>2.0</td><td>1.3</td><td>Batch cook, three days of dinners</td></tr>
</table>

<p>Where the gap gets awkward is that I need roughly 1.5x her food. Trying to close that at the
dinner table means either she is stuffed or I am short. Better answer: she eats a normal portion
and I close the rest of my gap with the shake and snack sections, which are built for exactly this.
A 700 kcal shake after training does more for the gap than a second helping does, and it does not
make dinner a chore for her.</p>

<h3>Groceries as a household</h3>

<p>Two people is where Costco starts making sense. A single person cannot get through a 6-pack of
tofu or 3 lb of Greek yogurt before it turns; two can. Flip the price toggle at the top of the app
to Costco and every recipe cost and shopping total recalculates. Items where the bulk size still
does not make sense for two are left on Walmart pricing, which is why some rows do not change.</p>

<p>Real numbers on our combined intake, worked from cost per calorie across the whole catalog
rather than by guessing. The median meal here runs <b>$3.92 per 1,000 kcal</b> at Walmart.</p>

<table>
<tr><th>Who</th><th>Per day</th><th>Per week</th><th>Per month</th></tr>
<tr><td>Me, 2,800 kcal</td><td>$10.98</td><td>$77</td><td>$329</td></tr>
<tr><td>Aaliyah, 1,900 kcal</td><td>$7.45</td><td>$52</td><td>$224</td></tr>
<tr><td><b>Both, 4,700 kcal</b></td><td><b>$18.44</b></td><td><b>$129</b></td><td><b>$553</b></td></tr>
<tr><td>Both, Costco pricing</td><td>$13.90</td><td>$97</td><td>$417</td></tr>
<tr><td>Both, budget-list week</td><td>$9.50</td><td>$67</td><td>$285</td></tr>
</table>

<p>So roughly <b>$550 a month</b> for all food for two people at Walmart, or <b>$417</b> shopping
Costco, or under <b>$300</b> on the cheap list of beans, lentils, rice, eggs, oats and frozen veg.
For comparison, the average American household of two spends around $800 to $900 a month on food
including eating out, so cooking from here lands well under that even before the budget list.</p>

<p>That spread between $285 and $553 is the actual lever. It is not about eating less, it is about
which recipes I lean on in a given week. Filter the collections for <b>Cheapest meals</b> during a
tight month and the number moves without touching calories or protein.</p>

<h3>What she can ignore</h3>

<p>Most of the front half. The calculation chapter, the leucine section and the gaining protocol
are my problems, not hers. The parts that are actually shared are the recipes, the collections, the
grocery rotation and the price data. If she wants her own targets running, hit <b>Aaliyah</b> in the
app bar and every recommendation reweights to her numbers instead of mine.</p>
"""
