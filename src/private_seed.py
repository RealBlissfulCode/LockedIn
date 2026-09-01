# -*- coding: utf-8 -*-
"""Everything personal that ships inside index.html, before encryption.

This is the only file in the repo that knows anything about where we might live,
what we earn, or what we owe. build.py encrypts the whole thing with the passcode
so none of it is readable in View Source.

It seeds ONCE, per browser, the first time the passcode is entered. After that it
is ordinary editable data: rename it, add to it, delete it, and it stays deleted.
Nothing here is a template and nothing re-appears on the next deploy.

Everything traces back to Moving_In_v7.xlsx.
"""

# --------------------------------------------------------------- big purchases
# Possible Places, the two in-zone tables. "All in" is rent + pet rent + utilities.

APARTMENTS = [
    ("Fox Meadows", 1119, "Fort Collins", "in town", "5-15 min", "1", "2", "", 35, 290, 1444,
     "3644 S Timberline. Closest thing to Timnath at the lowest price on the list. 1-2 bed."),
    ("706 2nd St, Apt A7", 1225, "Windsor", "southeast", "20 min", "2", "1", "", 35, 300, 1560,
     "Cheapest real 2 bed. Bare bones but the price is the price."),
    ("Aspenleaf Apartments", 1315, "Fort Collins", "in town", "5-15 min", "1", "2", "", 35, 290, 1640,
     "3501 S Stover. South FoCo, 1-2 bed, easy run to campus."),
    ("Governor's Park", 1350, "Fort Collins", "in town", "5-15 min", "2", "1", "", 35, 290, 1675,
     "700 E Drake. Studio through 2 bed, right in the south corridor."),
    ("Village Gardens", 1398, "Fort Collins", "in town", "5-15 min", "1", "1", "", 35, 290, 1723,
     "1025 Oxford Ln. Goes up to 3 bed, so the roommate plan works here. "
     "Reviews report $180-250 jumps at renewal, so ask for a capped increase in writing."),
    ("Brookview Apartments", 1407, "Fort Collins", "in town", "5-15 min", "1", "1", "", 35, 290, 1732,
     "1717 Welch St. 1-3 bed, south FoCo."),
    ("Peaks on Drake", 1425, "Fort Collins", "in town", "5-15 min", "2", "1", "", 35, 300, 1760,
     "515 E Drake. Renovated, pet friendly, 14 units open so there is room to negotiate."),
    ("Plat 10 at The Ranch", 1435, "Windsor", "southeast", "20 min", "Studio", "1", "543", 35, 220, 1690,
     "Studio. Bridge option only, 543 sqft with two of us and a cat is rough."),
    ("Max Flats", 1519, "Fort Collins", "in town", "5-15 min", "1", "1", "", 35, 290, 1844,
     "505 S Mason. Walkable to campus. Move in special running, ask what it is."),
    ("1134 W 10th St", 1550, "Loveland", "south", "25 min", "2", "1", "", 35, 300, 1885,
     "Cheapest 2 bed in Loveland. One unit, so it will go fast."),
    ("Rendezvous Trail", 1634, "Fort Collins", "in town", "5-15 min", "2", "", "", 35, 300, 1969,
     "2918 S Timberline. Southeast, in unit laundry, real 2 bed. Only 3 left."),
    ("Reserve at Centerra", 1653, "Loveland", "south", "25 min", "1", "1", "", 35, 300, 1988,
     "4264 McWhinney. Gym and pool on site, which cancels a gym membership."),
    ("Old Town Flats", 1671, "Fort Collins", "in town", "5-15 min", "2", "", "", 35, 300, 2006,
     "310 N Mason. Best walkability in town, big premium for it."),
    ("Easy Living Near It All", 1700, "Windsor", "southeast", "20 min", "2", "2", "1038", 35, 320, 2055,
     "Most space in the list. Two full baths matters when we both leave at once."),
    ("The Greens at Van de Water", 1736, "Loveland", "south", "25 min", "1", "1", "", 35, 300, 2071,
     "2900 Mountain Lion Dr. 21 units open."),
]

HOUSES = [
    ("220 Manor Ct #A", 395000, "Windsor", "southeast", "20 min", "2", "2", "2734", "1998", 144, 3190,
     "144/sqft, best value on the sheet. Check how much of it is actually finished."),
    ("6886 Autumn Leaf Dr", 415000, "Timnath", "southeast", "15 min", "2", "3", "2048", "2019", 203, 3363,
     "Closest to campus. 126 days on market, already reduced, 2k toward closing. Push past the 2k."),
    ("901-903 W Kelly Dr", 465000, "Loveland", "south", "25 min", "4", "2", "1433", "1963", 324, 3445,
     "THE DUPLEX. Maybe assumable, 307 days. A true two-unit deed unlocks the FHA 75% rent credit, "
     "which is worth about $2,175/mo of buying power. Best single lead on the sheet."),
    ("2366 Blissful Lane", 475000, "Windsor", "southeast", "20 min", "3", "2", "2906", "2024", 163, 3433,
     "2024 build at 163/sqft, no HOA. Last buyer flaked so they want someone real."),
    ("717 Shipman Mountain Ct", 475000, "Windsor", "southeast", "20 min", "5", "2", "2472", "1979", 192, 3433,
     "5 beds, no HOA or metro district. Two rented rooms = 1,400-1,600. Only 2 baths though."),
]


