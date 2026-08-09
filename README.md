# Rewind Dynamics — Website

A fast, dark, animated marketing website for **Rewind Dynamics** — an India-based
defence technology company (established 2024, New Delhi) developing autonomous
systems: unmanned aerial, humanoid and tactical platforms.

Built as a dependency-free static site — pure HTML, CSS and vanilla JavaScript.
No build step, no framework, deploys anywhere. The tone is deliberately factual:
the site explains what the company is working on **without** claiming finished
products or performance figures.

---

## Pages

| Page | File | Purpose |
|------|------|---------|
| Home | `index.html` | Intro, what we're building, capability areas, approach |
| Company | `about.html` | Story, mission & vision, values, timeline, team |
| Systems | `systems.html` | The systems in development: UAV, humanoid, tactical |
| Capabilities | `capabilities.html` | Areas of work: autonomy, perception, edge AI, systems engineering |
| Technology | `technology.html` | Plain-language tech overview + external references |
| Careers | `careers.html` | Culture, benefits, open roles, **application form** |
| Contact | `contact.html` | **Contact form**, direct emails, New Delhi location |
| Newsroom | `newsroom.html` | Company note + curated external reading, newsletter |
| Privacy & Terms | `privacy.html` | Legal template (have counsel review) |
| 404 | `404.html` | Error page |

Every navigation item is its own page, and outbound "Learn more / Reference"
links open reputable external sources (Wikipedia, arXiv, IEEE, DRDO) in a new tab.

---

## Email addresses

The site uses several addresses so enquiries reach the right place. Set up these
mailboxes (or forwards) on your domain:

| Address | Used for |
|---------|----------|
| `info@rewinddynamics.com` | General enquiries, contact form, newsletter |
| `careers@rewinddynamics.com` | Careers / applications (careers form) |
| `partnerships@rewinddynamics.com` | Suppliers, programs, collaborators |
| `press@rewinddynamics.com` | Media enquiries |

You can point them all at one inbox with forwarding to start.

### Form delivery (about 2 minutes)

Forms send submissions to your inbox via **Web3Forms** (free, no backend):

1. Go to **https://web3forms.com**, enter `info@rewinddynamics.com`, get a free **Access Key**.
2. Paste it into **`assets/js/form.js`** → `var ACCESS_KEY = "…"`.
3. Deploy.

> **Before a key is set,** forms fall back to opening the visitor's email client,
> addressed to the right inbox (contact → `info@`, careers → `careers@`), so the
> site works out of the box. Each form's destination is set with a `data-email`
> attribute; for fully separate routing you can create one Web3Forms key per inbox.

---

## Deploy

Static site — pick whichever is easiest:

- **Netlify / Vercel / Cloudflare Pages:** drag-and-drop this folder, or connect the repo.
  `netlify.toml` is included (publish dir `.`, custom 404, security headers).
- **GitHub Pages:** enable Pages on the branch; served from the root.
- **Any web host:** upload the files. `index.html` is the entry point.

No compile step. No `node_modules`.

---

## Brand & design

- **Logo:** recreated as crisp SVG (`assets/img/logo-mark.svg`) — metallic "R"
  monogram, motion chevron and electric-blue streak — tuned for dark backgrounds.
  `assets/img/favicon.svg` is the tab icon.
- **Type:** *Chakra Petch* (display), *Space Grotesk* (body), *JetBrains Mono* (labels).
- **Palette:** near-black `#06080C` with an electric-blue accent `#2F7BFF`.
- **Motion:** preloader + curtain wipe, scroll reveals, hero node-network canvas,
  radar/schematic SVGs, marquee, magnetic buttons — all respect `prefers-reduced-motion`.

### Customising

- **Colours / spacing / fonts:** CSS variables at the top of `assets/css/styles.css` (`:root`).
- **Copy:** edit the HTML directly — content is plain and clearly sectioned.
- **Social links:** the footer points to `linkedin.com/company/rewind-dynamics`,
  `x.com/rewinddynamics`, `youtube.com/@rewinddynamics` — create/confirm those handles
  (or edit them) so the icons land on your real profiles.

---

*An India-based defence technology company. New Delhi.*
