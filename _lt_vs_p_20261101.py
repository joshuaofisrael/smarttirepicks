#!/usr/bin/env python3
"""Re-runnable: create /guides/lt-vs-p-metric-tires/, link it, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "lt-vs-p-metric-tires"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TODAY = "2026-11-01"
TITLE = "LT vs P Metric Tires: Load Range, Pressure and Swaps"
H1 = "LT vs P metric tires: load ranges, pressure and when a truck needs LT"
DESC = "How LT and P metric tires differ, what load range C, D and E mean, why LT tires need more pressure to carry the same load, and the rules for swapping."
ALT = "Alloy wheel and tire on a vehicle, illustrating light truck and passenger tire size markings"
USTMA = "https://www.ustires.org/system/files/files/2024-05/Care%20and%20Service%20Passenger%20and%20Light%20Truck%20Tires%20FINAL%2006%2028%2017.pdf"
BSSIZE = "https://www.bridgestoneamericas.com/en/company/safety/choosing-tires/determining-tire-size"
BSLT = "https://www.bridgestoneamericas.com/en/company/safety/choosing-tires/light-trucks-and-suvs"
TREV = "https://www.tirereview.com/tire-types-and-load-capacity/"
FAQ = [
 ("What is the difference between LT and P metric tires?", "P metric tires, with a P before the size, are passenger tires standardized by the Tire and Rim Association for cars, minivans, SUVs and lighter pickups. LT metric tires, with LT before the size, are light truck tires built for heavier loads; they run at higher pressures and carry two load index numbers and a load range letter."),
 ("What do load range C, D and E mean?", "Load range is the light truck strength rating that replaced ply ratings. For most LT sizes, load range C reaches maximum load at 50 psi, D at 65 psi and E at 80 psi. The old ply numbers (6, 8 and 10 ply) no longer mean the actual number of plies."),
 ("Why does an LT tire have two load index numbers?", "As in LT245/75R17 119/116R, the first number is the load index when the tire is used singly and the second is for dual rear wheels. Passenger tires have one number because they cannot be used in a dual application."),
 ("Can I put LT tires on a truck that came with P metric tires?", "Often yes, but the LT tire usually needs higher pressure than the placard to carry the same load. USTMA says to check that the wheels suit the higher pressure and to get the adjusted pressure and load rating from the vehicle maker, tire maker or a professional dealer. Bridgestone notes LT tires do not raise the vehicle's own load capacity."),
 ("Can I replace LT tires with P metric tires?", "Not unless the vehicle maker says so. USTMA does not recommend replacing original equipment LT metric, LT flotation or C type commercial tires with P metric or Euro metric passenger tires."),
 ("Can I mix LT and P metric tires on the same vehicle?", "No. USTMA says never to mix P metric or metric passenger tires with light truck tires, including C type European commercial tires, on the same vehicle."),
 ("Why is a P metric tire rated lower on a truck?", "USTMA says a passenger tire's load capacity must be divided by 1.10 when it is used on a light truck. Its example P265/70R17 carries 2535 lb in passenger use but 2305 lb in a light truck application."),
]
SOURCES = [
 (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","passenger tire load divided by 1.10 for light truck applications (P265/70R17 example, 2535 lb to 2305 lb); replacing passenger tires with LT tires needs a significant pressure adjustment and wheel checks; do not replace OE LT tires with P metric unless the vehicle maker specifies; never mix passenger and LT tires on one vehicle; LT load ranges B to E for vehicles up to 10,000 lb GVWR"),
 (BSSIZE,"Bridgestone Americas, How to Read and Determine Tire Size","P metric and Euro metric passenger formats; LT metric and C type light truck formats; single and dual load index numbers; load range as an older term; load index scales differ between standards"),
 (BSLT,"Bridgestone Americas, Light Truck and SUV Tire Information","benefits of switching to LT tires do not include more vehicle load capacity; LT tires may need higher than placard pressure to carry the same load; TPMS considerations; 35 psi minimum recommended for LT tires"),
 ("https://tires.bridgestone.com/en-us/learn/automotive/tire-terminology","Bridgestone, Tire Terminology","definition of the LT metric sizing system, for example LT235/85R16 120/116Q E"),
 (TREV,"Tire Review, Tire Types and Load Capacity","load range C, D and E inflate to 50, 65 and 80 psi (old 6, 8 and 10 ply); LT construction and trade offs; P265/75R16 114S at 35 psi needs an LT265/75R16 at 50 psi to carry the same load"),
]
PICK = """      <section class="content-section tool" id="lt-load-check">
        <h2>Passenger tire load on a truck: quick check</h2>
        <p>Enter the maximum load molded on your P metric or Euro metric tire's sidewall. This applies the USTMA 1.10 rule for light truck use. It runs entirely in your browser and nothing is sent or stored.</p>
        <form id="ltp-form" onsubmit="return false">
          <label>Max load per tire <input id="ltp-load" type="number" min="200" max="5000" step="1" value="2535"></label>
          <label>Unit <select id="ltp-unit"><option value="lb">lb</option><option value="kg">kg</option></select></label>
        </form>
        <p id="ltp-out" aria-live="polite"></p>
        <script>
        (function(){var l=document.getElementById('ltp-load'),u=document.getElementById('ltp-unit'),o=document.getElementById('ltp-out');
        function run(){var v=parseFloat(l.value);if(!(v>0)){o.textContent='Enter the load from the sidewall.';return;}
        var d=v/1.10,un=u.value;
        o.innerHTML='<strong>Light truck rating:</strong> about '+Math.round(d)+' '+un+' per tire, or '+Math.round(d*4)+' '+un+' for four tires, at the tire\\'s maximum load pressure. Compare with the axle ratings on your door placard; the vehicle\\'s own limits still apply.';}
        l.addEventListener('input',run);u.addEventListener('change',run);run();})();
        </script>
        <p>General explanation only. Always confirm with the vehicle placard, owner's manual, tire maker or a professional tire dealer.</p>
      </section>
