#!/usr/bin/env python3
"""Inject Quarkus Club favicon links into slides/index.html (idempotent)."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "slides" / "index.html"

INJECT = """
<link rel="icon" href="./assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="./assets/favicon.png" sizes="32x32">
<link rel="apple-touch-icon" href="./assets/apple-touch-icon.png">
"""


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    if 'href="./assets/favicon.ico"' in html:
        print("Favicon already present")
        return
    m = re.search(r"<head[^>]*>", html, re.I)
    if not m:
        raise SystemExit("No <head> found in slides/index.html")
    html = html[: m.end()] + INJECT + html[m.end() :]
    HTML.write_text(html, encoding="utf-8")
    print(f"Injected favicon into {HTML}")


if __name__ == "__main__":
    main()
