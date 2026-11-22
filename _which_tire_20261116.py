#!/usr/bin/env python3
"""Build the /which-tire/ hub and first batch of 'Which tire for X' pages (16 Nov 2026). Idempotent: rewrites only which-tire/**.
Every factual claim maps to a source opened on 16 Nov 2026 (SRC below). No branded model is recommended."""
import json, html, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PUB = "2026-11-16"; PUB_H = "November 16, 2026"; READ = "read 16 November 2026"
PAGE_DATES = {"2026-11-16": (PUB, PUB_H, READ), "2026-11-17": ("2026-11-17", "November 17, 2026", "read 17 November 2026"), "2026-11-19": ("2026-11-19", "November 19, 2026", "read 19 November 2026")}
BASE = "https://smarttirepicks.com"

SRC = {
 "CS": ("https://www.ustires.org/system/files/files/2024-05/Care%20and%20Service%20Passenger%20and%20Light%20Truck%20Tires%20FINAL%2006%2028%2017.pdf", "USTMA, Care and Service of Passenger and Light Truck Tires"),
 "T37": ("https://www.ustires.org/system/files/2026-04/TISB_37_v7_December%202020.pdf", "USTMA, TISB 37: Definition for passenger and light truck tires for use in severe snow conditions"),
 "T54": ("https://www.ustires.org/sites/default/files/2024-08/TISB%2054%20No%202.pdf", "USTMA, TISB 54: High Load Capacity (HL) passenger tires"),
 "ECFR": ("https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-575/subpart-B/section-575.104", "eCFR, 49 CFR 575.104 Uniform tire quality grading standards"),
 "NWIN": ("https://www.nhtsa.gov/winter-driving-tips", "NHTSA, Winter Weather Driving Tips"),
 "NTOW": ("https://dmna.ny.gov/nynm/training/NHTSA%5FTowingSafety.pdf", "NHTSA, Towing a Trailer: Being Equipped for Safety (DOT HS 809 433, copy hosted by New York DMNA)"),
 "MTY": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/differences-in-types-of-seasonal-tires", "Michelin, Differences in types of seasonal tires"),
 "MSW": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/summer-winter-all-season-tires", "Michelin, Summer vs. Winter vs. All Season Tires"),
 "MHL": ("https://www.michelinman.com/auto/auto-tips-and-advice/electric-mobility-guide/tires-rated-for-high-load-capacity", "Michelin, High Load Capacity tires"),
 "MEV": ("https://www.michelinman.com/auto/electric-vehicles-faq", "Michelin, Electric vehicle tire FAQ"),
 "CEV": ("https://www.continental-tires.com/tire-knowledge/electric-vehicle-tires/", "Continental, Electric vehicle tires"),
 "TRC": ("https://www.tirerack.com/tires/tests/breaking-down-tire-performance-categories?ttid=333", "Tire Rack, Breaking Down Tire Performance Categories (2024 test with winter update)"),
 "TRH": ("https://www.tirerack.com/tires/tests/testDisplay.jsp?ttid=210", "Tire Rack, Highway All Season or On/Off Road All Terrain: testing the differences on paved roads (2015)"),
 "TRT": ("https://www.tirerack.com/tires/truck", "Tire Rack, Truck and SUV tires category page and FAQ"),
 "BFG": ("https://www.bfgoodrichtires.com/auto/learn/4x4-driving-guide/tire-selection", "BFGoodrich, 4x4 driving guide: tire selection"),
 "MCS": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/change-size-spec", "Michelin, Changing tire size or specifications"),
 "NT": ("https://www.nhtsa.gov/vehicle-safety/tires", "NHTSA, Tire Safety Ratings and Awareness (TireWise)"),
 "TRA": ("https://www.tirerack.com/tires/all-season", "Tire Rack, Touring and all season tire categories"),
 "MPH": ("https://www.michelinman.com/auto/auto-tips-and-advice/electric-mobility-guide/plug-in-hybrid-vehicle", "Michelin, How to select the best tires for your plug in hybrid (updated July 20, 2026)"),
 "MOE": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/michelin-developed-marked-tires", "Michelin, What are Michelin developed marked tires?"),
 "MSZ": ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/find-your-tire-size", "Michelin, Choosing the right tire size for your vehicle"),
 "FEG": ("https://www.fueleconomy.gov/feg/maintain.jsp", "FuelEconomy.gov (U.S. DOE and EPA), Keeping your vehicle in shape"),
}
def a(k, text): return f'<a href="{SRC[k][0]}" rel="noopener noreferrer" target="_blank">{text}</a>'
def esc(s): return html.escape(s, quote=True)

NAV = """        <ul>
          <li><a href="/which-tire/"{wt}>Which tire</a></li>
          <li><a href="/fitment/choose-tire-size/">Fitment</a></li>
          <li><a href="/reviews/michelin-crossclimate2/">Reviews</a></li>
          <li><a href="/comparisons/all-season-vs-winter/">Comparisons</a></li>
          <li><a href="/guides/">Guides</a></li>
          <li><a href="/about.html">About</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>"""
FOOT = Path(ROOT / "guides/lug-nut-torque/index.html").read_text()
FOOT = FOOT[FOOT.index("  <footer class=\"site-footer\">"):]
if '/which-tire/">Which tire' not in FOOT:
    FOOT = FOOT.replace('<li><a href="/fitment/choose-tire-size/">Fitment</a></li>', '<li><a href="/which-tire/">Which tire</a></li>\n            <li><a href="/fitment/choose-tire-size/">Fitment</a></li>', 1)
IMG = {  # existing site images, already in _content_rights.json
 "suv": ("review-allseason", "All season tire and alloy wheel of a crossover SUV on a wet country road"),
 "sedan": ("review-touring", "Sedan front tire and alloy wheel viewed from the side, the sidewall where size markings are molded"),
 "snow": ("winter-tires", "Car winter tire with packed snow in the tread on a snowy road"),
 "rain": ("home-hero", "Close up of a new passenger car tire tread covered in rain drops on wet asphalt"),
 "wheel": ("fitment-wheel", "Front wheel removed from a car on a lift in a workshop showing the brake rotor and caliper"),
 "pressure": ("tire-pressure", "Digital tire pressure gauge connected to the valve stem of a car wheel"),
}
DISC = '<aside class="disclaimer-box" role="note"><p><em>This page is for general information only and is not professional, safety, or legal advice. Always confirm tire size, load index, speed rating, and other specs against your vehicle’s door placard and owner’s manual, and have tires installed by a licensed professional. We have not lab tested products. See our <a href="/disclaimer/">Disclaimer</a>.</em></p></aside>'

def page(slug, title, h1, desc, lede, img, body, faqs, srcs, related, crumb, extra_head="", extra_tail="", pub=None):
    PUB, PUB_H, READ = PAGE_DATES.get(pub or "2026-11-16")
    url = f"{BASE}/which-tire/{slug}/" if slug else f"{BASE}/which-tire/"
    stem, alt = IMG[img]
    og = f"{BASE}/assets/img/og-{stem}.jpg"
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Which tire", "item": BASE + "/which-tire/"}]
    if slug: crumbs.append({"@type": "ListItem", "position": 3, "name": crumb, "item": url})
    org = {"@type": "Organization", "@id": BASE + "/#organization", "name": "Smart Tire Picks"}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "author": org, "publisher": org,
           "image": og, "datePublished": PUB, "dateModified": PUB, "inLanguage": "en-US",
           "isPartOf": {"@type": "WebSite", "@id": BASE + "/#website", "name": "Smart Tire Picks"}}
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(ans)}} for q, ans in faqs]}
    ld = lambda o: '  <script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + '\n  </script>\n'
    assert len(desc) <= 155, (slug, len(desc))
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Smart Tire Picks">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og}">
  <meta property="og:image:alt" content="{esc(alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{og}">
  <meta name="twitter:image:alt" content="{esc(alt)}">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/css/styles.css">
{ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs})}{ld(art)}{ld(faq)}{extra_head}<script src="/js/consent-analytics.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="/">Smart <span>Tire</span> Picks</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
{NAV.format(wt=' aria-current="page"')}
      </nav>
    </div>
  </header>
  <main id="main">
    <div class="wrap">
      <p class="note"><a href="/">Home</a> › <a href="/which-tire/">Which tire</a>{' › ' + esc(crumb) if slug else ''}</p>
      <h1 class="page-title">{esc(h1)}</h1>
<p class="lede">{lede}</p>
<p class="last-updated">Last updated: {PUB_H}</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/{stem}-1024.webp" srcset="/assets/img/{stem}-640.webp 640w, /assets/img/{stem}-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{esc(alt)}" fetchpriority="high" decoding="async"><figcaption>AI generated image. Source: <a href="/image-policy/">Image policy</a>.</figcaption></figure>
{DISC}
"""
    fq = "\n".join(f"        <details>\n          <summary>{esc(q)}</summary>\n          <p>{ans}</p>\n        </details>" for q, ans in faqs)
    sl = "\n".join(f'          <li><a href="{SRC[k][0]}" rel="noopener noreferrer" target="_blank">{esc(SRC[k][1])}</a>: {esc(why)} ({READ})</li>' for k, why in srcs)
    rl = "\n".join(f'          <li><a href="{h}">{esc(t)}</a></li>' for h, t in related)
    out = head + body + f"""
      <section class="faq-block" aria-labelledby="faq-heading">
        <h2 id="faq-heading">Frequently asked questions</h2>
{fq}
      </section>
      <section class="sources-block" aria-labelledby="sources-heading">
        <h2 id="sources-heading">Sources</h2>
        <p class="note">We paraphrase public references and link them so you can read the full wording. We did not test any tire for this page.</p>
        <ul>
{sl}
          <li><a href="/image-policy/">Image policy</a>: how the AI generated illustration is labeled</li>
        </ul>
      </section>
      <nav class="related-links" aria-label="Keep reading">
        <h2>Keep reading</h2>
        <ul>
{rl}
        </ul>
      </nav>
      <div class="cta-box">
        <h2>Not sure yet?</h2>
        <p>Use the <a href="/which-tire/">Which tire picker</a> to match your vehicle, climate and driving to a tire category, then confirm size, load index and speed rating on your <a href="/guides/placard/">door placard</a>.</p>
      </div>
    </div>
  </main>
{FOOT.rstrip()}
"""
    out = out.replace("</body>", extra_tail + "</body>") if extra_tail else out
    p = ROOT / "which-tire" / slug / "index.html" if slug else ROOT / "which-tire/index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(out + ("\n" if not out.endswith("\n") else ""))
    return url

CHECKS = f"""      <section class="content-section">
        <h2>Size, load and speed checks before you buy</h2>
        <ul>
          <li><b>Size:</b> USTMA says replacement tires should be the original equipment size or an approved option from the vehicle or tire maker, and never smaller or with less load capacity than the original size at placard pressure ({a('CS','USTMA Care and Service')}).</li>
          <li><b>Load index:</b> match or exceed the load capacity on the placard. See <a href="/guides/load-index-speed-rating/">load index and speed rating</a> and <a href="/guides/xl-vs-sl-tires/">XL vs SL</a>.</li>
          <li><b>Speed rating:</b> USTMA says the replacement speed rating must be equal to or greater than what the vehicle maker specifies to keep the vehicle's speed capability; a lower rated tire limits the vehicle to that tire's speed ({a('CS','USTMA')}).</li>
          <li><b>All four alike:</b> USTMA recommends all four tires share size, load index, speed rating and construction, and says never mix passenger tires with light truck tires on one vehicle ({a('CS','USTMA')}).</li>
        </ul>
      </section>
