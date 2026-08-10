/* ============================================================
   REWIND DYNAMICS — Interaction + Animation Engine
   Vanilla JS. Progressive enhancement; no dependencies.
   ============================================================ */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Preloader ---------- */
  function preloader() {
    var pl = $(".preloader");
    if (!pl) { liftCurtain(); return; }
    var bar = $(".pl-bar span", pl), pct = $(".pl-pct", pl);
    var p = 0;
    if (reduceMotion) { finish(); return; }
    var t = setInterval(function () {
      p += Math.random() * 16 + 6;
      if (p >= 100) { p = 100; clearInterval(t); setTimeout(finish, 260); }
      if (bar) bar.style.width = p + "%";
      if (pct) pct.textContent = "LOADING · " + Math.floor(p).toString().padStart(3, "0") + "%";
    }, 130);
    function finish() {
      if (bar) bar.style.width = "100%";
      if (pct) pct.textContent = "READY";
      pl.classList.add("done");
      document.body.style.overflow = "";
      liftCurtain();
      window.dispatchEvent(new Event("rd:ready"));
    }
    document.body.style.overflow = "hidden";
  }
  function liftCurtain() {
    var c = $(".curtain");
    if (c) c.classList.add("lift");
  }

  /* ---------- Nav ---------- */
  function nav() {
    var n = $(".nav");
    if (!n) return;
    var onScroll = function () { n.classList.toggle("scrolled", window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    var burger = $(".burger"), drawer = $(".drawer");
    if (burger && drawer) {
      var toggle = function (force) {
        var open = force !== undefined ? force : !drawer.classList.contains("open");
        drawer.classList.toggle("open", open);
        burger.classList.toggle("open", open);
        burger.setAttribute("aria-expanded", String(open));
        document.body.style.overflow = open ? "hidden" : "";
      };
      burger.addEventListener("click", function () { toggle(); });
      $$(".drawer a").forEach(function (a) { a.addEventListener("click", function () { toggle(false); }); });
      window.addEventListener("keydown", function (e) { if (e.key === "Escape") toggle(false); });
    }
  }

  /* ---------- Scroll Reveal ---------- */
  function reveals() {
    var els = $$(".reveal, .reveal-x, .clip-up, .line-anim");
    if (!("IntersectionObserver" in window) || reduceMotion) {
      els.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Count-up stats ---------- */
  function counters() {
    var els = $$("[data-count]");
    if (!els.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; io.unobserve(el);
        var target = parseFloat(el.getAttribute("data-count"));
        var dec = (el.getAttribute("data-dec") | 0);
        var dur = 1500, start = performance.now();
        (function step(now) {
          var t = Math.min(1, (now - start) / dur);
          var e = 1 - Math.pow(1 - t, 3);
          el.textContent = (target * e).toFixed(dec);
          if (t < 1) requestAnimationFrame(step);
          else el.textContent = target.toFixed(dec);
        })(start);
      });
    }, { threshold: 0.5 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Text scramble ---------- */
  function scramble() {
    var els = $$("[data-scramble]");
    if (!els.length || reduceMotion) return;
    var chars = "!<>-_\\/[]{}—=+*^?#01";
    els.forEach(function (el) {
      var done = false;
      var run = function () {
        if (done) return; done = true;
        var text = el.getAttribute("data-scramble") || el.textContent;
        var q = [], frame = 0;
        for (var i = 0; i < text.length; i++) {
          var start = Math.floor(Math.random() * 18);
          var end = start + Math.floor(Math.random() * 22) + 12;
          q.push({ from: "", to: text[i], start: start, end: end, ch: "" });
        }
        (function tick() {
          var out = "", complete = 0;
          for (var i = 0; i < q.length; i++) {
            var o = q[i];
            if (frame >= o.end) { complete++; out += o.to; }
            else if (frame >= o.start) {
              if (!o.ch || Math.random() < 0.28) o.ch = chars[Math.floor(Math.random() * chars.length)];
              out += '<span class="scr">' + o.ch + "</span>";
            } else out += "";
          }
          el.innerHTML = out;
          if (complete !== q.length) { frame++; requestAnimationFrame(tick); }
          else el.textContent = text;
        })();
      };
      var io = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { run(); io.disconnect(); }
      }, { threshold: 0.6 });
      io.observe(el);
    });
  }

  /* ---------- Accordion ---------- */
  function accordion() {
    $$(".acc__item").forEach(function (item) {
      var head = $(".acc__head", item), panel = $(".acc__panel", item);
      if (!head || !panel) return;
      head.addEventListener("click", function () {
        var open = item.classList.contains("open");
        var siblings = $$(".acc__item", item.parentElement);
        siblings.forEach(function (s) {
          if (s !== item) { s.classList.remove("open"); var p = $(".acc__panel", s); if (p) p.style.height = "0px"; var h = $(".acc__head", s); if (h) h.setAttribute("aria-expanded", "false"); }
        });
        item.classList.toggle("open", !open);
        head.setAttribute("aria-expanded", String(!open));
        panel.style.height = open ? "0px" : panel.scrollHeight + "px";
      });
    });
  }

  /* ---------- Hero node network ---------- */
  function heroCanvas() {
    var cv = $(".hero__canvas");
    if (!cv) return;
    var ctx = cv.getContext("2d");
    var w, h, dpr, nodes = [], mouse = { x: -9999, y: -9999 };
    var COUNT, running = true;

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      COUNT = Math.max(28, Math.min(80, Math.floor((w * h) / 20000)));
      build();
    }
    function build() {
      nodes = [];
      for (var i = 0; i < COUNT; i++) {
        nodes.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
          r: Math.random() * 1.4 + 0.6
        });
      }
    }
    var LINK = 132;
    function frame() {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;
        // links
        for (var j = i + 1; j < nodes.length; j++) {
          var m = nodes[j], dx = n.x - m.x, dy = n.y - m.y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < LINK) {
            var a = (1 - d / LINK) * 0.5;
            ctx.strokeStyle = "rgba(47,123,255," + a + ")";
            ctx.lineWidth = 0.6;
            ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(m.x, m.y); ctx.stroke();
          }
        }
        // mouse pull
        var mdx = n.x - mouse.x, mdy = n.y - mouse.y, md = Math.sqrt(mdx * mdx + mdy * mdy);
        if (md < 160) {
          ctx.strokeStyle = "rgba(127,180,255," + (1 - md / 160) * 0.55 + ")";
          ctx.lineWidth = 0.7;
          ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
        }
        ctx.beginPath();
        ctx.fillStyle = "rgba(150,190,255,.8)";
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2); ctx.fill();
      }
      requestAnimationFrame(frame);
    }
    size();
    window.addEventListener("resize", size);
    var host = cv.parentElement || cv;
    host.addEventListener("mousemove", function (e) {
      var rect = cv.getBoundingClientRect();
      mouse.x = e.clientX - rect.left; mouse.y = e.clientY - rect.top;
    });
    host.addEventListener("mouseleave", function () { mouse.x = -9999; mouse.y = -9999; });
    document.addEventListener("visibilitychange", function () {
      running = !document.hidden; if (running) frame();
    });
    if (!reduceMotion) frame(); else { ctx.clearRect(0, 0, w, h); }
  }

  /* ---------- Magnetic buttons ---------- */
  function magnetic() {
    if (reduceMotion || window.matchMedia("(pointer: coarse)").matches) return;
    $$("[data-magnetic]").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var mx = e.clientX - r.left - r.width / 2, my = e.clientY - r.top - r.height / 2;
        el.style.transform = "translate(" + mx * 0.16 + "px," + my * 0.22 + "px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- Footer year ---------- */
  function year() { $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); }); }

  /* ---------- Init ---------- */

  /* ---------- Scroll progress rail ----------
     A hairline at the top of the viewport showing read position. */
  function scrollProgress() {
    if (reduceMotion) return;
    var bar = document.createElement("div");
    bar.className = "scroll-rail";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = "<span></span>";
    document.body.appendChild(bar);
    var fill = bar.firstChild, ticking = false;
    function update() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? (window.pageYOffset / h) : 0;
      fill.style.transform = "scaleX(" + Math.min(1, Math.max(0, pct)) + ")";
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Watermark parallax ----------
     Decorative monograms drift slightly against the scroll. */
  function parallax() {
    if (reduceMotion) return;
    var els = $$(".wm");
    if (!els.length) return;
    var ticking = false;
    function update() {
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var progress = (r.top + r.height / 2 - vh / 2) / vh;   // -1 .. 1
        el.style.setProperty("--wm-shift", (progress * -26).toFixed(1) + "px");
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update, { passive: true });
    update();
  }

  /* ---------- SVG line draw ----------
     Schematic strokes draw themselves in when scrolled into view. */
  function drawSVG() {
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    var targets = $$(".panel svg, .article__cover svg");
    if (!targets.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var strokes = e.target.querySelectorAll("path, line, polyline, circle, rect");
        Array.prototype.forEach.call(strokes, function (el, i) {
          var len;
          try { len = el.getTotalLength ? el.getTotalLength() : 0; } catch (err) { len = 0; }
          if (!len || len > 6000) return;
          el.style.strokeDasharray = len;
          el.style.strokeDashoffset = len;
          el.style.transition = "stroke-dashoffset 1.1s cubic-bezier(.16,1,.3,1) " + (i * 55) + "ms";
          requestAnimationFrame(function () { el.style.strokeDashoffset = "0"; });
        });
        io.unobserve(e.target);
      });
    }, { threshold: 0.25 });
    targets.forEach(function (t) { io.observe(t); });
  }

  /* ---------- Section index ----------
     The § markers tick up as their section becomes active. */
  function sectionMarkers() {
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    var marks = $$(".shead__index");
    if (!marks.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        e.target.classList.toggle("is-active", e.isIntersecting);
      });
    }, { threshold: 0.4, rootMargin: "0px 0px -30% 0px" });
    marks.forEach(function (m) { io.observe(m); });
  }

  function init() {
    preloader(); nav(); reveals(); counters(); scramble(); accordion(); heroCanvas(); magnetic(); year();
    scrollProgress(); parallax(); drawSVG(); sectionMarkers();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
