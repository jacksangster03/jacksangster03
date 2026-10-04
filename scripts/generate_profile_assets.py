#!/usr/bin/env python3
"""Generate the hero SVG for the profile README (assets/hero-light.svg, assets/hero-dark.svg).

Static and deterministic: the output depends only on the constants below, there is no
network access, and re-running without edits changes nothing. Standard library only.

    python3 scripts/generate_profile_assets.py

The motif is a data -> model -> decision flow: three input signals (distinct dash styles,
so meaning does not rely on colour) converge on a node, which emits one decision line.
The accent line draws in once on load; with reduced motion enabled it is simply static.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 840, 190

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", line="#30363d", grid="#21262d",
                 text="#e6edf3", muted="#9198a1", accent="#4fd1c5", trace="#6e7681"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", line="#d0d7de", grid="#eaeef2",
                  text="#1f2328", muted="#59636e", accent="#0b7a75", trace="#8c959f"),
}

TAGLINE = "AI × SCIENCE × QUANTITATIVE SYSTEMS"
NAME = "JACK SANGSTER"
STATUS = "BUILDING"
PLACE = "MADRID, ES"
ALT = "Jack Sangster. AI × science × quantitative systems. Madrid, Spain. Currently building."


def text(x, y, s, size, fill, weight=400, spacing=0):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{sp}>{escape(s)}</text>')


def signal(kind, x0, x1, yc, amp):
    """Deterministic input signal drawn as a path between x0 and x1 centred on yc."""
    n = 40
    pts = []
    for i in range(n + 1):
        u = i / n
        if kind == "wave":
            v = math.sin(2 * math.pi * 1.5 * u)
        elif kind == "step":
            v = 1.0 if int(u * 6) % 2 == 0 else -1.0
        else:  # decaying oscillation
            v = math.sin(2 * math.pi * 3 * u) * (1 - u)
        pts.append(f"{x0 + u * (x1 - x0):.1f},{yc - v * amp:.1f}")
    return "M" + " L".join(pts)


def hero(theme):
    c = THEMES[theme]
    px0, px1, py0, py1 = 578, 808, 24, 126  # motif panel
    cy = (py0 + py1) // 2
    nx, dx = 724, 796  # node and decision marker x
    grid = "".join(f'<path d="M{x} 1V{H - 1}"/>' for x in range(30, W, 30))
    grid += "".join(f'<path d="M1 {y}H{W - 1}"/>' for y in range(30, H, 30))
    inputs = [(signal("wave", px0 + 12, nx - 22, cy - 30, 11), ""),
              (signal("step", px0 + 12, nx - 22, cy, 9), ' stroke-dasharray="6 4"'),
              (signal("decay", px0 + 12, nx - 22, cy + 30, 11), ' stroke-dasharray="1 4" stroke-linecap="round"')]
    flows = "".join(
        f'<path d="{d}" fill="none" stroke="{c["trace"]}" stroke-width="1.6"{dash}/>' for d, dash in inputs)
    links = "".join(
        f'<path d="M{nx - 22} {y}L{nx - 8} {cy}" stroke="{c["trace"]}" stroke-width="1.4"/>'
        for y in (cy - 30, cy, cy + 30))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Jack Sangster</title>
<desc id="d">{escape(ALT)}</desc>
<style>
.pulse{{animation:pulse 2.8s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
@media (prefers-reduced-motion:no-preference){{.draw{{animation:draw 2.4s .3s ease-out both}}}}
@keyframes draw{{from{{stroke-dasharray:1;stroke-dashoffset:1}}to{{stroke-dasharray:1;stroke-dashoffset:0}}}}
@media (prefers-reduced-motion:reduce){{.pulse{{animation:none}}}}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["line"]}"/>
<g stroke="{c["grid"]}" stroke-width="1" opacity="0.8">{grid}</g>
<g aria-hidden="true">
<rect x="{px0}" y="{py0}" width="{px1 - px0 + 12}" height="{py1 - py0}" rx="6" fill="{c["panel"]}" stroke="{c["line"]}"/>
{flows}{links}
<circle cx="{nx}" cy="{cy}" r="9" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2.5"/>
<path class="draw" pathLength="1" d="M{nx + 9} {cy}H{dx - 10}" stroke="{c["accent"]}" stroke-width="3" stroke-linecap="round"/>
<rect x="{dx - 10}" y="{cy - 10}" width="20" height="20" rx="3" fill="{c["accent"]}"/>
</g>
{text(32, 54, TAGLINE, 16, c["accent"], 600, 2)}
{text(32, 112, NAME, 52, c["text"], 700)}
<path d="M32 138H{W - 32}" stroke="{c["line"]}"/>
<circle class="pulse" cx="38" cy="164" r="5.5" fill="{c["accent"]}"/>
{text(54, 170, STATUS, 16, c["text"], 700, 1)}
{text(160, 170, PLACE, 16, c["muted"], 400, 1)}
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
