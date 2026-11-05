#!/usr/bin/env python3
"""Create three mechanic-focused FAQ guides: cold vs hot pressure, directional/asymmetric fitment, shop repair-or-replace."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
TODAY = "2026-11-05"
USTMA = "https://www.ustires.org/system/files/files/2024-05/Care%20and%20Service%20Passenger%20and%20Light%20Truck%20Tires%20FINAL%2006%2028%2017.pdf"
TIA = "https://www.tireindustry.org/"
NHTSA = "https://www.nhtsa.gov/equipment/tires"
BS = "https://www.bridgestoneamericas.com/en/company/safety/choosing-tires/determining-tire-size"

PAGES = []

def add(slug, title, h1, desc, alt, img_key, faq, sources, body_inner, related, hub_blurb, llms_blurb, home_label):
    PAGES.append(dict(slug=slug, title=title, h1=h1, desc=desc, alt=alt, img_key=img_key,
                      faq=faq, sources=sources, body_inner=body_inner, related=related,
                      hub_blurb=hub_blurb, llms_blurb=llms_blurb, home_label=home_label))

# ---- 1 cold vs hot ----
add(
 slug="cold-vs-hot-tire-pressure",
 title="Cold vs Hot Tire Pressure: Shop Rules for Mechanics",
 h1="Cold vs hot tire pressure: what mechanics should set and refuse",
 desc="Cold placard PSI vs hot bay readings: how much pressure rises after driving, why shops must not bleed hot tires, and a practical check SOP.",
 alt="Digital tire pressure gauge reading cold PSI on a passenger car wheel in a workshop",
 img_key="cold-hot-pressure",
 faq=[
  ("What is cold tire pressure?",
   "Cold tire pressure is the inflation measured before the tire has been warmed by driving or by sitting in hot sun that raises the reading. Vehicle door placards list recommended cold pressures. USTMA and vehicle makers expect you to set and judge pressure against that cold value."),
  ("How much does tire pressure rise when the tire is hot?",
   "As a working shop rule of thumb, pressure often rises about 4 to 6 psi after a normal drive as the air and tire warm up, and more after highway speeds or heavy load. The exact rise depends on speed, load, ambient temperature and starting pressure. Always treat a hot reading as elevated relative to the placard, not as a new target."),
  ("Should I bleed air from a hot tire that reads over the placard?",
   "No. USTMA warns never to reduce pressure when tires are hot. A hot tire that reads a few psi above the cold placard is usually normal. Bleeding it down can leave it underinflated once it cools, which builds heat and risks damage."),
  ("How should a shop check pressure on a car that just rolled in?",
   "Note that the tires are hot, record the hot readings for the work order if useful, then either ask the customer to return for a cold set or estimate only after explaining the limitation. Final set-to-placard work should be done cold whenever practical. Do not bleed hot tires down to the placard number."),
  ("Does TPMS change cold vs hot practice?",
   "TPMS warns about relative underinflation; it does not replace a gauge. After a cold fill to placard, a short drive may be needed before a lamp clears. A lamp that returns quickly on one corner still needs a leak inspection, not another hot bleed. See our TPMS guide."),
  ("Why do four tires gain pressure overnight in a hot shop bay?",
   "Ambient heat raises pressure roughly 1 to 2 psi per 10°F. A car that sat outside overnight in the cold then spends an hour in a warm bay will read higher even without road heat. Set to placard when the tire temperature matches the 'cold' condition the vehicle maker intends, usually before significant driving."),
 ],
 sources=[
  (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","cold inflation as the reference; never reduce pressure when tires are hot; temperature effects on inflation"),
  ("https://smarttirepicks.com/guides/tire-pressure/","Smart Tire Picks, Recommended cold tire pressure","placard vs sidewall max; 1–2 psi per 10°F ambient rule; spare caveats"),
  ("https://smarttirepicks.com/guides/tpms/","Smart Tire Picks, TPMS warning light guide","sensor warnings are prompts to gauge-check, not a complete diagnosis"),
 ],
 body_inner='''
      <section class="content-section">
        <h2>Cold is the spec; hot is a clue</h2>
        <p>Every US vehicle door placard lists <strong>cold</strong> inflation pressures. Mechanics who set or judge pressure against a hot bay reading without saying so will either overfill after the car cools or, worse, bleed a hot tire down to the placard and send it out underinflated. USTMA is direct: do not reduce pressure when tires are hot.</p>
        <p>Our consumer-facing <a href="/guides/tire-pressure/">cold tire pressure guide</a> covers placard versus sidewall max and the ambient 1 to 2 psi per 10°F rule. This page is the shop angle: what to do when the car is already warm.</p>
      </section>
      <section class="content-section">
        <h2>How much rise to expect</h2>
        <ul>
          <li><strong>After a normal local drive:</strong> often about 4 to 6 psi above the true cold starting pressure.</li>
          <li><strong>After highway or heavy load:</strong> more rise; do not chase the gauge back to placard while hot.</li>
          <li><strong>From bay heat alone:</strong> a cold car pulled into a warm shop can pick up 1 to 2 psi per 10°F of ambient change without turning a wheel.</li>
        </ul>
        <p>These are working estimates for training, not a universal formula. When the work order requires a documented set-to-placard, schedule or wait for a cold measurement.</p>
      </section>
      <section class="content-section">
        <h2>Shop SOP that keeps you out of trouble</h2>
        <ol>
          <li>Ask how far the car just drove. If it is hot, write “hot reading” next to the gauge numbers.</li>
          <li>Inspect for obvious damage, embedded objects and uneven wear before arguing about a couple of psi.</li>
          <li>Never bleed a hot tire down to the placard. Explain to the customer why the higher number is expected.</li>
          <li>Final inflation to placard happens cold — before the car is driven hard, or on a return visit.</li>
          <li>After a cold fill, road-test or advise that a TPMS lamp may need a short drive to clear. See <a href="/guides/tpms/">TPMS</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Related pressure mistakes</h2>
        <ul>
          <li>Using the big sidewall number as the target (that is usually a maximum construction pressure, not the vehicle load pressure).</li>
          <li>Matching all four corners to each other while ignoring axle-specific placard values.</li>
          <li>Copying road-tire PSI onto a T-type spare. Confirm the spare marking; see the cold pressure guide.</li>
        </ul>
      </section>
''',
 related=[
  ("/guides/tire-pressure/","Cold tire pressure guide"),
  ("/guides/tpms/","TPMS warning light"),
  ("/guides/placard/","How to read the door placard"),
  ("/guides/nitrogen-vs-air/","Nitrogen vs air"),
  ("/guides/","All tire guides"),
 ],
 hub_blurb="Cold placard PSI vs hot bay readings, why shops must not bleed hot tires, and a practical check SOP for mechanics.",
 llms_blurb="Cold vs hot tire pressure for mechanics: placard is cold; hot tires often read 4–6 psi higher after driving; USTMA says never bleed hot tires; shop SOP for hot arrivals; ambient 1–2 psi per 10°F; links to cold pressure and TPMS guides. Cites USTMA.",
 home_label="Cold vs hot tire pressure (shop rules)",
)

# ---- 2 directional / asymmetric fitment ----
add(
 slug="directional-asymmetric-fitment",
 title="Directional and Asymmetric Tire Fitment for Shops",
 h1="Directional and asymmetric tire fitment: mounting rules for shops",
 desc="How to mount directional and asymmetric tires correctly: rotation arrows, outside sidewalls, staggered axles, and when a tire cannot move to the other side.",
 alt="Close-up of a tire sidewall and tread in a shop with wheel weights nearby",
 img_key="directional-fitment",
 faq=[
  ("What is a directional tire?",
   "A directional tire has a tread pattern designed to roll in one direction, usually marked with a rotation arrow on the sidewall. Mounted correctly, the arrow points forward when the tire is on the vehicle. Mounting it backwards hurts wet traction and noise performance the pattern was built for."),
  ("What is an asymmetric tire?",
   "An asymmetric tire has different inner and outer tread zones. The sidewall is marked with an outside (or similar) cue that must face outboard. Unlike many directional tires, a correctly mounted asymmetric tire can usually move front to rear on the same side during rotation."),
  ("Can I rotate directional tires side to side?",
   "Not without demounting them from the wheels. A directional tire that simply swaps left to right would then rotate the wrong way. Same-side front-to-rear rotation keeps the arrow correct. If a full cross rotation is required, the tire must be broken down and remounted on the opposite wheel."),
  ("What if the customer bought the wrong outside facing?",
   "Do not ignore an outside marking to make a sale fit. Remount so outside faces outboard. If the set is staggered with different front and rear sizes, confirm each axle’s size, load index and speed rating before mounting. See load index and choose-size guides."),
  ("Do run-flat or XL markings change orientation rules?",
   "No. Construction tags such as run-flat, XL or load range do not replace rotation arrows or outside labels. Read every cue on both sidewalls before the bead reaches the rim."),
  ("How should a work order document fitment orientation?",
   "Note directional or asymmetric, arrow direction verified, outside facing verified, and any remount required for cross rotation. Photos of the sidewall marks before and after help if a noise or pull complaint returns."),
 ],
 sources=[
  (BS,"Bridgestone Americas, How to Read and Determine Tire Size","sidewall service description and construction cues; fitment must match vehicle requirements"),
  (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","replacement tires should match size and meet or exceed load and speed capability; professional mounting"),
  ("https://smarttirepicks.com/fitment/choose-tire-size/","Smart Tire Picks, How to choose the right tire size","placard-first size selection before pattern orientation"),
  ("https://smarttirepicks.com/guides/load-index-speed-rating/","Smart Tire Picks, Load index and speed rating","match or exceed OEM load index and appropriate speed rating"),
 ],
 body_inner='''
      <section class="content-section">
        <h2>Read the sidewall before the machine spins</h2>
        <p>Pattern type is a fitment gate, not a cosmetic note. <strong>Directional</strong> tires carry a rotation arrow. <strong>Asymmetric</strong> tires carry an outside (or inside) label. Some performance tires are both. Mounting past those marks creates noise, irregular wear and weak wet performance the customer will blame on the brand — or on your shop.</p>
      </section>
      <section class="content-section">
        <h2>Mounting checklist</h2>
        <ol>
          <li>Confirm size, load index and speed rating against the placard and the order. Orientation never excuses a lower load index.</li>
          <li>Find rotation arrows and outside labels on both sidewalls before lubricating the bead.</li>
          <li>On directional tires, the arrow must point forward once the wheel is on the hub.</li>
          <li>On asymmetric tires, the outside mark must face outboard.</li>
          <li>Torque lug nuts in stages to the vehicle spec after the car is down; re-torque per shop policy.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Rotation limits shops forget</h2>
        <p>Same-side front-to-rear rotation keeps directional arrows honest. A left-right swap of a directional tire without demounting reverses the tread. Cross patterns that look neat on a poster may require breaking the bead. Staggered fitments (different front and rear sizes) cannot swap axles at all — only left-right on the same axle when the pattern allows.</p>
        <p>For size and plus-sizing gates before pattern work, use <a href="/fitment/choose-tire-size/">how to choose tire size</a> and <a href="/guides/plus-sizing/">plus sizing</a>. For capacity marks, see <a href="/guides/load-index-speed-rating/">load index and speed rating</a> and <a href="/guides/xl-vs-sl-tires/">XL vs SL</a>.</p>
      </section>
      <section class="content-section">
        <h2>When to refuse the mount</h2>
        <ul>
          <li>Customer insists on ignoring an outside or arrow mark.</li>
          <li>Replacement load index or speed rating is below OEM requirements without written vehicle-maker approval.</li>
          <li>Staggered sizes mixed across an axle.</li>
          <li>Damaged beads, visible cords, or a tire already repaired outside industry limits (see our shop repair-or-replace guide).</li>
        </ul>
      </section>
''',
 related=[
  ("/fitment/choose-tire-size/","How to choose the right tire size"),
  ("/guides/load-index-speed-rating/","Load index and speed rating"),
  ("/guides/xl-vs-sl-tires/","XL vs SL tires"),
  ("/guides/plus-sizing/","Plus sizing"),
  ("/guides/tire-rotation/","Tire rotation"),
  ("/guides/","All tire guides"),
 ],
 hub_blurb="Rotation arrows, outside sidewalls, staggered axles, and when a tire must be demounted to move sides.",
 llms_blurb="Directional and asymmetric tire fitment for shops: rotation arrows must face forward; outside labels face outboard; directional tires need demount to swap sides; staggered axles cannot cross; refuse mounts that ignore marks or under-spec load index. Cites Bridgestone, USTMA.",
 home_label="Directional and asymmetric fitment",
)

# ---- 3 shop repair or replace ----
add(
 slug="shop-repair-or-replace",
 title="Tire Repair or Replace: Shop Decision Guide",
 h1="Tire repair or replace: a shop decision guide for mechanics",
 desc="When shops should repair a puncture vs replace: tread-area limits, sidewall no-repair zones, run-flats, age and prior plugs.",
 alt="Punctured tire on a changer with chalk marking the injury and shop gloves nearby",
 img_key="shop-repair-replace",
 faq=[
  ("When is a puncture repairable?",
   "Industry guidance (USTMA / TIA style limits taught in shops) allows proper repair only for injuries in the central tread area roughly between the shoulder belts, typically no larger than 1/4 inch (6 mm), repaired from the inside with a vulcanized patch-plug stem unit after the tire is demounted. Outside those limits, replace."),
  ("Why is a sidewall puncture a replace?",
   "Sidewalls and shoulders flex continuously and lack the same belt support as the tread center. A plug or patch there is not considered a lasting structural repair. Mark it, photograph it, and quote a replacement."),
  ("Is an external string plug alone enough?",
   "No. A string plug from the outside is a roadside temporary measure at best. The accepted permanent repair is an inside patch-plug combination with the tire off the wheel. See our plug vs patch guide for the consumer explanation of the same rule."),
  ("Should run-flat tires be repaired?",
   "Follow the tire maker. Many run-flat makers restrict or prohibit repair after the tire has carried load while flat, because the sidewall may already be damaged. If maker policy is unclear, replace. Our run-flat guide summarises common maker limits."),
  ("Does tire age force a replace even if the hole is small?",
   "Age alone is not the puncture rule, but many shops refuse repair on tires with six or more years of service, visible cracking, prior improper repairs, or tread at or below legal/safety limits. Document DOT week/year and tread depth on the work order. See when-to-replace and DOT date guides."),
  ("What should the work order show when you refuse a repair?",
   "Injury location (tread / shoulder / sidewall), measured size, whether the tire was demounted for inspection, prior repairs found, maker repair policy if relevant, and a clear replace recommendation. Photos protect the shop and the customer."),
 ],
 sources=[
  (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","puncture repair limits; professional inspection with tire demounted; replacement when repair criteria are not met"),
  ("https://smarttirepicks.com/guides/tire-plug-vs-patch/","Smart Tire Picks, Tire plug vs patch","plug-patch combo, 1/4 inch tread-area rule, why plug-only is not a proper repair"),
  ("https://smarttirepicks.com/guides/run-flat-tires/","Smart Tire Picks, Run flat tires explained","maker-specific repair restrictions after deflated running"),
  ("https://smarttirepicks.com/guides/when-to-replace/","Smart Tire Picks, When to replace tires","tread depth, age and damage replacement cues"),
 ],
 body_inner='''
      <section class="content-section">
        <h2>Repair is a narrow window</h2>
        <p>Customers hear “it’s just a nail.” Shops answer to the injury location, size and the tire’s history. USTMA-style guidance used across the industry limits permanent repair to small punctures in the <strong>central tread area</strong>, done from the <strong>inside</strong> with a proper patch-plug unit after demounting. Everything else is a replace conversation.</p>
        <p>For the consumer-facing version of plug versus patch chemistry, see <a href="/guides/tire-plug-vs-patch/">tire plug vs patch</a>. This page is the bay decision tree.</p>
      </section>
      <section class="content-section">
        <h2>Replace immediately when</h2>
        <ul>
          <li>Injury is in the sidewall or shoulder (outside the repairable tread belt area).</li>
          <li>Tread puncture is larger than about 1/4 inch (6 mm), or there are multiple injuries too close together.</li>
          <li>Cord, belt or inner liner is exposed, kinked or separated.</li>
          <li>The tire ran flat or very low long enough to heat-damage the structure (common on run-flats).</li>
          <li>An old outside string plug is the only prior “repair,” and a full inner inspection fails the limits above.</li>
          <li>Tread is already at replacement depth, or the carcass shows dry rot / bead damage.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>Repair only when all of these are true</h2>
        <ol>
          <li>Injury sits in the central tread area.</li>
          <li>Diameter is within the industry 1/4 inch style limit after probing.</li>
          <li>Tire is demounted; inner liner is inspected and prepared.</li>
          <li>A combined patch-plug (or equivalent maker-approved unit) is installed per procedure.</li>
          <li>Maker policy allows repair for that construction (especially run-flats).</li>
        </ol>
        <p>If any box fails, quote replacement. Pair the quote with <a href="/guides/when-to-replace/">when to replace</a> and <a href="/guides/dot-date-codes/">DOT date codes</a> so age and tread are on the same ticket.</p>
      </section>
      <section class="content-section">
        <h2>Talking to the customer without the argument</h2>
        <p>Show the chalk mark on the shoulder or sidewall. Show the inner liner if you demounted. Explain that a cheap outside plug skips the inspection that finds belt damage. Offer to transfer a road-hazard policy if one exists. Keep the refused repair on the invoice so the next shop is not guessing.</p>
      </section>
''',
 related=[
  ("/guides/tire-plug-vs-patch/","Tire plug vs patch"),
  ("/guides/when-to-replace/","When to replace tires"),
  ("/guides/run-flat-tires/","Run flat tires explained"),
  ("/guides/dot-date-codes/","DOT date codes"),
  ("/guides/sidewall-bulge/","Sidewall bulge"),
  ("/guides/","All tire guides"),
 ],
 hub_blurb="When to repair a puncture versus replace: tread-area limits, sidewall no-repair zones, run-flats, age and prior plugs.",
 llms_blurb="Shop repair-or-replace decision guide: USTMA/TIA-style limits — central tread only, about 1/4 inch max, inside patch-plug after demount; sidewall/shoulder replace; run-flat maker limits; document refused repairs. Links plug vs patch, when to replace, run-flat, DOT dates. Cites USTMA.",
 home_label="Repair or replace (shop guide)",
)

def faq_ld(faq):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^<]+?>','',a)}} for q,a in faq]}, indent=2)

def art_ld(p, url):
    org={"@type":"Organization","@id":"https://smarttirepicks.com/#organization","name":"Smart Tire Picks"}
    img=f"https://smarttirepicks.com/assets/img/og-{p['img_key']}.jpg"
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":p["h1"],"description":p["desc"],"mainEntityOfPage":{"@type":"WebPage","@id":url},"author":org,"publisher":org,"image":img,"datePublished":TODAY,"dateModified":TODAY,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":"https://smarttirepicks.com/#website","name":"Smart Tire Picks"}}, indent=2)

def bc_ld(name, url):
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},
      {"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},
      {"@type":"ListItem","position":3,"name":name,"item":url}]}, indent=2)

def build_one(p, position):
    slug=p["slug"]; url=f"https://smarttirepicks.com/guides/{slug}/"
    assert len(p["title"])<=60 and len(p["desc"])<=160, (len(p["title"]), len(p["desc"]), p["title"])
    img=p["img_key"]; alt=p["alt"]
    faq_html="\n".join(f"        <h3>{q}</h3>\n        <p>{a}</p>" for q,a in p["faq"])
    src_html="\n".join(f'          <li><a href="{u}" rel="noopener noreferrer" target="_blank">{t}</a>: {n}</li>' for u,t,n in p["sources"])
    rel_html="\n".join(f'          <li><a href="{u}">{t}</a></li>' for u,t in p["related"])
    body=f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{p["h1"]}</h1>
<p class="lede">{p["desc"]}</p>
<p class="last-updated">Last updated: November 5, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/{img}-1024.webp" srcset="/assets/img/{img}-640.webp 640w, /assets/img/{img}-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{alt}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
<aside class="disclaimer-box" role="note"><p><em>This page is for general information only and is not professional, safety, or legal advice. Always confirm tire size, load index, speed rating, and other specs against your vehicle’s door placard and owner’s manual, and have tires installed by a licensed professional. See our <a href="/disclaimer/">Disclaimer</a>.</em></p></aside>
{p["body_inner"]}      <section class="content-section faq">
        <h2>Frequently asked questions</h2>
{faq_html}
      </section>
      <section class="content-section sources">
        <h2>Sources</h2>
        <ul>
{src_html}
        </ul>
      </section>
      <nav class="related-links" aria-label="Keep reading">
        <h2>Keep reading</h2>
        <ul>
{rel_html}
        </ul>
      </nav>
    </div>
  </main>'''
    t=(R/"guides/speedometer-error-tire-size/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/speedometer-error-tire-size/", f"guides/{slug}/")
    head=re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", head)
    for prop in ["og:title","twitter:title"]:
        head=re.sub(rf'(property|name)="{prop}" content="[^"]*"', rf'\1="{prop}" content="{p["title"]}"', head)
    for prop in ['name="description"','property="og:description"','name="twitter:description"']:
        head=re.sub(rf'{prop} content="[^"]*"', f'{prop} content="{p["desc"]}"', head)
    for prop in ["og:image:alt","twitter:image:alt"]:
        head=re.sub(rf'"{prop}" content="[^"]*"', f'"{prop}" content="{alt}"', head)
    og=f"https://smarttirepicks.com/assets/img/og-{img}.jpg"
    head=re.sub(r'(property="og:image" content=")[^"]*"', rf'\g<1>{og}"', head)
    head=re.sub(r'(name="twitter:image" content=")[^"]*"', rf'\g<1>{og}"', head)
    head=re.sub(r'(property="og:image:width" content=")\d+"', r'\g<1>1200"', head)
    head=re.sub(r'(property="og:image:height" content=")\d+"', r'\g<1>675"', head)
    short=p["h1"].split(":")[0].strip()
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',
                lambda m: "<script type=\"application/ld+json\">\n"+bc_ld(short,url)+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld(p,url)+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld(p["faq"])+"\n  </script>\n</head>",
                head, flags=re.S)
    d=R/f"guides/{slug}"; d.mkdir(exist_ok=True)
    # keep hero.jpg as source asset too
    (d/"index.html").write_text(head+body+foot)
    return url, position, short

# Build pages
built=[]
for i,p in enumerate(PAGES):
    url, pos, short = build_one(p, 32+i)
    built.append((p, url, 32+i, short))
    print("built", p["slug"], "title_len", len(p["title"]), "desc_len", len(p["desc"]))

# Hub ItemList + cards
hub=R/"guides/index.html"; hs=hub.read_text()
last_item='''        "url": "https://smarttirepicks.com/guides/lt-vs-p-metric-tires/"
      }'''
if "cold-vs-hot-tire-pressure" not in hs:
    extra=[]
    for p, url, pos, short in built:
        extra.append(f''',
      {{
        "@type": "ListItem",
        "position": {pos},
        "name": "{short}",
        "url": "{url}"
      }}''')
    hs=hs.replace(last_item, last_item[:-1]+"".join(extra)+"\n      }", 1)
last_card='''          <a class="card-link" href="/guides/lt-vs-p-metric-tires/">Read the guide →</a>
        </article>'''
if 'href="/guides/cold-vs-hot-tire-pressure/"' not in hs:
    cards=""
    for p, url, pos, short in built:
        cards += f'''
        <article class="card">
          <h3>{short}</h3>
          <p>{p["hub_blurb"]}</p>
          <a class="card-link" href="/guides/{p["slug"]}/">Read the guide →</a>
        </article>'''
    assert last_card in hs
    hs=hs.replace(last_card, last_card+cards, 1)
hub.write_text(hs)

# Home new button + inline link
home=R/"index.html"; ho=home.read_text()
first=built[0]
ho=ho.replace('<a class="btn btn-ghost" href="/guides/lt-vs-p-metric-tires/">New: LT vs P metric tires explained</a>',
              f'<a class="btn btn-ghost" href="/guides/{first["slug"]}/">New: Cold vs hot tire pressure for shops</a>')
# sprinkle names near LT link if present
if f'/guides/{first["slug"]}/' not in ho or ho.count(f'/guides/{first["slug"]}/')<2:
    ho=ho.replace('<a href="/guides/lt-vs-p-metric-tires/">LT vs P tires</a>,',
                  f'<a href="/guides/lt-vs-p-metric-tires/">LT vs P tires</a>, <a href="/guides/{first["slug"]}/">cold vs hot pressure</a>, <a href="/guides/directional-asymmetric-fitment/">directional fitment</a>, <a href="/guides/shop-repair-or-replace/">repair or replace</a>,',1)
home.write_text(ho)

# Related links on a few existing guides
link_map = {
  "guides/tire-pressure": ("/guides/cold-vs-hot-tire-pressure/", "Cold vs hot tire pressure (shop rules)"),
  "guides/tpms": ("/guides/cold-vs-hot-tire-pressure/", "Cold vs hot tire pressure (shop rules)"),
  "guides/tire-plug-vs-patch": ("/guides/shop-repair-or-replace/", "Repair or replace (shop guide)"),
  "guides/when-to-replace": ("/guides/shop-repair-or-replace/", "Repair or replace (shop guide)"),
  "guides/tire-rotation": ("/guides/directional-asymmetric-fitment/", "Directional and asymmetric fitment"),
  "fitment/choose-tire-size": ("/guides/directional-asymmetric-fitment/", "Directional and asymmetric fitment"),
}
for g,(href,label) in link_map.items():
    fp=R/f"{g}/index.html"
    if not fp.exists():
        print("missing", g); continue
    s=fp.read_text()
    if href in s: continue
    li=f'          <li><a href="{href}">{label}</a></li>\n'
    s2,n=re.subn(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)', lambda m:m.group(1)+li, s, count=1)
    if n:
        fp.write_text(s2); print("linked", g)
    else:
        print("no related nav", g)

# sitemap
sm=R/"sitemap.xml"; ss=sm.read_text()
for p, url, pos, short in built:
    if p["slug"] in ss: continue
    img=f'https://smarttirepicks.com/assets/img/{p["img_key"]}-1024.webp'
    entry=f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>{img}</image:loc><image:caption>{p["alt"]}</image:caption></image:image></url>\n'
    ss=ss.replace('</urlset>', entry+'</urlset>')
for u in ["","guides/","guides/tire-pressure/","guides/tire-plug-vs-patch/","fitment/choose-tire-size/"]:
    ss=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*', rf'\g<1>{TODAY}', ss)
sm.write_text(ss)

# llms
ll=R/"llms.txt"; lt=ll.read_text()
block=""
for p, url, pos, short in built:
    if p["slug"] in lt: continue
    block += f'- [{short}]({url}): {p["llms_blurb"]}\n'
if block:
    lt=lt.replace("- [LT vs P metric tires]", block+"- [LT vs P metric tires]", 1)
    assert "cold-vs-hot-tire-pressure" in lt
    ll.write_text(lt)

print("ALL OK")
