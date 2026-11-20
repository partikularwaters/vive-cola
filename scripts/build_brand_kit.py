"""Build the VIVE Brand Kit catalog in brand/ (served unlisted at /brand).

The Markdown docs in brand/docs/<section>/<page>.md are the source. For each doc
this writes brand/<section>/<page>.html: the doc rendered with live specimens that
use the site's own site.css, a sidebar, search, and "Copy for agents". It also
writes brand/vive-brand-kit.md (the whole system in one file), brand/llms.txt (an
index for agents), and brand/index.html (a redirect to the introduction).

A doc marks a live example with an HTML comment, <!-- specimen: name -->, which
stays invisible in the copied Markdown. Shapes and patterns are read from
assets/shapes/ and assets/patterns/, so new files appear on the next build.
No site page links to the kit, and every page asks search engines not to index it.
Run from the repo root:
    python3 scripts/build_brand_kit.py
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
            f'<li><a href="@R@assets/shapes/{f}" title="Open {esc(f)}"><span class="tile"><img src="@R@assets/shapes/{f}" alt="" loading="lazy"></span>'
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
                f'<li><a href="@R@{f}" title="Open {key}-{v}.svg"><span class="swatch-pat" style="background:{ground} url(@R@{f}) 0 0 / {shown}px"></span>'
                f'<span class="cap">{esc(v.capitalize())} <code>{key}-{v}.svg</code></span></a></li>')
        out.append(f'<div class="family"><h3>{esc(name)}</h3><p>{esc(note)} Tile: {px}px, shown here at {shown}px.</p><ul class="pats">{"".join(cards)}</ul></div>')
    return "\n".join(out)


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------
import json
import urllib.parse

import markdown

KIT = ROOT / "brand"
DOCS = KIT / "docs"
SITE_URL = "https://vive-cola.vercel.app"
SECTIONS = [("getting-started", "Getting started"), ("foundations", "Foundations"),
            ("components", "Components"), ("blocks", "Blocks"), ("assets", "Assets")]


def asset_card(path, label, cls=""):
    return (f'<li class="{cls}"><a href="@R@{path}" title="Open {esc(path)}"><span class="frame"><img src="@R@{path}" alt="{esc(label)}" loading="lazy"></span>'
            f'<span class="cap">{esc(label)} <small>{size(path)}</small></span></a></li>')


def grid(cards, cls="grid"):
    return f'<ul class="{cls}">{"".join(cards)}</ul>'


def demo(title, body, cls="light"):
    return f'<div class="demo {cls}"><h4>{esc(title)}</h4>{body}</div>'


STAR = '<div class="burst star" style="background-image:url(@R@assets/shapes/star-10pt-sun.svg)"></div>'


def specimens():
    shapes_html, _ = shape_sections()
    return {
        "logo": grid([
            asset_card("assets/wordmark-vive-navy.png", "Wordmark, navy", "on-light"),
            asset_card("assets/wordmark-vive-white.png", "Wordmark, white", "on-dark"),
            asset_card("assets/logo-vive-navy-tagline.png", "Monogram with tagline", "on-light"),
            asset_card("assets/logo-color-variations.png", "Color variations", "on-light tall"),
            asset_card("assets/icons/icon-512.png", "App icon, VIVI on deep navy", "on-light"),
            asset_card("favicon.ico", "Favicon", "on-light small"),
        ]),
        "colors": f'<ul class="colors">{color_cards()}</ul>',
        "typography": "".join([
            '<div class="type-row"><div class="meta"><b>Display</b>Black 900 · uppercase</div><div class="t-display">Your dose of good vibes</div></div>',
            '<div class="type-row"><div class="meta"><b>Heading</b>Black 900 · uppercase</div><div class="t-head">Pick your vibe</div></div>',
            '<div class="type-row"><div class="meta"><b>Eyebrow</b>Black 900 · 0.12em tracking</div><div class="t-eyebrow">VIVE Classic · The original</div></div>',
            '<div class="type-row"><div class="meta"><b>Body</b>SemiBold 600</div><div class="t-body">The vitamin-charged cola. A convenient, refreshing way to get your vitamins A, B9, B12, and C from a cold can of cola.</div></div>',
            '<div class="type-row"><div class="meta"><b>Note</b>Regular 400</div><div class="t-small">Merch images are design mockups. Prices are sample prototype prices.</div></div>',
        ]),
        "cuts": '<div class="cut-demo" aria-hidden="true"><div class="c1">.cut-down</div><div class="c2">Chamfered corner</div><div class="c3">Tilted label edge</div></div>',
        "shapes": shapes_html,
        "patterns": pattern_sections(),
        "motion": demo("Hover each sample", '<button type="button" class="btn navy">Grab a VIVE!</button>'
                       '<div class="lift-zone mini-card" style="--tilt:-3deg"><div class="lift"><img src="@R@assets/merch/cap.webp" alt="VIVE cap mockup" width="900" height="900"></div></div>'),
        "label": demo("Labels on light", '<h2 class="lbl-row"><span class="label">Navy label</span></h2><h2 class="lbl-row"><span class="label orange">Orange label</span></h2><h2 class="lbl-row"><span class="label sun">Sun label</span></h2>')
                 + demo("Labels on navy", '<h2 class="lbl-row"><span class="label sun">The team</span><span class="label white">behind the can</span></h2>', "dark"),
        "button": demo("Buttons on light", '<button type="button" class="btn navy">Grab a VIVE!</button><button type="button" class="btn orange">See the flavors</button><button type="button" class="btn sun">Our story</button>')
                  + demo("Buttons on navy", '<button type="button" class="btn orange">Grab a VIVE!</button><button type="button" class="btn white">See the flavors</button><button type="button" class="btn sun">Our story</button>', "dark on-dark"),
        "cart-button": demo("Cart button on the orange header (sample)", '<button type="button" class="cart-btn"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 7V6a5 5 0 0 1 10 0v1h3.2l-1.3 15H5.1L3.8 7H7Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg>Cart <span class="cart-count">3</span><span class="vh"> items</span></button>', "orange"),
        "motion-toggle": f'<div class="demo dark spin-demo"><h4>Turning star with its pause button</h4>{STAR}<button class="motion-toggle" type="button"><span class="vh">Pause </span>Motion <span class="icon" aria-hidden="true"></span></button></div>',
        "hover-lift": demo("Hover the cards", "".join(
            f'<div class="lift-zone mini-card" style="--tilt:{t}"><div class="lift"><img src="@R@assets/merch/{m}.webp" alt="" width="900" height="900"></div></div>'
            for m, t in (("cap", "-1.5deg"), ("headband", "1deg"), ("mug", "-.6deg")))),
        "mascot": grid([asset_card(f"assets/mascot/vivi-{p}.webp", f"VIVI {p.replace('-', ' ')}", "on-sun") for p in ("pointing", "running", "dizzy", "need-more-vive")]),
        "site-header": '<div class="specimen-frame"><header class="site-header"><nav class="wrap" aria-label="Sample site navigation">'
                       '<a href="@R@index.html"><img src="@R@assets/wordmark-vive-navy.png" alt="VIVE home" width="125" height="32"></a>'
                       '<ul><li><a href="@R@index.html" aria-current="page">Home</a></li><li><a href="@R@about.html">About Us</a></li><li><a href="@R@product.html">Product</a></li><li><a href="@R@shop.html">Shop</a></li></ul>'
                       '<button type="button" class="cart-btn"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 7V6a5 5 0 0 1 10 0v1h3.2l-1.3 15H5.1L3.8 7H7Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg>Cart <span class="cart-count">0</span><span class="vh"> items</span></button></nav></header></div>',
        "facts-ribbon": '<div class="specimen-frame"><div class="facts wrap facts-sample"><span>Four vitamins in every can</span><span>VIVE Classic, Glow, and Focus</span><span>0 calories</span><span>12 oz can</span></div></div>',
        "section-grounds": '<div class="grounds">' + "".join(
            f'<div class="ground pat {pc}" style="background:{bg};color:{fg}"><span class="label {lc}">{esc(t)}</span><small>{esc(n)}</small></div>'
            for t, n, bg, fg, pc, lc in (
                ("Off-white", "Confetti Sparse", "var(--white)", "var(--navy)", "pat-sparse", ""),
                ("Sun", "Star Seal", "var(--sun)", "var(--navy)", "pat-seal", ""),
                ("Navy", "Blue Star Seal, full strength", "var(--navy)", "var(--white)", "pat-seal-blue full", "sun"),
                ("Ink", "Blue Star Seal", "var(--ink)", "var(--white)", "pat-seal-blue full", "orange"))) + '</div>',
        "footer": '<div class="specimen-frame footer-frame"><footer class="site-footer"></footer></div>',
        "cans": grid([asset_card(f"assets/can-{v}-web.webp", f"VIVE {v.capitalize()}", "can") for v in ("classic", "glow", "focus")]),
        "posters": grid([asset_card("assets/poster-intro-hires.webp", "Intro poster", "poster")]
                        + [asset_card(f"assets/poster-{v}-hires.webp", f"{v.capitalize()} poster", "poster") for v in ("glow", "classic", "focus")])
                   + grid([asset_card(f"assets/model-{v}-web.webp", f"{v.capitalize()} model photo", "square") for v in ("classic", "glow", "focus")])
                   + grid([asset_card("assets/mockup-intro-bus-shelter.webp", "Bus shelter mockup", "wide"),
                           asset_card("assets/video/vive-ad-cover.webp", "Ad cover", "wide"),
                           asset_card("assets/og-card.png", "Share card", "wide")]),
        "stationery": grid([asset_card("assets/stationery/business-card-front.webp", "Business card, front", "card"),
                            asset_card("assets/stationery/business-card-back.webp", "Business card, back", "card"),
                            asset_card("assets/stationery/letterhead.webp", "Letterhead", "letter")], "grid stationery"),
    }


def read_docs():
    docs = []
    for key, label in SECTIONS:
        for f in sorted((DOCS / key).glob("*.md")):
            text = f.read_text()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            assert m, f"{f}: missing front matter"
            meta = dict(line.split(": ", 1) for line in m.group(1).splitlines())
            body = text[m.end():].lstrip("\n")
            docs.append({"section": key, "section_label": label, "slug": f.stem, "title": meta["title"],
                         "summary": meta["summary"], "order": int(meta["order"]), "body": body})
    order = {k: i for i, (k, _) in enumerate(SECTIONS)}
    docs.sort(key=lambda d: (order[d["section"]], d["order"]))
    return docs


def agent_md(d):
    """The Markdown handed to an agent: the doc without front matter or specimen markers."""
    body = re.sub(r"\n?<!-- specimen: [\w-]+ -->\n?", "\n", d["body"]).strip()
    # Doc-to-doc links become full URLs, so they work in the one-file system and when pasted
    base = f"{SITE_URL}/brand/docs/{d['section']}/"
    body = re.sub(r"\]\(((?:\.\./)?[\w-]+(?:/[\w-]+)?\.md)\)",
                  lambda m: f"]({urllib.parse.urljoin(base, m.group(1))})", body)
    head, rest = body.split("\n", 1)
    return (f"{head}\n\n> {d['section_label']} · VIVE brand kit · {SITE_URL}/brand/{d['section']}/{d['slug']}\n"
            f"> Source: brand/docs/{d['section']}/{d['slug']}.md\n{rest}\n")


def render(d, spec):
    body = d["body"].split("\n", 1)[1]  # the page draws its own h1
    out = markdown.markdown(body, extensions=["tables", "fenced_code"], output_format="html")
    out = re.sub(r'href="([^":#]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', out)
    out = re.sub(r'<p><a href="(https://vive-cola\.vercel\.app[^"]*)">([^<]+)</a></p>',
                 r'<p><a class="btn white live" href="\1">\2</a></p>', out)

    def place(m):
        k = m.group(1)
        assert k in spec, f"{d['slug']}: unknown specimen {k}"
        return f'<div class="specimen" data-specimen="{k}">{spec[k]}</div>'
    out = re.sub(r"<!-- specimen: ([\w-]+) -->", place, out)
    return out


SHELL_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · VIVE Brand Kit</title>
<meta name="description" content="{summary}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VIVE">
<meta property="og:title" content="{title} · VIVE Brand Kit">
<meta property="og:description" content="{summary}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/og-brand-kit.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="VIVE Brand Kit: the VIVE wordmark beside a fan of brand swatch cards ending with VIVI, the mascot.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}/assets/og-brand-kit.png">
<link rel="icon" href="@R@favicon.ico" sizes="16x16 32x32 48x48">
<link rel="apple-touch-icon" href="@R@assets/icons/apple-touch-icon.png">
<link rel="alternate" type="text/markdown" href="@R@brand/docs/{section}/{slug}.md" title="This page as Markdown">
<link rel="preload" href="@R@assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="@R@assets/fonts/montserrat.css">
<link rel="stylesheet" href="@R@site.css">
<link rel="stylesheet" href="@R@brand/kit.css">
<script src="@R@brand/kit.js" defer></script>
{extra}<!-- Generated by scripts/build_brand_kit.py from brand/docs/{section}/{slug}.md. Edit the doc or the script, not this file. -->
</head>
"""


