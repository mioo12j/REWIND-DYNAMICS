/* ============================================================
   REWIND DYNAMICS — Form handling
   Delivers every submission to your inbox using FormSubmit
   (https://formsubmit.co) — a free relay that needs no API key
   and no signup.

   WHERE SUBMISSIONS GO
   ------------------------------------------------------------
   All forms (contact, careers, newsletter, investor) are emailed
   to TARGET_EMAIL below.

   FIRST-TIME ACTIVATION (one click, one time):
     1. Deploy the site.
     2. Submit any form once.
     3. FormSubmit emails TARGET_EMAIL a confirmation link — click it.
     4. From then on, every submission arrives in that inbox.

   To change where mail goes, edit TARGET_EMAIL.
   (Optional: once activated, FormSubmit gives you a random alias
   like formsubmit.co/xxxxxxxx that hides the address — paste that
   hash into ENDPOINT_BASE if you'd rather not expose the email.)
   ============================================================ */
(function () {
  "use strict";

  var TARGET_EMAIL   = "sid@siddhantkumar.in";
  var ENDPOINT_BASE  = "https://formsubmit.co/ajax/"; // + TARGET_EMAIL (or a hash)
  var ENDPOINT       = ENDPOINT_BASE + TARGET_EMAIL;

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

  function mailtoFallback(form, data) {
    var subject = encodeURIComponent(data._subject || "Website enquiry");
    var lines = [];
    Object.keys(data).forEach(function (k) {
      if (k.charAt(0) === "_" || ["botcheck"].indexOf(k) > -1) return;
      lines.push(k.replace(/_/g, " ").toUpperCase() + ":\n" + data[k] + "\n");
    });
    var body = encodeURIComponent(lines.join("\n"));
    window.location.href = "mailto:" + TARGET_EMAIL + "?subject=" + subject + "&body=" + body;
  }

  forms.forEach(function (form) {
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
      fd.forEach(function (v, k) { if (k !== "botcheck") data[k] = v; });

      // FormSubmit control fields
      data._subject  = (form.getAttribute("data-subject") || "New enquiry") + " — Rewind Dynamics website";
      data._template = "table";
      data._captcha  = "false";
      data._honey    = "";

      if (btn) btn.classList.add("loading");
      setStatus(status, "ok", "Sending…");

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function (json) {
          if (btn) btn.classList.remove("loading");
          var ok = json && (json.success === true || json.success === "true");
          if (ok) {
            form.reset();
            setStatus(status, "ok", "Message received. Thank you — we'll be in touch.");
          } else {
            setStatus(status, "err", (json && json.message) || "Couldn't send just now. Please email " + TARGET_EMAIL + ".");
          }
        })
        .catch(function () {
          if (btn) btn.classList.remove("loading");
          setStatus(status, "err", "Network error. Opening your email app instead…");
          mailtoFallback(form, data);
        });
    });
  });
})();
