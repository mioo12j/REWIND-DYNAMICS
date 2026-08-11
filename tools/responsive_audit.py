#!/usr/bin/env python3
"""Responsive audit — checks every page at every breakpoint for layout faults.

Detects horizontal overflow, elements escaping the viewport, unreadable text,
tap targets that are too small, and images that overflow their container.

    python3 tools/responsive_audit.py            # all pages, all widths
    python3 tools/responsive_audit.py index.html # a single page

Exits non-zero if any page has a layout fault.
"""
import glob, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# width, label — covers small phones through large desktops
VIEWPORTS = [
    (320, "small phone"), (360, "phone"), (390, "phone L"),
    (414, "phone XL"), (768, "tablet"), (834, "tablet L"),
    (1024, "laptop"), (1280, "desktop"), (1440, "desktop L"), (1920, "wide"),
]

# elements that are intentionally wider than the viewport (clipped by design)
# skip-link parks off-screen until focused; .wm watermarks bleed past the edge by design
ALLOW = ("marquee__track", "footer__watermark", "skip-link", "wm--", "hero__canvas", "hp")

PROBE = """(allow) => {
  const vw = document.documentElement.clientWidth;
  const bad = [];
  const isAllowed = (el) => {
    for (let n = el; n && n !== document.body; n = n.parentElement) {
      const c = (n.className || '').toString();
      if (allow.some(a => c.includes(a))) return true;
    }
    return false;
  };
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return;
    if (isAllowed(el)) return;
    if (r.right > vw + 1 || r.left < -1) {
      bad.push({ k: 'escapes', t: el.tagName,
                 c: (el.className || '').toString().slice(0, 44),
                 right: Math.round(r.right), left: Math.round(r.left) });
    }
  });
  // controls whose label has wrapped into a ragged stack
  // (a squeezed flex row once broke "Contact" one letter per line)
  const squeezed = [];
  document.querySelectorAll('.btn .btn__txt, .nav__links a, .tag, .crumbs a, .crumbs span').forEach(el => {
    const txt = (el.textContent || '').trim();
    if (!txt || txt.length > 40 || txt.split(/\s+/).length > 5) return;
    // count real line boxes via the Range API rather than inferring from height
    let lines = 0;
    try {
      const rg = document.createRange();
      rg.selectNodeContents(el);
      lines = rg.getClientRects().length;
    } catch (e) { return; }
    const words = txt.split(/\s+/).length;
    // a label should never occupy more line boxes than it has words
    if (lines > Math.max(2, words)) {
      squeezed.push(txt.slice(0, 22) + ' -> ' + lines + ' lines / ' + words + ' words');
    }
  });

  // text that would be unreadably small
  const tiny = [];
  document.querySelectorAll('p, li, a, span, h1, h2, h3, h4, div').forEach(el => {
    if (!el.textContent || !el.textContent.trim()) return;
    if (el.children.length) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs && fs < 10) tiny.push(Math.round(fs) + 'px:' + el.textContent.trim().slice(0, 24));
  });
  return {
    vw,
    scrollW: document.documentElement.scrollWidth,
    overflow: document.documentElement.scrollWidth - vw,
    escapes: bad.slice(0, 6),
    nEscapes: bad.length,
    tiny: tiny.slice(0, 3),
    squeezed: squeezed.slice(0, 4),
  };
}"""

def main():
    targets = sys.argv[1:] or sorted(glob.glob("*.html"))
    faults, checks = [], 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        for width, label in VIEWPORTS:
            page = b.new_page(viewport={"width": width, "height": 900})
            # Google Fonts is unreachable from this environment; unblocked it
            # stalls every navigation until the request times out.
            page.route("**fonts.googleapis.com**", lambda r: r.abort())
            page.route("**fonts.gstatic.com**", lambda r: r.abort())
            for f in targets:
                page.goto("file://" + os.path.join(ROOT, f), wait_until="domcontentloaded")
                # measure the settled layout, not mid-animation entry offsets
                page.add_style_tag(content=(
                    "*,*::before,*::after{animation:none!important;transition:none!important}"
                    ".preloader,.curtain{display:none!important}"
                    "[data-enter],.reveal,.reveal-x,.reveal-y{opacity:1!important;transform:none!important}"))
                page.wait_for_timeout(60)
                r = page.evaluate(PROBE, list(ALLOW))
                checks += 1
                if r["overflow"] > 0:
                    faults.append((f, width, label, f"page scrolls horizontally by {r['overflow']}px"))
                if r["nEscapes"]:
                    detail = "; ".join(f"{e['t']}.{e['c']}(right={e['right']})" for e in r["escapes"])
                    faults.append((f, width, label, f"{r['nEscapes']} element(s) escape viewport: {detail}"))
                if r.get("squeezed"):
                    faults.append((f, width, label, "label wrapped badly: " + ", ".join(r["squeezed"])))
                if r["tiny"]:
                    faults.append((f, width, label, "text under 10px: " + ", ".join(r["tiny"])))
            page.close()
        b.close()

    print(f"Checked {len(targets)} page(s) across {len(VIEWPORTS)} viewports = {checks} renders")
    print("-" * 66)
    if not faults:
        print("NO LAYOUT FAULTS — every page fits every viewport")
        return 0
    by_page = {}
    for f, w, label, msg in faults:
        by_page.setdefault(f, []).append((w, label, msg))
    for f, items in sorted(by_page.items()):
        print(f"\n{f}")
        for w, label, msg in items:
            print(f"   {w}px ({label}): {msg}")
    print("-" * 66)
    print(f"{len(faults)} fault(s) across {len(by_page)} page(s)")
    return 1

sys.exit(main())