def nav(docs, cur):
    out = []
    for key, label in SECTIONS:
        cur_attr = ' aria-current="page"'
        items = "".join(
            f'<li><a href="@R@brand/{d["section"]}/{d["slug"]}.html" data-summary="{esc(d["summary"])}"'
            f'{cur_attr if d is cur else ""}>{esc(d["title"])}</a></li>'
            for d in docs if d["section"] == key)
        out.append(f'<details open><summary>{esc(label)}</summary><ul>{items}</ul></details>')
    return "".join(out)


def page(docs, i, spec):
    d = docs[i]
    R = "../../"
    prev_d, next_d = (docs[i - 1] if i else None), (docs[i + 1] if i + 1 < len(docs) else None)
    pager = "".join(
        f'<a class="{cls}" href="@R@brand/{x["section"]}/{x["slug"]}.html"><small>{lab}</small>{esc(x["title"])}</a>'
        for x, cls, lab in ((prev_d, "prev", "Previous"), (next_d, "next", "Next")) if x)
    extra = '<script src="@R@site.js" defer></script>\n' if "<!-- specimen: footer -->" in d["body"] else ""
    head = SHELL_HEAD.format(title=esc(d["title"]), summary=esc(d["summary"]), url=f"{SITE_URL}/brand/{d['section']}/{d['slug']}",
                             site=SITE_URL, section=d["section"], slug=d["slug"], extra=extra)
    doc_json = json.dumps(agent_md(d)).replace("</", "<\\/")
    body = f"""<body class="kit" data-root="@R@">
<a class="skip" href="#doc">Skip to content</a>
<header class="kit-top">
  <a class="kit-brand" href="@R@brand/getting-started/introduction.html"><img src="@R@assets/wordmark-vive-navy.png" alt="VIVE" width="94" height="24"><span>Brand Kit</span></a>
  <label class="kit-search"><span class="vh">Search the brand kit</span><input type="search" placeholder="Search…" autocomplete="off" aria-controls="kit-nav"><kbd aria-hidden="true">/</kbd></label>
  <div class="kit-actions">
    <button type="button" class="kit-btn" data-copy-system="@R@brand/vive-brand-kit.md" title="Copy the whole brand kit as one Markdown file">Copy entire system</button>
    <button type="button" class="kit-btn icon" popovertarget="kit-more" aria-label="More ways to get the whole system">▾</button>
    <div id="kit-more" class="kit-menu" popover>
      <a href="@R@brand/vive-brand-kit.md" download>Download entire system (.md)</a>
      <a href="@R@brand/llms.txt">Agent index (llms.txt)</a>
      <a href="@R@brand/docs/{d["section"]}/{d["slug"]}.md">This page as Markdown</a>
    </div>
    <a class="kit-site" href="@R@index.html">VIVE site</a>
  </div>
</header>
<div class="kit-layout">
<nav class="kit-nav" id="kit-nav" aria-label="Brand Kit">{nav(docs, d)}<p class="kit-empty" hidden>No matches.</p></nav>
<main id="doc" class="kit-doc">
  <p class="crumb">{esc(d["section_label"])} <span aria-hidden="true">›</span> {esc(d["title"])}</p>
  <div class="doc-head">
    <h1>{esc(d["title"])}</h1>
    <button type="button" class="kit-btn" data-copy-page title="Copy this page as Markdown to paste into any AI agent">Copy for agents</button>
  </div>
  <p class="doc-summary">{esc(d["summary"])}</p>
  <article class="doc-body">
{render(d, spec)}
  </article>
  <nav class="pager" aria-label="Previous and next">{pager}</nav>
</main>
</div>
<script type="application/json" id="doc-md">{doc_json}</script>
</body>
</html>
"""
    return (head + body).replace("@R@", R)


