#!/usr/bin/env python3
"""Patch shared nav + footer across static HTML pages to match WordPress reference."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV_ZH = """<nav aria-label="主导航" class="navbar">
<div class="nav-container">
<a class="logo" href="/"><img alt="国医堂中医诊所标志（Guoyitang TCM）" height="42" src="image/guoyitang-logo-header-125x42.webp" width="125"/></a>
<ul class="nav-links">
<li><a href="/">主页</a></li>
<li><a href="/services">诊疗服务</a></li>
<li class="nav-has-sub"><a href="/about-us">关于我们</a>
<ul class="nav-sub">
<li><a href="/doctors">国医堂团队</a></li>
</ul>
</li>
<li class="nav-has-sub"><a href="/successful-cases">成功案例</a>
<ul class="nav-sub">
<li><a href="/patient-review">病人好评</a></li>
</ul>
</li>
<li><a href="/contact-us">联系我们</a></li>
<li><a class="nav-book" href="/book">在线预约</a></li>
</ul>
<div class="nav-actions">
<a class="cta-nav cta-nav--phone" href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">电话预约: 718-888-1133</a>
</div>
<button aria-controls="mobileMenu" aria-expanded="false" aria-label="打开菜单" class="mobile-menu-toggle" type="button">☰</button>
</div>
<div class="mobile-menu" id="mobileMenu">
<ul class="mobile-nav-links">
<li><a href="/">主页</a></li>
<li><a href="/services">诊疗服务</a></li>
<li><a href="/about-us">关于我们</a></li>
<li><a href="/doctors">国医堂团队</a></li>
<li><a href="/successful-cases">成功案例</a></li>
<li><a href="/patient-review">病人好评</a></li>
<li><a href="/contact-us">联系我们</a></li>
<li><a href="/book">在线预约</a></li>
</ul>
<div class="mobile-actions">
<a class="cta-nav cta-nav--phone" href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">电话预约: 718-888-1133</a>
</div>
</div>
</nav>"""

FOOTER_ZH = """<footer class="site-footer">
<div class="container">
<div class="footer-content">
<div class="footer-section">
<img alt="国医堂中医诊所标志" decoding="async" height="81" loading="lazy" src="image/guoyitang-logo-footer.webp" style="max-width:180px;height:auto;margin-bottom:1rem" width="241"/>
</div>
<div class="footer-section">
<h3>诊所信息</h3>
<p>142-38 37th Ave #1C1D<br/>Flushing, NY 11354</p>
<p>星期一至四、六、日 9:00–17:00<br/>星期五休息</p>
</div>
<div class="footer-section">
<h3>联系我们</h3>
<p><a href="tel:+17188881133" onclick="return gtag_report_phone_conversion('tel:+17188881133');">(718) 888-1133</a><br/>
<a href="tel:+17188868979" onclick="return gtag_report_phone_conversion('tel:+17188868979');">(718) 886-8979</a></p>
<p><a href="/contact-us">到院路线</a> · <a href="/book">在线预约</a></p>
</div>
</div>
<div class="footer-bottom">Copyright © 2026 Guoyitang</div>
</div>
</footer>"""

NAV_PATTERN = re.compile(r"<nav aria-label=\"主导航\" class=\"navbar\">.*?</nav>", re.DOTALL)
FOOTER_PATTERN = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.DOTALL)
THEME_COLOR = re.compile(r'<meta content="#354d2c" name="theme-color"/>')


def set_current(nav_html: str, href: str) -> str:
    nav = re.sub(r'\saria-current="page"', "", nav_html)
    nav = re.sub(
        rf'(<a href="{re.escape(href)}"(?![^>]*aria-current))',
        r'\1 aria-current="page"',
        nav,
        count=1,
    )
    return nav


PAGE_CURRENT = {
    "index.html": "/",
    "about-us.html": "/about-us",
    "doctors.html": "/doctors",
    "services.html": "/services",
    "successful-cases.html": "/successful-cases",
    "patient-review.html": "/patient-review",
    "contact-us.html": "/contact-us",
    "book.html": "/book",
}


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    rel = path.relative_to(ROOT)
    current = PAGE_CURRENT.get(str(rel))
    nav = NAV_ZH
    if current:
        nav = set_current(nav, current)

    if NAV_PATTERN.search(text):
        text = NAV_PATTERN.sub(nav, text, count=1)
    if FOOTER_PATTERN.search(text):
        text = FOOTER_PATTERN.sub(FOOTER_ZH, text, count=1)
    text = THEME_COLOR.sub('<meta content="#5c8607" name="theme-color"/>', text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if "reference.html" in path.name or "sample7.html" in path.name:
            continue
        if path.parent.name == "Aura-Cure-EMR":
            continue
        if patch_file(path):
            changed += 1
            print("patched", path.relative_to(ROOT))
    print(f"Done. {changed} files updated.")


if __name__ == "__main__":
    main()
