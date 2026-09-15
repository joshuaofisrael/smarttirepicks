#!/usr/bin/env python3
"""Generate Smart Tire Picks static HTML pages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://smarttirepicks.com"
DATE_PUB = "2026-09-08"
DATE_MOD = "2026-09-15"

PER_PAGE = (
    '<aside class="disclaimer-box" role="note">'
    "<p><em>This page is for general information only and is not professional, safety, or legal advice. "
    "Always confirm tire size, load index, speed rating, and other specs against your vehicle’s door placard "
    "and owner’s manual, and have tires installed by a licensed professional. We have not lab-tested products "
    "unless explicitly stated. See our <a href=\"/disclaimer/\">Disclaimer</a> and "
    '<a href="/affiliate-disclosure/">Affiliate Disclosure</a>.</em></p>'
    "</aside>"
)

FOOTER_BLURB = (
    "Informational only — not professional or safety advice. Verify size, load index, speed rating, TPMS, "
    "and OEM specs on your door placard and in your owner’s manual before buying or installing. "
    "We do not perform lab safety tests unless a page says otherwise. Have tires mounted by a licensed installer. "
    '<a href="/disclaimer/">Disclaimer</a> · <a href="/affiliate-disclosure/">Affiliate Disclosure</a>'
)

NAV_ITEMS = [
    ("Fitment", "/fitment/choose-tire-size/"),
    ("Reviews", "/reviews/michelin-crossclimate2/"),
    ("Comparisons", "/comparisons/all-season-vs-winter/"),
    ("Guides", "/guides/placard/"),
    ("About", "/about.html"),
    ("Contact", "/contact/"),
]


def nav_html(current_path: str) -> str:
    items = []
    for label, href in NAV_ITEMS:
        # Mark current section loosely
        cur = ""
        if current_path.startswith("/fitment") and href.startswith("/fitment"):
            cur = ' aria-current="page"'
        elif current_path.startswith("/reviews") and href.startswith("/reviews"):
            cur = ' aria-current="page"'
        elif current_path.startswith("/comparisons") and href.startswith("/comparisons"):
            cur = ' aria-current="page"'
        elif current_path.startswith("/guides") and href.startswith("/guides"):
            cur = ' aria-current="page"'
        elif current_path.startswith("/contact") and href.startswith("/contact"):
            cur = ' aria-current="page"'
        elif current_path == href or (href.endswith(".html") and current_path.endswith(href)):
            cur = ' aria-current="page"'
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n          ".join(items)



def canonical_for(path: str) -> str:
    if path == "/index.html":
        return BASE + "/"
    if path.endswith("/index.html"):
        return BASE + path[: -len("index.html")]
    return BASE + path


def json_ld_script(objs: list) -> str:
    parts = []
    for obj in objs:
        payload = json.dumps(obj, ensure_ascii=False, indent=2)
        parts.append(f'<script type="application/ld+json">\n{payload}\n  </script>')
    return "\n  ".join(parts)


def schema_organization_website() -> list:
    return [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Smart Tire Picks",
            "url": BASE + "/",
            "description": "Educational tire fitment guides and editorial reviews for US drivers.",
            "parentOrganization": {
                "@type": "Organization",
                "name": "Joshua Israel Ventures LLC",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Smart Tire Picks",
            "url": BASE + "/",
            "description": "Learn tire fitment, door placards, load index, and category trade-offs.",
            "publisher": {"@type": "Organization", "name": "Smart Tire Picks"},
        },
    ]


def schema_article_breadcrumb(*, headline: str, description: str, canonical: str, breadcrumbs: list) -> list:
    crumb_items = []
    for i, (name, url) in enumerate(breadcrumbs, start=1):
        item_url = url if url.startswith("http") else BASE + url
        crumb_items.append({"@type": "ListItem", "position": i, "name": name, "item": item_url})
    return [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumb_items},
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": headline,
            "description": description,
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "author": {"@type": "Organization", "name": "Smart Tire Picks"},
            "publisher": {
                "@type": "Organization",
                "name": "Smart Tire Picks",
                "parentOrganization": {"@type": "Organization", "name": "Joshua Israel Ventures LLC"},
            },
            "datePublished": DATE_PUB,
            "dateModified": DATE_MOD,
        },
    ]


def schema_faq(faqs: list) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def related_block(items: list) -> str:
    lis = "\n".join(f'          <li><a href="{href}">{label}</a></li>' for href, label in items)
    return f"""
      <nav class="related-links" aria-label="Keep reading">
        <h2>Keep reading</h2>
        <ul>
{lis}
        </ul>
      </nav>"""


def sources_block(items: list) -> str:
    lis = "\n".join(
        f'          <li><a href="{url}" rel="noopener noreferrer" target="_blank">{title}</a> — {note}</li>'
        for url, title, note in items
    )
    return f"""
      <section class="sources-block" aria-labelledby="sources-heading">
        <h2 id="sources-heading">Sources</h2>
        <p class="note">Outbound links to public references. We paraphrase; visit the source for full wording and updates.</p>
        <ul>
{lis}
        </ul>
      </section>"""


def faq_html(faqs: list) -> str:
    parts = [
        '      <section class="faq-block" aria-labelledby="faq-heading">',
        '        <h2 id="faq-heading">FAQ</h2>',
    ]
    for q, a in faqs:
        parts.append("        <details>")
        parts.append(f"          <summary>{q}</summary>")
        parts.append(f"          <p>{a}</p>")
        parts.append("        </details>")
    parts.append("      </section>")
    return "\n".join(parts)


def page(
    *,
    path: str,
    title: str,
    description: str,
    body: str,
    include_disclaimer: bool = True,
    h1: str | None = None,
    lede: str | None = None,
    hero: bool = False,
    hero_html: str = "",
    schema_objs: list | None = None,
):
    canonical = canonical_for(path)

    head_extra = ""
    if schema_objs:
        head_extra = "\n  " + json_ld_script(schema_objs)
    disclaimer = PER_PAGE if include_disclaimer else ""
    title_block = ""
    if not hero:
        if h1:
            title_block += f"<h1 class=\"page-title\">{h1}</h1>\n"
        if lede:
            title_block += f'<p class="lede">{lede}</p>\n'

    main_inner = ""
    if hero:
        main_inner = hero_html + f'\n    <div class="wrap">\n      {disclaimer}\n      {body}\n    </div>'
    else:
        main_inner = (
            f'<div class="wrap">\n      {title_block}{disclaimer}\n      {body}\n    </div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Smart Tire Picks">
  <link rel="stylesheet" href="/css/styles.css">{head_extra}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="/">Smart <span>Tire</span> Picks</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Primary">
        <ul>
          {nav_html(path)}
        </ul>
      </nav>
    </div>
  </header>
  <main id="main">
    {main_inner}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-grid">
        <div>
          <h2>Smart Tire Picks</h2>
          <p>Educational tire fitment, guides, and editorial reviews for US drivers. Owned by Joshua Israel Ventures LLC.</p>
        </div>
        <div>
          <h2>Explore</h2>
          <ul>
            <li><a href="/fitment/choose-tire-size/">Fitment</a></li>
            <li><a href="/reviews/michelin-crossclimate2/">Reviews</a></li>
            <li><a href="/comparisons/all-season-vs-winter/">Comparisons</a></li>
            <li><a href="/guides/placard/">Guides</a></li>
          </ul>
        </div>
        <div>
          <h2>Company</h2>
          <ul>
            <li><a href="/about.html">About</a></li>
            <li><a href="/contact/">Contact</a></li>
            <li><a href="/disclaimer/">Disclaimer</a></li>
            <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-legal">
        <p>{FOOTER_BLURB}</p>
        <p class="footer-meta">&copy; 2026 Joshua Israel Ventures LLC. Brand names used for identification only.</p>
      </div>
    </div>
  </footer>
  <script src="/js/main.js" defer></script>
</body>
</html>
"""
    out = ROOT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))



