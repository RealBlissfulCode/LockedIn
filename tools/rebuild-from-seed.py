# -*- coding: utf-8 -*-
"""Rebuild the household's real data as a file the app can load.

Sources are the files the product rewrite deleted, recovered out of git:
costs.json, jobs.json and private_seed.py. Everything gets brought forward to
the current shape: two members with ids, rows tagged with those ids, and the
cost sections mapped onto the ones that replaced them.
"""
import json, random, re, string, sys
sys.path.insert(0, '/tmp/recover')
import private_seed as SEED

def uid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))

JARON = uid()
AALIYAH = uid()
WHO = {'Jaron': JARON, 'Aaliyah': AALIYAH, 'Both': 'all'}

# The same mapping the app applies on load, done here so the file arrives correct.
# Whole words, in this order. Substring matching put Emergency Funds under Fun.
LIVING = [
    (r'savings?|emergency fund\w*|retirement|sinking fund\w*', 'Saving'),
    (r'groceries|grocery|food|eating out|restaurant|coffee', 'Food'),
    (r'fuel|petrol|cars?|vehicle|transit|parking|registration|tags', 'Getting around'),
    (r'gym|doctor|dental|dentist|medical|prescriptions?|therapy|eye|orthodontic\w*', 'Health'),
    (r'pets?|dogs?|cats?|child|children|childcare|daycare', 'People and pets'),
    (r'phone|mobile|cell|internet|broadband|electric\w*|water|sewer|trash', 'Utilities'),
    (r'social|fun|hobby|hobbies|travel|holiday|gifts?|birthdays?|night out|going out', 'Fun'),
    (r'debt|loans?|credit cards?|student loans?', 'Debt'),
]
DIRECT = {'Housing (rent)': 'Home (renting)', 'Housing (buy)': 'Home (buying)',
          'Utilities': 'Utilities', 'Health': 'Health', 'Debt': 'Debt', 'Savings': 'Saving'}

def section_for(sec, name):
    if sec in DIRECT:
        return DIRECT[sec]
    if sec == 'Living':
        low = (name or '').lower()
        for pattern, dest in LIVING:
            if re.search(r'\b(?:' + pattern + r')\b', low):
                return dest
        return 'Personal'
    return 'Personal'

costs = json.load(open('/tmp/recover/costs.json'))
jobs = json.load(open('/tmp/recover/jobs.json'))

state = {
    'v': 7, 'who': JARON, 'theme': 'dark', 'savedAt': None,
    'household': "Jaron and Aaliyah",
    'members': [
        {'id': JARON, 'name': 'Jaron', 'sex': 'm', 'w': 150, 'h': 68, 'age': 20,
         'bf': 20, 'act': 1.55, 'goal': 1.09, 'pf': 1.1, 'accent': ''},
        {'id': AALIYAH, 'name': 'Aaliyah', 'sex': 'f', 'w': 120, 'h': 66.5, 'age': 20,
         'bf': 24, 'act': 1.45, 'goal': 1.0, 'pf': 0.8, 'accent': ''},
    ],
    'ingOv': {}, 'fav': [], 'lists': {}, 'mine': [], 'photos': {},
    'shop': {'active': 'Weekly shop',
             'lists': {'Weekly shop': {'cat': 'Groceries', 'fav': True, 'items': []}}},
    'days': {},
    'fin': {
        'jobs': [{'id': uid(), 'who': WHO.get(j['who'], 'all'), 'name': j['name'],
                  'employer': j.get('employer', ''), 'title': j.get('title', ''),
                  'rate': None, 'low': j['low'], 'real': j['real'], 'high': j['high'],
                  'actual': None, 'off': False} for j in jobs],
        'costs': [{'id': uid(), 'name': c['name'],
                   'section': section_for(c['section'], c['name']),
                   'who': WHO.get(c['who'], 'all'),
                   'low': c['low'], 'real': c['real'], 'high': c['high'],
                   'actual': c.get('exact') or c.get('researched') or None,
                   'off': False} for c in costs],
        'shifts': [], 'actuals': [], 'scenarios': {},
        'purchases': {}, 'strategies': {},
        'costMode': 'real', 'path': 'rent', 'activeScenario': None, 'draft': None,
    },
    'plan': {'cols': []},
    'sched': {'tmpl': {}, 'cols': []},
    'exLog': {}, 'prefs': {}, 'onboarded': True,
    'seeded': True, 'seeded6': True, '__sections7': True,
}

for n, L in SEED.PURCHASES.items():
    state['fin']['purchases'][n] = {
        'cat': L.get('cat', ''), 'note': L.get('note', ''),
        'items': [{'id': uid(), 'name': it['name'], 'price': it.get('price'),
                   'link': it.get('link', ''), 'notes': it.get('notes', ''),
                   'fields': it.get('fields', {})} for it in L.get('items', [])]}

for n, L in SEED.STRATEGIES.items():
    state['fin']['strategies'][n] = {
        'note': L.get('note', ''),
        'items': [{'id': uid(), 'name': it['name'], 'low': it.get('low'),
                   'real': it.get('real'), 'high': it.get('high'),
                   'rate': it.get('rate', ''), 'effort': it.get('effort', ''),
                   'when': it.get('when', ''), 'status': it.get('status', ''),
                   'how': it.get('how', '')} for it in L.get('items', [])]}

for c in SEED.PLANNING:
    state['plan']['cols'].append({
        'id': uid(), 'name': c['name'], 'note': c.get('note', ''),
        'subs': [{'id': uid(), 'name': s['name'], 'note': s.get('note', ''),
                  'items': [{'id': uid(), 'text': i['text'], 'note': i.get('note', ''),
                             'done': False} for i in s.get('items', [])]}
                 for s in c.get('subs', [])]})

out = {'app': 'lockedin', 'version': 7,
       'exported': '2026-09-04T00:00:00Z',
       'note': 'Rebuilt from costs.json, jobs.json and private_seed.py',
       'state': state}
json.dump(out, open('/tmp/lockedin-restore.json', 'w'), indent=1)

sec = {}
for c in state['fin']['costs']:
    sec[c['section']] = sec.get(c['section'], 0) + 1
print('members   ', [m['name'] for m in state['members']])
print('income    ', len(state['fin']['jobs']), 'lines')
print('costs     ', len(state['fin']['costs']), 'lines across', len(sec), 'sections')
for k, v in sorted(sec.items(), key=lambda x: -x[1]):
    print('            %-16s %d' % (k, v))
print('purchases ', {k: len(v['items']) for k, v in state['fin']['purchases'].items()})
print('strategies', sum(len(v['items']) for v in state['fin']['strategies'].values()),
      'across', len(state['fin']['strategies']), 'tiers')
print('planning  ', [(c['name'], sum(len(s['items']) for s in c['subs'])) for c in state['plan']['cols']])
