#!/usr/bin/env python3
"""Generate search-index.json from every indexable page."""
import glob, json, os, re, html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
idx=[]
for f in sorted(glob.glob('*.html')):
    s=open(f,encoding='utf-8').read()
    if 'content="noindex' in s or f=='search.html': continue
    title=re.search(r'<title>(.*?)</title>',s,re.S).group(1)
    title=html.unescape(title).split(' | ')[0].split(' — Rewind')[0]
    desc=re.search(r'<meta name="description" content="(.*?)">',s,re.S)
    desc=html.unescape(desc.group(1)) if desc else ''
    # a little body text for keyword matching
    body=re.sub(r'<(script|style|nav|header|footer|svg).*?</\1>',' ',s,flags=re.S)
    body=re.sub(r'<[^>]+>',' ',body); body=html.unescape(body)
    body=re.sub(r'\s+',' ',body).strip()[:600]
    # crude section label from the breadcrumb
    crumb=re.findall(r'<nav class="crumbs"[^>]*>(.*?)</nav>',s,re.S)
    sect=''
    if crumb:
        parts=re.findall(r'>([^<>]+)<',crumb[0])
        parts=[p.strip() for p in parts if p.strip() and p.strip()!='/']
        sect=parts[1] if len(parts)>2 else 'Company'
    url='/'+('' if f=='index.html' else f)
    idx.append({"t":title,"d":desc,"u":url,"s":sect,"b":body})
json.dump(idx, open('search-index.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
print("search-index.json:",len(idx),"pages,",round(os.path.getsize('search-index.json')/1024),"KB")