NHTSA_TIRES = (
    "https://www.nhtsa.gov/vehicle-safety/tires",
    "NHTSA — Tires (TireWise)",
    "Public guidance on tire inflation, the Tire and Loading Information label/placard, maintenance, and UTQG consumer grades.",
)
NHTSA_SAVINGS = (
    "https://www.nhtsa.gov/tires/safety-and-savings-ride-your-tires",
    "NHTSA — Safety and savings ride on your tires",
    "Overview of why tire maintenance and labeling matter for everyday drivers.",
)
USTMA_REPLACE = (
    "https://www.ustires.org/tire-care-safety/replacing-tires",
    "USTMA — Replacing tires",
    "Industry consumer notes on matching size, load index, and speed rating when replacing tires.",
)
USTMA_CARE = (
    "https://www.ustires.org/tire-care-safety",
    "USTMA — Tire care & safety",
    "Trade-association hub for passenger/light-truck tire care topics for consumers.",
)

# ---------- PAGES ----------

page(
    path="/index.html",
    title="Smart Tire Picks — Tire Fitment Guides & Editorial Reviews",
    description="Learn how to choose tire size, read your door placard, and compare all-season vs winter tires. Educational guides from Smart Tire Picks.",
    include_disclaimer=True,
    hero=True,
    schema_objs=schema_organization_website(),
    hero_html="""
    <section class="hero">
      <div class="wrap">
        <p class="section-label" style="color:#a8e6df;">Educational tire site</p>
        <h1>Choose tires with clarity, not guesswork</h1>
        <p>Smart Tire Picks helps US drivers understand fitment, load and speed ratings, and category trade-offs — so you can verify the right size against your door placard before you buy.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/fitment/choose-tire-size/">Start with fitment</a>
          <a class="btn btn-ghost" href="/guides/placard/">Read your door placard</a>
        </div>
      </div>
    </section>
    """,
    body="""
      <p class="section-label">Popular starting points</p>
      <div class="card-grid">
        <article class="card">
          <h2>Choose the right tire size</h2>
          <p>Decode sidewall markings and match them to OEM specs without relying on marketing slogans.</p>
          <a class="card-link" href="/fitment/choose-tire-size/">Fitment guide →</a>
        </article>
        <article class="card">
          <h2>Tire placard checklist</h2>
          <p>A printable-style walkthrough of what to copy from your door label before you shop.</p>
          <a class="card-link" href="/guides/tire-placard-checklist/">Placard checklist →</a>
        </article>
        <article class="card">
          <h2>When to replace tires</h2>
          <p>Tread depth, age, damage, and other practical replacement signals explained plainly.</p>
          <a class="card-link" href="/guides/when-to-replace/">Replacement guide →</a>
        </article>
        <article class="card">
          <h2>How to check tread depth</h2>
          <p>Wear bars, gauges, and rough coin heuristics — with soft, educational caveats and when to see a pro.</p>
          <a class="card-link" href="/guides/tread-depth/">Tread depth guide →</a>
        </article>
        <article class="card">
          <h2>Editorial review: CrossClimate 2</h2>
          <p>Public manufacturer positioning summarized in soft language — no independent lab tests by us.</p>
          <a class="card-link" href="/reviews/michelin-crossclimate2/">Read review →</a>
        </article>
      </div>

      <div class="content-block" style="margin-top:1.5rem;">
        <h2>What we publish</h2>
        <p>Smart Tire Picks is an educational Flippa-style resource: fitment explainers, buying guides, editorial model overviews, and category comparisons. We prioritize clarity over hype.</p>
        <ul>
          <li><strong>Guides</strong> — placard reading, cold tire pressure / PSI, tread depth checks, load index &amp; speed rating, DOT date codes, replacement timing</li>
          <li><strong>Fitment</strong> — size selection and climate-category basics</li>
          <li><strong>Reviews &amp; comparisons</strong> — editorial summaries from public manufacturer positioning only</li>
        </ul>
        <p class="note">We do not claim any tire is the “safest” or guarantee outcomes for your vehicle. Always verify specs and use a licensed installer.</p>
      </div>

      <div class="cta-box">
        <h2>Retailer links</h2>
        <p>Affiliate purchase links are coming soon. Until then, check major tire retailers and confirm fitment with your installer.</p>
      </div>
    """,
)

page(
    path="/about.html",
    title="About Smart Tire Picks — Joshua Israel Ventures LLC",
    description="Learn about Smart Tire Picks, an educational tire fitment and review site operated by Joshua Israel Ventures LLC.",
    h1="About Smart Tire Picks",
    lede="An educational site focused on tire fitment literacy and calm, original editorial content for US drivers.",
    body="""
      <div class="content-block">
        <h2>Who we are</h2>
        <p><strong>Smart Tire Picks</strong> is owned and operated by <strong>Joshua Israel Ventures LLC</strong>. We publish guides, fitment explainers, comparisons, and editorial product overviews to help drivers ask better questions before buying tires.</p>
        <h2>What we are not</h2>
        <p>We are not a tire lab, installer network, or manufacturer. We do not perform independent instrumented testing unless a page explicitly says otherwise. Brand names appear for nominative identification only.</p>
        <h2>Editorial approach</h2>
        <ul>
          <li>Original US English copy — not scraped marketing pages</li>
          <li>Soft language; no “guaranteed safest” claims</li>
          <li>Clear prompts to verify door placard, OEM specs, load index, speed rating, and TPMS</li>
          <li>Licensed installer recommended for mounting and balancing</li>
        </ul>
        <h2>Contact</h2>
        <p>Questions or corrections? Visit our <a href="/contact/">contact page</a>.</p>
      </div>
    """,
)

# Contact FormSubmit lives at /contact/ (not generated here).

# GUIDES
PLACARD_FAQS = [
    (
        "Where is the tire information placard on most US vehicles?",
        "On many passenger vehicles it is on the driver’s door jamb (B-pillar area). Some models also list tire data in the owner’s manual. If labels differ, follow the vehicle manufacturer’s guidance and ask a qualified technician.",
    ),
    (
        "Should I inflate to the big PSI number on the tire sidewall?",
        "No. The sidewall figure is typically a maximum cold pressure for the tire’s construction. Use the vehicle placard (or OEM manual) recommended cold pressure unless a manufacturer service document says otherwise.",
    ),
    (
        "Can I change tire size from what the placard lists?",
        "Alternate sizes can affect load capacity, clearance, speedometer accuracy, and related systems. Confirm compatibility with OEM documentation and a licensed installer rather than relying only on an online picker.",
    ),
]

