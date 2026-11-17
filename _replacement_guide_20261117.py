#!/usr/bin/env python3
"""Build /guides/how-to-choose-replacement-tires/ (17 Nov 2026). Every claim maps to a source opened 17 Nov 2026.
Reuses the head, nav and footer pattern of _which_tire_20261116.py. No branded model is recommended."""
import json, re
from pathlib import Path
import importlib.util
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("wt", ROOT / "_which_tire_20261116.py"); wt = importlib.util.module_from_spec(spec); spec.loader.exec_module(wt)
a, esc, SRC, DISC, FOOT, BASE = wt.a, wt.esc, wt.SRC, wt.DISC, wt.FOOT, wt.BASE
NAV = wt.NAV.replace('<li><a href="/guides/">Guides</a></li>', '<li><a href="/guides/" aria-current="page">Guides</a></li>').format(wt='')
PUB, PUB_H, READ = "2026-11-17", "November 17, 2026", "read 17 November 2026"
SLUG = "how-to-choose-replacement-tires"; URL = f"{BASE}/guides/{SLUG}/"
STEM, ALT = "review-touring", "Sedan front tire and alloy wheel viewed from the side, the sidewall where size markings are molded"
TITLE = "How to choose replacement tires: copy the placard, then match 4 sidewall codes"
H1 = "How to choose replacement tires"
DESC = "Copy size, load index and speed rating from the door placard, never go lower, then pick a tire type for your climate. Two new tires go on the rear."
assert len(DESC) <= 155, len(DESC)
LEDE = "Start from the door placard, not the old tire. Buy the same size (or a maker approved option) with a load index that is not lower and a speed rating that is equal or higher, keep the same construction, then choose the tire type for your weather. Replace all four if you can; if you buy two, they go on the rear axle."
faqs = [
 ("How do I know what tire size my car needs?", f"NHTSA says to check the owner's manual or the Tire and Loading Information label on the driver's side door edge or post, and to buy the same size as the original tires or another size the vehicle maker recommends. If in doubt, ask the tire dealer."),
 ("Can I buy a different tire size?", "Only an approved option. USTMA says replacement tires should be the original equipment size or approved options recommended by the vehicle or tire maker, and never a smaller size or one with less load carrying capacity at placard pressure. Michelin gives the same advice."),
 ("Is a higher load index OK?", "Yes, equal or higher is allowed. Michelin says you can only mount a tire of equivalent or higher load than indicated for your vehicle. Lower is never OK, and pressure still comes from the placard."),
 ("Can I use a lower speed rating than the original tires?", "It is not recommended. USTMA says the speed rating must be equal to or greater than the vehicle maker specifies to keep the vehicle's speed capability; with a lower rated tire, the vehicle's speed is restricted to that of the tire and handling may change."),
 ("Should I inflate new tires to the max psi on the sidewall?", "No. NHTSA says the correct pressure is the one the vehicle maker lists on the door label or in the manual, not what is listed on the tire, measured cold (not driven for at least three hours)."),
 ("If I replace only two tires, do they go on the front or the rear?", "The rear. USTMA says two new tires of the same size and construction should go on the rear axle, because deeper tread grips better and clears water, which helps prevent oversteer on wet roads. Michelin says the same."),
 ("Can I replace just one tire on an AWD car?", "Check the owner's manual first. USTMA says some vehicle makers advise against replacing fewer than four tires, and that on 4WD and AWD vehicles even small differences in outside diameter may cause drivetrain damage."),
 ("Are used tires a good way to save money?", "Michelin advises avoiding used tires because you cannot know what damage or hard use a previously owned tire has had, and internal damage can lead to failure."),
]
srcs = [("NT", "where to find size and pressure, buying the original size, cold pressure, tire types, UTQG grades, spare use"),
        ("CS", "replacement size, load, inflation and speed rules, mixing, replacing one, two or four tires"),
        ("MCS", "approved sizes, load and speed rating rules, two new tires on the rear, used tires, speed and load charts"),
        ("MTY", "M+S vs 3PMSF and seasonal tire types")]
related = [("/guides/tire-size-sidewall-markings/", "How to read a tire size"), ("/guides/load-index-speed-rating/", "Load index and speed rating chart"),
           ("/guides/placard/", "Read your door placard"), ("/guides/mixing-tires/", "Can you mix tires? Replace 2 or 4"),
           ("/guides/utqg/", "UTQG treadwear and traction grades"), ("/which-tire/", "Which tire picker"), ("/guides/when-to-replace/", "When to replace tires")]
