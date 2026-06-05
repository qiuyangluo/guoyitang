#!/usr/bin/env python3
"""Replace site footer markup across static HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOOTER_ZH = (ROOT / "partials" / "footer-zh.html").read_text(encoding="utf-8").strip()
FOOTER_EN = (ROOT / "partials" / "footer-en.html").read_text(encoding="utf-8").strip()
FOOTER_RE = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.DOTALL)
SKIP_PARTS = {".tmp", "Aura-Cure-EMR", "sample7", "reference.html", "partials"}
SCRIPT_TAG = '<script defer src="/assets/footer-form.js"></script>'


def should_skip(path: Path) -> bool:
    text = str(path)
    return any(part in text for part in SKIP_PARTS)


def is_english(path: Path) -> bool:
    parts = path.parts
    return "en" in parts


def main() -> None:
    updated = 0
    for path in ROOT.rglob("*.html"):
        if should_skip(path):
            continue
        source = path.read_text(encoding="utf-8")
        if '<footer class="site-footer">' not in source:
            continue

        footer = FOOTER_EN if is_english(path) else FOOTER_ZH
        source = FOOTER_RE.sub(footer, source, count=1)

        if "footer-form.js" not in source:
            source = source.replace("</body>", f"{SCRIPT_TAG}\n</body>", 1)

        path.write_text(source, encoding="utf-8")
        updated += 1
        print(path.relative_to(ROOT))

    print(f"\nUpdated {updated} files.")


if __name__ == "__main__":
    main()