page(
    path="/guides/placard/index.html",
    title="How to Read Your Tire Door Placard — Smart Tire Picks",
    description="Find and read your vehicle’s tire information placard: size, pressure, load, and why OEM specs matter before you buy tires.",
    h1="How to read your tire door placard",
    lede="Your door-jamb placard is the primary reference for OEM tire size and cold inflation pressure — start here before shopping.",
    schema_objs=schema_article_breadcrumb(
        headline="How to read your tire door placard",
        description="Find and read your vehicle’s tire information placard: size, pressure, load, and why OEM specs matter before you buy tires.",
        canonical=canonical_for("/guides/placard/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("Door placard", "/guides/placard/"),
        ],
    )
    + [schema_faq(PLACARD_FAQS)],
    body="""
      <div class="content-block">
        <h2>Where to find it</h2>
        <p>On most passenger vehicles sold in the US, the tire information placard is on the driver’s door jamb (B-pillar area). Some vehicles also list tire data in the owner’s manual or fuel-filler area. If labels conflict, follow the vehicle manufacturer’s guidance and ask a qualified technician.</p>
        <h2>What the placard typically shows</h2>
        <ul>
          <li><strong>Original equipment tire size</strong> (for example, 225/65R17)</li>
          <li><strong>Cold inflation pressure</strong> for front and rear (and sometimes a spare)</li>
          <li>Occasionally notes about temporary spare limitations</li>
        </ul>
        <h2>Why pressure on the placard is not the sidewall max</h2>
        <p>The large PSI number molded on a tire sidewall is a maximum cold pressure for the tire’s construction — not the recommended operating pressure for your vehicle. Use the placard (or OEM manual) values unless a manufacturer service bulletin says otherwise.</p>
        <h2>Before you change sizes</h2>
        <p>Plus-sizing or alternate sizes can affect speedometer accuracy, load capacity, clearance, and driver-assistance calibration. Confirm compatibility with OEM documentation and a licensed installer — do not rely solely on an online size picker.</p>
        <p class="note">Also verify load index and speed rating meet or exceed OEM requirements for your trim and options package.</p>
      </div>
""" + faq_html(PLACARD_FAQS) + sources_block([NHTSA_TIRES, NHTSA_SAVINGS, USTMA_REPLACE]) + related_block([
    ("/guides/tire-placard-checklist/", "Tire placard checklist"),
    ("/guides/tire-pressure/", "Cold tire pressure / PSI"),
    ("/guides/load-index-speed-rating/", "Load index &amp; speed rating"),
    ("/fitment/choose-tire-size/", "How to choose tire size"),
]) + """
      <div class="cta-box">
        <h2>Next steps</h2>
        <p>Use the <a href="/guides/tire-placard-checklist/">placard checklist</a>, then confirm <a href="/guides/load-index-speed-rating/">load index &amp; speed rating</a>. Retailer links coming soon — check retailers and confirm with your installer.</p>
      </div>
    """,
)


CHECKLIST_FAQS = [
    (
        "What should I write down from the placard before shopping?",
        "At minimum: OEM tire size(s), recommended cold inflation pressures (front/rear/spare if listed), and any notes about temporary spares. Also record the load index and speed rating from a correctly fitted OEM tire or from OEM documentation.",
    ),
    (
        "Is the placard enough by itself?",
        "It is the usual starting point for size and pressure. Still cross-check your owner’s manual for trim-specific notes, and have a licensed installer confirm final fitment, TPMS needs, and mounting.",
    ),
]

page(
    path="/guides/tire-placard-checklist/index.html",
    title="Tire Placard Checklist — What to Copy Before You Buy | Smart Tire Picks",
    description="A practical checklist for recording OEM tire size, cold pressures, and related specs from your vehicle door placard before shopping.",
    h1="Tire placard checklist",
    lede="Copy the right details from your door label first — then shop. This checklist is educational, not a substitute for OEM docs or a licensed installer.",
    schema_objs=schema_article_breadcrumb(
        headline="Tire placard checklist",
        description="A practical checklist for recording OEM tire size, cold pressures, and related specs from your vehicle door placard before shopping.",
        canonical=canonical_for("/guides/tire-placard-checklist/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("Placard checklist", "/guides/tire-placard-checklist/"),
        ],
    )
    + [schema_faq(CHECKLIST_FAQS)],
    body="""
      <div class="content-block">
        <h2>Before you start</h2>
        <p>Park safely, open the driver’s door, and locate the Tire and Loading Information label (placard). Have a phone camera or notepad ready. Soft reminder: this list helps you organize facts — it does not approve a tire for your vehicle.</p>
        <h2>Checklist</h2>
        <ol>
          <li><strong>Vehicle identity</strong> — year, make, model, and trim (options packages can change OE tire specs).</li>
          <li><strong>OE tire size</strong> — copy the size string exactly (for example, 225/65R17). Note if front and rear differ.</li>
          <li><strong>Cold inflation pressure</strong> — record front and rear PSI/kPa from the placard, not the sidewall maximum.</li>
          <li><strong>Spare notes</strong> — temporary spares often have different size and pressure limits.</li>
          <li><strong>Load index &amp; speed rating</strong> — from a correct OE tire sidewall or OEM documentation; replacements should meet vehicle requirements.</li>
          <li><strong>Owner’s manual cross-check</strong> — look for trim-specific tire tables or warnings.</li>
          <li><strong>Installer questions</strong> — TPMS service, mounting/balancing, and whether any alternate size was previously fitted.</li>
        </ol>
        <h2>After you shop</h2>
        <p>Ask the seller for the DOT week/year on the set you will receive, and confirm the service description (load index/speed symbol) matches what you planned. Have a licensed professional mount and balance the tires.</p>
        <p class="note">We do not claim this checklist makes any tire choice “safe” for every vehicle. Verify against your placard, OEM materials, and installer guidance.</p>
      </div>
""" + faq_html(CHECKLIST_FAQS) + sources_block([NHTSA_TIRES, NHTSA_SAVINGS, USTMA_REPLACE]) + related_block([
    ("/guides/placard/", "How to read your door placard"),
    ("/guides/tire-pressure/", "Cold tire pressure / PSI"),
    ("/fitment/choose-tire-size/", "How to choose tire size"),
    ("/guides/load-index-speed-rating/", "Load index &amp; speed rating"),
]) + """
      <div class="cta-box">
        <h2>Related tools</h2>
        <p>Continue with <a href="/guides/placard/">placard reading</a> and <a href="/fitment/choose-tire-size/">size selection</a>. Retailer CTAs coming soon.</p>
      </div>
    """,
)


PRESSURE_FAQS = [
    (
        "Is the PSI on my tire sidewall the pressure I should use?",
        "Usually no. The large number molded on the sidewall is typically a maximum cold pressure for that tire’s construction. Your vehicle’s door placard (Tire and Loading Information label) or owner’s manual lists the recommended cold inflation pressures for that vehicle. Confirm with OEM materials and a licensed installer if anything is unclear.",
    ),
    (
        "How often should I check cold tire pressure?",
        "Many public safety resources encourage checking inflation regularly — for example monthly and before long trips — when tires are cold (before significant driving heats them). Exact habits can vary by vehicle and climate; follow your owner’s manual and ask a licensed installer if you are unsure how to measure accurately.",
    ),
    (
        "What does a TPMS warning light mean at a high level?",
        "A tire pressure monitoring system (TPMS) light generally indicates that the system detected a tire pressure condition outside its programmed threshold, or that the system itself needs service. It is a prompt to investigate safely — not a complete diagnosis. Check pressures with a quality gauge when cold if it is safe to do so, and have a licensed professional inspect the tires, valves, and sensors when needed.",
    ),
]

