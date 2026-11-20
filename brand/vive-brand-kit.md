# VIVE Brand Kit

> The whole VIVE brand system in one file: 26 docs across Getting started, Foundations, Components, Blocks, and Assets. Browse it at https://vive-cola.vercel.app/brand.

## Contents

- Getting started: Introduction
- Getting started: How to use
- Foundations: Logo
- Foundations: Colors
- Foundations: Typography
- Foundations: Layout
- Foundations: Shapes
- Foundations: Patterns
- Foundations: Motion
- Foundations: Voice
- Components: Label
- Components: Button
- Components: Cart button
- Components: Motion toggle
- Components: Hover lift
- Components: VIVI
- Blocks: Site header
- Blocks: Hero
- Blocks: Facts ribbon
- Blocks: Section grounds
- Blocks: Poster row
- Blocks: Product shelf
- Blocks: Footer
- Assets: Cans
- Assets: Posters and ads
- Assets: Stationery

---

# Introduction

> Getting started · VIVE brand kit · https://vive-cola.vercel.app/brand/getting-started/introduction
> Source: brand/docs/getting-started/introduction.md

The VIVE brand kit is the set of colors, type, shapes, components, and sections that every VIVE page is built from. VIVE is the vitamin-charged cola: three 12 oz cans, each with four vitamins, zero calories, and 100% stevia.

The kit has one source for two readers. People browse these pages and see each piece rendered with the site's own stylesheet. Agents read the same pages as Markdown: every page has **Copy for agents**, and the top bar can copy or download the whole system as one file.

## How the catalog is organized

