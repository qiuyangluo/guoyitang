#!/usr/bin/env python3
"""Replace main.min.css stylesheet link with preload+onload pattern (non-render-blocking)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"reference.html", "sample7.html"}

PAT = re.compile(
    r'<link href="([^"]*main\.min\.css)" rel="stylesheet"\s*/>',
    re.MULTILINE,
)

REPL = r'''<link rel="preload" href="\1" as="style" onload="this.onload=null;this.rel='stylesheet'"/>
<noscript><link rel="stylesheet" href="\1"></noscript>'''


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if path.name in SKIP:
            continue
        if "node_modules" in path.parts:
            continue
        raw = path.read_text(encoding="utf-8")
        if "main.min.css" not in raw:
            continue
        new, n = PAT.subn(REPL, raw, count=1)
        if n:
            path.write_text(new, encoding="utf-8")
            print("patched", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