page(
    path="/guides/tire-pressure/index.html",
    title="Recommended Cold Tire Pressure (PSI) — Placard vs Sidewall | Smart Tire Picks",
    description="Learn how recommended cold tire pressure (PSI) differs from sidewall maximums, why the door placard matters, and how to check inflation with soft, educational guidance.",
    h1="Recommended cold tire pressure (PSI): placard vs sidewall",
    lede="Cold inflation pressure is vehicle-specific. Start with your door placard and owner’s manual — not the big number molded on the tire sidewall.",
    schema_objs=schema_article_breadcrumb(
        headline="Recommended cold tire pressure (PSI): placard vs sidewall",
        description="Learn how recommended cold tire pressure (PSI) differs from sidewall maximums, why the door placard matters, and how to check inflation with soft, educational guidance.",
        canonical=canonical_for("/guides/tire-pressure/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("Cold tire pressure", "/guides/tire-pressure/"),
        ],
    )
    + [schema_faq(PRESSURE_FAQS)],
    body="""
      <div class="content-block">
        <h2>What “cold” tire pressure means</h2>
        <p>Recommended inflation figures on US vehicles are typically stated as <strong>cold</strong> pressures — meaning the tire has not been warmed by recent driving or hot ambient conditions that raise pressure. Driving heats air inside the tire, so a reading taken after a long trip can look higher than a true cold reading. This page is educational only; it does not prescribe a universal PSI for every vehicle.</p>
        <h2>Use the placard (or OEM manual), not a one-size rule</h2>
        <p>Your vehicle’s Tire and Loading Information label (door-jamb placard) usually lists recommended cold inflation pressures for the front and rear (and sometimes a spare). Trims and options packages can differ, so also cross-check the owner’s manual. We do not publish a single “correct” PSI that applies to all cars, trucks, or SUVs.</p>
        <h2>Placard recommendation vs sidewall maximum</h2>
        <p>The large PSI number on a tire sidewall is commonly a <strong>maximum cold pressure</strong> for that tire’s construction — not the everyday operating pressure your vehicle was designed around. Inflating only to a sidewall maximum without OEM guidance can be inappropriate for ride, wear, and load context. Soft rule of thumb for shoppers: copy the placard first, then confirm with a licensed installer if the vehicle has been modified or if labels conflict.</p>
        <h2>Practical checking habits (not a safety guarantee)</h2>
        <ul>
          <li>Use a quality pressure gauge and compare each tire to the placard values for that axle (including the spare if your setup uses one).</li>
          <li>Check when tires are cold when practical — for example before a day’s first drive — and follow any timing notes in your owner’s manual.</li>
          <li>After adding or releasing air, re-check and reseat valve caps; ask an installer about TPMS service if sensors or valve stems need attention.</li>
          <li>Uneven wear, repeated underinflation warnings, or visible damage are reasons to stop and have a licensed professional inspect the set — this site cannot diagnose your vehicle remotely.</li>
        </ul>
        <h2>Load, temperature, and “set it and forget it”</h2>
        <p>Pressure changes with temperature, and load (passengers, cargo, towing) can matter for how a vehicle manufacturer frames inflation guidance. Some manuals include alternate tables for heavy load. Treat brochure shortcuts and forum “run X PSI” posts cautiously; verify against OEM materials for your exact vehicle.</p>
        <h2>Before you buy or remount tires</h2>
        <p>Record placard pressures alongside size, load index, and speed rating (see our <a href="/guides/tire-placard-checklist/">placard checklist</a>). Have a licensed installer mount and balance tires, confirm TPMS function, and advise if an alternate size changes any service considerations. We do not claim lab tests, and we do not label any inflation practice as the “safest” for every driver.</p>
        <p class="note">Informational only — not professional, safety, or legal advice. Always verify placard/OEM specs for your vehicle and use a licensed installer for mounting, balancing, and related service.</p>
      </div>
""" + faq_html(PRESSURE_FAQS) + sources_block([NHTSA_TIRES, NHTSA_SAVINGS, USTMA_CARE]) + related_block([
    ("/guides/placard/", "How to read your door placard"),
    ("/guides/tire-placard-checklist/", "Tire placard checklist"),
    ("/guides/tread-depth/", "How to check tread depth"),
    ("/fitment/choose-tire-size/", "How to choose tire size"),
]) + """
      <div class="cta-box">
        <h2>Next steps</h2>
        <p>Copy pressures with the <a href="/guides/tire-placard-checklist/">placard checklist</a>, then confirm size and ratings via <a href="/fitment/choose-tire-size/">choose tire size</a>. Retailer links coming soon — check retailers and confirm with your installer.</p>
      </div>
    """,
)

page(
    path="/guides/load-index-speed-rating/index.html",
    title="Tire Load Index & Speed Rating Explained — Smart Tire Picks",
    description="Understand tire load index and speed rating codes, why they matter for fitment, and how to verify them against OEM requirements.",
    h1="Load index and speed rating explained",
    lede="Those numbers and letters after the size code are not optional fine print — they describe capacity and rated capability.",
    schema_objs=schema_article_breadcrumb(
        headline="Load index and speed rating explained",
        description="Understand tire load index and speed rating codes, why they matter for fitment, and how to verify them against OEM requirements.",
        canonical=canonical_for("/guides/load-index-speed-rating/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("Load index & speed rating", "/guides/load-index-speed-rating/"),
        ],
    ),
    body="""
      <div class="content-block">
        <h2>Where they appear</h2>
        <p>On a typical sidewall service description you might see something like <strong>225/65R17 102H</strong>. Here, <strong>102</strong> is the load index and <strong>H</strong> is the speed rating symbol. Always confirm the exact marking on the tire you buy.</p>
        <h2>Load index (plain English)</h2>
        <p>Load index maps to a maximum load capacity per tire at a specified inflation condition defined by industry standards. A higher index generally means higher capacity — but you still must meet your vehicle’s requirements and set pressure correctly.</p>
        <ul>
          <li>Do not choose a lower load index than OEM specifies for your vehicle.</li>
          <li>Replacing only two tires? Match load capability and follow installer guidance on axle placement.</li>
          <li>Heavy vehicles, towing packages, and some EV trims may require XL / reinforced constructions — check OEM docs.</li>
        </ul>
        <h2>Speed rating (plain English)</h2>
        <p>Speed symbols (such as T, H, V, W) correspond to rated speeds under standardized conditions. They are not a license to drive at those speeds, and real-world limits include road law, tire condition, inflation, and vehicle capability.</p>
        <table>
          <thead><tr><th>Symbol (examples)</th><th>Editorial note</th></tr></thead>
          <tbody>
            <tr><td>S, T</td><td>Common on many touring / all-season passenger applications</td></tr>
            <tr><td>H, V</td><td>Often seen on higher-performance touring fitments</td></tr>
            <tr><td>W, Y</td><td>Typically associated with higher-rated performance tires</td></tr>
          </tbody>
        </table>
        <p>Mixing speed ratings across an axle is generally discouraged; follow OEM and installer guidance.</p>
        <h2>TPMS and electronics</h2>
        <p>Changing wheels or tire constructions can interact with tire-pressure monitoring and other systems. Plan sensor service with your installer.</p>
      </div>
""" + sources_block([USTMA_REPLACE, NHTSA_TIRES, USTMA_CARE]) + related_block([('/guides/placard/', 'Door placard guide'), ('/guides/tire-placard-checklist/', 'Placard checklist'), ('/fitment/choose-tire-size/', 'Choose tire size'), ('/reviews/michelin-crossclimate2/', 'Editorial review example')]) + """
      <div class="cta-box">
        <h2>Related reading</h2>
        <p><a href="/guides/placard/">Door placard guide</a> · <a href="/fitment/choose-tire-size/">Choose tire size</a>. Affiliate CTAs coming soon — check retailers.</p>
      </div>
    """,
)

page(
    path="/guides/dot-date-codes/index.html",
    title="Tire DOT Date Codes: How to Read Tire Age — Smart Tire Picks",
    description="Learn how to read the DOT tire date code (week and year of manufacture) and why tire age matters alongside tread depth.",
    h1="DOT date codes and tire age",
    lede="Tread depth is only one aging signal. The DOT code helps you identify when a tire was manufactured.",
    schema_objs=schema_article_breadcrumb(
        headline="DOT date codes and tire age",
        description="Learn how to read the DOT tire date code (week and year of manufacture) and why tire age matters alongside tread depth.",
        canonical=canonical_for("/guides/dot-date-codes/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("DOT date codes", "/guides/dot-date-codes/"),
        ],
    ),
    body="""
      <div class="content-block">
        <h2>What “DOT” means here</h2>
        <p>US-bound tires carry a Department of Transportation identification sequence. Toward the end of that sequence is a <strong>four-digit date code</strong> on tires made in recent decades: the first two digits are the week (01–52/53), the last two are the year.</p>
        <p>Example for illustration only: <strong>2424</strong> would indicate the 24th week of 2024. Always read the actual sidewall on the tire in front of you.</p>
        <h2>Why age matters</h2>
        <ul>
          <li>Rubber compounds change over time with heat, UV, ozone, and storage conditions</li>
          <li>A tire can look “new” in tread depth yet be older inventory</li>
          <li>Vehicle manufacturers and tire makers publish guidance on inspection and replacement intervals — follow those sources</li>
        </ul>
        <h2>Practical shopping tips</h2>
        <p>Ask the retailer for the date codes on the specific set you will receive. Prefer transparent sellers who will confirm week/year before mounting. Storage history also matters; a licensed installer can help inspect for cracking, flat-spotting, and other issues.</p>
        <p class="note">We do not set a universal “must replace by” age on this site. Use OEM guidance, tire-manufacturer guidance, and professional inspection.</p>
      </div>
""" + sources_block([NHTSA_TIRES, NHTSA_SAVINGS, USTMA_CARE]) + related_block([('/guides/when-to-replace/', 'When to replace tires'), ('/guides/tread-depth/', 'How to check tread depth'), ('/guides/tire-placard-checklist/', 'Placard checklist'), ('/fitment/choose-tire-size/', 'Choose tire size')]) + """
      <div class="cta-box">
        <h2>Also see</h2>
        <p><a href="/guides/when-to-replace/">When to replace tires</a>. Retailer links coming soon.</p>
      </div>
    """,
)

