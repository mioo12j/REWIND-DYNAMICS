#!/usr/bin/env python3
"""Page builder for Rewind Dynamics.

Generates full pages from a compact content spec so every page shares the
same head, navigation, footer and section rhythm. Run from the repo root.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://rewinddynamics.com/"

NAV = [("about.html", "Company"), ("systems.html", "Systems"),
       ("capabilities.html", "Capabilities"), ("applications.html", "Applications"),
       ("technology.html", "Technology"), ("research.html", "Research"),
       ("investors.html", "Investors"), ("careers.html", "Careers"),
       ("newsroom.html", "Newsroom")]
DRAWER = [("index.html", "Home")] + NAV + [("contact.html", "Contact")]

ORG = ('{"@context": "https://schema.org", "@type": "Organization", "@id": "https://rewinddynamics.com/#organization", '
 '"name": "Rewind Dynamics", "legalName": "Rewind Dynamics", "url": "https://rewinddynamics.com/", '
 '"sameAs": ["https://www.instagram.com/rewinddynamics/"], '
 '"logo": {"@type": "ImageObject", "url": "https://rewinddynamics.com/assets/img/logo-mark.svg"}, '
 '"image": "https://rewinddynamics.com/assets/img/og.png", "foundingDate": "2020-01-26", '
 '"description": "Rewind Dynamics is a global defence-technology company developing '
 'autonomous systems \\u2014 autonomous drones (UAV), precision-guided and tactical platforms \\u2014 for defence and military applications.", '
 '"email": "info@rewinddynamics.com", "slogan": "Autonomous systems for defence.", '
 '"areaServed": {"@type": "Place", "name": "Worldwide"}, '
 '"knowsAbout": ["Autonomous systems", "Autonomous drones", "Military drones", "Automated drones", '
 '"Unmanned aerial vehicles", "UAV", "Precision guidance", "Loitering munitions", "Tactical systems", '
 '"Defence technology", "Edge AI", "Perception", "Autonomy", "Drone swarms", "Counter-drone systems", '
 '"Counter-UAS", "ISR", "GPS-denied navigation"]}')

TICK = ('<span class="mk"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" '
        'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
ARW = ('<svg class="arw" width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" '
       'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
LARW = ('<svg width="18" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ------------------------------------------------------------------ sections
def sec_intro(eyebrow, h2, paras, index):
    body = "".join(
        f'\n        <p class="{"lead " if i == 0 else ""}reveal" data-d="{i+1}">{p}</p>'
        for i, p in enumerate(paras))
    return f'''  <section class="section">
    <div class="container">
      <div class="shead">
        <div class="shead__l">
          <p class="eyebrow reveal">{eyebrow}</p>
          <h2 class="h1 reveal" data-d="1">{h2}</h2>
        </div>
        <span class="shead__index reveal" data-d="2">{index}</span>
      </div>
      <div class="prose-2">{body}
      </div>
    </div>
  </section>'''

def sec_split(eyebrow, h2, lead, items, panel_label, panel_corner, specs, rev=False):
    lis = "".join(
        f'\n            <li class="reveal" data-d="{i}">{TICK}<div><b>{t}</b>{d}</div></li>'
        for i, (t, d) in enumerate(items))
    sp = "".join(
        f'\n              <div class="spec"><span class="spec__k">{k}</span><span class="spec__v">{v}</span></div>'
        for k, v in specs)
    return f'''  <section class="section">
    <div class="container">
      <div class="split{' split--rev' if rev else ''}">
        <div class="split__body">
          <p class="eyebrow reveal">{eyebrow}</p>
          <h2 class="h2 reveal" data-d="1">{h2}</h2>
          <p class="lead reveal" data-d="2" style="margin:18px 0 22px">{lead}</p>
          <ul class="klist">{lis}
          </ul>
        </div>
        <div class="split__media reveal-x">
          <div class="panel panel--pad">
            <span class="panel__label">{panel_label}</span><span class="panel__corner">{panel_corner}</span>
            <div class="specs" style="margin-top:26px">{sp}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>'''

def sec_cards(eyebrow, h2, lead, cards, index):
    cs = "".join(
        f'<article class="card reveal" data-d="{(i % 4) + 1}"><span class="card__idx">{i+1:02d}</span>'
        f'<h3 style="margin-top:14px">{t}</h3><p>{d}</p></article>'
        for i, (t, d) in enumerate(cards))
    leadp = f'\n          <p class="lead reveal" data-d="2" style="margin-top:16px">{lead}</p>' if lead else ""
    return f'''  <section class="section">
    <div class="container">
      <div class="shead">
        <div class="shead__l">
          <p class="eyebrow reveal">{eyebrow}</p>
          <h2 class="h1 reveal" data-d="1">{h2}</h2>{leadp}
        </div>
        <span class="shead__index reveal" data-d="3">{index}</span>
      </div>
      <div class="grid cards">{cs}
      </div>
    </div>
  </section>'''

def sec_values(eyebrow, h2, lead, vals, index):
    vs = "".join(
        f'<div class="value reveal" data-d="{i+1}"><span class="value__n">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(vals))
    leadp = f'\n          <p class="lead reveal" data-d="2" style="margin-top:16px">{lead}</p>' if lead else ""
    return f'''  <section class="section--tight">
    <div class="container">
      <div class="shead">
        <div class="shead__l">
          <p class="eyebrow reveal">{eyebrow}</p>
          <h2 class="h1 reveal" data-d="1">{h2}</h2>{leadp}
        </div>
        <span class="shead__index reveal" data-d="3">{index}</span>
      </div>
      <div class="grid values">{vs}
      </div>
    </div>
  </section>'''

def sec_links(items, heading="Related reading."):
    cs = "".join(
        f'<a class="card reveal" data-d="{i+1}" href="{h}"><span class="card__idx">{i+1:02d}</span>'
        f'<h3 style="margin-top:14px">{t}</h3><p>{d}</p></a>' for i, (t, h, d) in enumerate(items))
    return f'''  <section class="section--tight">
    <div class="container">
      <div class="shead"><div class="shead__l"><p class="eyebrow reveal">Explore Further</p>
        <h2 class="h2 reveal" data-d="1">{heading}</h2></div></div>
      <div class="grid cards">{cs}
      </div>
    </div>
  </section>'''

def sec_note(text):
    return f'''  <section class="section--tight">
    <div class="container">
      <p class="muted reveal" style="font-size:.92rem;max-width:78ch">{text}</p>
    </div>
  </section>'''

RD_NOTE = ('Everything described here is under <strong style="color:var(--ink-soft)">active research and development</strong>. '
 'Nothing has been fielded, and we do not publish specifications or performance figures. Our first end-to-end '
 'mission test is planned for <a href="news-first-mission.html" style="color:var(--accent-2)">December 2026</a>. '
 'Technical detail is shared directly with partners, evaluators and the armed forces under appropriate terms — '
 '<a href="contact.html" style="color:var(--accent-2)">get in touch</a>.')

def sec_cta(eyebrow, h, lead, b1, b2):
    return f'''  <section class="section">
    <div class="container">
      <div class="cta reveal">
        <div class="wm wm--cta" aria-hidden="true"><img src="assets/img/watermark.svg" alt=""></div>
        <div class="cta__grid" aria-hidden="true"></div>
        <p class="eyebrow eyebrow--center" style="justify-content:center">{eyebrow}</p>
        <h2 class="h1">{h}</h2>
        <p class="lead" style="max-width:54ch;margin:0 auto">{lead}</p>
        <div class="cta__actions">
          <a class="btn btn--primary btn--lg" href="{b1[1]}" data-magnetic><span class="btn__txt">{b1[0]}</span>{ARW}</a>
          <a class="btn btn--ghost btn--lg" href="{b2[1]}" data-magnetic><span class="btn__txt">{b2[0]}</span></a>
        </div>
      </div>
    </div>
  </section>'''

def divider():
    return '  <div class="divider container" aria-hidden="true"></div>'

# ------------------------------------------------------------------ shell
def nav_html(active):
    return "\n".join('      <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else '', n)
                     for h, n in NAV)

def drawer_html():
    return "\n".join('  <a href="%s"><span>%02d</span> %s</a>' % (h, i + 1, n)
                     for i, (h, n) in enumerate(DRAWER))

FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="index.html" aria-label="Rewind Dynamics — home">
          <img class="brand__mark" src="assets/img/logo-mark.svg" alt="">
          <span class="brand__word"><b>Rewind</b><span>Dynamics</span></span>
        </a>
        <p>A global defence-technology company developing autonomous systems — unmanned aerial, precision-guided and tactical platforms — for defence and military applications.</p>
        <div class="footer__social">
          <a href="mailto:info@rewinddynamics.com" aria-label="Email" title="Email"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M4 7.5l8 5.5 8-5.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></a>
        </div>
        <p class="footer__loc mono">Global operations</p>
      </div>
      <div class="footer__col"><h4>Systems</h4><a href="systems.html">All Systems</a><a href="uav.html">Unmanned Aerial</a><a href="precision-guidance.html">Precision Guidance</a><a href="tactical.html">Tactical Miniature</a><a href="swarming.html">Swarm Autonomy</a></div>
      <div class="footer__col"><h4>Capabilities</h4><a href="capabilities.html">Overview</a><a href="autonomy.html">Autonomy</a><a href="perception.html">Perception</a><a href="edge-ai.html">Edge AI</a><a href="navigation.html">Navigation</a><a href="systems-engineering.html">Systems Engineering</a><a href="simulation.html">Simulation &amp; Test</a></div>
      <div class="footer__col"><h4>Applications</h4><a href="applications.html">Overview</a><a href="isr.html">ISR</a><a href="force-protection.html">Force Protection</a><a href="counter-uas.html">Counter-UAS</a><a href="technology.html">Technology</a><a href="research.html">Research</a></div>
      <div class="footer__col"><h4>Company</h4><a href="about.html">About</a><a href="timeline.html">Timeline</a><a href="locations.html">Locations</a><a href="governance.html">Governance</a><a href="investors.html">Investors</a><a href="careers.html">Careers</a></div>
      <div class="footer__col"><h4>Responsibility</h4><a href="responsibility.html">Responsible Autonomy</a><a href="ethics.html">Ethics &amp; Conduct</a><a href="human-rights.html">Human Rights</a><a href="sustainability.html">Sustainability</a><a href="security-compliance.html">Security &amp; Compliance</a><a href="quality.html">Quality &amp; Assurance</a></div>
      <div class="footer__col"><h4>Connect</h4><a href="contact.html">Contact</a><a href="partners.html">Partners</a><a href="suppliers.html">Suppliers</a><a href="newsroom.html">Newsroom</a><a href="insights.html">Insights</a><a href="glossary.html">Glossary</a><a href="press.html">Press</a><a href="faq.html">FAQ</a></div>
    </div>
  </div>
  <div class="footer__watermark" aria-hidden="true">REWIND</div>
  <div class="container">
    <div class="footer__bar">
      <span>© 2020–<span data-year>2026</span> Rewind Dynamics. All rights reserved.</span>
      <div class="footer__legal"><a href="privacy.html">Privacy</a><a href="privacy.html#terms">Terms</a><a href="accessibility.html">Accessibility</a><a href="search.html">Search</a><a href="site-map.html">Site Map</a></div>
    </div>
  </div>
</footer>'''

def build(fn, title, desc, crumbs, hero, sections, extra_ld=None, active=None):
    et, ed = esc(title), esc(desc)
    url = BASE + fn
    bc = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                     "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                          **({"item": u} if u else {})}
                                         for i, (n, u) in enumerate(crumbs)]}, ensure_ascii=False)
    wp = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage",
        "url": url, "name": title, "description": desc, "inLanguage": "en",
        "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#organization"},
        "publisher": {"@id": BASE + "#organization"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "assets/img/og.png"}},
        ensure_ascii=False)
    ws = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "#website",
        "name": "Rewind Dynamics", "url": BASE, "inLanguage": "en",
        "publisher": {"@id": BASE + "#organization"}}, ensure_ascii=False)
    lds = ('<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>\n'
           '<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
           % (ORG, bc, wp, ws))
    if extra_ld:
        lds += '\n<script type="application/ld+json">%s</script>' % extra_ld
    crumb_html = ""
    for i, (n, u) in enumerate(crumbs):
        if i: crumb_html += '<span class="sep">/</span>'
        last = i == len(crumbs) - 1
        crumb_html += ('<span>%s</span>' % n) if last or not u else \
                      ('<a href="%s">%s</a>' % (u.replace(BASE, "") or "index.html", n))
    body = "\n\n".join(sections)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{et}</title>
<meta name="description" content="{ed}">
<meta name="theme-color" content="#06080C">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<!-- seo:rd -->
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="Rewind Dynamics">
<meta property="og:site_name" content="Rewind Dynamics">
<meta property="og:locale" content="en">
<meta property="og:type" content="website">
<meta property="og:title" content="{et}">
<meta property="og:description" content="{ed}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://rewinddynamics.com/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rewind Dynamics — autonomous systems for defence">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{et}">
<meta name="twitter:description" content="{ed}">
<meta name="twitter:image" content="https://rewinddynamics.com/assets/img/og.png">
{lds}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="curtain" aria-hidden="true"></div>
<div class="grid-bg" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="brand" href="index.html" aria-label="Rewind Dynamics — home">
      <img class="brand__mark" src="assets/img/logo-mark.svg" alt="">
      <span class="brand__word"><b>Rewind</b><span>Dynamics</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
{nav_html(active)}
    </nav>
    <div class="nav__cta">
      <a class="btn btn--sm" href="contact.html" data-magnetic><span class="btn__txt">Contact</span></a>
      <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
{drawer_html()}
</div>

<main class="page-wrap" id="main">

  <section class="phero">
    <div class="wm wm--phero" aria-hidden="true"><img src="assets/img/watermark.svg" alt=""></div>
    <div class="phero__bg" aria-hidden="true"></div>
    <div class="phero__grid" aria-hidden="true"></div>
    <div class="container phero__in">
      <nav class="crumbs" aria-label="Breadcrumb">{crumb_html}</nav>
      <p class="eyebrow" data-enter="1">{hero["eyebrow"]}</p>
      <h1 class="display" data-enter="2" style="font-size:clamp(2.3rem,6.2vw,4.9rem)">{hero["h1"]}</h1>
      <p class="lead" data-enter="3">{hero["lead"]}</p>
    </div>
  </section>

{body}

</main>

{FOOTER}

<script src="assets/js/app.js"></script>
<script src="assets/js/form.js"></script>
</body>
</html>
'''


# ------------------------------------------------------------------ articles
def build_article(fn, title, desc, category, date_iso, date_human, h1, lead,
                  prose, related, cta, keywords=None, active="newsroom.html",
                  crumb_parent=("Newsroom", "newsroom.html")):
    """Long-form feature article with Article structured data."""
    et, ed = esc(title), esc(desc)
    url = BASE + fn
    parent_name, parent_file = crumb_parent
    bc = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": parent_name, "item": BASE + parent_file},
        {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}, ensure_ascii=False)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1,
           "description": desc, "datePublished": date_iso, "dateModified": "2026-08-10",
           "image": ["https://rewinddynamics.com/assets/img/og.png"],
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
           "inLanguage": "en", "articleSection": category,
           "author": {"@type": "Organization", "name": "Rewind Dynamics", "url": BASE},
           "publisher": {"@id": "https://rewinddynamics.com/#organization"},
           "isPartOf": {"@type": "WebSite", "name": "Rewind Dynamics", "url": BASE}}
    if keywords: art["keywords"] = ", ".join(keywords)
    lds = ('<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>\n'
           '<script type="application/ld+json">%s</script>'
           % (ORG, bc, json.dumps(art, ensure_ascii=False)))
    rel = "".join(
        f'<a class="card reveal" data-d="{i+1}" href="{h}"><span class="card__idx">{i+1:02d}</span>'
        f'<h3 style="margin-top:14px">{t}</h3><p>{d}</p></a>' for i, (t, h, d) in enumerate(related))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{et}</title>
<meta name="description" content="{ed}">
<meta name="theme-color" content="#06080C">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<!-- seo:rd -->
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="Rewind Dynamics">
<meta property="og:site_name" content="Rewind Dynamics">
<meta property="og:locale" content="en">
<meta property="og:type" content="article">
<meta property="article:published_time" content="{date_iso}">
<meta property="article:modified_time" content="2026-08-10">
<meta property="article:section" content="{esc(category)}">
<meta property="og:title" content="{et}">
<meta property="og:description" content="{ed}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://rewinddynamics.com/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rewind Dynamics — autonomous systems for defence">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{et}">
<meta name="twitter:description" content="{ed}">
<meta name="twitter:image" content="https://rewinddynamics.com/assets/img/og.png">
{lds}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="curtain" aria-hidden="true"></div>
<div class="grid-bg" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<header class="nav" id="nav">
  <div class="nav__inner">
    <a class="brand" href="index.html" aria-label="Rewind Dynamics — home">
      <img class="brand__mark" src="assets/img/logo-mark.svg" alt="">
      <span class="brand__word"><b>Rewind</b><span>Dynamics</span></span>
    </a>
    <nav class="nav__links" aria-label="Primary">
{nav_html(active)}
    </nav>
    <div class="nav__cta">
      <a class="btn btn--sm" href="contact.html" data-magnetic><span class="btn__txt">Contact</span></a>
      <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
{drawer_html()}
</div>

<main class="page-wrap" id="main">
  <section class="phero" style="padding-bottom:0">
    <div class="wm wm--phero" aria-hidden="true"><img src="assets/img/watermark.svg" alt=""></div>
    <div class="phero__bg" aria-hidden="true"></div>
    <div class="phero__grid" aria-hidden="true"></div>
    <div class="container phero__in">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span class="sep">/</span><a href="{parent_file}">{parent_name}</a><span class="sep">/</span><span>Feature</span></nav>
      <div class="article article__head" data-enter="2" style="margin-bottom:0">
        <div class="article__meta"><span class="cat">{category}</span><span>{date_human}</span></div>
        <h1 class="article__title">{h1}</h1>
        <p class="article__lead">{lead}</p>
      </div>
    </div>
  </section>
  <section class="section" style="padding-top:clamp(40px,6vw,72px)">
    <div class="container">
      <div class="article">
        <div class="article__cover reveal"><div class="sch"></div><img src="assets/img/logo-mark.svg" alt=""></div>
        <div class="prose reveal">
{prose}
        </div>
        <div class="article__foot">
          <span class="article__sign">&mdash; Rewind Dynamics &middot; {category}</span>
          <a class="link-arrow" href="{parent_file}">Back to {parent_name}
            {LARW}</a>
        </div>
      </div>
    </div>
  </section>
  <section class="section--tight">
    <div class="container">
      <div class="shead"><div class="shead__l"><p class="eyebrow reveal">Explore Further</p>
        <h2 class="h2 reveal" data-d="1">Related reading.</h2></div></div>
      <div class="grid cards">{rel}
      </div>
    </div>
  </section>
{cta}
</main>

{FOOTER}

<script src="assets/js/app.js"></script>
<script src="assets/js/form.js"></script>
</body>
</html>
'''
