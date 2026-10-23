#!/usr/bin/env python3
"""Idempotent audit fixes, 23 Oct 2026. Edits live HTML directly; does not use _generate.py."""
import re,glob,datetime,html
FILES=[f for f in glob.glob('**/*.html',recursive=True)]
MD={'index.html':('Educational tire fitment for US drivers: door placards, UTQG grades, cold PSI, load index, and plain English editorial reviews with public citations.'),
'guides/index.html':('Tire guides by task: door placard, cold PSI, TPMS, tread depth, DOT date codes, load index, UTQG, winter and mixed tires, and storage.'),
'terms/index.html':('Terms of Use for Smart Tire Picks, owned by Joshua Israel Ventures LLC: general information only, limitation of liability, Florida governing law.'),
'privacy/index.html':('Privacy Policy for Smart Tire Picks: what the contact form, Cloudflare Web Analytics and GitHub Pages hosting collect, and your choices.'),
'disclaimer/index.html':('Disclaimer for Smart Tire Picks, a brand of Joshua Israel Ventures LLC: general information only, accuracy limits, and affiliate and ad disclosure.'),
'comparisons/touring-vs-performance-all-season/index.html':('Touring vs performance all season tires: ride, handling, wear and winter limits, with a decision framework. Verify size against your door placard.')}
PLACARD={'guides/tire-pressure','guides/plus-sizing','guides/when-to-replace','guides/how-long-do-tires-last','guides/mixing-tires','fitment/choose-tire-size','tools/tire-size-calculator','guides/placard','guides/tire-placard-checklist','guides/spare-tire-limits','guides/tread-depth','guides/tpms'}
CALL=('<aside class="placard-callout" role="note"><p><strong>Check your tire placard and owner’s manual first.</strong> '
 'The door jamb placard and your owner’s manual give the size, load index, speed rating and cold inflation pressure set for your vehicle. '
 'If anything on this page differs, follow the vehicle maker, and not this site.</p></aside>\n')
FOOT_OLD='Smart Tire Picks is owned and operated by Joshua Israel Ventures LLC.</p>'
FOOT_NEW=('Smart Tire Picks is owned and operated by Joshua Israel Ventures LLC, a Florida limited liability company. '
 'Our <a href="/terms/">Terms of Use</a> are governed by Florida law, and disputes go to the state or federal courts located in Florida unless the law where you live requires otherwise.</p>')
METHOD=('<p class="method-note"><strong>Method:</strong> this is an editorial overview based on public manufacturer information and general category context. '
 'We have not performed laboratory, track or instrumented testing, and this page is not professional advice.</p>\n')
n=0
for f in FILES:
    s=o=open(f).read()
    key=f
    d=MD.get(key)
    if d:
        s=re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*(")',lambda m:m.group(1)+html.escape(d,quote=True)+m.group(2),s)
        s=re.sub(r'("description": ")[^"]*(")',lambda m:m.group(1)+d+m.group(2),s,count=1) if key!='index.html' else s
    if key=='guides/index.html':
        s=s.replace('Tire Guides: Placard, PSI, TPMS, Tread, Age & Ratings | Smart Tire Picks','Tire Guides: Placard, PSI, TPMS, Tread & Ratings | Smart Tire Picks')
    if 'twitter:card' not in s and '<meta property="og:title"' in s:
        s=s.replace('<meta property="og:title"','<meta name="twitter:card" content="summary_large_image">\n  <meta property="og:title"',1)
    if FOOT_OLD in s and 'a Florida limited liability company' not in s:
        s=s.replace(FOOT_OLD,FOOT_NEW)
    m=re.search(r'"dateModified": ?"(\d{4})-(\d\d)-(\d\d)"',s)
    if m and 'class="last-updated"' not in s:
        dt=datetime.date(int(m[1]),int(m[2]),int(m[3])).strftime('%B %-d, %Y')
        line=f'<p class="last-updated">Last updated: {dt}</p>\n'
        # after lede paragraph following h1
        s2=re.sub(r'(<h1 class="page-title">.*?</h1>\s*<p class="lede">.*?</p>\n?)',lambda mm:mm.group(1)+('\n' if not mm.group(1).endswith('\n') else '')+line,s,count=1,flags=re.S)
        if s2==s: print('no lede',f)
        s=s2
    dirkey=f[:-len('/index.html')] if f.endswith('/index.html') else f
    if dirkey in PLACARD and 'placard-callout' not in s:
        s=re.sub(r'(<aside class="disclaimer-box".*?</aside>\n?)',lambda mm:mm.group(1)+('\n' if not mm.group(1).endswith('\n') else '')+CALL,s,count=1,flags=re.S)
    if f.startswith('reviews/') and 'method-note' not in s:
        s=re.sub(r'(<p class="last-updated">.*?</p>\n)',lambda mm:mm.group(1)+METHOD,s,count=1)
    if s!=o: open(f,'w').write(s); n+=1; print('edited',f)
css=open('css/styles.css').read()
if 'placard-callout' not in css:
    css+='''
.placard-callout{margin:1rem 0;padding:.9rem 1.1rem;border-left:5px solid #b45309;background:#fff7e6;border-radius:6px;color:#3b2a00;font-size:1rem}
.placard-callout p{margin:0}
.last-updated{margin:.25rem 0 1rem;font-size:.9rem;color:#555}
.method-note{margin:0 0 1rem;font-size:.95rem;color:#333}
'''
    open('css/styles.css','w').write(css)
print('files',n)
