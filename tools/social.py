#!/usr/bin/env python3
"""Wire social/company profiles into the site.

Two things happen when you fill PROFILES in below and run this:

  1. `sameAs` is added to the Organization schema on every page. This is the
     statement that links your website to your profiles elsewhere, and it is
     how Google confirms that a site and a company are the same entity. It is
     the single most valuable piece of markup you are currently missing.

  2. Icon links are added to the footer on every page.

IMPORTANT: only add a URL here once the profile actually exists and is public.
Pointing sameAs at a 404 is worse than leaving it out — Google follows these,
and a dead profile is a negative signal, not a neutral one.

    python3 tools/social.py --check   # show what is configured
    python3 tools/social.py           # apply to all pages
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ---------------------------------------------------------------------------
# FILL THESE IN. Leave a value as "" and it is skipped entirely.
# Order matters: put the most authoritative profile first.
# ---------------------------------------------------------------------------
PROFILES = [
    # key            url                                                    label
    ("linkedin",     "",  "LinkedIn"),
    ("crunchbase",   "",  "Crunchbase"),
    ("x",            "https://x.com/RewindDynamics",  "X"),
    ("youtube",      "",  "YouTube"),
    ("github",       "",  "GitHub"),
    ("instagram",    "https://www.instagram.com/rewinddynamics/",  "Instagram"),
]

ICONS = {
 "linkedin":  '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3zM10 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.07 1.4-2.07 2.85V21h-4z" fill="currentColor" stroke="none"/>',
 "crunchbase":'<rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="1.6"/><path d="M10.5 10.2a2.4 2.4 0 1 0 0 3.6M13.6 8v8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
 "x":         '<path d="M4 4l7.2 9.3L4.4 20h1.9l5.6-5.9 4.6 5.9H21l-7.5-9.7L20 4h-1.9l-5.2 5.5L8.6 4H4Z" fill="currentColor" stroke="none"/>',
 "youtube":   '<rect x="2.5" y="6" width="19" height="12" rx="3.4" stroke="currentColor" stroke-width="1.6"/><path d="M10.5 9.8v4.4L14.4 12z" fill="currentColor" stroke="none"/>',
 "github":    '<path d="M12 2.6a9.4 9.4 0 0 0-3 18.3c.47.09.64-.2.64-.45v-1.6c-2.6.57-3.16-1.25-3.16-1.25-.43-1.1-1.05-1.39-1.05-1.39-.86-.58.07-.57.07-.57.95.07 1.45.98 1.45.98.84 1.45 2.22 1.03 2.76.79.08-.61.33-1.03.6-1.27-2.08-.24-4.26-1.04-4.26-4.63 0-1.02.36-1.86.96-2.51-.1-.24-.42-1.2.09-2.5 0 0 .79-.25 2.58.96a8.9 8.9 0 0 1 4.7 0c1.79-1.21 2.577-.96 2.577-.96.51 1.3.19 2.26.1 2.5.6.65.95 1.49.95 2.51 0 3.6-2.19 4.39-4.27 4.62.34.29.64.87.64 1.75v2.6c0 .25.17.55.65.45A9.4 9.4 0 0 0 12 2.6Z" fill="currentColor" stroke="none"/>',
 "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/>',
}

EMAIL_LINK = ('<a href="mailto:info@rewinddynamics.com" aria-label="Email" title="Email">'
 '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="2" '
 'stroke="currentColor" stroke-width="1.6"/><path d="M4 7.5l8 5.5 8-5.5" stroke="currentColor" stroke-width="1.6" '
 'stroke-linecap="round"/></svg></a>')

def active():
    return [(k, u, lbl) for k, u, lbl in PROFILES if u.strip()]

def social_html(items):
    out = [EMAIL_LINK]
    for k, u, lbl in items:
        out.append(
            '<a href="%s" aria-label="%s" title="%s" rel="me noopener" target="_blank">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none">%s</svg></a>'
            % (u, lbl, lbl, ICONS.get(k, "")))
    return "".join(out)

def main():
    items = active()
    if "--check" in sys.argv:
        print("Configured profiles:", len(items))
        for k, u, lbl in items: print("  %-11s %s" % (lbl, u))
        if not items:
            print("  (none yet — fill PROFILES in tools/social.py)")
        return 0
    if not items:
        print("No profiles configured. Fill PROFILES in tools/social.py first.")
        print("Adding sameAs pointing at pages that do not exist would hurt, not help.")
        return 1

    same_as = json.dumps([u for _, u, _ in items], ensure_ascii=False)
    n_schema = n_footer = 0
    for f in sorted(glob.glob("*.html")):
        s = open(f, encoding="utf-8").read(); o = s

        # 1) sameAs into the Organization node (insert right after "url")
        if '"@type": "Organization"' in s and '"sameAs"' not in s:
            s = s.replace('"url": "https://rewinddynamics.com/", "logo"',
                          '"url": "https://rewinddynamics.com/", "sameAs": %s, "logo"' % same_as, 1)
            n_schema += 1
        elif '"sameAs"' in s:
            s = re.sub(r'"sameAs": \[[^\]]*\]', '"sameAs": %s' % same_as, s)

        # 2) footer icon row
        s2 = re.sub(r'<div class="footer__social">.*?</div>',
                    '<div class="footer__social">%s</div>' % social_html(items), s, count=1, flags=re.S)
        if s2 != s: n_footer += 1
        s = s2

        if s != o:
            open(f, "w", encoding="utf-8").write(s)

    print("sameAs added/updated on %d pages" % n_schema)
    print("footer links updated on %d pages" % n_footer)
    print("\nNow run:  python3 tools/audit.py")
    return 0

sys.exit(main())
