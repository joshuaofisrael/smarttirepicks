#!/usr/bin/env python3
"""28 Oct 2026: release rule 4 holds by adding verified outside sources (all URLs returned 200 on 28 Oct),
correcting the CrossClimate 2 category wording to match Michelin's own page, and expanding all-season vs winter.
Re-runnable (idempotent markers). Never run _generate.py."""
from pathlib import Path
R = Path(__file__).resolve().parent
A = 'rel="noopener noreferrer" target="_blank"'
def src(items):
    li = "\n".join(f'          <li><a href="{u}" {A}>{t}</a> — {d}</li>' for u, t, d in items)
    return f'''      <section class="content-section sources" data-sources="20261028">
        <h2>Sources</h2>
        <p class="note">Accessed 28 October 2026. Manufacturer pages describe the maker's own claims; we have not verified them by testing.</p>
        <ul>
{li}
        </ul>
      </section>
'''
MICH_CC2 = ("https://www.michelinman.com/auto/tires/michelin-crossclimate-2", "Michelin USA, CrossClimate2 product page")
MICH_SWA = ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/summer-winter-all-season-tires", "Michelin USA, Summer vs winter vs all-season tires")
MICH_WIN = ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/guide-to-buying-winter-tires", "Michelin USA, Winter tire buying guide")
MICH_TYPES = ("https://www.michelinman.com/auto/auto-tips-and-advice/tire-buying-guide/differences-in-types-of-seasonal-tires", "Michelin USA, Differences in types of seasonal tires")
MICH_FAQ = ("https://www.michelinman.com/auto/assistance/michelin-faqs", "Michelin USA, FAQs")
USTMA = ("https://www.ustires.org/system/files/2026-04/TISB_37_v7_December%202020.pdf", "USTMA, Tire Information Service Bulletin 37: definition of tires for use in severe snow conditions (PDF)")
BS_QT = ("https://www.bridgestonetire.com/tire/turanza-quiettrack/225-65r17/", "Bridgestone, Turanza QuietTrack product page")
BS_PR = ("https://www.bridgestoneamericas.com/en/press-release-details.en.2019.bridgestone-launches-new-touring-tire-engineered-for-long-lastin", "Bridgestone Americas, Turanza QuietTrack launch press release (24 April 2019)")
TP = ("https://www.tiresplus.com/blog/tires/touring-tires-vs-performance-tires/", "Tires Plus, Performance tires vs touring tires")
PAGES = {
 "reviews/michelin-crossclimate2/index.html": {
  "repl": [
   ("Michelin positions the CrossClimate 2 as an all-weather oriented grand touring tire for drivers who want stronger cold weather cues than a basic all-season while keeping one mounted set.",
    "Michelin lists the CrossClimate2 as an all-season tire for cars, SUVs, crossovers and vans, and its product page shows the three peak mountain snowflake (3PMSF) severe snow mark. That makes it a common pick for drivers who want stronger cold weather credentials than a basic all-season while keeping one mounted set."),
   ("Michelin markets the CrossClimate 2 in the grand-touring / all-weather-oriented space, emphasizing year-round capability and winter-oriented branding cues (including 3PMSF marking on applicable sizes — verify on the specific tire).",
    "Michelin's product page lists the CrossClimate2 as an all-season tire with the 3PMSF and mud and snow marks, and describes it as designed for every climate condition. Some reviewers call this kind of 3PMSF all-season an all-weather tire. Michelin's own comparison claims (shorter stopping and longer tread life against named competitors) are manufacturer claims we have not tested, so we do not repeat them as fact. Confirm the 3PMSF mark on the exact size you buy."),
   ("Michelin positions it in an all-weather / grand-touring oriented space, and many sizes carry",
    "Michelin lists it as an all-season tire, and its product page shows"),
  ],
  "sources": [MICH_CC2 + ("product category (all-season), 3PMSF and mud and snow marks, warranty and size listings",),
              USTMA + ("what the 3PMSF symbol means: a tire that meets a minimum snow traction index against a standard reference tire in a packed snow test",),
              MICH_SWA + ("how all-season, all-weather 3PMSF and dedicated winter tires differ, and when two sets make sense",)],
 },
 "reviews/bridgestone-turanza-quiettrack/index.html": {
  "repl": [
   ("Exact features, warranties, and available sizes should be confirmed on current manufacturer materials for your size.",
    "Bridgestone's product page lists it in the touring, all-season category for sedans and minivans, names its top three features as quiet ride, ride comfort and tread life, and states a limited mileage warranty of up to 80,000 miles (conditions apply). Its 2019 launch release says it replaced the Turanza Serenity Plus. Exact features, warranties, and available sizes should be confirmed on current manufacturer materials for your size."),
  ],
  "sources": [BS_QT + ("category (touring, all-season), top features, stated up to 80,000 mile limited warranty with conditions, size list",),
              BS_PR + ("launch details, noise dampening tread technology, replacement of the Serenity Plus line",),
              MICH_SWA + ("general limits of all-season tires in heavy snow and on ice",)],
 },
 "comparisons/touring-vs-performance-all-season/index.html": {
  "repl": [("(all-weather / grand-touring oriented editorial)", "(3PMSF all-season editorial)")],
  "sources": [TP + ("touring tires generally prioritise a smooth, quiet ride and longer tread life; performance tires prioritise cornering, braking feel and response",),
              MICH_TYPES + ("all-season tires balance dry and wet performance with acceptable light snow traction and typically long tread life",),
              BS_QT + ("example of a touring all-season line marketed on quiet ride, comfort and tread life",)],
 },
 "comparisons/all-season-vs-winter/index.html": {
  "repl": [], "sources": [MICH_SWA + ("all-season limits in heavy snow and ice; M+S is not a severe snow certification; winter compounds stay flexible below about 45°F (7°C); all-weather 3PMSF tires as a middle ground",),
              MICH_WIN + ("what to look for on a winter tire sidewall, including 3PMSF and the newer ice grip symbol",),
              MICH_FAQ + ("Michelin recommends a full set of four winter tires; winter tires carry no UTQG grades",),
              USTMA + ("industry definition of the 3PMSF severe snow symbol and the packed snow traction test behind it",)],
 },
}
EXPAND = '''        <h2>The 45°F rule of thumb</h2>
        <p>Michelin's tire buying guide says winter tire compounds stay flexible below about 45°F (7°C), the point where it says summer and all-season compounds start to harden and lose grip. It suggests switching to winter tires when average daily temperatures fall below that level and switching back once temperatures stay above it. Treat this as a manufacturer guideline, not a fixed law; your local roads and storms matter as much as the thermometer.</p>
        <h2>What the sidewall marks actually mean</h2>
        <div class="table-wrap"><table>
          <thead><tr><th>Mark</th><th>What it indicates</th><th>Source</th></tr></thead>
          <tbody>
            <tr><td>M+S (mud and snow)</td><td>A tread design marking common on all-season tires. Michelin notes it is not a severe snow certification.</td><td>Michelin</td></tr>
            <tr><td>3PMSF (three peak mountain snowflake)</td><td>Under the USTMA definition, a passenger or light truck tire that reaches a minimum snow traction index against a standard reference tire in a packed snow test (ASTM F1805) may carry this symbol next to its M+S marking.</td><td>USTMA TISB 37</td></tr>
            <tr><td>Ice grip symbol</td><td>A newer mark Michelin describes as indicating added braking performance on ice, seen on some winter tires.</td><td>Michelin</td></tr>
          </tbody>
        </table></div>
        <h2>The middle option: 3PMSF all-season or all-weather tires</h2>
        <p>Some all-season tires carry the 3PMSF mark, and many shops call these all-weather tires. Michelin describes them as a middle ground for drivers who want tested severe snow traction without managing two seasonal sets. They are still a compromise: a dedicated winter tire is built only for cold conditions, while a 3PMSF all-season also has to work in summer heat. Example on this site: <a href="/reviews/michelin-crossclimate2/">Michelin CrossClimate 2 overview</a>.</p>
        <h2>Fit four, not two</h2>
        <p>Michelin recommends installing winter tires on all four wheel positions. Its FAQ warns that mixing winter tires on one axle with non winter tires on the other can upset vehicle balance, causing understeer or oversteer depending on which axle has less grip. AWD or 4WD helps you get moving, but Michelin notes it does not replace winter tires for braking and cornering.</p>
        <h2>Quick decision table</h2>
        <div class="table-wrap"><table>
          <thead><tr><th>Your winters</th><th>Common approach</th></tr></thead>
          <tbody>
            <tr><td>Mostly above freezing, occasional frost or light snow</td><td>A quality all-season tire may be enough</td></tr>
            <tr><td>Regular cold snaps, some snow, want one set</td><td>Consider a 3PMSF all-season (all-weather) tire</td></tr>
            <tr><td>Long periods below freezing, packed snow or ice, hills or rural roads</td><td>Dedicated winter set on four wheels, swapped seasonally</td></tr>
          </tbody>
        </table></div>
        <p class="note">This table is general guidance based on the sources below, not a safety guarantee. Local law, road conditions and your vehicle maker's guidance come first.</p>
        <h2>FAQ</h2>
        <h3>Do winter tires wear out faster?</h3>
        <p>Michelin says winter tires wear at a comparable rate when used in cold months, but wear faster if left on through warm weather, which is one reason to swap them off in spring.</p>
        <h3>Why don't winter tires have UTQG treadwear grades?</h3>
        <p>According to Michelin's FAQ, winter tires are not assigned UTQG treadwear, traction or temperature grades. See our <a href="/guides/utqg/">UTQG guide</a> for how grades work on other tires.</p>
'''
for rel, cfg in PAGES.items():
    p = R / rel; s = p.read_text()
    for old, new in cfg["repl"]:
        if old in s: s = s.replace(old, new)
    if 'data-sources="20261028"' not in s:
        block = src(cfg["sources"])
        if '<nav class="related-links"' in s: s = s.replace('      <nav class="related-links"', block + '      <nav class="related-links"', 1)
        else: s = s.replace('      <div class="cta-box">', block + '      <div class="cta-box">', 1)
    if rel.startswith("comparisons/all-season-vs-winter") and "The 45°F rule of thumb" not in s:
        s = s.replace('        <p class="note">Related: <a href="/guides/winter-tires/">', EXPAND + '        <p class="note">Related: <a href="/guides/winter-tires/">', 1)
    for d in ("2026-10-08", "2026-10-01"): s = s.replace(f'"dateModified": "{d}"', '"dateModified": "2026-10-28"')
    for d in ("October 8, 2026", "October 1, 2026"): s = s.replace(f"Last updated: {d}", "Last updated: October 28, 2026")
    p.write_text(s); print("patched", rel)
