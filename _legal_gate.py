#!/usr/bin/env python3
"""Pre-publish legal hold gate (JI Ventures global rule, 27 Oct 2026). Re-runnable, no side effects on HTML.
Usage: python3 _legal_gate.py [--root DIR] [--queue FILE] [--approvals FILE] [--files a.html b.md ...]
Exit 0 = PASS (publish allowed). Exit 1 = HOLD_REVIEW (do not publish); each flag appended once to queue.jsonl.
A held file publishes only if approvals.jsonl has {"site","path","sha256"} matching that exact version,
recorded from Joshua's explicit approval. This script never writes approvals.
Amendment (27 Oct): HIGH rules 1, 2, 6, 8 need Joshua's approval. A file with only MODERATE flags (3, 4, 5, 7) also
publishes if moderate-clearances.jsonl has a SAFE ChatGPT verdict for {"site","path","sha256"} of that exact version."""
import re, json, sys, hashlib, argparse, datetime, html
from pathlib import Path
SITE, BOT = "smarttirepicks.com", "Tire Review Bot"
CR = Path("/workspace/content-review")
ap = argparse.ArgumentParser()
ap.add_argument("--root", default=str(Path(__file__).resolve().parent))
ap.add_argument("--queue", default=str(CR / "queue.jsonl"))
ap.add_argument("--approvals", default=str(CR / "approvals.jsonl"))
ap.add_argument("--clearances", default=str(CR / "moderate-clearances.jsonl"))
ap.add_argument("--files", nargs="*")
ap.add_argument("--changed", metavar="BASE", help="only check files changed between BASE and HEAD (pre-push / CI)")
a = ap.parse_args(); ROOT = Path(a.root)
rights = json.loads((ROOT / "_content_rights.json").read_text()) if (ROOT / "_content_rights.json").exists() else {"assets": {}}
LEGAL_PAGES = {"privacy/index.html", "terms/index.html", "disclaimer/index.html", "affiliate-disclosure/index.html", "contact/index.html", "contact.html", "about.html"}
W = lambda p: re.compile(p, re.I)
TEXT_RULES = [
 (1, W(r"\b(fraud\w*|scam(med|mer|s)?|criminal|crimes?|lawsuit|sued|corrupt\w*|bribe\w*|misconduct|embezzl\w*|cheat(ed|ing)|lied|liars?|dishonest\w*|abuse[sd]?|allegedly|accused)\b"), "Possible damaging allegation"),
 (2, W(r"\b(ssn|social security number|bank account|routing number|home address|date of birth|diagnosed with|medical records?)\b"), "Possible sensitive personal information"),
 (5, W(r"\b(guaranteed (returns?|profit|income)|you should (invest|buy shares)|risk[- ]free (return|investment)|dosage|consult us for legal|tax advice for you)\b"), "Possible personalised financial, medical, legal or tax advice"),
 (6, W(r"\b(election|elections|ballots?|polling (place|station|location)s?|voter registration|register to vote|early voting|certified results?)\b"), "Election information needs election authority confirmation"),
 (7, W(r"\b(endorsed by|official (partner|retailer|dealer|site|supplier) of|in partnership with|certified by|approved by (michelin|bridgestone|goodyear|continental|pirelli|nhtsa|dot)|sponsored by)\b"), "Possible implied endorsement or affiliation"),
 (8, W(r"\b(cease and desist|dmca|takedown notice|legal notice|embargo(ed)?|reporting restriction|under seal)\b"), "Legal complaint or restriction wording"),
]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"); PHONE = re.compile(r"(?<!\d)(\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")
ALLOWED_PII = {"joshuaofisrael@gmail.com", "5640 W Maple Rd"}
QUOTE = re.compile(r"[\u201c\"]([^\u201d\"<>]{25,300})[\u201d\"]\s*,?\s*(said|says|told|according to)", re.I)
def visible(t):
    t = re.sub(r"<script\b(?![^>]*ld\+json)[\s\S]*?</script>|<style[\s\S]*?</style>", " ", t, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))