def build():
    docs = read_docs()
    spec = specimens()
    for i, d in enumerate(docs):
        out = KIT / d["section"] / f"{d['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(docs, i, spec))
    # One file with the whole system, for agents
    parts = [f"# VIVE Brand Kit\n\n> The whole VIVE brand system in one file: {len(docs)} docs across "
             f"{', '.join(l for _, l in SECTIONS[:-1])}, and {SECTIONS[-1][1]}. Browse it at {SITE_URL}/brand.\n\n"
             "## Contents\n\n" + "\n".join(f"- {d['section_label']}: {d['title']}" for d in docs) + "\n"]
    parts += ["\n---\n\n" + agent_md(d) for d in docs]
    (KIT / "vive-brand-kit.md").write_text("".join(parts))
    # Agent index (llms.txt convention)
    lines = ["# VIVE Brand Kit", "",
             "> The design system behind the VIVE website: tokens, components, blocks, and assets for the vitamin-charged cola. "
             "Every page is Markdown; fetch one, or fetch the whole system in one file.", "",
             f"- [Entire system]({SITE_URL}/brand/vive-brand-kit.md): every doc in one Markdown file"]
    for key, label in SECTIONS:
        lines += ["", f"## {label}", ""]
        lines += [f"- [{d['title']}]({SITE_URL}/brand/docs/{key}/{d['slug']}.md): {d['summary']}" for d in docs if d["section"] == key]
    (KIT / "llms.txt").write_text("\n".join(lines) + "\n")
    # /brand opens the introduction. Link previews read this page's own tags and do not
    # follow the redirect, so it carries the Brand Kit share card too.
    desc = "The VIVE brand system for people and agents: colors, type, shapes, components, blocks, and assets, with every page as Markdown."
    card_alt = "VIVE Brand Kit: the VIVE wordmark beside a fan of brand swatch cards ending with VIVI, the mascot."
    (KIT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VIVE Brand Kit</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VIVE">
<meta property="og:title" content="VIVE Brand Kit">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}/brand">
<meta property="og:image" content="{SITE_URL}/assets/og-brand-kit.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{card_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="VIVE Brand Kit">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}/assets/og-brand-kit.png">
<meta name="twitter:image:alt" content="{card_alt}">
<link rel="icon" href="../favicon.ico" sizes="16x16 32x32 48x48">
<link rel="canonical" href="{SITE_URL}/brand/getting-started/introduction">
<meta http-equiv="refresh" content="0; url=getting-started/introduction.html">
</head>
<body><p><a href="getting-started/introduction.html">Open the VIVE Brand Kit</a></p></body>
</html>
""")
    print(f"wrote {len(docs)} pages, vive-brand-kit.md, llms.txt, and index.html in brand/")


build()
