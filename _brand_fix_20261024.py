#!/usr/bin/env python3
"""24 Oct 2026: LLC/owner name only on legal pages. Re-runnable."""
import re, pathlib
L='Joshua Israel Ventures LLC'
LEGAL={'terms','disclaimer','privacy','affiliate-disclosure'}
NEUTRAL='<p class="footer-owner">&copy; 2026 Smart Tire Picks. All rights reserved.</p>'
_OLD='<p class="footer-owner">&copy; 2026 Smart Tire Picks. All rights reserved. <a href="/terms/">Terms of Use</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/disclaimer/">Disclaimer</a> · <a href="/affiliate-disclosure/">Affiliate Disclosure</a> · <a href="/contact/">Contact</a></p>'
changed=[]
for p in pathlib.Path('.').rglob('*.html'):
    if '.git' in p.parts: continue
    s=o=p.read_text()
    legal=p.parts[0] in LEGAL
    s=re.sub(r'<p class="footer-owner">.*?</p>',NEUTRAL,s,flags=re.S)
    s=re.sub(r'\s*<p class="footer-meta">Operated by .*?</p>','',s,flags=re.S)
    s=s.replace(' Owned by '+L+'.','')
    # head metadata on every page
    head,sep,body=s.partition('</head>')
    head=head.replace(' ('+L+')','').replace(' — '+L,'').replace(' — '+L,'')
    head=head.replace(', owned by '+L,'').replace(', a brand of '+L,'')
    head=head.replace('Contact '+L+' about Smart Tire Picks','Contact Smart Tire Picks')
    head=head.replace('operated by '+L,'operated as Smart Tire Picks')
    head=re.sub(r'\s*"legalName": "'+L+'",','',head)
    head=head.replace('"description": "'+L+' owns and operates Smart Tire Picks, an','"description": "Smart Tire Picks is an')
    head=head.replace('"name": "'+L+'"','"name": "Smart Tire Picks"')
    if not legal: head=re.sub(r'\s*"email": "joshuaofisrael@gmail.com",','',head)
    s=head+sep+body
    if not legal:
        s=s.replace('<p><strong>Smart Tire Picks is a brand of '+L+'.</strong> It is a brand name only, not a separate company, and all business connected with this site is done by '+L+'.</p>\n','')
        s=s.replace('<strong>Smart Tire Picks</strong> is owned and operated by <strong>'+L+'</strong>. We','<strong>Smart Tire Picks</strong> is an independent tire information site. We')
        s=s.replace('Send a message to '+L+' about Smart Tire Picks.','Send a message to Smart Tire Picks.')
        s=re.sub(r'\s*<p>&copy; 2026 '+L+r'.*?</p>','',s,flags=re.S)
    s=s.replace(' or email <a href="mailto:joshuaofisrael@gmail.com">joshuaofisrael@gmail.com</a>.</p>','.</p>') if not legal else s
    if s!=o: p.write_text(s); changed.append(str(p))
t=pathlib.Path('llms.txt'); s=t.read_text()
s=re.sub(r'^Operated by '+L+r'\..*?done by '+L+r'\. ?','',s,flags=re.M)
s=s.replace('Smart Tire Picks is a brand of '+L+'; who','who')
t.write_text(s)
print(len(changed)); print('\n'.join(sorted(changed)))