"""
CAT_LINKS = ""  # filled for hub

PAGES = []
def P(**k): PAGES.append(k)

# 1 SUV
P(slug="suv", crumb="SUV or crossover", img="suv",
  title="Which tire should I get for my SUV or crossover?",
  h1="Which tire should I get for my SUV or crossover?",
  desc="For most SUVs and crossovers on paved roads: a highway or crossover touring all season tire, or a 3PMSF all weather tire if you see snow. How to choose.",
  lede="Most crossovers and SUVs that stay on pavement are best matched with a highway all season or crossover/SUV touring all season tire. Choose an all weather tire with the 3PMSF symbol if you get real snow, and all terrain only if you leave the pavement.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>If your SUV or crossover spends nearly all its time on paved roads, start with the <b>highway all season</b> or <b>crossover/SUV touring all season</b> category. Tire Rack describes these as the categories for daily commuters who rarely leave pavement, tuned for a quiet, comfortable ride, and offered in both all season and all weather versions ({a('TRT','Tire Rack truck and SUV tires')}). If winter brings packed snow, look for an all weather tire with the three peak mountain snowflake (3PMSF) symbol. Pick <b>all terrain</b> only if you regularly drive dirt, sand, mud or rocks.</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Start at the door placard.</b> It lists the original size, load and pressure. Copy it with our <a href="/guides/tire-placard-checklist/">placard checklist</a>.</li>
          <li><b>Decide where you drive.</b> In Tire Rack's paved road comparison, the highway all season tire rode better and was quieter, while the all terrain tire had a steady growl above 20 mph, less wet grip and a longer wet braking distance ({a('TRH','Tire Rack test')}).</li>
          <li><b>Decide how much winter you get.</b> Michelin says all season tires carry M+S, which is based on tread design rather than a snow test, while 3PMSF tires have passed a standardized packed snow traction test ({a('MTY','Michelin')}). For regular ice and deep cold, a dedicated <a href="/guides/winter-tires/">winter tire</a> is still the stronger choice.</li>
          <li><b>Rank your priorities.</b> If quiet and comfort matter most, touring and highway all season tires are built for that. If long tread life matters, compare UTQG treadwear numbers on the tires you shortlist (see <a href="/guides/utqg/">UTQG</a>).</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>All terrain tires for looks only.</b> You give up some quiet, wet grip and, in Tire Rack's test, about 3 percent fuel economy (22.7 vs 22.0 mpg) for capability you may not use ({a('TRH','Tire Rack')}).</li>
          <li><b>Switching to LT tires without checking.</b> Many SUVs ship on passenger tires. USTMA says passenger tires can sometimes be replaced with light truck tires, but it takes a significant pressure change, rim and clearance checks, and handling may be affected ({a('CS','USTMA')}). See <a href="/guides/lt-vs-p-metric-tires/">LT vs P metric</a>.</li>
          <li><b>Mixing tread types on AWD.</b> USTMA says do not mix tread pattern types such as all terrain and all season on 4WD and AWD vehicles, and keep all four the same size ({a('CS','USTMA')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Do I need all terrain tires on an AWD crossover?", "Not for paved driving. AWD helps you accelerate but does not change which tire suits your roads. Tire Rack found highway all season tires quieter, smoother and grippier in the wet on pavement, while all terrain tires make sense when you regularly leave the pavement."),
        ("Are all weather tires good for an SUV?", "If you get packed snow but do not want a second set, an all weather tire with the 3PMSF symbol is the category to look at. Michelin says the 3PMSF symbol means the tire passed a standardized packed snow traction test, but it does not cover pure ice."),
        ("Can I put LT tires on my SUV?", "Sometimes. USTMA says it requires a significant inflation pressure adjustment to carry the same load, rim width and rim load checks, and clearance checks, and that handling may change. Ask the vehicle maker or a tire professional first, and never mix LT and passenger tires on one vehicle."),
        ("How do I know which load index my SUV needs?", "Use the size and load index on the door placard or in the owner's manual. USTMA says never choose a replacement with less load carrying capacity than the original tire at placard pressure.")],
  srcs=[("TRT", "categories for paved commuters, all season and all weather options, all terrain subcategories"), ("TRH", "highway all season vs all terrain on paved roads: noise, wet braking, fuel economy"), ("MTY", "M+S vs 3PMSF and seasonal categories"), ("CS", "replacement size, load, speed rating, mixing and LT replacement rules")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/snow-without-winter-tires/", "Which tire for snow without winter tires"), ("/which-tire/gravel-roads/", "Which tire for gravel roads"), ("/guides/lt-vs-p-metric-tires/", "LT vs P metric tires"), ("/guides/all-weather-vs-all-season/", "All weather vs all season")])

# 2 Pickup
P(slug="pickup-truck", crumb="Pickup truck", img="wheel",
  title="Which tire should I get for my pickup truck?",
  h1="Which tire should I get for my pickup truck?",
  desc="Highway all season for paved miles, all terrain for dirt and job sites, LT load range for heavy hauling. Pickup tire choice, load checks and what to avoid.",
  lede="For a pickup that mostly drives paved roads, a highway all season tire is the usual match. Choose all terrain if you work or play off pavement, and an LT tire in the load range your truck specifies if you haul or tow heavy.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Match the tire to the hardest job your truck does regularly. Tire Rack groups truck tires from highway all season for paved commuting through on road all terrain up to max traction "mud" tires for serious off road use ({a('TRT','Tire Rack truck tires')}). Then make sure the construction is right: if your truck came on LT tires, USTMA says not to replace them with passenger tires unless the vehicle maker says otherwise ({a('CS','USTMA')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Read the placard and the sidewall.</b> An LT size such as LT245/75R16 Load Range E tells you it is a light truck tire, and USTMA says the load range identifies its load and inflation limits ({a('CS','USTMA')}). A P in front of the size means a passenger tire.</li>
          <li><b>Paved roads most days:</b> highway all season. Tire Rack found it quieter and better in the wet on pavement than an all terrain tire ({a('TRH','Tire Rack')}).</li>
          <li><b>Dirt roads, job sites, trails:</b> all terrain. Tire Rack says all terrain tires are built to dig through loose dirt and sand, mud and rocky ground, at the cost of more tread noise, a little less responsive handling and a modest drop in wet traction on pavement ({a('TRH','Tire Rack')}).</li>
          <li><b>Heavy hauling or towing:</b> LT construction. Tire Rack says LT tires use thicker plies, reinforced sidewalls and heavier materials, and come in load ranges such as C, D, E and F ({a('TRT','Tire Rack')}). See <a href="/which-tire/towing/">which tire for towing</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Putting passenger tires on a truck that came with LT.</b> USTMA advises against it unless the vehicle maker specifies otherwise ({a('CS','USTMA')}).</li>
          <li><b>Assuming a passenger tire carries its full rating on a truck.</b> USTMA says passenger tire load capacity is divided by 1.10 on light trucks; its example P265/70R17 drops from 2535 lb to 2305 lb ({a('CS','USTMA')}).</li>
          <li><b>Mixing.</b> USTMA says never mix passenger and LT tires on one vehicle, and on 4WD do not mix all terrain with all season tread ({a('CS','USTMA')}).</li>
          <li><b>Upsizing without checks.</b> Larger tires need rim, load and clearance checks. See <a href="/guides/plus-sizing/">plus sizing</a>.</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Are all terrain tires worth it on a pickup?", "Only if you use the capability. Tire Rack's paved road test found the all terrain tire louder, slightly less precise and weaker in the wet than a highway all season tire, and it used about 3 percent more fuel in their test."),
        ("What does load range E mean?", "It is a light truck load range. USTMA says the load range identifies the tire's load and inflation limits. Our LT vs P guide lists the inflation pressures for load ranges C, D and E."),
        ("Can I replace LT tires with P metric tires?", "USTMA says it is not recommended to replace original LT tires with P metric or Euro metric tires unless the vehicle maker specifies it."),
        ("Do mud terrain tires work on the highway?", "They are the most specialized end of the all terrain range, which Tire Rack calls max traction or mud tires. Expect the paved road trade offs of all terrain tires (noise, wet grip) to be larger, so pick them only for regular mud or rock use.")],
  srcs=[("TRT", "truck tire categories, LT construction and load ranges"), ("TRH", "highway all season vs all terrain on pavement"), ("CS", "LT markings, P to LT rules, 1.10 load reduction, mixing rules")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/towing/", "Which tire for towing"), ("/guides/lt-vs-p-metric-tires/", "LT vs P metric tires"), ("/guides/st-trailer-tires/", "ST trailer tires"), ("/which-tire/gravel-roads/", "Which tire for gravel roads"), ("/which-tire/4x4-off-road/", "Which tire for a Jeep style 4x4")])

# 3 EV
P(slug="electric-vehicle", crumb="Electric vehicle", img="pressure",
  title="Which tire should I get for my EV?",
  h1="Which tire should I get for my electric vehicle?",
  desc="EV tires: match HL or XL load ratings on the placard, look for low rolling resistance and quiet construction, and expect faster wear. What to check.",
  lede="For an EV, start with load: if the placard or original tires say HL, the replacement must be HL. After that, look for low rolling resistance for range and quiet construction, in the season category that suits your climate.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>An EV tire is mostly about <b>load capacity</b>, then <b>rolling resistance</b> and <b>noise</b>. Michelin says if your EV came from the factory with HL tires, every replacement must also be HL rated, because HL tires carry more weight than XL tires at the same pressure ({a('MHL','Michelin HL guide')}). Continental says lower rolling resistance means more range and that quiet tires matter more without engine noise ({a('CEV','Continental')}). Choose all season, all weather or winter the same way you would for any car.</p>
      </section>
      <section class="content-section">
        <h2>What HL means</h2>
        <p>USTMA's bulletin on High Load Capacity tires gives an example in one size: 245/40R19 94Y standard load carries 1477 lb at 36 psi, the XL version 98Y carries 1653 lb at 42 psi, and HL245/40R19 101Y carries 1819 lb at the same 42 psi ({a('T54','USTMA TISB 54')}). USTMA recommends replacing an HL tire with an HL tire of equal size and load capacity and notes that approved rim widths may differ. Michelin adds that an HL tire can replace an XL tire to add capacity ({a('MHL','Michelin')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Copy size, load index and speed rating</b> from the placard; check for an HL prefix on the current tires.</li>
          <li><b>Pick the season category</b> for your climate (see the <a href="/which-tire/">picker</a>).</li>
          <li><b>Prefer low rolling resistance</b> for range, which Continental calls essential for EVs ({a('CEV','Continental')}).</li>
          <li><b>Consider noise.</b> Some tires use foam inside the tread to reduce cabin noise; Continental describes this for its own line ({a('CEV','Continental')}).</li>
          <li><b>Plan for wear.</b> Michelin says that on average EVs wear tires about 20 percent faster than comparable gas cars, because of weight, torque and regenerative braking ({a('MEV','Michelin EV FAQ')}). Continental recommends checking alignment every 6 months or after a hard curb or pothole hit ({a('CEV','Continental')}).</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Standard load or XL where HL is specified.</b> Michelin says that runs the tire beyond its rated load, raising heat, wear and failure risk ({a('MHL','Michelin')}).</li>
          <li><b>Buying on size alone.</b> A tire in the right size but a lower load index does not meet the requirement.</li>
          <li><b>Skipping rotations.</b> Faster wear makes regular <a href="/guides/tire-rotation/">rotation</a> and <a href="/guides/tire-pressure/">pressure checks</a> more important.</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Do EVs need special tires?", "They need tires that meet the load index on the placard, which may mean HL or XL tires. Low rolling resistance and low noise help range and comfort. The season category still depends on your climate."),
        ("Can I put XL tires on an EV that came with HL tires?", "No. Michelin says that if the vehicle came with HL tires, replacements must also be HL rated. USTMA recommends replacing HL with HL of equal size and load capacity."),
        ("Why do EV tires wear out faster?", "Michelin says more weight, instant torque and regenerative braking combine to wear tires about 20 percent faster on average than a comparable gas vehicle."),
        ("Do low rolling resistance tires increase EV range?", "Continental says lower rolling resistance means increased electric range and higher efficiency. How much depends on the vehicle and driving.")],
  srcs=[("MHL", "HL vs XL, replace HL with HL, risks of under rated load"), ("T54", "HL load table and replacement recommendation"), ("MEV", "EVs wear tires about 20 percent faster on average"), ("CEV", "rolling resistance, noise, alignment every 6 months")],
  related=[("/which-tire/", "Which tire picker"), ("/guides/xl-vs-sl-tires/", "XL vs SL tires"), ("/guides/load-index-speed-rating/", "Load index and speed rating"), ("/guides/tire-rotation/", "Tire rotation"), ("/which-tire/highway-commuting/", "Which tire for highway commuting"), ("/which-tire/hybrid/", "Which tire for a hybrid")])

# 4 Snow without winter tires
P(slug="snow-without-winter-tires", crumb="Snow without winter tires", img="snow",
  title="Best tire type for snow without winter tires: all weather 3PMSF",
  h1="Which tire for snow if you don't want winter tires?",
  desc="Want one set of tires that handles snow? Look for an all weather tire with the 3PMSF symbol, not M+S alone. What it can and cannot do on ice.",
  lede="If you want one set of tires year round and still see snow, choose an all weather tire with the three peak mountain snowflake (3PMSF) symbol. An M+S marking alone does not mean the tire passed a snow test.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Look for <b>3PMSF</b> on the sidewall. Michelin says all weather tires carry the 3PMSF symbol, which requires passing a standardized severe snow traction test, while all season tires carry M+S, which is based on tread geometry and not a performance test ({a('MTY','Michelin')}). In Tire Rack's category test, the 3PMSF all weather tire was well ahead of the other all season tires in snow, but a dedicated winter tire was ahead of everything ({a('TRC','Tire Rack')}).</p>
      </section>
      <section class="content-section">
        <h2>What 3PMSF actually means</h2>
        <p>USTMA's severe snow definition requires a snow grip index of at least 1.10 or 1.12 (depending on the reference tire) against a standard reference test tire on medium packed snow, using ASTM F1805. Tires that pass may be marked with M+S plus a three peak mountain pictograph with a snowflake inside ({a('T37','USTMA TISB 37')}). Michelin notes the test does not cover pure ice ({a('MTY','Michelin')}).</p>
      </section>
      <section class="content-section">
        <h2>When one set is not enough</h2>
        <ul>
          <li><b>Regular ice or long deep cold.</b> Michelin says you likely need winter tires where it regularly approaches freezing or gets heavy snow or ice ({a('MTY','Michelin')}). Tire Rack's ice braking test favored the dedicated winter tire by a wide margin ({a('TRC','Tire Rack')}).</li>
          <li><b>You must drive whatever the weather.</b> A winter set on all four wheels is the stronger choice. See <a href="/guides/winter-tires/">winter tires</a>.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Treating M+S as a snow rating.</b> USTMA describes M+S as intended for limited mud and snow service ({a('CS','USTMA')}).</li>
          <li><b>Winter or snow tires on one axle only.</b> USTMA says if winter tires go on the front, they must go on the rear too ({a('CS','USTMA')}).</li>
          <li><b>Worn tread.</b> NHTSA says tread should be at least 2/32 inch on all tires, and suggests considering snow tires ({a('NWIN','NHTSA winter tips')}). More tread helps in snow; see <a href="/guides/tread-depth/">tread depth</a>.</li>
          <li><b>Summer tires in winter.</b> Michelin says summer tire rubber hardens below about 45°F and loses grip even on dry roads ({a('MSW','Michelin')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Are all weather tires as good as winter tires in snow?", "No. In Tire Rack's 2024 category test, the 3PMSF all weather tire was clearly better in snow than the other all season tires, but the dedicated winter tire was better than everything, including on ice."),
        ("Is M+S good enough for snow?", "M+S means the tire is intended for limited mud and snow service. Michelin says it is based on tread design, not a snow traction test. The 3PMSF symbol is the one that requires a packed snow test."),
        ("Does 3PMSF mean the tire is good on ice?", "Not necessarily. Michelin says the 3PMSF test is on medium packed snow and does not cover pure ice."),
        ("Can I keep all weather tires on in summer?", "All weather tires are designed for year round use without a seasonal swap, which is the point of the category. Check the speed rating and load index match your placard.")],
  srcs=[("T37", "severe snow definition, snow grip index, 3PMSF marking"), ("MTY", "M+S vs 3PMSF, ice not covered, when winter tires are needed"), ("MSW", "summer tires harden below 45°F"), ("TRC", "category test including all weather and dedicated winter tires in snow and ice"), ("CS", "M+S meaning, winter tires on all positions"), ("NWIN", "2/32 inch minimum, consider snow tires")],
  related=[("/which-tire/", "Which tire picker"), ("/guides/all-weather-vs-all-season/", "All weather vs all season"), ("/guides/winter-tires/", "Winter tires"), ("/comparisons/all-season-vs-winter/", "All season vs winter"), ("/guides/how-long-do-winter-tires-last/", "How long winter tires last")])

# 5 Highway commuting
P(slug="highway-commuting", crumb="Highway commuting", img="sedan",
  title="Which tire is best for highway commuting? Touring all season",
  h1="Which tire should I get for highway commuting?",
  desc="Long highway commutes: grand touring all season for quiet and comfort, standard touring for tread life. How to compare UTQG, speed rating and noise.",
  lede="For a car that racks up highway miles, a touring all season tire is the usual match. Grand touring leans toward quiet, comfort and handling; standard touring leans toward long tread life.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Tire Rack calls <b>grand touring all season</b> the go to category for most people: pretty good at everything without being the best at any one thing. <b>Standard touring all season</b> tires focus on tread life, and in Tire Rack's test one standard touring tire took longer to stop from 60 mph than the grand touring tires ({a('TRC','Tire Rack category test')}). Tire Rack describes grand touring all season tires as focused on comfort, road noise reduction and long tread life ({a('TRA','Tire Rack')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Quiet and comfort first:</b> grand touring all season.</li>
          <li><b>Lowest cost per mile first:</b> standard touring all season, and compare UTQG treadwear. Under federal rules, a tire graded 150 wears one and a half times as well as one graded 100 on the government test course ({a('ECFR','49 CFR 575.104')}). Your real miles will differ; see <a href="/guides/utqg/">UTQG</a>.</li>
          <li><b>Wet roads:</b> compare the UTQG traction grade (AA, A, B, C). It reflects straight ahead wet braking only, not cornering or hydroplaning ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Snow on the commute:</b> look at 3PMSF all weather options. See <a href="/which-tire/snow-without-winter-tires/">snow without winter tires</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>A lower speed rating than the placard.</b> USTMA says the vehicle is then limited to the tire's speed capability and handling may change ({a('CS','USTMA')}).</li>
          <li><b>Treating speed ratings as permission.</b> USTMA says a speed rating does not mean the vehicle can be safely driven at that speed, and ratings do not apply to underinflated, overloaded, worn or damaged tires ({a('CS','USTMA')}).</li>
          <li><b>Skipping pressure checks before long trips.</b> USTMA says to check pressure at least monthly and before long trips ({a('CS','USTMA')}). See <a href="/guides/tire-pressure/">tire pressure</a>.</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("What is the difference between grand touring and standard touring tires?", "Tire Rack says standard touring all season tires focus on tread life, while grand touring all season tires are the all round choice with an emphasis on comfort and handling. In its test, a standard touring tire needed more distance to stop from 60 mph than the grand touring tires."),
        ("Does a higher treadwear number mean more miles?", "On the government test course, yes, relatively: a 150 wears one and a half times as well as a 100. Real mileage depends on alignment, inflation, load, roads and driving."),
        ("Do I need a higher speed rating for highway driving?", "Match or exceed the speed rating the vehicle maker specifies. USTMA says a speed rating is not permission to drive at that speed."),
        ("Is a performance tire better for the highway?", "Not usually for commuting. Tire Rack found ultra high performance all season tires gave up ride comfort and winter traction compared with touring tires.")],
  srcs=[("TRC", "standard vs grand touring vs ultra high performance all season trade offs"), ("TRA", "grand touring all season focus on comfort, noise and tread life"), ("ECFR", "UTQG treadwear and traction grade definitions"), ("CS", "speed rating rules, pressure checks")],
  related=[("/which-tire/", "Which tire picker"), ("/comparisons/touring-vs-performance-all-season/", "Touring vs performance all season"), ("/guides/utqg/", "UTQG grades"), ("/guides/how-long-do-tires-last/", "How long tires last"), ("/which-tire/rain/", "Which tire for rain"), ("/which-tire/hybrid/", "Which tire for a hybrid")])

# 6 Towing
P(slug="towing", crumb="Towing", img="wheel",
  title="Which tire should I get for towing? LT load range guide",
  h1="Which tire should I get for towing?",
  desc="Towing tires: meet or beat the placard load index, use LT construction and load range if specified, and set tow pressures from the owner's manual.",
  lede="For towing, the tire category matters less than load capacity. Use the size, load index and load range your vehicle maker specifies (often an LT tire on trucks), set pressure from the owner's manual for towing, and keep the trailer on its own correct tires.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Start with the vehicle maker's tow rating and tire spec. NHTSA says manufacturers' tow ratings can guide the choice of tow vehicle tires, and that tow vehicle tires may need higher pressure for towing, especially with heavy loads ({a('NTOW','NHTSA towing guide')}). If your truck came on LT tires, stay with LT tires in at least the same load range; USTMA advises against replacing original LT tires with passenger tires unless the vehicle maker allows it ({a('CS','USTMA')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Load capacity first.</b> USTMA says replacements must have load capacity equal to or greater than the original tire at placard pressure ({a('CS','USTMA')}).</li>
          <li><b>LT construction for heavy work.</b> Tire Rack says LT tires use thicker plies and reinforced sidewalls, suiting heavy hauling and towing, in load ranges C through F ({a('TRT','Tire Rack')}).</li>
          <li><b>Load range on the sidewall.</b> USTMA says the load range (for example Load Range E) identifies the tire's load and inflation limits ({a('CS','USTMA')}). See <a href="/guides/lt-vs-p-metric-tires/">LT vs P metric</a> for pressures by load range.</li>
          <li><b>Tread category second.</b> Highway all season for paved towing, all terrain if you launch boats on gravel or work off road. See <a href="/which-tire/pickup-truck/">pickup truck tires</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Pressure and checks</h2>
        <ul>
          <li>NHTSA says underinflation reduces load capacity, may cause sway and control problems, and can lead to overheating and blowouts ({a('NTOW','NHTSA')}).</li>
          <li>USTMA says to check pressure before towing a trailer, before long trips and before carrying heavy loads ({a('CS','USTMA')}).</li>
          <li>Never exceed the maximum pressure on the sidewall.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Passenger tires at their full rating on a truck.</b> USTMA divides passenger tire load by 1.10 on light trucks ({a('CS','USTMA')}).</li>
          <li><b>Mismatched trailer tires.</b> NHTSA says trailer tires should all be the same type, size and construction, in the size and load range on the trailer's label ({a('NTOW','NHTSA')}). See <a href="/guides/st-trailer-tires/">ST trailer tires</a>.</li>
          <li><b>Mixing LT and passenger tires</b> on the tow vehicle ({a('CS','USTMA')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Do I need LT tires to tow?", "Use what the vehicle maker specifies. If the truck came with LT tires, stay with LT tires in at least the same load range. Some lighter vehicles tow on passenger tires within their tow rating; check the owner's manual."),
        ("Should I raise tire pressure when towing?", "NHTSA says tow vehicle tires may require higher pressure for towing, especially heavy loads. Use the towing pressure in the owner's manual and never exceed the sidewall maximum."),
        ("What load range do I need for towing?", "At least the load capacity of the original tires at placard pressure. Load range E is common on heavier pickups, but the right answer is on your placard and in the owner's manual."),
        ("Can I use LT tires on my trailer?", "Follow the trailer's certification label. NHTSA says to buy the size, type and load range shown there. USTMA says ST tires should not be replaced with any other type.")],
  srcs=[("NTOW", "tow ratings, tow vehicle pressure, underinflation risks, trailer tire matching"), ("CS", "load capacity rules, load range meaning, P to LT and 1.10 rule, pressure checks before towing"), ("TRT", "LT construction and load ranges")],
  related=[("/which-tire/", "Which tire picker"), ("/guides/lt-vs-p-metric-tires/", "LT vs P metric tires"), ("/guides/st-trailer-tires/", "ST trailer tires"), ("/guides/load-index-speed-rating/", "Load index and speed rating"), ("/which-tire/pickup-truck/", "Which tire for a pickup truck")])

# 7 Minivan
P(slug="minivan", crumb="Minivan", img="sedan",
  title="Which tire should I get for my minivan?",
  h1="Which tire should I get for my minivan?",
  desc="Minivan tires: standard or grand touring all season for comfort and tread life, 3PMSF all weather for snow, and a load index that covers a full van.",
  lede="Most minivans are best matched with a touring all season tire: standard touring if tread life and cost per mile matter most, grand touring if you want a quieter, more composed ride. Make sure the load index covers a fully loaded van.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Tire Rack says standard touring all season tires are designed for cars, vans and crossovers, with everyday dependability, comfort and long tread life ({a('TRA','Tire Rack')}). Its category test found standard touring tires focus on tread life, while grand touring is the all round choice ({a('TRC','Tire Rack')}). For a family van that sees snow, consider a 3PMSF all weather tire.</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Load first.</b> A van loaded with people and luggage puts more weight on each tire. USTMA says never pick a tire with less load capacity than the original at placard pressure ({a('CS','USTMA')}). Some vans list an XL tire; see <a href="/guides/xl-vs-sl-tires/">XL vs SL</a>.</li>
          <li><b>Comfort and noise:</b> grand touring all season.</li>
          <li><b>Tread life and budget:</b> standard touring all season; compare UTQG treadwear ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Winter:</b> 3PMSF all weather or a winter set. See <a href="/which-tire/snow-without-winter-tires/">snow without winter tires</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Running low pressure with a full load.</b> The UTQG temperature warning says underinflation and excessive loading can cause heat buildup and possible tire failure ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Replacing just two tires with a different type.</b> USTMA recommends all four share size, load index, speed rating and construction ({a('CS','USTMA')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("What type of tire is best for a minivan?", "For most minivans, a touring all season tire. Tire Rack lists standard touring all season tires for cars, vans and crossovers. Choose grand touring for more quiet and comfort, or a 3PMSF all weather tire for snow."),
        ("Do minivans need XL tires?", "Only if the placard or owner's manual calls for that load index. Match or exceed the original load capacity at placard pressure."),
        ("How do I make minivan tires last longer?", "Keep pressure at the placard value, rotate on schedule and compare UTQG treadwear grades when you buy. See our tire rotation and tire pressure guides.")],
  srcs=[("TRA", "standard touring all season for cars, vans and crossovers"), ("TRC", "standard vs grand touring trade offs"), ("ECFR", "UTQG treadwear and temperature warning"), ("CS", "load capacity and matching rules")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/highway-commuting/", "Which tire for highway commuting"), ("/guides/xl-vs-sl-tires/", "XL vs SL tires"), ("/guides/tire-pressure/", "Recommended tire pressure"), ("/guides/tire-rotation/", "Tire rotation")])

# 8 Sports car
P(slug="sports-car", crumb="Sports car", img="sedan",
  title="Which tire should I get for a sports car? Summer vs UHP all season",
  h1="Which tire should I get for a sports car?",
  desc="Sports car tires: max performance summer for warm weather grip, ultra high performance all season for year round use, winter set below about 45°F.",
  lede="If it stays warm where you drive, a max performance summer tire gives the most grip. If you need one tire year round, an ultra high performance all season tire trades some grip for cold weather use. Below about 45°F, summer tires should come off.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Tire Rack's category test reported that its max performance summer tires out braked the other categories by 13 feet or more and called them the go to for peak wet performance, while giving up cold weather use and some comfort. Ultra high performance all season tires were a step up from touring tires in grip, but gave up ride quality and were a step down in snow ({a('TRC','Tire Rack category test')}). Michelin says summer tires work best above about 45°F and should come off before sustained cold ({a('MSW','Michelin')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Warm climate, spirited driving:</b> max performance summer.</li>
          <li><b>Mostly dry track days:</b> extreme performance summer, which Tire Rack describes as focused on dry grip with more noise, a stiff ride and a tendency to hydroplane in standing water ({a('TRC','Tire Rack')}).</li>
          <li><b>One tire all year:</b> ultra high performance all season, plus a <a href="/guides/winter-tires/">winter set</a> if you get snow.</li>
          <li><b>Staggered sizes:</b> many sports cars run different front and rear sizes. Keep the maker's sizes; see <a href="/guides/staggered-tire-fitment/">staggered fitment</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Summer tires in the cold.</b> Michelin says their rubber hardens below about 45°F and loses grip on every surface, not just snow ({a('MSW','Michelin')}).</li>
          <li><b>Dropping the speed rating.</b> USTMA says replacements need an equal or higher speed rating to keep the vehicle's speed capability ({a('CS','USTMA')}).</li>
          <li><b>Mixing summer and all season tires.</b> Michelin says all four should be the same type ({a('MSW','Michelin')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Can I drive summer tires in winter?", "Michelin says no: summer tire rubber hardens below about 45°F, reducing grip even on cold dry roads, and grip drops severely in snow or ice."),
        ("Are ultra high performance all season tires good in snow?", "They are all season tires, but in Tire Rack's category test they were a clear step down in snow and ice from the touring all season tires."),
        ("What is the difference between max performance and extreme performance summer tires?", "Tire Rack says max performance summer tires lead in the wet and balance some comfort and tread life, while extreme performance summer tires chase dry grip with more noise and a stiffer ride."),
        ("Do I need a Y or W speed rating?", "You need at least the speed rating the vehicle maker specifies. USTMA says a lower rating limits the vehicle to the tire's speed capability.")],
  srcs=[("TRC", "max, extreme and ultra high performance category trade offs"), ("MSW", "summer tires below 45°F, do not mix types"), ("CS", "speed rating rules")],
  related=[("/which-tire/", "Which tire picker"), ("/comparisons/touring-vs-performance-all-season/", "Touring vs performance all season"), ("/guides/staggered-tire-fitment/", "Staggered tire fitment"), ("/fitment/all-season-vs-winter-vs-summer/", "All season vs winter vs summer"), ("/which-tire/hot-climate/", "Which tire for hot climates")])

# 9 Rain
P(slug="rain", crumb="Rain", img="rain",
  title="Which tire is best for rain? What actually matters in the wet",
  h1="Which tire should I get for rain?",
  desc="Tires for rain: grand touring or performance categories, a high UTQG traction grade, and enough tread. What the AA traction grade does not tell you.",
  lede="For wet roads, choose a category built for wet grip, compare the UTQG traction grade among your shortlist, and replace tires before tread runs low. Remember the traction grade measures straight ahead wet braking only.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Wet grip varies a lot by category. In Tire Rack's category test, max performance summer tires were the wet leaders, ultra high performance all season tires improved on touring tires in the wet, and the standard touring tires struggled for wet grip ({a('TRC','Tire Rack')}). Tire Rack describes grand touring summer tires as emphasizing wet traction and hydroplaning resistance ({a('TRA','Tire Rack')}). Whatever you choose, keep the tread healthy.</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Compare the traction grade.</b> Grades run AA, A, B, C, based on wet braking on government test surfaces; a C tire may have poor traction ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Know its limits.</b> The same rule warns the grade is based on straight ahead braking and does not include acceleration, cornering, hydroplaning or peak traction ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Pick the category for your temperatures.</b> Summer tires suit warm rain; below about 45°F choose all season, all weather or winter ({a('MSW','Michelin')}).</li>
          <li><b>Watch tread depth.</b> NHTSA says tread should be at least 2/32 inch on all tires ({a('NWIN','NHTSA')}). See <a href="/guides/tread-depth/">tread depth</a> and <a href="/guides/when-to-replace/">when to replace</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>All terrain tires for a wet commute.</b> Tire Rack's paved road test found a longer wet braking distance for the all terrain tire ({a('TRH','Tire Rack')}).</li>
          <li><b>Extreme performance tires in standing water.</b> Tire Rack noted its extreme performance summer tire tended to hydroplane in standing water ({a('TRC','Tire Rack')}).</li>
          <li><b>Low pressure.</b> Check monthly; see <a href="/guides/tire-pressure/">tire pressure</a>.</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Does a traction AA tire stop best in the rain?", "AA is the highest UTQG traction grade for straight ahead wet braking on the government test. It does not measure cornering or hydroplaning, so treat it as one clue."),
        ("Which tire category is best in the wet?", "In Tire Rack's category test, max performance summer tires led in the wet, but they are for warm weather. For year round use, the ultra high performance all season tires improved on the touring tires in the wet."),
        ("When should I replace tires for rain?", "NHTSA's minimum is 2/32 inch. Many drivers replace earlier for wet roads; see our tread depth guide for how to measure.")],
  srcs=[("TRC", "wet performance by category, hydroplaning note"), ("TRA", "grand touring summer emphasizes wet grip and hydroplaning resistance"), ("TRH", "all terrain wet braking on pavement"), ("ECFR", "traction grade definition and limits"), ("MSW", "45°F guidance"), ("NWIN", "2/32 inch minimum")],
  related=[("/which-tire/", "Which tire picker"), ("/guides/utqg/", "UTQG grades"), ("/guides/tread-depth/", "Tread depth"), ("/which-tire/highway-commuting/", "Which tire for highway commuting"), ("/which-tire/hot-climate/", "Which tire for hot climates")])

# 10 Hot climate
P(slug="hot-climate", crumb="Hot climate (Florida, Southwest)", img="rain",
  title="Which tire for Florida and hot climates? Heat, rain and UTQG",
  h1="Which tire should I get for a hot climate like Florida?",
  desc="Hot climate tires: no winter compound needed, summer or all season both work above 45°F, check UTQG temperature grade and keep pressure right in heat.",
  lede="Where it rarely gets cold, you do not need winter capability. A grand touring all season tire suits most drivers, and summer tires are an option in places that stay warm. Check the UTQG temperature grade and keep pressure at the placard value.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Michelin says that in climates that stay above freezing, summer tires can make sense even for everyday driving, since they are optimized for warm weather grip and wet roads above about 45°F ({a('MTY','Michelin')}). Most commuters will still be happy with a touring all season tire for its comfort and tread life ({a('TRC','Tire Rack')}). Frequent summer storms make wet grip worth prioritizing; see <a href="/which-tire/rain/">which tire for rain</a>.</p>
      </section>
      <section class="content-section">
        <h2>Heat: what the temperature grade means</h2>
        <p>UTQG temperature grades are A, B and C, measuring resistance to heat buildup on an indoor test wheel. Grade C is the federal minimum under FMVSS 109; A and B are higher ({a('ECFR','49 CFR 575.104')}). The rule warns that excessive speed, underinflation or excessive load can still cause heat buildup and possible tire failure. USTMA repeats that the grade assumes proper inflation and load ({a('CS','USTMA')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Commuting, comfort, tread life:</b> grand or standard touring all season.</li>
          <li><b>Sporty car, always warm:</b> max performance summer. See <a href="/which-tire/sports-car/">sports car tires</a>.</li>
          <li><b>Compare temperature and traction grades</b> on your shortlist.</li>
          <li><b>Check pressure cold.</b> NHTSA says check tires when cold, after at least three hours parked, and inflate to the placard, not the sidewall maximum ({a('NWIN','NHTSA')}).</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Underinflation in heat,</b> which the UTQG warning links to heat buildup ({a('ECFR','49 CFR 575.104')}).</li>
          <li><b>Overloading</b> the vehicle beyond the placard limits.</li>
          <li><b>Summer tires on a trip north in winter.</b> Michelin says they should not be used near freezing ({a('MTY','Michelin')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Do I need all season tires in Florida?", "You do not need winter capability. All season tires remain a sensible default for comfort and tread life, and Michelin says summer tires can be worth considering where it stays above freezing."),
        ("What UTQG temperature grade should I look for?", "A is the highest, C is the federal minimum. A higher grade means more resistance to heat on the lab test, but the grade assumes correct inflation and load."),
        ("Does heat make tires wear faster?", "We could not find a source we trust that gives a number, so we do not state one. What the federal grading text does say is that speed, underinflation and overload drive heat buildup, which can damage a tire.")],
  srcs=[("MTY", "summer tires above 45°F in warm climates, not near freezing"), ("TRC", "touring all season as the all round choice"), ("ECFR", "UTQG temperature grade and heat warning"), ("CS", "temperature grade assumes correct inflation and load"), ("NWIN", "check cold, placard vs sidewall pressure")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/rain/", "Which tire for rain"), ("/guides/utqg/", "UTQG grades"), ("/guides/cold-vs-hot-tire-pressure/", "Cold vs hot tire pressure"), ("/guides/dot-date-codes/", "DOT date codes and tire age")])

# 11 Gravel
P(slug="gravel-roads", crumb="Gravel and dirt roads", img="suv",
  title="Which tire for gravel and dirt roads? Highway vs all terrain",
  h1="Which tire should I get for gravel and dirt roads?",
  desc="Gravel roads: highway all season handles graded dirt and two tracks; all terrain for loose dirt, sand, mud and rocks. LT tires add toughness.",
  lede="For a graded gravel road or dirt driveway, a highway all season tire is usually enough. If you drive loose dirt, sand, mud or rocks often, an all terrain tire is the better tool, and LT construction adds toughness.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Tire Rack says highway all season tires are not built for serious off roading but handle a dirt driveway or a two track down to a boat ramp. All terrain tires are built to dig through loose dirt and sand, mud and rocky terrain, with more noise and a little less wet grip on pavement ({a('TRH','Tire Rack')}).</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Mostly pavement, some graded gravel:</b> highway all season or crossover touring all season.</li>
          <li><b>Regular rough or loose roads:</b> on road or off road all terrain. Tire Rack lists five all terrain subcategories, from on road all terrain to max traction "mud tires" ({a('TRT','Tire Rack')}).</li>
          <li><b>Sharp rock and puncture risk:</b> Tire Rack says LT tires' thicker plies and reinforced sidewalls increase durability and puncture resistance ({a('TRT','Tire Rack')}). Check fitment first; see <a href="/guides/lt-vs-p-metric-tires/">LT vs P metric</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Mixing tread types on 4WD or AWD.</b> USTMA says do not mix all terrain and all season tread ({a('CS','USTMA')}).</li>
          <li><b>LT tires at passenger tire pressures.</b> USTMA says switching to LT tires requires a significant pressure adjustment ({a('CS','USTMA')}).</li>
          <li><b>Assuming all terrain means good on snow and ice.</b> In Tire Rack's test the highway tire had better packed snow traction, and there was no real difference on ice ({a('TRH','Tire Rack')}).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Do I need all terrain tires for a gravel road?", "Not for a well graded gravel road. Tire Rack says highway all season tires handle dirt driveways and two tracks; all terrain tires are for loose dirt, sand, mud and rocks."),
        ("Are LT tires better on gravel?", "Tire Rack says LT construction increases durability and puncture resistance. It can also make the ride firmer and needs higher pressure, so confirm fitment with USTMA's P to LT guidance."),
        ("Are all terrain tires good in snow?", "Some carry the 3PMSF symbol. In Tire Rack's 2015 test, the highway all season tire had better packed snow traction than the all terrain tire, and they were about equal on ice.")],
  srcs=[("TRH", "highway all season vs all terrain capability and trade offs, snow and ice results"), ("TRT", "all terrain subcategories, LT durability and puncture resistance"), ("CS", "mixing and P to LT rules")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/pickup-truck/", "Which tire for a pickup truck"), ("/which-tire/suv/", "Which tire for an SUV"), ("/guides/lt-vs-p-metric-tires/", "LT vs P metric tires"), ("/guides/tire-plug-vs-patch/", "Tire plug vs patch"), ("/which-tire/4x4-off-road/", "Which tire for a Jeep style 4x4")])

# 12 4x4 off-roader (added 17 Nov 2026)
P(slug="4x4-off-road", crumb="4x4 off-roader", img="suv", pub="2026-11-17",
  title="Which tire for a Jeep Wrangler style 4x4? All terrain vs mud terrain",
  h1="Which tire should I get for a Jeep Wrangler style 4x4?",
  desc="For a 4x4 on pavement with some trails: all terrain. Mud terrain only for regular deep mud or rock. LT vs P, upsizing, spare and 4WD mixing rules.",
  lede="If your 4x4 spends most of its miles on pavement with weekend trails, choose an all terrain tire. Pick mud terrain only if you regularly drive deep mud, loose soil or rock, and a highway all season if you rarely leave the road.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>Choose by where you actually drive, not by looks. BFGoodrich says all terrain tires give a quieter, more comfortable highway ride and better on road handling than mud terrain tires while still handling moderate trails, and that mud terrain tires are for deep mud, sand, loose soil and technical rock crawling, at the cost of noise, fuel economy and tread life ({a('BFG','BFGoodrich tire selection')}). Its own advice: if most of your miles are highway with occasional trails, all terrain is the better tire even though mud terrain looks tougher. If your 4x4 rarely leaves pavement, a highway all season tire in the placard size is the quieter, simpler choice (see <a href="/which-tire/suv/">which tire for an SUV</a>).</p>
      </section>
      <section class="content-section">
        <h2>All terrain, mud terrain or highway: by use</h2>
        <table>
          <thead><tr><th>How you use the 4x4</th><th>Tire type to look at</th><th>Trade off</th></tr></thead>
          <tbody>
            <tr><td>Daily driver, rarely off pavement</td><td>Highway all season (or all weather with 3PMSF for snow)</td><td>Light off road use only</td></tr>
            <tr><td>Mostly highway, weekend trails, overlanding, towing</td><td>All terrain ({a('BFG','BFGoodrich')})</td><td>Less bite than mud terrain in deep mud</td></tr>
            <tr><td>Regular deep mud, sand, loose soil, rock crawling</td><td>Mud terrain ({a('BFG','BFGoodrich')})</td><td>Louder, lower fuel economy, shorter tread life on pavement</td></tr>
          </tbody>
        </table>
        <p>NHTSA describes all terrain tires as mainly used on four wheel drive vehicles and as a good compromise between on road driving and off road capability ({a('NT','NHTSA TireWise')}).</p>
      </section>
      <section class="content-section">
        <h2>Snow: check the symbol, not the tread blocks</h2>
        <p>Many off road tires carry M+S. Michelin says M+S is based on tread geometry, not a performance test, while the three peak mountain snowflake (3PMSF) symbol requires passing a standardized traction test on medium packed snow, and it still does not cover pure ice ({a('MTY','Michelin')}). If you drive in winter, look for 3PMSF on the all terrain sizes you shortlist, or run a dedicated <a href="/guides/winter-tires/">winter tire</a>.</p>
      </section>
      <section class="content-section">
        <h2>LT or P, bigger sizes and pressure</h2>
        <ul>
          <li><b>Keep LT if it came with LT.</b> BFGoodrich says never replace original LT tires with P metric tires because you lose load capacity and durability ({a('BFG','BFGoodrich')}). USTMA says P to LT swaps are possible on some vehicles but need a rim and inflation check, clearance check and may change handling ({a('CS','USTMA')}). See <a href="/guides/lt-vs-p-metric-tires/">LT vs P metric</a>.</li>
          <li><b>Going bigger is a vehicle change, not just a tire change.</b> BFGoodrich says larger than stock tires often need a lift kit and changes to brake lines, steering and suspension, which can affect handling and rollover risk ({a('BFG','BFGoodrich')}). USTMA says any size change needs clearance checks at all four wheels through full suspension travel and full lock, and that diameter changes can affect the speedometer, ABS, TPMS and 4WD systems ({a('CS','USTMA')}). See <a href="/guides/plus-sizing/">plus sizing</a> and <a href="/guides/speedometer-error-tire-size/">speedometer error</a>.</li>
          <li><b>New size, new pressure.</b> BFGoodrich says the door placard pressures no longer apply after an upsize and to have a tire professional work out the right pressure ({a('BFG','BFGoodrich')}). Air back up after airing down for a trail before you drive on pavement.</li>
          <li><b>Do not mix tread types.</b> USTMA and Michelin both say not to mix tread pattern types such as all terrain and all season on 4WD vehicles, and to keep all four the same size; Michelin says the outside circumferences should be within 1 inch of each other ({a('CS','USTMA')}, {a('MCS','Michelin')}).</li>
          <li><b>Match the spare.</b> BFGoodrich suggests carrying a full size spare within about 1 inch of your main tire diameter ({a('BFG','BFGoodrich')}), and a spare that matches the other four lets you rotate five (see <a href="/guides/tire-rotation/">tire rotation</a>).</li>
        </ul>
      </section>
{CHECKS}""",
  faqs=[("Are mud terrain tires bad on the highway?", "They work on the road but cost you comfort. BFGoodrich says mud terrain tires are not quiet or fuel efficient and trade road noise, on road grip and tread life for maximum bite in deep mud. If most of your miles are paved, it recommends all terrain instead."),
        ("Do I need all terrain tires on a Jeep that never goes off road?", "No. NHTSA describes all terrain tires as a compromise between on road and off road use. If you never leave pavement, a highway all season tire in the placard size gives up nothing you use."),
        ("Are all terrain tires good in snow?", "It depends on the tire. Look for the 3PMSF symbol, which Michelin says requires passing a packed snow traction test; M+S alone is based on tread design. Neither symbol covers pure ice."),
        ("Can I put bigger tires on my 4x4?", "Only with the checks done. BFGoodrich says larger tires often require a lift and steering, brake line and suspension changes that can raise rollover risk, and USTMA says to check clearance at all four wheels and that a diameter change can affect the speedometer, ABS, TPMS and 4WD systems."),
        ("Can I replace just two tires on a 4x4?", "Check the owner's manual first. USTMA says that for 4WD and AWD vehicles even small differences in outside diameter may cause drivetrain damage, and that replacing all four together is recommended and preferred.")],
  srcs=[("BFG", "all terrain vs mud terrain uses and trade offs, LT vs P, upsizing, pressure, spare size"), ("NT", "what all terrain tires are for"), ("MTY", "M+S vs 3PMSF, ice limits"), ("MCS", "4WD mixing rules and 1 inch circumference"), ("CS", "4WD mixing, P to LT checks, diameter and clearance, replacing less than four")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/gravel-roads/", "Which tire for gravel roads"), ("/which-tire/pickup-truck/", "Which tire for a pickup truck"), ("/guides/lt-vs-p-metric-tires/", "LT vs P metric tires"), ("/guides/mixing-tires/", "Mixing tires"), ("/guides/plus-sizing/", "Plus sizing")])

P(slug="hybrid", crumb="Hybrid", img="sedan", pub="2026-11-19",
  title="Which tire for a hybrid? Low rolling resistance, at the placard load rating",
  h1="Which tire should I get for a hybrid?",
  desc="Hybrid tires: copy size, load index (XL or HL if listed) and speed rating from the placard, then choose low rolling resistance and a quiet touring tread.",
  lede="For a hybrid or plug in hybrid, start with the door placard: same size, a load index at least as high (XL or HL if that is what it lists) and a speed rating at least as high. Then pick a low rolling resistance tire in a touring all season or all weather tread for your climate, and keep it at placard pressure.",
  body=f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>A hybrid needs the same basics as any car plus two priorities: <b>low rolling resistance</b>, because that is what protects the fuel economy you bought the car for, and <b>enough load capacity</b>, because the battery adds weight. NHTSA says low rolling resistance replacement tires improve fuel economy and extend the range of electric and hybrid vehicles, and that carmakers increasingly fit them from the factory ({a('NT','NHTSA TireWise')}). Michelin's plug in hybrid guide says if the vehicle specifies XL or HL tires, replacements must carry the same designation ({a('MPH','Michelin plug in hybrid guide')}). Choose all season, all weather or winter by climate, as for any car.</p>
      </section>
      <section class="content-section">
        <h2>Why rolling resistance matters on a hybrid</h2>
        <p>NHTSA estimates that a 10 percent reduction in tire rolling resistance gives a 1 to 2 percent improvement in fuel economy, and says low rolling resistance tires commonly have higher inflation pressure and reduced sidewall and tread deflection ({a('NT','NHTSA')}). Michelin says that on a plug in hybrid, lower rolling resistance stretches electric range and also improves mpg when the engine is running ({a('MPH','Michelin')}).</p>
        <p>Size matters too. Michelin says a wider tire generally improves dry grip but increases rolling resistance, and that the factory size is the vehicle maker's balance of those trade offs ({a('MSZ','Michelin tire size guide')}). On a hybrid that is one more reason to stay with the placard size rather than going wider; see <a href="/guides/plus-sizing/">plus sizing</a> before changing it.</p>
      </section>
      <section class="content-section">
        <h2>How to choose</h2>
        <ol>
          <li><b>Copy the placard.</b> Size, load index and speed rating, plus any XL or HL marking on the current tires. Michelin says HL tires are built for heavier vehicles such as electric vehicles, hybrids and SUVs, an HL tire must be replaced with HL, and HL can replace XL for extra capacity ({a('MHL','Michelin HL guide')}).</li>
          <li><b>Check for an automaker marking</b> on the sidewall of the original tires. Michelin says marked original equipment tires are engineered for the vehicle's handling, ride, noise and rolling resistance targets, and recommends replacing them with the same approved marking when you can ({a('MOE','Michelin marked tires')}).</li>
          <li><b>Pick the tread for your climate:</b> touring all season for most drivers, all weather with the 3PMSF symbol if you get snow (see <a href="/which-tire/snow-without-winter-tires/">snow without winter tires</a>), dedicated winter for regular ice.</li>
          <li><b>Within that category, prefer low rolling resistance</b> as described by the tire maker, and compare UTQG treadwear grades for tread life (<a href="/guides/utqg/">UTQG guide</a>).</li>
          <li><b>Consider noise.</b> Michelin notes that plug in hybrids can be quieter than gas cars, so tire noise in the cabin can stand out if the tire is not designed for a quiet ride ({a('MPH','Michelin')}).</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Keep the savings: pressure and rotation</h2>
        <ul>
          <li><b>Pressure:</b> FuelEconomy.gov says keeping tires at the right pressure improves gas mileage by 0.6 percent on average and up to 3 percent in some cases, that under inflation lowers mileage by about 0.2 percent for every 1 psi drop in the average pressure of all tires, and that the right number is on the door jamb sticker, not the sidewall maximum ({a('FEG','FuelEconomy.gov')}). See <a href="/guides/tire-pressure/">tire pressure</a>.</li>
          <li><b>Rotation:</b> Michelin says plug in hybrid tires wear faster than tires on equivalent gas cars because of battery weight and motor torque, and its guide suggests rotating every 6,000 to 8,000 miles or at the first sign of uneven wear, while following the vehicle maker's interval ({a('MPH','Michelin')}). See <a href="/guides/tire-rotation/">tire rotation</a>.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>What to avoid</h2>
        <ul>
          <li><b>Trading load or speed rating for efficiency.</b> A lower load index or speed rating than the placard does not meet the requirement, however efficient the tire is ({a('CS','USTMA')}).</li>
          <li><b>Standard load where XL or HL is specified</b> ({a('MPH','Michelin')}, {a('MHL','Michelin')}).</li>
          <li><b>A wider size for looks,</b> which Michelin says raises rolling resistance ({a('MSZ','Michelin')}).</li>
        </ul>
        <p>Full electric car? See <a href="/which-tire/electric-vehicle/">which tire for an EV</a>.</p>
      </section>
{CHECKS}""",
  faqs=[("Do hybrids need special tires?", "Not a separate tire type, but they do best on low rolling resistance tires in the placard size and load rating. NHTSA says low rolling resistance replacement tires improve fuel economy and extend the range of electric and hybrid vehicles."),
        ("How much fuel do low rolling resistance tires save?", "NHTSA estimates that a 10 percent cut in rolling resistance improves fuel economy by 1 to 2 percent. Your result depends on the tire you are replacing and how you drive."),
        ("Do I need XL or HL tires on my hybrid?", "Only if the placard or original tires call for them. Michelin says if the vehicle specifies XL or HL, replacements must carry that designation, an HL tire must be replaced with HL, and HL can replace XL."),
        ("Can I put regular all season tires on a hybrid?", "Yes, if they match the placard size, load index and speed rating. Prefer a model the maker describes as low rolling resistance if fuel economy matters to you."),
        ("Does tire pressure affect hybrid mpg?", "Yes. FuelEconomy.gov says under inflation lowers gas mileage by about 0.2 percent for every 1 psi drop in average pressure, and proper inflation improves mileage by 0.6 percent on average. Use the door jamb pressure, not the sidewall maximum."),
        ("Should I replace original equipment tires with the same model?", "Where the original tires carry an automaker marking, Michelin recommends replacing them with the same approved marking when possible, because those tires are tuned for the vehicle's handling, noise and rolling resistance targets.")],
  srcs=[("NT", "low rolling resistance tires, fuel economy estimate, hybrids and EVs"), ("MPH", "plug in hybrid load, XL or HL, rolling resistance, noise, wear and rotation"), ("MHL", "HL tires for hybrids and EVs, HL replacement rules"), ("MOE", "automaker marked original equipment tires"), ("MSZ", "wider tires and rolling resistance, factory size"), ("FEG", "tire pressure and gas mileage"), ("CS", "size, load, speed rating and mixing rules")],
  related=[("/which-tire/", "Which tire picker"), ("/which-tire/electric-vehicle/", "Which tire for an EV"), ("/which-tire/highway-commuting/", "Which tire for highway commuting"), ("/guides/xl-vs-sl-tires/", "XL vs SL tires"), ("/guides/tire-pressure/", "Tire pressure"), ("/guides/utqg/", "UTQG grades")])

# 20 Nov 2026: /which-tire/awd/ and /which-tire/ice/ are hand written HTML.
# The live picker (which-tire/index.html) has the AWD vehicle option and the ice branch.
# Do not run this script until those branches are copied into the picker string below,
# or a rebuild will drop them and overwrite the hand written pages.
def build():
    urls = []
    for k in PAGES: urls.append(page(**k))
    # HUB
    cards = "\n".join(f'        <article class="card"><h2>{esc(k["h1"])}</h2><p>{esc(re.sub("<[^>]+>","",k["lede"]))}</p><a class="card-link" href="/which-tire/{k["slug"]}/">Read the guide →</a></article>' for k in PAGES)
    body = f"""      <section class="content-section" id="picker">
        <h2>Which tire picker</h2>
        <p>Answer four questions. The picker runs only in your browser, needs no login and stores or sends nothing. It suggests a tire <b>category</b>, not a brand or model.</p>
        <form id="wt-picker" onsubmit="return false">
          <div class="calc-row"><label for="wt-veh">Vehicle</label><select id="wt-veh"><option value="car">Car or sedan</option><option value="suv">SUV or crossover</option><option value="truck">Pickup truck</option><option value="x4">Jeep style 4x4 or off-roader</option><option value="ev">Electric vehicle</option><option value="hyb">Hybrid or plug in hybrid</option><option value="van">Minivan</option><option value="sport">Sports car</option></select></div>
          <div class="calc-row"><label for="wt-clim">Climate</label><select id="wt-clim"><option value="mild">Mild, little snow</option><option value="rain">Lots of rain</option><option value="snow">Snow or ice in winter</option><option value="hot">Hot, rarely below freezing</option></select></div>
          <div class="calc-row"><label for="wt-drive">Driving</label><select id="wt-drive"><option value="commute">Commuting and errands</option><option value="highway">Lots of highway miles</option><option value="offroad">Gravel, dirt or off road</option><option value="perf">Spirited or performance</option><option value="tow">Towing or heavy hauling</option></select></div>
          <div class="calc-row"><label for="wt-pri">Top priority</label><select id="wt-pri"><option value="quiet">Quiet and comfort</option><option value="life">Long tread life</option><option value="budget">Budget</option><option value="grip">Grip</option></select></div>
          <div class="calc-result" id="wt-out" aria-live="polite"></div>
        </form>
        <p class="note">A rough guide based on the general guidance in the sources below. Your door placard, the vehicle maker and a licensed installer take priority.</p>
      </section>
      <section class="content-section">
        <h2>Tire categories in plain English</h2>
        <table>
          <thead><tr><th>Category</th><th>Built for</th><th>Trade off</th></tr></thead>
          <tbody>
            <tr><td>Standard touring all season</td><td>Tread life, comfort; cars, vans, crossovers ({a('TRA','Tire Rack')})</td><td>Weaker wet grip, and a longer 60 to 0 mph stop than grand touring for one tire in Tire Rack's test ({a('TRC','Tire Rack')})</td></tr>
            <tr><td>Grand touring all season</td><td>The all round choice for most drivers ({a('TRC','Tire Rack')})</td><td>Not the best at any single thing</td></tr>
            <tr><td>Highway or crossover/SUV touring all season</td><td>SUVs and trucks on pavement; quiet ride ({a('TRT','Tire Rack')})</td><td>Only light off road use ({a('TRH','Tire Rack')})</td></tr>
            <tr><td>All weather (3PMSF)</td><td>One set that passed a packed snow test ({a('T37','USTMA TISB 37')})</td><td>Test does not cover pure ice ({a('MTY','Michelin')})</td></tr>
            <tr><td>Dedicated winter</td><td>Cold, snow, ice, slush; stays flexible below about 45°F ({a('MSW','Michelin')})</td><td>Not for year round use ({a('MTY','Michelin')})</td></tr>
            <tr><td>All terrain / mud terrain</td><td>Loose dirt, sand, mud, rocks ({a('TRH','Tire Rack')})</td><td>More noise, less wet grip on pavement</td></tr>
            <tr><td>Ultra high performance all season</td><td>More grip than touring, year round</td><td>Firmer ride, weaker in snow ({a('TRC','Tire Rack')})</td></tr>
            <tr><td>Max performance summer</td><td>Best wet and dry grip in warm weather ({a('TRC','Tire Rack')})</td><td>Hardens below about 45°F ({a('MSW','Michelin')})</td></tr>
            <tr><td>LT (load range C to F)</td><td>Heavy hauling, towing, rough use ({a('TRT','Tire Rack')})</td><td>Needs higher pressure; firmer ride ({a('CS','USTMA')})</td></tr>
            <tr><td>EV fitments (HL or XL, low rolling resistance)</td><td>Heavy battery vehicles, range ({a('MHL','Michelin')}, {a('CEV','Continental')})</td><td>Faster wear on average ({a('MEV','Michelin')})</td></tr>
          </tbody>
        </table>
      </section>
      <section class="content-section">
        <h2>Five marks to check on any tire</h2>
        <ul>
          <li><b>Size and load index:</b> never smaller or with less load capacity than the original at placard pressure ({a('CS','USTMA')}). <a href="/guides/load-index-speed-rating/">Load index guide</a>.</li>
          <li><b>Speed rating:</b> equal to or higher than the vehicle maker specifies ({a('CS','USTMA')}).</li>
          <li><b>UTQG:</b> treadwear, traction (AA to C, straight ahead wet braking only) and temperature (A to C) grades ({a('ECFR','49 CFR 575.104')}). <a href="/guides/utqg/">UTQG guide</a>.</li>
          <li><b>3PMSF vs M+S:</b> 3PMSF requires a packed snow test; M+S does not ({a('MTY','Michelin')}).</li>
          <li><b>LT vs P, and HL or XL:</b> never mix passenger and LT tires on one vehicle ({a('CS','USTMA')}); replace HL with HL ({a('T54','USTMA TISB 54')}). <a href="/guides/lt-vs-p-metric-tires/">LT vs P guide</a>.</li>
        </ul>
      </section>
      <p class="section-label">Which tire for...</p>
      <div class="card-grid">
{cards}
        <article class="card"><h2>All weather vs all season vs winter</h2><p>How the sidewall marks differ and which type fits your winters.</p><a class="card-link" href="/guides/all-weather-vs-all-season/">Read the guide →</a></article>
      </div>
"""
    tail = """<style>.calc-row{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:.5rem 0}.calc-row label{min-width:9rem;font-weight:600}.calc-row select{padding:.4rem;max-width:22rem}.calc-result{margin-top:1rem;padding:1rem;border:1px solid #9ec5ff;border-radius:8px}.calc-result h3{margin-top:0}</style>
<script>
(function(){
  var $=function(i){return document.getElementById(i)};
  var CHECK='Before you buy: match the size and load index on your door placard (never lower), keep a speed rating at least as high as the vehicle maker specifies, and buy four alike.';
  function rec(v,c,d,p){
    var r={cat:'',why:[],link:'',label:'',also:[]};
    if(d==='tow'){r.cat='Load first: the load range your vehicle specifies (often LT, such as Load Range E on heavier pickups), in a highway all season tread';r.why=['Towing is about load capacity and the right pressure, which NHTSA says may need to be higher when towing.','LT tires use thicker plies and reinforced sidewalls for heavy hauling.'];r.link='/which-tire/towing/';r.label='Which tire for towing';if(v==='car'||v==='van'||v==='ev'||v==='sport')r.why.push('On a car, van or EV, stay with the placard size and load index and the tow rating in your owner\\'s manual.');return r;}
    if(v==='x4'){if(d==='offroad'){r.cat=(p==='grip')?'Mud terrain (LT) if you face deep mud, loose soil or rock often; otherwise all terrain':'All terrain (LT if your 4x4 came with LT)';}else if(d==='commute'||d==='highway'){r.cat=(p==='quiet'||p==='life')?'Highway all season, or all terrain if you take trails on weekends':'All terrain, or highway all season if you rarely leave pavement';}else{r.cat='All terrain';}r.why=['All terrain tires are quieter and handle better on the road than mud terrain while still managing moderate trails.','Mud terrain tires trade noise, fuel economy and tread life for grip in deep mud and rock.','Do not mix all terrain and all season tread on a 4WD, and keep LT if it came with LT.'];if(c==='snow')r.why.push('For snow, look for the 3PMSF symbol; M+S alone is not a snow test.');r.link='/which-tire/4x4-off-road/';r.label='Which tire for a Jeep style 4x4';return r;}
    if(d==='offroad'){
      if(v==='truck'||v==='suv'){r.cat=(p==='grip')?'All terrain (or mud terrain if you face deep mud or rock often)':'All terrain, or highway all season if your gravel is well graded';r.why=['All terrain tires dig through loose dirt, sand, mud and rocks.','They are louder and grip less in the wet on pavement than highway tires.'];if(c==='snow')r.why.push('For snow, look for the 3PMSF symbol; it is printed on some all terrain sizes.');r.link='/which-tire/gravel-roads/';r.label='Which tire for gravel and dirt roads';return r;}
      r.cat=(c==='snow')?'All weather with the 3PMSF symbol, in your placard size':'Touring all season in your placard size';r.why=['Cars and minivans rarely offer all terrain sizes; a durable all season handles graded gravel.','Keep the original size and load index.'];r.link='/which-tire/gravel-roads/';r.label='Which tire for gravel roads';return r;}
    if(c==='snow'&&!(v==='sport'&&d==='perf')){
      r.cat=(p==='grip')?'Dedicated winter tires on all four wheels (with a second set for summer)':'All weather with the 3PMSF symbol, or dedicated winter tires for regular ice';
      r.why=['3PMSF means the tire passed a packed snow traction test; M+S alone does not.','Dedicated winter tires stay flexible below about 45°F and lead on ice.'];
      if(v==='ev')r.why.push('On an EV, keep HL or XL load ratings if the placard calls for them.');
      if(v==='hyb'){r.why.push('On a hybrid, keep XL or HL if the placard calls for it and prefer low rolling resistance.');r.also.push(['/which-tire/hybrid/','Which tire for a hybrid']);}
      if(v==='truck')r.why.push('Keep LT construction if your truck came with it.');
      r.link='/which-tire/snow-without-winter-tires/';r.label='Which tire for snow without winter tires';r.also=[['/guides/winter-tires/','Winter tires guide']];return r;}
    if(v==='sport'||d==='perf'){
      if(c==='snow'){r.cat='Ultra high performance all season, plus a winter set';r.why=['Summer tires harden below about 45°F.','UHP all season tires grip better than touring tires but are weaker in snow.'];}
      else if(p==='quiet'||p==='life'||p==='budget'){r.cat='Ultra high performance all season';r.why=['More grip than touring tires with year round use.','Expect a firmer ride than touring tires.'];}
      else{r.cat='Max performance summer';r.why=['Best wet and dry grip of the street categories in Tire Rack\\'s test.','Only for weather that stays above about 45°F.'];}
      r.link='/which-tire/sports-car/';r.label='Which tire for a sports car';return r;}
    if(v==='hyb'){r.cat='Low rolling resistance '+(c==='hot'?'touring all season':'touring all season, or all weather with 3PMSF')+', in the placard size and load rating (XL or HL if specified)';r.why=['NHTSA says low rolling resistance tires improve fuel economy and extend hybrid and EV range.','If the placard or original tires say XL or HL, the replacement must match.','A wider size than the placard raises rolling resistance.'];r.link='/which-tire/hybrid/';r.label='Which tire for a hybrid';return r;}
    if(v==='ev'){r.cat='EV fitment: HL or XL as the placard requires, low rolling resistance, in a '+(c==='hot'?'touring all season or summer':'touring all season or all weather')+' tread';r.why=['If the original tires are HL, replacements must be HL.','Low rolling resistance helps range; quiet construction matters without engine noise.','EVs wear tires about 20 percent faster on average, per Michelin.'];r.link='/which-tire/electric-vehicle/';r.label='Which tire for an EV';return r;}
    if(v==='truck'){r.cat=(p==='life'||p==='quiet'||p==='budget')?'Highway all season (P or LT as your placard specifies)':'Highway all season, or on road all terrain';r.why=['Highway all season tires are quieter and grip better in the wet on pavement.','Never mix P and LT tires on one truck.'];r.link='/which-tire/pickup-truck/';r.label='Which tire for a pickup truck';return r;}
    if(v==='suv'){r.cat='Crossover/SUV touring or highway all season';r.why=['Built for paved commuting with a quiet, comfortable ride.','All weather versions exist if you see snow.'];r.link='/which-tire/suv/';r.label='Which tire for an SUV';return r;}
    if(v==='van'){r.cat=(p==='quiet')?'Grand touring all season':'Standard touring all season';r.why=['Touring all season tires are designed for cars, vans and crossovers.','Make sure the load index covers a fully loaded van.'];r.link='/which-tire/minivan/';r.label='Which tire for a minivan';return r;}
    if(c==='hot'){r.cat=(p==='grip')?'Grand touring summer or max performance summer':'Grand or standard touring all season';r.why=['No winter capability needed where it stays above freezing.','Compare the UTQG temperature grade (A is highest) and keep pressure at the placard value.'];r.link='/which-tire/hot-climate/';r.label='Which tire for hot climates';return r;}
    if(c==='rain'){r.cat=(p==='grip')?'Ultra high performance all season with a high UTQG traction grade':'Grand touring all season with a high UTQG traction grade';r.why=['Compare UTQG traction grades (AA is highest) among tires in your size.','Traction grades measure straight ahead wet braking only, so keep tread depth healthy too.'];r.link='/which-tire/rain/';r.label='Which tire for rain';return r;}
    r.cat=(p==='life'||p==='budget')?'Standard touring all season':'Grand touring all season';
    r.why=(p==='life'||p==='budget')?['Focused on tread life; compare UTQG treadwear grades.','Expect slightly longer wet stops than grand touring.']:['The all round choice for most drivers: quiet, comfortable, good in most conditions.'];
    r.link='/which-tire/highway-commuting/';r.label='Which tire for highway commuting';return r;}
  function go(){
    var r=rec($('wt-veh').value,$('wt-clim').value,$('wt-drive').value,$('wt-pri').value);
    var h='<h3>Suggested category: '+r.cat+'</h3><ul>';r.why.forEach(function(w){h+='<li>'+w+'</li>'});
    h+='</ul><p>'+CHECK+'</p><p><a href="'+r.link+'">'+r.label+' →</a>';r.also.forEach(function(x){h+=' · <a href="'+x[0]+'">'+x[1]+'</a>'});
    $('wt-out').innerHTML=h+'</p>';}
  ['wt-veh','wt-clim','wt-drive','wt-pri'].forEach(function(i){$(i).addEventListener('change',go)});go();
})();
</script>
"""
    hub_faqs = [("Which tire should I buy for my car?", "Start with your door placard for size, load index and speed rating. Then choose a category: for most cars that is a grand touring all season tire, standard touring if tread life matters most, a 3PMSF all weather or winter tire if you get snow, or summer tires for warm weather performance."),
        ("Does this picker recommend brands?", "No. It recommends a tire category and what to check on the sidewall. We do not rank branded models unless we have a sourced review page."),
        ("What is the difference between all season and all weather tires?", "Michelin says all season tires carry M+S, based on tread design, while all weather tires carry the 3PMSF symbol, which requires passing a packed snow traction test."),
        ("Do I need to replace all four tires at once?", "USTMA says replacing all four at once is recommended and preferred, and on 4WD and AWD vehicles even small diameter differences can damage the drivetrain. See our mixing tires guide.")]
    hub_srcs = [("TRC", "category trade offs from a 2024 multi category test"), ("TRA", "touring and summer category descriptions"), ("TRT", "truck and SUV categories, LT construction"), ("TRH", "highway all season vs all terrain"), ("T37", "3PMSF definition"), ("MTY", "M+S vs 3PMSF, seasonal categories"), ("MSW", "45°F guidance"), ("MHL", "HL tires"), ("T54", "HL replacement"), ("MEV", "EV wear"), ("CEV", "EV rolling resistance and noise"), ("ECFR", "UTQG grades"), ("CS", "replacement and mixing rules"), ("NTOW", "towing pressure")]
    hub_rel = [("/guides/", "All tire guides"), ("/fitment/choose-tire-size/", "How to choose tire size"), ("/tools/tire-size-calculator/", "Tire size calculator"), ("/guides/mixing-tires/", "Mixing tires"), ("/guides/placard/", "Read your door placard")]
    urls.insert(0, page(slug="", crumb="", img="suv", title="Which tire should I get? Free tire type picker and guides",
        h1="Which tire should I get?", desc="Free which tire picker: pick vehicle, climate, driving and priority to get a tire category with plain English reasons. No login, no brands pushed.",
        lede="Tell us your vehicle, climate, driving and top priority, and the picker suggests a tire category with plain English reasons. Then use the guides below to check size, load index, speed rating and the snow symbol.",
        body=body, faqs=hub_faqs, srcs=hub_srcs, related=hub_rel, extra_tail=tail))
    return urls

if __name__ == "__main__":
    for u in build(): print(u)
