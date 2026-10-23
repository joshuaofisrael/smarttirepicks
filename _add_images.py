#!/usr/bin/env python3
"""Idempotent post-build step: adds AI generated, subject related photos (WebP, srcset) to pages,
sets og:image / twitter:image to a 1200x675 JPG for those pages, and adds image entries to sitemap.xml.
Run after editing HTML: python3 _add_images.py
Images in assets/img/ are hyper-realistic generated photos with no people, no readable text, no brand logos."""
import re, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BASE = "https://smarttirepicks.com"
CAP = "Illustrative AI generated photo."
IMG = {
 "home-hero": "Close up of a new passenger car tire tread covered in rain drops on wet asphalt",
 "guides-hub": "Tidy home garage with a stack of four tires and a floor jack beside a hatchback",
 "tire-pressure": "Digital tire pressure gauge connected to the valve stem of a car wheel",
 "tread-depth": "Metal tread depth gauge probe measuring a main groove of a car tire",
 "winter-tires": "Car winter tire with packed snow in the tread on a snowy road",
 "review-allseason": "All season tire and alloy wheel of a crossover SUV on a wet country road",
 "review-touring": "Touring tire and silver alloy wheel on a sedan parked on a suburban street at sunset",
 "fitment-wheel": "Front wheel removed from a car on a lift in a workshop showing the brake rotor and caliper",
}
# page path -> (image key, page specific alt)
PAGES = {
 "/guides/index.html": ("guides-hub", IMG["guides-hub"]),
 "/guides/tire-pressure/index.html": ("tire-pressure", IMG["tire-pressure"]),
 "/guides/tpms/index.html": ("tire-pressure", "Tire pressure gauge on a wheel, the manual check that backs up a TPMS warning light"),
 "/guides/nitrogen-vs-air/index.html": ("tire-pressure", "Digital tire pressure gauge on a valve stem for checking air or nitrogen fill"),
 "/guides/tread-depth/index.html": ("tread-depth", IMG["tread-depth"]),
 "/guides/when-to-replace/index.html": ("home-hero", "Tire tread with water droplets, the kind of tread worth checking before replacement"),
 "/guides/winter-tires/index.html": ("winter-tires", IMG["winter-tires"]),
 "/guides/tire-rotation/index.html": ("fitment-wheel", IMG["fitment-wheel"]),
 "/guides/seasonal-tire-storage/index.html": ("guides-hub", "Stack of tires stored in a garage next to a floor jack"),
 "/reviews/michelin-crossclimate2/index.html": ("review-allseason", IMG["review-allseason"]),
 "/reviews/bridgestone-turanza-quiettrack/index.html": ("review-touring", IMG["review-touring"]),
 "/fitment/choose-tire-size/index.html": ("review-touring", "Sedan front tire and alloy wheel viewed from the side, the sidewall where size markings are molded"),
 "/fitment/all-season-vs-winter-vs-summer/index.html": ("winter-tires", IMG["winter-tires"]),
 "/comparisons/all-season-vs-winter/index.html": ("winter-tires", IMG["winter-tires"]),
 "/comparisons/touring-vs-performance-all-season/index.html": ("review-allseason", IMG["review-allseason"]),
}
HOME = "/index.html"
CARDS = {  # home card href -> image key
 "/fitment/choose-tire-size/": "fitment-wheel", "/guides/when-to-replace/": "home-hero",
 "/guides/tread-depth/": "tread-depth", "/guides/tpms/": "tire-pressure",
 "/guides/seasonal-tire-storage/": "guides-hub", "/reviews/michelin-crossclimate2/": "review-allseason",
 "/comparisons/touring-vs-performance-all-season/": "review-touring",
}
def tag(key, alt, cls, eager, sizes):
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img{cls} src="/assets/img/{key}-1024.webp" srcset="/assets/img/{key}-640.webp 640w, /assets/img/{key}-1024.webp 1024w" '
            f'sizes="{sizes}" width="1024" height="576" alt="{alt}" {load}>')
def set_og(h, key, alt):
    u = f"{BASE}/assets/img/og-{key}.jpg"
    h = re.sub(r'(<meta property="og:image" content=")[^"]*"', rf'\g<1>{u}"', h)
    h = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', rf'\g<1>{u}"', h)
    h = re.sub(r'(<meta property="og:image:width" content=")\d+"', r'\g<1>1200"', h)
    h = re.sub(r'(<meta property="og:image:height" content=")\d+"', r'\g<1>675"', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', rf'\g<1>{alt}"', h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*"', rf'\g<1>{alt}"', h)
    return h
changed = {}
for p, (key, alt) in PAGES.items():
    f = ROOT / p.lstrip("/"); h = f.read_text(encoding="utf-8")
    if "data-photo" in h: continue
    fig = (f'<figure class="page-photo" data-photo>{tag(key, alt, "", True, "(max-width: 900px) 100vw, 900px")}'
           f'<figcaption>{CAP}</figcaption></figure>')
    n, c = re.subn(r'(<p class="lede">.*?</p>\n?)', lambda m: m.group(1) + fig + "\n", h, count=1, flags=re.S)
    if not c:
        n, c = re.subn(r'(<h1 class="page-title">.*?</h1>\n?)', lambda m: m.group(1) + fig + "\n", h, count=1, flags=re.S)
    if not c: print("NO ANCHOR", p); continue
    f.write_text(set_og(n, key, alt), encoding="utf-8"); changed[p] = (key, alt)
# home
f = ROOT / "index.html"; h = f.read_text(encoding="utf-8")
if "data-photo" not in h:
    alt = IMG["home-hero"]
    h = h.replace('<section class="hero">', '<section class="hero hero-photo" data-photo>\n      ' + tag("home-hero", alt, ' class="hero-bg"', True, "100vw"), 1)
    for href, key in CARDS.items():
        pat = re.compile(r'(<article class="card">)(\s*<h2>[^<]*</h2>\s*<p>[^<]*</p>\s*<a class="card-link" href="' + re.escape(href) + '")')
        im = tag(key, IMG[key], ' class="card-img"', False, "(max-width: 600px) 100vw, 350px")
        h, c = pat.subn(lambda m: m.group(1) + "\n          " + im + m.group(2), h, count=1)
        if not c: print("NO CARD", href)
    h = set_og(h, "home-hero", IMG["home-hero"])
    f.write_text(h, encoding="utf-8"); changed[HOME] = ("home-hero", IMG["home-hero"])
# sitemap
sm = ROOT / "sitemap.xml"; s = sm.read_text(encoding="utf-8")
if "xmlns:image" not in s:
    s = s.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
today = datetime.date.today().isoformat()
for p, (key, alt) in changed.items():
    loc = BASE + ("/" if p == HOME else p.replace("index.html", ""))
    imgs = f'<image:image><image:loc>{BASE}/assets/img/{key}-1024.webp</image:loc><image:caption>{alt}</image:caption></image:image>'
    m = re.search(r'(<url><loc>' + re.escape(loc) + r'</loc><lastmod>)[^<]*(</lastmod>.*?)(</url>)', s)
    if m and "image:image" not in m.group(0):
        s = s.replace(m.group(0), m.group(1) + today + m.group(2) + imgs + m.group(3))
sm.write_text(s, encoding="utf-8")
print("changed", len(changed), "pages")
