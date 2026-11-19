#!/usr/bin/env python3
"""Build /guides/sidewall-cracks/ (19 Nov 2026). Every claim maps to a source opened 19 Nov 2026.
Reuses the head, nav and footer pattern of _which_tire_20261116.py. No branded model is recommended."""
import json, re
from pathlib import Path
import importlib.util
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("wt", ROOT / "_which_tire_20261116.py"); wt = importlib.util.module_from_spec(spec); spec.loader.exec_module(wt)
esc, SRC, DISC, FOOT, BASE = wt.esc, dict(wt.SRC), wt.DISC, wt.FOOT, wt.BASE
SRC.update({
 "MSP": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/sidewall-problems", "Michelin, Sidewall Problems (updated October 18, 2026)"),
 "MNEW": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/when-do-i-need-new-tires", "Michelin, When to Replace Tires (updated November 12, 2026)"),
 "MREP": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-maintenance/can-my-tire-be-repaired", "Michelin, Can My Tire Be Repaired?"),
 "CREP": ("https://www.continental-tires.com/tire-knowledge/replacing-tires/", "Continental, When to replace your tires"),
})
def a(k, text): return f'<a href="{SRC[k][0]}" rel="noopener noreferrer" target="_blank">{text}</a>'
NAV = wt.NAV.replace('<li><a href="/guides/">Guides</a></li>', '<li><a href="/guides/" aria-current="page">Guides</a></li>').format(wt='')
PUB, PUB_H, READ = "2026-11-19", "November 19, 2026", "read 19 November 2026"
SLUG = "sidewall-cracks"; URL = f"{BASE}/guides/{SLUG}/"
STEM, ALT = "tire-inspection-hoist", "Mechanic seen from behind under a car raised on a shop lift, with its tires and wheels in view"
TITLE = "Tire sidewall cracks: fine checking means inspect, deep cracks mean replace"
H1 = "Tire sidewall cracks: when do you have to replace the tire?"
DESC = "Fine surface cracks are aging: get the tire inspected. Cracks that are deep, numerous, open when flexed or reach the cords mean replace. No repair exists."
assert len(DESC) <= 155, len(DESC)
LEDE = "Fine, shallow cracks on the sidewall (weather checking) are a sign the rubber is aging, so have the tire inspected and check its date code. Replace the tire if the cracks are deep or numerous, open up when the tire flexes, or reach the cords. Sidewall cracks cannot be repaired, and tire dressing does not fix them."
faqs = [
 ("Are small cracks in tire sidewalls normal?", "They are common on older tires, but they are a warning, not a cosmetic quirk. Michelin says fine surface cracking is a sign of age related rubber oxidation and ozone exposure; if the cracks are fine and shallow they indicate age but may not be an immediate safety issue. Have the tire inspected and check how old it is."),
 ("When are sidewall cracks bad enough to replace the tire?", "Michelin says replace the tire if the cracks open visibly when the tire is flexed, or if they are deep or numerous. USTMA says tires with severe weather checking or ozone cracking, or any cracking that extends to the casing cords or plies, should be removed from service."),
 ("Can a cracked sidewall be patched or plugged?", "No. Michelin says sidewall damage cannot be repaired, and its repair criteria limit repairs to punctures in the tread area no larger than 1/4 inch (6 mm), done with a combined plug and inside patch with the tire off the wheel. See our <a href=\"/guides/puncture-repair-or-replace/\">puncture repair or replace</a> guide."),
 ("Will tire shine or dressing fix dry rot?", "No. Nothing in the maker or USTMA guidance treats a dressing as a repair. USTMA actually warns that incompatible dressings or harsh cleaning agents hasten oxidation and cause premature cracking, and says to always avoid petroleum based tire dressings and cleaners."),
 ("Is a 10 year old tire safe if it has no cracks?", "Michelin and Continental both say to replace tires ten years after manufacture, including the spare, whatever they look like. Continental adds that drivers cannot rely on a visual check to spot age related deterioration. Michelin recommends a yearly professional inspection once a tire has been in service five years."),
 ("What causes sidewall cracking?", "USTMA lists ozone and heat from sunlight, and ozone from sources such as electric motors and welding equipment. It says excessive cracking is typically caused by under inflation, overloading, improper storage or improper long term parking. NHTSA adds that infrequent use, sunlight, warmer climates and poor storage contribute to tire aging."),
 ("Should I check the spare tire for cracks too?", "Yes. Michelin says spares sit out of sight for years and can develop age related cracking, and that a spare with visible sidewall cracking, or one past ten years from its manufacture date, should be replaced. NHTSA notes that spare tires are prone to aging because they are seldom replaced."),
 ("Do I need to replace all four tires if one has cracks?", "Not automatically. Cracking usually comes from age and storage, so tires of the same age often show it together; have all of them inspected. If you replace only some, follow the rules for <a href=\"/guides/mixing-tires/\">mixing tires and replacing two or four</a>, and the owner's manual on AWD vehicles."),
]
srcs = [("MSP", "fine vs deep cracking, cracks that open when flexed, spare tires, antiozonant browning"),
        ("MNEW", "sidewall cuts, cracks and bulges, no sidewall repair, five year inspection, ten year limit"),
        ("MREP", "repair criteria: tread area only, 1/4 inch maximum, plug and patch off the wheel"),
        ("CS", "ozone cracking causes, removal from service, dressings, inspection, service life"),
        ("NT", "tire aging causes, cracks as a reason to stop using a tire, DOT date code, spares"),
        ("CREP", "ten year limit including spares, visual checks are not enough")]
