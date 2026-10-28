#!/usr/bin/env python3
"""Re-runnable: create /guides/speedometer-error-tire-size/, link it, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "speedometer-error-tire-size"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TODAY = "2026-10-28"
TITLE = "Speedometer Error After a Tire Size Change: Calculator"
H1 = "Speedometer error after a tire size change"
DESC = "Bigger or smaller tires change what your speedometer reads. See how to work out your real speed, the 3 percent rule and try our free in browser calculator."
ALT = "Alloy wheel and tire on a car, illustrating how a tire size change affects the speedometer"
def dia(w,a,r): return w*a/100*2/25.4+r
EX = [(225,65,17,235,65,17),(205,55,16,225,45,17),(265,70,17,285,75,17),(225,65,17,265,70,17)]
def exrow(s):
    o=dia(*s[:3]); n=dia(*s[3:]); p=(n/o-1)*100
    return f"<tr><td>{s[0]}/{s[1]}R{s[2]}</td><td>{s[3]}/{s[4]}R{s[5]}</td><td>{o:.2f} in to {n:.2f} in</td><td>{p:+.1f}%</td><td>{60*n/o:.1f} mph</td></tr>"
FAQ = [
 ("Do bigger tires make my speedometer read slower or faster?", "Taller tires make the speedometer read lower than your real speed, because each turn of the tire covers more ground. Shorter tires make it read higher than your real speed. The size of the error depends on how much the overall diameter changes."),
 ("How do I work out my real speed after a tire size change?", "Divide the new overall diameter by the old one and multiply by the speed on your speedometer. For example, going from 225/65R17 to 235/65R17 raises the diameter by about 1.8 percent, so an indicated 60 mph is about 61.1 mph."),
 ("How much can tire size change without affecting the speedometer?", "Continental says that under most circumstances a change in rolling circumference within plus or minus 3 percent does not require adjusting the speedometer, ABS or stability control. Outside that range, or if in doubt, follow the vehicle manufacturer."),
 ("Does the odometer change too?", "Yes. The odometer uses the same signal as the speedometer, so it records distance with the same percentage error. Taller tires make it count fewer miles than you actually drive; shorter tires make it count more."),
 ("Can a speedometer be recalibrated for new tires?", "On many vehicles a dealer or specialist shop can update the tire size setting or recalibrate the speedometer. The method depends on the make and model, so ask the vehicle manufacturer or a dealer."),
 ("Does tread wear change the speedometer reading?", "Slightly. As tread wears, the tire's diameter shrinks a little, so the error from a size change shifts a bit over the tire's life. The calculator here uses nominal sizes, which describe a new tire."),
]
SOURCES = [
 ("https://continentaltire.com/sites/default/files/media/file/2021-01/plus_sizing_0.pdf","Continental Tire, Plus sizing (PDF)","a rolling circumference different from the original fitment can affect speedometer calibration, ABS and stability control; under most circumstances a change within plus or minus 3 percent needs no adjustment; ask the vehicle manufacturer if in doubt"),
 ("https://www.nhtsa.gov/vehicle-safety/tires","NHTSA, Tires","tire size, the placard and choosing replacement tires"),
]
CALC = '''      <section class="content-section tool" id="speedo-calculator">
        <h2>Speedometer error calculator</h2>
        <p>Enter your original and new tire sizes. This runs entirely in your browser and nothing is sent or stored.</p>
        <form id="sp-form" onsubmit="return false">
          <label>Original size <input id="sp-old" value="225/65R17" inputmode="text" autocomplete="off"></label><br>
          <label>New size <input id="sp-new" value="235/65R17" inputmode="text" autocomplete="off"></label><br>
          <label>Speedometer reads (mph) <input id="sp-mph" type="number" value="60" min="1" max="200"></label>
        </form>
        <p id="sp-out" aria-live="polite"></p>
        <script>
        (function(){function p(s){var m=String(s).toUpperCase().replace(/\\s/g,'').match(/^(?:P|LT)?(\\d{3})\\/(\\d{2})Z?R?(\\d{2})/);if(!m)return null;return (+m[1])*(+m[2])/100*2/25.4+(+m[3]);}
        var f=document.getElementById('sp-form'),o=document.getElementById('sp-out');
        function run(){var a=p(document.getElementById('sp-old').value),b=p(document.getElementById('sp-new').value),v=+document.getElementById('sp-mph').value;
        if(!a||!b||!(v>0)){o.innerHTML='<strong>Result:</strong> enter sizes like 225/65R17 and a speed.';return;}
        var r=b/a,pc=(r-1)*100,t=v*r,w=Math.abs(pc)<=3?'Within the plus or minus 3 percent range Continental gives as normally needing no adjustment.':'Outside plus or minus 3 percent. Check with the vehicle manufacturer before fitting.';
        o.innerHTML='<strong>Result:</strong> diameter '+a.toFixed(2)+' in to '+b.toFixed(2)+' in ('+(pc>=0?'+':'')+pc.toFixed(1)+'%). When the speedometer reads '+v+' mph you are actually doing about <strong>'+t.toFixed(1)+' mph</strong>. '+w;}
        f.addEventListener('input',run);run();})();
        </script>
        <p>Calculated from nominal sizes. Real tires vary slightly by brand, model and tread depth.</p>
      </section>
'''
BODY = f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: if your new tires are <strong>taller</strong> than the originals, your speedometer reads <strong>lower</strong> than your real speed; if they are <strong>shorter</strong>, it reads higher. Your real speed is roughly the speedometer reading times the new diameter divided by the old diameter. Continental says a change within plus or minus 3 percent normally needs no adjustment.</p>
<p class="last-updated">Last updated: October 28, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/fitment-wheel-1024.webp" srcset="/assets/img/fitment-wheel-640.webp 640w, /assets/img/fitment-wheel-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
{CALC}      <section class="content-section">
        <h2>Why a tire size change affects the speedometer</h2>
        <p>Most speedometers work out speed from how fast the wheels or drivetrain turn, calibrated for the original tire size. A taller tire travels farther with each turn, so the car moves faster than the speedometer thinks. A shorter tire does the opposite. Continental notes that a different rolling circumference can also affect ABS and stability control, not only the speedometer.</p>
        <h3>The math</h3>
        <ol>
          <li>Sidewall height in inches = width in mm times aspect ratio divided by 100, then divided by 25.4.</li>
          <li>Overall diameter = rim diameter plus two sidewalls.</li>
          <li>Real speed = speedometer reading times new diameter divided by old diameter.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>Worked examples at an indicated 60 mph</h2>
        <table class="data-table">
          <thead><tr><th>Original</th><th>New</th><th>Diameter</th><th>Change</th><th>Real speed</th></tr></thead>
          <tbody>
''' + "\n".join("            "+exrow(s) for s in EX) + f'''
          </tbody>
        </table>
        <p>The first two stay inside the plus or minus 3 percent range. The last two are well outside it, so the speedometer would read noticeably low and the change should be checked with the vehicle manufacturer. Size changes can also affect clearance and load capacity; see <a href="/guides/plus-sizing/">plus sizing</a> and <a href="/guides/load-index-speed-rating/">load index and speed rating</a>.</p>
      </section>
      <section class="content-section">
        <h2>Before you change sizes</h2>
        <ul>
          <li>Start from the size on your <a href="/guides/placard/">door placard</a>, which is what the speedometer was set up for.</li>
          <li>Keep the overall diameter as close to stock as you can, ideally within plus or minus 3 percent.</li>
          <li>Match or exceed the original load index and speed rating.</li>
          <li>Fit the same size on all four wheels unless the vehicle came with a staggered setup. See <a href="/guides/mixing-tires/">mixing tires</a>.</li>
          <li>If you go outside the range, ask a dealer whether the speedometer can be recalibrated for the new size.</li>
        </ul>
        <p>Compare width, sidewall and revolutions per mile as well in our <a href="/tools/tire-size-calculator/">tire size calculator</a>, or read <a href="/fitment/choose-tire-size/">how to choose the right tire size</a>.</p>
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
          <li><a href="/tools/tire-size-calculator/">Tire size calculator</a></li>
          <li><a href="/guides/plus-sizing/">Plus sizing guide</a></li>
          <li><a href="/guides/load-index-speed-rating/">Load index and speed rating</a></li>
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
def bc_ld(): return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"Speedometer error after a tire size change","item":URL}]},indent=2)
def build():
    assert len(TITLE)<=60 and len(DESC)<=155,(len(TITLE),len(DESC))
    t=(R/"guides/tire-balancing-vs-wheel-alignment/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/tire-balancing-vs-wheel-alignment/",f"guides/{SLUG}/")
    head=re.sub(r"<title>.*?</title>",f"<title>{TITLE}</title>",head)
    for p in ['og:title','twitter:title']: head=re.sub(rf'(property|name)="{p}" content="[^"]*"',rf'\1="{p}" content="{TITLE}"',head)
    for p in ['name="description"','property="og:description"','name="twitter:description"']: head=re.sub(rf'{p} content="[^"]*"',f'{p} content="{DESC}"',head)
    for p in ['og:image:alt','twitter:image:alt']: head=re.sub(rf'"{p}" content="[^"]*"',f'"{p}" content="{ALT}"',head)
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',lambda m:"<script type=\"application/ld+json\">\n"+bc_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld()+"\n  </script>\n</head>",head,flags=re.S)
    d=R/f"guides/{SLUG}"; d.mkdir(exist_ok=True); (d/"index.html").write_text(head+BODY+foot)
def links():
    L=f'/guides/{SLUG}/'; p=R/"guides/index.html"; s=p.read_text()
    if URL not in s:
        old='''        "url": "https://smarttirepicks.com/guides/tire-balancing-vs-wheel-alignment/"
      }'''
        assert old in s
        s=s.replace(old,old[:-1]+'''},
      {
        "@type": "ListItem",
        "position": 28,
        "name": "Speedometer error after a tire size change",
        "url": "'''+URL+'''"
      }''',1)
    if f'href="{L}"' not in s:
        card='''          <a class="card-link" href="/guides/tire-balancing-vs-wheel-alignment/">Read the guide →</a>
        </article>'''
        assert card in s
        s=s.replace(card,card+f'''
        <article class="card">
          <h3>Speedometer error after a tire size change</h3>
          <p>Bigger or smaller tires? Work out your real speed, see worked examples and the 3 percent guidance, with a free in browser calculator.</p>
          <a class="card-link" href="{L}">Read the guide →</a>
        </article>''',1)
    p.write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/tire-balancing-vs-wheel-alignment/">New: Tire balancing vs wheel alignment</a>',f'<a class="btn btn-ghost" href="{L}">New: Speedometer error after a tire size change</a>')
    if f'<a href="{L}">speedometer error' not in s:
        s=s.replace('<a href="/guides/plus-sizing/">plus sizing</a>,',f'<a href="/guides/plus-sizing/">plus sizing</a>, <a href="{L}">speedometer error after a size change</a>,',1)
    p.write_text(s)
    li=f'          <li><a href="{L}">Speedometer error after a tire size change</a></li>\n'
    for g in ["guides/plus-sizing","tools/tire-size-calculator","guides/load-index-speed-rating","fitment/choose-tire-size"]:
        p=R/f"{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,1); assert L in s,g; p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        s=s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/fitment-wheel-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n</urlset>')
    for u in ["","guides/","guides/plus-sizing/","tools/tire-size-calculator/","guides/load-index-speed-rating/","fitment/choose-tire-size/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>'+TODAY,s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [Speedometer error after a tire size change]({URL}): Taller tires make the speedometer read low, shorter tires read high; real speed = indicated speed x new diameter / old diameter; worked examples; Continental's plus or minus 3 percent rolling circumference guidance; odometer error; client side calculator. Cites Continental and NHTSA.\n"
        s=s.replace("- [Nitrogen vs air",line+"- [Nitrogen vs air",1); assert SLUG in s; p.write_text(s)
build(); links(); sitemap_llms(); print("ok")
