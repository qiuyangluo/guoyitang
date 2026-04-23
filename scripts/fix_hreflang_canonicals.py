#!/usr/bin/env python3
"""Fix hreflang + canonical + og:url after zh_canonical logic update (no translation)."""
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "en"


def zh_canonical_for(src: Path) -> str:
    rel = src.relative_to(ROOT)
    if rel.parts[:1] == ("en",):
        rel = Path(*rel.parts[1:])
    path = "/" + str(rel.with_suffix("")).replace("\\", "/")
    if path.endswith("/index"):
        path = path[: -len("index")]
    base = "https://guoyitangus.com"
    if path in ("/index", "/"):
        return base + "/"
    return base + path.rstrip("/")


def en_canonical_for(zh_src: Path) -> str:
    z = zh_canonical_for(zh_src)
    if z.endswith("guoyitangus.com/"):
        return "https://guoyitangus.com/en/"
    if z == "https://guoyitangus.com":
        return "https://guoyitangus.com/en/"
    return z.replace("guoyitangus.com/", "guoyitangus.com/en/")


def patch_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    if 'hreflang="en"' not in raw and path.suffix == ".html":
        return
    soup = BeautifulSoup(raw, "html.parser")
    head = soup.find("head")
    if not head:
        return
    zh_src = path
    if path.is_relative_to(EN_ROOT):
        zh_src = ROOT / path.relative_to(EN_ROOT)
    zc, ec = zh_canonical_for(zh_src), en_canonical_for(zh_src)
    for l in head.find_all("link", rel=lambda x: x and "alternate" in x):
        hl = l.get("hreflang")
        if hl == "zh-Hans":
            l["href"] = zc
        elif hl == "en":
            l["href"] = ec
        elif hl == "x-default":
            l["href"] = zc
    can = head.find("link", rel="canonical")
    if can:
        can["href"] = ec if path.is_relative_to(EN_ROOT) else zc
    og_url = head.find("meta", property="og:url")
    if og_url:
        og_url["content"] = ec if path.is_relative_to(EN_ROOT) else zc
    if path.is_relative_to(EN_ROOT):
        import json
        from bs4 import NavigableString

        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string or '"url"' not in script.string:
                continue
            try:
                data = json.loads(script.string)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                u = data.get("url")
                if isinstance(u, str) and u.startswith("https://guoyitangus.com") and "/en/" not in u:
                    if u.rstrip("/") == zc.rstrip("/"):
                        data["url"] = ec
            script.clear()
            script.append(NavigableString(json.dumps(data, ensure_ascii=False)))

    path.write_text(str(soup), encoding="utf-8")
    print("patched", path.relative_to(ROOT))


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        if p.name in ("reference.html", "sample7.html"):
            continue
        patch_file(p)
    for p in sorted(EN_ROOT.rglob("*.html")):
        patch_file(p)


if __name__ == "__main__":
    main()
