# Rewind Dynamics — Website

A fast, dark, animated marketing website for **Rewind Dynamics** — an Indian
defence-technology company (established **26 January 2020**, New Delhi) developing
indigenous autonomous systems: unmanned aerial (UAV), humanoid and tactical
miniature platforms. Everything is currently under **active research &
development**; the first real-world mission test is planned for **December 2026**.

Dependency-free static site — pure HTML, CSS and vanilla JavaScript. No build
step, no framework, deploys anywhere.

---

## Pages (21)

Home · Company · Systems · Capabilities · Technology · **Investors** · Careers ·
Newsroom · Contact · Privacy · 404, plus **10 newsroom articles** (`news-*.html`)
dated 2020–2026. Every nav item is its own page.

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
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, …); points to the sitemap.
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
- Create the **LinkedIn** and **X** company profiles (footer links already point
  to `linkedin.com/company/rewind-dynamics` and `x.com/rewinddynamics`).
- Set up the `@rewinddynamics.com` mailboxes (or forwards).
- Activate FormSubmit (submit one form, click the confirmation email).

---

*Indigenous autonomous systems for defence. New Delhi, India — since 2020.*