"""
LR_ROWS = [("C","6 ply rated","50 psi (350 kPa)"),("D","8 ply rated","65 psi (450 kPa)"),("E","10 ply rated","80 psi (550 kPa)")]
BODY = f"""<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: <strong>P metric</strong> tires are passenger tires; <strong>LT</strong> tires are light truck tires with stronger construction, a <strong>load range</strong> letter (C, D or E) and higher pressures. An LT tire usually needs <strong>more air than the placard</strong> to carry the same load as the original passenger tire, and a passenger tire is rated about 10 percent lower on a light truck. Never mix the two on one vehicle.</p>
<p class="last-updated">Last updated: November 1, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/fitment-wheel-1024.webp" srcset="/assets/img/fitment-wheel-640.webp 640w, /assets/img/fitment-wheel-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
      <section class="content-section">
        <h2>How to tell them apart</h2>
        <ul>
          <li><strong>P metric:</strong> a P before the size, such as P225/70R16 97H. Bridgestone describes this as a Tire and Rim Association passenger car designation used on cars, minivans, SUVs and lighter pickups.</li>
          <li><strong>Euro metric:</strong> no letter in front, such as 225/70R16 98H. Also a passenger tire, under the European ETRTO standard.</li>
          <li><strong>LT metric:</strong> LT in front, such as LT245/75R17 119/116R Load Range E. Two load index numbers (single and dual use) plus a load range.</li>
          <li><strong>C type commercial:</strong> a C after the rim size, with two load index numbers. The European light truck and van equivalent.</li>
        </ul>
        <p>Bridgestone notes that load index numbers are not always on the same scale across standards, so check the actual load in pounds or kilograms, not just the index. See our <a href="/guides/load-index-speed-rating/">load index and speed rating guide</a>.</p>
      </section>
      <section class="content-section">
        <h2>Load range C, D and E</h2>
        <p>Load range replaced the old ply rating, and the ply number is now an equivalent strength rating rather than a count of plies. Tire Review gives the inflation each load range is built for:</p>
        <table class="data-table">
          <thead><tr><th>Load range</th><th>Old rating</th><th>Max load pressure</th></tr></thead>
          <tbody>
