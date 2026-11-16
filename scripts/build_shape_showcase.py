#!/usr/bin/env python3
"""
build_shape_showcase.py — Builds an interactive HTML showcase for all brand assets
in source/deck-extract/ and renders a high-res overview contact sheet image.
"""

import os
import subprocess

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    deck_dir = os.path.join(repo_root, "source", "deck-extract")
    html_out = os.path.join(deck_dir, "showcase.html")
    png_out = os.path.join(deck_dir, "brand-assets-contact-sheet.png")

    groups = [
        ("1. 10-Point Stars (VIVE Signature Bursts)", [
            ("star-10pt-sun", "Sun Yellow", "#F4BD6A"),
            ("star-10pt-orange", "VIVE Orange", "#F27A21"),
            ("star-10pt-navy", "VIVE Navy", "#2B3990"),
            ("star-10pt-white", "Off-White", "#F9F9F9"),
            ("star-10pt-deep", "Deep Navy", "#1D2766"),
            ("star-10pt-cream", "Cream (Decaf)", "#E4CEAF"),
            ("star-10pt-black", "Black (Extra Caffeine)", "#111111"),
            ("star-10pt-outline-sun", "Sun Outline", "#F4BD6A"),
            ("star-10pt-outline-orange", "Orange Outline", "#F27A21"),
            ("star-10pt-outline-navy", "Navy Outline", "#2B3990"),
            ("star-10pt-outline-white", "White Outline", "#F9F9F9"),
            ("star-10pt-concentric-sun-navy", "Sun + Navy Inner", "Multi"),
            ("star-10pt-concentric-navy-sun", "Navy + Sun Inner", "Multi"),
            ("star-10pt-concentric-orange-white", "Orange + White Inner", "Multi"),
            ("star-10pt-concentric-deep-sun", "Deep + Sun Inner", "Multi"),
            ("star-10pt-tilted-12deg-sun", "+12° Dynamic Tilt", "#F4BD6A"),
            ("star-10pt-tilted-minus15deg-navy", "-15° Dynamic Tilt", "#2B3990"),
            ("star-10pt-tilted-18deg-orange", "+18° Dynamic Tilt", "#F27A21"),
        ]),
        ("2. 5-Point Stars (Classic & Bold Pentagram Stars)", [
            ("star-5pt-sun", "Sun 5-Point", "#F4BD6A"),
            ("star-5pt-orange", "Orange 5-Point", "#F27A21"),
            ("star-5pt-navy", "Navy 5-Point", "#2B3990"),
            ("star-5pt-white", "White 5-Point", "#F9F9F9"),
            ("star-5pt-deep", "Deep Navy 5-Point", "#1D2766"),
            ("star-5pt-cream", "Cream 5-Point", "#E4CEAF"),
            ("star-5pt-black", "Black 5-Point", "#111111"),
            ("star-5pt-bold-sun", "Sun Bold Pop", "#F4BD6A"),
            ("star-5pt-bold-orange", "Orange Bold Pop", "#F27A21"),
            ("star-5pt-bold-navy", "Navy Bold Pop", "#2B3990"),
            ("star-5pt-bold-white", "White Bold Pop", "#F9F9F9"),
            ("star-5pt-outline-sun", "Sun 5-Pt Outline", "#F4BD6A"),
            ("star-5pt-outline-navy", "Navy 5-Pt Outline", "#2B3990"),
            ("star-5pt-concentric-sun-navy", "Sun + Navy 5-Pt Badge", "Multi"),
            ("star-5pt-concentric-navy-sun", "Navy + Sun 5-Pt Badge", "Multi"),
            ("star-5pt-tilted-12deg-sun", "+12° Tilted 5-Pt", "#F4BD6A"),
            ("star-5pt-tilted-minus15deg-navy", "-15° Tilted 5-Pt", "#2B3990"),
            ("star-5pt-tilted-18deg-orange", "+18° Tilted 5-Pt", "#F27A21"),
        ]),
        ("3. 4-Point Stars (Retro Sparkles & Diamond Flares)", [
            ("star-4pt-sun", "Sun 4-Point", "#F4BD6A"),
            ("star-4pt-orange", "Orange 4-Point", "#F27A21"),
            ("star-4pt-navy", "Navy 4-Point", "#2B3990"),
            ("star-4pt-white", "White 4-Point", "#F9F9F9"),
            ("star-4pt-deep", "Deep Navy 4-Point", "#1D2766"),
            ("star-4pt-cream", "Cream 4-Point", "#E4CEAF"),
            ("star-4pt-black", "Black 4-Point", "#111111"),
            ("star-4pt-sparkle-sun", "Sun Sparkle Flare", "#F4BD6A"),
            ("star-4pt-sparkle-orange", "Orange Sparkle Flare", "#F27A21"),
            ("star-4pt-sparkle-navy", "Navy Sparkle Flare", "#2B3990"),
            ("star-4pt-sparkle-white", "White Sparkle Flare", "#F9F9F9"),
            ("star-4pt-outline-sun", "Sun 4-Pt Outline", "#F4BD6A"),
            ("star-4pt-outline-navy", "Navy 4-Pt Outline", "#2B3990"),
            ("star-4pt-concentric-sun-navy", "Sun + Navy 4-Pt Badge", "Multi"),
            ("star-4pt-concentric-navy-sun", "Navy + Sun 4-Pt Badge", "Multi"),
            ("star-4pt-tilted-15deg-sun", "+15° Tilted 4-Pt", "#F4BD6A"),
            ("star-4pt-tilted-minus15deg-navy", "-15° Tilted 4-Pt", "#2B3990"),
        ]),
        ("4. Squares & Diamonds", [
            ("square-solid-sun", "Sun Square", "#F4BD6A"),
            ("square-solid-orange", "Orange Square", "#F27A21"),
            ("square-solid-navy", "Navy Square", "#2B3990"),
            ("square-solid-white", "White Square", "#F9F9F9"),
            ("square-solid-deep", "Deep Navy Square", "#1D2766"),
            ("square-diamond-sun", "Sun 45° Diamond", "#F4BD6A"),
            ("square-diamond-orange", "Orange 45° Diamond", "#F27A21"),
            ("square-diamond-navy", "Navy 45° Diamond", "#2B3990"),
            ("square-diamond-white", "White 45° Diamond", "#F9F9F9"),
            ("square-diamond-deep", "Deep 45° Diamond", "#1D2766"),
            ("square-chamfer-sun", "Sun Chamfer Square", "#F4BD6A"),
            ("square-chamfer-orange", "Orange Chamfer Square", "#F27A21"),
            ("square-chamfer-navy", "Navy Chamfer Square", "#2B3990"),
            ("square-chamfer-white", "White Chamfer Square", "#F9F9F9"),
            ("square-outline-sun", "Sun Square Outline", "#F4BD6A"),
            ("square-outline-navy", "Navy Square Outline", "#2B3990"),
            ("square-diamond-outline-sun", "Sun Diamond Outline", "#F4BD6A"),
            ("square-diamond-outline-navy", "Navy Diamond Outline", "#2B3990"),
            ("square-concentric-sun-navy", "Sun + Navy Nested Square", "Multi"),
            ("square-concentric-navy-sun", "Navy + Sun Nested Square", "Multi"),
        ]),
        ("5. Brand Triangles (Equilateral, Directional, Acute, and Corners)", [
            ("triangle-equilateral-sun", "Sun Equilateral", "#F4BD6A"),
            ("triangle-equilateral-orange", "Orange Equilateral", "#F27A21"),
            ("triangle-equilateral-navy", "Navy Equilateral", "#2B3990"),
            ("triangle-equilateral-white", "White Equilateral", "#F9F9F9"),
            ("triangle-down-sun", "Sun Down", "#F4BD6A"),
            ("triangle-down-navy", "Navy Down", "#2B3990"),
            ("triangle-right-sun", "Sun Right", "#F4BD6A"),
            ("triangle-left-sun", "Sun Left", "#F4BD6A"),
            ("triangle-acute-sun", "Acute Sun Energy", "#F4BD6A"),
            ("triangle-acute-orange", "Acute Orange Energy", "#F27A21"),
            ("triangle-acute-navy", "Acute Navy Energy", "#2B3990"),
            ("triangle-acute-white", "Acute White Energy", "#F9F9F9"),
            ("triangle-acute-deep", "Acute Deep Energy", "#1D2766"),
            ("triangle-acute-tilt-right-20deg-sun", "+20° Acute Sun", "#F4BD6A"),
            ("triangle-acute-tilt-left-20deg-navy", "-20° Acute Navy", "#2B3990"),
            ("triangle-outline-sun", "Sun Triangle Outline", "#F4BD6A"),
            ("triangle-outline-navy", "Navy Triangle Outline", "#2B3990"),
            ("triangle-corner-topright-navy", "Corner Top-Right", "#2B3990"),
            ("triangle-corner-topright-sun", "Corner Top-Right", "#F4BD6A"),
            ("triangle-corner-bottomleft-orange", "Corner Bottom-Left", "#F27A21"),
        ]),
        ("6. Angled Cut Banners & Ribbons (Direction A)", [
            ("banner-angled-navy", "Angled Navy Banner", "#2B3990"),
            ("banner-angled-orange", "Angled Orange Banner", "#F27A21"),
            ("banner-angled-sun", "Angled Sun Banner", "#F4BD6A"),
            ("banner-angled-white", "Angled White Banner", "#F9F9F9"),
            ("banner-angled-deep", "Angled Deep Navy Banner", "#1D2766"),
            ("banner-angled-reverse-navy", "Rev Angled Navy", "#2B3990"),
            ("banner-angled-reverse-orange", "Rev Angled Orange", "#F27A21"),
            ("banner-angled-reverse-sun", "Rev Angled Sun", "#F4BD6A"),
        ]),
        ("7. Dynamic Energy Clusters & Burst Badges", [
            ("cluster-energy-trio", "Tri-Color Energy Trio", "Multi"),
            ("cluster-star-scatter-sun", "Sun Star + Particles", "Multi"),
            ("badge-price-67-sun", "₱67 Burst Sun", "#F4BD6A"),
            ("badge-price-67-navy", "₱67 Burst Navy", "#2B3990"),
            ("badge-price-67-orange", "₱67 Burst Orange", "#F27A21"),
            ("badge-vitamins-sun", "Vitamins A, C, B9, B12", "#F4BD6A"),
            ("badge-zero-calories-navy", "0 Cal • Stevia Burst", "#2B3990"),
        ]),
        ("8. Retailer Logos (Monochromatic White)", [
            ("lawson-logo-white", "Lawson White Wordmark", "#FFFFFF"),
            ("ayala-malls-logo-white", "Ayala Malls White Logo", "#FFFFFF"),
        ])
    ]

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VIVE Brand Asset Library — Deck Extract Showcase</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --orange: #F27A21;
    --navy: #2B3990;
    --sun: #F4BD6A;
    --white: #F9F9F9;
    --deep: #1D2766;
    --dark: #0D1026;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--dark);
    color: var(--white);
    font-family: 'Montserrat', sans-serif;
    padding: 48px 40px;
    -webkit-font-smoothing: antialiased;
  }}
  header {{
    max-width: 1360px;
    margin: 0 auto 48px;
    border-bottom: 2px solid rgba(244, 189, 106, 0.2);
    padding-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  h1 {{
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: var(--sun);
  }}
  .subtitle {{
    font-size: 16px;
    color: rgba(249, 249, 249, 0.7);
    margin-top: 6px;
  }}
  .badge-count {{
    background: var(--orange);
    color: var(--white);
    font-size: 13px;
    font-weight: 900;
    padding: 6px 14px;
    border-radius: 4px;
    letter-spacing: 0.05em;
  }}
  .container {{
    max-width: 1360px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 56px;
  }}
  .section-title {{
    font-size: 22px;
    font-weight: 900;
    color: var(--white);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .section-title::before {{
    content: '';
    display: inline-block;
    width: 12px;
    height: 12px;
    background: var(--orange);
    transform: rotate(45deg);
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 18px;
  }}
  .grid.wide {{
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }}
  .card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: transform 0.15s, border-color 0.15s, background 0.15s;
  }}
  .card:hover {{
    transform: translateY(-3px);
    border-color: var(--sun);
    background: rgba(255, 255, 255, 0.06);
  }}
  .preview-box {{
    width: 100%;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
    border-radius: 6px;
    position: relative;
    overflow: hidden;
    background: repeating-conic-gradient(rgba(255,255,255,0.06) 0% 25%, transparent 0% 50%) 50% / 16px 16px;
  }}
  .preview-box.wide {{
    height: 90px;
  }}
  .preview-box img {{
    max-width: 82%;
    max-height: 82%;
    object-fit: contain;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
  }}
  .card-title {{
    font-size: 13px;
    font-weight: 800;
    color: var(--white);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
  }}
  .card-meta {{
    font-size: 11px;
    color: rgba(249, 249, 249, 0.5);
    margin-bottom: 12px;
  }}
  .links {{
    display: flex;
    gap: 8px;
    width: 100%;
  }}
  .btn {{
    flex: 1;
    display: inline-block;
    padding: 6px 0;
    font-size: 11px;
    font-weight: 800;
    text-decoration: none;
    text-align: center;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    transition: background 0.15s, color 0.15s;
  }}
  .btn-svg {{
    background: var(--navy);
    color: var(--white);
    border: 1px solid rgba(244, 189, 106, 0.3);
  }}
  .btn-svg:hover {{
    background: var(--sun);
    color: var(--navy);
  }}
  .btn-png {{
    background: var(--orange);
    color: var(--white);
  }}
  .btn-png:hover {{
    background: #ff8e38;
  }}
</style>
</head>
<body>

<header>
  <div>
    <h1>VIVE Brand Asset Showcase</h1>
    <div class="subtitle">Complete library of 10-point stars, 5-point stars, 4-point stars, squares, diamonds, triangles, banners, and retailer monochromes in SVG & high-res PNG.</div>
  </div>
  <div class="badge-count">148 SHAPE ASSETS</div>
</header>

<div class="container">
'''

    for g_title, items in groups:
        is_wide = "Banners" in g_title or "Retailer" in g_title
        grid_cls = "grid wide" if is_wide else "grid"
        preview_cls = "preview-box wide" if is_wide else "preview-box"
        html += f'  <section>\n    <h2 class="section-title">{g_title} ({len(items)})</h2>\n    <div class="{grid_cls}">\n'
        for asset_name, label, color_tag in items:
            html += f'''      <div class="card">
        <div class="{preview_cls}">
          <img src="{asset_name}.svg" alt="{label}">
        </div>
        <div class="card-title">{label}</div>
        <div class="card-meta">{asset_name}</div>
        <div class="links">
          <a class="btn btn-svg" href="{asset_name}.svg" download>SVG</a>
          <a class="btn btn-png" href="{asset_name}.png" download>PNG</a>
        </div>
      </div>\n'''
        html += '    </div>\n  </section>\n'

    html += '''</div>
</body>
</html>'''

    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Showcase HTML written to {html_out}")

    # Render high-resolution contact sheet image using Brave
    print(f"Rendering updated high-resolution contact sheet screenshot...")
    subprocess.run([
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "--headless",
        "--disable-gpu",
        "--window-size=1440,3400",
        f"--screenshot={png_out}",
        f"file://{html_out}"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Contact sheet rendered to {png_out}")

if __name__ == "__main__":
    main()
