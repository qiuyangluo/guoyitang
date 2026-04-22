#!/usr/bin/env python3
"""
Rewrite internal links and guoyitangus.com canonicals to extensionless paths.
Requires hosting with extensionless mapping (e.g. Vercel cleanUrls).
Run from repo root: python3 scripts/strip-html-from-urls.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_absolute_path(path: str) -> str:
    """/foo.html or /blog/index.html -> extensionless path."""
    if not path.endswith(".html"):
        return path
    p = path[:-5]
    if p == "/index" or p == "":
        return "/"
    if p.endswith("/index"):
        return p[: -len("/index")] + "/"
    return p


def clean_guoyitang_url(url: str) -> str:
    from urllib.parse import urlparse, urlunparse

    prefix = "https://guoyitangus.com"
    if not url.startswith(prefix):
        return url
    u = urlparse(url)
    newpath = clean_absolute_path(u.path)
    return urlunparse((u.scheme, u.netloc, newpath, u.params, u.query, u.fragment))


def path_file_to_url(rel: Path) -> str:
    s = rel.as_posix()
    if s == "index.html":
        return "/"
    if s.endswith("/index.html"):
        return "/" + s[: -len("/index.html")] + "/"
    if s.endswith(".html"):
        return "/" + s[: -len(".html")]
    return "/" + s


def rewrite_href(href: str, current: Path) -> str | None:
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return None
    if ".html" not in href:
        return None
    cur = current.parent
    raw = href.split("#", 1)
    path_part, frag = raw[0], ("#" + raw[1] if len(raw) > 1 else "")
    target = (cur / path_part).resolve()
    try:
        rel = target.relative_to(ROOT.resolve())
    except ValueError:
        return None
    if not str(rel).endswith(".html"):
        return None
    return path_file_to_url(rel) + frag


def process_html(path: Path, text: str) -> str:
    # _template.html lives under blog/ but hrefs are authored like blog/posts/*.html
    href_base = path
    if path == ROOT / "blog" / "_template.html":
        href_base = ROOT / "blog" / "posts" / "__href_base__.html"

    if path.name == "reference.html":
        # Archive export: only normalize absolute guoyitangus.com *.html URLs
        return re.sub(
            r"https://guoyitangus\.com[^\s\"'<>]*?\.html(?:#[^\s\"'<>]+)?",
            lambda m: clean_guoyitang_url(m.group(0).rstrip(".,);")),
            text,
        )

    def href_repl(m: re.Match) -> str:
        full = m.group(0)
        inner = m.group(1)
        new = rewrite_href(inner, href_base)
        if new is None:
            return full
        return 'href="' + new + '"'

    text = re.sub(r'href="([^"]+)"', href_repl, text)

    text = re.sub(
        r"https://guoyitangus\.com[^\s\"'<>]*?\.html(?:#[^\s\"'<>]+)?",
        lambda m: clean_guoyitang_url(m.group(0).rstrip(".,);")),
        text,
    )
    return text


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        old = path.read_text(encoding="utf-8")
        new = process_html(path, old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            print("updated", path.relative_to(ROOT))

    sm = ROOT / "sitemap.xml"
    if sm.exists():
        t = sm.read_text(encoding="utf-8")

        def loc_repl(m: re.Match) -> str:
            return "<loc>" + clean_guoyitang_url(m.group(1)) + "</loc>"

        t2 = re.sub(r"<loc>(https://guoyitangus\.com[^<]+)</loc>", loc_repl, t)
        if t2 != t:
            sm.write_text(t2, encoding="utf-8")
            print("updated sitemap.xml")

    bj = ROOT / "assets" / "blog-index.js"
    if bj.exists():
        t = bj.read_text(encoding="utf-8")
        t2 = t.replace(
            'var href = "posts/" + encodeURIComponent(p.slug) + ".html";',
            'var href = "/blog/posts/" + encodeURIComponent(p.slug);',
        )
        if t2 != t:
            bj.write_text(t2, encoding="utf-8")
            print("updated assets/blog-index.js")


if __name__ == "__main__":
    main()
