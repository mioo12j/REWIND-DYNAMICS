#!/usr/bin/env python3
"""Generate sitemap.xml from the indexable pages on disk."""
import glob, os, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
BASE="https://rewinddynamics.com/"; LASTMOD="2026-08-30"

PRIORITY=[
 (r'^index\.html$', 1.0, 'weekly'),
 (r'^(systems|capabilities|applications|investors)\.html$', 0.9, 'monthly'),
 (r'^(uav|humanoid|tactical|isr|force-protection|counter-uas)\.html$', 0.9, 'monthly'),
 (r'^(about|technology|research|careers|contact)\.html$', 0.8, 'monthly'),
 (r'^(autonomy|perception|edge-ai|navigation|systems-engineering|swarming|simulation)\.html$', 0.8, 'monthly'),
 (r'^(partners|suppliers|security-compliance|quality|timeline)\.html$', 0.7, 'monthly'),
 (r'^(newsroom|insights)\.html$', 0.8, 'weekly'),
 (r'^(glossary|responsibility|faq|press)\.html$', 0.7, 'monthly'),
 (r'^insight-', 0.6, 'yearly'),
 (r'^news-', 0.5, 'yearly'),
]
def rank(f):
    for pat,pr,cf in PRIORITY:
        if re.match(pat,f): return pr,cf
    return 0.5,'monthly'

pages=[f for f in sorted(glob.glob('*.html'))
       if 'noindex' not in (re.search(r'<meta name="robots" content="([^"]*)"', open(f,encoding='utf-8').read()) or type('',(),{'group':lambda s,i:''})()).group(1)]
rows=[]
for f in sorted(pages, key=lambda x:(-rank(x)[0], x)):
    pr,cf=rank(f)
    loc=BASE if f=='index.html' else BASE+f
    if f=='index.html':
        rows.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{LASTMOD}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>
    <image:image><image:loc>{BASE}assets/img/og.png</image:loc>
      <image:title>Rewind Dynamics — autonomous systems for defence</image:title></image:image>
  </url>''')
    else:
        rows.append(f'  <url><loc>{loc}</loc><lastmod>{LASTMOD}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>')
out='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+"\n".join(rows)+'\n</urlset>\n'
open('sitemap.xml','w',encoding='utf-8').write(out)
print("sitemap.xml written with", len(rows), "URLs")
