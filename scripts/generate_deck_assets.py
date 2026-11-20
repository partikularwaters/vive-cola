#!/usr/bin/env python3
"""
generate_deck_assets.py — Generates exact brand spec geometric assets
(10-point stars, triangles, angled banners, clusters, and badges)
in vector SVG and high-resolution alpha-transparent PNG.

Output directories:
- source/deck-extract/ (deck source assets)
- assets/shapes/ (mirror for website prototype)
"""

import os
import math
import subprocess
from PIL import Image, ImageDraw

from outline_ring import outline_png, outline_svg

# Exact Brand Palette from brand-spec.md
COLORS = {
    "sun": "#F4BD6A",       # Sun Yellow (triangles / stars)
    "orange": "#F27A21",    # VIVE Orange (primary ground)
    "navy": "#2B3990",      # VIVE Navy (primary structural contrast)
    "white": "#F9F9F9",     # Brand Off-White
    "deep": "#1D2766",      # Deep Ink / Navy
    "cream": "#E4CEAF",     # Decaffeinated flavor ground
    "black": "#111111",     # Extra Caffeine flavor ground / Black
}

# 20-vertex normalized coordinates for VIVE 10-point star (0 to 100)
STAR_SPEC_POINTS = [
    (50.0, 0.0), (59.5, 20.8), (79.4, 9.5), (77.0, 32.3), (97.6, 34.5),
    (84.6, 50.0), (97.6, 65.5), (77.0, 67.7), (79.4, 90.5), (59.5, 79.2),
    (50.0, 100.0), (40.5, 79.2), (20.6, 90.5), (23.0, 67.7), (2.4, 65.5),
    (15.4, 50.0), (2.4, 34.5), (23.0, 32.3), (20.6, 9.5), (40.5, 20.8)
]

def rotate_point(x, y, cx, cy, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    nx = cx + (x - cx) * cos_a - (y - cy) * sin_a
    ny = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return (nx, ny)

def make_star_points(size, rotation_deg=0.0, scale_factor=1.0):
    cx = size / 2.0
    cy = size / 2.0
    pts = []
    for nx, ny in STAR_SPEC_POINTS:
        # Scale to size
        x = (nx / 100.0 - 0.5) * size * scale_factor + cx
        y = (ny / 100.0 - 0.5) * size * scale_factor + cy
        if rotation_deg != 0.0:
            x, y = rotate_point(x, y, cx, cy, rotation_deg)
        pts.append((x, y))
    return pts

# Spiky variant: same 10 tip angles as the brand star, with inner vertices pulled in to
# 0.40 of the outer radius (the brand star sits near 0.61) for sharper spikes.
SPIKY_INNER_RATIO = 0.40

# Deep-cut sparkle proportion, matching star-4pt-sparkle (110 / 480)
SPARKLE_INNER_RATIO = 110.0 / 480.0

def make_spiky_star_points(size, inner_ratio=SPIKY_INNER_RATIO, scale_factor=1.0, rotation_deg=0.0):
    cx = size / 2.0
    cy = size / 2.0
    outer_r = (size / 2.0) * scale_factor
    pts = []
    for i in range(20):
        # Tips at 0, 36, 72... degrees clockwise from 12 o'clock; valleys halfway between
        angle = math.radians(i * 18.0)
        radius = outer_r if i % 2 == 0 else outer_r * inner_ratio
        x = cx + radius * math.sin(angle)
        y = cy - radius * math.cos(angle)
        if rotation_deg != 0.0:
            x, y = rotate_point(x, y, cx, cy, rotation_deg)
        pts.append((x, y))
    return pts

def generate_spiky_family(size, target_dirs):
    """Spiky 10-point family. Variant set mirrors the star-4pt family: solid, sparkle, outline, concentric, tilted."""
    spiky_pts = make_spiky_star_points(size)

    # Solid (all 7 colors)
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(spiky_pts, size, hex_code)
        png = render_polygon_png(spiky_pts, size, hex_code)
        save_asset(f"star-10pt-spiky-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-spiky-{c_name}")

    # Sparkle (deep-cut spikes, 5 colors as in star-4pt-sparkle)
    sparkle_pts = make_spiky_star_points(size, inner_ratio=SPARKLE_INNER_RATIO)
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = make_svg_polygon(sparkle_pts, size, hex_code)
        png = render_polygon_png(sparkle_pts, size, hex_code)
        save_asset(f"star-10pt-spiky-sparkle-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-spiky-sparkle-{c_name}")

    # Outlines (28px stroke, inset to 0.96 as in star-10pt-outline)
    outline_pts = make_spiky_star_points(size, scale_factor=0.96)
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = outline_svg(outline_pts, size, hex_code, 28)
        png = outline_png(outline_pts, size, hex_code, 28)
        save_asset(f"star-10pt-spiky-outline-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-spiky-outline-{c_name}")

    # Concentric two-tone badges (inner star at 0.62 scale, as in star-10pt-concentric)
    concentric_pairs = [
        ("sun-navy", "sun", "navy"),
        ("navy-sun", "navy", "sun"),
        ("orange-white", "orange", "white"),
        ("deep-sun", "deep", "sun")
    ]
    inner_pts = make_spiky_star_points(size, scale_factor=0.62)
    for pair_name, outer_c, inner_c in concentric_pairs:
        outer_hex = COLORS[outer_c]
        inner_hex = COLORS[inner_c]
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in spiky_pts)}" fill="{outer_hex}"/>
  <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in inner_pts)}" fill="{inner_hex}"/>