body = f"""      <section class="content-section">
        <h2>The short answer</h2>
        <p>{LEDE} Every rule below comes from NHTSA, USTMA or Michelin pages we opened for this guide; your vehicle maker's instructions win if they differ.</p>
      </section>
      <section class="content-section" id="placard">
        <h2>Step 1: copy the placard, not the old tire</h2>
        <p>NHTSA says the correct size is in the owner's manual or on the Tire and Loading Information label on the driver's side door edge or post, and that you should buy the same size as the original tires or another size the vehicle maker recommends ({a('NT','NHTSA TireWise')}). USTMA adds that the placard also lists the spare size and the cold pressures for the front and rear axles, and says not to guess ({a('CS','USTMA Care and Service')}). The tires on the car now may not be the original size, so treat them as a cross check only. Our <a href="/guides/tire-placard-checklist/">placard checklist</a> lists what to write down.</p>
      </section>
      <section class="content-section" id="codes">
        <h2>Step 2: match these four codes on the sidewall</h2>
        <p>Using P225/60R16 97V as the example (full breakdown in <a href="/guides/tire-size-sidewall-markings/">how to read a tire size</a>):</p>
        <table>
          <thead><tr><th>Code</th><th>Example</th><th>Rule for the replacement</th></tr></thead>
          <tbody>
            <tr><td>Size</td><td>P225/60R16</td><td>Same size or a maker approved option; never smaller ({a('CS','USTMA')})</td></tr>
            <tr><td>Load index</td><td>97 (1,609 lb per tire on Michelin's chart)</td><td>Equal or higher; never less load capacity at placard pressure ({a('MCS','Michelin')}, {a('CS','USTMA')})</td></tr>
            <tr><td>Speed rating</td><td>V (149 mph on Michelin's chart)</td><td>Equal or higher than the vehicle maker specifies ({a('CS','USTMA')})</td></tr>
            <tr><td>Construction</td><td>R (radial), P (passenger) or LT</td><td>Keep all four the same size, speed rating and construction ({a('CS','USTMA')})</td></tr>
          </tbody>
        </table>
        <p>USTMA also says a replacement must have an inflation pressure capability at least equal to the placard pressure, and that front and rear differences on the placard must be kept ({a('CS','USTMA')}). If a lower speed rated tire is fitted, USTMA says the vehicle's speed is restricted to that tire's rating and handling could change. If mixing speed ratings cannot be avoided, Michelin says the lower rated tires go on the front axle ({a('MCS','Michelin')}). Load index and speed symbols are listed in our <a href="/guides/load-index-speed-rating/">chart</a>; XL tires are explained in <a href="/guides/xl-vs-sl-tires/">XL vs SL</a>.</p>
      </section>
      <section class="content-section" id="type">
        <h2>Step 3: choose the tire type for your weather</h2>
        <p>With the codes fixed, the real choice is the tire type. NHTSA says all season tires handle a variety of road conditions with some mud and snow ability, winter tires are more effective in deep snow, summer tires are not designed for temperatures below freezing or for snow and ice, and all terrain tires are mainly for four wheel drive vehicles as an on road and off road compromise ({a('NT','NHTSA')}). For snow without a second set, Michelin says all weather tires carry the 3PMSF symbol, which requires a packed snow traction test, while M+S is based on tread geometry only ({a('MTY','Michelin')}). Our <a href="/which-tire/">which tire picker</a> narrows the category by vehicle, climate and driving.</p>
        <p>To compare tires within a type, NHTSA says the UTQG treadwear grade is relative to a control tire graded 100 (a 200 should wear twice as long under the test), and traction grades run AA, A, B, C for stopping on wet pavement ({a('NT','NHTSA')}). See our <a href="/guides/utqg/">UTQG guide</a>.</p>
      </section>
      <section class="content-section" id="how-many">
        <h2>Step 4: decide how many to replace</h2>
        <ul>
          <li><b>Four:</b> USTMA says replacing all four at the same time is recommended and preferred, and some vehicle makers advise against replacing fewer ({a('CS','USTMA')}).</li>
          <li><b>Two:</b> the new pair goes on the rear axle. USTMA says deeper tread grips better and clears water, and more grip at the rear on wet roads helps prevent oversteer ({a('CS','USTMA')}, {a('MCS','Michelin')}).</li>
          <li><b>One:</b> USTMA says pair the new tire with the tire that has the deepest tread and put both on the rear axle ({a('CS','USTMA')}).</li>
          <li><b>AWD and 4WD:</b> USTMA says even small differences in outside diameter may cause drivetrain damage, so follow the owner's manual ({a('CS','USTMA')}). More in <a href="/guides/mixing-tires/">mixing tires</a>.</li>
        </ul>
      </section>
      <section class="content-section" id="install">
        <h2>Step 5: at the shop</h2>
        <ul>
          <li><b>Pressure:</b> set to the placard, measured cold. NHTSA says the correct pressure is the vehicle maker's figure, not the number on the tire, and cold means not driven for at least three hours ({a('NT','NHTSA')}). See <a href="/guides/tire-pressure/">tire pressure</a>.</li>
          <li><b>Skip used tires:</b> Michelin says you cannot know what damage a previously owned tire has had ({a('MCS','Michelin')}).</li>
          <li><b>Do not count the spare:</b> NHTSA recommends that a full size spare not be used to replace worn tires except in emergencies such as a flat ({a('NT','NHTSA')}).</li>
          <li><b>Check the date code</b> on the new tires before they are mounted: <a href="/guides/dot-date-codes/">how to read the DOT date code</a>.</li>
        </ul>
      </section>
"""
crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Guides","item":BASE+"/guides/"},{"@type":"ListItem","position":3,"name":"How to choose replacement tires","item":URL}]
org = {"@type":"Organization","@id":BASE+"/#organization","name":"Smart Tire Picks"}
og = f"{BASE}/assets/img/og-{STEM}.jpg"
art = {"@context":"https://schema.org","@type":"Article","headline":H1,"description":DESC,"mainEntityOfPage":{"@type":"WebPage","@id":URL},"author":org,"publisher":org,"image":og,"datePublished":PUB,"dateModified":PUB,"inLanguage":"en-US","isPartOf":{"@type":"WebSite","@id":BASE+"/#website","name":"Smart Tire Picks"},"citation":[SRC[k][0] for k,_ in srcs]}
strip = lambda s: re.sub(r"<[^>]+>", "", s)
faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(x)}} for q,x in faqs]}
ld = lambda o: '  <script type="application/ld+json">\n' + json.dumps(o, indent=2, ensure_ascii=False) + '\n  </script>\n'
fq = "\n".join(f"        <details>\n          <summary>{esc(q)}</summary>\n          <p>{x}</p>\n        </details>" for q,x in faqs)
sl = "\n".join(f'          <li><a href="{SRC[k][0]}" rel="noopener noreferrer" target="_blank">{esc(SRC[k][1])}</a>: {esc(why)} ({READ})</li>' for k,why in srcs)
rl = "\n".join(f'          <li><a href="{h}">{esc(t)}</a></li>' for h,t in related)
out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(TITLE)}</title>
  <meta name="description" content="{esc(DESC)}">
  <link rel="canonical" href="{URL}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{esc(TITLE)}">
  <meta property="og:description" content="{esc(DESC)}">
  <meta property="og:url" content="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Smart Tire Picks">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og}">
  <meta property="og:image:alt" content="{esc(ALT)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(TITLE)}">
  <meta name="twitter:description" content="{esc(DESC)}">
  <meta name="twitter:image" content="{og}">
  <meta name="twitter:image:alt" content="{esc(ALT)}">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <link rel="stylesheet" href="/css/styles.css">
{ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumbs})}{ld(art)}{ld(faq)}<script src="/js/consent-analytics.js" defer></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5681559774142917" crossorigin="anonymous"></script></head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="/">Smart <span>Tire</span> Picks</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
{NAV}
      </nav>
    </div>
  </header>
  <main id="main">
    <div class="wrap">
      <p class="note"><a href="/">Home</a> › <a href="/guides/">Guides</a> › How to choose replacement tires</p>
      <h1 class="page-title">{esc(H1)}</h1>
<p class="lede">{LEDE}</p>
<p class="last-updated">Last updated: {PUB_H}</p>
<p class="byline">By Smart Tire Picks Editorial Team</p>
<figure class="page-photo" data-photo><img src="/assets/img/{STEM}-1024.webp" srcset="/assets/img/{STEM}-640.webp 640w, /assets/img/{STEM}-1024.webp 1024w" sizes="(max-width: 900px) 100vw, 900px" width="1024" height="576" alt="{esc(ALT)}" fetchpriority="high" decoding="async"><figcaption>AI generated image. Source: <a href="/image-policy/">Image policy</a>.</figcaption></figure>
{DISC}
{body}
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
    </div>
  </main>
{FOOT.rstrip()}
"""
p = ROOT / "guides" / SLUG / "index.html"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(out + "\n")
print(URL)
