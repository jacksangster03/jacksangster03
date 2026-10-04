#!/usr/bin/env python3
"""Generate the hero SVG for the profile README (assets/hero-light.svg, assets/hero-dark.svg).

Static and deterministic: the output depends only on the constants below, there is no
network access, and re-running without edits changes nothing. Standard library only.

    python3 scripts/generate_profile_assets.py

Edit NAME and PLACE to change the hero. The script exists to keep the light and dark
variants in sync.
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 840, 104

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", line="#30363d", grid="#21262d", text="#e6edf3", muted="#9198a1"),
    "light": dict(bg="#ffffff", line="#d0d7de", grid="#eaeef2", text="#1f2328", muted="#59636e"),
}

NAME = "Jack Sangster"
PLACE = "Madrid"


def text(x, y, s, size, fill, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def hero(theme):
    c = THEMES[theme]
    grid = "".join(f'<path d="M{x} 1V{H - 1}"/>' for x in range(30, W, 30))
    grid += "".join(f'<path d="M1 {y}H{W - 1}"/>' for y in range(30, H, 30))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{escape(NAME)}</title>
<desc id="d">{escape(NAME)}, {escape(PLACE)}.</desc>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["line"]}"/>
<g stroke="{c["grid"]}" stroke-width="1" opacity="0.8">{grid}</g>
{text(32, 66, NAME, 52, c["text"], 600)}
{text(W - 32, 66, PLACE, 16, c["muted"], 400, "end")}
</svg>
'''


def main():
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        path = ASSETS / f"hero-{theme}.svg"
        content = hero(theme)
        if not path.exists() or path.read_text() != content:
            path.write_text(content)
            print(f"wrote {path.relative_to(ASSETS.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