</svg>'''
        super_scale = 4
        large_size = size * super_scale
        im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.polygon([(x * super_scale, y * super_scale) for x, y in spiky_pts], fill=outer_hex)
        draw.polygon([(x * super_scale, y * super_scale) for x, y in inner_pts], fill=inner_hex)
        png = im.resize((size, size), Image.Resampling.LANCZOS)
        save_asset(f"star-10pt-spiky-concentric-{pair_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-spiky-concentric-{pair_name}")

    # Tilted (same three angles and colors as star-4pt-tilted)
    tilted_spiky = [
        ("tilted-15deg-sun", 15.0, "sun"),
        ("tilted-minus15deg-navy", -15.0, "navy"),
        ("tilted-25deg-orange", 25.0, "orange")
    ]
    for t_name, angle, c_name in tilted_spiky:
        hex_code = COLORS[c_name]
        pts = make_spiky_star_points(size, rotation_deg=angle)
        svg = make_svg_polygon(pts, size, hex_code)
        png = render_polygon_png(pts, size, hex_code)
        save_asset(f"star-10pt-spiky-{t_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-spiky-{t_name}")

def render_polygon_png(pts, size, fill_color, stroke_color=None, stroke_width=0):
    super_scale = 4
    large_size = size * super_scale
    im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    scaled_pts = [(x * super_scale, y * super_scale) for x, y in pts]
    draw.polygon(scaled_pts, fill=fill_color, outline=stroke_color, width=int(stroke_width * super_scale))
    
    final_im = im.resize((size, size), Image.Resampling.LANCZOS)
    return final_im

def make_svg_polygon(pts, size, fill_color, stroke_color=None, stroke_width=0):
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    stroke_attr = f' stroke="{stroke_color}" stroke-width="{stroke_width}"' if stroke_color and stroke_width > 0 else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <polygon points="{pts_str}" fill="{fill_color}"{stroke_attr}/>
</svg>'''

def badge_font_css(text):
    """@font-face rules that embed Montserrat Black for `text` as base64 WOFF2.

    The badges are shown with <img>, and browsers block every external load
    inside an image SVG (an @import of Google Fonts or of assets/fonts/ alike),
    so the font travels inside the file. It is subset to the badge's own
    glyphs from the self-hosted files in assets/fonts/ and pinned to weight
    900. Latin letters and the peso sign live in different files, so each
    file contributes its own rule."""
    import base64
    import io
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    fonts = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")
    rules = []
    for part in ("latin", "latin-ext"):
        font = TTFont(os.path.join(fonts, f"montserrat-{part}.woff2"))
        chars = "".join(sorted({c for c in text if ord(c) in font.getBestCmap()}))
        if not chars.strip():
            continue
        font = instancer.instantiateVariableFont(font, {"wght": 900})
        sub = subset.Subsetter(subset.Options(flavor="woff2", layout_features=["kern"], name_IDs=["*"]))
        sub.populate(text=chars)
        sub.subset(font)
        font.flavor = "woff2"
        buf = io.BytesIO()
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
        rules.append("@font-face { font-family: 'Montserrat'; font-weight: 900; "
                     f"src: url(data:font/woff2;base64,{data}) format('woff2'); }}")
    return "\n      ".join(rules)

