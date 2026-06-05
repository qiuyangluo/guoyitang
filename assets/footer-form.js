(function () {
  var forms = document.querySelectorAll('.footer-form');
  if (!forms.length) return;

  forms.forEach(function (form) {
    var textarea = form.querySelector('textarea[name="message"]');
    var counter = form.querySelector('.footer-form__count');
    var max = 180;

    if (textarea && counter) {
      var updateCount = function () {
        counter.textContent = textarea.value.length + ' / ' + max;
      };
      textarea.addEventListener('input', updateCount);
      updateCount();
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var nameInput = form.querySelector('[name="name"]');
      var phoneInput = form.querySelector('[name="phone"]');
      var name = nameInput ? nameInput.value.trim() : '';
      var phone = phoneInput ? phoneInput.value.trim() : '';
      var message = textarea ? textarea.value.trim() : '';

      if (!name) {
        if (nameInput) nameInput.focus();
        return;
      }

      var isEn = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
      var subject = encodeURIComponent(isEn ? 'Guoyitang website inquiry' : '国医堂网站预约咨询');
      var body = encodeURIComponent(
        (isEn ? 'Name: ' : '姓名: ') + name + '\n' +
        (isEn ? 'Phone: ' : '电话: ') + (phone || (isEn ? 'N/A' : '未提供')) + '\n\n' +
        message
      );

      window.location.href = 'mailto:guoyitang11366@gmail.com?subject=' + subject + '&body=' + body;
    });
  });
})();
