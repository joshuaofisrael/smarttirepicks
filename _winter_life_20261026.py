#!/usr/bin/env python3
"""Re-runnable: create /guides/how-long-do-winter-tires-last/, link it, retitle pages, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "how-long-do-winter-tires-last"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TITLE = "How Long Do Winter Tires Last? Seasons and Tread"
H1 = "How long do winter tires last?"
DESC = "Most winter tires last about 3 to 4 seasons. Replace them for snow use near 6/32 inch, or at 4/32 at the latest, and check age, storage and wear signs."
ALT = "Car tire with packed snow in the tread on a snowy road, showing winter tire tread at work"
FAQ = [
 ("How many seasons do winter tires last?", "Consumer Reports gives a guideline of two or three seasons, and many drivers who swap tires on and off each year get three or four. The real limit is remaining tread depth and condition, not a fixed number of winters, so measure each fall."),
 ("At what tread depth should I replace winter tires?", "For dependable snow grip, plan to replace winter tires at about 6/32 inch (about 5 mm). Consumer Reports says you want at least 4/32 inch in the middle of winter. British Columbia requires 3.5 mm (about 4/32 inch) for a tire to count as a legal winter tire on signed routes."),
 ("How many miles do winter tires last?", "Many drivers get roughly 10,000 to 20,000 miles of winter use before the tread is too shallow for good snow traction, but this varies widely with the model, the car, mileage per winter and how warm the roads are. Treat any mileage number as a rough guide and measure the tread."),
 ("Can I use winter tires all year?", "It is not recommended. Soft winter compounds wear quickly on warm pavement, and Transport Canada notes winter tires are designed for cold weather. Running them in summer can use up a season or more of tread and give up dry and wet handling."),
 ("Do winter tires expire if they are not used?", "Rubber ages even in storage. Goodyear recommends replacing tires after 6 years in service and Michelin and Continental say no tire should stay in service beyond 10 years from manufacture. Read the DOT date code and have older tires inspected."),
 ("How can I make winter tires last longer?", "Take them off once temperatures stay above about 7°C (45°F), store them cool, dry and out of sunlight away from ozone sources, keep them at the placard cold pressure, rotate them each season, and keep the alignment in spec."),
]
SOURCES = [
 ("https://www.consumerreports.org/cro/news/2012/11/time-to-start-thinking-about-winter-tires/index.htm","Consumer Reports, Time to start thinking about winter tires","as a guideline, two or three seasons from a set of winter tires; inspect before installing"),
 ("https://www.consumerreports.org/cars/tires/make-sure-your-tires-have-enough-tread-for-winter-a6082176624","Consumer Reports, Make sure your tires have enough tread for a snowy winter","half worn tires lost about 14 percent snow traction; keep at least 4/32 inch through winter"),
 ("https://tc.canada.ca/en/road-transportation/stay-safe-when-driving/winter-driving/using-winter-tires","Transport Canada, Using winter tires","below 7°C all season tires lose elasticity; winter tires designed for cold; fit four"),
 ("https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/traveller-information/seasonal/winter-driving/about-winter-tires","Government of British Columbia, Winter tire requirements","legal winter tire needs at least 3.5 mm of tread and M+S or 3PMSF"),
 ("https://www.bridgestonetire.com/catalog/bridgestone/blizzak-ws90/","Bridgestone, Blizzak WS90","Multicell winter compound in the upper part of the tread (about the first 55 percent), so ice grip declines as it wears"),
 ("https://www.nhtsa.gov/equipment/tires","NHTSA, Tires","tire aging, DOT date codes and checking tread"),
 ("https://www.ustires.org/tire-care","USTMA, Tire care","proper storage, inflation and rotation"),
]
def faq_ld():
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},indent=2)
def art_ld():
    org={"@type":"Organization","@id":"https://smarttirepicks.com/#organization","name":"Smart Tire Picks"}
    return json.dumps({"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":"https://smarttirepicks.com/assets/img/og-winter-tires.jpg","datePublished":"2026-10-26","dateModified":"2026-10-26","inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":"https://smarttirepicks.com/#website","name":"Smart Tire Picks"}},indent=2)
def bc_ld():
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"How long do winter tires last","item":URL}]},indent=2)
BODY = f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: most winter tires last about three to four seasons if you put them on only for the cold months, and Consumer Reports uses two or three seasons as a conservative guideline. The number that matters is tread depth: plan to replace winter tires at about 6/32 inch for dependable snow grip, and do not start a winter below 4/32 inch.</p>
<p class="last-updated">Last updated: October 26, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/winter-tires-1024.webp" srcset="/assets/img/winter-tires-640.webp 640w, /assets/img/winter-tires-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
      <section class="content-section">
        <h2>Seasons, miles and tread at a glance</h2>
        <table class="data-table">
          <thead><tr><th>Measure</th><th>Typical range</th><th>What drives it</th></tr></thead>
          <tbody>
            <tr><td>Seasons</td><td>About 3 to 4 (CR guideline 2 to 3)</td><td>Miles per winter, how early you swap off in spring</td></tr>
            <tr><td>Miles of winter use</td><td>Roughly 10,000 to 20,000, varies widely</td><td>Tire model, vehicle weight, warm dry road time</td></tr>
            <tr><td>New tread depth</td><td>Often about 10/32 to 12/32 inch</td><td>Check the exact model's spec</td></tr>
            <tr><td>Replace for snow use</td><td>About 6/32 inch (5 mm)</td><td>Snow traction falls as the tread gets shallow</td></tr>
            <tr><td>Do not start winter below</td><td>4/32 inch (about 3.5 mm, the BC legal minimum)</td><td>Consumer Reports and British Columbia rules</td></tr>
            <tr><td>Age limit</td><td>6 years in service (Goodyear) to 10 years from manufacture (Michelin, Continental)</td><td>Rubber ages even in storage</td></tr>
          </tbody>
        </table>
        <p>Mileage figures are rough, editorial ranges, not test results. Your own tread gauge is the real answer.</p>
      </section>
      <section class="content-section">
        <h2>Why tread depth matters more for winter tires</h2>
        <p>Snow grip comes from deep grooves and many sipes that pack and hold snow. Consumer Reports found that all season tires worn to about half their tread lost roughly 14 percent of their snow traction and stopped about 7 percent longer in the wet. Winter tires lose the same kind of bite as they wear, which is why a winter tire can be legal for dry roads long before it is still good in snow.</p>
        <p>Some winter tires also put their special cold weather compound only in the upper part of the tread. Bridgestone describes its Blizzak Multicell compound this way, and it is commonly cited as about the first 55 percent of the tread. Once that layer is gone, ice grip drops noticeably, which is one more reason to retire winter tires around 6/32 inch rather than running them to the 2/32 inch wear bars.</p>
        <p>As a legal benchmark, British Columbia only counts a tire as a winter tire on its signed routes if it has at least 3.5 mm of tread (about 4/32 inch) and the M+S or three peak mountain snowflake mark. See our <a href="/guides/tread-depth/">tread depth guide</a> for how to measure and a 32nds to mm chart.</p>
      </section>
      <section class="content-section">
        <h2>Check your winter tires every fall</h2>
        <ol>
          <li><strong>Measure tread</strong> in the center and both shoulders of every tire with a gauge. Plan replacements at about 6/32 inch.</li>
          <li><strong>Read the DOT date code.</strong> The last four digits are the week and year made. See <a href="/guides/dot-date-codes/">how to read DOT date codes</a>.</li>
          <li><strong>Look for damage:</strong> cracks in the sidewall or tread grooves, cuts, bulges, or uneven wear that hints at alignment or pressure problems.</li>
          <li><strong>Check that all four match.</strong> Transport Canada advises fitting winter tires in sets of four. If one is worn out, compare the others before mixing.</li>
          <li><strong>Set cold pressure</strong> to your door placard after mounting, since pressure drops as temperatures fall. See our <a href="/guides/tire-pressure/">tire pressure guide</a>.</li>
        </ol>
      </section>
      <section class="content-section">
        <h2>What wears winter tires out faster</h2>
        <ul>
          <li><strong>Warm pavement.</strong> Soft winter compounds wear quickly once temperatures stay above about 7°C (45°F). Swap them off in spring rather than leaving them on.</li>
          <li><strong>Using them all year.</strong> A summer on winter tires can cost a full season or more of tread.</li>
          <li><strong>Low pressure or bad alignment</strong>, which wear the shoulders or one edge.</li>
          <li><strong>Poor storage</strong>: heat, sunlight and ozone from motors age the rubber. See <a href="/guides/seasonal-tire-storage/">seasonal tire storage</a>.</li>
          <li><strong>Heavy vehicles and hard driving</strong>, including fast starts and high speed highway miles.</li>
        </ul>
      </section>
      <section class="content-section">
        <h2>How to make winter tires last longer</h2>
        <ul>
          <li>Put them on when temperatures stay near 7°C (45°F) and take them off when they stay above it. Our <a href="/guides/winter-tires/">winter tires guide</a> covers timing.</li>
          <li>Mount them on a second set of wheels so each swap is quick and the beads are not stressed by repeated mounting.</li>
          <li>Rotate them each season, marking position when you remove them. See <a href="/guides/tire-rotation/">tire rotation patterns</a>.</li>
          <li>Clean, dry and store them cool, dark and away from ozone sources.</li>
          <li>If winters are mild where you live, an all weather tire may suit you better than two sets. Compare in <a href="/guides/all-weather-vs-all-season/">all weather vs all season tires</a>.</li>
        </ul>
        <p>Not sure how long your regular tires will last? See <a href="/guides/how-long-do-tires-last/">how long do tires last</a> and <a href="/guides/when-to-replace/">when to replace tires</a>. Have a licensed professional inspect any tire you are unsure about.</p>
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
          <li><a href="/guides/winter-tires/">Winter tires: when to switch and what to buy</a></li>
          <li><a href="/guides/all-weather-vs-all-season/">All weather vs all season tires</a></li>
          <li><a href="/guides/seasonal-tire-storage/">Seasonal tire storage</a></li>
          <li><a href="/guides/tread-depth/">Tread depth guide</a></li>
          <li><a href="/guides/how-long-do-tires-last/">How long do tires last?</a></li>
          <li><a href="/guides/">All tire guides</a></li>
        </ul>
      </nav>
    </div>
  </main>'''
def build():
    t=(R/"guides/all-weather-vs-all-season/index.html").read_text()
    head,rest=t.split('<main id="main">',1); foot=rest.split('</main>',1)[1]
    head=head.replace("guides/all-weather-vs-all-season/",f"guides/{SLUG}/")
    head=re.sub(r"<title>.*?</title>",f"<title>{TITLE}</title>",head)
    for p in ['og:title','twitter:title']: head=re.sub(rf'(property|name)="{p}" content="[^"]*"',rf'\1="{p}" content="{TITLE}"',head)
    for p in ['name="description"','property="og:description"','name="twitter:description"']: head=re.sub(rf'{p} content="[^"]*"',f'{p} content="{DESC}"',head)
    for p in ['og:image:alt','twitter:image:alt']: head=re.sub(rf'"{p}" content="[^"]*"',f'"{p}" content="{ALT}"',head)
    head=re.sub(r'(<script type="application/ld\+json">).*(</head>)',lambda m:"<script type=\"application/ld+json\">\n"+bc_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+art_ld()+"\n  </script>\n  <script type=\"application/ld+json\">\n"+faq_ld()+"\n  </script>\n</head>",head,flags=re.S)
    d=R/f"guides/{SLUG}"; d.mkdir(exist_ok=True); (d/"index.html").write_text(head+BODY+foot)
def sub_once(path, marker, old, new):
    p=R/path; s=p.read_text()
    if marker in s: return
    assert old in s, (path, old[:40]); p.write_text(s.replace(old,new,1))
def links():
    L=f'/guides/{SLUG}/'
    sub_once("guides/index.html",L,'''        "url": "https://smarttirepicks.com/guides/all-weather-vs-all-season/"
      }''','''        "url": "https://smarttirepicks.com/guides/all-weather-vs-all-season/"
      },
      {
        "@type": "ListItem",
        "position": 26,
        "name": "How long do winter tires last",
        "url": "https://smarttirepicks.com/guides/how-long-do-winter-tires-last/"
      }''')
    s=(R/"guides/index.html").read_text()
    if s.count(L)<2:
        card='''          <a class="card-link" href="/guides/all-weather-vs-all-season/">Read the guide →</a>
        </article>'''
        s=s.replace(card,card+'''
        <article class="card">
          <h3>How long do winter tires last?</h3>
          <p>How many seasons and miles to expect, why to replace winter tires near 6/32 inch, age limits, a fall checklist, and how to make a set last longer.</p>
          <a class="card-link" href="/guides/how-long-do-winter-tires-last/">Read the guide →</a>
        </article>''',1); (R/"guides/index.html").write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/all-weather-vs-all-season/">New: All weather vs all season tires</a>',f'<a class="btn btn-ghost" href="{L}">New: How long do winter tires last?</a>')
    if f'<a href="{L}">how long winter tires last' not in s:
        s=s.replace('<a href="/guides/all-weather-vs-all-season/">all weather vs all season tires</a>,',f'<a href="/guides/all-weather-vs-all-season/">all weather vs all season tires</a>, <a href="{L}">how long winter tires last</a>,',1)
    p.write_text(s)
    li=f'          <li><a href="{L}">How long do winter tires last?</a></li>\n'
    for g in ["winter-tires","seasonal-tire-storage","all-weather-vs-all-season","how-long-do-tires-last","tread-depth"]:
        p=R/f"guides/{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,1); assert L in s,g; p.write_text(s)
RETITLE={
 "guides/when-to-replace/index.html":("When to Replace Tires: Tread Depth, Age and Damage","When should you replace tires? At 2/32 inch tread at the latest, sooner for rain and snow, plus age limits, damage signs and uneven wear to watch for."),
 "guides/placard/index.html":("Tire Placard: How to Read Your Door Tire Label","Where to find the tire placard on your door jamb and how to read it: original tire size, cold PSI front, rear and spare, load limits, and if it is missing."),
 "comparisons/all-season-vs-winter/index.html":("All Season vs Winter Tires: Which Do You Need?","All season vs winter tires compared: grip below 45°F, snow and ice, cost of two sets, and when all season tires are enough for your winters."),
 "guides/seasonal-tire-storage/index.html":("How to Store Tires: Winter and Summer Tire Storage","How to store tires off season: stack or stand them, on or off rims, cool, dark and away from ozone. A simple USTMA cited tire storage checklist."),
 "guides/winter-tires/index.html":("When to Put On Winter Tires (45°F Rule) and What to Buy","When to put on winter tires: once it stays near 45°F (7°C). Snowflake vs M+S marks, all weather vs winter, stud rules by state, and why to fit four."),
}
def retitle():
    for f,(t,d) in RETITLE.items():
        assert len(t)<=60 and len(d)<=155,(f,len(t),len(d))
        p=R/f; s=p.read_text()
        s=re.sub(r"<title>.*?</title>",f"<title>{t}</title>",s,1)
        for k in ['property="og:title"','name="twitter:title"']: s=re.sub(rf'{k} content="[^"]*"',f'{k} content="{t}"',s)
        for k in ['name="description"','property="og:description"','name="twitter:description"']: s=re.sub(rf'{k} content="[^"]*"',f'{k} content="{d}"',s)
        p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        entry=f'  <url><loc>{URL}</loc><lastmod>2026-10-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/winter-tires-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n'
        s=s.replace('</urlset>',entry+'</urlset>')
    for u in ["","guides/","guides/winter-tires/","guides/seasonal-tire-storage/","guides/all-weather-vs-all-season/","guides/how-long-do-tires-last/","guides/tread-depth/","guides/when-to-replace/","guides/placard/","comparisons/all-season-vs-winter/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>2026-10-26',s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [How long do winter tires last?]({URL}): Most winter tires last about 3 to 4 seasons (Consumer Reports guideline 2 to 3); replace for snow use near 6/32 inch and do not start a winter below 4/32 inch (BC legal minimum 3.5 mm); some compounds such as Bridgestone Multicell sit in the upper tread; age limits 6 to 10 years; fall checklist and tips. Cites Consumer Reports, Transport Canada, British Columbia, Bridgestone, NHTSA and USTMA.\n"
        s=s.replace("- [Nitrogen vs air",line+"- [Nitrogen vs air",1)
        p.write_text(s)
build(); links(); retitle(); sitemap_llms(); print("ok")
