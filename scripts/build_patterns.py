"""Build the brand pattern tiles into assets/patterns/: Confetti Toss (approved 2026-11-20) and
Star Seal (approved 2026-11-20, with a sparkle in each star and no VIVE logo).

The shapes and their placement come from design-demos/shape-patterns-build/shapes_lib.py.
Each tile is a standalone 520x520 SVG with a transparent ground, so CSS sets the
section color and the tile's opacity. Run from the repo root:
    python3 scripts/build_patterns.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "design-demos/shape-patterns-build"))
import shapes_lib as S  # noqa: E402

ORANGE, NAVY, SUN, WHITE, DEEP = "#FF9447", "#2B3990", "#F4BD6A", "#F9F9F9", "#1D2766"

TILES = {
    # Full brand colors, for cream, white, and mist grounds
    "confetti-color": (ORANGE, NAVY, SUN),
    # Warm set for navy and deep grounds
    "confetti-warm": (ORANGE, SUN, WHITE),
    # Single-color tiles for quiet tone-on-tone layers; CSS lowers their opacity
    "confetti-white": (WHITE, WHITE, WHITE),
    "confetti-deep": (DEEP, DEEP, DEEP),
    "confetti-navy": (NAVY, NAVY, NAVY),
}

def tile(c1, c2, c3):
    pat = S.confetti_shapes("p", "none", c1, c2, c3)
    body = re.search(r"<g transform=\"scale\(1\)\">(.*)</g></pattern>", pat, re.S).group(1)
    body = body.replace('<rect width="520" height="520" fill="none"/>', "")
    # Concentric badges cut their inner star in the ground color; with no ground, use a contrast color
    body = body.replace('fill="none"/></g>', f'fill="{c2 if c2 != c1 else c3}" fill-opacity="{1 if c2 != c1 else 0}"/></g>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 520" width="520" height="520">'
            f"<defs>{S.SYM}</defs>{body}</svg>\n")

for name, cols in TILES.items():
    out = ROOT / f"assets/patterns/{name}.svg"
    out.write_text(tile(*cols))
    print("wrote", out.relative_to(ROOT), out.stat().st_size, "bytes")


def seal(star, mark, tri):
    """Star Seal: 10-point stars on the diagonal, each stamped with a 4-point sparkle, plus small triangles."""
    body = (f'<use href="#s10" x="6" y="6" width="58" height="58" fill="{star}"/>'
            f'<use href="#s4" x="23" y="23" width="24" height="24" fill="{mark}"/>'
            f'<use href="#s10" x="76" y="76" width="58" height="58" fill="{star}"/>'
            f'<use href="#s4" x="93" y="93" width="24" height="24" fill="{mark}"/>'
            f'<use href="#tri" x="94" y="22" width="22" height="19" fill="{tri}" transform="rotate(20 105 31)"/>'
            f'<use href="#tri" x="24" y="98" width="22" height="19" fill="{tri}" transform="rotate(-20 35 107)"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140" width="140" height="140">'
            f"<defs>{S.SYM}</defs>{body}</svg>\n")

SEALS = {
    "seal-color": (ORANGE, NAVY, NAVY),   # on sun or cream
    "seal-sun": (SUN, NAVY, ORANGE),      # on navy or deep
    "seal-white": (WHITE, "none", WHITE), # quiet tone-on-tone
}
for name, cols in SEALS.items():
    out = ROOT / f"assets/patterns/{name}.svg"
    out.write_text(seal(*cols))
    print("wrote", out.relative_to(ROOT), out.stat().st_size, "bytes")

# Web-orange pass: the shape generators write the print orange #F27A21 into assets/shapes/.
# The website uses the lighter web orange (site.css --orange), so recolor the site copies.
# Rerun this script after any shape generator.
n = 0
for svg in sorted((ROOT / "assets/shapes").glob("*.svg")):
    text = svg.read_text()
    if "#F27A21" in text:
        svg.write_text(text.replace("#F27A21", ORANGE))
        n += 1
print("recolored", n, "shape SVGs to", ORANGE)

def sparse(c1, c2, c3):
    """Confetti Sparse (2026-11-20): the Confetti Toss shapes at about a fifth of the
    density on a larger tile, so sections with busy content keep room to breathe."""
    pieces = [("s10", 40, 60, 54, c1, -12), ("tac", 300, 30, 26, c2, 22), ("cham", 520, 120, 34, c3, 18),
              ("s4", 200, 210, 22, c2, 0), ("tri", 420, 300, 46, c1, -30), ("s10k", 110, 400, 40, c3, 8),
              ("strip", 330, 500, 48, c2, -18), ("dia", 560, 470, 24, c1, 0), ("s4", 30, 560, 18, c1, 0)]
    out = []
    for kind, x, y, w, c, r in pieces:
        h = w * (2.6 if kind == "tac" else .3 if kind == "strip" else 1)
        if kind == "tac":
            w, h = w, w * 2.8
        cx, cy = x + w / 2, y + h / 2
        t = f'transform="rotate({r} {cx:.1f} {cy:.1f})"'
        if kind == "strip":
            out.append(f'<polygon points="{x+4},{y} {x+w},{y+1} {x+w-4},{y+h:.1f} {x},{y+h-1:.1f}" fill="{c}" {t}/>')
        else:
            out.append(f'<use href="#{kind}" x="{x}" y="{y}" width="{w}" height="{h:.1f}" fill="{c}" {t}/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="640" height="640">'
            f"<defs>{S.SYM}</defs>{''.join(out)}</svg>\n")

for name, cols in {"sparse-color": (ORANGE, NAVY, SUN), "sparse-warm": (ORANGE, SUN, NAVY)}.items():
    out = ROOT / f"assets/patterns/{name}.svg"
    out.write_text(sparse(*cols))
    print("wrote", out.relative_to(ROOT), out.stat().st_size, "bytes")