def save_asset(name, svg_content, png_image, dirs):
    for d in dirs:
        svg_path = os.path.join(d, f"{name}.svg")
        png_path = os.path.join(d, f"{name}.png")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content.strip() + "\n")
        png_image.save(png_path, "PNG")

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dirs = [
        os.path.join(repo_root, "source", "deck-extract"),
        os.path.join(repo_root, "assets", "shapes")
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    print(f"Generating assets into {target_dirs}...")
    size = 1024

    # -------------------------------------------------------------
    # 1. 10-Point Stars (Solid)
    # -------------------------------------------------------------
    star_pts = make_star_points(size)
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(star_pts, size, hex_code)
        png = render_polygon_png(star_pts, size, hex_code)
        save_asset(f"star-10pt-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-{c_name}")

    # -------------------------------------------------------------
    # 2. 10-Point Stars (Outlines)
    # -------------------------------------------------------------
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        pts = make_star_points(size, scale_factor=0.96)
        svg = outline_svg(pts, size, hex_code, 28)
        png = outline_png(pts, size, hex_code, 28)
        save_asset(f"star-10pt-outline-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-outline-{c_name}")

    # -------------------------------------------------------------
    # 3. 10-Point Stars (Concentric Badges)
    # -------------------------------------------------------------
    concentric_pairs = [
        ("sun-navy", "sun", "navy"),
        ("navy-sun", "navy", "sun"),
        ("orange-white", "orange", "white"),
        ("deep-sun", "deep", "sun")
    ]
    for pair_name, outer_c, inner_c in concentric_pairs:
        outer_hex = COLORS[outer_c]
        inner_hex = COLORS[inner_c]
        outer_pts = make_star_points(size, scale_factor=1.0)
        inner_pts = make_star_points(size, scale_factor=0.62)
        
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in outer_pts)}" fill="{outer_hex}"/>
  <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in inner_pts)}" fill="{inner_hex}"/>
