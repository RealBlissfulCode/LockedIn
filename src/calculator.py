# -*- coding: utf-8 -*-
"""Live calculator. HTML only. Degrades to a static note in print."""

CALCULATOR = """
<h2 id="live">Live calculator</h2>
<p>Change any input and every number below moves with it. Printed, it shows the defaults and I
run the arithmetic from the formula pages that follow.</p>

<div class="calcwrap" id="calcwrap">
  <div class="calcinputs">
    <label>Body weight <input type="number" id="ciW" value="150" step="1"> lb</label>
    <label>Height <input type="number" id="ciH" value="68" step="0.5"> in</label>
    <label>Age <input type="number" id="ciA" value="20" step="1"> yrs</label>
    <label>Sex
      <select id="ciSex"><option value="m" selected>Male</option><option value="f">Female</option></select>
    </label>
    <label>Body fat <input type="number" id="ciBF" value="20" step="0.5"> %</label>
    <label>Activity
      <select id="ciAct">
        <option value="1.15">1.15 Bedbound</option>
        <option value="1.20">1.20 Fully sedentary desk job</option>
        <option value="1.30">1.30 Desk job plus training</option>
        <option value="1.40">1.40 Light standing work plus training</option>
        <option value="1.50">1.50 Bench or shop work plus training</option>
        <option value="1.55" selected>1.55 Engraving shop plus daily training</option>
        <option value="1.62">1.62 On feet all shift plus training</option>
        <option value="1.70">1.70 Very active, light trade work</option>
        <option value="1.80">1.80 Trade work plus daily training</option>
        <option value="1.90">1.90 Heavy labour plus training</option>
        <option value="2.10">2.10 Athlete in camp</option>
        <option value="2.40">2.40 Extreme endurance</option>
      </select>
    </label>
    <label>Goal
      <select id="ciGoal">
        <option value="0.70">Aggressive cut (-30%)</option>
        <option value="0.78">Standard cut (-22%)</option>
        <option value="0.85">Conservative cut (-15%)</option>
        <option value="0.75">Mini cut (-25%)</option>
        <option value="1.00">Maintenance / diet break</option>
        <option value="1.02">Maingaining (+2%)</option>
        <option value="1.03">Underfed recomp (+3%)</option>
        <option value="1.06">Conservative lean gain (+6%)</option>
        <option value="1.09" selected>Standard lean gain (+9%)</option>
        <option value="1.15">Moderate bulk (+15%)</option>
        <option value="1.20">Aggressive bulk (+20%)</option>
        <option value="1.05">Performance block (+5%)</option>
        <option value="0.92">Deload / flare week (-8%)</option>
      </select>
    </label>
    <label>Protein factor
      <select id="ciP">
        <option value="0.7">0.7 g/lb Recreational</option>
        <option value="0.9">0.9 g/lb Standard lifter</option>
        <option value="1.1" selected>1.1 g/lb Plant-heavy gain</option>
        <option value="1.25">1.25 g/lb In a deficit</option>
        <option value="1.4">1.4 g/lb Aggressive cut</option>
      </select>
    </label>
    <label>Fat setting
      <select id="ciF">
        <option value="0.30">0.30 g/lb Floor</option>
        <option value="0.38">0.38 g/lb Cutting</option>
        <option value="0.45">0.45 g/lb Maintenance</option>
        <option value="pct25" selected>25% of calories</option>
        <option value="pct35">35% of calories</option>
      </select>
    </label>
    <label>Training today
      <select id="ciT">
        <option value="0">Rest day</option>
        <option value="60">60 min</option>
        <option value="75" selected>75 min</option>
        <option value="120">120 min</option>
        <option value="180">180 min</option>
      </select>
    </label>
  </div>

  <div class="calcout">
    <div class="cocard big"><span id="coKcal">2,800</span><em>calories / day</em></div>
    <div class="cocard"><span id="coP">162 g</span><em>protein</em></div>
    <div class="cocard"><span id="coC">365 g</span><em>carbs</em></div>
    <div class="cocard"><span id="coF">86 g</span><em>fat</em></div>
    <div class="cocard"><span id="coFib">43 g</span><em>fiber</em></div>
    <div class="cocard"><span id="coW">125 oz</span><em>water</em></div>
  </div>

  <table class="calcdetail">
    <tr><th>Derived value</th><th>Result</th><th>How</th></tr>
    <tr><td>RMR, Mifflin-St Jeor</td><td id="coRmrM">1,636</td><td>(10 x kg) + (6.25 x cm) - (5 x age) + 5</td></tr>
    <tr><td>RMR, Katch-McArdle</td><td id="coRmrK">1,595</td><td>370 + (21.6 x LBM kg)</td></tr>
    <tr><td>RMR, Cunningham</td><td id="coRmrC">1,747</td><td>500 + (22 x LBM kg)</td></tr>
    <tr><td>Maintenance (TDEE)</td><td id="coTdee">2,580</td><td>RMR x activity factor</td></tr>
    <tr><td>Lean body mass</td><td id="coLbm">120 lb</td><td>weight x (1 - body fat)</td></tr>
    <tr><td>Fat mass</td><td id="coFm">21 lb</td><td>weight x body fat</td></tr>
    <tr><td>FFMI (normalised)</td><td id="coFfmi">20.4</td><td>LBM kg / m squared, height-corrected</td></tr>
    <tr><td>Room to natural ceiling</td><td id="coRoom">4.6 points</td><td>25 normalised FFMI is the practical natural limit</td></tr>
    <tr><td>Weight at 10% body fat</td><td id="coGoalW">140 lb</td><td>LBM / (1 - 0.10)</td></tr>
    <tr><td>Expected weekly change</td><td id="coRate">+0.4 lb</td><td>surplus or deficit / 3,500</td></tr>
    <tr><td>Protein per feeding (x4)</td><td id="coPerMeal">41 g</td><td>daily protein / 4</td></tr>
    <tr><td>Leucine per feeding target</td><td id="coLeu">2.5-3.0 g</td><td>threshold for MPS in a trained male</td></tr>
    <tr><td>Energy availability</td><td id="coEa">44 kcal/kg</td><td>(intake - training kcal) / LBM kg. Under 30 is a problem.</td></tr>
    <tr><td>Thermic effect of food</td><td id="coTef">310 kcal</td><td>~10% of intake</td></tr>
    <tr><td>Training energy cost</td><td id="coEat">450 kcal</td><td>~6 kcal/min resistance work</td></tr>
    <tr><td>Creatine dose</td><td id="coCr">5 g</td><td>0.03 g/kg, rounded to the practical 5 g</td></tr>
    <tr><td>Caffeine, performance dose</td><td id="coCaf">200-400 mg</td><td>3-6 mg/kg. Start low.</td></tr>
    <tr><td>Muscle glycogen capacity</td><td id="coGly">1,001 g</td><td>~15 g/kg bodyweight</td></tr>
  </table>
  <p class="small">Ramp guidance: if my current intake is well below the target, add 250 to 300
  calories per week rather than jumping. Protein goes to target immediately.</p>
</div>

<script>
(function(){
  var ids=['ciW','ciH','ciA','ciBF','ciAct','ciGoal','ciP','ciF','ciT','ciSex'];
  function n(id){return parseFloat(document.getElementById(id).value);}
  function fmt(x){return Math.round(x).toLocaleString();}
  function set(id,v){var e=document.getElementById(id); if(e) e.textContent=v;}
  function calc(){
    var lb=n('ciW'), inch=n('ciH'), age=n('ciA'), bf=n('ciBF')/100;
    var act=n('ciAct'), goal=n('ciGoal'), pf=n('ciP'), tmin=n('ciT');
    var fsel=document.getElementById('ciF').value;
    var kg=lb*0.45359237, cm=inch*2.54, m=cm/100;
    var lbmKg=kg*(1-bf), lbmLb=lb*(1-bf);
    var sex=document.getElementById('ciSex').value;
    var rmrM=(10*kg)+(6.25*cm)-(5*age)+(sex==='f'?-161:5);
    var rmrK=370+(21.6*lbmKg);
    var rmrC=500+(22*lbmKg);
    var tdee=rmrM*act;
    var kcal=tdee*goal;
    var prot=lb*pf;
    var fat = (fsel==='pct25') ? kcal*0.25/9 : (fsel==='pct35') ? kcal*0.35/9 : lb*parseFloat(fsel);
    var carb=(kcal-(prot*4)-(fat*9))/4;
    var fib=kcal/1000*14;
    var water=(lb*0.6)+(tmin/60*25)+10;
    var ffmi=lbmKg/(m*m); var nffmi=ffmi+6.1*(1.8-m);
    var eat=tmin*6;
    var ea=(kcal-eat)/lbmKg;
    var rate=(kcal-tdee)*7/3500;
    set('coKcal',fmt(kcal));
    set('coP',fmt(prot)+' g'); set('coC',fmt(carb)+' g'); set('coF',fmt(fat)+' g');
    set('coFib',fmt(fib)+' g'); set('coW',fmt(water)+' oz');
    set('coRmrM',fmt(rmrM)); set('coRmrK',fmt(rmrK)); set('coRmrC',fmt(rmrC));
    set('coTdee',fmt(tdee));
    set('coLbm',fmt(lbmLb)+' lb'); set('coFm',fmt(lb-lbmLb)+' lb');
    set('coFfmi',nffmi.toFixed(1));
    set('coRoom',(25-nffmi).toFixed(1)+' points');
    set('coGoalW',fmt(lbmLb/0.90)+' lb');
    set('coRate',(rate>=0?'+':'')+rate.toFixed(2)+' lb');
    set('coPerMeal',fmt(prot/4)+' g');
    set('coEa',fmt(ea)+' kcal/kg'+(ea<30?'  LOW':''));
    set('coTef',fmt(kcal*0.10)+' kcal');
    set('coEat',fmt(eat)+' kcal');
    set('coCr',(kg*0.03).toFixed(1)+' g (use 5 g)');
    set('coCaf',fmt(kg*3)+'-'+fmt(kg*6)+' mg');
    set('coGly',fmt(kg*15)+' g');
  }
  ids.forEach(function(i){
    var e=document.getElementById(i);
    if(e){e.addEventListener('input',calc); e.addEventListener('change',calc);}
  });
  calc();
})();
</script>
"""

