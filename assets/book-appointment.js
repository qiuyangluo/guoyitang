(function () {
  var script = document.currentScript;
  var LANG = (script && script.getAttribute("data-lang")) || "zh";
  var T =
    LANG === "en"
      ? {
          today: "Today",
          tomorrow: "Tomorrow",
          weekdays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
          dateHint: "Closed Fridays — pick a date below",
          moreDates: "Other date",
          timeHintNeedDate: "Choose a date first",
          timeHintPick: "Pick a time slot",
          morning: "Morning",
          afternoon: "Afternoon",
          fridayPick: "We're closed Fridays. Please pick another day.",
          fridaySubmit: "We're closed Fridays. Choose Mon–Thu, Sat, or Sun.",
          missingDateTime: "Please choose a date and time slot.",
          missingPhone: "Please enter your phone number.",
          invalidPhone: "Please enter a valid phone number (at least 10 digits).",
          invalidFormat: "Invalid date or time.",
          unparseable: "Could not read the selected date and time.",
          network: "Network error. Please call the clinic to book.",
          apiFail: "Could not save. Please call the clinic or try again.",
          successTitle: "Request received",
          successDetail: "Preferred visit",
          successHint: "We've saved your request. To reschedule, call",
          successNew: "Book another visit",
          contactLink: "Contact",
          submitting: "Submitting…",
        }
      : {
          today: "今天",
          tomorrow: "明天",
          weekdays: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
          dateHint: "周五休诊，请从下方可约日期中选择",
          moreDates: "选择其他日期",
          timeHintNeedDate: "请先选择日期",
          timeHintPick: "请选择到诊时段",
          morning: "上午",
          afternoon: "下午",
          fridayPick: "周五休诊，请改选其他日期。",
          fridaySubmit: "周五休诊，请选择周一至周四、周六或周日。",
          missingDateTime: "请选择日期与时间段。",
          missingPhone: "请填写手机号码。",
          invalidPhone: "请填写有效的手机号码（至少 10 位数字）。",
          invalidFormat: "日期或时间格式无效。",
          unparseable: "无法解析所选日期时间。",
          network: "网络错误，请致电诊所预约。",
          apiFail: "提交失败，请改打电话预约或稍后再试。",
          successTitle: "预约已收到",
          successDetail: "您的到诊意向",
          successHint: "我们已记录您的预约。如需改期请致电",
          successNew: "再约一次",
          contactLink: "联系我们",
          submitting: "提交中…",
        };

  var SLOT_MS = 60 * 60 * 1000;
  var TZ_LABEL = "America/New_York";
  var QUICK_DATE_COUNT = 8;

  var form = document.getElementById("book-form");
  var errEl = document.getElementById("book-err");
  var successPanel = document.getElementById("book-success");
  var successDetailEl = document.getElementById("book-success-detail");
  var successNewBtn = document.getElementById("book-success-new");
  var quickDatesEl = document.getElementById("book-quick-dates");
  var timeSection = document.getElementById("book-time-section");
  var timeHintEl = document.getElementById("book-time-hint");
  var extraSection = document.getElementById("book-form-extra");
  var stepItems = document.querySelectorAll(".book-steps__item");
  var stepsEl = document.querySelector(".book-steps");

  if (!form) return;

  var submitting = false;
  var submitBtn = form.querySelector('button[type="submit"]');
  var submitBtnDefaultText = submitBtn ? submitBtn.textContent : "";

  function setSubmitting(on) {
    submitting = on;
    if (!submitBtn) return;
    submitBtn.disabled = on;
    submitBtn.setAttribute("aria-busy", on ? "true" : "false");
    submitBtn.textContent = on ? T.submitting : submitBtnDefaultText;
  }

  function bookEvent(name, params) {
    if (typeof gtag !== "function") return;
    var p = {
      form_id: "book-form",
      form_name: "book_appointment",
      language: LANG,
    };
    if (params) {
      for (var k in params) {
        if (Object.prototype.hasOwnProperty.call(params, k)) p[k] = params[k];
      }
    }
    gtag("event", name, p);
  }

  bookEvent("book_form_view");

  function showErr(msg) {
    if (!errEl) return;
    errEl.textContent = msg || "";
    errEl.style.display = msg ? "block" : "none";
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function ymdFromDate(d) {
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function fmtLocal(dt) {
    return (
      dt.getFullYear() +
      "-" +
      pad(dt.getMonth() + 1) +
      "-" +
      pad(dt.getDate()) +
      "T" +
      pad(dt.getHours()) +
      ":" +
      pad(dt.getMinutes()) +
      ":00"
    );
  }

  function isFridayYmd(y, m, d) {
    return new Date(y, m - 1, d, 12, 0, 0).getDay() === 5;
  }

  function parseYmd(v) {
    var p = v.split("-").map(Number);
    return p.length >= 3 ? p : null;
  }

  function phoneDigits(raw) {
    return String(raw || "").replace(/\D/g, "");
  }

  function formatPhoneNumber(raw) {
    var digits = phoneDigits(raw).slice(0, 10);
    if (digits.length <= 3) return digits;
    if (digits.length <= 6) {
      return "(" + digits.slice(0, 3) + ") " + digits.slice(3);
    }
    return (
      "(" +
      digits.slice(0, 3) +
      ") " +
      digits.slice(3, 6) +
      "-" +
      digits.slice(6)
    );
  }

  function sameYmd(a, b) {
    return a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate();
  }

  function quickDateLabel(d, index, today, tomorrow) {
    if (index === 0 && sameYmd(d, today)) return T.today;
    if (sameYmd(d, tomorrow)) return T.tomorrow;
    return (
      T.weekdays[d.getDay()] +
      " " +
      (d.getMonth() + 1) +
      "/" +
      d.getDate()
    );
  }

  function formatDisplayDateTime(dateStr, timeStr) {
    var p = parseYmd(dateStr);
    if (!p) return dateStr + " " + timeStr;
    var d = new Date(p[0], p[1] - 1, p[2], 12, 0, 0);
    var tp = timeStr.split(":");
    var datePart =
      T.weekdays[d.getDay()] +
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
    var timePart =
      LANG === "en"
        ? (h > 12 ? h - 12 : h === 0 ? 12 : h) +
          ":" +
          m +
          (h >= 12 ? " pm" : " am")
        : h + ":" + m;
    return datePart + " · " + timePart;
  }

  function updateSteps() {
    var dateStr = dateInput && dateInput.value;
    var timeStr = timeHidden && timeHidden.value;
    stepItems.forEach(function (li) {
      var step = li.getAttribute("data-step");
      li.classList.remove("is-active", "is-done");
      if (step === "1") {
        if (dateStr) li.classList.add("is-done");
        else li.classList.add("is-active");
      } else if (step === "2") {
        if (timeStr) li.classList.add("is-done");
        else if (dateStr) li.classList.add("is-active");
      } else if (step === "3") {
        if (timeStr) li.classList.add("is-active");
      }
    });
  }

  function unlockTimeSection(on) {
    if (!timeSection) return;
    timeSection.classList.toggle("book-time--locked", !on);
    if (timeHintEl) {
      timeHintEl.textContent = on ? T.timeHintPick : T.timeHintNeedDate;
    }
  }

  function unlockExtraSection(on) {
    if (extraSection) extraSection.classList.toggle("book-form__extra--locked", !on);
  }

  var selectedQuickYmd = "";
  var datePills = [];
  var dateInput = form.querySelector('input[name="date"]');
  var timeHidden = form.querySelector('input[name="time"]');
  var phoneInput = form.querySelector('input[name="phone"]');
  var timeButtons = form.querySelectorAll(".book-time-slot");

  function setQuickPillSelected(ymd) {
    selectedQuickYmd = ymd || "";
    datePills.forEach(function (btn) {
      var on = ymd && btn.getAttribute("data-date") === ymd;
      btn.classList.toggle("is-selected", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function setSelectedTime(value) {
    if (timeHidden) timeHidden.value = value || "";
    timeButtons.forEach(function (btn) {
      var t = btn.getAttribute("data-time") || "";
      var on = value && t === value;
      btn.classList.toggle("is-selected", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    unlockExtraSection(!!value);
    updateSteps();
  }

  function selectDate(ymd, source) {
    if (!ymd || !dateInput) return;
    var p = parseYmd(ymd);
    if (!p) return;
    if (isFridayYmd(p[0], p[1], p[2])) {
      showErr(T.fridayPick);
      bookEvent("book_date_rejected_friday", { appointment_date: ymd });
      return;
    }
    showErr("");
    dateInput.value = ymd;
    setQuickPillSelected(ymd);
    setSelectedTime("");
    unlockTimeSection(true);
    updateSteps();
    bookEvent("book_date_selected", {
      appointment_date: ymd,
      date_source: source || "quick",
    });
  }

  function buildQuickDates() {
    if (!quickDatesEl) return;
    quickDatesEl.innerHTML = "";
    datePills = [];
    var today = new Date();
    today.setHours(12, 0, 0, 0);
    var tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    var cursor = new Date(today);
    var built = 0;
    var index = 0;
    while (built < QUICK_DATE_COUNT) {
      if (cursor.getDay() !== 5) {
        var ymd = ymdFromDate(cursor);
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "book-date-pill";
        btn.setAttribute("data-date", ymd);
        btn.setAttribute("aria-pressed", "false");
        btn.textContent = quickDateLabel(cursor, index, today, tomorrow);
        (function (picked) {
          btn.addEventListener("click", function () {
            selectDate(picked, "quick");
          });
        })(ymd);
        quickDatesEl.appendChild(btn);
        datePills.push(btn);
        built++;
        index++;
      }
      cursor.setDate(cursor.getDate() + 1);
    }
  }

  function showSuccessPanel(dateStr, timeStr) {
    form.hidden = true;
    if (stepsEl) stepsEl.hidden = true;
    if (successPanel) {
      successPanel.hidden = false;
      if (successDetailEl) {
        successDetailEl.textContent = formatDisplayDateTime(dateStr, timeStr);
      }
    }
    showErr("");
    bookEvent("book_submit_success", {
      appointment_date: dateStr,
      appointment_time: timeStr,
    });
    bookEvent("form_submit", {
      appointment_date: dateStr,
      appointment_time: timeStr,
    });
    successPanel && successPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function resetBookingUi() {
    setSubmitting(false);
    form.hidden = false;
    if (stepsEl) stepsEl.hidden = false;
    if (successPanel) successPanel.hidden = true;
    form.reset();
    setQuickPillSelected("");
    setSelectedTime("");
    unlockTimeSection(false);
    unlockExtraSection(false);
    updateSteps();
    showErr("");
  }

  buildQuickDates();

  if (dateInput) {
    dateInput.min = ymdFromDate(new Date());
    dateInput.addEventListener("change", function () {
      var v = dateInput.value;
      if (!v) {
        setQuickPillSelected("");
        unlockTimeSection(false);
        setSelectedTime("");
        updateSteps();
        return;
      }
      var p = parseYmd(v);
      if (!p) return;
      if (isFridayYmd(p[0], p[1], p[2])) {
        showErr(T.fridayPick);
        dateInput.value = "";
        setQuickPillSelected("");
        bookEvent("book_date_rejected_friday", { appointment_date: v });
        return;
      }
      showErr("");
      setQuickPillSelected(v);
      setSelectedTime("");
      unlockTimeSection(true);
      updateSteps();
      bookEvent("book_date_selected", {
        appointment_date: v,
        date_source: "picker",
      });
    });
  }

  if (phoneInput) {
    phoneInput.maxLength = 14;
    phoneInput.addEventListener("input", function () {
      phoneInput.value = formatPhoneNumber(phoneInput.value);
    });
    phoneInput.addEventListener("blur", function () {
      phoneInput.value = formatPhoneNumber(phoneInput.value);
    });
  }

  timeButtons.forEach(function (btn) {
    btn.setAttribute("aria-pressed", "false");
    btn.addEventListener("click", function () {
      if (timeSection && timeSection.classList.contains("book-time--locked")) return;
      var t = btn.getAttribute("data-time");
      if (!t) return;
      setSelectedTime(t);
      showErr("");
      bookEvent("book_time_selected", { appointment_time: t });
    });
  });

  if (successNewBtn) {
    successNewBtn.addEventListener("click", function () {
      resetBookingUi();
      buildQuickDates();
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  form.addEventListener("reset", function () {
    setQuickPillSelected("");
    setSelectedTime("");
    unlockTimeSection(false);
    unlockExtraSection(false);
    updateSteps();
  });

  unlockTimeSection(false);
  unlockExtraSection(false);
  updateSteps();

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (submitting) return;
    showErr("");
    bookEvent("book_submit_click");

    var fd = new FormData(form);
    var phone = formatPhoneNumber(fd.get("phone"));
    if (phoneInput) phoneInput.value = phone;
    var dateStr = fd.get("date");
    var timeStr = fd.get("time") || "";
    var notes = String(fd.get("notes") || "").trim();
    var hasPhone = phone ? "yes" : "no";
    var hasNotes = notes ? "yes" : "no";

    if (!dateStr || !timeStr) {
      showErr(T.missingDateTime);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "missing_date_or_time",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }

    if (!phone) {
      showErr(T.missingPhone);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "missing_phone",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }

    if (phoneDigits(phone).length < 10) {
      showErr(T.invalidPhone);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "invalid_phone",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }

    var dp = parseYmd(dateStr);
    var tp = timeStr.split(":").map(Number);
    if (!dp || tp.length < 2) {
      showErr(T.invalidFormat);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "invalid_format",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }
    if (isFridayYmd(dp[0], dp[1], dp[2])) {
      showErr(T.fridaySubmit);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "friday_closed",
        appointment_date: dateStr,
        appointment_time: timeStr,
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }

    var start = new Date(dp[0], dp[1] - 1, dp[2], tp[0], tp[1] || 0, 0);
    if (isNaN(start.getTime())) {
      showErr(T.unparseable);
      bookEvent("book_submit_validation_failed", {
        failure_reason: "unparseable_datetime",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      return;
    }
    var end = new Date(start.getTime() + SLOT_MS);

    var payload = {
      summary:
        LANG === "en"
          ? phone
            ? "Guoyitang booking · " + phone
            : "Guoyitang booking"
          : phone
            ? "国医堂预约 · " + phone
            : "国医堂预约",
      start: fmtLocal(start),
      end: fmtLocal(end),
      timeZone: TZ_LABEL,
      contactName: LANG === "en" ? "Website booking" : "网站预约",
      contactPhone: phone,
    };
    if (notes) payload.notes = notes;

    setSubmitting(true);
    try {
      var res = await fetch("/api/calendar-event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      var ct = res.headers.get("content-type") || "";
      var j = ct.indexOf("application/json") !== -1 ? await res.json() : {};

      if (res.ok && j.ok) {
        showSuccessPanel(dateStr, timeStr);
        return;
      }

      bookEvent("book_submit_failed", {
        failure_reason: "api_error",
        http_status: res.status,
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      showErr((j && j.error) || T.apiFail + " (" + res.status + ")");
      setSubmitting(false);
    } catch (_) {
      bookEvent("book_submit_failed", {
        failure_reason: "network",
        has_phone: hasPhone,
        has_notes: hasNotes,
      });
      showErr(T.network);
      setSubmitting(false);
    }
  });
})();