related = [("/guides/sidewall-bulge/", "Sidewall bulge: is it safe to drive?"), ("/guides/dot-date-codes/", "How old are my tires? Read the DOT date code"),
           ("/guides/how-long-do-tires-last/", "How long do tires last?"), ("/guides/when-to-replace/", "When to replace tires"),
           ("/guides/seasonal-tire-storage/", "How to store tires"), ("/guides/how-to-choose-replacement-tires/", "How to choose replacement tires"), ("/which-tire/", "Which tire picker")]
body = f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>{LEDE} Everything below comes from Michelin, Continental, USTMA and NHTSA pages we opened for this guide. A tire professional who can see the tire, inside and out, makes the final call.</p>
      </section>
      <section class="content-section" id="fine-or-deep">
        <h2>Fine weather checking or deep cracks?</h2>
        <p>Michelin's sidewall FAQ draws the line on depth and spread. Fine surface cracking across the sidewall is age related rubber oxidation and ozone exposure, common on older tires; fine, shallow cracks indicate age but may not be an immediate safety issue. Cracks that open visibly when the tire flexes, or that are deep or numerous, mean the tire has degraded past safe use and should be replaced ({a('MSP','Michelin, Sidewall Problems')}). USTMA's service manual is just as direct: tires with severe weather checking or ozone cracking, or any cracking that reaches the casing cords or plies, should be removed from service ({a('CS','USTMA Care and Service')}).</p>
        <table>
          <thead><tr><th>What you see</th><th>What the sources say</th></tr></thead>
          <tbody>
            <tr><td>Fine, shallow surface lines</td><td>Age related oxidation and ozone exposure; may not be an immediate safety issue. Get it inspected and check the date code ({a('MSP','Michelin')})</td></tr>
            <tr><td>Cracks that open when the tire flexes</td><td>Replace ({a('MSP','Michelin')})</td></tr>
            <tr><td>Deep or numerous cracks</td><td>Replace ({a('MSP','Michelin')}); severe weather checking means remove from service ({a('CS','USTMA')})</td></tr>
            <tr><td>Cracks down to the cords or plies</td><td>Remove from service ({a('CS','USTMA')})</td></tr>
            <tr><td>Bulge, bubble or cut</td><td>Not a crack problem: replace. See <a href="/guides/sidewall-bulge/">sidewall bulge</a> ({a('MSP','Michelin')})</td></tr>
            <tr><td>Brown film on the sidewall</td><td>Michelin's sidewall tool treats antiozonant browning as a normal feature, not damage ({a('MSP','Michelin')})</td></tr>
          </tbody>
        </table>
        <p>Michelin's replacement guide also lists cuts, cracks, bulges or blisters on the sidewall as possible signs of structural damage, says sidewall damage cannot be repaired, and says any tire with visible sidewall damage should be inspected right away by a trained tire professional ({a('MNEW','Michelin, When to Replace Tires')}). NHTSA counts cracks with cuts and bulges among the signs that a tire should no longer be used ({a('NT','NHTSA TireWise')}).</p>
      </section>
      <section class="content-section" id="age">
        <h2>Check how old the tire is</h2>
        <p>Cracking and age go together, so read the date before deciding. NHTSA says the last four digits of the DOT Tire Identification Number give the week and year the tire was made (0308 means the third week of 2008), and that the full number may be on only one side, so look at both ({a('NT','NHTSA')}). Our <a href="/guides/dot-date-codes/">DOT date code guide</a> walks through it.</p>
        <ul>
          <li><b>Five years:</b> Michelin recommends a thorough inspection by a trained tire professional at least once a year after five years of service ({a('MNEW','Michelin')}).</li>
          <li><b>Ten years:</b> Michelin recommends replacing tires ten years after their date of manufacture regardless of tread or condition, spares included ({a('MNEW','Michelin')}). Continental says all tires, including spares, more than ten years old should be removed from service, and that drivers cannot depend on a visual check for age related deterioration ({a('CREP','Continental')}).</li>
          <li><b>Six to ten years:</b> NHTSA notes that some vehicle and tire makers recommend replacing tires that are six to ten years old regardless of treadwear ({a('NT','NHTSA')}).</li>
          <li><b>Your vehicle maker:</b> Continental says some vehicle makers set a different age and drivers should follow it ({a('CREP','Continental')}). USTMA says no scientific data sets a specific minimum or maximum service life, so a maker's recommendation should not be treated as a minimum ({a('CS','USTMA')}).</li>
        </ul>
        <p>Age limits work one way only: a crack bad enough to replace is a reason to replace on a two year old tire too. More on lifespan in <a href="/guides/how-long-do-tires-last/">how long do tires last</a>.</p>
      </section>
      <section class="content-section" id="causes">
        <h2>Why tires crack before the tread wears out</h2>
        <p>USTMA says weather checking and ozone cracking come from direct and extended exposure to ozone and heat from sunlight, and ozone can also come from electric motors, welding equipment and other ozone generating sources. It says excessive cracking on the tread or sidewall is typically caused by under inflation, overloading, improper storage or improper long term parking ({a('CS','USTMA')}).</p>
        <p>NHTSA says the vehicles most at risk from aging are the ones that are not driven much: RVs, 15 passenger vans, collector cars and other low mileage vehicles. It adds sunlight, warmer climates, poor storage and poor maintenance as factors, and says aging is a greater concern in the southern Sun Belt states ({a('NT','NHTSA')}). That is why a garage queen with deep tread can need tires sooner than a commuter car.</p>
      </section>
      <section class="content-section" id="repair">
        <h2>Can cracks be repaired?</h2>
        <p>No. Michelin's repair criteria allow a repair only when the damage is in the tread area, the puncture is no larger than 1/4 inch (6 mm) and the tire was not driven flat, and it says sidewall damage ruins a tire immediately ({a('MREP','Michelin')}). There is no patch, sealant or glue for a cracked sidewall. The full repair rules are in <a href="/guides/tire-plug-vs-patch/">plug vs patch</a>.</p>
        <p>Do not rely on tire shine to hide cracks either. USTMA warns that incompatible dressings or harsh cleaning agents hasten oxidation and cause premature cracking, and says to always avoid petroleum based tire dressings and cleaners ({a('CS','USTMA')}).</p>
      </section>
      <section class="content-section" id="check">
        <h2>How to check your sidewalls</h2>
        <ul>
          <li><b>Monthly:</b> USTMA says to look at the tread and sidewalls during monthly pressure checks for cuts, cracks, scrapes, snags, bulges and foreign objects, and to have the tires, spare included, inspected by a tire professional at routine services such as oil changes and rotations ({a('CS','USTMA')}).</li>
          <li><b>Both sides:</b> check the inner sidewall as well as the outer one; the date code may only be on one side ({a('NT','NHTSA')}).</li>
          <li><b>The spare:</b> Michelin says a spare with visible sidewall cracking or older than ten years should be replaced ({a('MSP','Michelin')}).</li>
          <li><b>Pressure:</b> set to the door placard, since under inflation is one of the causes USTMA lists. See <a href="/guides/tire-pressure/">tire pressure</a>.</li>
          <li><b>Stored tires:</b> keep them away from sun and ozone sources; our <a href="/guides/seasonal-tire-storage/">tire storage guide</a> has the details.</li>
        </ul>
        <p>If a tire with deep cracks, a bulge or exposed cords is on the car, Michelin's advice is not to drive on it: fit the spare and have the damaged tire assessed ({a('MSP','Michelin')}). When it is time for new ones, start with <a href="/guides/how-to-choose-replacement-tires/">how to choose replacement tires</a> or the <a href="/which-tire/">which tire picker</a>.</p>
      </section>
