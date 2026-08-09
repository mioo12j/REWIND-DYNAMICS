# Rewind Dynamics — Website

A fast, dark, highly-animated marketing website for **Rewind Dynamics**, a defense
company building autonomous systems. Built as a dependency-free static site — pure
HTML, CSS and vanilla JavaScript. No build step, no framework, deploys anywhere.

---

## Pages

| Page | File | Purpose |
|------|------|---------|
| Home | `index.html` | Hero, mission, capability overview, stats, flywheel, newsroom teaser |
| Company | `about.html` | Story, mission & vision, values, roadmap, leadership |
| Capabilities | `capabilities.html` | The four capability domains + multi-domain + FAQ |
| Technology | `technology.html` | Autonomy architecture, sim-first dev, the "rewind" flywheel, security |
| Careers | `careers.html` | Culture, benefits, open roles, **application form** |
| Contact | `contact.html` | **Contact form**, direct channels, HQ grid |
| Newsroom | `newsroom.html` | Featured post, article grid, newsletter signup |
| Privacy & Terms | `privacy.html` | Legal template (have counsel review) |
| 404 | `404.html` | "Signal lost" error page |

---

## Forms → your email

All forms (contact, careers application, newsletter) send submissions to your inbox.

### Set it up (about 2 minutes)

1. Go to **https://web3forms.com**
2. Enter **info@rewinddynamics.com** and click to get a **free Access Key** (it's emailed to you).
3. Open **`assets/js/form.js`** and paste the key:

   ```js
   var ACCESS_KEY = "paste-your-web3forms-key-here";
   ```

4. Deploy. Every submission now lands in **info@rewinddynamics.com**.

> **Before setup / no key configured:** forms automatically fall back to opening the
> visitor's own email client addressed to `info@rewinddynamics.com`, so the site is
> fully functional out of the box — just less seamless than the hosted relay.

Want submissions to also reach another address (e.g. a personal inbox)? Add a mail
rule/forward on `info@rewinddynamics.com`, or create a second Web3Forms key. The
destination address is controlled entirely on the Web3Forms side — no code change needed.

---

## Deploy

It's a static site — pick whichever is easiest:

- **Netlify / Vercel / Cloudflare Pages:** drag-and-drop this folder, or connect the repo.
  `netlify.toml` is included (publish dir `.`, custom 404, security headers).
- **GitHub Pages:** enable Pages on the branch; the site is served from the root.
- **Any web host:** upload the files. `index.html` is the entry point.

No compile step. No `node_modules`. Nothing to install.

---

## Brand & design

- **Logo:** recreated as crisp SVG (`assets/img/logo-mark.svg`) in the spirit of the
  supplied mark — metallic "R" monogram, motion chevron and electric-blue speed streak —
  tuned for dark backgrounds. `assets/img/favicon.svg` is the browser-tab icon.
- **Type:** *Chakra Petch* (sharp technical display), *Space Grotesk* (body),
  *JetBrains Mono* (labels/data) — loaded from Google Fonts.
- **Palette:** near-black `#06080C` with an electric-blue accent `#2F7BFF`.
- **Motion:** preloader + curtain wipe, scroll reveals, hero node-network canvas,
  count-up stats, text-scramble, radar/schematic SVGs, marquee, magnetic buttons.
  All motion respects `prefers-reduced-motion`.

### Customising

- **Colours / spacing / fonts:** CSS variables at the top of `assets/css/styles.css` (`:root`).
- **Copy:** edit the HTML directly — content is plain and clearly sectioned.
- **Contact email:** it's `info@rewinddynamics.com` throughout; update the `mailto:`
  links and `CONTACT_EMAIL` in `assets/js/form.js` if it ever changes.
- **Social links:** placeholder `#` hrefs in every footer — point them at your profiles.

---

## Structure

```
.
├── index.html · about.html · capabilities.html · technology.html
├── careers.html · contact.html · newsroom.html · privacy.html · 404.html
├── assets/
│   ├── css/styles.css      # design system + components + animations
│   ├── js/app.js           # nav, reveals, canvas, counters, accordion…
│   ├── js/form.js          # form validation + email delivery
│   └── img/                # logo-mark.svg, favicon.svg
├── robots.txt · sitemap.xml · netlify.toml
└── README.md
```

---

*Autonomy for the decisive edge.*
