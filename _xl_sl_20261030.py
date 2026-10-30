#!/usr/bin/env python3
"""Re-runnable: create /guides/xl-vs-sl-tires/, link it, sitemap, llms."""
import json, re, pathlib
R = pathlib.Path(__file__).parent
SLUG = "xl-vs-sl-tires"
URL = f"https://smarttirepicks.com/guides/{SLUG}/"
TODAY = "2026-10-30"
TITLE = "XL vs SL Tires: Extra Load, Standard Load and RF Explained"
H1 = "XL vs SL tires: what Extra Load, Standard Load and RF mean"
DESC = "What XL, SL, REINF and RF mean on a tire sidewall, how Extra Load changes max load and pressure, why the door placard still rules, and when you need XL."
ALT = "Alloy wheel and tire on a car, illustrating the load markings on a tire sidewall"
USTMA = "https://www.ustires.org/system/files/files/2024-05/Care%20and%20Service%20Passenger%20and%20Light%20Truck%20Tires%20FINAL%2006%2028%2017.pdf"
BSMAN = "https://www.bridgestoneamericas.com/content/dam/corpcomm/americas/images/company/tire-safety/TireReplacementManual.pdf"
CONTI = "https://continentaltire.com/sites/default/files/media/file/2021-01/plus_sizing_0.pdf"
FAQ = [
 ("What does XL mean on a tire?", "XL stands for Extra Load. An XL tire is built to carry more weight than the standard load version of the same size, but it only reaches that extra capacity at a higher inflation pressure. Euro metric tires may say Reinforced, REINF or RF instead; these mean the same thing as Extra Load."),
 ("What does SL mean, and what if there is no marking?", "SL stands for Standard Load. Many standard load tires carry no load marking at all, so a passenger tire without XL, Extra Load or Reinforced on the sidewall is a standard load tire."),
 ("Is RF on a tire reinforced or run flat?", "It depends where it appears. As a separate marking next to the size, RF means reinforced, the same as XL. When the letters RF sit inside the size itself before the rim diameter, as in 245/45RF19, they mark a self supporting run flat tire."),
 ("Should I inflate XL tires to the pressure on the sidewall?", "No. The pressure molded on the sidewall is the maximum the tire can hold, not a setting for your vehicle. Start from the cold pressure on the vehicle placard, never go below it, and never exceed the sidewall maximum."),
 ("Can I put XL tires on a car that came with SL tires?", "Usually yes, as long as the replacement carries at least the original load capacity at the pressure you run. Continental advises a higher pressure when an XL tire replaces an SL tire with the same or a slightly higher load index; see the table above, and ask the installer to confirm."),
 ("Do XL tires always carry more weight?", "Not at every pressure. In the USTMA load tables, a 205/55R16 94 XL carries slightly less than a 205/55R16 91 SL at 35 psi and only pulls ahead from 38 psi up. That is why a higher load index alone does not prove an XL tire is a suitable swap."),
 ("When do I need XL tires?", "When the vehicle maker specifies XL or a load index that only an XL tire offers in your size, and often when plus sizing to a lower profile tire that would otherwise carry less load than the original. Check the placard and owner's manual first."),
]
SOURCES = [
 (USTMA,"USTMA, Care and Service of Passenger and Light Truck Tires (PDF)","sidewall maximum pressures for Standard Load (35, 36, 44 or 51 psi) and Extra Load (41, 42 or 50 psi) tires; sidewall pressure is a maximum, not a vehicle setting; never go below the placard pressure; load capacity table for 205/55R16 SL and XL"),
 (BSMAN,"Bridgestone Americas, Replacement Tire Selection Manual (PDF)","XL and reinforced tires need higher pressure to reach added load; Euro metric XL tires may offer less load at some pressures; minimum pressure for maximum load by tire type; no load increase above 41 psi (P metric XL) or 42 psi (Euro metric XL)"),
 ("https://tires.bridgestone.com/en-us/learn/automotive/tire-terminology","Bridgestone, Tire Terminology","for Euro metric tires Reinforced means the same as Extra Load; P metric and Euro metric size formats"),
 (CONTI,"Continental Tire, Plus sizing (PDF)","replacement load capacity must equal or exceed the original at placard pressure; pressure increases when Extra Load tires replace Standard Load tires"),
 ("https://www.michelin.co.uk/auto/advice/van/reinforced-tyres-utility-vehicles","Michelin UK, Are reinforced tyres mandatory for utility vehicles?","XL means a higher load rating than usual for the size; REINF or RF means reinforced; C marking is for vans and light commercial vehicles"),
 ("https://www.toyotires.com/media/pxcjubjs/application_of_load_inflation_tables_20200723.pdf","Toyo Tires, Application of Load Inflation Tables (PDF)","Reinforced and Extra Load both mean extra load capacity at higher pressure; no marking means standard load; ETRTO publishes separate standard and reinforced tables"),
 ("https://energy-efficient-products.ec.europa.eu/product-list/tyres/how-read-tyre-parameters_en","European Commission, How to read the tyre parameters","run flat tyres carry an F before the rim diameter, as in 245/45RF19, plus a pictogram"),
]
PICK = '''      <section class="content-section tool" id="load-marking-picker">
        <h2>What does my sidewall marking mean?</h2>
        <p>Pick the marking you see near the tire size. This runs entirely in your browser and nothing is sent or stored.</p>
        <form id="lm-form" onsubmit="return false">
          <label>Marking <select id="lm-sel">
            <option value="none">No load marking</option>
            <option value="sl">SL</option>
            <option value="xl">XL or EXTRA LOAD</option>
            <option value="rf">REINF, REINFORCED or RF (separate from the size)</option>
            <option value="rfsize">RF inside the size, for example 245/45RF19</option>
            <option value="c">C after the size (van tires)</option>
          </select></label><br>
          <label>Size starts with P? <select id="lm-p"><option value="eu">No (Euro metric)</option><option value="p">Yes (P metric)</option></select></label>
        </form>
        <p id="lm-out" aria-live="polite"></p>
        <script>
        (function(){var T={none:'Standard load. A passenger tire with no XL or Reinforced marking is a standard load tire.',sl:'Standard Load. The normal load version of this size.',xl:'Extra Load. Carries more than the standard version of the same size, but only at higher pressure.',rf:'Reinforced. On Euro metric tires this means the same as Extra Load (XL).',rfsize:'Run flat. RF inside the size marks a self supporting run flat tire, not a load marking.',c:'Commercial. A C tire is a van or light commercial tire with its own load rules; follow the vehicle maker.'};
        var M={p:{sl:35,xl:41},eu:{sl:36,xl:42}};
        var s=document.getElementById('lm-sel'),q=document.getElementById('lm-p'),o=document.getElementById('lm-out');
        function run(){var v=s.value,k=(v==='xl'||v==='rf')?'xl':((v==='none'||v==='sl')?'sl':null),t='<strong>Meaning:</strong> '+T[v];
        if(k){t+=' Bridgestone lists '+M[q.value][k]+' psi as the minimum pressure for this tire\\'s maximum load. Your actual cold pressure still comes from the vehicle placard.';}
        o.innerHTML=t;}
        s.addEventListener('change',run);q.addEventListener('change',run);run();})();
        </script>
        <p>General explanation only. Always confirm with the vehicle placard, owner's manual and tire maker.</p>
      </section>
'''
TABLE_ROWS = [("205/55R16 91 (SL)","1224","1312","1356","1356","1356"),("205/55R16 94 (XL)","1179","1268","1356","1433","1477")]
CONTI_ROWS = [("Same as the original SL tire","Add 0.4 bar (6 psi)"),("Original plus 1","Add 0.3 bar (4 psi)"),("Original plus 2","Add 0.2 bar (3 psi)"),("Original plus 3","Add 0.1 bar (2 psi)"),("Original plus 4 or more","Same pressure as the original")]
BODY = f'''<main id="main">
    <div class="wrap">
      <h1 class="page-title">{H1}</h1>
<p class="lede">Short answer: <strong>SL</strong> (Standard Load) is the normal version of a tire size. <strong>XL</strong> (Extra Load), also marked <strong>REINF</strong> or <strong>RF</strong> on Euro metric tires, can carry more weight, but only at a <strong>higher inflation pressure</strong>. Whichever you fit, set cold pressure from your vehicle placard, never below it, and never above the maximum on the sidewall.</p>
<p class="last-updated">Last updated: October 30, 2026</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/fitment-wheel-1024.webp" srcset="/assets/img/fitment-wheel-640.webp 640w, /assets/img/fitment-wheel-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{ALT}" fetchpriority="high" decoding="async"><figcaption>Illustrative AI generated photo.</figcaption></figure>
{PICK}      <section class="content-section">
        <h2>What the markings mean</h2>
        <ul>
          <li><strong>SL or no marking:</strong> Standard Load. Toyo notes that when a sidewall has no Reinforced or Extra Load marking, the tire is a standard load tire.</li>
          <li><strong>XL or EXTRA LOAD:</strong> a tire with a higher load rating than is usual for the same size, so it can work at higher pressures (Michelin).</li>
          <li><strong>REINF, REINFORCED or RF:</strong> the Euro metric term. Bridgestone says Reinforced means the same as Extra Load for Euro metric tires.</li>
          <li><strong>RF inside the size, such as 245/45RF19:</strong> not a load marking. The European Commission explains that an F before the rim diameter, plus a pictogram, marks a self supporting run flat tire.</li>
          <li><strong>C after the size:</strong> a van or light commercial tire, a separate category from XL (Michelin).</li>
        </ul>
        <p>The load index number in the service description, such as the 94 in 205/55R16 94V, gives the maximum load. See our <a href="/guides/load-index-speed-rating/">load index and speed rating guide</a> for the chart.</p>
      </section>
      <section class="content-section">
        <h2>How XL changes load and pressure</h2>
        <p>Bridgestone explains that an XL tire offers a higher maximum load than the SL version of the same size, but needs higher inflation pressure to reach it. The USTMA load table shows what that looks like in pounds per tire:</p>
        <table class="data-table">
          <thead><tr><th>Tire</th><th>32 psi</th><th>35 psi</th><th>38 psi</th><th>41 psi</th><th>44 psi</th></tr></thead>
          <tbody>
''' + "\n".join("            <tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in TABLE_ROWS) + f'''
          </tbody>
        </table>
        <p>Source: USTMA, load capacity in lb. At 35 psi the XL tire actually carries a little less than the SL tire, even though its load index is higher. It only pulls ahead from 38 psi up. Bridgestone warns about exactly this: a higher load index on a Euro metric XL tire is not always proof it can carry the load at your pressure.</p>
        <h3>Minimum pressure for maximum load</h3>
        <table class="data-table">
          <thead><tr><th>Tire type</th><th>Standard Load</th><th>Extra Load</th></tr></thead>
          <tbody>
            <tr><td>P metric (size starts with P)</td><td>35 psi (240 kPa)</td><td>41 psi (280 kPa)</td></tr>
            <tr><td>Euro metric (no P)</td><td>36 psi (250 kPa)</td><td>42 psi (290 kPa)</td></tr>
          </tbody>
        </table>
        <p>Source: Bridgestone. Bridgestone also notes that some XL tires are branded with a higher maximum, such as 50 or 51 psi, but carry no more load above 41 psi (P metric) or 42 psi (Euro metric). The two size systems use different load tables, so compare like with like.</p>
      </section>
      <section class="content-section">
        <h2>Why the vehicle placard still rules</h2>
        <p>USTMA is clear that the pressure molded on the sidewall is the maximum the tire can hold, regardless of vehicle or load, and is not the pressure to run. Typical sidewall maximums are 35, 36, 44 or 51 psi for Standard Load tires and 41, 42 or 50 psi for Extra Load tires. Your starting point is the cold pressure on the <a href="/guides/placard/">door placard</a> or in the owner's manual, and you should never set pressure below it. Read more in our <a href="/guides/tire-pressure/">cold tire pressure guide</a>.</p>
      </section>
      <section class="content-section">
        <h2>When you need XL tires</h2>
        <ul>
          <li><strong>The vehicle maker specifies it.</strong> If the placard or manual lists an XL size or a load index only XL tires reach, stay with XL.</li>
          <li><strong>Plus sizing.</strong> Continental says a replacement must carry at least the original load at the placard pressure. A lower profile size may need XL construction, and sometimes a higher pressure, to get there. See <a href="/guides/plus-sizing/">plus sizing</a>.</li>
          <li><strong>Swapping SL for XL.</strong> Continental gives these pressure changes when an XL tire replaces the original SL tire:</li>
        </ul>
        <table class="data-table">
          <thead><tr><th>XL load index vs original SL</th><th>Pressure change</th></tr></thead>
          <tbody>
''' + "\n".join(f"            <tr><td>{a}</td><td>{b}</td></tr>" for a,b in CONTI_ROWS) + f'''
          </tbody>
        </table>
        <p>Never exceed the sidewall maximum, and keep any front to rear pressure difference the vehicle maker specifies. If the new pressure differs from the placard, note it so anyone who checks the tires later uses the right figure. For sizes, start with <a href="/fitment/choose-tire-size/">how to choose the right tire size</a>.</p>
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
          <li><a href="/guides/load-index-speed-rating/">Load index and speed rating</a></li>
          <li><a href="/guides/tire-pressure/">Cold tire pressure guide</a></li>
          <li><a href="/guides/plus-sizing/">Plus sizing guide</a></li>
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
def bc_ld(): return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://smarttirepicks.com/"},{"@type":"ListItem","position":2,"name":"Guides","item":"https://smarttirepicks.com/guides/"},{"@type":"ListItem","position":3,"name":"XL vs SL tires","item":URL}]},indent=2)
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
        old='''        "url": "https://smarttirepicks.com/guides/speedometer-error-tire-size/"
      }'''
        assert old in s
        s=s.replace(old,old[:-1]+'''},
      {
        "@type": "ListItem",
        "position": 29,
        "name": "XL vs SL tires",
        "url": "'''+URL+'''"
      }''',1)
    if f'href="{L}"' not in s:
        card='''          <a class="card-link" href="/guides/speedometer-error-tire-size/">Read the guide →</a>
        </article>'''
        assert card in s
        s=s.replace(card,card+f'''
        <article class="card">
          <h3>XL vs SL tires</h3>
          <p>What XL, SL, REINF and RF mean on a sidewall, how Extra Load changes load and pressure, and when you need it. Includes a marking picker.</p>
          <a class="card-link" href="{L}">Read the guide →</a>
        </article>''',1)
    p.write_text(s)
    p=R/"index.html"; s=p.read_text()
    s=s.replace('<a class="btn btn-ghost" href="/guides/speedometer-error-tire-size/">New: Speedometer error after a tire size change</a>',f'<a class="btn btn-ghost" href="{L}">New: XL vs SL tires explained</a>')
    if f'<a href="{L}">XL vs SL' not in s:
        s=s.replace('<a href="/guides/plus-sizing/">plus sizing</a>,',f'<a href="/guides/plus-sizing/">plus sizing</a>, <a href="{L}">XL vs SL tires</a>,',1)
    assert f'<a href="{L}">XL vs SL' in s; p.write_text(s)
    li=f'          <li><a href="{L}">XL vs SL tires (Extra Load explained)</a></li>\n'
    for g in ["guides/plus-sizing","guides/load-index-speed-rating","fitment/choose-tire-size","guides/tire-pressure"]:
        p=R/f"{g}/index.html"; s=p.read_text()
        if L in s: continue
        s=re.sub(r'(<nav class="related-links"[^>]*>\s*<h2>Keep reading</h2>\s*<ul>\n)',lambda m:m.group(1)+li,s,1); assert L in s,g
        if g=="guides/load-index-speed-rating":
            s=s.replace('<h2>XL / Extra Load (or Reinforced) vs standard load</h2>\n',f'<h2>XL / Extra Load (or Reinforced) vs standard load</h2>\n        <p>Full explainer with load tables and pressure guidance: <a href="{L}">XL vs SL tires</a>.</p>\n',1)
        p.write_text(s)
def sitemap_llms():
    p=R/"sitemap.xml"; s=p.read_text()
    if SLUG not in s:
        s=s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority><image:image><image:loc>https://smarttirepicks.com/assets/img/fitment-wheel-1024.webp</image:loc><image:caption>{ALT}</image:caption></image:image></url>\n</urlset>')
    for u in ["","guides/","guides/plus-sizing/","guides/load-index-speed-rating/","fitment/choose-tire-size/","guides/tire-pressure/"]:
        s=re.sub(rf'(<loc>https://smarttirepicks.com/{re.escape(u)}</loc><lastmod>)[^<]*',r'\g<1>'+TODAY,s)
    p.write_text(s)
    p=R/"llms.txt"; s=p.read_text()
    if SLUG not in s:
        line=f"- [XL vs SL tires]({URL}): SL is standard load (often unmarked); XL, Extra Load, REINF or RF mean extra load capacity at higher pressure; RF inside the size (245/45RF19) means run flat; USTMA 205/55R16 SL vs XL load table; minimum pressure for max load (P metric 35/41 psi, Euro metric 36/42 psi); placard pressure rules; Continental SL to XL pressure table; client side marking picker. Cites USTMA, Bridgestone, Continental, Michelin, Toyo, European Commission.\n"
        s=s.replace("- [Nitrogen vs air",line+"- [Nitrogen vs air",1); assert SLUG in s; p.write_text(s)
build(); links(); sitemap_llms(); print("ok")