</svg>'''
        super_scale = 4
        large_size = size * super_scale
        im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.polygon([(x * super_scale, y * super_scale) for x, y in outer_pts], fill=outer_hex)
        draw.polygon([(x * super_scale, y * super_scale) for x, y in inner_pts], fill=inner_hex)
        png = im.resize((size, size), Image.Resampling.LANCZOS)
        save_asset(f"star-10pt-concentric-{pair_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-concentric-{pair_name}")

    # -------------------------------------------------------------
    # 4. 10-Point Stars (Tilted Angles)
    # -------------------------------------------------------------
    tilted_stars = [
        ("tilted-12deg-sun", 12.0, "sun"),
        ("tilted-minus15deg-navy", -15.0, "navy"),
        ("tilted-18deg-orange", 18.0, "orange"),
    ]
    for t_name, angle, c_name in tilted_stars:
        hex_code = COLORS[c_name]
        pts = make_star_points(size, rotation_deg=angle)
        svg = make_svg_polygon(pts, size, hex_code)
        png = render_polygon_png(pts, size, hex_code)
        save_asset(f"star-10pt-{t_name}", svg, png, target_dirs)
        print(f"Generated: star-10pt-{t_name}")

    # -------------------------------------------------------------
    # 4b. 10-Point Star (Spiky family, same variant set as star-4pt)
    # -------------------------------------------------------------
    generate_spiky_family(size, target_dirs)

    # -------------------------------------------------------------
    # 5. Triangles (Equilateral — 0°, 90°, 180°, 270°)
    # -------------------------------------------------------------
    # Center = (512, 512), radius = 500
    r = 490
    cx, cy = size / 2.0, size / 2.0 + 35
    equi_up = [
        (cx, cy - r),
        (cx + r * math.cos(math.radians(30)), cy + r * math.sin(math.radians(30))),
        (cx - r * math.cos(math.radians(30)), cy + r * math.sin(math.radians(30)))
    ]
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(equi_up, size, hex_code)
        png = render_polygon_png(equi_up, size, hex_code)
        save_asset(f"triangle-equilateral-{c_name}", svg, png, target_dirs)
        print(f"Generated: triangle-equilateral-{c_name}")

    # Rotated Equilaterals (Down, Right, Left)
    directional = [
        ("down", 180.0),
        ("right", 90.0),
        ("left", 270.0)
    ]
    for d_name, d_rot in directional:
        pts = [rotate_point(x, y, size/2.0, size/2.0, d_rot) for x, y in equi_up]
        for c_name in ["sun", "navy", "orange", "white"]:
            hex_code = COLORS[c_name]
            svg = make_svg_polygon(pts, size, hex_code)
            png = render_polygon_png(pts, size, hex_code)
            save_asset(f"triangle-{d_name}-{c_name}", svg, png, target_dirs)
            print(f"Generated: triangle-{d_name}-{c_name}")

    # -------------------------------------------------------------
    # 6. Triangles (Acute / Dynamic — Sharp Energy Triangles)
    # -------------------------------------------------------------
    acute_pts = [
        (cx, 40),
        (cx + 260, 960),
        (cx - 260, 960)
    ]
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = make_svg_polygon(acute_pts, size, hex_code)
        png = render_polygon_png(acute_pts, size, hex_code)
        save_asset(f"triangle-acute-{c_name}", svg, png, target_dirs)
        print(f"Generated: triangle-acute-{c_name}")

    # Tilted Dynamic Acute Triangles
    tilted_acute = [
        ("tilt-right-20deg-sun", 20.0, "sun"),
        ("tilt-left-20deg-navy", -20.0, "navy"),
        ("tilt-right-35deg-orange", 35.0, "orange"),
        ("tilt-left-35deg-sun", -35.0, "sun")
    ]
    for a_name, angle, c_name in tilted_acute:
        hex_code = COLORS[c_name]
        pts = [rotate_point(x, y, size/2.0, size/2.0, angle) for x, y in acute_pts]
        svg = make_svg_polygon(pts, size, hex_code)
        png = render_polygon_png(pts, size, hex_code)
        save_asset(f"triangle-acute-{a_name}", svg, png, target_dirs)
        print(f"Generated: triangle-acute-{a_name}")

    # -------------------------------------------------------------
    # 7. Triangles (Outline / Wireframe)
    # -------------------------------------------------------------
    for c_name in ["sun", "navy", "orange", "white"]:
        hex_code = COLORS[c_name]
        pts = equi_up
        svg = outline_svg(pts, size, hex_code, 32)
        png = outline_png(pts, size, hex_code, 32)
        save_asset(f"triangle-outline-{c_name}", svg, png, target_dirs)
        print(f"Generated: triangle-outline-{c_name}")

    # -------------------------------------------------------------
    # 8. Right-Angled Corner Wedges
    # -------------------------------------------------------------
    corners = [
        ("topright-navy", [(size, 0), (size, size), (0, 0)], "navy"),
        ("topright-sun", [(size, 0), (size, size), (0, 0)], "sun"),
        ("bottomleft-orange", [(0, 0), (0, size), (size, size)], "orange"),
        ("bottomright-navy", [(size, 0), (size, size), (0, size)], "navy")
    ]
    for c_label, c_pts, c_color in corners:
        hex_code = COLORS[c_color]
        svg = make_svg_polygon(c_pts, size, hex_code)
        png = render_polygon_png(c_pts, size, hex_code)
        save_asset(f"triangle-corner-{c_label}", svg, png, target_dirs)
        print(f"Generated: triangle-corner-{c_label}")

    # -------------------------------------------------------------
    # 9. Angled Banners & Direction A Tilted Ribbons
    # -------------------------------------------------------------
    bw, bh = 1200, 240
    banner_pts = [
        (0.02 * bw, 0),
        (1.00 * bw, 0.06 * bh),
        (0.98 * bw, 1.00 * bh),
        (0.00 * bw, 0.94 * bh)
    ]
    banner_rev_pts = [
        (0.00 * bw, 0.06 * bh),
        (0.98 * bw, 0),
        (1.00 * bw, 0.94 * bh),
        (0.02 * bw, 1.00 * bh)
    ]
    for c_name in ["navy", "orange", "sun", "white", "deep"]:
        hex_code = COLORS[c_name]
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in banner_pts)
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw} {bh}" width="{bw}" height="{bh}">
  <polygon points="{pts_str}" fill="{hex_code}"/>
</svg>'''
        im = Image.new("RGBA", (bw * 2, bh * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.polygon([(x * 2, y * 2) for x, y in banner_pts], fill=hex_code)
        png = im.resize((bw, bh), Image.Resampling.LANCZOS)
        save_asset(f"banner-angled-{c_name}", svg, png, target_dirs)
        print(f"Generated: banner-angled-{c_name}")

    for c_name in ["navy", "orange", "sun"]:
        hex_code = COLORS[c_name]
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in banner_rev_pts)
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw} {bh}" width="{bw}" height="{bh}">
  <polygon points="{pts_str}" fill="{hex_code}"/>
