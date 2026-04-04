/**
 * Subtle section reveal on scroll (transform only — no opacity hide, avoids “loading” flash).
 * Near-viewport targets are marked visible immediately for LCP-friendly first paint.
 */
(function () {
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var ROOT_MARGIN = "0px 0px -8% 0px";
  var THRESH = 0.03;
  var VH_FRAC = 0.97;

  function mark(el) {
    el.classList.add("page-reveal-el--visible");
  }

  function collect() {
    var out = [];
    var seen = new Set();

    function add(el) {
      if (!el || seen.has(el)) return;
      seen.add(el);
      out.push(el);
    }

    var home = document.querySelector("main#main-content");
    if (home) {
      home.querySelectorAll(":scope > section.section").forEach(add);
    }

    var pm = document.querySelector("main.page-main");
    if (pm) {
      pm.querySelectorAll(":scope > .container.inner-block").forEach(function (block) {
        var directSections = block.querySelectorAll(":scope > section.section");
        if (directSections.length) {
          directSections.forEach(add);
        } else {
          add(block);
        }
      });
    }

    return out;
  }

  var targets = collect();
  if (!targets.length) return;

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        mark(e.target);
        io.unobserve(e.target);
      });
    },
    { root: null, rootMargin: ROOT_MARGIN, threshold: THRESH }
  );

  var vh = window.innerHeight;
  targets.forEach(function (el) {
    el.classList.add("page-reveal-el");
    var top = el.getBoundingClientRect().top;
    if (top < vh * VH_FRAC) {
      mark(el);
    } else {
      io.observe(el);
    }
  });
})();
