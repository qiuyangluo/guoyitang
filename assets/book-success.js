(function () {
  var script = document.currentScript;
  var LANG = (script && script.getAttribute("data-lang")) || "zh";
  var weekdays =
    LANG === "en"
      ? ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
      : ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function parseYmd(v) {
    var p = String(v || "").split("-").map(Number);
    return p.length >= 3 && p[0] && p[1] && p[2] ? p : null;
  }

  function formatDisplayDateTime(dateStr, timeStr) {
    var p = parseYmd(dateStr);
    if (!p) return dateStr + " " + timeStr;
    var d = new Date(p[0], p[1] - 1, p[2], 12, 0, 0);
    var tp = String(timeStr || "").split(":");
    var datePart =
      weekdays[d.getDay()] +
      " " +
      (LANG === "en"
        ? pad(d.getMonth() + 1) + "/" + pad(d.getDate()) + "/" + d.getFullYear()
        : d.getFullYear() +
          "年" +
          (d.getMonth() + 1) +
          "月" +
          d.getDate() +
          "日");
    var h = parseInt(tp[0], 10);
    var m = tp[1] || "00";
    if (isNaN(h)) return datePart;
    var timePart =
      LANG === "en"
        ? (h > 12 ? h - 12 : h === 0 ? 12 : h) +
          ":" +
          m +
          (h >= 12 ? " pm" : " am")
        : h + ":" + m;
    return datePart + " · " + timePart;
  }

  var params = new URLSearchParams(window.location.search);
  var dateStr = params.get("date") || "";
  var timeStr = params.get("time") || "";
  var detailEl = document.getElementById("book-success-detail");
  var labelEl = document.getElementById("book-success-label");
  var langLink = document.getElementById("book-success-lang");
  var langLinkMobile = document.getElementById("book-success-lang-mobile");

  if (dateStr && timeStr && detailEl) {
    detailEl.textContent = formatDisplayDateTime(dateStr, timeStr);
    detailEl.hidden = false;
    if (labelEl) labelEl.hidden = false;
  }

  var qs =
    dateStr && timeStr
      ? "?date=" + encodeURIComponent(dateStr) + "&time=" + encodeURIComponent(timeStr)
      : "";
  if (langLink) {
    langLink.href =
      (LANG === "en" ? "/book-success" : "/en/book-success") + qs;
  }
  if (langLinkMobile) {
    langLinkMobile.href =
      (LANG === "en" ? "/book-success" : "/en/book-success") + qs;
  }

  if (typeof gtag === "function") {
    gtag("event", "book_success_page_view", {
      form_id: "book-form",
      form_name: "book_appointment",
      language: LANG,
      appointment_date: dateStr || undefined,
      appointment_time: timeStr || undefined,
    });
  }
})();
