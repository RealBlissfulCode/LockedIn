# -*- coding: utf-8 -*-
"""Reorganise Jaron's own plan rows into roads. Nothing is reworded and nothing
is invented: every Item and Note comes straight out of his file, only the road,
the plan and the section change."""
import csv, sys

rows = list(csv.reader(open('/tmp/hisplans.csv', encoding='utf-8')))
head, body = rows[0], rows[1:]
by_item = {r[2]: r for r in body}

# item text -> (Road, Plan, Section). Order here is the order in the file.
PLAN = [
 # ---------------- the thing actually in front of him ----------------
 ("Happening now", "Moving in together", "This week, in this order", [
   "Get the soft-pull preapproval",
   "Apply to all six staffing agencies the same week",
   "Book the Larimer County Workforce Center visit",
   "Submit the Colorado DVR application",
 ]),
 ("Happening now", "Moving in together", "Earning more before the lease", [
   "Wage conversation at Ritchey",
   "Get on the Zoup! schedule, or better, find a job in Fort Collins",
 ]),

 # ---------------- the lease road ----------------
 ("Renting together", "Getting the lease", "Finding the place", [
   "Pick 2 or 3 places to apply to",
   "Get a Portable Tenant Screening Report",
 ]),
 ("Renting together", "Getting the lease", "What to ask for at signing", [
   "Ask for the rate cut, the capped renewal, and the home-purchase clause",
 ]),
 ("Renting together", "Getting the lease", "Setting the tenancy up", [
   "Renters insurance",
   "Set up utilities and ask about deposit waivers",
 ]),

 # ---------------- the mortgage road ----------------
 ("Buying a home", "Buying", "Before anyone will lend to you", [
   "Wall off the trading account",
   "Three months of clean rent history",
   "Start the $300/mo house fund on autopay",
 ]),

 # ---------------- true whichever road ----------------
 ("True either way", "Setting up the home", "Before you sign anything", [
   "Both of us on our own auto policies",
   "Emergency fund at $3,000",
 ]),
 ("True either way", "Setting up the home", "Memberships and accounts", [
   "Costco Gold Star membership",
   "Have Aaliyah verify Costco through UNiDAYS",
   "Walmart+",
   "Connexion internet on her student rate",
   "Spotify student for her, then look at a Duo plan",
   "Amazon Prime Student",
   "Chewy autoship for the cat",
   "Free Transfort and MAX with her RamCard",
 ]),
 ("True either way", "Setting up the home", "Bringing our stuff with us", [
   "Blue couch", "Rocking couch chair", "TV",
   "Adjustable barbells", "Pullup bar", "Weighted vest", "Resistance bands",
   "Ab roller", "Parallettes",
   "Paintings", "Mirror", "Tools and knives", "Electronics and computers",
   "Manscaped razor", "Water bottles", "Sunglasses and glasses", "Necklace", "Clothes",
 ]),
 ("True either way", "Setting up the home", "Buy before the first night", [
   "Mattress and frame", "Pillows", "Bed covers and blankets",
   "Shower curtain and liner", "Toilet paper, paper towels, trash bags",
   "Basic kitchen: plates, silverware, pans, chef knife",
   "Carbon monoxide detector", "Fire extinguisher", "Light bulbs and command strips",
 ]),
 ("True either way", "Setting up the home", "Furniture, hunted not bought", [
   "Two desks", "Desk chairs", "Dining table", "Weight bench", "TV stand",
   "Vacuum", "Auto cat litter box", "RGB lights",
 ]),
 ("True either way", "Setting up the home", "Once we are actually in", [
   "Go out to eat twice a month, starting month one",
 ]),

 # ---------------- decisions, not tasks ----------------
 ("Still undecided", "Open questions", "Money", [
   "Is a roommate actually on the table?",
   "Do we split Eating Out, Social and Emergency 50/50?",
   "Add a health insurance premium line?",
   "Confirm the phone device balance",
 ]),
 ("Still undecided", "Open questions", "Housing", [
   "Duplex or single family?",
   "Does Aaliyah go on the loan?",
   "Ask both assumable listings for the loan payoff balance",
 ]),
]

out = [["Road", "Plan", "Section", "Item", "Done", "Note"]]
used = set()
for road, plan, sec, items in PLAN:
    for it in items:
        if it not in by_item:
            print("NOT IN HIS FILE:", it); sys.exit(1)
        if it in used:
            print("USED TWICE:", it); sys.exit(1)
        used.add(it)
        r = by_item[it]
        out.append([road, plan, sec, r[2], r[3], r[4]])

missing = [r[2] for r in body if r[2] not in used]
if missing:
    print("LEFT BEHIND:", missing); sys.exit(1)

with open('/tmp/plans-organised.csv', 'w', newline='', encoding='utf-8') as fh:
    csv.writer(fh).writerows(out)

print("his rows in: %d" % len(body))
print("rows out:    %d" % (len(out) - 1))
print("every row accounted for, none duplicated, none invented")
print()
from collections import Counter
c = Counter((r[0], r[1], r[2]) for r in out[1:])
last = None
for (road, plan, sec), n in c.items():
    if road != last:
        print(road.upper()); last = road
    print("   %-22s %-32s %d" % (plan, sec, n))
