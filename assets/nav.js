(function () {
  var btn = document.querySelector(".mobile-menu-toggle");
  var menu = document.getElementById("mobileMenu");
  if (!btn || !menu) return;

  btn.addEventListener("click", function () {
    var open = menu.classList.toggle("active");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      var nav = document.querySelector(".navbar");
      if (nav) nav.classList.remove("navbar--scroll-hidden");
    }
  });

  menu.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      menu.classList.remove("active");
      btn.setAttribute("aria-expanded", "false");
    });
  });
})();

(function () {
  var nav = document.querySelector(".navbar");
  if (!nav) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var menu = document.getElementById("mobileMenu");
  var lastY = window.scrollY || 0;
  var ticking = false;
  var topRevealPx = 56;
  var deltaPx = 10;

  function update() {
    ticking = false;
    var y = window.scrollY || 0;

    if (menu && menu.classList.contains("active")) {
      nav.classList.remove("navbar--scroll-hidden");
      lastY = y;
      return;
    }

    if (y < topRevealPx) {
      nav.classList.remove("navbar--scroll-hidden");
    } else if (y > lastY + deltaPx) {
      nav.classList.add("navbar--scroll-hidden");
    } else if (y < lastY - deltaPx) {
      nav.classList.remove("navbar--scroll-hidden");
    }

    lastY = y;
  }

  window.addEventListener(
    "scroll",
    function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    },
    { passive: true }
  );
})();
