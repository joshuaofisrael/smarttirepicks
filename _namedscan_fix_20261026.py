import re,glob,json,html
faq=[
("What is Smart Tire Picks?","Smart Tire Picks is a free educational site for US drivers. We publish tire fitment guides, buying guides, editorial model overviews and category comparisons, plus browser based tools such as a tire size calculator and a DOT date code decoder."),
("Do you road test or lab test tires?","No. We do not run our own road or lab tests. Our reviews and comparisons summarize public manufacturer information and published industry guidance, and each page says so. Always confirm specs with the tire maker and a licensed installer."),
("Where do I find the right tire size and pressure for my car?","Use the tire and loading information placard, usually on the driver side door jamb, and your owner's manual. The pressure on the placard is the recommended cold pressure for your vehicle. The number molded on the tire sidewall is the tire's maximum pressure, not the pressure to run."),
("How can I tell how old a tire is?","Look for the DOT code on the sidewall. The last four digits are the week and year of manufacture, so 2324 means the 23rd week of 2024. Our DOT date code tool decodes it for you in your browser."),
("When should I replace a tire for tread wear?","Tires have molded tread wear indicator bars at about 2/32 inch. When the tread is level with those bars, it is time to replace the tire. Many drivers replace sooner, around 4/32 inch, for better wet and snow traction. Bulges, cuts or other damage are also reasons to have a tire inspected right away."),
("Do your tools collect my data?","No. Our calculators run entirely in your browser. Nothing you type is sent to us or stored, and you do not need an account."),
("Do you get paid by tire brands?","No. Brands do not pay for coverage and cannot buy a positive verdict. The site carries no affiliate links right now; if that changes, our Affiliate Disclosure will explain how it works."),
]
links={"DOT date code tool":'<a href="/tools/dot-date-code/">DOT date code tool</a>',"Affiliate Disclosure":'<a href="/affiliate-disclosure/">Affiliate Disclosure</a>',"tire size calculator":'<a href="/tools/tire-size-calculator/">tire size calculator</a>'}
s=open('index.html').read()
assert 'FAQPage' not in s
items=""
for q,a in faq:
    h=html.escape(a,quote=False)
    for k,v in links.items(): h=h.replace(k,v,1)
    items+=f'        <details>\n          <summary>{html.escape(q,quote=False)}</summary>\n          <p>{h}</p>\n        </details>\n'
block=f'      <section class="faq-block" aria-labelledby="faq-heading" style="margin-top:1.5rem;">\n        <h2 id="faq-heading">Frequently asked questions</h2>\n{items}      </section>\n\n'
anchor='      <div class="cta-box retailer-cta">'
assert s.count(anchor)==1
s=s.replace(anchor,block+anchor)
ld={"@context":"https://schema.org","@type":"FAQPage","@id":"https://smarttirepicks.com/#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
s=s.replace('</head>','<script type="application/ld+json">\n'+json.dumps(ld,indent=2,ensure_ascii=False)+'\n</script>\n</head>',1)
open('index.html','w').write(s)
changed=['/']
for f in sorted(glob.glob('**/index.html',recursive=True)):
    t=open(f).read()
    if '"author"' not in t or 'class="byline"' in t: continue
    m=re.search(r'(<p class="last-updated">[^<]*</p>)',t)
    if not m: continue
    t=t.replace(m.group(1),m.group(1)+'\n<p class="byline">By Smart Tire Picks Editorial Team</p>',1)
    open(f,'w').write(t); changed.append('/'+f[:-len('index.html')])
open('/tmp/stp_changed.txt','w').write('\n'.join(changed))
print(len(changed),changed)
