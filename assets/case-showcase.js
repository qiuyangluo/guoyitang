/**
 * Homepage 成功案例：点击卡片封面在卡片内播放视频（YouTube 或 MP4），支持全屏。
 */
(function () {
  var grid = document.querySelector(".case-showcase-grid");
  if (!grid) return;

  function validYtId(s) {
    return typeof s === "string" && /^[a-zA-Z0-9_-]{11}$/.test(s);
  }

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  function pauseOthers(activeCard) {
    grid.querySelectorAll(".case-showcase-card.is-playing").forEach(function (card) {
      if (card === activeCard) return;
      var video = card.querySelector("video");
      if (video) {
        video.pause();
      }
      card.classList.remove("is-playing");
    });
  }

  function playYoutube(media, card, btn) {
    var id = btn.getAttribute("data-youtube-id");
    if (!validYtId(id)) return;
    var label = btn.getAttribute("aria-label") || "国医堂案例视频";
    pauseOthers(card);
    media.innerHTML =
      '<iframe title="' +
      escapeAttr(label) +
      '" src="https://www.youtube.com/embed/' +
      id +
      '?rel=0&modestbranding=1&playsinline=1&autoplay=1" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>';
    card.classList.add("is-playing");
  }

  function playMp4(media, card, btn) {
    var src = btn.getAttribute("data-video-src");
    if (!src) return;
    var label = btn.getAttribute("aria-label") || "国医堂案例视频";
    pauseOthers(card);
    var video = document.createElement("video");
    video.className = "case-showcase-card__player";
    video.src = src;
    video.controls = true;
    video.playsInline = true;
    video.setAttribute("playsinline", "");
    video.setAttribute("controlsList", "nodownload");
    video.title = label.replace(/^播放视频：/, "");
    media.innerHTML = "";
    media.appendChild(video);
    card.classList.add("is-playing");
    video.play().catch(function () {});
  }

  grid.addEventListener("click", function (e) {
    var btn = e.target.closest(".case-showcase-card__poster");
    if (!btn || !grid.contains(btn)) return;
    e.preventDefault();
    var card = btn.closest(".case-showcase-card");
    var media = card ? card.querySelector(".case-showcase-card__media") : null;
    if (!card || !media) return;

    if (btn.hasAttribute("data-youtube-id")) {
      playYoutube(media, card, btn);
      return;
    }
    if (btn.hasAttribute("data-video-src")) {
      playMp4(media, card, btn);
    }
  });
})();