</svg>'''
        im = Image.new("RGBA", (bw * 2, bh * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.polygon([(x * 2, y * 2) for x, y in banner_rev_pts], fill=hex_code)
        png = im.resize((bw, bh), Image.Resampling.LANCZOS)
        save_asset(f"banner-angled-reverse-{c_name}", svg, png, target_dirs)
        print(f"Generated: banner-angled-reverse-{c_name}")

    # -------------------------------------------------------------
    # 10. Multi-Shape Dynamic Energy Clusters
    # -------------------------------------------------------------
    # Energy Trio: overlapping Sun, Navy, Orange triangles
    cluster_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <polygon points="512,120 840,780 184,780" fill="{COLORS['navy']}" transform="rotate(15 512 512)"/>
  <polygon points="512,160 810,760 214,760" fill="{COLORS['orange']}" transform="rotate(-10 512 512)"/>
  <polygon points="512,200 780,740 244,740" fill="{COLORS['sun']}"/>
</svg>'''
    im = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    # We can write an html wrapper and render it crisp with Brave
    with open("/tmp/cluster_trio.html", "w") as f:
        f.write(f'''<!DOCTYPE html><html><body style="margin:0;background:transparent;width:1024px;height:1024px;overflow:hidden;">{cluster_svg}</body></html>''')
    subprocess.run([
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "--headless", "--disable-gpu", "--default-background-color=00000000",
        "--window-size=1024,1024", "--screenshot=/tmp/cluster_trio.png",
        "file:///tmp/cluster_trio.html"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    trio_png = Image.open("/tmp/cluster_trio.png")
    save_asset("cluster-energy-trio", cluster_svg, trio_png, target_dirs)
    print("Generated: cluster-energy-trio")

    # Star + Particles Scatter
    star_scatter_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <!-- Outer scatter triangles -->
  <polygon points="180,240 220,310 140,310" fill="{COLORS['navy']}" transform="rotate(-25 180 275)"/>
  <polygon points="860,260 900,330 820,330" fill="{COLORS['orange']}" transform="rotate(30 860 295)"/>
  <polygon points="140,740 180,810 100,810" fill="{COLORS['sun']}" transform="rotate(45 140 775)"/>
  <polygon points="880,720 920,790 840,790" fill="{COLORS['deep']}" transform="rotate(-15 880 755)"/>
  <polygon points="512,60 540,110 484,110" fill="{COLORS['orange']}"/>
  <polygon points="512,940 540,990 484,990" fill="{COLORS['navy']}" transform="rotate(180 512 965)"/>
  <!-- Central 10-point Sun Star -->
  <polygon points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in make_star_points(1024, scale_factor=0.68))}" fill="{COLORS['sun']}"/>