page(
    path="/guides/when-to-replace/index.html",
    title="When to Replace Tires: Tread, Age & Damage — Smart Tire Picks",
    description="Practical signs it may be time to replace tires: tread depth, uneven wear, damage, age, and seasonal considerations — verify with a pro.",
    h1="When to replace your tires",
    lede="Replacement timing depends on tread, damage, age, use case, and climate — not a single marketing slogan.",
    schema_objs=schema_article_breadcrumb(
        headline="When to replace your tires",
        description="Practical signs it may be time to replace tires: tread depth, uneven wear, damage, age, and seasonal considerations — verify with a pro.",
        canonical=canonical_for("/guides/when-to-replace/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("When to replace", "/guides/when-to-replace/"),
        ],
    ),
    body="""
      <div class="content-block">
        <h2>Tread depth</h2>
        <p>Many US consumer safety materials discuss remaining tread around <strong>2/32 inch</strong> as a point of elevated wet-traction risk, and tires include molded wear bars near that depth — but state rules and vehicle use can differ. Use a gauge; wear bars are a visual backup, not a complete inspection. See our dedicated <a href="/guides/tread-depth/">how to check tread depth</a> guide.</p>
        <h2>Damage and irregular wear</h2>
        <ul>
          <li>Sidewall bulges, cuts, or exposed cords — have a professional evaluate immediately</li>
          <li>Punctures outside repairable areas or prior improper repairs</li>
          <li>Cupping, feathering, or shoulder wear that suggests alignment, inflation, or suspension issues</li>
        </ul>
        <h2>Age and storage</h2>
        <p>Even with remaining tread, older tires may need retirement after inspection. See our <a href="/guides/dot-date-codes/">DOT date code guide</a>.</p>
        <h2>Seasonal sets</h2>
        <p>Drivers who run dedicated winter tires typically switch when temperatures and road conditions change. All-season tires are a compromise category — they are not identical to winter-rated tires. See <a href="/fitment/all-season-vs-winter-vs-summer/">all-season vs winter vs summer</a>.</p>
        <h2>What to do next</h2>
        <p>Document pressures, inspect visually, then have a licensed installer measure tread, check for damage, and confirm a replacement size that meets placard and OEM requirements (including load index and speed rating).</p>
      </div>
""" + sources_block([USTMA_REPLACE, NHTSA_TIRES, USTMA_CARE]) + related_block([('/guides/tread-depth/', 'How to check tread depth'), ('/guides/dot-date-codes/', 'DOT date codes'), ('/guides/tire-pressure/', 'Cold tire pressure / PSI'), ('/fitment/choose-tire-size/', 'Choose tire size')]) + """
      <div class="cta-box">
        <h2>Shopping note</h2>
        <p>Affiliate links coming soon — check major retailers and confirm mounting with a licensed installer.</p>
      </div>
    """,
)


TREAD_FAQS = [
    (
        "What are treadwear indicators (wear bars)?",
        "Most modern passenger tires have molded treadwear indicators — raised bars across the tread grooves. When the surrounding tread wears down so it is level with those bars, public safety materials commonly treat that as a signal that remaining depth is near a widely cited minimum (often discussed as about 2/32 inch / 1.6 mm). Wear bars are a visual cue, not a full inspection of every groove or of damage elsewhere on the tire.",
    ),
    (
        "Is 2/32 inch the legal minimum everywhere?",
        "Not necessarily as a single nationwide “law for every vehicle.” Many US consumer guidance materials and state inspection practices discuss about 2/32 inch remaining tread as a critical wet-traction risk threshold, and federal tire standards require wear indicators near that depth. Individual states and vehicle uses can differ. Treat 2/32 inch as an educational benchmark from public safety materials — verify local rules, OEM guidance, and have a licensed professional measure and advise for your set.",
    ),
    (
        "Are the penny and quarter tests accurate?",
        "Coin tests are rough, free heuristics — not calibrated measurements. A common penny-test description places Lincoln’s head upside down in a groove; if you can see the top of his head, tread may be near a widely discussed replacement threshold. Quarters are sometimes used as a more conservative heuristic. Prefer a dedicated tread-depth gauge across multiple locations on each tire, and ask a licensed installer to confirm readings, especially if wear looks uneven.",
    ),
    (
        "When should I see a licensed professional about tread?",
        "See a licensed tire installer or qualified shop if wear bars are exposed, a gauge shows low remaining depth, you notice uneven wear, cuts, bulges, vibrations, or repeated underinflation warnings, or before a long trip or seasonal change. This site cannot diagnose your vehicle remotely and does not replace professional inspection, mounting, or balancing.",
    ),
]

