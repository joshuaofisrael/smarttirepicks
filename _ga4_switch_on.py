#!/usr/bin/env python3
"""Re-runnable: python3 _ga4_switch_on.py G-XXXXXXXXXX  -> sets GA_ID, adds consent loader to every page, inserts privacy section."""
import re, sys
from pathlib import Path
R = Path(__file__).resolve().parent; gid = sys.argv[1]
assert re.fullmatch(r"G-[A-Z0-9]{6,12}", gid), "need a real G- measurement ID"
js = R / "js/consent-analytics.js"; js.write_text(re.sub(r'var GA_ID = "[^"]*";', f'var GA_ID = "{gid}";', js.read_text()))
tag = '<script src="/js/consent-analytics.js" defer></script>'
for p in R.rglob("*.html"):
    if ".git" in p.parts or "_drafts" in p.parts: continue
    s = p.read_text()
    if tag not in s and "</head>" in s: p.write_text(s.replace("</head>", tag + "\n</head>", 1))
pv = R / "privacy/index.html"; s = pv.read_text()
if 'id="google-analytics"' not in s:
    sec = re.sub(r"<!--.*?-->\s*", "", (R / "_drafts/privacy-google-analytics-section.html").read_text(), flags=re.S)
    m = re.search(r"<h2[^>]*>\s*Information you give us", s) or re.search(r"</main>", s)
    s = s[:m.start()] + sec + "\n" + s[m.start():]
    pv.write_text(s)
print("GA4 switched on with", gid, "(update privacy Last updated date, review, then publish.sh)")
