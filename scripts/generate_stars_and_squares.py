#!/usr/bin/env python3
"""
generate_stars_and_squares.py — Generates 4-point stars, 5-point stars,
and squares/diamonds in SVG and high-resolution alpha-transparent PNG.

Output directories:
- source/deck-extract/
- assets/shapes/
"""

import os
import math
from PIL import Image, ImageDraw

from outline_ring import outline_png, outline_svg

COLORS = {
    "sun": "#F4BD6A",       # Sun Yellow
    "orange": "#F27A21",    # VIVE Orange
    "navy": "#2B3990",      # VIVE Navy
    "white": "#F9F9F9",     # Brand Off-White
    "deep": "#1D2766",      # Deep Navy / Ink
    "cream": "#E4CEAF",     # Decaffeinated flavor ground
    "black": "#111111",     # Extra Caffeine flavor ground / Black
}

def rotate_point(x, y, cx, cy, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    nx = cx + (x - cx) * cos_a - (y - cy) * sin_a
    ny = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return (nx, ny)

def get_star_points(n_points, cx, cy, R, r, start_deg=-90.0, rotation_deg=0.0):
    pts = []
    total_steps = n_points * 2
    step_deg = 360.0 / total_steps
    for i in range(total_steps):
        angle = math.radians(start_deg + i * step_deg)
        radius = R if (i % 2 == 0) else r
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        if rotation_deg != 0.0:
            x, y = rotate_point(x, y, cx, cy, rotation_deg)
        pts.append((x, y))
    return pts

def render_polygon_png(pts, size, fill_color, stroke_color=None, stroke_width=0):
    super_scale = 4
    large_size = size * super_scale
    im = Image.new("RGBA", (large_size, large_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    scaled_pts = [(x * super_scale, y * super_scale) for x, y in pts]
    actual_fill = None if (fill_color is None or fill_color.lower() == "none") else fill_color
    draw.polygon(scaled_pts, fill=actual_fill, outline=stroke_color, width=int(stroke_width * super_scale))
    final_im = im.resize((size, size), Image.Resampling.LANCZOS)
    return final_im

def make_svg_polygon(pts, size, fill_color, stroke_color=None, stroke_width=0):
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    stroke_attr = f' stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-linejoin="round"' if stroke_color and stroke_width > 0 else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <polygon points="{pts_str}" fill="{fill_color}"{stroke_attr}/>
</svg>'''

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

    size = 1024
    cx, cy = size / 2.0, size / 2.0
    print(f"Generating 4-point stars, 5-point stars, and squares into {target_dirs}...")

    # =========================================================================
    # 1. 4-POINT STARS
    # =========================================================================
    # Standard 4-point star (balanced)
    R4, r4 = 480.0, 180.0
    pts_4pt = get_star_points(4, cx, cy, R4, r4)

    # 1a. Solid 4-Point Stars (All 7 Colors)
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(pts_4pt, size, hex_code)
        png = render_polygon_png(pts_4pt, size, hex_code)
        save_asset(f"star-4pt-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-4pt-{c_name}")

    # 1b. Acute / Sparkle 4-Point Stars (Retro Diamond Flare)
    r4_sparkle = 110.0
    pts_4pt_sparkle = get_star_points(4, cx, cy, R4, r4_sparkle)
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = make_svg_polygon(pts_4pt_sparkle, size, hex_code)
        png = render_polygon_png(pts_4pt_sparkle, size, hex_code)
        save_asset(f"star-4pt-sparkle-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-4pt-sparkle-{c_name}")

    # 1c. Outlined 4-Point Stars
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = outline_svg(pts_4pt, size, hex_code, 28)
        png = outline_png(pts_4pt, size, hex_code, 28)
        save_asset(f"star-4pt-outline-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-4pt-outline-{c_name}")

    # 1d. Concentric Two-Tone 4-Point Badges
    concentric_pairs = [
        ("sun-navy", "sun", "navy"),
        ("navy-sun", "navy", "sun"),
        ("orange-white", "orange", "white"),
        ("deep-sun", "deep", "sun")
    ]
    for pair_name, outer_c, inner_c in concentric_pairs:
        outer_hex = COLORS[outer_c]
        inner_hex = COLORS[inner_c]
        outer_pts = pts_4pt
        inner_pts = get_star_points(4, cx, cy, R4 * 0.58, r4 * 0.58)
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
        save_asset(f"star-4pt-concentric-{pair_name}", svg, png, target_dirs)
        print(f"Generated: star-4pt-concentric-{pair_name}")

    # 1e. Tilted 4-Point Stars
    tilted_4pt = [
        ("tilted-15deg-sun", 15.0, "sun"),
        ("tilted-minus15deg-navy", -15.0, "navy"),
        ("tilted-25deg-orange", 25.0, "orange")
    ]
    for t_name, angle, c_name in tilted_4pt:
        hex_code = COLORS[c_name]
        pts = get_star_points(4, cx, cy, R4, r4, rotation_deg=angle)
        svg = make_svg_polygon(pts, size, hex_code)
        png = render_polygon_png(pts, size, hex_code)
        save_asset(f"star-4pt-{t_name}", svg, png, target_dirs)
        print(f"Generated: star-4pt-{t_name}")

    # =========================================================================
    # 2. 5-POINT STARS
    # =========================================================================
    R5 = 480.0
    r5 = R5 * 0.381966  # Standard golden ratio pentagram star
    pts_5pt = get_star_points(5, cx, cy, R5, r5)

    # 2a. Solid 5-Point Stars (All 7 Colors)
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(pts_5pt, size, hex_code)
        png = render_polygon_png(pts_5pt, size, hex_code)
        save_asset(f"star-5pt-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-5pt-{c_name}")

    # 2b. Outlined 5-Point Stars
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = outline_svg(pts_5pt, size, hex_code, 28)
        png = outline_png(pts_5pt, size, hex_code, 28)
        save_asset(f"star-5pt-outline-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-5pt-outline-{c_name}")

    # 2c. Concentric Two-Tone 5-Point Badges
    for pair_name, outer_c, inner_c in concentric_pairs:
        outer_hex = COLORS[outer_c]
        inner_hex = COLORS[inner_c]
        outer_pts = pts_5pt
        inner_pts = get_star_points(5, cx, cy, R5 * 0.58, r5 * 0.58)
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
        save_asset(f"star-5pt-concentric-{pair_name}", svg, png, target_dirs)
        print(f"Generated: star-5pt-concentric-{pair_name}")

    # 2d. Tilted 5-Point Stars
    tilted_5pt = [
        ("tilted-12deg-sun", 12.0, "sun"),
        ("tilted-minus15deg-navy", -15.0, "navy"),
        ("tilted-18deg-orange", 18.0, "orange")
    ]
    for t_name, angle, c_name in tilted_5pt:
        hex_code = COLORS[c_name]
        pts = get_star_points(5, cx, cy, R5, r5, rotation_deg=angle)
        svg = make_svg_polygon(pts, size, hex_code)
        png = render_polygon_png(pts, size, hex_code)
        save_asset(f"star-5pt-{t_name}", svg, png, target_dirs)
        print(f"Generated: star-5pt-{t_name}")

    # 2e. Bold / Chubby Pop 5-Point Stars (r/R = 0.50)
    pts_5pt_bold = get_star_points(5, cx, cy, R5, R5 * 0.50)
    for c_name in ["sun", "orange", "navy", "white"]:
        hex_code = COLORS[c_name]
        svg = make_svg_polygon(pts_5pt_bold, size, hex_code)
        png = render_polygon_png(pts_5pt_bold, size, hex_code)
        save_asset(f"star-5pt-bold-{c_name}", svg, png, target_dirs)
        print(f"Generated: star-5pt-bold-{c_name}")

    # =========================================================================
    # 3. SQUARES & DIAMONDS
    # =========================================================================
    # 3a. Upright Solid Squares (800x800 centered)
    sq_size = 780.0
    half_s = sq_size / 2.0
    pts_sq = [
        (cx - half_s, cy - half_s),
        (cx + half_s, cy - half_s),
        (cx + half_s, cy + half_s),
        (cx - half_s, cy + half_s)
    ]
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(pts_sq, size, hex_code)
        png = render_polygon_png(pts_sq, size, hex_code)
        save_asset(f"square-solid-{c_name}", svg, png, target_dirs)
        print(f"Generated: square-solid-{c_name}")

    # 3b. Rotated Squares / Diamonds (45° Diamond)
    d_radius = 480.0
    pts_diamond = [
        (cx, cy - d_radius),
        (cx + d_radius, cy),
        (cx, cy + d_radius),
        (cx - d_radius, cy)
    ]
    for c_name, hex_code in COLORS.items():
        svg = make_svg_polygon(pts_diamond, size, hex_code)
        png = render_polygon_png(pts_diamond, size, hex_code)
        save_asset(f"square-diamond-{c_name}", svg, png, target_dirs)
        print(f"Generated: square-diamond-{c_name}")

    # 3c. Chamfered / Angled-Cut Squares (Direction A style, 100px corner cuts)
    cut = 120.0
    pts_chamfer = [
        (cx - half_s + cut, cy - half_s),
        (cx + half_s - cut, cy - half_s),
        (cx + half_s, cy - half_s + cut),
        (cx + half_s, cy + half_s - cut),
        (cx + half_s - cut, cy + half_s),
        (cx - half_s + cut, cy + half_s),
        (cx - half_s, cy + half_s - cut),
        (cx - half_s, cy - half_s + cut)
    ]
    for c_name in ["sun", "orange", "navy", "white", "deep"]:
        hex_code = COLORS[c_name]
        svg = make_svg_polygon(pts_chamfer, size, hex_code)
        png = render_polygon_png(pts_chamfer, size, hex_code)
        save_asset(f"square-chamfer-{c_name}", svg, png, target_dirs)
        print(f"Generated: square-chamfer-{c_name}")

    # 3d. Outlined Squares and Diamonds
    for c_name in ["sun", "orange", "navy", "white"]:
        hex_code = COLORS[c_name]
        # Square outline
        svg_sq_out = outline_svg(pts_sq, size, hex_code, 32)
        png_sq_out = outline_png(pts_sq, size, hex_code, 32)
        save_asset(f"square-outline-{c_name}", svg_sq_out, png_sq_out, target_dirs)
        print(f"Generated: square-outline-{c_name}")

        # Diamond outline
        svg_d_out = outline_svg(pts_diamond, size, hex_code, 32)
        png_d_out = outline_png(pts_diamond, size, hex_code, 32)
        save_asset(f"square-diamond-outline-{c_name}", svg_d_out, png_d_out, target_dirs)
        print(f"Generated: square-diamond-outline-{c_name}")

    # 3e. Concentric Two-Tone Square Badges
    for pair_name, outer_c, inner_c in concentric_pairs:
        outer_hex = COLORS[outer_c]
        inner_hex = COLORS[inner_c]
        outer_pts = pts_sq
        inner_half = half_s * 0.60
        inner_pts = [
            (cx - inner_half, cy - inner_half),
            (cx + inner_half, cy - inner_half),
            (cx + inner_half, cy + inner_half),
            (cx - inner_half, cy + inner_half)
        ]
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
        save_asset(f"square-concentric-{pair_name}", svg, png, target_dirs)
        print(f"Generated: square-concentric-{pair_name}")

    print("\nAll 4-point stars, 5-point stars, and squares successfully generated!")

if __name__ == "__main__":
    main()
