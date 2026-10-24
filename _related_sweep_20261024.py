#!/usr/bin/env python3
"""24 Oct 2026: internal link sweep. Adds topical cluster links to each guide's Keep reading list. Re-runnable."""
import re, pathlib
L={'dot-date-codes':'Read the DOT date code','how-long-do-tires-last':'How long tires last','load-index-speed-rating':'Load index and speed rating chart',
'mixing-tires':'Can you mix tires','nitrogen-vs-air':'Nitrogen vs air','placard':'How to read the door placard','plus-sizing':'Plus sizing tires',
'seasonal-tire-storage':'Seasonal tire storage','sidewall-bulge':'Sidewall bulge or dent','spare-tire-limits':'Spare tire limits',
'tire-placard-checklist':'Placard checklist','tire-plug-vs-patch':'Plug vs patch repairs','tire-pressure':'What PSI your tires need',
'tire-rotation':'Tire rotation patterns','tpms':'TPMS light meanings','tread-depth':'Tread depth chart and penny test','utqg':'UTQG ratings explained',
'when-to-replace':'When to replace tires','winter-tires':'Winter tires guide'}
EXTRA={'/tools/tire-size-calculator/':'Tire size calculator','/comparisons/all-season-vs-winter/':'All season vs winter tires'}
M={'dot-date-codes':['how-long-do-tires-last','sidewall-bulge'],
'plus-sizing':['load-index-speed-rating','utqg','mixing-tires','tire-pressure','/tools/tire-size-calculator/'],
'tire-placard-checklist':['placard','load-index-speed-rating','plus-sizing','tire-pressure'],
'load-index-speed-rating':['plus-sizing','placard','utqg','mixing-tires'],
'nitrogen-vs-air':['tire-pressure','tpms','placard','spare-tire-limits'],
'placard':['tire-pressure','load-index-speed-rating','plus-sizing','tire-placard-checklist'],
'utqg':['how-long-do-tires-last','load-index-speed-rating','plus-sizing','tread-depth'],
'mixing-tires':['tire-rotation','plus-sizing','tread-depth','load-index-speed-rating'],
'tire-rotation':['mixing-tires','tread-depth','how-long-do-tires-last','tire-pressure'],
'tread-depth':['when-to-replace','how-long-do-tires-last','winter-tires','sidewall-bulge'],
'seasonal-tire-storage':['winter-tires','dot-date-codes','tire-pressure','/comparisons/all-season-vs-winter/'],
'spare-tire-limits':['tire-plug-vs-patch','sidewall-bulge','tpms','tire-pressure'],
'winter-tires':['seasonal-tire-storage','tire-pressure','tread-depth','/comparisons/all-season-vs-winter/'],
'sidewall-bulge':['tire-plug-vs-patch','when-to-replace','spare-tire-limits'],
'tire-plug-vs-patch':['sidewall-bulge','spare-tire-limits','tpms'],
'tire-pressure':['nitrogen-vs-air','tpms','winter-tires'],
'tpms':['nitrogen-vs-air','tire-pressure','spare-tire-limits'],
'when-to-replace':['sidewall-bulge','dot-date-codes','tread-depth'],
'how-long-do-tires-last':['utqg','tire-rotation','dot-date-codes']}
changed=[]
for slug,targets in M.items():
    p=pathlib.Path('guides')/slug/'index.html'; s=o=p.read_text()
    add=[]
    for t in targets:
        href=t if t.startswith('/') else f'/guides/{t}/'
        lab=EXTRA.get(t) or L[t]
        if f'href="{href}"' in s: continue
        add.append(f'          <li><a href="{href}">{lab}</a></li>')
    if not add: continue
    m=re.search(r'(<nav class="related-links"[^>]*>\s*<h2>[^<]*</h2>\s*<ul>.*?)(\s*</ul>)',s,re.S)
    if m:
        s=s[:m.end(1)]+'\n'+'\n'.join(add)+s[m.end(1):]
    else:
        nav='      <nav class="related-links" aria-label="Keep reading">\n        <h2>Keep reading</h2>\n        <ul>\n'+'\n'.join(add)+'\n        </ul>\n      </nav>\n'
        i=s.find('<div class="cta-box">'); i=i if i>0 else s.find('</main>')
        s=s[:i]+nav+'      '+s[i:]
    if s!=o: p.write_text(s); changed.append(str(p))
print('\n'.join(changed))