| Section | What it holds |
| --- | --- |
| Getting started | This introduction and [How to use](https://vive-cola.vercel.app/brand/docs/getting-started/how-to-use.md) |
| Foundations | Logo, colors, typography, layout, shapes, patterns, motion, and voice |
| Components | The shared pieces in `site.css`: label, button, cart button, motion toggle, hover lift, and VIVI |
| Blocks | Full-width sections: site header, heroes, facts ribbon, section grounds, product shelf, poster row, and footer |
| Assets | The cans, the posters and ads, and the stationery |

## Building a page in three steps

1. **Browse.** Find the blocks a page needs. Blocks are whole sections; components are the parts inside them.
2. **Pick.** Choose an order: a hero first, then the sections, then a closing call to action on a light ground.
3. **Assemble.** Ask for the page in plain language, naming the blocks: "A Glow launch page: hero, facts ribbon, poster row, and footer." The agent builds it from these pieces and your words.

You never pick colors, fonts, or spacing by hand. Those are fixed, and that is what keeps every page on-brand.

## When something is missing

Build it from the foundations: a ground from [Colors](https://vive-cola.vercel.app/brand/docs/foundations/colors.md), a label from [Label](https://vive-cola.vercel.app/brand/docs/components/label.md), and shapes from [Shapes](https://vive-cola.vercel.app/brand/docs/foundations/shapes.md). If the same new section is needed twice, add it to the kit as a block.

---

# How to use

> Getting started · VIVE brand kit · https://vive-cola.vercel.app/brand/getting-started/how-to-use
> Source: brand/docs/getting-started/how-to-use.md

There are two ways in. If you do not write code, you describe what you want and an agent builds it from these pieces. If you write code, you use the same classes directly. Both paths end with the same page.

## If you don't write code

1. **Start with the goal.** "A page announcing VIVE Focus for students" gives an agent more to work with than a list of parts.
2. **Point at the pieces.** Open a block or component and use **Copy for agents**. It hands over that page's documentation: what the piece is for, its markup, and its rules. When a page needs several blocks, use **Copy entire system** in the top bar.
3. **Describe the content.** Bring the words and the intent. The kit brings the look.
4. **Review and refine.** Ask for changes in plain language: "Make the hero shorter," or "Move the poster row above the video."

## If you write code

Every page loads two shared files from the site root, plus the self-hosted font:

```html
<link rel="preload" href="assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts/montserrat.css">
<link rel="stylesheet" href="site.css">
<script src="site.js" defer></script>
```

- `site.css` holds the tokens, the header, labels, buttons, shapes, patterns, cuts, the hover lift, the facts ribbon, the cart panel, and the footer.
- `site.js` renders the global footer, wires the cart button and its panel, keeps the cart in `localStorage`, wires every `[data-add]` button and quantity stepper, and wires every `.motion-toggle`.
- Page files keep only page-specific styles in their own `<style>` block.

## Rules for agents

- **Use tokens, never raw values.** Write `var(--navy)`, not `#2B3990`. The tokens are listed in [Colors](https://vive-cola.vercel.app/brand/docs/foundations/colors.md) and [Layout](https://vive-cola.vercel.app/brand/docs/foundations/layout.md).
- **Compose; do not fork.** Build new sections from existing classes. Do not add a variant to `.btn` or `.label` for one page.
- **One layer of background detail per section.** A section carries a pattern or large shapes, not both.
- **Copy rules:** follow [Voice](https://vive-cola.vercel.app/brand/docs/foundations/voice.md). Use the Oxford comma. Avoid contrast reveals ("not X, but Y"), negation lists, and buzzwords.
- **Assets come from `assets/`.** Never hotlink, and never invent an image. New team files enter through `scripts/sync_assets.py`.
- **Desktop first.** The site targets desktop widths from 1280 to 1920px. Mobile layouts are out of scope.
- **Every link works.** Internal links go to the four pages; social links go to the platform root.

## Files an agent can fetch

| File | What it is |
| --- | --- |
| `brand/llms.txt` | An index of every doc, with links and one-line summaries |
| `brand/vive-brand-kit.md` | The entire system in one Markdown file |
| `brand/docs/<section>/<page>.md` | One doc per page, the source of this catalog |

---

# Logo

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/logo
> Source: brand/docs/foundations/logo.md

The VIVE wordmark sets its middle letters as a bold exclamation mark and **IV**, the Roman numeral for the four vitamins in every can. The logo is an image drawn in Gardin Bold Rounded. Never set it as live text.


## Files

| File | Use it on |
| --- | --- |
| `assets/wordmark-vive-navy.png` | Light, off-white, sun, and orange grounds. The site header uses it at 125×32 |
| `assets/wordmark-vive-white.png` | Navy, deep navy, and ink grounds |
| `assets/logo-vive-navy-tagline.png` | The monogram with "The vitamin-charged cola" |
| `assets/logo-color-variations.png` | Reference sheet of approved color pairings |
| `assets/icons/icon-512.png` and `favicon.ico` | App icon and favicon: VIVI on a deep navy tile |

## Rules

- Keep the wordmark's proportions. Scale it by height only.
- Give it clear space at least the height of its exclamation mark on every side.
- Never place it inside a pattern tile, and never rebuild its letters from shapes.
- On orange, use the navy wordmark. White on orange is too faint (2.08:1).

```html
<a href="index.html"><img src="assets/wordmark-vive-navy.png" alt="VIVE home" width="125" height="32"></a>
```

---

# Colors

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/colors
> Source: brand/docs/foundations/colors.md

Orange, navy, sun, and off-white are the core four. Deep navy, ink, and mist give the grounds their range. Every color has a token in `site.css`; use the token, never the hex.


## Tokens

| Token | Hex | Role |
| --- | --- | --- |
| `--orange` | #FF9447 | The main web color: the header, accents, buttons, and display words |
| `--navy` | #2B3990 | The primary dark ground, labels, and body text on light grounds |
| `--sun` | #F4BD6A | Triangles, stars, name plates, and warm grounds |
| `--white` | #F9F9F9 | Light grounds, and text on navy |
| `--deep` | #1D2766 | The footer, the header's base line, and text on orange |
| `--ink` | #14183F | The darkest ground, behind the team portraits |
| `--mist` | #F1F2F8 | A quiet light ground for long reading sections |

Print pieces, the deck, and the can art keep the client's original orange, #F27A21. The web uses the lighter #FF9447 so navy text on it passes contrast (4.58:1).

## Text pairings

| Ground | Text | Contrast |
| --- | --- | --- |
| Orange | Deep navy | 6.24:1 |
| Sun | Navy | 5.9:1 |
| Navy | Off-white | 9.54:1 |
| Off-white | Navy | 9.54:1 |

## Rules

- Never put white text on orange.
- Do not use the deck's purple (#2A2882) as a page ground.
- On blue grounds, patterns switch to blue-toned tiles at full strength instead of fading orange tiles.

---

# Typography

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/typography
> Source: brand/docs/foundations/typography.md

Montserrat carries every line of live text, self-hosted in `assets/fonts/` and set by the `--f` token. Black (900) does the shouting, ExtraBold (800) labels things, SemiBold (600) carries body copy, and Regular (400) holds long notes.


## Roles

| Role | Weight and case | Size |
| --- | --- | --- |
| Display | Black 900, uppercase | 48 to 128px, line height 0.9 |
| Heading | Black 900, uppercase, usually inside a [Label](https://vive-cola.vercel.app/brand/docs/components/label.md) | 32 to 72px |
| Eyebrow and button | Black or ExtraBold, uppercase, 0.04 to 0.12em tracking | 13 to 15px |
| Body | SemiBold 600 | 16 to 22px, line height 1.5 to 1.6 |
| Note | Regular 400 | 13 to 15px |

## Rules

- Set sizes with `clamp()` so type scales between 1280 and 1920px wide.
- Paragraphs use `text-wrap: pretty` (set in `site.css`) so none ends on a single word.
- A fallback face, "Montserrat Fallback," is Arial resized to Montserrat's widths, so text keeps its line breaks while the font loads. Keep it in the stack.
- The logo is an image. Never set "VIVE" in Montserrat to stand in for it.

---

# Layout

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/layout
> Source: brand/docs/foundations/layout.md

A section paints its ground across the full width of the screen and keeps its content inside generous side gutters. Sections meet at diagonal cuts instead of straight lines.


## Gutters and the content column

| Token or class | Value | What it does |
| --- | --- | --- |
| `--gutter` | `max(clamp(16px, 7vw, 120px), calc((100% - 1240px) / 2))` | Side padding: at least 7vw, and on wide screens the content holds at 1240px |
| `.wrap` | `padding-inline: var(--gutter)` | Puts a section's content inside the gutters |
| `--cut` | `clamp(28px, 5vw, 72px)` | Depth of every diagonal cut |

## Cuts

| Class | Shape |
| --- | --- |
| `.cut-down` | The bottom edge slopes down to the left |
| `.cut-up` | The top edge slopes, and the section tucks under the one above |
| `.cut-both` | Both edges slope |

```html
<section class="posters wrap cut-up pat pat-sparse">…</section>
```

## Rules

- Each hero keeps equal space above and below its content (112px at desktop widths).
- The sticky header sits above every page; in-page links stop 96px below the top (`scroll-padding-top`).
- VIVI stands in a gutter only at 1280px and wider. See [VIVI](https://vive-cola.vercel.app/brand/docs/components/mascot.md).
- Decorative shapes never overlap text, buttons, images, cards, or VIVI between 1280 and 1920px.

---

# Shapes

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/shapes
> Source: brand/docs/foundations/shapes.md

The 10-point star and the triangle are VIVE's signature shapes. The full library lives in `assets/shapes/` as SVG files in every brand color, mirrored from `source/deck-extract/`.


## Using shapes on a page

Triangles are `<i class="tri">` elements. Set the size, the SVG, and the angle with custom properties. They snap in on load.

```html
<i class="tri" aria-hidden="true"
   style="--s:58px;--c:url(assets/shapes/triangle-equilateral-sun.svg);--r:-24deg;left:42%;top:28px"></i>
```

Stars are elements with the `.star` class and a `background-image`. Large static shapes behind a section's content go in a `.deco` layer:

```html
<div class="deco" aria-hidden="true">
  <i style="--s:420px;--img:url(assets/shapes/star-10pt-sun.svg);--r:12deg;right:-80px;top:40px"></i>
</div>
```

## Rules

- Set shapes at sharp angles. Never straighten a triangle to 0°.
- Place hero triangles in the band above the content, anchor large edge triangles in the gutter, and center small ones in a gutter.
- One layer of background detail per section: shapes or a [pattern](https://vive-cola.vercel.app/brand/docs/foundations/patterns.md), not both.
- Every decorative shape gets `aria-hidden="true"`.

---

# Patterns

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/patterns
> Source: brand/docs/foundations/patterns.md

Three patterns turn a color ground into a branded surface: Confetti Toss, Confetti Sparse, and Star Seal. They are SVG tiles in `assets/patterns/`, built by `scripts/build_patterns.py`.


## Using a pattern

Add `.pat` and one pattern class to a section. The tile sits on a layer between the section's ground and its content.

```html
<section class="intro wrap pat pat-seal">…</section>
```

| Class | Tile |
| --- | --- |
| `.pat-confetti`, `-warm`, `-white`, `-deep`, `-navy` | Confetti Toss, 312px |
| `.pat-sparse`, `-light`, `-blue` | Confetti Sparse, 640px |
| `.pat-seal`, `-sun`, `-white`, `-blue`, `-deep` | Star Seal, 140px |

`--pat-op` sets the strength (default 0.16), and `--pat-mask` can fade the tile with a gradient.

## Rules

- Use patterns sparingly. A heavier first pass felt suffocating.
- One pattern per section, and never on a section that already carries large shapes.
- On navy, deep, or ink grounds, use the blue-toned tiles (`-blue`, `-deep`, `-navy`) at full strength.
- A pattern tile never contains the VIVE logo or its letters.
- Keep patterns off product cards: shelves that hold cards stay plain.

---

# Motion

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/motion
> Source: brand/docs/foundations/motion.md

VIVE moves like it is charged: quick, snappy, and physical, never floaty.


## Tokens

| Token | Value | Use |
| --- | --- | --- |
| `--ease-out` | `cubic-bezier(.23, 1, .32, 1)` | Hovers, panels, and reveals |
| `--ease-pop` | `cubic-bezier(.2, 1.5, .4, 1)` | Brand pops: cans, VIVI, and the cart count |

## Rules

- **Hovers never move their own hit area.** A card or image lifts an inner `.lift` inside a static `.lift-zone`. See [Hover lift](https://vive-cola.vercel.app/brand/docs/components/hover-lift.md).
- **Every hover waits about 120ms before reversing**, so a pointer resting on an edge does not flicker.
- **Durations stay short:** 140 to 260ms for interface feedback, up to 700ms for a reveal.
- **Always-turning stars carry a pause button.** See [Motion toggle](https://vive-cola.vercel.app/brand/docs/components/motion-toggle.md).
- **Reduced motion keeps meaning, drops movement.** Under `prefers-reduced-motion: reduce`, rises become fades and turning stops.

---

# Voice

> Foundations · VIVE brand kit · https://vive-cola.vercel.app/brand/foundations/voice
> Source: brand/docs/foundations/voice.md

VIVE sounds sharp, energetic, and cheerful. Lead with the vitamins; stevia and zero calories are the reassurance that follows.

## Lines

| Line | Where it goes |
| --- | --- |
| The vitamin-charged cola. | The brand line |
| Your dose of good vibes. | VIVE Classic: vitamins A, B9, B12, and C |
| Your dose of radiant vibes. | VIVE Glow: vitamins A, B7, C, and E, for skin health |
| Your dose of sharp vibes. | VIVE Focus: vitamins B6, B9, B12, and C, for mental performance |

## Calls to action

| Line | Where it goes |
| --- | --- |
| Grab a VIVE! | The primary button |
| Spread the vibes! | Posters and sharing |
| Sip the vibe now! | The ad |
| I need more VIVE | VIVI's sticker |

## Product facts

Every can is 12 oz, ₱67, sweetened with 100% stevia, and has zero calories. VIVE is sold at Lawson, 7-Eleven, SM, and Ayala Malls.

## Rules

- Write short, declarative sentences with a concrete benefit.
- Use the Oxford comma in every list of three or more.
- Avoid contrast reveals ("not X, but Y"), negation lists ("no X, no Y, no Z"), rhetorical questions, and buzzwords such as "elevate" or "game-changer."
- Never promote the retired deck-era variants (Decaffeinated and Extra Caffeine).

---

# Label

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/label
> Source: brand/docs/components/label.md

A label is a tilted strip of color behind a heading's words. It is VIVE's heading style: a section title is one or two labels stacked, never plain text.


## Using it

Wrap each line of a heading in `<span class="label">`. A second label tilts less than the first, so the pair reads as one stacked heading.

```html
<h2 id="vibe-title"><span class="label">Pick your vibe</span></h2>

<h2>
  <span class="label sun">The team</span>
  <span class="label white">behind the can</span>
</h2>
```

## Variants

| Class | Ground and text | Use it on |
| --- | --- | --- |
| `.label` | Navy, off-white text | Light, sun, and orange grounds |
| `.label.orange` | Orange, deep navy text | Light and navy grounds |
| `.label.sun` | Sun, navy text | Navy and light grounds |
| `.label.white` | Off-white, navy text | Navy and orange grounds |

## Rules

- Inside `h1` to `h3`, labels become blocks, one per line. Keep a heading to two labels.
- Pick a label color that differs from the ground it sits on.
- Keep heading copy short: two to four words per label.

---

# Button

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/button
> Source: brand/docs/components/button.md

The button has a chamfered right edge and a shadow block that slides out on hover. Hover the samples to see it; press one to see the squeeze.


## Using it

Use `<a class="btn">` for navigation and `<button class="btn">` for actions. Add one color class.

```html
<a class="btn orange" href="shop.html">Grab a VIVE!</a>
<a class="btn white" href="product.html">See the flavors</a>
<button class="btn navy add" type="button" data-add>Add to cart</button>
```

## Variants

| Class | Ground, text, and shadow | Use it on |
| --- | --- | --- |
| `.btn.navy` | Navy, off-white text, orange shadow | Light and sun grounds |
| `.btn.orange` | Orange, deep navy text, sun shadow | Navy and light grounds: the primary call to action |
| `.btn.white` | Off-white, navy text, orange shadow | Navy and orange grounds: the second action |
| `.btn.sun` | Sun, navy text, orange shadow | Navy and light grounds |

`.btn.is-added` fills the button sun for a beat after an item goes into the cart; `site.js` sets it.

## Rules

- One primary button per section. A second action uses a quieter color beside it.
- Labels are short and say what happens: "Grab a VIVE!", "See the flavors," or "Add to cart."
- The hover never moves the button's hit area; only the shadow block moves.
- On navy and deep grounds, add `.on-dark` to the section so the focus ring turns sun.

---

# Cart button

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/cart-button
> Source: brand/docs/components/cart-button.md

The cart button sits at the end of the primary navigation on every page. Its badge shows a live count of the items in the cart, kept in `localStorage` so it carries across pages and visits.


## Using it

Ship the button in each page's nav markup, after the link list. `site.js` wires it and builds the panel it opens, so the nav never shifts when the script runs.

```html
<nav class="wrap" aria-label="Primary">
  …
  <button type="button" class="cart-btn" popovertarget="cart-panel"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 7V6a5 5 0 0 1 10 0v1h3.2l-1.3 15H5.1L3.8 7H7Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg>Cart <span class="cart-count">0</span><span class="vh"> items</span></button>
</nav>
```

## Behavior

- The panel is a native popover. It scales in from the button's corner in 200ms and exits in 140ms.
- The count badge pops (`.bump`) when an item is added.
- Any `<button data-add>` inside an element with `data-id`, `data-name`, and `data-price` adds that item, using the nearest quantity input.

## Rules

- There are no cart, checkout, or payment pages. The panel lists items, a total, "Keep shopping," and "Clear cart."
- The button has a fixed size, so a count change never shifts the nav.

---

# Motion toggle

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/motion-toggle
> Source: brand/docs/components/motion-toggle.md

Any section whose stars turn without stopping carries a **Motion** button, so a visitor can pause it (WCAG 2.2.2).


## Using it

Place the button inside the section. `site.js` toggles `.is-still` on the section, which pauses every `.burst.star` inside it.

```html
<section class="hero cut-down on-dark pat pat-confetti-warm">
  …
  <div class="burst star"></div>
  <button class="motion-toggle" type="button"><span class="vh">Pause </span>Motion <span class="icon" aria-hidden="true"></span></button>
</section>
```

## Rules

- Every hero with turning stars has one, in the same corner on each page.
- Under `prefers-reduced-motion: reduce`, the stars do not turn, so the button is not needed.

---

# Hover lift

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/hover-lift
> Source: brand/docs/components/hover-lift.md

Cards and images sit at a slight tilt and straighten and rise on hover. The moving part is an inner `.lift`; the hover belongs to its static parent, `.lift-zone`.


## Using it

```html
<div class="art lift-zone" style="--tilt:-1.5deg">
  <div class="lift"><img src="assets/merch/cap.webp" alt="VIVE cap mockup" width="900" height="900"></div>
</div>
```

| Property | Default | What it does |
| --- | --- | --- |
| `--tilt` | `0deg` | The resting angle. The hover straightens it to 0 |
| `--rise` | `0px` | The resting offset. The hover lifts it 6px |

## Why it works this way

The `.lift` layer has `pointer-events: none`, so its tilted corners cannot start or end a hover. Only the static zone can. The lift also waits 120ms before falling back, so a pointer resting on an edge never makes it flicker.

---

# VIVI

> Components · VIVE brand kit · https://vive-cola.vercel.app/brand/components/mascot
> Source: brand/docs/components/mascot.md

VIVI is the VIVE mascot: the V from the wordmark with a sweatband, arms, and legs. It stands in the side gutters beside section titles, and on a turning star in a hero.


## Files

| File | Pose | Typical spot |
| --- | --- | --- |
| `assets/mascot/vivi-pointing.webp` | Pointing | Beside a section title, pointing at it (mirror it with `.flip` on the left) |
| `assets/mascot/vivi-running.webp` | Running | Beside a shelf or a call to action |
| `assets/mascot/vivi-dizzy.webp` | Dizzy | Playful moments: "I need more VIVE" |
| `assets/mascot/vivi-need-more-vive.webp` | Dizzy, with the line | The Shop hero sticker |

All four are the team's outlined versions, with a white sticker edge built in.

## Using it

```html
<section class="shelf wrap">
  <img class="mascot left" src="assets/mascot/vivi-running.webp" alt="" width="606" height="720" loading="lazy" style="top:38%">
  …
</section>
```

`.mascot.left` or `.mascot.right` centers VIVI in that side's gutter. It shows only at 1280px and wider, where the gutter can hold it.

## Rules

- VIVI is decoration beside content: `alt=""`, and never on top of text or cards.
- One VIVI per section.
- VIVI faces the title it stands beside.

---

# Site header

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/site-header
> Source: brand/docs/blocks/site-header.md

The header is an orange bar with a deep navy base line, pinned to the top of every page. It holds the navy wordmark, the four page links, and the [cart button](https://vive-cola.vercel.app/brand/docs/components/cart-button.md).


## Markup

```html
<header class="site-header">
<nav class="wrap" aria-label="Primary">
  <a href="index.html"><img src="assets/wordmark-vive-navy.png" alt="VIVE home" width="125" height="32"></a>
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About Us</a></li>
    <li><a href="product.html">Product</a></li>
    <li><a href="shop.html">Shop</a></li>
  </ul>
  <button type="button" class="cart-btn" popovertarget="cart-panel">…</button>
</nav>
</header>
```

## Rules

- Mark the current page with `aria-current="page"`. It gets a color and an inset underline only, so no tab changes size.
- The header is orange on every page, so it always stands apart from the hero below it.
- Once the page scrolls, the bar gains a soft shadow (a `scroll-state` container query).

---

# Hero

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/hero
> Source: brand/docs/blocks/hero.md

Every page opens with a hero that states one idea in display type, backs it with a short paragraph, and offers one or two buttons. Each page's hero looks different on purpose.

[See the Home hero live](https://vive-cola.vercel.app/)

## The four heroes

| Page | Ground | What it shows |
| --- | --- | --- |
| Home | Navy, warm Confetti Toss, cut down | Split: "Your dose of good vibes" with the Classic can on two turning stars |
| About Us | Off-white, Confetti Sparse | Centered story opener, with VIVI rising from two counter-turning stars |
| Product | Off-white, Confetti Toss | A navy headline over three color panels, one per can |
| Shop | Navy, deep Star Seal, cut down | A storefront: VIVI's sticker and three aisle tiles |

## Shared parts

```html
<section class="hero cut-down on-dark pat pat-confetti-warm">
  <i class="tri" aria-hidden="true" style="--s:120px;--c:url(assets/shapes/triangle-equilateral-sun.svg);--r:18deg;left:calc(var(--gutter) - var(--s) - 28px);top:120px"></i>
  <div class="grid wrap">
    <div>
      <h1>Your dose of <em>good vibes</em></h1>
      <p>The vitamin-charged cola. A convenient, refreshing way to get your vitamins A, B9, B12, and C from a cold can of cola.</p>
      <a class="btn orange" href="shop.html">Grab a VIVE!</a>
      <a class="btn white" href="product.html">See the flavors</a>
    </div>
    <div class="stage"><div class="burst back star"></div><div class="burst star"></div><img class="can" src="assets/can-classic-web.webp" alt="VIVE Classic can, 12 oz" width="600" height="1569" fetchpriority="high"></div>
  </div>
  <button class="motion-toggle" type="button"><span class="vh">Pause </span>Motion <span class="icon" aria-hidden="true"></span></button>
</section>
```

The hero's layout styles live in its page's own `<style>` block; the shared parts (`.cut-down`, `.pat`, `.tri`, `.btn`, and `.motion-toggle`) come from `site.css`.

## Rules

- No price in a hero.
- Equal space above and below the content: 112px at desktop widths.
- Turning stars need a [motion toggle](https://vive-cola.vercel.app/brand/docs/components/motion-toggle.md).
- The hero's main image loads with `fetchpriority="high"`; nothing else on the page does.

---

# Facts ribbon

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/facts-ribbon
> Source: brand/docs/blocks/facts-ribbon.md

A sun strip of three or four short facts, set in uppercase Black with a small navy triangle before each one. It sits under a hero and tucks under that hero's diagonal cut.


## Markup

```html
<div class="facts wrap">
  <span>Four vitamins in every can</span>
  <span>VIVE Classic, Glow, and Focus</span>
  <span>0 calories</span>
  <span>12 oz can</span>
</div>
```

## Rules

- Facts are short noun phrases, never sentences.
- Three or four facts. More than that wraps to a second line.

---

# Section grounds

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/section-grounds
> Source: brand/docs/blocks/section-grounds.md

Every content section is a full-width color ground with one layer of background detail and diagonal cuts where it meets its neighbors. Alternate grounds so neighboring sections never share a color.


## Recipe

```html
<section class="posters wrap cut-up pat pat-sparse" aria-labelledby="vibe-title">
  <h2 id="vibe-title"><span class="label">Pick your vibe</span></h2>
  …
</section>
```

1. **Ground:** off-white, mist, sun, orange, navy, deep navy, or ink. Set it in the page's styles with a color token.
2. **One layer of detail:** a [pattern](https://vive-cola.vercel.app/brand/docs/foundations/patterns.md) (`.pat .pat-…`) or a `.deco` layer of large [shapes](https://vive-cola.vercel.app/brand/docs/foundations/shapes.md). Never both.
3. **Cuts:** `.cut-up`, `.cut-down`, or `.cut-both` where the section meets a different ground.
4. **Heading:** one or two [labels](https://vive-cola.vercel.app/brand/docs/components/label.md).
5. **On dark grounds:** add `.on-dark` so focus rings turn sun.

## Ground pairings used on the site

| Ground | Detail | Example |
| --- | --- | --- |
| Off-white | Confetti Sparse | Home's poster row, Product's "In every can" |
| Sun | Star Seal | Home's intro poster and video |
| Navy | Blue Star Seal at full strength | Product's comparison table |
| Ink | Blue Star Seal | About's team |
| Off-white | Confetti Toss | Closing calls to action |

---

# Poster row

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/poster-row
> Source: brand/docs/blocks/poster-row.md

The poster row shows the three variant posters side by side, each tilted on a block of its color, with the variant's name, line, vitamins, and a button to the Shop.

[See it live on Home](https://vive-cola.vercel.app/#vibe-title)

## Markup

```html
<figure style="--b:var(--sun)">
  <div class="art lift-zone"><div class="lift"><img src="assets/poster-glow-hires.webp" alt="VIVE Glow poster: a woman in pink closes her eyes and holds up a pink VIVE Glow can" width="1024" height="1636" loading="lazy"></div></div>
  <figcaption>
    <h3>VIVE Glow</h3>
    <p class="tagline">Your dose of radiant vibes</p>
    <p class="vits">Vitamins A, B7, C, and E to support skin health.</p>
    <a class="btn navy" href="shop.html">Grab VIVE Glow</a>
  </figcaption>
</figure>
```

The row's layout lives in `index.html`; the [hover lift](https://vive-cola.vercel.app/brand/docs/components/hover-lift.md) and [button](https://vive-cola.vercel.app/brand/docs/components/button.md) come from `site.css`.

## Rules

- Order: Glow, Classic, and Focus, so Classic sits in the middle.
- `--b` sets the block behind each poster: sun for Glow, orange for Classic, and navy for Focus.
- Posters are the team's 1024×1636 files from `assets/`. See [Posters and ads](https://vive-cola.vercel.app/brand/docs/assets/posters.md).

---

# Product shelf

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/product-shelf
> Source: brand/docs/blocks/product-shelf.md

A shelf is a section of product cards: the Shop's cans, packs, and merch. Each card has a tilted photo, a name, one line of description, a price, a quantity stepper, and **Add to cart**.

[See it live on the Shop](https://vive-cola.vercel.app/shop#merch)

## Markup

```html
<article class="item" data-item data-id="merch-headband" data-name="Sport headband" data-price="249">
  <div class="art lift-zone" style="--g:var(--orange)"><div class="lift"><img class="photo" src="assets/merch/headband.webp" alt="Sport headband mockup: white band with navy edges, the orange VIVE wordmark, and sun triangles" width="900" height="900" loading="lazy"></div></div>
  <h3>Sport headband</h3>
  <p class="desc">The sweatband VIVI wears, sized for you. Stretch knit with the wordmark up front.</p>
  <div class="buy">
    <p class="price">₱249</p>
    <div class="qty">
      <button type="button" data-step="-1" aria-label="Decrease quantity for Sport headband">−</button>
      <label class="vh" for="q-merch-headband">Quantity for Sport headband</label>
      <input id="q-merch-headband" type="number" inputmode="numeric" min="1" max="99" value="1">
      <button type="button" data-step="1" aria-label="Increase quantity for Sport headband">+</button>
    </div>
  </div>
  <button class="btn navy add" type="button" data-add>Add to cart<span class="vh">: Sport headband</span></button>
</article>
```

The card styles live in `shop.html`. `site.js` wires the stepper and the button for any element with `data-id`, `data-name`, and `data-price`.

## Rules

- `--g` sets the tilted frame's color. Frames cycle orange, sun, and navy only.
- Shelves that hold cards stay plain: no pattern behind product cards.
- Prices are sample prototype prices, and merch photos are mockups; the page says so in a note.
- The three single-can cards reveal their model photo on hover; see the Shop can reveal in the project decisions.

---

# Footer

> Blocks · VIVE brand kit · https://vive-cola.vercel.app/brand/blocks/footer
> Source: brand/docs/blocks/footer.md

The footer sits on ink with blue Confetti Sparse and a top edge tilted against the page cuts. Four columns sit under tilted sun labels: the brand with a Shop button, the pages, where to find VIVE, and how to say hi. Social links and the copyright line run along the base.


## Using it

Every page ends with an empty footer. `site.js` fills it, so the footer is defined in one place.

```html
<footer class="site-footer"></footer>
<script src="site.js" defer></script>
```

## Rules

- Edit the footer in `site.js`, never on a page.
- Retailer logos (Lawson, 7-Eleven, SM, and Ayala Malls) stack on 28px rows.
- Social links go to each platform's root: Facebook, Instagram, and TikTok.

---

# Cans

> Assets · VIVE brand kit · https://vive-cola.vercel.app/brand/assets/cans
> Source: brand/docs/assets/cans.md

Three 12 oz cans, each with four vitamins for one daily need, zero calories, and 100% stevia. Each is ₱67.


| Can | Line | Vitamins | For | File |
| --- | --- | --- | --- | --- |
| VIVE Classic | Your dose of good vibes | A, B9, B12, and C | Everyday energy | `assets/can-classic-web.webp` |
| VIVE Glow | Your dose of radiant vibes | A, B7, C, and E | Skin health | `assets/can-glow-web.webp` |
| VIVE Focus | Your dose of sharp vibes | B6, B9, B12, and C | Mental performance | `assets/can-focus-web.webp` |

The Classic label and its nutrition facts are in `assets/label-classic-nutrition.webp`.

## Rules

- Renders are transparent WebP at 600px wide. Set `width="600"` and the file's height to avoid layout shift.
- Show a can on a star or a color panel, with a soft drop shadow.
- Name the variant in full: "VIVE Glow," never "Glow" alone in a heading.

---

# Posters and ads

> Assets · VIVE brand kit · https://vive-cola.vercel.app/brand/assets/posters
> Source: brand/docs/assets/posters.md

The posters and the ad are the team's own work, synced into `assets/` by `scripts/sync_assets.py` from the team's Drive folder.


| File | What it is | Where it runs |
| --- | --- | --- |
| `assets/poster-intro-hires.webp` | Intro poster, "Your dose of good vibes," 1350×1800 | Home, after the hero |
| `assets/poster-classic-hires.webp`, `-glow-`, `-focus-` | Variant posters, 1024×1636 | Home's [poster row](https://vive-cola.vercel.app/brand/docs/blocks/poster-row.md) |
| `assets/model-classic-web.webp`, `-glow-`, `-focus-` | The poster photos without headlines, cropped square with matched head sizes | The Shop can reveal |
| `assets/mockup-intro-bus-shelter.webp`, `-street-wall.webp` | The intro poster in place | Home, "Spotted around town" |
| `assets/video/vive-ad.mp4` and `vive-ad-cover.webp` | The 45-second ad and its cover | Home's video strip |
| `assets/og-card.png` | The 1200×630 share card | Link previews for every page |

## Rules

- Never crop a poster's headline in a full poster view.
- Alt text names the variant and describes the scene: "VIVE Glow poster: a woman in pink closes her eyes and holds up a pink VIVE Glow can."
- New or corrected posters enter through `scripts/sync_assets.py`, never by hand.

---

# Stationery

> Assets · VIVE brand kit · https://vive-cola.vercel.app/brand/assets/stationery
> Source: brand/docs/assets/stationery.md

The business card and the letterhead carry the brand onto paper: the wordmark, the four core colors, and the star and triangle shapes.


| File | Size |
| --- | --- |
| `assets/stationery/business-card-front.webp` | 1575×900 |
| `assets/stationery/business-card-back.webp` | 1575×900 |
| `assets/stationery/letterhead.webp` | 1131×1600 |

The letterhead's body text is placeholder copy from the team's template. Replace it before any printed use.
