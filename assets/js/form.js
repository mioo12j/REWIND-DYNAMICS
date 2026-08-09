/* ============================================================
   REWIND DYNAMICS — Form handling
   Sends submissions to your inbox.

   HOW EMAIL DELIVERY WORKS
   ------------------------------------------------------------
   Forms POST to Web3Forms (https://web3forms.com) — a free,
   no-backend relay that emails every submission to your address.

   SETUP (2 minutes):
     1. Go to https://web3forms.com
     2. Enter  info@rewinddynamics.com  and get a free Access Key
     3. Paste that key into ACCESS_KEY below
     4. Deploy. Every submission now lands in that inbox.

   Until a real key is set, the form gracefully falls back to
   opening the visitor's email client addressed to CONTACT_EMAIL,
   so the site is fully functional out of the box.
   ============================================================ */
(function () {
  "use strict";

  var ACCESS_KEY   = "YOUR_WEB3FORMS_ACCESS_KEY"; // <-- paste your Web3Forms key here
  var CONTACT_EMAIL = "info@rewinddynamics.com";
  var ENDPOINT      = "https://api.web3forms.com/submit";

  var forms = document.querySelectorAll("form[data-rd-form]");
  if (!forms.length) return;

  function setStatus(box, type, msg) {
    if (!box) return;
    box.className = "form-status show " + type;
    box.innerHTML = (type === "ok"
      ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 8v5M12 16.5v.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/></svg>'
    ) + "<span>" + msg + "</span>";
  }

  function validate(form) {
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (el) {
      var field = el.closest(".field") || el.closest(".consent");
      var valid = true;
      if (el.type === "checkbox") valid = el.checked;
      else if (el.type === "email") valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim());
      else valid = el.value.trim().length > 1;
      if (field) field.classList.toggle("invalid", !valid);
      if (!valid && ok) { try { el.focus(); } catch (e) {} }
      if (!valid) ok = false;
    });
    return ok;
  }

  function formEmail(form) {
    return form.getAttribute("data-email") || CONTACT_EMAIL;
  }

  function mailtoFallback(form, data) {
    var subject = encodeURIComponent((form.getAttribute("data-subject") || "Website enquiry") + " — Rewind Dynamics");
    var lines = [];
    Object.keys(data).forEach(function (k) {
      if (["access_key", "botcheck", "subject", "from_name"].indexOf(k) > -1) return;
      lines.push(k.replace(/_/g, " ").toUpperCase() + ":\n" + data[k] + "\n");
    });
    var body = encodeURIComponent(lines.join("\n"));
    window.location.href = "mailto:" + formEmail(form) + "?subject=" + subject + "&body=" + body;
  }

  forms.forEach(function (form) {
    // clear invalid state as the user types
    form.querySelectorAll("input, textarea, select").forEach(function (el) {
      el.addEventListener("input", function () {
        var f = el.closest(".field") || el.closest(".consent");
        if (f) f.classList.remove("invalid");
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector("[type=submit]");

      // honeypot
      var hp = form.querySelector('input[name="botcheck"]');
      if (hp && hp.checked) return;

      if (!validate(form)) {
        setStatus(status, "err", "Please complete the highlighted fields.");
        return;
      }

      var fd = new FormData(form);
      var data = {};
      fd.forEach(function (v, k) { data[k] = v; });
      data.access_key = ACCESS_KEY;
      data.subject = (form.getAttribute("data-subject") || "New enquiry") + " — Rewind Dynamics";
      data.from_name = "Rewind Dynamics Website";

      // No real key configured -> use mailto so the form still works.
      if (!ACCESS_KEY || ACCESS_KEY === "YOUR_WEB3FORMS_ACCESS_KEY") {
        setStatus(status, "ok", "Opening your email client to send this securely…");
        mailtoFallback(form, data);
        return;
      }

      if (btn) { btn.classList.add("loading"); }
      setStatus(status, "ok", "Transmitting…");

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          if (btn) btn.classList.remove("loading");
          if (json.success) {
            form.reset();
            setStatus(status, "ok", "Transmission received. Our team will be in contact.");
          } else {
            setStatus(status, "err", json.message || "Something went wrong. Please email " + formEmail(form) + ".");
          }
        })
        .catch(function () {
          if (btn) btn.classList.remove("loading");
          setStatus(status, "err", "Network error. Please email " + formEmail(form) + " directly.");
        });
    });
  });
})();