def check(rel, raw):
    flags = []; txt = visible(raw)
    for n, rx, why in TEXT_RULES:
        for m in rx.finditer(txt):
            flags.append((n, txt[max(0, m.start()-60):m.end()+60].strip(), why))
    if rel not in LEGAL_PAGES:
        for m in EMAIL.finditer(txt):
            if m.group(0).lower() not in ALLOWED_PII and not m.group(0).endswith((".webp", ".png", ".jpg")):
                flags.append((2, m.group(0), "Email address in public content"))
        for m in PHONE.finditer(txt): flags.append((2, m.group(0), "Phone number in public content"))
    # Rule 3: every image/media asset needs a documented rights record
    for m in re.finditer(r"""(?:src|href|content|srcset)=["']([^"']+\.(?:webp|jpe?g|png|gif|svg|mp4|webm|avif))""", raw, re.I):
        for u in m.group(1).split(","):
            u = u.strip().split(" ")[0]
            if not u: continue
            if re.match(r"https?://", u) and not u.startswith("https://smarttirepicks.com/"):
                flags.append((3, u, "External media asset with no documented permission")); continue
            key = re.sub(r"^https://smarttirepicks\.com", "", u).lstrip("/")
            if key not in rights["assets"]: flags.append((3, u, "Media asset missing from _content_rights.json"))
    # Rule 4: article pages need an accessed external source; quotes need manual verification
    if re.match(r"(guides|reviews|comparisons)/[^/]+/index\.html$", rel):
        ext = [h for h in re.findall(r'href="(https?://[^"]+)"', raw) if "smarttirepicks.com" not in h and "cloudflare" not in h]
        if not ext: flags.append((4, rel, "Article has no external source links"))
    for m in QUOTE.finditer(txt): flags.append((4, m.group(0)[:200], "Attributed quote needs verification against accessed source"))
    return flags
def files():
    if a.files: return [Path(f).resolve() for f in a.files]
    if a.changed:
        import subprocess
        out = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", "--diff-filter=ACMR", a.changed, "HEAD"], capture_output=True, text=True)
        if out.returncode: print("legal gate: cannot diff, checking everything"); a.changed = None; return files()
        ch = [ROOT / f for f in out.stdout.split()]
        if any(f.startswith("assets/") for f in out.stdout.split()): pass
        return [p for p in ch if p.exists() and p.suffix in (".html", ".md", ".txt", ".xml") and not p.name.startswith("_") and p.name != "README.md"]
    return [p for p in ROOT.rglob("*") if p.suffix in (".html", ".md", ".txt", ".xml") and ".git" not in p.parts and not p.name.startswith("_") and p.name != "README.md"]
approved = set()
if Path(a.approvals).exists():
    for l in Path(a.approvals).read_text().splitlines():
        try:
            j = json.loads(l)
            if j.get("site") == SITE and j.get("approved_by", "").lower().startswith("joshua"): approved.add((j["path"], j["sha256"]))
        except Exception: pass
HIGH_RULES = {1, 2, 6, 8}  # Amendment 27 Oct 18:25: Joshua only
cleared = set()  # MODERATE only: SAFE ChatGPT review logged for this exact site+path+sha256
if Path(a.clearances).exists():
    for l in Path(a.clearances).read_text().splitlines():
        try:
            j = json.loads(l)
            v = str(j.get("verdict") or j.get("chatgpt_verdict") or "").strip().upper()
            pth = j.get("path") or j.get("draft_path")
            if j.get("site") == SITE and v.startswith("SAFE") and pth and j.get("sha256"): cleared.add((pth, j["sha256"]))
        except Exception: pass
existing = Path(a.queue).read_text() if Path(a.queue).exists() else ""
held = 0
for p in files():
    raw = p.read_text(errors="ignore"); rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    fl = check(rel, raw)
    if not fl: continue
    h = hashlib.sha256(raw.encode()).hexdigest()
    if (rel, h) in approved: print(f"APPROVED (exact version) {rel}"); continue
    if not any(n in HIGH_RULES for n, _, _ in fl) and (rel, h) in cleared:
        print(f"MODERATE CLEARED (SAFE review, exact version) {rel}"); continue
    held += 1
    t = re.search(r"<title>(.*?)</title>", raw, re.S); title = html.unescape(t.group(1).strip()) if t else rel
    for n, flagged, why in fl:
        print(f"HOLD_REVIEW rule {n}: {rel}: {why}: {flagged[:140]!r}")
        key = f'"draft_path": "{rel}", "sha256": "{h}", "rule": {n}'
        if key in existing: continue
        rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "site": SITE, "bot": BOT,
               "title": title, "flagged": flagged[:500], "rule": n, "sources": re.findall(r'href="(https?://(?!smarttirepicks)[^"]+)"', raw)[:10],
               "suggestion": why + ". Joshua to review; do not publish until approved (approvals.jsonl, exact sha256).",
               }
        rec2 = {k: rec[k] for k in ("ts","site","bot","title","flagged")}; rec2.update({"draft_path": rel, "sha256": h, "rule": n})
        rec2.update({k: rec[k] for k in ("sources","suggestion")}); rec2["status"] = "HOLD_REVIEW"
        with open(a.queue, "a") as f: f.write(json.dumps(rec2) + "\n")
        existing += json.dumps(rec2)
        if n == 8: print("RULE 8: message Personal assistant immediately with priority.")
print(f"legal gate: {'HOLD_REVIEW' if held else 'PASS'} ({held} file(s) held)")
sys.exit(1 if held else 0)