""" + "\n".join("            <tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in LR_ROWS) + f"""
          </tbody>
        </table>
        <p>Source: Tire Review. Some LT sizes, especially very wide flotation sizes, are rated at different pressures, so the maximum molded on your sidewall always wins. USTMA notes that light truck tires for vehicles up to 10,000 lb GVWR typically come in load ranges B through E.</p>
      </section>
{PICK}      <section class="content-section">
        <h2>Why LT tires need more air for the same load</h2>
        <p>Light truck and passenger tires follow different load and pressure tables. USTMA says replacing passenger tires with light truck tires requires a significant inflation pressure adjustment to carry the same load as the original size. Tire Review gives a worked example: an original P265/75R16 114S carries 2,601 lb at 35 psi, and an LT265/75R16 must run at 50 psi to carry that load, whether it is load range C, D or E.</p>
        <p>There is a second adjustment too. USTMA says a passenger tire's load capacity must be divided by 1.10 when it is used on a light truck. Its example P265/70R17 is rated 2,535 lb in passenger use and 2,305 lb in a light truck application. The checker above does that sum for you.</p>
        <p>Bridgestone recommends at least 35 psi for LT tires and says that if your truck has TPMS you should work with your installer on any special considerations for the new pressure. See our <a href="/guides/tpms/">TPMS guide</a>.</p>
      </section>
      <section class="content-section">
        <h2>Swapping between P metric and LT</h2>
        <ul>
          <li><strong>P metric to LT:</strong> often possible. USTMA says to check with the vehicle maker that the wheels suit the higher pressure, check rim width and clearance, and get the adjusted pressure and load rating from the vehicle maker, tire maker or a professional dealer.</li>
          <li><strong>LT to P metric:</strong> USTMA does not recommend it unless the vehicle maker specifies it.</li>
          <li><strong>Mixing:</strong> USTMA says never mix passenger and light truck tires, including C type tires, on the same vehicle.</li>
          <li><strong>Payload:</strong> Bridgestone is clear that LT tires do not raise the vehicle's load capacity. The ratings on the door placard still set the limit.</li>
        </ul>
        <p>Why switch at all? Bridgestone lists heavy duty construction for bruise and impact resistance, cut and chip resistant tread, off road tread designs and better handling under heavy load. Tire Review notes the trade offs: more weight, a stiffer ride, higher rolling resistance and lower fuel economy. Compare passenger load markings in our <a href="/guides/xl-vs-sl-tires/">XL vs SL guide</a>, and start with <a href="/fitment/choose-tire-size/">how to choose the right tire size</a>.</p>
      </section>
      <section class="content-section faq">
        <h2>Frequently asked questions</h2>
