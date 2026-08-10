#!/usr/bin/env python3
"""Rewind Dynamics — site auditor.

Checks structure, SEO, structured data, links and accessibility across the
static site. Run from the repository root:  python3 tools/audit.py
Exits non-zero if any ERROR-level problem is found.
"""
import glob, json, os, re, sys
from collections import defaultdict

BASE = "https://rewinddynamics.com/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

errors, warnings = [], []
def err(f, m): errors.append((f, m))
def warn(f, m): warnings.append((f, m))

pages = sorted(glob.glob("*.html"))
docs = {f: open(f, encoding="utf-8").read() for f in pages}

def one(pat, s, flags=re.S):
    m = re.search(pat, s, flags)
    return m.group(1).strip() if m else None

def noindex(s):
    r = one(r'<meta name="robots" content="([^"]*)"', s) or ""
    return "noindex" in r

indexable = [f for f in pages if not noindex(docs[f])]

# ---------------------------------------------------------------- per page
titles, descs = defaultdict(list), defaultdict(list)
for f in pages:
    s = docs[f]

    if not re.search(r'<html lang="en"', s): err(f, "missing <html lang>")
    if 'name="viewport"' not in s: err(f, "missing viewport meta")
    if "<!DOCTYPE html>" not in s: err(f, "missing doctype")

    t = one(r"<title>(.*?)</title>", s)
    d = one(r'<meta name="description" content="(.*?)">', s)
    if not t: err(f, "missing <title>")
    else:
        titles[t].append(f)
        if len(t) > 70: warn(f, f"title {len(t)} chars (Google truncates ~60-70)")
        if len(t) < 15: warn(f, f"title very short ({len(t)})")
    if not d: err(f, "missing meta description")
    else:
        descs[d].append(f)
        if len(d) < 70: warn(f, f"description short ({len(d)} chars)")
        if len(d) > 320: warn(f, f"description very long ({len(d)} chars)")

    # headings
    h1s = re.findall(r"<h1[ >]", s)
    if len(h1s) != 1: err(f, f"{len(h1s)} <h1> tags (need exactly 1)")

    # canonical
    can = one(r'<link rel="canonical" href="([^"]*)"', s)
    if not noindex(f in docs and s):
        pass
    if not can:
        if not noindex(s): err(f, "missing canonical")
    else:
        expect = BASE if f == "index.html" else BASE + f
        if can != expect: err(f, f"canonical {can} != {expect}")

    # social tags
    if not noindex(s):
        for tag in ['property="og:title"', 'property="og:description"',
                    'property="og:url"', 'property="og:image"',
                    'name="twitter:card"', 'name="twitter:title"']:
            if tag not in s: err(f, f"missing {tag}")
        ogurl = one(r'<meta property="og:url" content="([^"]*)"', s)
        expect = BASE if f == "index.html" else BASE + f
        if ogurl and ogurl != expect: err(f, f"og:url {ogurl} != {expect}")

    # images need alt (empty alt is fine = decorative)
    for img in re.findall(r"<img\b[^>]*>", s):
        if "alt=" not in img: err(f, "img without alt: " + img[:70])

    # JSON-LD
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    for i, b in enumerate(blocks):
        try:
            data = json.loads(b)
        except Exception as e:
            err(f, f"JSON-LD #{i} invalid: {e}")
            continue
        for node in (data if isinstance(data, list) else [data]):
            if not isinstance(node, dict): continue
            if "@context" not in node: err(f, f"JSON-LD #{i} missing @context")
            typ = node.get("@type")
            if typ == "BreadcrumbList":
                items = node.get("itemListElement", [])
                if not items: err(f, "empty BreadcrumbList")
                for n, it in enumerate(items, 1):
                    if it.get("position") != n: err(f, "breadcrumb position out of order")
            if typ in ("NewsArticle", "Article", "TechArticle"):
                for k in ("headline", "datePublished", "author", "publisher", "mainEntityOfPage"):
                    if k not in node: err(f, f"{typ} missing {k}")
                hl = node.get("headline", "")
                if len(hl) > 110: warn(f, f"{typ} headline >110 chars")
    if not noindex(s) and not any('"BreadcrumbList"' in b for b in blocks) and f != "index.html":
        warn(f, "no BreadcrumbList schema")

# duplicates
for t, fs in titles.items():
    if len(fs) > 1: err(fs[0], f"duplicate title across {fs}")
for d, fs in descs.items():
    if len(fs) > 1: err(fs[0], f"duplicate description across {fs}")

