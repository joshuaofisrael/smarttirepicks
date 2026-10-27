#!/usr/bin/env python3
"""Re-runnable: create /guides/tire-balancing-vs-wheel-alignment/, link it, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "tire-balancing-vs-wheel-alignment"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TODAY = "2026-10-27"
TITLE = "Tire Balancing vs Wheel Alignment: Which Do You Need?"
H1 = "Tire balancing vs wheel alignment: which do you need?"
DESC = "Balancing fixes vibration at speed; alignment fixes pulling, an off center wheel and edge wear. Match your symptom to the right service with our checker."
ALT = "Close up of a car wheel and tire on a vehicle, the assembly that balancing and alignment service"
FAQ = [
 ("What is the difference between tire balancing and wheel alignment?", "Balancing evens out the weight around a tire and wheel so it spins smoothly; a technician adds small weights to the rim to offset heavy spots. Alignment adjusts the angles of the wheels (camber, caster and toe) relative to the vehicle so the tires point straight and sit flat on the road. Balancing is about the wheel assembly; alignment is about the car's suspension and steering."),
 ("How do I know if I need balancing or alignment?", "Vibration in the steering wheel, seat or floor that shows up in a certain highway speed range usually points to imbalance. A car that pulls to one side on a straight, level road, a steering wheel that sits off center when driving straight, or wear on the inside or outside edge of the tread usually points to alignment. Check that all tires are at the placard pressure first, since uneven pressure can also cause a pull."),
 ("Should I get my tires balanced when I buy new tires?", "Yes. New tires are normally balanced when they are mounted on the wheels, because no tire and wheel is perfectly uniform. Tires are also commonly rebalanced when they are remounted, after a flat repair that removes the tire from the rim, or whenever a vibration appears."),
 ("When should I get a wheel alignment?", "Consider an alignment when you fit new tires, after hitting a large pothole or curb, after suspension or steering work, or whenever you notice pulling, an off center steering wheel or uneven edge wear. Your owner's manual may also list a check interval."),
 ("Can bad alignment cause vibration?", "Alignment problems mainly cause pulling and uneven wear rather than a speed dependent vibration. If a vibration remains after a proper balance, the cause may be a bent rim, an out of round tire, tire uniformity issues, worn suspension parts or brakes, so have a technician inspect the car."),
 ("Do I need both balancing and alignment?", "Often both are worth checking, because they solve different problems. Michelin notes a car can be perfectly aligned and still vibrate from imbalance, and a balanced wheel can still wear unevenly if the alignment angles are wrong."),
 ("If my car pulls only when braking, is it alignment?", "Probably not. A pull that happens only when you brake usually points to the braking system, not alignment, so have the brakes inspected."),
]
SOURCES = [
 ("https://rosap.ntl.bts.gov/view/dot/16477/dot_16477_DS1.pdf","NHTSA, Tire Safety: Everything Rides On It (brochure)","balancing uses weights to counter heavy spots and prevent vibration; alignment sets wheel angles relative to the frame, maximizes tire life and prevents veering; both need special equipment and a qualified technician"),
 ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-maintenance/wheel-alignment-wheel-balancing","Michelin USA, Wheel alignment and balancing explained","signs of misalignment and imbalance; why a car can need both"),
 ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-damage/handling-problems","Michelin USA, Handling problems","speed specific vibration points to imbalance; a steady pull after equalizing pressure points to alignment; a pull only while braking points to brakes"),
 ("https://www.ustires.org/tire-care","USTMA, Tire care","inflation, rotation and inspection basics"),
]
ROWS = [
 ("Steering wheel shakes in a certain speed range, often around highway speed","Balancing","Classic sign of imbalance; check for a lost wheel weight"),
 ("Vibration felt through the seat or floor","Balancing (often a rear wheel)","Also check for tire damage or a bent rim"),
 ("Car drifts or pulls to one side on a straight, level road","Alignment","Set all tires to placard pressure first; uneven pressure can cause a pull"),
 ("Steering wheel is off center when driving straight","Alignment","Common after a pothole or curb strike"),
 ("Tread worn on the inside or outside edge","Alignment","Underinflation wears both shoulders instead"),
 ("Scalloped or cupped patches around the tread","Balancing and an inspection","Cupping can also point to worn shocks or struts"),
 ("Pull only when braking","Brake inspection","Not usually an alignment problem"),
 ("Vibration remains after a fresh balance","Inspection","Bent rim, out of round tire or tire uniformity; ask about a road force balance"),
]
CHECKER = '''      <section class="content-section tool" id="symptom-checker">
        <h2>Symptom checker: balancing, alignment or something else?</h2>
        <p>Tick what you notice. This runs entirely in your browser and nothing is sent or stored.</p>
        <form id="ba-form" onsubmit="return false">
          <label><input type="checkbox" value="b2"> Steering wheel shakes at a certain speed</label><br>
          <label><input type="checkbox" value="b2"> Vibration in the seat or floor</label><br>
          <label><input type="checkbox" value="b1"> Cupped or scalloped tread patches</label><br>
          <label><input type="checkbox" value="a2"> Car pulls to one side on a straight road</label><br>
          <label><input type="checkbox" value="a2"> Steering wheel off center when going straight</label><br>
          <label><input type="checkbox" value="a2"> Wear on the inside or outside edge of the tread</label><br>
          <label><input type="checkbox" value="a1"> Recently hit a big pothole or curb</label><br>
          <label><input type="checkbox" value="b1"> Just bought new tires or had a flat repaired</label><br>
          <label><input type="checkbox" value="x3"> Pull or shake only when braking</label>
        </form>
        <p id="ba-out" aria-live="polite"><strong>Result:</strong> tick a symptom above.</p>
        <script>
        (function(){var f=document.getElementById('ba-form'),o=document.getElementById('ba-out');
        f.addEventListener('change',function(){var b=0,a=0,x=0;f.querySelectorAll('input:checked').forEach(function(i){var t=i.value[0],n=+i.value[1];if(t==='b')b+=n;else if(t==='a')a+=n;else x+=n;});
        var m=[];if(x)m.push('have the brakes inspected, since a pull or shake only when braking usually points there');
        if(b&&a)m.push('ask for both a balance and an alignment check');else if(b)m.push('start with a tire balance');else if(a)m.push('start with an alignment check, after setting every tire to the placard pressure');
        o.innerHTML='<strong>Result:</strong> '+(m.length?m.join('; ')+'. If symptoms remain, have a qualified technician inspect the tires, wheels and suspension.':'tick a symptom above.');});})();
        </script>
        <p>This is a general guide, not a diagnosis. A technician can confirm the cause.</p>
      </section>
'''
BODY = f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: get your tires <strong>balanced</strong> if you feel a vibration that comes and goes with speed, and get a wheel <strong>alignment</strong> if the car pulls to one side, the steering wheel sits off center, or the tread wears on one edge. Balancing fixes how the tire and wheel spin; alignment fixes the angle the wheels point.</p>
<p class="last-updated">Last updated: October 27, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/fitment-wheel-1024.webp" srcset="/assets/img/fitment-wheel-640.webp 640w, /assets/img/fitment-wheel-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
      <section class="content-section">
        <h2>The difference in one table</h2>
        <table class="data-table">
          <thead><tr><th></th><th>Tire balancing</th><th>Wheel alignment</th></tr></thead>
          <tbody>
            <tr><td>What it fixes</td><td>Uneven weight around the tire and wheel</td><td>Wheel angles: camber, caster and toe</td></tr>
            <tr><td>Main symptom</td><td>Vibration or shake at certain speeds</td><td>Pulling, off center steering wheel, edge wear</td></tr>
            <tr><td>How it is done</td><td>Wheel spun on a balancer; small weights added to the rim</td><td>Suspension and steering adjusted to the maker's specs on an alignment rack</td></tr>
            <tr><td>Works on</td><td>Each tire and wheel assembly</td><td>The vehicle's suspension and steering</td></tr>
            <tr><td>Typical times</td><td>New tires, remounting, flat repairs, any new vibration</td><td>New tires, after a pothole or curb hit, suspension work, any pull or edge wear</td></tr>
          </tbody>
        </table>
        <p>NHTSA's tire safety brochure sums it up: balancing places weights to counter heavy spots and prevent vibration, while alignment sets the wheel angles so the car does not veer and the tires last longer. Both need special equipment and a qualified technician.</p>
      </section>
      <section class="content-section">
        <h2>Match your symptom to the service</h2>
        <table class="data-table">
          <thead><tr><th>What you notice</th><th>Likely service</th><th>Notes</th></tr></thead>
          <tbody>
''' + "\n".join(f'            <tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in ROWS) + f'''
          </tbody>
        </table>
      </section>
{CHECKER}      <section class="content-section">
        <h2>Check these first, for free</h2>
        <ol>
          <li><strong>Tire pressure.</strong> Set every tire to the cold pressure on your door placard. A low tire can make a car pull. See our <a href="/guides/tire-pressure/">tire pressure guide</a>.</li>
          <li><strong>Look at the tread.</strong> Edge wear on one side hints at alignment; wear on both shoulders hints at low pressure; wear in the center hints at overinflation. Our <a href="/guides/tread-depth/">tread depth guide</a> shows how to measure.</li>
          <li><strong>Look for damage.</strong> A bulge, a missing wheel weight or a bent rim lip can all cause shaking. See <a href="/guides/sidewall-bulge/">sidewall bulges</a>.</li>
          <li><strong>Note when it happens.</strong> Only at certain speeds, only when braking, or all the time. That detail helps a shop find the cause quickly.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Where rotation fits in</h2>
        <p>Rotation moves tires between positions so they wear evenly; it does not change balance or wheel angles. Many shops check balance when they rotate, and rotating on schedule can make alignment wear easier to spot early. See our <a href="/guides/tire-rotation/">tire rotation patterns</a>, and if you are replacing only some tires, read <a href="/guides/mixing-tires/">mixing tires</a> first.</p>
        <p>Prices vary by shop, region and vehicle, so ask for a quote for each service separately. Some shops include balancing with tire installation.</p>
      </section>
      <section class="content-section faq">
        <h2>Frequently asked questions</h2>
''' + "\n".join(f'        <h3>{q}</h3>\n        <p>{a}</p>' for q,a in FAQ) + '''
      </section>
      <section class="content-section sources">
        <h2>Sources</h2>
        <ul>
''' + "\n".join(f'          <li><a href="{u}" rel="noopener noreferrer" target="_blank">{t}</a> — {n}</li>' for u,t,n in SOURCES) + '''
        </ul>
      </section>
      <nav class="related-links" aria-label="Keep reading">
        <h2>Keep reading</h2>
        <ul>
          <li><a href="/guides/tire-rotation/">Tire rotation patterns</a></li>
          <li><a href="/guides/tire-pressure/">Tire pressure guide</a></li>
          <li><a href="/guides/when-to-replace/">When to replace tires</a></li>
          <li><a href="/guides/how-long-do-tires-last/">How long do tires last?</a></li>
          <li><a href="/guides/">All tire guides</a></li>
        </ul>
      </nav>
    </div>
  </main>'''
def faq_ld(): return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},indent=2)
def art_ld():
    org={"@type":"Organization","@id":"https://smarttirepicks.com/#organization","name":"Smart Tire Picks"}
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":"https://smarttirepicks.com/assets/img/og-fitment-wheel.jpg","datePublished":TODAY,"dateModified":TODAY,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":"https://smarttirepicks.com/#website","name":"Smart Tire Picks"}},indent=2)
def bc_ld(): return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"Tire balancing vs wheel alignment","item":URL}]},indent=2)
def build():
    assert len(TITLE)<=60 and len(DESC)<=155,(len(TITLE),len(DESC))
    t=(R/"guides/how-long-do-winter-tires-last/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/how-long-do-winter-tires-last/",f"guides/{SLUG}/").replace("og-winter-tires.jpg","og-fitment-wheel.jpg")
    head=re.sub(r"<title>.*?</title>",f"<title>{TITLE}</title>",head)
    for p in ['og:title','twitter:title']: head=re.sub(rf'(property|name)="{p}" content="[^"]*"',rf'\1="{p}" content="{TITLE}"',head)
    for p in ['name="description"','property="og:description"','name="twitter:description"']: head=re.sub(rf'{p} content="[^"]*"',f'{p} content="{DESC}"',head)
    for p in ['og:image:alt','twitter:image:alt']: head=re.sub(rf'"{p}" content="[^"]*"',f'"{p}" content="{ALT}"',head)
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',lambda m:"<script type=\"application/ld+json\">\n"+bc_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld()+"\n  </script>\n</head>",head,flags=re.S)
    d=R/f"guides/{SLUG}"; d.mkdir(exist_ok=True); (d/"index.html").write_text(head+BODY+foot)
def links():
    L=f'/guides/{SLUG}/'; p=R/"guides/index.html"; s=p.read_text()
    if URL not in s:
        old='''        "url": "https://smarttirepicks.com/guides/how-long-do-winter-tires-last/"
      }'''
        assert old in s
        s=s.replace(old,old[:-1]+'''},
      {
        "@type": "ListItem",
        "position": 27,
        "name": "Tire balancing vs wheel alignment",
        "url": "'''+URL+'''"
      }''',1)
    if f'href="{L}"' not in s:
        card='''          <a class="card-link" href="/guides/how-long-do-winter-tires-last/">Read the guide →</a>
        </article>'''
        assert card in s
        s=s.replace(card,card+f'''
        <article class="card">
          <h3>Tire balancing vs wheel alignment</h3>
          <p>Vibration or pulling? Match your symptom to balancing, alignment or a brake check, with a quick in browser symptom checker and what to check first for free.</p>
          <a class="card-link" href="{L}">Read the guide →</a>
        </article>''',1)
    p.write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/how-long-do-winter-tires-last/">New: How long do winter tires last?</a>',f'<a class="btn btn-ghost" href="{L}">New: Tire balancing vs wheel alignment</a>')
    if f'<a href="{L}">balancing vs alignment' not in s:
        s=s.replace('<a href="/guides/how-long-do-winter-tires-last/">how long winter tires last</a>,',f'<a href="/guides/how-long-do-winter-tires-last/">how long winter tires last</a>, <a href="{L}">balancing vs alignment</a>,',1)
    p.write_text(s)
    li=f'          <li><a href="{L}">Tire balancing vs wheel alignment</a></li>\n'
    for g in ["tire-rotation","tire-pressure","when-to-replace","mixing-tires","how-long-do-tires-last","tread-depth"]:
        p=R/f"guides/{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,1); assert L in s,g; p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        s=s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/fitment-wheel-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n</urlset>')
    for u in ["","guides/","guides/tire-rotation/","guides/tire-pressure/","guides/when-to-replace/","guides/mixing-tires/","guides/how-long-do-tires-last/","guides/tread-depth/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>'+TODAY,s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [Tire balancing vs wheel alignment]({URL}): Balancing adds rim weights so the tire and wheel spin smoothly (fixes speed dependent vibration); alignment sets camber, caster and toe (fixes pulling, off center steering wheel, edge wear); pull only when braking points to brakes; symptom table, free checks, client side symptom checker. Cites NHTSA, Michelin and USTMA.\n"
        s=s.replace("- [Nitrogen vs air",line+"- [Nitrogen vs air",1); p.write_text(s)
build(); links(); sitemap_llms(); print("ok")
