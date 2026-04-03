/**
 * Blog index: uses window.__BLOG_MANIFEST__ from assets/blog-manifest.js,
 * or falls back to fetch(data/blog-manifest.json).
 */
(function () {
  var listEl = document.getElementById("blog-list");
  var emptyEl = document.getElementById("blog-empty");
  var updatedEl = document.getElementById("blog-updated");

  function escapeHtml(s) {
    if (!s) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatDate(iso) {
    if (!iso) return "";
    var p = iso.split("-");
    if (p.length !== 3) return iso;
    return p[0] + "年" + String(+p[1]) + "月" + String(+p[2]) + "日";
  }

  if (!listEl) return;

  function manifestFetchUrl() {
    var sel = document.querySelector('script[src*="blog-index"]');
    if (sel && sel.src) {
      try {
        return new URL("../data/blog-manifest.json", sel.src).href;
      } catch (e) {}
    }
    try {
      return new URL("../data/blog-manifest.json", window.location.href).href;
    } catch (e2) {
      return "../data/blog-manifest.json";
    }
  }

  function renderFromData(data) {
    if (updatedEl && data.updated) {
      updatedEl.textContent = "目录更新：" + formatDate(data.updated);
      updatedEl.hidden = false;
    }
    var posts = (data.posts || []).slice().sort(function (a, b) {
      return (b.date || "").localeCompare(a.date || "");
    });
    if (!posts.length) {
      if (emptyEl) emptyEl.hidden = false;
      return;
    }
    if (emptyEl) emptyEl.hidden = true;
    listEl.innerHTML = posts
      .map(function (p) {
        var href = "posts/" + encodeURIComponent(p.slug) + ".html";
        return (
          '<article class="blog-card">' +
          '<time class="blog-card__time" datetime="' +
          escapeHtml(p.date) +
          '">' +
          escapeHtml(formatDate(p.date)) +
          "</time>" +
          "<h2 class=\"blog-card__title\"><a href=\"" +
          href +
          '">' +
          escapeHtml(p.title) +
          "</a></h2>" +
          '<p class="blog-card__excerpt">' +
          escapeHtml(p.excerpt) +
          "</p>" +
          '<div class="blog-card__foot">' +
          (p.author
            ? '<span class="blog-card__author">' + escapeHtml(p.author) + "</span>"
            : "") +
          '<a class="learn-more" href="' +
          href +
          '">阅读全文</a>' +
          "</div>" +
          "</article>"
        );
      })
      .join("");
  }

  var embedded = window.__BLOG_MANIFEST__;
  if (embedded && Array.isArray(embedded.posts)) {
    renderFromData(embedded);
    return;
  }

  fetch(manifestFetchUrl(), { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error("load");
      return r.json();
    })
    .then(renderFromData)
    .catch(function () {
      if (emptyEl) {
        emptyEl.hidden = false;
        emptyEl.textContent = "暂时无法加载文章列表，请稍后再试或直接致电诊所。";
      }
    });
})();