def _apartments():
    out = []
    for name, rent, city, direction, csu, beds, baths, sqft, pet, util, allin, why in APARTMENTS:
        f = {"City": city, "Direction": direction, "To CSU": csu, "Beds": beds}
        if baths:
            f["Baths"] = baths
        if sqft:
            f["Sq ft"] = sqft
        f["Pet rent"] = "$%d" % pet
        f["Utilities"] = "$%d" % util
        f["All in"] = "$%s" % format(allin, ",")
        out.append({"name": name, "price": rent, "link": "", "notes": why, "fields": f})
    return out


def _houses():
    out = []
    for name, price, city, direction, csu, beds, baths, sqft, built, psf, pay, why in HOUSES:
        out.append({"name": name, "price": price, "link": "", "notes": why, "fields": {
            "City": city, "Direction": direction, "To CSU": csu, "Beds": beds, "Baths": baths,
            "Sq ft": sqft, "Built": built, "$/sqft": "$%d" % psf,
            "Payment": "$%s" % format(pay, ","),
        }})
    return out


PURCHASES = {
    "Places we could rent": {
        "cat": "Housing",
        "note": "Everything 20 minutes or less to CSU, south or southeast. Aaliyah drives to campus "
                "every day and the shorter drive buys us overtime, homework, gym and sleep. "
                "Price shown is rent; All in is rent + pet rent + utilities. Cheapest first. "
                "Colorado caps pet rent at $35/mo or 1.5% of rent, and the pet deposit at $300 refundable. "
                "Non-refundable pet fees are illegal here.",
        "items": _apartments(),
    },
    "Houses in the zone": {
        "cat": "Housing",
        "note": "Same 20 minute zone. Payment is the all-in estimate: P&I, MIP, tax, insurance and HOA. "
                "Cheapest is $395k, average $205/sqft.",
        "items": _houses(),
    },
}


# ------------------------------------------------------------------ strategies
# The Strategies sheet, one list per tier. Sorted by dollars per hour of effort
# inside each list. Anything marked DEAD has been checked and is dead.

def _s(name, low, real, high, rate, effort, when, status, how):
    return {"name": name, "low": low, "real": real, "high": high,
            "rate": rate, "effort": effort, "when": when, "status": status, "how": how}