COVER = """
<div class="cover">
  <div class="coverinner">
    <div class="coverleft">
      <p class="eyebrow">Training &middot; Nutrition &middot; Recovery &nbsp;/&nbsp; August 2026</p>
      <h1>The Meal<br>Handbook</h1>
      <p class="subtitle">My food system. All gluten-free, all worked out in grams, built around
      one problem: getting 2,800 calories a day down without it running my life.</p>
      <div class="coverstats">
        <div><b>{n}</b><span>Recipes</span></div>
        <div><b>{ing}</b><span>Ingredients</span></div>
        <div><b>15</b><span>Collections</span></div>
        <div><b>100%</b><span>Gluten-free</span></div>
      </div>
      <p class="coverfoot">Breakfast, mains, snacks, drinks, and clean meat and fish kept in its own
      section. Plus the calculator, the grocery rotation and the full ingredient reference.</p>
    </div>

    <div class="coverright">
      <p class="panelhead">Inside</p>
      <ol class="panel">
        <li><a href="#howto"><em>01</em> Start here</a></li>
        <li><a href="#household"><em>02</em> Cooking for two</a></li>
        <li><a href="#app"><em>03</em> The kitchen app</a></li>
        <li><a href="#live"><em>04</em> Live calculator</a></li>
        <li><a href="#calc"><em>05</em> The calculation engine</a></li>
        <li><a href="#targets"><em>06</em> My numbers</a></li>
        <li><a href="#protein"><em>05</em> Protein, EAAs and leucine</a></li>
        <li><a href="#micros"><em>06</em> Micronutrients</a></li>
        <li><a href="#goals"><em>07</em> Gain, cut and recomp</a></li>
        <li><a href="#collections"><em>08</em> Collections</a></li>
        <li><a href="#grocery-rotation"><em>09</em> Grocery rotation</a></li>
        <li><a href="#ingredients"><em>10</em> Ingredient reference</a></li>
        <li><a href="#library"><em>11</em> The recipes</a></li>
      </ol>
      <div class="panelnums">
        <div><b>2,800</b><span>kcal / day</span></div>
        <div><b>1,900</b><span>her kcal</span></div>
        <div><b>365 g</b><span>carbs</span></div>
        <div><b>$2.13</b><span>avg / serving</span></div>
      </div>
    </div>
  </div>
</div>
"""