"""
crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Guides","item":BASE+"/guides/"},{"@type":"ListItem","position":3,"name":"Tire sidewall cracks","item":URL}]
org = {"@type":"Organization","@id":BASE+"/#organization","name":"Smart Tire Picks"}
og = f"{BASE}/assets/img/og-{STEM}.jpg"
art = {"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":og,"datePublished":PUB,"dateModified":PUB,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":"Smart Tire Picks"},"citation":[SRC[k][0] for k,_ in srcs]}
strip = lambda s: re.sub(r"<[^>]+>", "", s)
faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(x)}} for q,x in faqs]}
ld = lambda o: '  <script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + '\n  </script>\n'
fq = "\n".join(f"        <details>\n          <summary>{esc(q)}</summary>\n          <p>{x}</p>\n        </details>" for q,x in faqs)
sl = "\n".join(f'          <li><a href="{SRC[k][0]}" rel="noopener noreferrer" target="_blank">{esc(SRC[k][1])}</a>: {esc(why)} ({READ})</li>' for k,why in srcs)
rl = "\n".join(f'          <li><a href="{h}">{esc(t)}</a></li>' for h,t in related)
src = (ROOT / "_replacement_guide_20261117.py").read_text()
tmpl = src[src.index('out = f"""'):src.index('p = ROOT / "guides" / SLUG')]
tmpl = tmpl.replace("› How to choose replacement tires</p>", "› Tire sidewall cracks</p>")
assert "› Tire sidewall cracks</p>" in tmpl
exec(tmpl)
p = ROOT / "guides" / SLUG / "index.html"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(out + "\n")
print(URL)
