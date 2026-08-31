# -*- coding: utf-8 -*-
"""Assembles the five-section app."""
import json, os, sys, csv
sys.path.insert(0,'.')
from app_core import APP_CORE
from app_views1 import APP_VIEWS1
from app_views2 import APP_VIEWS2
from app_wire import APP_WIRE
from spa_css import APP_CSS
from ingredient_list import AISLES
import prices as PR

OUT="/mnt/user-data/outputs"

def aisle_of(k):
    for n,ks in AISLES:
        if k in ks: return n
    return "Other"

def build(DATA, ING):
    recipes=[]
    for d in DATA:
        r=d["r"]; p=d["per"]
        w,ws,_=PR.cost_of(r,r["servings"],"walmart")
        c,cs,_=PR.cost_of(r,r["servings"],"costco")
        recipes.append({"id":r["id"],"n":r["name"],"cat":r["cat"],"sv":r["servings"],
            "t":d["time"],"diff":d["diff"],"k":round(p["kcal"]),"p":round(p["p"],1),
            "c":round(p["c"],1),"f":round(p["f"],1),"fib":round(p["fib"],1),
            "leu":round(p["leu"],2),"tg":d["tags"],
            "cw":round(w,2),"cws":round(ws,2),"cc":round(c,2),"ccs":round(cs,2),
            "ing":[[m,k,g] for k,g,m in r["ing"]],
            "st":r["steps"],"storage":r.get("storage",""),"prep":r.get("prep_notes",""),
            "subs":r.get("subs",[]),"vars":r.get("variations",[])})
    ings={}
    for k,v in ING.items():
        pr=PR.PRICE.get(k,(None,None))
        ings[k]={"n":v["name"],"a":aisle_of(k),"w":pr[0],"c":pr[1],
                 "k":v["kcal"],"p":v["p"],"cb":v["c"],"f":v["f"],"fib":v["fib"]}
    blob={"recipes":recipes,"ing":ings,
          "aisles":[[a,k] for a,k in AISLES],
          "learn":[],
          "exercises":json.load(open("exercises.json")),
          "sessions":json.load(open("sessions.json")),
          "costs":json.load(open("costs.json")),
          "jobs":json.load(open("jobs.json"))}
    data_js="window._DATA="+json.dumps(blob,separators=(",",":"))+";\n"
    js=("<script>\n(function(){\n'use strict';\nvar _D=window._DATA;\n"
        +APP_CORE+APP_VIEWS1+APP_VIEWS2+APP_WIRE+"\n})();\n</script>")
    shell=('<!DOCTYPE html><html lang="en" data-theme="dark"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<meta name="theme-color" content="#0B0C0E">'
      '<title>The Handbook</title>'
      '<meta name="description" content="Meals, training, shopping, money and schedule for two people.">'
      '<meta name="apple-mobile-web-app-capable" content="yes">'
      '<meta name="apple-mobile-web-app-title" content="Handbook">'
      '<link rel="icon" href="data:image/svg+xml,'
      "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
      "%3Crect width='100' height='100' rx='22' fill='%230B0C0E'/%3E"
      "%3Ccircle cx='38' cy='52' r='17' fill='none' stroke='%23C2A24B' stroke-width='4'/%3E"
      "%3Cpath d='M64 33v38M72 33v11a4 4 0 004 4v23M80 33v38' stroke='%23C2A24B' "
      "stroke-width='4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E\">"
      +APP_CSS+'</head><body>'
      '<header class="top"><div class="topin">'
      '<div class="brand">The <em>Handbook</em></div>'
      '<div class="whoswitch" id="who"></div>'
      '<nav class="tabs" id="tabs"></nav>'
      '<button class="iconbtn" id="themeBtn" title="Theme"></button>'
      '<button class="iconbtn" id="settings" title="Settings"></button>'
      '</div></header><main class="wrap" id="view"></main>'
      '<nav class="btmnav" id="btm"></nav>'
      '<script>'+data_js+'</script>'+js+'</body></html>')
    open(f"{OUT}/handbook.html","w",encoding="utf-8").write(shell)
    # also return the split pieces so the repo builder can write real asset files
    css = APP_CSS.replace("<style>","",1).replace("</style>","",1).strip()
    js_only = (APP_CORE+APP_VIEWS1+APP_VIEWS2+APP_WIRE)
    return {"bytes":len(shell),"recipes":len(recipes),"ings":len(ings),
            "ex":len(blob["exercises"]),"sess":len(blob["sessions"]),
            "css":css,"js":js_only,"blob":blob}