""" + "\n".join(f'        <h3>{q}</h3>\n        <p>{a}</p>' for q,a in FAQ) + '''
      </section>
      <section class="content-section sources">
        <h2>Sources</h2>
        <ul>
''' + "\n".join(f'          <li><a href="{u}" rel="noopener noreferrer" target="_blank">{t}</a>: {n}</li>' for u,t,n in SOURCES) + '''
        </ul>
      </section>
      <nav class="related-links" aria-label="Keep reading">
        <h2>Keep reading</h2>
        <ul>
          <li><a href="/guides/load-index-speed-rating/">Load index and speed rating</a></li>
          <li><a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a></li>
          <li><a href="/guides/tire-pressure/">Cold tire pressure guide</a></li>
          <li><a href="/fitment/choose-tire-size/">How to choose the right tire size</a></li>
          <li><a href="/guides/">All tire guides</a></li>
        </ul>
      </nav>
    </div>
  </main>'''
def faq_ld(): return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},indent=2)
def art_ld():
    org={"@type":"Organization","@id":"https://smarttirepicks.com/#organization","name":"Smart Tire Picks"}
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":"https://smarttirepicks.com/assets/img/og-fitment-wheel.jpg","datePublished":TODAY,"dateModified":TODAY,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":"https://smarttirepicks.com/#website","name":"Smart Tire Picks"}},indent=2)
def bc_ld(): return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"LT vs P metric tires","item":URL}]},indent=2)
def build():
    assert len(TITLE)<=60 and len(DESC)<=155,(len(TITLE),len(DESC))
    t=(R/"guides/speedometer-error-tire-size/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/speedometer-error-tire-size/",f"guides/{SLUG}/")
    head=re.sub(r"<title>.*?</title>",f"<title>{TITLE}</title>",head)
    for p in ['og:title','twitter:title']: head=re.sub(rf'(property|name)="{p}" content="[^"]*"',rf'\1="{p}" content="{TITLE}"',head)
    for p in ['name="description"','property="og:description"','name="twitter:description"']: head=re.sub(rf'{p} content="[^"]*"',f'{p} content="{DESC}"',head)
    for p in ['og:image:alt','twitter:image:alt']: head=re.sub(rf'"{p}" content="[^"]*"',f'"{p}" content="{ALT}"',head)
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',lambda m:"<script type=\"application/ld+json\">\n"+bc_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld()+"\n  </script>\n</head>",head,flags=re.S)
    d=R/f"guides/{SLUG}"; d.mkdir(exist_ok=True); (d/"index.html").write_text(head+BODY+foot)
def links():
    L=f'/guides/{SLUG}/'; p=R/"guides/index.html"; s=p.read_text()
    if URL not in s:
        old='''        "url": "https://smarttirepicks.com/guides/run-flat-tires/"
      }'''
        assert old in s
        s=s.replace(old,old[:-1]+'''},
      {
        "@type": "ListItem",
        "position": 31,
        "name": "LT vs P metric tires",
        "url": "'''+URL+'''"
      }''',1)
    if f'href="{L}"' not in s:
        card='''          <a class="card-link" href="/guides/run-flat-tires/">Read the guide →</a>
        </article>'''
        assert card in s
        s=s.replace(card,card+f'''
        <article class="card">
          <h3>LT vs P metric tires</h3>
          <p>Load range C, D and E, why LT tires need more pressure for the same load, and the rules for swapping and mixing. Includes a truck load checker.</p>
          <a class="card-link" href="{L}">Read the guide →</a>
        </article>''',1)
    p.write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/run-flat-tires/">New: Run flat tires explained</a>',f'<a class="btn btn-ghost" href="{L}">New: LT vs P metric tires explained</a>')
    if f'<a href="{L}">LT vs P' not in s:
        s=s.replace('<a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a>,',f'<a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a>, <a href="{L}">LT vs P tires</a>,',1)
    assert f'<a href="{L}">LT vs P' in s; p.write_text(s)
    li=f'          <li><a href="{L}">LT vs P metric tires (load range explained)</a></li>\n'
    for g in ["guides/load-index-speed-rating","guides/xl-vs-sl-tires","fitment/choose-tire-size"]:
        p=R/f"{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,count=1); assert L in s,g
        p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        s=s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/fitment-wheel-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n</urlset>')
    for u in ["","guides/","guides/load-index-speed-rating/","guides/xl-vs-sl-tires/","fitment/choose-tire-size/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>'+TODAY,s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [LT vs P metric tires]({URL}): P metric and Euro metric are passenger tires; LT metric and C type are light truck tires with single and dual load index plus load range; load range C, D, E inflate to 50, 65, 80 psi (old 6, 8, 10 ply); LT tires need more pressure than the placard to carry the same load (P265/75R16 at 35 psi vs LT at 50 psi); passenger tire load divided by 1.10 on light trucks (USTMA P265/70R17, 2535 to 2305 lb); swap and never mix rules; client side truck load checker. Cites USTMA, Bridgestone, Tire Review.\n"
        s=s.replace("- [Run flat tires explained",line+"- [Run flat tires explained",1); assert SLUG in s; p.write_text(s)
build(); links(); sitemap_llms(); print("ok")
