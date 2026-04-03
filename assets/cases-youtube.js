/**
 * 成功案例页：每个案例对应一条 YouTube 嵌入视频。
 * 在下方数组中按顺序填入视频 ID（来自 youtube.com/watch?v= 或 youtu.be/ 后的 11 位字符）。
 * 留空字符串则显示「视频待配置」占位。
 */
(function () {
  var IDS = [
    "R0YGztEmv9k", // 0 月经不调、脱发
    "zJtT54B0liY", // 1 头重、脚无力、没胃口
    "6K_41TFipCs", // 2 慢性偏头痛
    "HD9_l7_MeIg", // 3 前列腺炎
    "bhuKUn6Yua4", // 4 腰椎骨错位、腕管症
  ];

  function validId(s) {
    return typeof s === "string" && /^[a-zA-Z0-9_-]{11}$/.test(s);
  }

  function escapeAttr(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/</g, "&lt;");
  }

  function posterHtml(id, title) {
    return (
      '<button type="button" class="case-video-poster" aria-label="播放视频：' +
      escapeAttr(title) +
      '" data-yt-id="' +
      escapeAttr(id) +
      '">' +
      '<img src="https://i.ytimg.com/vi/' +
      id +
      '/hqdefault.jpg" alt="" loading="lazy" decoding="async" width="480" height="360">' +
      '<span class="case-video-play" aria-hidden="true"></span>' +
      "</button>"
    );
  }

  document.querySelectorAll("[data-case-video-index]").forEach(function (card) {
    var i = parseInt(card.getAttribute("data-case-video-index"), 10);
    if (isNaN(i) || i < 0 || i >= IDS.length) return;
    var frame = card.querySelector(".case-video-frame");
    if (!frame) return;
    var h3 = card.querySelector("h3");
    var title = h3 ? h3.textContent.trim() : "国医堂案例视频";
    var id = IDS[i];

    if (validId(id)) {
      frame.innerHTML = posterHtml(id, title);
    } else {
      frame.innerHTML =
        '<p class="case-video-placeholder">视频待配置：请在 <code>assets/cases-youtube.js</code> 第 ' +
        (i + 1) +
        " 条填入 YouTube 视频 ID。</p>";
    }
    frame.removeAttribute("aria-busy");
  });

  var grid = document.querySelector(".cases-video-grid");
  if (!grid) return;

  grid.addEventListener("click", function (e) {
    var btn = e.target.closest(".case-video-poster");
    if (!btn || !grid.contains(btn)) return;
    var id = btn.getAttribute("data-yt-id");
    if (!validId(id)) return;
    var wrap = btn.closest(".case-video-frame");
    if (!wrap) return;
    var card = wrap.closest(".case-video-card");
    var h3 = card ? card.querySelector("h3") : null;
    var t = h3 ? h3.textContent.trim() : "国医堂案例视频";
    wrap.innerHTML =
      '<iframe title="' +
      escapeAttr(t) +
      '" src="https://www.youtube.com/embed/' +
      id +
      '?rel=0&modestbranding=1&playsinline=1" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>';
  });
})();
