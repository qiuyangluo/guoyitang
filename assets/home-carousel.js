(function () {
  document.querySelectorAll("[data-clinic-carousel]").forEach(function (root) {
    var track = root.querySelector(".clinic-carousel__track");
    var slides = root.querySelectorAll(".clinic-carousel__slide");
    var dotsWrap = root.querySelector(".clinic-carousel__dots");
    var prev = root.querySelector(".clinic-carousel__nav--prev");
    var next = root.querySelector(".clinic-carousel__nav--next");
    if (!track || !slides.length) return;

    var index = 0;
    var isTriple = root.classList.contains("clinic-carousel--triple");
    var isEn =
      (document.documentElement.lang || "").toLowerCase().startsWith("en") ||
      location.pathname.indexOf("/en") === 0;

    function getVisible() {
      if (!isTriple) return 1;
      if (window.innerWidth <= 640) return 1;
      if (window.innerWidth <= 1024) return 2;
      return Math.min(3, slides.length);
    }

    function getMaxIndex() {
      var visible = getVisible();
      return Math.max(0, slides.length - visible);
    }

    function renderDots() {
      if (!dotsWrap) return;
      dotsWrap.innerHTML = "";
      var max = getMaxIndex();
      for (var i = 0; i <= max; i++) {
        var dot = document.createElement("button");
        dot.type = "button";
        dot.className = "clinic-carousel__dot" + (i === index ? " is-active" : "");
        dot.setAttribute(
          "aria-label",
          isEn ? "Slide " + (i + 1) : "第 " + (i + 1) + " 张"
        );
        (function (target) {
          dot.addEventListener("click", function () {
            index = target;
            update();
          });
        })(i);
        dotsWrap.appendChild(dot);
      }
    }

    function getTripleGap() {
      var styles = getComputedStyle(track);
      var gap = parseFloat(styles.columnGap);
      if (!gap || isNaN(gap)) gap = parseFloat(styles.gap);
      if (!gap || isNaN(gap)) gap = 6;
      return gap;
    }

    function getTripleMetrics() {
      var visible = getVisible();
      var gap = getTripleGap();
      var slideWidth = (root.clientWidth - gap * (visible - 1)) / visible;
      return { visible: visible, gap: gap, slideWidth: slideWidth, step: slideWidth + gap };
    }

    function layoutTripleSlides() {
      var metrics = getTripleMetrics();
      root.style.setProperty("--carousel-visible", String(metrics.visible));
      slides.forEach(function (slide) {
        slide.style.flexBasis = metrics.slideWidth + "px";
        slide.style.width = metrics.slideWidth + "px";
        slide.style.maxWidth = metrics.slideWidth + "px";
      });
      return metrics;
    }

    function update() {
      var visible = getVisible();
      var max = getMaxIndex();
      if (index > max) index = max;

      if (isTriple) {
        var metrics = layoutTripleSlides();
        track.style.transform = "translateX(-" + index * metrics.step + "px)";
      } else {
        root.style.setProperty("--carousel-visible", "1");
        track.style.transform = "translateX(-" + index * 100 + "%)";
      }

      if (dotsWrap) {
        dotsWrap.querySelectorAll(".clinic-carousel__dot").forEach(function (dot, i) {
          dot.classList.toggle("is-active", i === index);
        });
      }

      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index >= max;
    }

    if (prev) {
      prev.addEventListener("click", function () {
        index = Math.max(0, index - 1);
        update();
      });
    }

    if (next) {
      next.addEventListener("click", function () {
        index = Math.min(getMaxIndex(), index + 1);
        update();
      });
    }

    window.addEventListener("resize", function () {
      renderDots();
      update();
    });

    renderDots();
    update();

    setInterval(function () {
      var max = getMaxIndex();
      index = index >= max ? 0 : index + 1;
      update();
    }, 5000);
  });
})();
