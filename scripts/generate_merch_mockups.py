#!/usr/bin/env python3
"""Generate flat VIVE merch mockups as standalone SVGs in assets/merch/.

These are prototype mockups in the brand palette, not product photography.
The VIVE wordmark is drawn as polygons because SVGs loaded through <img>
cannot use the page's web fonts.

Run: python3 scripts/generate_merch_mockups.py
"""
from pathlib import Path

O, N, S, W, D = "#F27A21", "#2B3990", "#F4BD6A", "#F9F9F9", "#1D2766"
OUT = Path(__file__).resolve().parent.parent / "assets" / "merch"

STAR = [(50, 0), (59.5, 20.8), (79.4, 9.5), (77, 32.3), (97.6, 34.5), (84.6, 50), (97.6, 65.5),
        (77, 67.7), (79.4, 90.5), (59.5, 79.2), (50, 100), (40.5, 79.2), (20.6, 90.5), (23, 67.7),
        (2.4, 65.5), (15.4, 50), (2.4, 34.5), (23, 32.3), (20.6, 9.5), (40.5, 20.8)]


def pts(points, x=0, y=0, k=1.0):
    return " ".join(f"{x + px * k:.1f},{y + py * k:.1f}" for px, py in points)


def star(cx, cy, r, fill):
    k = 2 * r / 100
    return f'<polygon fill="{fill}" points="{pts(STAR, cx - r, cy - r, k)}"/>'


def wordmark(cx, cy, h, fill, bang):
    """V!VE in block polygons; width is 2.6 * h, centered on (cx, cy)."""
    k = h / 100
    x, y = cx - 130 * k, cy - 50 * k
    v1 = [(0, 0), (22, 0), (40, 62), (58, 0), (80, 0), (52, 100), (28, 100)]
    v2 = [(px + 110, py) for px, py in v1]
    e = [(196, 0), (260, 0), (260, 20), (218, 20), (218, 40), (254, 40), (254, 60), (218, 60),
         (218, 80), (260, 80), (260, 100), (196, 100)]
    bar = [(86, 0), (104, 0), (104, 68), (86, 68)]
    dot = [(86, 80), (104, 80), (104, 100), (86, 100)]
    return (f'<g><polygon fill="{fill}" points="{pts(v1, x, y, k)}"/>'
            f'<polygon fill="{bang}" points="{pts(bar, x, y, k)}"/>'
            f'<polygon fill="{bang}" points="{pts(dot, x, y, k)}"/>'
            f'<polygon fill="{fill}" points="{pts(v2, x, y, k)}"/>'
            f'<polygon fill="{fill}" points="{pts(e, x, y, k)}"/></g>')


def shadow(cx, cy, rx, ry=14):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{D}" opacity=".18"/>'