STRATEGIES = {
    "Tier 1 - Do this week": {
        "note": "Free, no purchase decision needed, highest dollar per hour spent. "
                "The preapproval is the one thing blocking everything else.",
        "items": [
            _s("Soft-pull preapproval", 0, 0, 0, "", "2 calls", "NOW", "NOT DONE",
               "THE ONE THING BLOCKING EVERYTHING. Every place on the rent and buy lists has been judged "
               "against an estimated DTI. Ryan Lococo at NEO plus one independent CHFA lender. Soft pull, "
               "no credit hit, free. Ask: max price solo, max with Aaliyah, can you do CHFA, can you do 203k."),
            _s("Staffing agencies, all six", 0, 800, 1700, "$400", "2 hrs", "NOW", "NOT DONE",
               "TEKsystems, Insight Global, Robert Half, Actalent, Aerotek, Express. Free to you, the "
               "employer pays. Contract-to-hire help desk in this corridor runs $25-32. This is the only "
               "move that raises the number underwriters actually count. Apply to all six the same week, "
               "then CALL the branch the next day."),
            _s("Shop auto insurance properly", 60, 150, 300, "$50", "1 afternoon", "Before lease", "NOT DONE",
               "American National is $2,631/yr for a CO 20-year-old. Allstate is $8,038 for the SAME driver. "
               "A $5,400/yr spread. Quote AmNat, California Casualty, Progressive. Quote joint AND separate "
               "with Aaliyah, because her at-fault accident can cross-rate against you and eat the multi-car discount."),
            _s("Larimer County Workforce Center", 0, 0, 0, "", "1 visit", "NOW", "NOT DONE",
               "Free WIOA training money, NO waitlist. Ask for an Individual Training Account for CompTIA A+. "
               "~$500 in exam fees, 2-3 months study. A+ plus the Google Cybersecurity cert plus GitHub is a "
               "real $25-30/hr profile. Say the credential and the job title, not 'I want training.'"),
            _s("Colorado DVR application", 0, 0, 0, "", "30 min", "NOW", "NOT DONE",
               "Waitlist went active Jan 28 2026, all categories closed. Release is by priority category AND "
               "APPLICATION DATE, so applying now buys queue position for free. Bring CRMO documentation, "
               "rheumatology records, imaging. Frame it as a career transition: 'I need to move into IT "
               "before the physical work becomes a problem.'"),
            _s("MVNO phone switch", 60, 90, 120, "$90", "1 afternoon", "NOW", "CHECK FIRST",
               "Total Wireless $20/line BYO with autopay. Two lines ~$40 vs $120-160 postpaid. BUT check "
               "whether you are a line on your parents' Verizon first. You may already pay less than $20 "
               "and switching would COST you money."),
        ],
    },
    "Tier 2 - Earn more": {
        "note": "Ranked by real dollars per hour after costs, not gross.",
        "items": [
            _s("Overtime at Ritchey", 150, 400, 800, "$30", "Hours", "Now", "ACTIVE",
               "$30/hr at time and a half, 8 mile drive. Highest real wage available to you. ASK BEFORE THE "
               "LASER IS BACK UP. Covering structural sheets is your whole case and it vanishes the week the "
               "machine returns. Frame it as revisiting scope, not a raise request, since Bryce already said no once."),
            _s("Rent the spare room", 0, 700, 1600, "n/a", "Low once filled", "With the lease", "PENDING",
               "Biggest single number on this page and it costs you almost nothing. Aaliyah picks the person; "
               "a friend of hers solves the guy problem and the jealousy problem at once. Frame it to her as: "
               "one person we both like means we can buy instead of lease."),
            _s("Raise at Ritchey", 100, 300, 600, "n/a", "One talk", "Now", "NOT DONE",
               "Worth LESS in dollars than OT but MORE in leverage: base wage counts for a mortgage after 30 "
               "days of paystubs, overtime needs 2 years. Anchor at $26 so $24 is the compromise. Never give "
               "a personal reason, it turns a business case into a favor."),
            _s("Plasma, both of us", 300, 500, 720, "$18", "6 hrs/wk", "Now", "CHECK ELIGIBILITY",
               "CSL on Horsetooth $55-80, BioLife on College $60-90. CALL FIRST: CRMO is an autoinflammatory "
               "condition and many centers defer donors with autoimmune or autoinflammatory diagnoses. "
               "Do not budget this until it is confirmed."),
            _s("Doordash", 0, 700, 1100, "$14", "10-20 hrs", "Now", "ACTIVE",
               "$15-20 gross in the busy window, about $14/hr after gas and wear. Fine as flex cash. "
               "Zero mortgage credit without 2 years of returns."),
            _s("MysticNoob monetization", 0, 0, 0, "?", "?", "Own conversation", "UNTOUCHED",
               "275,000 subscribers. The single largest untouched asset in this entire plan and it has not "
               "come up once across weeks of housing math. Scales without your body, which matters with CRMO. "
               "Will not help you qualify (1099 needs 2 yrs of returns) but it funds the reserve that lets an "
               "underwriter stretch your DTI. Worth its own session."),
            _s("Zoup! Firestone", 900, 1250, 1500, "$10.60", "24 hrs + 6.5 driving", "Started", "RECONSIDER",
               "YOUR OWN MATH: $10.60/hr once the 40-mile-each-way drive is priced in. That is below every "
               "other option here AND it gets worse when you move to Fort Collins. Find a second job IN Fort "
               "Collins. Same $15.50 with a 10 minute drive is worth $300/mo in fuel and 6.5 hrs a week of your life."),
            _s("Car wrap advertising", 0, 150, 500, "passive", "Passive", "At 21", "BLOCKED",
               "Wrapify requires age 21. Carvertise needs a 2008+ vehicle and a clean record; your tickets and "
               "her F150's year both fail. Campaigns cluster in Denver metro and pay only if 25%+ of driving is "
               "in-zone. Free to sign up, treat as a lottery ticket. They pay for wrap AND removal; never pay a "
               "cent yourself or it is a scam."),
            _s("Learn vinyl wrapping", 0, 0, 800, "n/a", "Months", "Later", "YEAR 2",
               "$500-2,000 a car once you are good. Practice on your own hood. Real trade, wrong year."),
        ],
    },
    "Tier 3 - Negotiate": {
        "note": "Costs nothing but nerve. December and January is the window, and our timing is already right.",
        "items": [
            _s("Ask for the RATE cut, not a free month", 0, 125, 200, "n/a", "One ask", "At signing", "READY",
               "CORRECTION TO THE SHEET: this was backwards. $1,500 off once = $125/mo in year one, identical "
               "to a $125 rate cut. But renewal is calculated off FACE rent. Sign at $1,600 with a free month "
               "and they renew from $1,600. Sign at $1,475 flat and they renew from $1,475. That is ~$135/mo "
               "apart in year two. Ask for the rate. Take the concession only if they refuse."),
            _s("Capped renewal increase in writing", 0, 0, 0, "n/a", "One ask", "At signing", "READY",
               "Kicks in at RENEWAL, year two, so it is not year-one cash. Almost nobody asks. Village Gardens "
               "reviews report $180-250 jumps at renewal. Worth more than a free month over a 16-month lease."),
            _s("Home-purchase early termination clause", 0, 0, 0, "n/a", "One ask", "At signing", "READY",
               "ONE-TIME, avoids a ~$3,000 lease-break penalty. Terminate with 60 days notice and proof of a "
               "purchase contract, no penalty. Standard lease break is two months rent. If we buy in month 8 "
               "this clause is worth $3,000+. Most properties agree because it is rare and costs them nothing to promise."),
            _s("Sign in the slow season", 0, 80, 200, "n/a", "Timing", "Oct-Feb", "ON TRACK",
               "Nobody moves in Northern Colorado in winter. Railway Flats has run $1,500 off, Pavilions $1,000 off. "
               "The December/January timing is already right."),
            _s("16-17 month lease", 0, 50, 100, "n/a", "One ask", "At signing", "READY",
               "Not just 'longer.' 16-17 months makes it expire in May/June, their PEAK re-leasing season. "
               "That is what they actually want and they will price it better than a plain 12 or 18. "
               "It also lands the purchase in spring 2028."),
            _s("Portable Tenant Screening Report", 0, 0, 0, "n/a", "Free", "Applying", "READY",
               "ONE-TIME, $100-150 in avoided application fees. Colorado law: provide a PTSR under 30 days old "
               "and they CANNOT charge an application fee. Every property on the rent list acknowledges this in "
               "its own listing. Two or three applications at $50-75 each."),
            _s("Point at days on market", 0, 0, 0, "n/a", "Research", "Touring", "READY",
               "ONE-TIME price concession, not monthly. Say the number out loud. 307 days on Kelly Dr, "
               "126 on Autumn Leaf. A listing that has sat has a seller who has already lost the argument with themselves."),
            _s("Seller-paid closing costs", 0, 0, 0, "n/a", "At offer", "Buying", "READY",
               "ONE-TIME, up to 6% of price. On $340k that is $20,400. CRITICAL: concessions can NEVER fund the "
               "down payment, only closing costs, prepaids and rate buydown. CHFA assistance covers the down "
               "payment. You need BOTH, and they do stack. NEO's own lender confirmed it in writing."),
            _s("Walk on the first offer", 0, 0, 0, "n/a", "Nerve", "Always", "READY",
               "We have somewhere to live right now. That is the whole leverage and it is real."),
        ],
    },
    "Tier 4 - Grants and free money": {
        "note": "Only applies when actually buying. These are one-time amounts at closing, not monthly, "
                "so they are deliberately left out of the monthly swing total.",
        "items": [
            _s("Impact Development Fund", 0, 0, 0, "n/a", "One call", "When buying", "NOT CALLED",
               "ONE-TIME, up to $46,000 at closing. BIGGEST NUMBER AVAILABLE and it was not on the sheet. "
               "Larimer and Weld specifically. Up to 10% of price capped at $50,000, or up to 15% under their "
               "Proposition 123 tier. On a $340k purchase that is $34,000-51,000. Ask which lenders originate "
               "for them AND whether the Prop 123 tier applies. Most people do not know to ask."),
            _s("CHFA down payment assistance", 0, 0, 0, "n/a", "With lender", "When buying", "NOT DONE",
               "ONE-TIME, $9,000-12,400 at closing. A grant at 3% of the first mortgage, never repaid. Or a "
               "deferred second at 4% with no monthly payment and no DTI hit. TAKE THE GRANT if offered both; "
               "the second is repaid at sale and reduces real equity. Larimer income limit ~$127,600, we are far under."),
            _s("FHA 75% rental income rule", 0, 0, 0, "n/a", "Buy a duplex", "When buying", "KEY",
               "NOT CASH. It raises qualifying INCOME by ~$2,175/mo of buying power, which is a different thing. "
               "On an owner-occupied 2-4 unit, FHA counts 75% of the other unit's market rent toward qualifying "
               "income IMMEDIATELY, no history required. ONLY works on a true two-unit deed; a half-duplex or "
               "paired home does NOT count. 901-903 W Kelly Dr is the one on the list."),
            _s("FHA 203k renovation loan", 0, 0, 0, "n/a", "Ask lender", "When buying", "ASK RYAN",
               "Buy a rough house and roll up to $75,000 of repairs into the mortgage at 3.5% down. Your "
               "electrical background means you can read a padded contractor bid, which is exactly where "
               "first-timers get destroyed."),
            _s("metroDPA / CHAC / High Plains", 0, 0, 0, "n/a", "Calls", "When buying", "NOT DONE",
               "metroDPA covers Larimer. CHAC is a statewide nonprofit doing low-interest seconds. High Plains "
               "is the Weld agency. Most cannot be combined, so pick the largest one you qualify for."),
            _s("CHFA homebuyer class", 0, 0, 0, "n/a", "One evening", "When real", "HOLD",
               "Do NOT pay for this yet. ~$75, expires in 12 months, and it is only useful if we buy. Take it "
               "the week the preapproval says buying is real. Ask the lender first whether a free HUD-counselor "
               "version is accepted."),
        ],
    },
    "Tier 5 - Discounts we qualify for": {
        "note": "Small individually, real together, and none of them require anyone to say yes.",
        "items": [
            _s("Aaliyah's student status", 50, 120, 200, "n/a", "Show the .edu", "Day one", "READY",
               "Connexion takes $20 off internet. Free Transfort and MAX. Spotify student $6 not $12. "
               "Costco via UNiDAYS gets a bonus Shop Card. Amazon Prime Student is half price."),
            _s("Costco Gold Star membership", 0, 100, 150, "n/a", "One signup", "Now", "READY",
               "$65/yr. Bulk gluten-free is where the GF premium actually closes. Sign up as a NEW member for "
               "the $50 Shop Card promo, so year one is effectively $15. Have Aaliyah verify as a CSU student "
               "for the bonus card. Skip Executive until we clear $3,250/yr of Costco spend."),
            _s("Costco restaurant gift cards", 0, 90, 120, "n/a", "Free", "Now", "READY",
               "20-25% off face value on restaurants and entertainment. NOT groceries; Amazon and Walmart cards "
               "sell at face value everywhere. Saves on the eating-out line only."),
            _s("CSU Health Network for her", 40, 90, 150, "n/a", "Enroll", "Registration", "READY",
               "SHIP dental covers $1,000/yr. Billed to the student account."),
            _s("Health District dental for you", 30, 60, 120, "n/a", "One call", "Now", "READY",
               "202 Bristlecone, Fort Collins. Sliding scale for Larimer residents."),
            _s("Prescription discount cards", 10, 25, 50, "n/a", "Free", "Now", "READY",
               "GoodRx plus Health District prescription assistance. Works even with insurance."),
            _s("Ritchey health plan", 0, 0, 0, "n/a", "One form", "Open enrollment", "OPTIONAL NOW",
               "You are on your dad's plan until 26 and so is Aaliyah, so this is not urgent. Compare the "
               "Ritchey plan against staying on his: pre-tax premiums lower taxable income, but a parent's plan "
               "is usually cheaper outright. With CRMO, never go uninsured."),
        ],
    },
    "Tier 6 - Cut the bills": {
        "note": "Note that four of these COST money and are still correct. Cheapest is not the same as right.",
        "items": [
            _s("Drop collision on both cars", 0, 275, 350, "n/a", "One call", "At move-out", "STAGED",
               "Accord ~$15k, F150 ~$6k. Collision is the expensive half and the one your driving skill actually "
               "affects. Rule: drop it when annual premium plus deductible passes half the car's value."),
            _s("Stop paying the GF label premium", 80, 100, 120, "n/a", "Read labels", "Now", "READY",
               "GF products run 183% over wheat counterparts (bread 229%, pasta 227%). But plain rice, corn "
               "tortillas, potatoes, beans and most chocolate NEVER contained gluten; you are paying for a sticker. "
               "Spend the premium only on bread and pasta, and buy those at Aldi liveGfree or Costco."),
            _s("Meal prep the handbook", 50, 120, 200, "n/a", "1 hr Sunday", "Weekly", "READY",
               "Kills most of the eating-out line. Cooking at home saves YOU more than most people because "
               "GF restaurants carry the biggest premium."),
            _s("Cut the brand extras on Shopping", 0, 107, 213, "n/a", "Willpower", "Monthly", "READY",
               "Staples $677, brands add $213. Half of that is the easiest $100 on this page."),
            _s("Rent her textbooks", 0, 60, 120, "n/a", "Per semester", "Each term", "READY",
               "Never buy new. Rent, buy used, or use CSU library reserve copies."),
            _s("Telematics app", 20, 50, 90, "n/a", "Let it track", "At signup", "READY",
               "10-30% for young drivers with clean habits. Hard braking hurts you."),
            _s("Good student discount for Aaliyah", 0, 45, 80, "n/a", "Show grades", "At CSU", "READY",
               "8-25% off with a 3.0+. Lasts until 25."),
            _s("Household hacks", 20, 45, 80, "n/a", "Free", "Now", "READY",
               "Half scoop of detergent, wool dryer balls, vinegar and water. The bottles overdose on purpose."),
            _s("Menstrual cup or period underwear", 5, 15, 25, "n/a", "One buy", "Now", "READY",
               "Cup is $25 and lasts years against ~$13/mo. Roughly a 3,000% return over its life. Colorado "
               "killed the tampon tax in 2022, so this is the cheapest state in the country for these."),
            _s("Safety razor", 5, 10, 13, "n/a", "One buy", "Whenever", "READY",
               "Blades are pennies against $13 a pack."),
            _s("KEEP comprehensive on the Accord", -50, -40, -30, "n/a", "One call", "At move-out", "STAGED",
               "COSTS money, does not save it, and keep it anyway. Colorado is #2 nationally for hail claims: "
               "167,000 auto claims from one Front Range afternoon in 2017. Your CDOT sign claim WAS a "
               "comprehensive claim. $30-50/mo. Skill does not protect you from hail."),
            _s("KEEP UM/UIM on both", -25, -20, -15, "n/a", "One call", "At move-out", "STAGED",
               "1 in 5 Colorado drivers is uninsured, ninth highest in the nation. $15-25/mo. Colorado requires "
               "carriers to offer it and you must reject it IN WRITING. Do not."),
            _s("Raise liability limits to 100/300/100", -40, -30, -20, "n/a", "One call", "At move-out", "STAGED",
               "CO minimum property damage is $15,000. Hit a new truck and you personally owe the difference, "
               "and they can get a judgment. You have a 780 and a house plan; this is the one place not to go cheapest."),
        ],
    },
    "Tier 7 - Protect the plan": {
        "note": "Zero dollars, highest consequence if ignored. Nothing on any other list survives breaking these.",
        "items": [
            _s("Pick three income streams, not six", 0, 0, 0, "n/a", "Discipline", "Always", "CRITICAL",
               "Ritchey plus OT plus Zoup plus Doordash plus plasma plus gym plus LoopedIn is 70+ hours. You have "
               "a chronic inflammatory bone condition and you have mentioned driving tired. Sustained 70-hour "
               "weeks are the exact stressor that pushes inflammatory conditions out of remission, and a flare "
               "costs months, not a week. Set an END DATE on the sprint before you start it."),
            _s("Do not skip the doctor", 0, 0, 0, "n/a", "Honest note", "Always", "CRITICAL",
               "One CRMO flare that needs real treatment costs more than every line on this page combined. "
               "This is the one item with no dollar figure and it should not have one."),
            _s("Wall off the trading account", 0, 0, 0, "n/a", "Discipline", "90 days out", "CRITICAL",
               "Underwriters read 90 days of statements. Large unexplained transfers next to a down payment kill "
               "files. Every deposit needs a paper trail."),
            _s("Own auto policies before the lease", 0, 0, 0, "n/a", "Two calls", "Before lease", "CRITICAL",
               "Staying on a parent's policy after establishing your own residence is material misrepresentation. "
               "The consequence is not a fee, it is a DENIED CLAIM or a rescinded policy at the moment you need it. "
               "Budget the jump: $150 to $250-400."),
            _s("LoopedIn stays at zero", 0, 0, 0, "n/a", "Discipline", "Always", "LOCKED",
               "The apartment stands on W2 alone. If money lands it goes to the house fund."),
            _s("Never take a deed subject-to", 0, 0, 0, "n/a", "Discipline", "Always", "LOCKED",
               "If you ever talk to a distressed owner: never take a deed while the mortgage stays in their name. "
               "And you are only exempt from Colorado's Foreclosure Protection Act because you will LIVE there a "
               "year. Violations are a criminal misdemeanor, up to 1 year and $25,000."),
        ],
    },
    "Verified dead - do not revisit": {
        "note": "All checked, all dead. Kept so the same idea does not get re-researched in three months.",
        "items": [
            _s("SNAP", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "CO gross limit is 200% FPL = $2,610/mo for one person. You are at $3,467, and it uses GROSS not "
               "net. Adding Aaliyah makes it WORSE: the two-person limit is ~$3,526 while her income adds "
               "$1,700-2,000. It stacks, it does not average. The celiac deduction only applies to households "
               "with someone 60+ or on disability."),
            _s("Federal EITC", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "Childless filers must be 25. You are 20. Worth ONE question to a tax preparer about whether "
               "Colorado's state EITC has a lower age floor."),
            _s("Celiac tax deduction", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "Only the amount above 7.5% of AGI, and only if you itemize. The standard deduction wins at your "
               "income. KEEP THE PAPERWORK anyway; it becomes real if income rises or costs spike."),
            _s("Rent-to-own", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "You still have to qualify at the end: same income, same DTI. Non-refundable option fee of 3-5%, "
               "above-market rent, and most contracts void the option if you are late once. Incompatible with "
               "CHFA and FHA. The path your mom is looking for IS CHFA plus DPA."),
            _s("Foreclosure auctions", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "Cashier's check due at the sale, same day. No financing exists. Needs $200-400k cash. Also no "
               "interior access and you inherit the occupants."),
            _s("Manufactured home on leased land", 0, 0, 0, "n/a", "-", "-", "DEAD",
               "2211 W Mulberry was $124,250 PLUS $1,035/mo lot rent = $2,857 all in. More than a $310k house, "
               "on land you never own, in a 55+ community you cannot legally buy into."),
            _s("Medicaid", 0, 0, 0, "n/a", "-", "-", "N/A",
               "Both of you are on your fathers' plans until 26. Nothing to apply for, and it saves $250+/mo "
               "you were never going to spend."),
            _s("TABOR refund", 0, 0, 0, "n/a", "-", "-", "NEGLIGIBLE",
               "$20-62 for single filers, and economists project NO general refund in 2027. Automatic when you file."),
        ],
    },
}


