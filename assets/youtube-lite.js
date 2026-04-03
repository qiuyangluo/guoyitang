/**
 * Click-to-play YouTube embed (reduces initial JS/CSS from youtube.com on first load).
 */
(function () {
  document.querySelectorAll(".intro-video-lite").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-youtube-id");
      if (!id || !/^[a-zA-Z0-9_-]{11}$/.test(id)) return;
      var wrap = btn.parentElement;
      if (!wrap) return;
      var iframe = document.createElement("iframe");
      iframe.className = "intro-video-player intro-video-player--loaded";
      iframe.src = "https://www.youtube.com/embed/" + id + "?rel=0&autoplay=1";
      iframe.title = btn.getAttribute("aria-label") || "YouTube video";
      iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
      iframe.setAttribute("allowfullscreen", "");
      iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
      wrap.replaceChild(iframe, btn);
    });
  });
})();