page(
    path="/guides/tread-depth/index.html",
    title="How to Check Tire Tread Depth — Wear Bars &amp; Gauges | Smart Tire Picks",
    description="Learn how to check tire tread depth with wear bars, a tread gauge, and rough coin heuristics. Educational NHTSA-cited guidance with soft caveats — verify with a licensed installer.",
    h1="How to check tire tread depth",
    lede="Tread depth affects wet-road grip. Learn what wear bars mean, how gauges and coin heuristics work, and when to have a licensed professional confirm your readings.",
    schema_objs=schema_article_breadcrumb(
        headline="How to check tire tread depth",
        description="Learn how to check tire tread depth with wear bars, a tread gauge, and rough coin heuristics. Educational NHTSA-cited guidance with soft caveats — verify with a licensed installer.",
        canonical=canonical_for("/guides/tread-depth/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Guides", "/guides/placard/"),
            ("Tread depth", "/guides/tread-depth/"),
        ],
    )
    + [schema_faq(TREAD_FAQS)],
    body="""
      <div class="content-block">
        <h2>Why tread depth matters (educational overview)</h2>
        <p>Tire tread helps channel water and maintain grip on wet or slippery roads. As grooves wear down, traction can decline — especially in rain. Public US safety materials (including NHTSA TireWise consumer guidance) discuss remaining tread around <strong>2/32 of an inch</strong> as a point where tires are widely described as unsafe to continue using and due for replacement. That figure is an educational benchmark from consumer safety materials, not a substitute for your state’s rules, your vehicle manufacturer’s guidance, or a hands-on inspection by a licensed installer.</p>
        <h2>Wear bars / treadwear indicators</h2>
        <p>Most passenger tires include molded <strong>treadwear indicators</strong> (often called wear bars) — raised sections spaced across the tread grooves. When the tread surface wears down so it is roughly even with those bars, remaining depth is near the depth those indicators were designed around (commonly discussed as about 2/32 inch / 1.6 mm). Soft practice: look across multiple grooves around each tire; one visible bar does not replace measuring other areas or checking for damage, cracking, or uneven wear.</p>
        <h2>Minimum tread concepts — phrase carefully</h2>
        <ul>
          <li>Many US consumer guides and inspection practices treat about <strong>2/32 inch</strong> remaining tread as a critical wet-traction risk threshold.</li>
          <li>Some drivers and regions prefer replacing earlier (for example nearer 4/32 inch) for wet or winter driving confidence — that is a judgment call to discuss with a licensed professional, not a universal rule we mandate here.</li>
          <li>We do not claim a single depth is “legal everywhere” or “safest for every vehicle.” Confirm local requirements and OEM recommendations.</li>
        </ul>
        <h2>How to measure (with caveats)</h2>
        <ol>
          <li><strong>Tread-depth gauge</strong> — The most practical DIY method. Insert the probe into the main grooves at several points across the tread and around the circumference. Record the lowest readings; uneven wear can matter as much as the average.</li>
          <li><strong>Wear-bar visual check</strong> — If tread is flush with the wear bars in places you can see, treat that as a strong prompt to measure carefully and book a professional inspection.</li>
          <li><strong>Penny / quarter heuristics</strong> — Rough, free checks only. A commonly cited penny test places Lincoln’s head upside down in a groove; if the top of his head is visible, public materials often say it is time to replace. A quarter (Washington’s head) is sometimes used as a more conservative heuristic. These are <em>not</em> calibrated instruments and can mislead on uneven wear or siped winter tires.</li>
        </ol>
        <p>Check monthly habits alongside cold pressure checks when practical, and inspect before long trips. This page does not diagnose your tires remotely.</p>
        <h2>When to see a licensed professional</h2>
        <p>Have a licensed tire installer measure tread, inspect for cuts, bulges, exposed cord, irregular wear, and advise on repair vs replacement. Also ask them to confirm inflation against your door placard, and to review age via the <a href="/guides/dot-date-codes/">DOT date code</a> if the set is older inventory. Mounting, balancing, and TPMS service belong with qualified shops — not DIY curb-side guesses.</p>
        <h2>How this ties to replacement timing</h2>
        <p>Tread depth is one replacement signal among several. Damage, age, storage history, and climate use also matter. Continue with our <a href="/guides/when-to-replace/">when to replace tires</a> overview after you understand how to measure depth.</p>
        <p class="note">Informational only — not professional, safety, or legal advice. We have not lab-tested your tires. Always verify OEM guidance and use a licensed installer for measurement confirmation, mounting, and related service.</p>
      </div>
""" + faq_html(TREAD_FAQS) + sources_block([NHTSA_TIRES, NHTSA_SAVINGS, USTMA_CARE, USTMA_REPLACE]) + related_block([
    ("/guides/when-to-replace/", "When to replace tires"),
    ("/guides/dot-date-codes/", "DOT date codes"),
    ("/guides/tire-pressure/", "Cold tire pressure / PSI"),
    ("/guides/tire-placard-checklist/", "Tire placard checklist"),
]) + """
      <div class="cta-box">
        <h2>Next steps</h2>
        <p>Measure tread, then review <a href="/guides/when-to-replace/">when to replace</a> and confirm cold pressures with the <a href="/guides/tire-placard-checklist/">placard checklist</a>. Retailer links coming soon — check retailers and confirm with your installer.</p>
      </div>
    """,
)

# FITMENT
page(
    path="/fitment/choose-tire-size/index.html",
    title="How to Choose the Right Tire Size — Smart Tire Picks",
    description="A step-by-step approach to choosing tire size: door placard first, then load index, speed rating, and installer confirmation.",
    h1="How to choose the right tire size",
    lede="Start with the vehicle — not the sale rack. Size, load, and speed rating must fit your OEM requirements.",
    schema_objs=schema_article_breadcrumb(
        headline="How to choose the right tire size",
        description="A step-by-step approach to choosing tire size: door placard first, then load index, speed rating, and installer confirmation.",
        canonical=canonical_for("/fitment/choose-tire-size/index.html"),
        breadcrumbs=[
            ("Home", "/"),
            ("Fitment", "/fitment/choose-tire-size/"),
            ("Choose tire size", "/fitment/choose-tire-size/"),
        ],
    ),
    body="""
      <div class="content-block">
        <h2>Step 1 — Read the placard</h2>
        <p>Locate the tire information placard and note the OEM size and cold pressures. Cross-check the owner’s manual for your trim. Details: <a href="/guides/placard/">placard guide</a> · <a href="/guides/tire-placard-checklist/">placard checklist</a>.</p>
        <h2>Step 2 — Decode the current sidewall</h2>
        <p>Compare what is on the car today with the placard. Previous owners may have installed a different size. Matching “what’s already on it” is not always correct.</p>
        <h2>Step 3 — Confirm load index and speed rating</h2>
        <p>Replacement tires should meet or exceed OEM load index and appropriate speed rating guidance for your vehicle. See <a href="/guides/load-index-speed-rating/">load &amp; speed explained</a>.</p>
        <h2>Step 4 — Decide category for your climate</h2>
        <p>All-season, winter, and summer tires serve different temperature and surface conditions. Category overview: <a href="/fitment/all-season-vs-winter-vs-summer/">compare categories</a>.</p>
        <h2>Step 5 — Plan install and TPMS</h2>
        <p>Budget for mounting, balancing, valve stems or TPMS service, and alignment checks when wear patterns suggest it. Improper install can create vibration or premature wear.</p>
        <h2>Optional plus-sizing</h2>
        <p>Larger wheels with lower-profile tires change ride, risk of wheel damage, and gearing feel. Treat plus-sizing as an engineering change — verify clearance, load capacity, and OEM guidance rather than copying a forum setup.</p>
      </div>
""" + sources_block([NHTSA_TIRES, USTMA_REPLACE, NHTSA_SAVINGS]) + related_block([('/guides/tire-placard-checklist/', 'Placard checklist'), ('/guides/tire-pressure/', 'Cold tire pressure / PSI'), ('/guides/load-index-speed-rating/', 'Load index &amp; speed rating'), ('/guides/placard/', 'Door placard guide')]) + """
      <div class="cta-box">
        <h2>Check retailers</h2>
        <p>Purchase CTAs coming soon. Until then, compare availability at major tire retailers and confirm final specs with your installer.</p>
      </div>
    """,
)

page(
    path="/fitment/all-season-vs-winter-vs-summer/index.html",
    title="All-Season vs Winter vs Summer Tires — Smart Tire Picks",
    description="Compare all-season, winter, and summer tire categories: climate fit, trade-offs, and what to verify before you buy.",
    h1="All-season vs winter vs summer tires",
    lede="Tire categories are about compound and tread design priorities — not marketing adjectives alone.",
    body="""
      <div class="content-block">
        <h2>All-season</h2>
        <p>Positioned for year-round use in many temperate US climates. Compounds and siping aim to balance dry, wet, and light winter performance. They remain a compromise: dedicated winter tires are typically designed for colder temperatures and snow/ice surfaces.</p>
        <h2>Winter (snow) tires</h2>
        <p>Winter tires use compounds that stay more flexible in cold weather and tread patterns intended for snow and ice. Many carry the three-peak mountain snowflake (3PMSF) symbol. They are not a substitute for careful driving, and local studded-tire rules vary.</p>
        <h2>Summer tires</h2>
        <p>Summer / performance-summer tires prioritize warm-weather grip and handling. In cold temperatures, compounds can harden and traction may fall off sharply — they are generally a poor choice for freezing climates or snow.</p>
        <h2>Quick comparison</h2>
        <table>
          <thead><tr><th>Category</th><th>Typical use case</th><th>Watch-outs</th></tr></thead>
          <tbody>
            <tr><td>All-season</td><td>Mild winters, convenience of one set</td><td>Not identical to winter tires in deep snow/ice</td></tr>
            <tr><td>Winter</td><td>Cold regions, frequent snow/ice</td><td>Swap seasonally; confirm storage and size</td></tr>
            <tr><td>Summer</td><td>Warm climates / performance focus</td><td>Avoid freezing temps; check speed/load ratings</td></tr>
          </tbody>
        </table>
        <p class="note">“All-weather” marketing is another label some manufacturers use — read the actual sidewall markings and manufacturer datasheets rather than the brochure headline.</p>
      </div>
      <div class="cta-box">
        <h2>Deeper comparison</h2>
        <p>See <a href="/comparisons/all-season-vs-winter/">all-season vs winter</a>. Retailer links coming soon.</p>
      </div>
    """,
)

