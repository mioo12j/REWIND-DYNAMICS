# Rewind Dynamics — Website

A fast, dark, animated marketing website for **Rewind Dynamics** — a global
defence-technology company (established **26 January 2020**, headquartered in New
Delhi) developing autonomous systems: unmanned aerial (UAV), precision-guided and tactical
platforms for governments and armed forces worldwide. Everything is
currently under **active research & development**; the first real-world mission
test is planned for **December 2026**.

Dependency-free static site — pure HTML, CSS and vanilla JavaScript. No build
step, no framework, deploys anywhere.

---

## Pages (53)

The site is organised as **hubs and spokes** so each topic has its own
keyword-targeted page and a clear path from the hub above it.

| Hub | Spokes |
|---|---|
| `systems.html` | Unmanned Aerial · Guided · Tactical Miniature |
| `capabilities.html` | Autonomy · Perception · Edge AI · Navigation · Systems Engineering |
| `applications.html` | ISR · Force Protection · Counter-UAS |
| `technology.html` | Simulation & Test |
| `research.html` | Swarm Autonomy |
| `newsroom.html` | 10 news articles |
| `insights.html` | 7 long-form feature articles |

Company & trust: About · Timeline · Responsible Autonomy · Security &
Compliance · Quality & Assurance · Suppliers · Partners · Investors ·
Careers · Contact · FAQ · Press · Glossary · Privacy · 404.

---

## Tooling

- `python3 tools/audit.py` — full site audit: titles, descriptions, canonicals,
  Open Graph, JSON-LD validity, one-H1 rule, heading order, broken links and
  anchors, missing assets, sitemap coverage, nav consistency, **orphan pages**
  and thin content. Exits non-zero on any error.
- `python3 tools/gen_sitemap.py` — regenerates `sitemap.xml` from the indexable
  pages on disk, so it can never drift out of sync.
- `tools/build_pages.py` — page and article generator (shared head, nav,
  footer and section components).

---

## Forms → your inbox (FormSubmit)

All forms (contact, careers, investor, newsletter) are delivered by email using
**FormSubmit** (https://formsubmit.co) — free, no signup, no API key.

**Destination:** `sid@siddhantkumar.in` (set as `TARGET_EMAIL` in `assets/js/form.js`).

**One-time activation:** after deploying, submit any form once. FormSubmit emails
`sid@siddhantkumar.in` a confirmation link — click it once, and every submission
from then on lands in that inbox.

- To change the destination, edit `TARGET_EMAIL` in `assets/js/form.js`.
- Optional privacy: once activated, FormSubmit gives you a random alias
  (`formsubmit.co/xxxx`) that hides the address — paste it into `ENDPOINT_BASE`.
- If the relay is ever unreachable, forms fall back to opening the visitor's
  email client addressed to the same inbox.

The public **display** emails on the site (info@, careers@, partnerships@, press@,
investors@ `@rewinddynamics.com`) are just contact addresses to set up on your
domain — form *delivery* goes to `sid@siddhantkumar.in`.

---

## SEO (built in)

- **Per-page** `<title>` + meta description, **canonical** URLs, and
  `robots` directives (`index, follow, max-image-preview:large`).
- **Open Graph** + **Twitter** card tags on every page, with a rendered
  **1200×630 share image** at `assets/img/og.png`.
- **JSON-LD structured data**: `Organization` (site-wide), `WebSite` (home),
  and `NewsArticle` (each newsroom article, with real publish dates).
- **`sitemap.xml`** — all pages with `lastmod` + priorities (image sitemap on home).
- **`robots.txt`** — allows Google/Bing/DuckDuckGo and AI crawlers
  (GPTBot, PerplexityBot, Google-Extended, …); points to the sitemap.
- **`llms.txt`** — a concise, LLM-readable summary of the company and pages.

After deploying to the real domain, submit the site to **Google Search Console**
and **Bing Webmaster Tools** and paste in the sitemap URL for fastest indexing.
If you host on a different domain than `rewinddynamics.com`, update the absolute
URLs in the `<head>` SEO block, `sitemap.xml`, `robots.txt` and `llms.txt`.

---

## Deploy

Static site — pick whichever is easiest:

- **Netlify / Vercel / Cloudflare Pages:** drag-and-drop the folder, or connect the repo.
  `netlify.toml` is included (custom 404 + security headers).
- **GitHub Pages:** enable Pages on the branch; served from the root.
- **Any web host:** upload the files. `index.html` is the entry point.

---

## Brand & design

- **Logo:** crisp SVG (`assets/img/logo-mark.svg`) — metallic "R" monogram with a
  motion chevron and electric-blue streak. `favicon.svg` is the tab icon;
  `og.png` is the social share card.
- **Type:** Chakra Petch (display), Space Grotesk (body), JetBrains Mono (labels).
- **Palette:** near-black `#06080C` + electric-blue `#2F7BFF`.
- **Motion:** preloader + curtain wipe, scroll reveals, hero canvas mesh, an
  orbital brand emblem, radar/schematic SVGs — all respect `prefers-reduced-motion`.
- **CSS variables** live at the top of `assets/css/styles.css`.

### To finish setting up
- Set up the `@rewinddynamics.com` mailboxes (or forwards).
- Activate FormSubmit (submit one form, click the confirmation email).

---

*Autonomous systems for defence. Headquartered in New Delhi — since 2020.*

---

## Measured performance

Served locally, fonts unavailable (worst case), 1350×940 viewport:

| Metric | index.html | glossary.html | Google "good" |
|---|---|---|---|
| First Contentful Paint | 236 ms | 192 ms | < 1800 ms |
| Largest Contentful Paint | 232 ms | 188 ms | < 2500 ms |
| Cumulative Layout Shift | **0** | **0** | < 0.1 |
| DOMContentLoaded | 100 ms | 85 ms | — |
| Requests / transfer | 7 / 72 KB | 7 / 72 KB | — |

How it stays fast: no framework and no build step; one 48 KB stylesheet and
20 KB of vanilla JS loaded with `defer`; web fonts preloaded and swapped in
without blocking first paint; every `<img>` carries intrinsic dimensions so
nothing shifts while loading, with lazy loading below the fold.

## Machine-readable surface

| File | Purpose |
|---|---|
| `sitemap.xml` | Every indexable page, tiered priorities, generated from disk |
| `sitemap-news.xml` | Articles in Google News format, with publication dates |
| `sitemap-index.xml` | Points at both sitemaps |
| `feed.xml` | RSS 2.0 of newsroom + insights, autodiscovered from every page |
| `llms.txt` | Structured summary of the company and every page |
| `llms-full.txt` | Full readable text of the whole site (~219 KB) for AI systems |
| `.well-known/security.txt` | Responsible-disclosure contact |
| `robots.txt` | Welcomes search and answer-engine crawlers; points at all of the above |

Structured data: `Organization`, `WebSite` and `WebPage` linked by `@id` into
one entity graph on every page, plus `BreadcrumbList` sitewide, `Article` /
`NewsArticle` on all 16 articles, `FAQPage` on FAQ, UAV, precision-guidance
and applications, `DefinedTermSet` on the glossary, `CollectionPage` and
`ItemList` on hubs.

## Verification

Both auditors must pass before any change ships:

    python3 tools/audit.py             # 60 pages: SEO, schema, links, orphans
    python3 tools/responsive_audit.py  # 600 renders: 60 pages x 10 viewports

Current state: **zero errors, zero warnings, zero layout faults.**
