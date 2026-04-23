#!/usr/bin/env python3
"""Insert Chinese/English toggle link in .nav-actions and .mobile-actions (idempotent)."""
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "en"
SKIP = {"reference.html", "sample7.html"}


def zh_url_path(rel: Path) -> str:
    """Public URL path for Chinese site from path relative to site root (no 'en/')."""
    if rel.name == "index.html":
        parent = rel.parent
        if parent == Path("."):
            return "/"
        return "/" + parent.as_posix().replace("\\", "/").strip("/") + "/"
    return "/" + rel.with_suffix("").as_posix().replace("\\", "/")


def counterpart_href(file: Path) -> tuple[str, str]:
    if file.is_relative_to(EN_ROOT):
        rel = file.relative_to(EN_ROOT)
        return zh_url_path(rel), "中文"
    rel = file.relative_to(ROOT)
    zp = zh_url_path(rel)
    if zp == "/":
        return "/en/", "English"
    return "/en" + zp, "English"


def inject(path: Path) -> None:
    if path.name in SKIP:
        return
    raw = path.read_text(encoding="utf-8")
    if 'class="lang-switch"' in raw:
        return
    soup = BeautifulSoup(raw, "html.parser")
    href, label = counterpart_href(path)
    for sel in (".nav-actions", ".mobile-actions"):
        box = soup.select_one(sel)
        if not box:
            continue
        a = soup.new_tag("a", href=href, **{"class": "lang-switch"})
        a.string = label
        cta = box.select_one(".cta-nav")
        if cta:
            cta.insert_before(a)
            cta.insert_before(" ")
        else:
            box.append(a)
    path.write_text(str(soup), encoding="utf-8")
    print("lang-switch:", path.relative_to(ROOT))


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        inject(p)
    for p in sorted((ROOT / "blog").rglob("*.html")):
        inject(p)
    for p in sorted(EN_ROOT.rglob("*.html")):
        inject(p)


if __name__ == "__main__":
    main()