# REVIEWS
page(
    path="/reviews/michelin-crossclimate2/index.html",
    title="Michelin CrossClimate 2 — Editorial Overview | Smart Tire Picks",
    description="Editorial overview of the Michelin CrossClimate 2 based on public manufacturer positioning. No independent lab test by Smart Tire Picks.",
    h1="Michelin CrossClimate 2 — editorial overview",
    lede="A nominative, educational summary of how Michelin publicly positions this model — not a lab test or safety ranking.",
    body="""
      <div class="content-block">
        <p><strong>Important:</strong> Smart Tire Picks has <em>not</em> performed independent laboratory, track, or instrumented testing of the CrossClimate 2. Comments below reflect publicly available manufacturer positioning and category context only. Brand names are used for identification.</p>
        <h2>Category context</h2>
        <p>Michelin markets the CrossClimate 2 in the grand-touring / all-weather-oriented space, emphasizing year-round capability and winter-oriented branding cues (including 3PMSF marking on applicable sizes — verify on the specific tire). Always confirm the exact size’s load index, speed rating, and sidewall marks for your vehicle.</p>
        <h2>What buyers typically evaluate</h2>
        <ul>
          <li>Whether an all-weather-oriented touring tire fits their climate better than a conventional all-season or a dual-set winter strategy</li>
          <li>Warranty mileage statements published by the manufacturer (read the current warranty booklet; terms change)</li>
          <li>Noise, wear, and wet-braking expectations relative to other touring options — which vary by vehicle, alignment, and driving style</li>
        </ul>
        <h2>Fitment checklist</h2>
        <ol>
          <li>Match size to door placard / OEM guidance</li>
          <li>Meet or exceed required load index and speed rating</li>
          <li>Confirm TPMS and install plan with a licensed installer</li>
          <li>Check DOT date codes on the set you receive</li>
        </ol>
        <h2>Soft takeaway</h2>
        <p>The CrossClimate 2 is frequently discussed as an option for drivers who want stronger cold-weather positioning than a basic all-season without running a dedicated winter set. That does not mean it is the right — or “safest” — choice for every vehicle or climate. Compare against your placard requirements and local conditions.</p>
      </div>
      <div class="cta-box">
        <h2>Where to buy</h2>
        <p>Affiliate links coming soon. Check major tire retailers for current sizing and pricing, then verify fitment with your installer.</p>
      </div>
    """,
)

page(
    path="/reviews/bridgestone-turanza-quiettrack/index.html",
    title="Bridgestone Turanza QuietTrack — Editorial Overview | Smart Tire Picks",
    description="Editorial overview of the Bridgestone Turanza QuietTrack from public manufacturer positioning. No independent lab test by us.",
    h1="Bridgestone Turanza QuietTrack — editorial overview",
    lede="Educational summary of public positioning for this touring all-season line — not an instrumented review.",
    body="""
      <div class="content-block">
        <p><strong>Important:</strong> We have <em>not</em> lab-tested the Turanza QuietTrack. This page paraphrases public manufacturer positioning and general touring-category expectations. Nominative brand use only.</p>
        <h2>Category context</h2>
        <p>Bridgestone presents the Turanza QuietTrack as a passenger touring all-season tire with emphasis on comfortable, quiet on-road manners and everyday wet/dry usability in typical US climates. Exact features, warranties, and available sizes should be confirmed on current manufacturer materials for your size.</p>
        <h2>What buyers typically evaluate</h2>
        <ul>
          <li>Cabin noise sensitivity on highway commutes</li>
          <li>Treadwear expectations versus performance-oriented all-seasons</li>
          <li>Whether winter traction needs call for a 3PMSF winter or all-weather product instead</li>
        </ul>
        <h2>Fitment checklist</h2>
        <ol>
          <li>Verify size, load index, and speed rating against the door placard</li>
          <li>Ask about alignment if prior tires wore unevenly</li>
          <li>Confirm TPMS service during mount/balance</li>
          <li>Inspect DOT week/year on delivery</li>
        </ol>
        <h2>Soft takeaway</h2>
        <p>QuietTrack is commonly considered in the comfort-focused touring all-season segment. Comfort priorities can trade against maximum warm-weather grip or dedicated winter performance. Choose based on verified specs and your climate — not headline adjectives.</p>
      </div>
      <div class="cta-box">
        <h2>Where to buy</h2>
        <p>Affiliate CTAs coming soon — check retailers and confirm with a licensed installer.</p>
      </div>
    """,
)

# COMPARISONS
page(
    path="/comparisons/all-season-vs-winter/index.html",
    title="All-Season vs Winter Tires Comparison — Smart Tire Picks",
    description="Compare all-season and winter tires: temperature, snow/ice priorities, cost of dual sets, and what to verify before switching.",
    h1="All-season vs winter tires",
    lede="A practical comparison for drivers deciding between one all-season set and a dedicated winter strategy.",
    body="""
      <div class="content-block">
        <h2>Core difference</h2>
        <p>All-season tires aim for acceptable performance across a wide range of conditions. Winter tires prioritize cold-temperature flexibility and snow/ice traction design. Neither category removes the need for appropriate speeds, pressures, and maintenance.</p>
        <h2>When all-seasons may be enough</h2>
        <ul>
          <li>Mild winters with rare ice and light snow</li>
          <li>Preference for a single mounted set and simpler logistics</li>
          <li>Vehicles that see mostly clear paved roads</li>
        </ul>
        <h2>When winter tires are often considered</h2>
        <ul>
          <li>Regular sub-freezing temperatures and packed snow or ice</li>
          <li>Hills, rural roads, or early/late season storms</li>
          <li>Willingness to store a second set and schedule seasonal swaps</li>
        </ul>
        <h2>Cost and logistics</h2>
        <p>A winter set adds tire (and sometimes wheel) cost plus storage and mount/balance cycles. Some drivers keep winters on dedicated wheels to simplify swaps and preserve TPMS sensors — discuss options with your installer.</p>
        <h2>Symbols and labels</h2>
        <p>Look for the three-peak mountain snowflake (3PMSF) on tires marketed for severe snow service. M+S alone is a mud-and-snow designation with a different meaning — read manufacturer explanations for your model.</p>
        <p class="note">Related: <a href="/fitment/all-season-vs-winter-vs-summer/">three-category overview</a>.</p>
      </div>
      <div class="cta-box">
        <h2>Next</h2>
        <p>Affiliate links coming soon. Check retailers for sizes that meet your placard requirements.</p>
      </div>
    """,
)

page(
    path="/comparisons/touring-vs-performance-all-season/index.html",
    title="Touring vs Performance All-Season Tires — Smart Tire Picks",
    description="Touring all-season vs performance all-season: ride comfort, handling priorities, wear expectations, and fitment checks.",
    h1="Touring vs performance all-season",
    lede="Both may be labeled “all-season,” but the design priorities — comfort versus sharper response — usually differ.",
    body="""
      <div class="content-block">
        <h2>Touring all-season</h2>
        <p>Typically oriented toward comfort, even wear, and everyday wet/dry manners. Often chosen for sedans, crossovers, and high-mileage commuting. Noise reduction and warranty mileage claims are common marketing themes — verify current manufacturer details per size.</p>
        <h2>Performance all-season</h2>
        <p>Usually prioritizes steering response and warm/dry grip closer to performance tires while retaining some all-season usability. Ride may feel firmer; tread life and cold-weather manners can differ from touring products.</p>
        <h2>Decision factors</h2>
        <table>
          <thead><tr><th>Factor</th><th>Touring lean</th><th>Performance lean</th></tr></thead>
          <tbody>
            <tr><td>Ride &amp; noise</td><td>Often prioritized</td><td>May trade comfort for response</td></tr>
            <tr><td>Handling feel</td><td>Adequate for daily driving</td><td>Sharper emphasis</td></tr>
            <tr><td>Winter capability</td><td>Varies widely by model</td><td>Still not a dedicated winter tire</td></tr>
            <tr><td>Wear</td><td>Often marketed for longevity</td><td>Can wear faster depending on compound/use</td></tr>
          </tbody>
        </table>
        <h2>Fitment reminder</h2>
        <p>Speed rating and load index still must satisfy OEM requirements. A “performance” label does not override placard specs or install quality.</p>
        <p class="note">Editorial examples on this site: <a href="/reviews/bridgestone-turanza-quiettrack/">Turanza QuietTrack</a> (touring comfort positioning) — not a lab ranking.</p>
      </div>
      <div class="cta-box">
        <h2>Check retailers</h2>
        <p>Coming soon: affiliate purchase placeholders. For now, compare current specs at major retailers with your installer.</p>
      </div>
    """,
)

