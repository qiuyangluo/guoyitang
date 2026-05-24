function gtag_report_phone_conversion(url) {
  var phoneNumber = "";
  if (typeof url === "string" && url.indexOf("tel:") === 0) {
    phoneNumber = url.slice(4);
  }
  var lang =
    (document.documentElement.getAttribute("lang") || "")
      .toLowerCase()
      .indexOf("en") === 0
      ? "en"
      : window.location.pathname.indexOf("/en/") === 0
        ? "en"
        : "zh";

  if (typeof gtag === "function") {
    gtag("event", "click_to_call", {
      phone_number: phoneNumber,
      link_url: url || "",
      language: lang,
      page_path: window.location.pathname || "",
    });
  }

  var callback = function () {
    if (typeof url !== "undefined") {
      window.location = url;
    }
  };
  gtag("event", "conversion", {
    send_to: "AW-17707030959/PKUsCISw0Z0cEK-zr_tB",
    value: 1.0,
    currency: "USD",
    event_callback: callback,
  });
  return false;
}