# -------------------------------------------------------------------- planning
# General plans. Collections hold subsections, subsections hold items.

def _c(name, note, subs):
    return {"name": name, "note": note, "subs": subs}


def _sub(name, note, items):
    return {"name": name, "note": note, "items": items}


def _i(text, note=""):
    return {"text": text, "note": note}


PLANNING = [
    _c("Moving in together", "Everything that has to happen to actually get the keys and be able to live "
       "there. Roughly in order. The money side lives on Financial; this is the doing side.", [
        _sub("Before we sign anything", "None of these cost money and all of them get harder to do later.", [
            _i("Get the soft-pull preapproval", "Blocks every other housing decision. Ryan Lococo at NEO plus one independent CHFA lender."),
            _i("Both of us on our own auto policies", "Required the day we establish our own residence. Budget $250-400, not $150."),
            _i("Get a Portable Tenant Screening Report", "Under 30 days old means Colorado landlords cannot charge an application fee."),
            _i("Emergency fund at $3,000", "Three months solo at the low column. Before signing, not after."),
            _i("Wall off the trading account", "Underwriters read 90 days back. Do this 90 days before applying."),
            _i("Pick 2 or 3 places to apply to", "Not eight. Application fees add up and the PTSR only helps so much."),
            _i("Ask for the rate cut, the capped renewal, and the home-purchase clause", "All three at signing. All three are free to ask."),
        ]),
        _sub("Memberships and accounts", "Set these up in the first week. Several of them pay for themselves "
             "inside a month, and a few need her .edu address.", [
            _i("Costco Gold Star membership", "$65/yr. Sign up as a NEW member for the $50 Shop Card promo, so year one is really $15. Store is 4705 Weitzel St, Timnath, on the way home from Ritchey."),
            _i("Have Aaliyah verify Costco through UNiDAYS", "Student verification adds a bonus Shop Card."),
            _i("Walmart+", "Worth it if we are doing the Walmart run weekly. Free delivery and fuel discount. Check the student rate first."),
            _i("Connexion internet on her student rate", "1 Gig for $50 instead of $70 with a .edu."),
            _i("Renters insurance", "$15-25/mo. Every lease requires proof, so have it before the walkthrough."),
            _i("Set up utilities and ask about deposit waivers", "FoCo may waive with good credit. Ask, do not assume."),
            _i("Spotify student for her, then look at a Duo plan", "$6 not $12, and Duo would cut both of ours."),
            _i("Amazon Prime Student", "Half price with the .edu."),
            _i("Chewy autoship for the cat", "5-10% under retail on food."),
            _i("Free Transfort and MAX with her RamCard", "Already covered by tuition. This is why her fuel line is $50 and not $280."),
        ]),
        _sub("Bringing our stuff with us", "Already owned, already paid for. Every line here is a thing we do "
             "NOT buy. Worth about $900 against the furniture list.", [
            _i("Blue couch", "Worn but fine. Saves $300-600. Replace it in year two."),
            _i("Rocking couch chair", "Covers part of the seating. We still need two desk chairs."),
            _i("TV", "Good condition. Only need a stand, about $35 used at ReStore or ARC."),
            _i("Adjustable barbells", "Gym"),
            _i("Pullup bar", "Gym"),
            _i("Weighted vest", "Gym"),
            _i("Resistance bands", "Gym"),
            _i("Ab roller", "Gym"),
            _i("Parallettes", "Gym. With these the gym is ~90% covered. Only a bench left, $50-80 used."),
            _i("Paintings", "Covers most of the decoration line. Only RGB lights left."),
            _i("Mirror", "Also decoration."),
            _i("Tools and knives", "This is why the Tools row on Shopping is empty."),
            _i("Electronics and computers", "Open question: do we actually have a router?"),
            _i("Manscaped razor", "Blades still recur monthly on Shopping."),
            _i("Water bottles"),
            _i("Sunglasses and glasses"),
            _i("Necklace"),
            _i("Clothes", "Normal replacement only, ~$40/mo each."),
        ]),
        _sub("Buy before the first night", "The short list that makes the place liveable on day one. "
             "Everything else can wait a paycheck.", [
            _i("Mattress and frame", "$150 used route. NEVER buy a used mattress; the $150 is a new Placid queen at AFW plus a used frame."),
            _i("Pillows", "Buy new. Same reason as the mattress."),
            _i("Bed covers and blankets", "Used is fine if it washes."),
            _i("Shower curtain and liner"),
            _i("Toilet paper, paper towels, trash bags", "Costco run."),
            _i("Basic kitchen: plates, silverware, pans, chef knife", "About $65 total at Walmart."),
            _i("Carbon monoxide detector", "Required in Colorado rentals. Confirm whether the landlord supplies it."),
            _i("Fire extinguisher", "$25, and some landlords knock the renters premium for having one."),
            _i("Light bulbs and command strips", "Renter safe. No holes means the deposit comes back."),
        ]),
        _sub("Furniture, hunted not bought", "Time this to CSU move-out in May and December and the whole list "
             "is roughly half price. Used route is $843 against $1,781 new.", [
            _i("Two desks", "$80 used. CSU dumps these every May and December."),
            _i("Desk chairs", "$50 used, same timing."),
            _i("Dining table", "$75. AFW starts at $199 new, Marketplace has sets at $75-125."),
            _i("Weight bench", "$50-80 used. The only gym item we do not already own."),
            _i("TV stand", "Under $40 at ARC or Habitat ReStore."),
            _i("Vacuum", "$30 minimum. Cat hair. Under $70 and you buy it twice."),
            _i("Auto cat litter box", "$179 Autoscooper does what a $699 Litter Robot does. Skip ScoopFree, the cartridges are $20-25/mo forever."),
            _i("RGB lights", "Her note. Govee is $25-40."),
        ]),
        _sub("First month, once we are in", "", [
            _i("Get on the Zoup! schedule, or better, find a job in Fort Collins", "$15.50 with a 10 minute drive beats $15.50 with a 40 mile one by $300/mo in fuel."),
            _i("Apply to all six staffing agencies the same week", "Then call the branch the next day."),
            _i("Book the Larimer County Workforce Center visit", "Ask for an Individual Training Account for CompTIA A+."),
            _i("Submit the Colorado DVR application", "Applying now buys queue position for free."),
            _i("Start the $300/mo house fund on autopay", "On payday, so it is never a decision."),
            _i("Three months of clean rent history", "Month 3 of the lease. This is mortgage ammunition."),
            _i("Wage conversation at Ritchey", "At the 90 day mark. Bring numbers, not feelings. Anchor at $26."),
            _i("Go out to eat twice a month, starting month one", "Budgets fail from austerity, not from a $50 dinner. The $100 is already in the Costs tab."),
        ]),
    ]),
    _c("Open questions", "Things that are genuinely undecided. Not a to-do list, a decide-list. "
       "Delete each one as it gets answered.", [
        _sub("Money", "", [
            _i("Is a roommate actually on the table?", "Earnings row 9 is a placeholder at 0 / 700 / 1,600. It is the single biggest number in the plan, so it matters whether it is real."),
            _i("Do we split Eating Out, Social and Emergency 50/50?", "They currently sit in both Mine and Hers, which double counts them."),
            _i("Add a health insurance premium line?", "Both on our fathers' plans until 26, so it is $0 today. The Ritchey plan is $80-250 pre-tax as a fallback."),
            _i("Confirm the phone device balance", "About $800 left, so ~$33/mo over two years on top of the $22 service."),
        ]),
        _sub("Housing", "", [
            _i("Duplex or single family?", "901-903 W Kelly Dr is the only address that stacks three advantages: duplex, in-zone, 307 days on market and possibly assumable."),
            _i("Does Aaliyah go on the loan?", "It roughly doubles buying power and it puts her on a 30-year note at 18. She cannot come off without a full refinance."),
            _i("Ask both assumable listings for the loan payoff balance", "The cash gap is the number that decides everything, and it is the FIRST question, before condition."),
        ]),
    ]),
]