</svg>'''
    with open("/tmp/cluster_scatter.html", "w") as f:
        f.write(f'''<!DOCTYPE html><html><body style="margin:0;background:transparent;width:1024px;height:1024px;overflow:hidden;">{star_scatter_svg}</body></html>''')
    subprocess.run([
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "--headless", "--disable-gpu", "--default-background-color=00000000",
        "--window-size=1024,1024", "--screenshot=/tmp/cluster_scatter.png",
        "file:///tmp/cluster_scatter.html"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    scatter_png = Image.open("/tmp/cluster_scatter.png")
    save_asset("cluster-star-scatter-sun", star_scatter_svg, scatter_png, target_dirs)
    print("Generated: cluster-star-scatter-sun")

    # -------------------------------------------------------------
    # 11. Ready-to-Use Brand Burst Badges (with Montserrat Typography)
    # -------------------------------------------------------------
    badges = [
        ("badge-price-67-sun", COLORS['sun'], COLORS['navy'], "₱67", "ONLY"),
        ("badge-price-67-navy", COLORS['navy'], COLORS['sun'], "₱67", "ONLY"),
        ("badge-price-67-orange", COLORS['orange'], COLORS['white'], "₱67", "ONLY"),
        ("badge-vitamins-sun", COLORS['sun'], COLORS['navy'], "VIT A, C", "B9, B12"),
        ("badge-zero-calories-navy", COLORS['navy'], COLORS['sun'], "0 CAL", "STEVIA")
    ]
    for b_name, bg_color, text_color, line1, line2 in badges:
        pts = make_star_points(size, scale_factor=0.96)
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        badge_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
  html, body {{
    margin: 0; padding: 0; width: 1024px; height: 1024px;
    background: transparent; overflow: hidden;
    font-family: 'Montserrat', sans-serif;
  }}
  .wrap {{
    position: relative; width: 1024px; height: 1024px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center;
  }}
  svg {{
    position: absolute; top: 0; left: 0; width: 1024px; height: 1024px; z-index: 1;
  }}
  .text {{
    position: relative; z-index: 2; color: {text_color};
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    line-height: 0.95;
  }}
  .l1 {{
    font-size: 190px; font-weight: 900; letter-spacing: -0.04em;
  }}
  .l2 {{
    font-size: 80px; font-weight: 900; letter-spacing: 0.16em; margin-top: 10px;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="wrap">
  <svg viewBox="0 0 1024 1024">
    <polygon points="{pts_str}" fill="{bg_color}"/>
  </svg>
  <div class="text">
    <div class="l1">{line1}</div>
    <div class="l2">{line2}</div>
  </div>
</div>
</body>
</html>'''
        tmp_html = f"/tmp/{b_name}.html"
        tmp_png = f"/tmp/{b_name}.png"
        with open(tmp_html, "w") as f:
            f.write(badge_html)
        subprocess.run([
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "--headless", "--disable-gpu", "--default-background-color=00000000",
            "--window-size=1024,1024", f"--screenshot={tmp_png}",
            f"file://{tmp_html}"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        b_png = Image.open(tmp_png)
        
        # Self-contained SVG badge with text embedded
        badge_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <style>
      {badge_font_css(line1 + line2)}
      .badge-text {{ font-family: 'Montserrat', 'Avenir Next', Arial, sans-serif; font-weight: 900; text-anchor: middle; }}
    </style>
  </defs>
  <polygon points="{pts_str}" fill="{bg_color}"/>
  <text class="badge-text" x="512" y="490" font-size="190" fill="{text_color}" letter-spacing="-4">{line1}</text>
  <text class="badge-text" x="512" y="600" font-size="80" fill="{text_color}" letter-spacing="12">{line2}</text>
</svg>'''
        save_asset(b_name, badge_svg, b_png, target_dirs)
        print(f"Generated: {b_name}")

    print("\nAll brand assets successfully generated!")

if __name__ == "__main__":
    main()
