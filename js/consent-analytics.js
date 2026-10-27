/* Consent gated Google Analytics 4 loader for Smart Tire Picks. Inactive until GA_ID is set.
   Nothing loads from Google and no cookie is set until the visitor clicks Accept. Choice stored in localStorage. */
(function () {
  var GA_ID = ""; // set to the G- measurement ID once Joshua provides it; empty = disabled
  if (!GA_ID) return;
  var KEY = "stp_analytics_consent";
  function load() {
    var s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", GA_ID, { anonymize_ip: true, allow_google_signals: false, allow_ad_personalization_signals: false });
  }
  var c = null; try { c = localStorage.getItem(KEY); } catch (e) {}
  if (c === "yes") return load();
  if (c === "no") return;
  var b = document.createElement("div");
  b.setAttribute("role", "dialog"); b.setAttribute("aria-label", "Analytics consent");
  b.style.cssText = "position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;background:#fff;border:1px solid #ccc;border-radius:8px;padding:12px 14px;box-shadow:0 2px 12px rgba(0,0,0,.15);font:14px/1.4 system-ui,sans-serif;max-width:640px;margin:0 auto";
  b.innerHTML = 'May we use Google Analytics cookies to understand how visitors use this site? <a href="/privacy/#google-analytics">Privacy Policy</a> <span style="display:inline-flex;gap:8px;margin-left:8px"><button type="button" data-v="yes">Accept</button><button type="button" data-v="no">Decline</button></span>';
  b.addEventListener("click", function (e) {
    var v = e.target.getAttribute && e.target.getAttribute("data-v"); if (!v) return;
    try { localStorage.setItem(KEY, v); } catch (x) {}
    b.remove(); if (v === "yes") load();
  });
  (document.body ? Promise.resolve() : new Promise(function (r) { document.addEventListener("DOMContentLoaded", r); })).then(function () { document.body.appendChild(b); });
})();
