#!/usr/bin/env python3
"""Generate StarUI favicons (4-point star ornament).

Produces:
  static/images/favicon-light.svg  – orange star for dark backgrounds
  static/images/favicon-dark.svg   – dark navy star for light backgrounds
  static/images/apple-touch-icon.png – 180x180 with gradient background

Usage:
    uv run --extra og python generate_favicon.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT_DIR = Path(__file__).parent / "static" / "images"

SUNSET = (251, 146, 60)      # #FB923C
NAVY = (11, 18, 33)          # #0B1221
WHITE = (240, 238, 235)      # warm white


def _star_polygon(cx: float, cy: float, outer: float, inner: float) -> list[tuple]:
    """Return polygon coordinates for a 4-point star."""
    points = []
    for i in range(8):
        angle = math.radians(i * 45 - 90)
        r = outer if i % 2 == 0 else inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def _star_svg_path(cx: float, cy: float, outer: float, inner: float) -> str:
    """Return SVG path data for a 4-point star."""
    pts = _star_polygon(cx, cy, outer, inner)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for p in pts[1:]:
        d += f" L{p[0]:.1f} {p[1]:.1f}"
    d += " Z"
    return d


def generate_svg_favicons():
    """Generate SVG favicons for light/dark mode."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    viewbox = 32
    cx, cy = viewbox / 2, viewbox / 2
    outer, inner = 14, 4.5

    path_d = _star_svg_path(cx, cy, outer, inner)

    # Light favicon (orange star) — used on dark browser chrome
    light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}" width="{viewbox}" height="{viewbox}">
  <path d="{path_d}" fill="#FB923C"/>
</svg>'''

    # Dark favicon (navy star) — used on light browser chrome
    dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}" width="{viewbox}" height="{viewbox}">
  <path d="{path_d}" fill="#0B1221"/>
</svg>'''

    (OUTPUT_DIR / "favicon-light.svg").write_text(light_svg)
    print(f"  Generated: {OUTPUT_DIR / 'favicon-light.svg'}")

    (OUTPUT_DIR / "favicon-dark.svg").write_text(dark_svg)
    print(f"  Generated: {OUTPUT_DIR / 'favicon-dark.svg'}")


def generate_apple_touch_icon():
    """Generate 180x180 apple-touch-icon with gradient background."""
    size = 180
    img = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(img)

    # Fill with navy-to-warm gradient (simplified 2-stop)
    for y in range(size):
        t = y / (size - 1)
        r = int(NAVY[0] + (62 - NAVY[0]) * t)
        g = int(NAVY[1] + (76 - NAVY[1]) * t)
        b = int(NAVY[2] + (95 - NAVY[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Draw the 4-point star centered
    cx, cy = size / 2, size / 2
    outer, inner = 72, 23
    pts = _star_polygon(cx, cy, outer, inner)
    draw.polygon(pts, fill=(*SUNSET, 255))

    output = Image.new("RGB", (size, size))
    output.paste(img, mask=img.split()[3])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "apple-touch-icon.png"
    output.save(str(output_path), "PNG", optimize=True)
    print(f"  Generated: {output_path}")


def main():
    print("Generating favicons...")
    generate_svg_favicons()
    generate_apple_touch_icon()
    print("Done!")


if __name__ == "__main__":
    main()