# LEGAL
page(
    path="/disclaimer/index.html",
    title="Disclaimer — Smart Tire Picks",
    description="Informational-use disclaimer for Smart Tire Picks: verify placard and OEM specs; no lab tests unless stated; licensed installer recommended.",
    include_disclaimer=False,
    h1="Disclaimer",
    lede="Last updated: September 8, 2026",
    body="""
      <div class="content-block">
        <h2>Informational use only</h2>
        <p>Content on this website (including fitment notes, size charts, reviews, comparisons, and buying guides) is provided for <strong>general informational and educational purposes only</strong>. It is <strong>not</strong> professional advice of any kind — including automotive, safety, engineering, legal, or insurance advice — and it is <strong>not</strong> a substitute for the vehicle manufacturer’s specifications, a licensed tire technician, or a qualified mechanic.</p>
        <h2>You must verify before buying or installing</h2>
        <p>Before purchasing, mounting, or using any tire, <strong>you</strong> are solely responsible for confirming that the tire is correct and safe for <strong>your</strong> vehicle and use case. At a minimum, verify:</p>
        <ul>
          <li>Tire size, load index, and speed rating against your vehicle’s <strong>door-jamb placard</strong> and owner’s manual</li>
          <li>OEM and aftermarket wheel/tire compatibility (including offset, load capacity, and clearance)</li>
          <li>TPMS, ABS, and any driver-assistance system requirements or limitations</li>
          <li>Local laws and regulations (including winter/studded-tire rules where applicable)</li>
          <li>Tire age (DOT date code), condition, inflation pressure, and torque specs at install</li>
        </ul>
        <p><strong>Do not rely solely on this website</strong> when choosing tires. Specs published by manufacturers can change; always cross-check current manufacturer data and your vehicle documentation.</p>
        <h2>No lab tests, rankings, or safety guarantees</h2>
        <p>Unless a page <strong>explicitly</strong> states that we performed a named test under described conditions, we have <strong>not</strong> conducted laboratory, track, or instrumented safety testing. Phrases such as “best,” “top,” or “recommended” reflect editorial opinion and publicly available information only. We <strong>do not</strong> guarantee that any tire is the safest, most durable, or most appropriate choice for any driver, vehicle, road, or weather condition.</p>
        <h2>Installation</h2>
        <p>Tire mounting, balancing, and related service should be performed by a <strong>licensed, qualified tire installer</strong>. Improper installation, inflation, or maintenance can cause tire failure, loss of vehicle control, property damage, injury, or death.</p>
        <h2>Limitation of liability</h2>
        <p>To the fullest extent permitted by law, Joshua Israel Ventures LLC and its owners, operators, writers, and affiliates are <strong>not liable</strong> for any loss, damage, injury, claim, or cost arising from your use of this site or from any tire selection, purchase, installation, or use made in connection with information on this site — whether based on warranty, contract, tort (including negligence), or otherwise. Your use of this site is at your own risk.</p>
        <h2>No endorsement</h2>
        <p>Brand names and model names are used for identification and nominative reference only. Mentions of manufacturers or retailers do <strong>not</strong> imply affiliation, sponsorship, or endorsement unless clearly stated.</p>
        <h2>Affiliate relationships</h2>
        <p>Some links may be affiliate links. See our <a href="/affiliate-disclosure/">Affiliate Disclosure</a>. Commissions do not change our editorial standards, and they do not constitute a recommendation that a product is right for your vehicle.</p>
        <h2>Contact</h2>
        <p>Questions about this disclaimer: contact via the site’s <a href="/contact/">contact page</a> (Joshua Israel Ventures LLC).</p>
        <p>If you do not agree with these terms, do not use this website.</p>
      </div>
    """,
)

page(
    path="/affiliate-disclosure/index.html",
    title="Affiliate Disclosure — Smart Tire Picks",
    description="How Smart Tire Picks (Joshua Israel Ventures LLC) may earn affiliate commissions and how that relates to editorial content.",
    include_disclaimer=False,
    h1="Affiliate Disclosure",
    lede="Last updated: September 8, 2026",
    body="""
      <div class="content-block">
        <p>This website is owned and operated by <strong>Joshua Israel Ventures LLC</strong>.</p>
        <h2>How we may earn money</h2>
        <p>Some links on this site are <strong>affiliate links</strong>. If you click a link and purchase a product or service, we may earn a commission at <strong>no additional cost to you</strong>. We may also participate in display advertising or similar programs in the future.</p>
        <p>Affiliate partners may include online tire retailers and related networks (for example, programs associated with major tire retailers). Partner lists can change; when a specific page uses affiliate links, we aim to make that clear in context.</p>
        <h2>Editorial independence</h2>
        <p>Affiliate relationships do <strong>not</strong> mean a manufacturer or retailer endorses us, and they do <strong>not</strong> mean we endorse a product as safe or suitable for your vehicle. Commissions do not determine our conclusions. We may link to products we discuss critically or comparatively.</p>
        <h2>Your responsibility</h2>
        <p>Affiliate links do not change the responsibilities in our <a href="/disclaimer/">Disclaimer</a>. You must still verify fitment, load/speed ratings, OEM specs, and have tires installed by a licensed professional.</p>
        <h2>FTC note</h2>
        <p>This disclosure is provided in accordance with applicable guidance on endorsements and affiliate marketing (including FTC guidelines in the United States). We aim to be transparent whenever compensation may be involved.</p>
        <p class="note">Retailer CTAs on content pages are currently labeled coming soon / check retailers — no live affiliate URLs yet.</p>
      </div>
    """,
)


SITEMAP_URLS = [
    ("/", "weekly", "1.0"),
    ("/about.html", "monthly", "0.6"),
    ("/contact/", "monthly", "0.5"),
    ("/guides/placard/", "monthly", "0.8"),
    ("/guides/tire-placard-checklist/", "monthly", "0.8"),
    ("/guides/tire-pressure/", "monthly", "0.8"),
    ("/guides/load-index-speed-rating/", "monthly", "0.8"),
    ("/guides/dot-date-codes/", "monthly", "0.8"),
    ("/guides/when-to-replace/", "monthly", "0.8"),
    ("/guides/tread-depth/", "monthly", "0.8"),
    ("/fitment/choose-tire-size/", "monthly", "0.8"),
    ("/fitment/all-season-vs-winter-vs-summer/", "monthly", "0.8"),
    ("/reviews/michelin-crossclimate2/", "monthly", "0.7"),
    ("/reviews/bridgestone-turanza-quiettrack/", "monthly", "0.7"),
    ("/comparisons/all-season-vs-winter/", "monthly", "0.7"),
    ("/comparisons/touring-vs-performance-all-season/", "monthly", "0.7"),
    ("/disclaimer/", "yearly", "0.3"),
    ("/affiliate-disclosure/", "yearly", "0.3"),
]
_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for _loc, _freq, _pri in SITEMAP_URLS:
    _lines.append(f'  <url><loc>{BASE}{_loc}</loc><changefreq>{_freq}</changefreq><priority>{_pri}</priority></url>')
_lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(_lines) + "\n", encoding="utf-8")
print("wrote sitemap.xml")

print("HTML generation complete")