def svg(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


ITEMS = {}

ITEMS["baseball-jersey"] = ("VIVE baseball jersey mockup", "".join([
    shadow(240, 432, 140),
    f'<path fill="{N}" d="M150 90 L200 68 Q240 96 280 68 L330 90 L412 142 L380 214 L340 194 L340 420 L140 420 L140 194 L100 214 L68 142 Z"/>',
    f'<path fill="{O}" d="M68 142 L82 132 L112 200 L100 214 Z M412 142 L398 132 L368 200 L380 214 Z"/>',
    f'<polygon fill="{W}" points="200,68 240,128 280,68 268,64 240,104 212,64"/>',
    f'<rect x="236" y="128" width="8" height="292" fill="{O}"/>',
    "".join(f'<circle cx="240" cy="{y}" r="6" fill="{S}"/>' for y in (160, 210, 260, 310, 360)),
    wordmark(240, 236, 46, W, O),
    star(312, 330, 22, S),
    f'<text x="174" y="350" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="64" fill="{S}" text-anchor="middle">IV</text>',
]))

ITEMS["running-set"] = ("VIVE running shirt and shorts mockup", "".join([
    f'<defs><pattern id="mesh" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.6" fill="#D9661A"/></pattern></defs>',
    shadow(240, 430, 200),
    f'<path fill="{O}" d="M86 112 L128 90 Q160 132 192 90 L234 112 L222 172 Q244 204 244 234 L244 404 L76 404 L76 234 Q76 204 98 172 Z"/>',
    f'<path fill="url(#mesh)" d="M76 260 L244 260 L244 404 L76 404 Z"/>',
    f'<path d="M98 172 Q160 200 222 172" stroke="{N}" stroke-width="6" fill="none"/>',
    wordmark(160, 236, 28, D, W),
    f'<path fill="{N}" d="M268 234 L436 234 L452 404 L374 404 L352 304 L330 404 L252 404 Z"/>',
    f'<rect x="268" y="226" width="168" height="24" fill="{S}"/>',
    f'<polygon fill="{W}" points="252,404 272,404 262,330"/><polygon fill="{W}" points="452,404 432,404 442,330"/>',
    star(410, 290, 14, O),
]))

ITEMS["jacket"] = ("VIVE bomber jacket mockup", "".join([
    shadow(240, 430, 190),
    f'<path fill="{N}" d="M150 100 L200 80 L280 80 L330 100 L400 150 L424 382 L382 388 L360 214 L340 204 L340 404 L140 404 L140 204 L120 214 L98 388 L56 382 L80 150 Z"/>',
    f'<polygon fill="{O}" points="194,78 240,116 286,78 302,92 240,142 178,92"/>',
    f'<rect x="140" y="390" width="200" height="22" fill="{O}"/>',
    f'<rect x="140" y="396" width="200" height="4" fill="{S}"/>',
    f'<polygon fill="{O}" points="56,382 98,388 96,408 54,402"/><polygon fill="{O}" points="424,382 382,388 384,408 426,402"/>',
    f'<line x1="240" y1="142" x2="240" y2="404" stroke="{S}" stroke-width="5"/>',
    wordmark(292, 186, 20, W, O),
    star(190, 250, 30, S),
    star(90, 250, 16, O),
]))

ITEMS["tote-bag"] = ("VIVE tote bag mockup", "".join([
    shadow(240, 434, 140),
    f'<path d="M180 168 Q180 66 240 66 Q300 66 300 168" stroke="{N}" stroke-width="16" fill="none"/>',
    f'<rect x="116" y="160" width="248" height="266" fill="{W}"/>',
    f'<rect x="116" y="160" width="248" height="14" fill="#E9E5DC"/>',
    star(240, 270, 78, O),
    wordmark(240, 382, 34, N, O),
]))

ITEMS["coasters"] = ("VIVE coaster set mockup", "".join([
    shadow(260, 418, 170, 18),
    f'<circle cx="200" cy="210" r="118" fill="{N}"/>',
    star(200, 210, 70, S),
    f'<circle cx="286" cy="292" r="118" fill="{O}"/>',
    f'<circle cx="286" cy="292" r="100" fill="none" stroke="{W}" stroke-width="4" stroke-dasharray="2 10"/>',
    wordmark(286, 292, 44, W, D),
]))

ITEMS["cap"] = ("VIVE cap mockup", "".join([
    shadow(250, 380, 170, 16),
    f'<path fill="{N}" d="M108 300 Q112 142 240 132 Q368 142 372 300 Z"/>',
    f'<path d="M240 132 Q200 200 196 300 M240 132 Q280 200 284 300" stroke="{D}" stroke-width="3" fill="none"/>',
    f'<path fill="{O}" d="M108 300 Q240 278 372 300 Q470 318 446 352 Q300 330 150 344 Q96 330 108 300 Z"/>',
    f'<circle cx="240" cy="134" r="10" fill="{S}"/>',
    wordmark(240, 236, 42, W, O),
]))

ITEMS["notebook"] = ("VIVE notebook mockup", "".join([
    shadow(250, 428, 130),
    f'<rect x="150" y="84" width="226" height="330" rx="6" fill="{W}"/>',
    f'<rect x="138" y="76" width="226" height="330" rx="6" fill="{S}"/>',
    f'<rect x="138" y="76" width="18" height="330" fill="#E2A752"/>',
    f'<rect x="322" y="76" width="14" height="330" fill="{N}"/>',
    star(246, 210, 62, N),
    wordmark(240, 352, 30, N, O),
]))

ITEMS["pens"] = ("VIVE pen set mockup", "".join([
    shadow(240, 400, 170, 16),
    *[(f'<g transform="translate(240 {cy}) rotate(-28)">'
       f'<rect x="-160" y="-13" width="290" height="26" rx="13" fill="{c}"/>'
       f'<polygon points="130,-11 170,0 130,11" fill="#D8D8D8"/>'
       f'<polygon points="160,-3 172,0 160,3" fill="{D}"/>'
       f'<rect x="-140" y="-19" width="90" height="8" rx="4" fill="{clip}"/>'
       f'</g>') for cy, c, clip in ((180, O, N), (250, N, S), (320, S, O))],
]))

ITEMS["stickers"] = ("VIVE sticker pack mockup", "".join([
    shadow(240, 436, 140),
    f'<rect x="112" y="64" width="256" height="352" rx="12" fill="{W}"/>',
    f'<rect x="132" y="84" width="216" height="92" rx="46" fill="{N}"/>',
    wordmark(240, 130, 40, W, O),
    star(190, 252, 54, S),
    f'<polygon points="300,206 344,296 256,296" fill="{O}" stroke="{W}" stroke-width="6"/>',
    f'<circle cx="190" cy="356" r="40" fill="{O}"/>',
    f'<text x="190" y="370" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="38" fill="{D}" text-anchor="middle">IV</text>',
    f'<rect x="250" y="324" width="96" height="64" fill="{S}" transform="rotate(-8 298 356)"/>',
    star(298, 356, 20, N),
]))

ITEMS["tumbler"] = ("VIVE tumbler mockup", "".join([
    shadow(240, 432, 110),
    f'<rect x="232" y="40" width="12" height="70" rx="6" fill="{O}" transform="rotate(12 238 75)"/>',
    f'<rect x="160" y="92" width="160" height="38" rx="10" fill="{D}"/>',
    f'<polygon fill="{N}" points="170,128 310,128 294,420 186,420"/>',
    f'<polygon fill="{O}" points="174,200 306,200 303,232 177,232"/>',
    wordmark(240, 290, 30, W, S),
    star(240, 366, 22, S),
]))

ITEMS["mug"] = ("VIVE mug mockup", "".join([
    shadow(250, 404, 150, 16),
    f'<path d="M332 200 Q404 200 404 262 Q404 324 332 324" stroke="{W}" stroke-width="26" fill="none"/>',
    f'<rect x="130" y="148" width="210" height="244" rx="20" fill="{W}"/>',
    f'<ellipse cx="235" cy="152" rx="104" ry="18" fill="{O}"/>',
    f'<ellipse cx="235" cy="156" rx="88" ry="11" fill="#6B2E10"/>',
    star(235, 246, 46, O),
    wordmark(235, 340, 32, N, O),
]))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, body) in ITEMS.items():
        (OUT / f"{name}.svg").write_text(svg(title, body))
    print(f"Wrote {len(ITEMS)} mockups to {OUT}")


if __name__ == "__main__":
    main()
