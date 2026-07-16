#!/usr/bin/env python3
"""Sync navbar markup across Chinese and English HTML pages (matches CN layout)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "en"
NAV_RE = re.compile(r'<nav aria-label="[^"]*" class="navbar">.*?</nav>', re.DOTALL)
SKIP_PARTS = {".tmp", "Aura-Cure-EMR", "sample7", "reference.html", "partials"}


def should_skip(path: Path) -> bool:
    return any(part in str(path) for part in SKIP_PARTS)


def public_path(path: Path) -> str:
    if EN_ROOT in path.parents or path.parent == EN_ROOT:
        rel = path.relative_to(EN_ROOT)
        prefix = "/en"
    else:
        rel = path.relative_to(ROOT)
        prefix = ""
    if rel.name == "index.html":
        if rel.parent == Path("."):
            return prefix + "/" if prefix else "/"
        return f"{prefix}/{rel.parent.as_posix()}/"
    return f"{prefix}/{rel.with_suffix('').as_posix()}"


def lang_switch_href(path: Path) -> str:
    if EN_ROOT in path.parents or path.parent == EN_ROOT:
        rel = path.relative_to(EN_ROOT)
        if rel.name == "index.html" and rel.parent == Path("."):
            return "/"
        zp = "/" + rel.with_suffix("").as_posix()
        return zp.replace("\\", "/")
    rel = path.relative_to(ROOT)
    if rel.name == "index.html" and rel.parent == Path("."):
        return "/en/"
    zp = "/" + rel.with_suffix("").as_posix()
    return "/en" + zp.replace("\\", "/")


def active_key(path: Path) -> str:
    p = public_path(path).rstrip("/") or "/"
    if p in ("/", "/en"):
        return "home"
    tail = p.split("/")[-1]
    if tail.startswith("service-"):
        return "services"
    mapping = {
        "services": "services",
        "about-us": "about",
        "doctors": "doctors",
        "successful-cases": "cases",
        "patient-review": "reviews",
        "activities": "activities",
        "contact-us": "contact",
        "book": "book",
        "blog": "blog",
    }
    return mapping.get(tail, "")


def ac(flag: bool) -> str:
    return ' aria-current="page"' if flag else ""


def render_nav(path: Path) -> str:
    en = EN_ROOT in path.parents or path.parent == EN_ROOT
    key = active_key(path)
    lang_href = lang_switch_href(path)
    phone_onclick = "onclick=\"return gtag_report_phone_conversion('tel:+17188881133');\""

    if en:
        home, services, about, doctors = "/en/", "/en/services", "/en/about-us", "/en/doctors"
        cases, reviews, activities, contact, book = (
            "/en/successful-cases",
            "/en/patient-review",
            "/en/activities",
            "/en/contact-us",
            "/en/book",
        )
        aria = "Main navigation"
        labels = dict(
            home="Home",
            services="Services",
            about="About Us",
            doctors="Our Team",
            cases="Success Stories",
            reviews="Patient Reviews",
            activities="Clinic Activities",
            contact="Contact",
            book="Book Online",
            lang="中文",
            phone="Call: 718-888-1133",
            menu="Open menu",
        )
        logo_alt = "Guoyitang Traditional Chinese Medicine Clinic Logo (Guoyitang TCM)"
        img = "/image/guoyitang-logo-header-125x42.webp"
    else:
        home, services, about, doctors = "/", "/services", "/about-us", "/doctors"
        cases, reviews, activities, contact, book = (
            "/successful-cases",
            "/patient-review",
            "/activities",
            "/contact-us",
            "/book",
        )
        aria = "主导航"
        labels = dict(
            home="主页",
            services="诊疗服务",
            about="关于我们",
            doctors="国医堂团队",
            cases="成功案例",
            reviews="病人好评",
            activities="诊所活动",
            contact="联系我们",
            book="在线预约",
            lang="English",
            phone="电话预约: 718-888-1133",
            menu="打开菜单",
        )
        logo_alt = "国医堂中医诊所标志（Guoyitang TCM）"
        img = "image/guoyitang-logo-header-125x42.webp"

    a = {
        "home": ac(key == "home"),
        "services": ac(key == "services"),
        "about": ac(key == "about"),
        "doctors": ac(key == "doctors"),
        "cases": ac(key == "cases"),
        "reviews": ac(key == "reviews"),
        "activities": ac(key == "activities"),
        "contact": ac(key == "contact"),
        "book": ac(key == "book"),
    }

    return f"""<nav aria-label="{aria}" class="navbar">
<div class="nav-container">
<a class="logo" href="{home}"><img alt="{logo_alt}" height="42" src="{img}" width="125"/></a>
<ul class="nav-links">
<li><a href="{home}"{a["home"]}>{labels["home"]}</a></li>
<li><a href="{services}"{a["services"]}>{labels["services"]}</a></li>
<li class="nav-has-sub"><a href="{about}"{a["about"]}>{labels["about"]}</a>
<ul class="nav-sub">
<li><a href="{doctors}"{a["doctors"]}>{labels["doctors"]}</a></li>
</ul>
</li>
<li class="nav-has-sub"><a href="{cases}"{a["cases"]}>{labels["cases"]}</a>
<ul class="nav-sub">
<li><a href="{reviews}"{a["reviews"]}>{labels["reviews"]}</a></li>
</ul>
</li>
<li><a href="{activities}"{a["activities"]}>{labels["activities"]}</a></li>
<li><a href="{contact}"{a["contact"]}>{labels["contact"]}</a></li>
<li><a class="nav-book" href="{book}"{a["book"]}>{labels["book"]}</a></li>
</ul>
<div class="nav-actions">
<a class="lang-switch" href="{lang_href}">{labels["lang"]}</a> <a class="cta-nav cta-nav--phone" href="tel:+17188881133" {phone_onclick}>{labels["phone"]}</a>
</div>
<button aria-controls="mobileMenu" aria-expanded="false" aria-label="{labels["menu"]}" class="mobile-menu-toggle" type="button">☰</button>
</div>
<div class="mobile-menu" id="mobileMenu">
<ul class="mobile-nav-links">
<li><a href="{home}"{a["home"]}>{labels["home"]}</a></li>
<li><a href="{services}"{a["services"]}>{labels["services"]}</a></li>
<li><a href="{about}"{a["about"]}>{labels["about"]}</a></li>
<li><a href="{doctors}"{a["doctors"]}>{labels["doctors"]}</a></li>
<li><a href="{cases}"{a["cases"]}>{labels["cases"]}</a></li>
<li><a href="{reviews}"{a["reviews"]}>{labels["reviews"]}</a></li>
<li><a href="{activities}"{a["activities"]}>{labels["activities"]}</a></li>
<li><a href="{contact}"{a["contact"]}>{labels["contact"]}</a></li>
<li><a href="{book}"{a["book"]}>{labels["book"]}</a></li>
</ul>
<div class="mobile-actions">
<a class="lang-switch" href="{lang_href}">{labels["lang"]}</a> <a class="cta-nav cta-nav--phone" href="tel:+17188881133" {phone_onclick}>{labels["phone"]}</a>
</div>
</div>
</nav>"""


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            continue
        if "blog/_template" in str(path):
            continue
        source = path.read_text(encoding="utf-8")
        if not NAV_RE.search(source):
            continue
        nav = render_nav(path)
        source = NAV_RE.sub(nav, source, count=1)
        path.write_text(source, encoding="utf-8")
        updated += 1
        print(path.relative_to(ROOT))
    print(f"\nUpdated {updated} files.")


if __name__ == "__main__":
    main()
