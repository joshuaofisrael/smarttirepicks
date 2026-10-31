#!/usr/bin/env python3
"""Re-runnable: create /guides/run-flat-tires/, link it, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "run-flat-tires"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TODAY = "2026-10-31"
TITLE = "Run Flat Tires Explained: Markings, Limits and Repairs"
H1 = "Run flat tires explained: markings, how far you can drive, and repairs"
DESC = "How run flat tires work, what RFT, ZP, SSR, EMT and RF in the size mean, maker limits for driving deflated, why TPMS is required, and repair rules."
ALT = "Alloy wheel and tire on a car, illustrating run flat tire markings on a sidewall"
BSRFT = "https://www.bridgestone.com/technology_innovation/run-flat_tire/"
BSDG = "https://www.bridgestoneamericas.com/en/press-release-details.en.2022.bridgestone-launches-driveguard-plus"
MZP = "https://cxf-prod.azureedge.net/b2c-experience-production/attachments/cma5uhnph02sh01jru277qi2y-michelin-oe-tires-owners-manual-warranty.pdf"
MRF = "https://middle-east.michelin.com/en/auto/auto-tips-and-advice/tires-101/run-flat-tires"
CSSR = "https://www.continental-tires.com/products/car/continental-tire-technologies/runflat-tires/"
CPDF = "https://www.continental-tires.com/content/dam/conti-tires-cms/continental/b2c/technologies/car/ssr-tyres-download-1-data.pdf.coredownload.pdf"
CDB = "https://www.continental-tyres.co.uk/content/dam/conti-tires-cms/continental/market-content/gb/tyre-knowledge/Conti_Tyre_Databook_2025_EN_screen.pdf.coredownload.pdf"
EC = "https://energy-efficient-products.ec.europa.eu/product-list/tyres/how-read-tyre-parameters_en"
USTMA = "https://www.ustires.org/system/files/files/2024-05/Care%20and%20Service%20Passenger%20and%20Light%20Truck%20Tires%20FINAL%2006%2028%2017.pdf"
FAQ = [
 ("What is a run flat tire?", "A run flat tire has reinforced sidewalls that keep supporting the vehicle after it loses air, so you can drive a limited distance at reduced speed to get help instead of changing a wheel at the roadside. Bridgestone, Michelin and Continental all describe their run flat ranges this way."),
 ("How far can you drive on a flat run flat tire?", "Use the tire maker's figure and any limit in your vehicle owner's manual. Bridgestone says up to 50 miles (80 km) at up to 50 mph (80 km/h). Continental SSR tires are rated for 80 km at a maximum of 80 km/h. Michelin's US ZP owner's manual says up to 50 miles at 55 mph unless the vehicle manual says otherwise. Load, heat, speed and damage can all shorten that distance."),
 ("How do I know if I have run flat tires?", "Look on the sidewall. Makers use their own codes, such as RFT or DriveGuard (Bridgestone), ZP or EMT (Michelin) and SSR (Continental). Under the European marking rules, a run flat tire can also show RF inside the size, as in 205/55 RF 16, or an EMT marking."),
 ("Do run flat tires need TPMS?", "Yes. Because a deflated run flat tire can feel almost normal, Continental says its SSR tires may only be used on vehicles with a tire pressure monitoring system, and Michelin says ZP tires must be used only with an operating low pressure warning system."),
 ("Can a run flat tire be repaired?", "Only sometimes. Continental says its SSR tires must not be repaired. Bridgestone says DriveGuard repairability depends on the damage, how much pressure was lost and how the vehicle was driven. Michelin says the fewer miles you drive after air loss, the better the chance a ZP tire can be repaired or returned to service. A tire shop should inspect the tire inside and out before any repair."),
 ("Can I put run flat tires on any car?", "Michelin says only vehicles originally equipped with run flat tires should mount them, because those vehicles have suspension and chassis changes for them. Continental says SSR tires may only be fitted on vehicles the vehicle maker approves and that have TPMS."),
 ("Can I mix run flat and regular tires?", "Continental advises against mixing SSR run flat tires with standard tires on the same vehicle. If your car came with run flats and has no spare, replacing them with regular tires also leaves you with no way to keep driving after a puncture, so check the owner's manual first."),
]
SOURCES = [
 (BSRFT,"Bridgestone, Run Flat Tire Technology","reinforced sidewalls support the vehicle after air loss; up to 50 miles (80 km) at 50 mph (80 km/h) under ISO based or vehicle specific test conditions; no roadside wheel change needed"),
 (BSDG,"Bridgestone Americas, DriveGuard Plus launch","up to 50 miles at up to 50 mph after a puncture; repairability depends on tire damage, pressure loss and operating conditions (technical bulletin P 14 02)"),
 (MZP,"Michelin, Passenger and Light Truck Tire Owner's Manual and Limited Warranty (PDF)","ZP tires: up to 50 miles (80 km) at 55 mph (90 km/h) unless the vehicle owner's manual says otherwise; must be used with an operational low pressure warning system; avoid high speed and hard cornering when deflated; SH M wheel note"),
 (MRF,"Michelin, Learn about run flat tires","only vehicles originally equipped with run flat tires should mount them; ZP and EMT markings"),
 (CSSR,"Continental Tires, Runflat tires","SSR sidewall support; 80 km at a maximum of 80 km/h after a puncture; TPMS required and ESC recommended; compatible with standard rims"),
 (CPDF,"Continental, SSR self supporting runflat tyre (PDF)","fitting on all four positions highly recommended; tyre repair not allowed; TPMS mandatory"),
 (CDB,"Continental, Tyre Databook 2025 (PDF)","RF and EMT run flat markings under UN Regulation 30, as in 205/55 RF 16; SSR only on vehicles approved by the maker with TPMS; do not mix SSR with standard tyres"),
 (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","a proper repair combines a plug and a patch from the inside, never a plug alone or a patch alone; tire maker limits may apply to run flat tires"),
 (EC,"European Commission, How to read the tyre parameters","run flat tyres carry an F before the rim diameter, as in 245/45RF19, plus a pictogram"),
]
CHECK = '''      <section class="content-section tool" id="run-flat-checker">
        <h2>How far can my run flat go?</h2>
        <p>Pick the marking on your tire to see the maker's published limit after air loss. This runs entirely in your browser and nothing is sent or stored.</p>
        <form id="rf-form" onsubmit="return false">
          <label>Marking on the sidewall <select id="rf-sel">
            <option value="rft">RFT or DriveGuard (Bridgestone)</option>
            <option value="zp">ZP (Michelin, US owner's manual)</option>
            <option value="ssr">SSR (Continental)</option>
            <option value="gen">RF inside the size, EMT, or another run flat code</option>
            <option value="none">No run flat marking</option>
          </select></label><br>
          <label>Miles already driven since the warning <input id="rf-mi" type="number" min="0" max="200" step="1" value="0"></label>
        </form>
        <p id="rf-out" aria-live="polite"></p>
        <script>
        (function(){var L={rft:[50,50,'Bridgestone'],zp:[50,55,'Michelin'],ssr:[50,50,'Continental (80 km at 80 km/h)'],gen:[50,50,'the common industry figure; check the tire maker and owner\\'s manual']};
        var s=document.getElementById('rf-sel'),m=document.getElementById('rf-mi'),o=document.getElementById('rf-out');
        function run(){var v=s.value;if(v==='none'){o.innerHTML='<strong>Not a run flat.</strong> A regular tire should not be driven flat. Pull over safely and use your spare or inflator kit.';return;}
        var x=L[v],d=Math.max(0,parseFloat(m.value)||0),left=Math.max(0,x[0]-d);
        o.innerHTML='<strong>Published limit:</strong> up to '+x[0]+' miles at no more than '+x[1]+' mph, per '+x[2]+'. '+(left>0?'That leaves at most about '+left+' miles, and less with heavy loads, heat or damage.':'You have reached the published limit. Stop driving on this tire.')+' Your vehicle owner\\'s manual limit takes priority.';}
        s.addEventListener('change',run);m.addEventListener('input',run);run();})();
        </script>
        <p>General information only. A maximum is not a guarantee; get the tire inspected as soon as you can.</p>
      </section>
'''
LIM = [("Bridgestone RFT and DriveGuard","Up to 50 miles (80 km)","Up to 50 mph (80 km/h)"),("Continental SSR","80 km (about 50 miles)","80 km/h (about 50 mph)"),("Michelin ZP (US owner's manual)","Up to 50 miles (80 km)","55 mph (90 km/h), unless the vehicle manual says otherwise")]
BODY = f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: a <strong>run flat tire</strong> has reinforced sidewalls that hold the car up after a puncture, so you can drive a <strong>limited distance at reduced speed</strong>, typically about <strong>50 miles at around 50 mph</strong> by the makers' own figures, to reach a tire shop. Run flats need a working <strong>TPMS</strong>, and many cannot be repaired.</p>
<p class="last-updated">Last updated: October 31, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/fitment-wheel-1024.webp" srcset="/assets/img/fitment-wheel-640.webp 640w, /assets/img/fitment-wheel-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
{CHECK}      <section class="content-section">
        <h2>How run flat tires work</h2>
        <p>A regular tire relies on air pressure to carry the vehicle. When it goes flat, the sidewall gets crushed between the rim and the road. Bridgestone and Continental explain that a self supporting run flat tire uses stiffer, reinforced sidewalls that keep carrying the weight after air is lost, and stop the tire from slipping off the rim. Continental says its SSR tires fit standard rims. Michelin notes that some ZP tires marked SH M need special wheels, so never mount those on a standard wheel.</p>
      </section>
      <section class="content-section">
        <h2>Run flat markings</h2>
        <ul>
          <li><strong>RFT or DriveGuard:</strong> Bridgestone run flat tires.</li>
          <li><strong>ZP or EMT:</strong> Michelin Zero Pressure and Extended Mobility Tire.</li>
          <li><strong>SSR:</strong> Continental Self Supporting Runflat.</li>
          <li><strong>RF inside the size, such as 205/55 RF 16 or 245/45RF19:</strong> the general run flat marking under UN Regulation 30, according to Continental and the European Commission, which adds that a pictogram is shown too. Do not confuse this with RF as a separate marking next to the size, which means reinforced. See <a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a>.</li>
          <li><strong>EMT or RUN FLAT:</strong> Continental says the EMT marking is an alternative general run flat marking and will appear more often on its future SSR tires.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>How far and how fast you can drive deflated</h2>
        <table class="data-table">
          <thead><tr><th>Tire</th><th>Distance</th><th>Speed</th></tr></thead>
          <tbody>
''' + "\n".join("            <tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in LIM) + f'''
          </tbody>
        </table>
        <p>Sources: Bridgestone, Continental and Michelin. These are maximums. Michelin says the safe distance depends on speed, load, outside temperature, how much air was lost and the damage. Hard braking, cornering and sharp maneuvers greatly shorten it, and a deflated tire handles differently. If the tire starts to vibrate or the car becomes hard to control, stop. If your owner's manual gives a lower limit, follow it.</p>
      </section>
      <section class="content-section">
        <h2>Why run flats need TPMS</h2>
        <p>Run flat tires ride so normally when deflated that you may not notice. Continental says SSR tires may only be used on vehicles with a tire pressure monitoring system, and recommends electronic stability control. Michelin says ZP tires must be used only with an operating low pressure warning system, or the limited warranty is void. Learn what the warning light means in our <a href="/guides/tpms/">TPMS guide</a>.</p>
      </section>
      <section class="content-section">
        <h2>Can a run flat be repaired?</h2>
        <ul>
          <li><strong>Continental SSR:</strong> Continental says a tire repair is not allowed.</li>
          <li><strong>Bridgestone DriveGuard:</strong> repairable in limited circumstances, depending on the damage, how much pressure was lost and how the car was driven.</li>
          <li><strong>Michelin ZP:</strong> the fewer miles driven after air loss, the better the chance the tire can be reinflated or repaired and returned to service.</li>
        </ul>
        <p>Where a repair is allowed, USTMA says a proper repair needs a patch and plug combination from the inside, never a plug alone, and the tire maker's own limits apply. See <a href="/guides/tire-plug-vs-patch/">tire plug vs patch</a>.</p>
      </section>
      <section class="content-section">
        <h2>No spare, and replacing run flats</h2>
        <p>Cars built for run flats often carry no spare wheel or jack, which saves weight and trunk space. Michelin says only vehicles originally equipped with run flat tires should mount them, because those cars have suspension and chassis changes for them. Continental says SSR tires should only go on vehicles the maker approves with TPMS, recommends fitting them on all four positions, and advises against mixing them with standard tires. If you switch to regular tires, plan for a puncture: carry a spare or inflator kit and check our <a href="/guides/spare-tire-limits/">spare tire limits</a>.</p>
      </section>
      <section class="content-section faq">
        <h2>Frequently asked questions</h2>
''' + "\n".join(f'        <h3>{q}</h3>\n        <p>{a}</p>' for q,a in FAQ) + '''
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
          <li><a href="/guides/tpms/">TPMS warning light guide</a></li>
          <li><a href="/guides/tire-plug-vs-patch/">Tire plug vs patch</a></li>
          <li><a href="/guides/spare-tire-limits/">Spare tire (donut) limits</a></li>
          <li><a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a></li>
          <li><a href="/guides/">All tire guides</a></li>
        </ul>
      </nav>
    </div>
  </main>'''
def faq_ld(): return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},indent=2)
def art_ld():
    org={"@type":"Organization","@id":"https://smarttirepicks.com/#organization","name":"Smart Tire Picks"}
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":"https://smarttirepicks.com/assets/img/og-fitment-wheel.jpg","datePublished":TODAY,"dateModified":TODAY,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":"https://smarttirepicks.com/#website","name":"Smart Tire Picks"}},indent=2)
def bc_ld(): return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"Run flat tires","item":URL}]},indent=2)
def build():
    assert len(TITLE)<=60 and len(DESC)<=155,(len(TITLE),len(DESC))
    t=(R/"guides/xl-vs-sl-tires/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/xl-vs-sl-tires/",f"guides/{SLUG}/")
    head=re.sub(r"<title>.*?</title>",f"<title>{TITLE}</title>",head)
    for p in ['og:title','twitter:title']: head=re.sub(rf'(property|name)="{p}" content="[^"]*"',rf'\1="{p}" content="{TITLE}"',head)
    for p in ['name="description"','property="og:description"','name="twitter:description"']: head=re.sub(rf'{p} content="[^"]*"',f'{p} content="{DESC}"',head)
    for p in ['og:image:alt','twitter:image:alt']: head=re.sub(rf'"{p}" content="[^"]*"',f'"{p}" content="{ALT}"',head)
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',lambda m:"<script type=\"application/ld+json\">\n"+bc_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld()+"\n  </script>\n</head>",head,flags=re.S)
    d=R/f"guides/{SLUG}"; d.mkdir(exist_ok=True); (d/"index.html").write_text(head+BODY+foot)
def links():
    L=f'/guides/{SLUG}/'; p=R/"guides/index.html"; s=p.read_text()
    if URL not in s:
        old='''        "url": "https://smarttirepicks.com/guides/xl-vs-sl-tires/"
      }'''
        assert old in s
        s=s.replace(old,old[:-1]+'''},
      {
        "@type": "ListItem",
        "position": 30,
        "name": "Run flat tires explained",
        "url": "'''+URL+'''"
      }''',1)
    if f'href="{L}"' not in s:
        card='''          <a class="card-link" href="/guides/xl-vs-sl-tires/">Read the guide →</a>
        </article>'''
        assert card in s
        s=s.replace(card,card+f'''
        <article class="card">
          <h3>Run flat tires explained</h3>
          <p>RFT, ZP, SSR and RF markings, how far you can drive deflated by maker limits, why TPMS is required, and repair rules. Includes a distance checker.</p>
          <a class="card-link" href="{L}">Read the guide →</a>
        </article>''',1)
    p.write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/xl-vs-sl-tires/">New: XL vs SL tires explained</a>',f'<a class="btn btn-ghost" href="{L}">New: Run flat tires explained</a>')
    if f'<a href="{L}">run flat' not in s:
        s=s.replace('<a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a>,',f'<a href="/guides/xl-vs-sl-tires/">XL vs SL tires</a>, <a href="{L}">run flat tires</a>,',1)
    assert f'<a href="{L}">run flat' in s; p.write_text(s)
    li=f'          <li><a href="{L}">Run flat tires explained</a></li>\n'
    for g in ["guides/tpms","guides/tire-plug-vs-patch","guides/spare-tire-limits","guides/xl-vs-sl-tires"]:
        p=R/f"{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,count=1); assert L in s,g
        p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        s=s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/fitment-wheel-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n</urlset>')
    for u in ["","guides/","guides/tpms/","guides/tire-plug-vs-patch/","guides/spare-tire-limits/","guides/xl-vs-sl-tires/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>'+TODAY,s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [Run flat tires explained]({URL}): reinforced sidewalls carry the car after air loss; markings RFT/DriveGuard (Bridgestone), ZP/EMT (Michelin), SSR (Continental), RF inside the size or EMT under UN R30; maker limits after air loss (Bridgestone 50 mi at 50 mph, Continental 80 km at 80 km/h, Michelin US ZP 50 mi at 55 mph); TPMS required; repair rules by maker; no spare; client side distance checker. Cites Bridgestone, Michelin, Continental, European Commission, USTMA.\n"
        s=s.replace("- [XL vs SL tires",line+"- [XL vs SL tires",1); assert SLUG in s; p.write_text(s)
build(); links(); sitemap_llms(); print("ok")
