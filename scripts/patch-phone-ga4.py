#!/usr/bin/env python3
"""Replace inline gtag_report_phone_conversion with shared phone-analytics.js."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACEMENT = '<script src="/assets/phone-analytics.js"></script>'

# Multiline: phone conversion snippet only (before booking conversion or vercel)
PATTERN = re.compile(
    r"<script>\s*function gtag_report_phone_conversion\(url\) \{.*?\}\s*</script>\s*",
    re.DOTALL,
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "phone-analytics.js" in text:
        return False
    if "gtag_report_phone_conversion" not in text:
        return False
    new_text, n = PATTERN.subn(REPLACEMENT + "\n", text, count=1)
    if n == 0:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name == "reference.html":
            continue
        if patch_file(path):
            updated.append(path.relative_to(ROOT))
    print(f"Updated {len(updated)} files")
    for p in updated:
        print(f"  {p}")


if __name__ == "__main__":
    main()
