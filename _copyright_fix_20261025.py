import pathlib
OLD='        <p class="footer-owner">&copy; 2026 Smart Tire Picks. All rights reserved.</p>\n'
S='© 2026 Joshua Israel Ventures LLC. All rights reserved. Smart Tire Picks is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company.'
LEGAL={'terms','privacy','disclaimer','affiliate-disclosure'}
for p in pathlib.Path('.').rglob('*.html'):
    t=p.read_text(); o=t
    t=t.replace(OLD,'')
    if p.parts[0] in LEGAL and S not in t:
        t=t.replace('</main>','<p class="legal-copyright">'+S+'</p>\n</main>',1)
    if t!=o: p.write_text(t); print(p)
