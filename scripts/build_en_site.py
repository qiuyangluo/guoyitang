#!/usr/bin/env python3
"""
Generate English mirror under /en from Chinese HTML sources.
Uses Google Translate (deep-translator) with glossary pre-pass and translation cache.

After regenerating HTML, run `python3 scripts/patch_nonblocking_main_css.py` so
`main.min.css` loads via preload+onload (non–render-blocking) on all pages.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "en"
CACHE_PATH = ROOT / "scripts" / ".en_translate_cache.json"

translator = GoogleTranslator(source="zh-CN", target="en")

# Protect brand / place names before machine translation
GLOSSARY_PRE = [
    ("国医堂", "Guoyitang"),
    ("纽约国医堂", "Guoyitang NYC"),
    ("法拉盛国医堂", "Guoyitang Flushing"),
    ("华美大楼", "Huamei Building"),
    ("Queens", "Queens"),
]

# Fix common mistranslations after MT
GLOSSARY_POST = [
    ("Chinese Medical Hall", "Guoyitang"),
    ("National Medical Hall", "Guoyitang"),
    ("Imperial Medical Hall", "Guoyitang"),
    ("Chinese medicine hall", "Guoyitang"),
    ("Chinese Medicine Hall", "Guoyitang"),
    # 乐 → standard pinyin Yue (not Le) for English romanization
    ("Charles Le Guixiang", "Charles Yue Guixiang"),
    ("Le Guixiang Charles", "Yue Guixiang (Charles)"),
    ("Dr. Charles Le Guixiang", "Dr. Charles Yue Guixiang"),
    ("Dr. Le Guixiang", "Dr. Yue Guixiang"),
    ("Dr. Le has", "Dr. Yue has"),
    ("Dr. Le's", "Dr. Yue's"),
    ("Le Guixiang", "Yue Guixiang"),
]

CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s))


def protect(s: str) -> str:
    for a, b in GLOSSARY_PRE:
        s = s.replace(a, b)
    return s


def post_fix(s: str) -> str:
    for a, b in GLOSSARY_POST:
        s = s.replace(a, b)
    return s


def load_cache() -> dict:
    if CACHE_PATH.is_file():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(c: dict) -> None:
    CACHE_PATH.write_text(json.dumps(c, ensure_ascii=False, indent=0), encoding="utf-8")


def translate_text(text: str, cache: dict) -> str:
    text = text.replace("\u00a0", " ")
    if not text.strip() or not has_cjk(text):
        return text
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]
    src = protect(text)
    try:
        out = translator.translate(src)
    except Exception as e:
        print("translate error:", e, "for:", text[:60])
        cache[key] = text
        return text
    out = post_fix(out)
    time.sleep(0.12)
    cache[key] = out
    return out


def translate_ld_json_raw(raw: str, cache: dict) -> str:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        if isinstance(o, str) and has_cjk(o):
            return translate_text(o, cache)
        return o

    return json.dumps(walk(data), ensure_ascii=False)


SKIP_FILES = {"reference.html", "sample7.html"}

# Chinese HTML whose /en mirror is maintained by hand (do not overwrite with MT).
SKIP_EN_TRANSLATE = frozenset(
    {
        "book.html",
        "blog/posts/tcm-yinyang-explained.html",
        "blog/posts/lixia-solar-term-wellness.html",
    }
)


def list_source_html() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.glob("*.html")):
        if p.name in SKIP_FILES:
            continue
        out.append(p)
    for p in sorted((ROOT / "blog").rglob("*.html")):
        if p.name in SKIP_FILES:
            continue
        out.append(p)
    return out


def rel_en_path(src: Path) -> Path:
    rel = src.relative_to(ROOT)
    return EN_ROOT / rel


INTERNAL_PREFIXES = (
    "/assets/",
    "/image/",
    "/video/",
    "/favicon",
    "/apple-touch",
    "/_vercel",
    "/en/",
)


def prefix_internal_href(href: str) -> str:
    if not href or href.startswith("#"):
        return href
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("mailto:") or href.startswith("tel:"):
        return href
    if href.startswith(INTERNAL_PREFIXES):
        return href
    if href.startswith("/"):
        if href == "/":
            return "/en/"
        return "/en" + href
    return href


def absolutize_asset_url(url: str) -> str:
    if not url or url.startswith("http") or url.startswith("data:") or url.startswith("mailto:"):
        return url
    if url.startswith("//"):
        return url
    # strip relative prefixes
    u = url
    while u.startswith("../"):
        u = u[3:]
    if u.startswith("assets/") or u.startswith("/assets/"):
        u = u.lstrip("/")
        return "/" + u
    if u.startswith("image/") or u.startswith("/image/"):
        u = u.lstrip("/")
        return "/" + u
    if u.startswith("video/") or u.startswith("/video/"):
        u = u.lstrip("/")
        return "/" + u
    if u.startswith("data/") or u.startswith("/data/"):
        u = u.lstrip("/")
        return "/" + u
    return url


def translate_attrs(soup: BeautifulSoup, cache: dict) -> None:
    for tag in soup.find_all(True):
        for attr in ("alt", "aria-label", "title", "placeholder", "content"):
            val = tag.get(attr)
            if val and has_cjk(val):
                tag[attr] = translate_text(val, cache)


def translate_soup(soup: BeautifulSoup, cache: dict) -> None:
    translate_attrs(soup, cache)

    for tag in soup.find_all(string=True):
        if isinstance(tag, Comment):
            s = str(tag).strip()
            if s and has_cjk(s):
                tag.replace_with(Comment(translate_text(s, cache)))
            continue
        parent = tag.parent
        if parent is None:
            continue
        if parent.name in ("script", "style", "noscript"):
            continue
        if parent.name == "script" and parent.get("type") == "application/ld+json":
            continue
        s = str(tag)
        if not has_cjk(s):
            continue
        tag.replace_with(translate_text(s, cache))

    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string
        if raw and has_cjk(raw):
            new_raw = translate_ld_json_raw(raw, cache)
            script.clear()
            script.append(NavigableString(new_raw))


def patch_links_and_assets(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(True):
        if tag.name == "a" and tag.get("href"):
            tag["href"] = prefix_internal_href(tag["href"])
        for attr in ("src", "href"):
            if tag.get(attr) and tag.name in ("link", "script", "img", "source", "video"):
                v = tag[attr]
                if v.startswith("#") or v.startswith("http") or v.startswith("mailto:") or v.startswith("tel:"):
                    continue
                if attr == "href" and tag.name == "link" and "fonts.googleapis" in v:
                    continue
                if "youtube" in v or "ytimg" in v:
                    continue
                tag[attr] = absolutize_asset_url(v)
        if tag.get("srcset"):
            parts = []
            for chunk in tag["srcset"].split(","):
                chunk = chunk.strip()
                if not chunk:
                    continue
                bits = chunk.split()
                if bits:
                    bits[0] = absolutize_asset_url(bits[0])
                    parts.append(" ".join(bits))
            tag["srcset"] = ", ".join(parts)


def set_lang_and_alternates(soup: BeautifulSoup, zh_canonical: str, en_canonical: str) -> None:
    html = soup.find("html")
    if html:
        html["lang"] = "en"
    head = soup.find("head")
    if not head:
        return
    for l in head.find_all("link", attrs={"rel": "alternate"}):
        if l.get("hreflang"):
            l.decompose()
    first = head.find("meta")
    alt_zh = soup.new_tag("link", rel="alternate", hreflang="zh-Hans", href=zh_canonical)
    alt_en = soup.new_tag("link", rel="alternate", hreflang="en", href=en_canonical)
    alt_def = soup.new_tag("link", rel="alternate", hreflang="x-default", href=zh_canonical)
    if first:
        first.insert_before(alt_zh)
        first.insert_before(alt_en)
        first.insert_before(alt_def)
    else:
        head.append(alt_zh)
        head.append(alt_en)
        head.append(alt_def)
    can = head.find("link", rel="canonical")
    if can:
        can["href"] = en_canonical
    og_url = head.find("meta", property="og:url")
    if og_url:
        og_url["content"] = en_canonical
    og_loc = head.find("meta", property="og:locale")
    if og_loc:
        og_loc["content"] = "en_US"


def zh_canonical_for(src: Path) -> str:
    rel = src.relative_to(ROOT)
    path = "/" + str(rel.with_suffix("")).replace("\\", "/")
    if path.endswith("/index"):
        path = path[: -len("index")]
    base = "https://guoyitangus.com"
    if path in ("/index", "/"):
        return base + "/"
    return base + path.rstrip("/")


def en_canonical_for(src: Path) -> str:
    z = zh_canonical_for(src)
    if z.endswith("guoyitangus.com/"):
        return "https://guoyitangus.com/en/"
    if z == "https://guoyitangus.com":
        return "https://guoyitangus.com/en/"
    return z.replace("guoyitangus.com/", "guoyitangus.com/en/")


def fix_broken_cta_attrs(soup: BeautifulSoup) -> None:
    """Remove stray URL tokens after rel=noopener on some legacy pages."""
    for a in soup.find_all("a"):
        unknown = [k for k in a.attrs if k.startswith("http")]
        for k in unknown:
            del a.attrs[k]


def process_file(src: Path, cache: dict) -> None:
    raw = src.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    fix_broken_cta_attrs(soup)
    translate_soup(soup, cache)
    patch_links_and_assets(soup)
    zc, ec = zh_canonical_for(src), en_canonical_for(src)
    set_lang_and_alternates(soup, zc, ec)
    out = rel_en_path(src)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def patch_zh_hreflang(src: Path, cache: dict) -> None:
    """Add alternate links to Chinese source (no translation)."""
    raw = src.read_text(encoding="utf-8")
    if 'hreflang="en"' in raw:
        return
    soup = BeautifulSoup(raw, "html.parser")
    head = soup.find("head")
    if not head:
        return
    zc, ec = zh_canonical_for(src), en_canonical_for(src)
    first = head.find("meta")
    alt_zh = soup.new_tag("link", rel="alternate", hreflang="zh-Hans", href=zc)
    alt_en = soup.new_tag("link", rel="alternate", hreflang="en", href=ec)
    alt_def = soup.new_tag("link", rel="alternate", hreflang="x-default", href=zc)
    if first:
        first.insert_before(alt_zh)
        first.insert_before(alt_en)
        first.insert_before(alt_def)
    else:
        head.append(alt_zh)
        head.append(alt_en)
        head.append(alt_def)
    src.write_text(str(soup), encoding="utf-8")
    print("hreflang zh:", src.relative_to(ROOT))


def main() -> None:
    EN_ROOT.mkdir(parents=True, exist_ok=True)
    cache = load_cache()
    for src in list_source_html():
        rel = src.relative_to(ROOT).as_posix()
        if rel in SKIP_EN_TRANSLATE:
            patch_zh_hreflang(src, cache)
            continue
        process_file(src, cache)
        patch_zh_hreflang(src, cache)
    save_cache(cache)
    print("done; cache entries:", len(cache))


if __name__ == "__main__":
    main()
