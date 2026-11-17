#!/usr/bin/env python3
"""Draw outline shapes as filled rings with mitered corners.

An outline used to be a polygon with a stroke. Pillow draws a wide polygon
outline as separate line segments with flat ends, so every sharp corner showed
a notch, and the SVG versions rounded each spike. This module instead fills the
area between the shape and a copy offset inward by the line width. Each
corner's inner point is where the two offset edges meet, so the lines follow
the edges into every spike in both the SVG and the PNG.

The generators import outline_svg() and outline_png(). Run this file directly
to rebuild every existing *-outline-* asset in source/deck-extract/ and
assets/shapes/ from the points and widths already stored in their SVGs:

    python3 scripts/outline_ring.py
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DIRS = [ROOT / "source" / "deck-extract", ROOT / "assets" / "shapes"]
SUPER = 4


def _signed_area(pts):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2


def inset(pts, d):
    """Offset a simple polygon inward by d, joining edges with miters."""
    sign = 1 if _signed_area(pts) > 0 else -1
    n = len(pts)
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        length = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / length * sign, dx / length * sign  # inward normal
        lines.append(((x0 + nx * d, y0 + ny * d), (dx, dy)))
    out = []
    for i in range(n):
        (px, py), (ax, ay) = lines[i - 1]
        (qx, qy), (bx, by) = lines[i]
        den = ax * by - ay * bx
        if abs(den) < 1e-9:
            out.append((qx, qy))
            continue
        t = ((qx - px) * by - (qy - py) * bx) / den
        out.append((px + ax * t, py + ay * t))
    return out


def _fmt(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def outline_svg(pts, size, color, width):
    inner = inset(pts, width)
    d = f"M{' L'.join(_fmt([p]) for p in pts)}Z M{' L'.join(_fmt([p]) for p in inner)}Z"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">\n'
            f'  <path d="{d}" fill="{color}" fill-rule="evenodd"/>\n</svg>')


def outline_png(pts, size, color, width):
    big = size * SUPER
    mask = Image.new("L", (big, big), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon([(x * SUPER, y * SUPER) for x, y in pts], fill=255)
    draw.polygon([(x * SUPER, y * SUPER) for x, y in inset(pts, width)], fill=0)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    im = Image.new("RGBA", (size, size), color)
    im.putalpha(mask)
    return im


def _parse(svg_text):
    size = int(re.search(r'viewBox="0 0 (\d+)', svg_text).group(1))
    m = re.search(r'<polygon points="([^"]+)" fill="none" stroke="(#[0-9A-Fa-f]{6})" stroke-width="([\d.]+)"', svg_text)
    if not m:
        return None
    pts = [tuple(map(float, p.split(","))) for p in m.group(1).split()]
    return pts, size, m.group(2), float(m.group(3))


def main():
    count = 0
    for d in DIRS:
        for svg_path in sorted(d.glob("*-outline-*.svg")):
            parsed = _parse(svg_path.read_text())
            if not parsed:
                print(f"skipped (not a stroked polygon): {svg_path.relative_to(ROOT)}")
                continue
            pts, size, color, width = parsed
            svg_path.write_text(outline_svg(pts, size, color, width) + "\n")
            outline_png(pts, size, color, width).save(svg_path.with_suffix(".png"), "PNG")
            count += 1
    print(f"Rebuilt {count} outline assets as mitered rings")


if __name__ == "__main__":
    main()