# ---------------------------------------------------------------- links
ids = {f: set(re.findall(r'\sid="([^"]+)"', docs[f])) for f in pages}
for f in pages:
    for href in re.findall(r'href="([^"]+)"', docs[f]):
        if href.startswith(("http", "mailto:", "tel:", "data:")): continue
        tgt, _, frag = href.partition("#")
        if tgt.startswith("assets/"):
            if not os.path.exists(tgt): err(f, f"missing asset {tgt}")
            continue
        if tgt == "":
            if frag and frag not in ids[f]: err(f, f"dead in-page anchor #{frag}")
            continue
        if not tgt.endswith(".html"):
            if not os.path.exists(tgt): err(f, f"missing file {tgt}")
            continue
        if tgt not in pages: err(f, f"broken link -> {href}")
        elif frag and frag not in ids[tgt]: err(f, f"dead anchor {href}")
    for src in re.findall(r'<(?:img|script)[^>]+src="([^"]+)"', docs[f]):
        if src.startswith(("http", "data:")): continue
        if not os.path.exists(src): err(f, f"missing src {src}")
    for hr in re.findall(r'<link[^>]+href="([^"]+)"', docs[f]):
        if hr.startswith(("http", "data:")): continue
        if not os.path.exists(hr): err(f, f"missing linked file {hr}")

# ---------------------------------------------------------------- sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
if len(locs) != len(set(locs)): err("sitemap.xml", "duplicate <loc> entries")
for f in indexable:
    u = BASE if f == "index.html" else BASE + f
    if u not in locs: err("sitemap.xml", f"missing {u}")
for u in locs:
    name = u.replace(BASE, "") or "index.html"
    if name not in pages: err("sitemap.xml", f"lists non-existent {u}")
    elif noindex(docs[name]): err("sitemap.xml", f"lists noindex page {u}")

# ---------------------------------------------------------------- robots
rb = open("robots.txt", encoding="utf-8").read()
if "Sitemap:" not in rb: err("robots.txt", "no Sitemap directive")
if re.search(r"^Disallow: /$", rb, re.M): err("robots.txt", "blanket Disallow: /")

# ---------------------------------------------------------------- nav/footer consistency
navsets = defaultdict(list)
for f in pages:
    m = re.search(r'<nav class="nav__links".*?</nav>', docs[f], re.S)
    if m:
        navsets[tuple(re.findall(r'href="([^"]+)"', m.group(0)))].append(f)
if len(navsets) > 1:
    err("nav", f"inconsistent primary nav across pages: {[v[:3] for v in navsets.values()]}")


# ---------------------------------------------------------------- orphans & depth
inbound = defaultdict(set)
for f in pages:
    body = re.sub(r"<footer.*?</footer>", "", docs[f], flags=re.S)   # footer links don't count as editorial
    for href in re.findall(r'href="([^"]+)"', body):
        t = href.split("#")[0]
        if t.endswith(".html") and t in pages and t != f:
            inbound[t].add(f)
for f in indexable:
    if f == "index.html": continue
    if not inbound[f]:
        err(f, "ORPHAN: no in-content link from any other page (footer-only)")
    elif len(inbound[f]) == 1 and list(inbound[f])[0] == f:
        warn(f, "only self-linked")

# ---------------------------------------------------------------- headings order
for f in pages:
    main = re.sub(r"<footer.*?</footer>|<header.*?</header>", "", docs[f], flags=re.S)
    lv = [int(m) for m in re.findall(r"<h([1-4])[ >]", main)]
    prev = 0
    for n in lv:
        if prev and n > prev + 1:
            warn(f, f"heading jumps h{prev} -> h{n}")
            break
        prev = n

# ---------------------------------------------------------------- thin content
for f in indexable:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", docs[f], flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    words = len(re.sub(r"\s+", " ", text).split())
    if words < 320: warn(f, f"thin content (~{words} words)")

# ---------------------------------------------------------------- duplicate H1 text
h1s = defaultdict(list)
for f in pages:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", docs[f], re.S)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        h1s[t].append(f)
for t, fs in h1s.items():
    if len(fs) > 1: warn(fs[0], f"duplicate H1 text '{t}' on {fs}")

# ---------------------------------------------------------------- report
print(f"Pages: {len(pages)}  (indexable {len(indexable)}, noindex {len(pages)-len(indexable)})")
print(f"Sitemap URLs: {len(locs)}")
print("-" * 62)
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for f, m in warnings: print(f"  ~ {f}: {m}")
if errors:
    print(f"ERRORS ({len(errors)}):")
    for f, m in errors: print(f"  ! {f}: {m}")
    print("-" * 62); print("FAILED")
    sys.exit(1)
print("-" * 62); print("ALL CHECKS PASSED")
