# Smart Tire Picks (`smarttirepicks.com`)

Static educational tire site for **Smart Tire Picks**, owned by **Joshua Israel Ventures LLC**.

## Stack

- Plain HTML pages (folder `index.html` URLs for clean paths)
- One shared stylesheet: `css/styles.css`
- Minimal JS: `js/main.js` (mobile nav toggle only)
- No required build step

Optional: re-run `python3 _generate.py` only if you edit that generator; published files are the HTML already in this folder.

## Local preview

From this directory:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/` — root-absolute asset paths (`/css/...`) work correctly under a local server (not always via `file://`).

## Deploy — Netlify (drag & drop)

1. Zip **the contents** of `smarttirepicks-site/` (or deploy the folder itself).
2. Netlify → Sites → **Add new site** → **Deploy manually** → drop the folder.
3. Set domain `smarttirepicks.com` (DNS already at registrar as applicable).
4. Publish directory = site root (where `index.html` lives). No build command.

`netlify.toml` is optional; none is required for a static drop.

## Deploy — GitHub Pages

1. Push this folder as a repo (or `/docs` / Actions artifact).
2. Settings → Pages → Deploy from branch → root (or `/docs`).
3. For a custom domain, add a `CNAME` file containing `smarttirepicks.com` and point DNS per GitHub’s docs.
4. Ensure Pages serves from the directory that contains `index.html`.

## SEO / legal

- Unique `<title>` + meta description on each page
- Canonical URLs → `https://smarttirepicks.com/...`
- `robots.txt` + `sitemap.xml`
- Per-page editorial disclaimer + sitewide footer soft language
- Full `/disclaimer/` and `/affiliate-disclosure/`

## Affiliate CTAs

Placeholders say “coming soon / check retailers” — no live affiliate URLs yet.
