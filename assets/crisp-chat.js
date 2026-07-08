(function () {
  var lang = (document.documentElement.getAttribute("lang") || "").toLowerCase();
  var locale = lang.indexOf("en") === 0 ? "en" : "zh-cn";

  window.$crisp = window.$crisp || [];
  window.CRISP_WEBSITE_ID = "7860ca4b-a8a0-4685-af06-da8125463d6b";
  window.CRISP_RUNTIME_CONFIG = Object.assign({}, window.CRISP_RUNTIME_CONFIG, {
    locale: locale,
  });

  var d = document;
  var s = d.createElement("script");
  s.src = "https://client.crisp.chat/l.js";
  s.async = 1;
  d.getElementsByTagName("head")[0].appendChild(s);
})();
