"""Build brand.html, the unlisted VIVE Brand Kit (served at /brand).

The page shows every brand element in one place: logos, color, type, the shape
library, the approved patterns, VIVI, the cans, UI components, voice, and the
brand in use. It reads assets/shapes/ and assets/patterns/ so new files appear
on the next build. No site page links to it; it is reachable only by direct
link, and it asks search engines not to index it. Run from the repo root:
    python3 scripts/build_brand_page.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COLORS = [
    ("Orange", "#FF9447", "--orange", "Main brand color on the web. Navbar, accents, buttons, and display words."),
    ("Print orange", "#F27A21", None, "The client's original orange. Print pieces, the deck, and the can art keep it."),
    ("Navy", "#2B3990", "--navy", "Primary dark ground, headline labels, and body text on light grounds."),
    ("Sun", "#F4BD6A", "--sun", "Triangles, stars, name plates, and warm grounds."),
    ("Off-white", "#F9F9F9", "--white", "Light grounds and text on navy."),
    ("Deep navy", "#1D2766", "--deep", "Footer, facts strip, and text on orange."),
    ("Ink", "#14183F", "--ink", "The darkest ground, behind the team portraits."),
    ("Mist", "#F1F2F8", "--mist", "A quiet light ground for long reading sections."),
]

SHAPE_FAMILIES = [
    ("10-point stars", "The signature burst. Solid, spiky, outline, sparkle, two-color, and tilted.", r"^star-10pt"),
    ("5-point stars", "Bold and outline stars for badges and small accents.", r"^star-5pt"),
    ("4-point sparkles", "Small sparkles that fill gaps between larger shapes.", r"^star-4pt"),
    ("Triangles", "Equilateral, slim acute, pointer, corner, and outline triangles, set at sharp angles.", r"^triangle-"),
    ("Squares and diamonds", "Solid, chamfered, outline, two-color, and diamond squares.", r"^square-"),
    ("Angled banners", "The slanted label strips behind headings.", r"^banner-"),
    ("Badges and clusters", "Ready-made price, vitamin, and zero-calorie badges, and shape clusters.", r"^(badge|cluster)-"),
]

PATTERNS = [
    ("Confetti Toss", "confetti", "Stars, slim triangles, chamfered squares, sparkles, diamonds, and strips tossed at angles. Approved 2026-11-20.",
     [("color", "#F9F9F9"), ("warm", "#2B3990"), ("white", "#FF9447"), ("navy", "#1D2766"), ("deep", "#2B3990")], 312, 260),
    ("Confetti Sparse", "sparse", "The same shapes at about a fifth of the density, for sections with busy content.",
     [("color", "#F9F9F9"), ("warm", "#F9F9F9"), ("light", "#2B3990"), ("blue", "#2B3990")], 640, 260),
    ("Star Seal", "seal", "10-point stars set on the diagonal, each with a 4-point sparkle, plus small triangles. Never carries the VIVE logo.",
     [("color", "#F4BD6A"), ("sun", "#2B3990"), ("white", "#FF9447"), ("blue", "#14183F"), ("deep", "#2B3990")], 140, 100),
]


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def contrast(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + .05) / (y + .05)


def size(path):
    n = (ROOT / path).stat().st_size
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1048576:.1f} MB"


def nice(stem):
    words = stem.replace("10pt", "10-point").replace("5pt", "5-point").replace("4pt", "4-point")
    words = words.replace("minus", "−").replace("deg", "°").replace("-", " ")
    return words[:1].upper() + words[1:]


esc = html.escape


def color_cards():
    out = []
    for name, hexc, token, role in COLORS:
        rgb = ", ".join(str(int(hexc[i:i + 2], 16)) for i in (1, 3, 5))
        on = "#1D2766" if lum(hexc) > .3 else "#F9F9F9"
        pairs = [(n, h) for n, h in (("navy", "#2B3990"), ("deep navy", "#1D2766"), ("off-white", "#F9F9F9")) if h != hexc]
        best = max(pairs, key=lambda p: contrast(hexc, p[1]))
        tok = f"<code>var({token})</code>" if token else "<code>print only</code>"
        out.append(
            f'<li class="swatch"><div class="chip" style="background:{hexc};color:{on}">{esc(name)}</div>'
            f'<dl><dt>Hex</dt><dd>{hexc}</dd><dt>RGB</dt><dd>{rgb}</dd><dt>Token</dt><dd>{tok}</dd>'
            f'<dt>Best text</dt><dd>{best[0]}, {contrast(hexc, best[1]):.2f}:1</dd></dl><p>{esc(role)}</p></li>')
    return "\n".join(out)


def shape_sections():
    files = sorted(p.name for p in (ROOT / "assets/shapes").glob("*.svg"))
    used, out = set(), []
    for title, note, rx in SHAPE_FAMILIES:
        group = [f for f in files if re.search(rx, f) and f not in used]
        used.update(group)
        cards = "".join(
            f'<li><a href="assets/shapes/{f}" title="Open {esc(f)}"><span class="tile"><img src="assets/shapes/{f}" alt="" loading="lazy"></span>'
            f'<span class="cap">{esc(nice(f[:-4]))}</span></a></li>' for f in group)
        out.append(f'<div class="family"><h3>{esc(title)} <small>{len(group)}</small></h3><p>{esc(note)}</p><ul class="shapes">{cards}</ul></div>')
    rest = [f for f in files if f not in used]
    assert not rest, f"Unsorted shapes: {rest}"
    return "\n".join(out), len(files)


def pattern_sections():
    out = []
    for name, key, note, variants, px, shown in PATTERNS:
        cards = []
        for v, ground in variants:
            f = f"assets/patterns/{key}-{v}.svg"
            if not (ROOT / f).exists():
                continue
            cards.append(
                f'<li><a href="{f}" title="Open {key}-{v}.svg"><span class="swatch-pat" style="background:{ground} url({f}) 0 0 / {shown}px"></span>'
                f'<span class="cap">{esc(v.capitalize())} <code>{key}-{v}.svg</code></span></a></li>')
        out.append(f'<div class="family"><h3>{esc(name)}</h3><p>{esc(note)} Tile: {px}px, shown here at {shown}px.</p><ul class="pats">{"".join(cards)}</ul></div>')
    return "\n".join(out)


def asset_card(path, label, cls=""):
    return (f'<li class="{cls}"><a href="{path}" title="Open {esc(path)}"><span class="frame"><img src="{path}" alt="{esc(label)}" loading="lazy"></span>'
            f'<span class="cap">{esc(label)} <small>{size(path)}</small></span></a></li>')


def build():
    shapes_html, n_shapes = shape_sections()
    sections = [("logo", "Logo"), ("color", "Color"), ("type", "Type"), ("shapes", "Shapes"), ("patterns", "Patterns"),
                ("vivi", "VIVI"), ("cans", "Cans"), ("components", "Components"), ("voice", "Voice"), ("in-use", "In use")]
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in sections)
    logos = "".join([
        asset_card("assets/wordmark-vive-navy.png", "Wordmark, navy", "on-light"),
        asset_card("assets/wordmark-vive-white.png", "Wordmark, white", "on-dark"),
        asset_card("assets/logo-vive-navy-tagline.png", "Monogram with tagline", "on-light"),
        asset_card("assets/logo-color-variations.png", "Color variations", "on-light tall"),
        asset_card("assets/icons/icon-512.png", "App icon, VIVI on deep navy", "on-light"),
        asset_card("favicon.ico", "Favicon", "on-light small"),
    ])
    vivi = "".join(asset_card(f"assets/mascot/vivi-{p}.webp", f"VIVI {p}", "on-sun") for p in ("pointing", "running", "dizzy"))
    cans = "".join([
        asset_card("assets/can-classic-web.webp", "VIVE Classic · Your dose of good vibes · A, B9, B12, and C", "can"),
        asset_card("assets/can-glow-web.webp", "VIVE Glow · Your dose of radiant vibes · A, B7, C, and E", "can"),
        asset_card("assets/can-focus-web.webp", "VIVE Focus · Your dose of sharp vibes · B6, B9, B12, and C", "can"),
    ])
    in_use = "".join([
        asset_card("assets/poster-classic-hires.webp", "Classic poster", "poster"),
        asset_card("assets/poster-glow-hires.webp", "Glow poster", "poster"),
        asset_card("assets/poster-focus-hires.webp", "Focus poster", "poster"),
        asset_card("assets/poster-intro-hires.webp", "Intro poster", "poster"),
        asset_card("assets/video/vive-ad-cover.webp", "Ad cover", "wide"),
        asset_card("assets/og-card.png", "Share card", "wide"),
        asset_card("assets/label-classic-nutrition.webp", "Classic label and nutrition facts", "wide"),
    ])
    stationery = "".join([
        asset_card("assets/stationery/business-card-front.webp", "Business card, front", "card"),
        asset_card("assets/stationery/business-card-back.webp", "Business card, back", "card"),
        asset_card("assets/stationery/letterhead.webp", "Letterhead", "letter"),
    ])
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VIVE · Brand Kit</title>
<meta name="description" content="Every VIVE brand element in one place: logo, color, type, shapes, patterns, VIVI, cans, components, and voice.">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VIVE">
<meta property="og:title" content="VIVE Brand Kit">
<meta property="og:description" content="Every VIVE brand element in one place: logo, color, type, shapes, patterns, VIVI, cans, components, and voice.">
<meta property="og:url" content="https://vive-cola.vercel.app/brand">
<meta property="og:image" content="https://vive-cola.vercel.app/assets/og-brand-kit.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VIVE Brand Kit: the VIVE wordmark beside a fan of brand swatch cards ending with VIVI, the mascot.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="VIVE Brand Kit">
<meta name="twitter:description" content="Every VIVE brand element in one place: logo, color, type, shapes, patterns, VIVI, cans, components, and voice.">
<meta name="twitter:image" content="https://vive-cola.vercel.app/assets/og-brand-kit.png">
<meta name="twitter:image:alt" content="VIVE Brand Kit: the VIVE wordmark beside a fan of brand swatch cards ending with VIVI, the mascot.">
<link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/montserrat.css">
<link rel="stylesheet" href="site.css">
<!-- Generated by scripts/build_brand_page.py. Edit the script, not this file.
     Unlisted: no site page links here, and robots are asked not to index it. -->
<style>
  body {{ background:var(--white); color:var(--navy); }}
  .kit-head {{ position:sticky; top:0; z-index:50; display:flex; align-items:center; gap:24px; padding:16px var(--gutter); background:var(--orange); border-bottom:4px solid var(--deep); }}
  .kit-head img {{ height:30px; width:auto; }}
  .kit-head b {{ font:900 13px/1 var(--f); letter-spacing:.14em; text-transform:uppercase; color:var(--deep); }}
  .kit-head nav {{ margin-left:auto; padding:0; }}
  .kit-head ul {{ display:flex; flex-wrap:wrap; gap:4px 18px; margin:0; padding:0; list-style:none; font:800 12px/1 var(--f); letter-spacing:.06em; text-transform:uppercase; }}
  .kit-head a {{ color:var(--deep); text-decoration:none; padding:6px 0; display:inline-block; }}
  .kit-head a:hover, .kit-head a:focus-visible {{ box-shadow:inset 0 -3px var(--white); }}
  .intro {{ position:relative; background:var(--navy); color:var(--white); padding:clamp(56px,6vw,96px) var(--gutter) clamp(64px,7vw,104px); --pat-op:.5; --pat-mask:linear-gradient(100deg,#000,transparent 60%); }}
  .intro h1 {{ margin:0; font:900 clamp(48px,7vw,104px)/.9 var(--f); text-transform:uppercase; letter-spacing:-.01em; }}
  .intro h1 em {{ display:block; font-style:normal; color:var(--orange); }}
  .intro p {{ max-width:40em; margin:24px 0 0; font-size:clamp(16px,1.4vw,19px); line-height:1.6; font-weight:600; }}
  section.kit {{ padding:clamp(56px,6vw,96px) var(--gutter); scroll-margin-top:72px; }}
  section.kit:nth-of-type(even) {{ background:var(--mist); }}
  .kit > h2 {{ margin:0 0 12px; font:900 clamp(32px,4vw,56px)/.95 var(--f); text-transform:uppercase; }}
  .kit > .lede {{ max-width:46em; margin:18px 0 36px; font-size:17px; line-height:1.6; font-weight:600; color:#2a3366; }}
  .family {{ margin-top:40px; }}
  .family h3 {{ margin:0; font:900 20px/1.1 var(--f); text-transform:uppercase; }}
  .family h3 small {{ font-size:13px; color:#4a5384; margin-left:6px; }}
  .family > p {{ margin:6px 0 18px; font-size:15px; line-height:1.5; color:#3a4370; }}
  ul.grid, ul.shapes, ul.pats, ul.colors {{ list-style:none; margin:0; padding:0; display:grid; gap:16px; }}
  ul.colors {{ grid-template-columns:repeat(4,1fr); gap:20px; }}
  .swatch {{ background:#fff; box-shadow:0 10px 24px rgba(20,24,63,.08); clip-path:polygon(0 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%); }}
  .swatch .chip {{ height:120px; display:flex; align-items:flex-end; padding:14px 16px; font:900 18px/1 var(--f); text-transform:uppercase; }}
  .swatch dl {{ display:grid; grid-template-columns:auto 1fr; gap:6px 12px; margin:16px; font-size:14px; }}
  .swatch dt {{ font-weight:800; text-transform:uppercase; font-size:11px; letter-spacing:.1em; color:#4a5384; align-self:center; }}
  .swatch dd {{ margin:0; font-weight:600; }}
  .swatch p {{ margin:0 16px 18px; font-size:14px; line-height:1.5; color:#3a4370; }}
  code {{ font:600 13px/1.4 ui-monospace, Menlo, monospace; }}
  ul.shapes {{ grid-template-columns:repeat(auto-fill,minmax(132px,1fr)); }}
  ul.pats {{ grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); }}
  ul.grid {{ grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); }}
  .shapes a, .pats a, .grid a {{ display:block; text-decoration:none; color:var(--navy); }}
  .tile {{ display:grid; place-items:center; aspect-ratio:1; padding:18px; background:#fff; background-image:linear-gradient(45deg,#eceef6 25%,transparent 25%,transparent 75%,#eceef6 75%),linear-gradient(45deg,#eceef6 25%,transparent 25%,transparent 75%,#eceef6 75%); background-size:16px 16px; background-position:0 0,8px 8px; transition:transform .16s var(--ease-out); }}
  .tile img {{ max-width:100%; max-height:100%; }}
  .swatch-pat {{ display:block; height:180px; transition:transform .16s var(--ease-out); }}
  .frame {{ position:relative; display:block; aspect-ratio:4/3; background:#fff; transition:transform .16s var(--ease-out); }}
  .frame {{ overflow:hidden; }}
  /* Absolute fit: a percentage height cannot resolve inside an aspect-ratio box */
  .frame img {{ position:absolute; inset:var(--pad, 24px); width:calc(100% - 2 * var(--pad, 24px)); height:calc(100% - 2 * var(--pad, 24px)); max-width:none; object-fit:contain; }}
  .on-dark .frame {{ background:var(--navy); }}
  .on-sun .frame {{ background:var(--sun); }}
  .tall .frame {{ aspect-ratio:3/4; }}
  .small .frame {{ --pad:38%; }}
  .can .frame {{ aspect-ratio:3/4; background:var(--sun) url(assets/shapes/star-10pt-white.svg) center / 86% no-repeat; }}
  .can .frame {{ --pad:7%; }}
  .can .frame img {{ filter:drop-shadow(0 18px 16px rgba(20,24,63,.3)); }}
  .poster .frame {{ aspect-ratio:1024/1636; --pad:0px; background:var(--deep); }}
  .poster .frame img, .wide .frame img {{ object-fit:cover; }}
  .wide {{ grid-column:span 2; }}
  .wide .frame {{ aspect-ratio:16/9; --pad:0px; }}
  .stationery {{ align-items:start; grid-auto-flow:row dense; }}
  .letter {{ grid-row:span 2; }}
  .card {{ grid-column:span 2; }}
  .card .frame {{ aspect-ratio:1575/900; --pad:0px; }}
  .letter .frame {{ aspect-ratio:2121/3000; --pad:0px; background:#fff; }}
  .card .frame img, .letter .frame img {{ object-fit:cover; }}
  .sub {{ margin:48px 0 0; font:900 22px/1.1 var(--f); text-transform:uppercase; color:var(--navy); }}
  .cap {{ display:block; margin-top:10px; font-size:13px; font-weight:700; line-height:1.35; }}
  .cap small, .cap code {{ display:block; font-weight:600; color:#4a5384; font-size:12px; margin-top:2px; }}
  @media (hover:hover) and (pointer:fine) {{ a:hover > .tile, a:hover > .swatch-pat, a:hover > .frame {{ transform:translateY(-4px); }} }}
  a:focus-visible > .tile, a:focus-visible > .swatch-pat, a:focus-visible > .frame {{ outline:3px solid var(--orange); outline-offset:3px; }}
  .type-row {{ display:grid; grid-template-columns:200px 1fr; gap:24px; align-items:baseline; padding:22px 0; border-bottom:1px solid rgba(43,57,144,.14); }}
  .type-row .meta {{ font-size:13px; font-weight:700; color:#4a5384; line-height:1.5; }}
  .type-row .meta b {{ display:block; color:var(--navy); text-transform:uppercase; letter-spacing:.06em; }}
  .t-display {{ font:900 clamp(48px,6vw,88px)/.9 var(--f); text-transform:uppercase; }}
  .t-head {{ font:900 clamp(30px,3.6vw,52px)/.95 var(--f); text-transform:uppercase; }}
  .t-eyebrow {{ font:900 14px/1 var(--f); letter-spacing:.12em; text-transform:uppercase; }}
  .t-body {{ font:600 18px/1.6 var(--f); max-width:36em; }}
  .t-small {{ font:400 15px/1.6 var(--f); max-width:40em; }}
  .demo {{ display:flex; flex-wrap:wrap; align-items:center; gap:18px; padding:32px; margin-top:18px; }}
  .demo.light {{ background:#fff; }}
  .demo.dark {{ background:var(--navy); }}
  .demo.orange {{ background:var(--orange); }}
  .demo h4 {{ flex-basis:100%; margin:0; font:800 12px/1 var(--f); letter-spacing:.12em; text-transform:uppercase; color:#4a5384; }}
  .demo.dark h4 {{ color:#c8cce6; }}
  .demo.orange h4 {{ color:var(--deep); }}
  .demo .label {{ font:900 30px/1 var(--f); text-transform:uppercase; }}
  .cut-demo {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:18px; }}
  .cut-demo div {{ height:140px; display:grid; place-items:center; color:var(--white); font:900 14px/1 var(--f); letter-spacing:.1em; text-transform:uppercase; background:var(--navy); }}
  .cut-demo .c1 {{ clip-path:polygon(0 0,100% 0,100% 70%,0 100%); }}
  .cut-demo .c2 {{ clip-path:polygon(0 0,100% 0,100% calc(100% - 22px),calc(100% - 22px) 100%,0 100%); background:var(--orange); color:var(--deep); }}
  .cut-demo .c3 {{ clip-path:polygon(2% 0,100% 6%,98% 100%,0 94%); background:var(--sun); color:var(--navy); }}
  table.tokens {{ border-collapse:collapse; margin-top:18px; font-size:15px; }}
  table.tokens th, table.tokens td {{ text-align:left; padding:12px 24px 12px 0; border-bottom:1px solid rgba(43,57,144,.14); }}
  table.tokens th {{ font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:#4a5384; }}
  .voice {{ display:grid; grid-template-columns:repeat(2,1fr); gap:20px; }}
  .voice div {{ padding:28px; background:#fff; clip-path:polygon(0 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%); }}
  .voice h3 {{ margin:0 0 14px; font:900 16px/1 var(--f); letter-spacing:.08em; text-transform:uppercase; color:#4a5384; }}
  .voice ul {{ margin:0; padding:0; list-style:none; display:grid; gap:10px; font-size:17px; font-weight:700; }}
  .voice li span {{ display:block; font-size:14px; font-weight:600; color:#3a4370; }}
  .kit-foot {{ padding:32px var(--gutter); background:var(--deep); color:var(--white); font-size:14px; display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; }}
  .kit-foot a {{ color:var(--sun); }}
</style>
</head>
<body>
<header class="kit-head">
  <a href="index.html"><img src="assets/wordmark-vive-navy.png" alt="VIVE home" width="118" height="30"></a>
  <b>Brand Kit</b>
  <nav aria-label="Brand Kit sections"><ul>{toc}</ul></nav>
</header>
<main>
<section class="intro pat pat-confetti-deep" aria-labelledby="kit-title">
  <h1 id="kit-title">Everything <em>VIVE</em></h1>
  <p>Every brand element in one place: the logo, color, type, {n_shapes} shapes, three patterns, VIVI, the cans, the site's components, and the voice. Select any asset to open its file.</p>
</section>

<section class="kit" id="logo" aria-labelledby="logo-title">
  <h2 id="logo-title"><span class="label">Logo</span></h2>
  <p class="lede">The VIVE wordmark sets the middle letters as a bold exclamation mark and IV, the Roman numeral for the four vitamins in every can. Use the navy wordmark on light and orange grounds, and the white one on navy.</p>
  <ul class="grid">{logos}</ul>
</section>

<section class="kit" id="color" aria-labelledby="color-title">
  <h2 id="color-title"><span class="label">Color</span></h2>
  <p class="lede">Orange, navy, sun, and off-white are the core four. Deep navy, ink, and mist give the grounds their range. On blue grounds, patterns change color instead of fading orange.</p>
  <ul class="colors">{color_cards()}</ul>
</section>

<section class="kit" id="type" aria-labelledby="type-title">
  <h2 id="type-title"><span class="label">Type</span></h2>
  <p class="lede">Montserrat in four weights: Black for display and headings, ExtraBold for labels and buttons, SemiBold for body copy, and Regular for long notes.</p>
  <div class="type-row"><div class="meta"><b>Display</b>Black 900 · uppercase · 48 to 128px</div><div class="t-display">Your dose of good vibes</div></div>
  <div class="type-row"><div class="meta"><b>Heading</b>Black 900 · uppercase · 32 to 72px</div><div class="t-head">Pick your vibe</div></div>
  <div class="type-row"><div class="meta"><b>Eyebrow</b>Black 900 · 14px · 0.12em tracking</div><div class="t-eyebrow">VIVE Classic · The original</div></div>
  <div class="type-row"><div class="meta"><b>Body</b>SemiBold 600 · 16 to 22px</div><div class="t-body">The vitamin-charged cola. A convenient, refreshing way to get your vitamins A, B9, B12, and C from a cold can of cola.</div></div>
  <div class="type-row"><div class="meta"><b>Note</b>Regular 400 · 13 to 15px</div><div class="t-small">Merch images are design mockups. Prices are sample prototype prices.</div></div>
</section>

<section class="kit" id="shapes" aria-labelledby="shapes-title">
  <h2 id="shapes-title"><span class="label">Shapes</span></h2>
  <p class="lede">{n_shapes} vector shapes in the brand colors. Set them at sharp angles, use them generously, and keep one layer of background detail per section.</p>
  {shapes_html}
</section>

<section class="kit" id="patterns" aria-labelledby="patterns-title">
  <h2 id="patterns-title"><span class="label">Patterns</span></h2>
  <p class="lede">Three approved patterns, built by <code>scripts/build_patterns.py</code>. Use them sparingly, one per section, and never with the VIVE logo characters.</p>
  {pattern_sections()}
</section>

<section class="kit" id="vivi" aria-labelledby="vivi-title">
  <h2 id="vivi-title"><span class="label">VIVI</span></h2>
  <p class="lede">VIVI is the VIVE mascot: the V from the wordmark with a sweatband, arms, and legs. VIVI stands in the side gutters beside section titles, and on a turning star in a hero.</p>
  <ul class="grid">{vivi}</ul>
</section>

<section class="kit" id="cans" aria-labelledby="cans-title">
  <h2 id="cans-title"><span class="label">Cans</span></h2>
  <p class="lede">Three 12 oz cans, each with four vitamins for one daily need, zero calories, and 100% stevia.</p>
  <ul class="grid">{cans}</ul>
</section>

<section class="kit" id="components" aria-labelledby="components-title">
  <h2 id="components-title"><span class="label">Components</span></h2>
  <p class="lede">The site's building blocks, from <code>site.css</code>: tilted labels, angled buttons, and the brand's cuts. The buttons here are samples: hover, focus, or press them to see each state.</p>
  <div class="demo light"><h4>Labels on light</h4><span class="label">Navy label</span><span class="label orange">Orange label</span><span class="label sun">Sun label</span></div>
  <div class="demo dark"><h4>Labels on navy</h4><span class="label sun">Sun label</span><span class="label white">White label</span><span class="label orange">Orange label</span></div>
  <div class="demo light"><h4>Buttons on light</h4><button type="button" class="btn navy">Grab a VIVE!</button><button type="button" class="btn orange">See the flavors</button><button type="button" class="btn sun">Our story</button></div>
  <div class="demo dark on-dark"><h4>Buttons on navy</h4><button type="button" class="btn orange">Grab a VIVE!</button><button type="button" class="btn white">See the flavors</button><button type="button" class="btn sun">Our story</button></div>
  <div class="cut-demo" aria-hidden="true"><div class="c1">Diagonal section cut</div><div class="c2">Chamfered corner</div><div class="c3">Tilted label edge</div></div>
  <table class="tokens">
    <caption class="vh">Motion tokens</caption>
    <thead><tr><th scope="col">Motion token</th><th scope="col">Value</th><th scope="col">Use</th></tr></thead>
    <tbody>
      <tr><td><code>--ease-out</code></td><td><code>cubic-bezier(.23, 1, .32, 1)</code></td><td>Hovers, panels, and reveals</td></tr>
      <tr><td><code>--ease-pop</code></td><td><code>cubic-bezier(.2, 1.5, .4, 1)</code></td><td>Brand pops: cans, VIVI, and the cart count</td></tr>
      <tr><td><code>--cut</code></td><td><code>clamp(28px, 5vw, 72px)</code></td><td>Depth of the diagonal section cuts</td></tr>
    </tbody>
  </table>
</section>

<section class="kit" id="voice" aria-labelledby="voice-title">
  <h2 id="voice-title"><span class="label">Voice</span></h2>
  <p class="lede">Lead with the vitamins, keep stevia as reassurance, and write plain, upbeat lines.</p>
  <div class="voice">
    <div><h3>Lines</h3><ul>
      <li>The vitamin-charged cola.<span>Brand line</span></li>
      <li>Your dose of good vibes.<span>VIVE Classic</span></li>
      <li>Your dose of radiant vibes.<span>VIVE Glow</span></li>
      <li>Your dose of sharp vibes.<span>VIVE Focus</span></li>
    </ul></div>
    <div><h3>Calls to action</h3><ul>
      <li>Grab a VIVE!<span>Primary button</span></li>
      <li>Spread the vibes!<span>Posters and sharing</span></li>
      <li>Sip the vibe now!<span>The ad</span></li>
      <li>I need more VIVE<span>VIVI's sticker line</span></li>
    </ul></div>
  </div>
</section>

<section class="kit" id="in-use" aria-labelledby="in-use-title">
  <h2 id="in-use-title"><span class="label">In use</span></h2>
  <p class="lede">The posters, the ad cover, the share card, the can label, and the stationery.</p>
  <ul class="grid">{in_use}</ul>
  <h3 class="sub">Stationery</h3>
  <ul class="grid stationery">{stationery}</ul>
</section>
</main>
<footer class="kit-foot"><span>VIVE Brand Kit · unlisted page</span><a href="index.html">Back to the VIVE site</a></footer>
</body>
</html>
"""
    (ROOT / "brand.html").write_text(page)
    print("wrote brand.html with", n_shapes, "shapes")


build()
