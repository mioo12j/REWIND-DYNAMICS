#!/usr/bin/env python3
"""Submit every indexable URL to IndexNow.

IndexNow is an open protocol supported by Bing, Yandex, Seznam and Naver.
One POST tells all of them a set of URLs is new or changed, and they crawl
far sooner than they would on their own schedule.

Google does NOT participate in IndexNow — for Google use Search Console's
URL Inspection -> Request Indexing. But Bing matters on its own terms, and
Bing's index is what several AI answer engines read from.

    python3 tools/indexnow.py           # submit everything
    python3 tools/indexnow.py uav.html  # submit specific pages
"""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
HOST = "rewinddynamics.com"
KEY = "806b5b14b2b143ec83e5326b8970c382"

def indexable():
    out = []
    for f in sorted(glob.glob("*.html")):
        if re.search(r'content="noindex', open(f, encoding="utf-8").read()):
            continue
        out.append("https://%s/%s" % (HOST, "" if f == "index.html" else f))
    return out

def main():
    args = sys.argv[1:]
    urls = ["https://%s/%s" % (HOST, "" if a == "index.html" else a) for a in args] if args else indexable()
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls,
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    print("Submitting %d URLs to IndexNow..." % len(urls))
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("HTTP", r.status, "-", "accepted" if r.status in (200, 202) else r.read()[:200])
    except Exception as e:
        print("Submission failed:", e)
        print("Run this from a machine with outbound internet access.")
        return 1
    return 0

sys.exit(main())
