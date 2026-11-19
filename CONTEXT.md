# VIVE Website — Canonical Router and Scope Contract

This document is the canonical router and functional contract for the VIVE four-page website prototype. It defines the page specifications, folder roles, quality constraints, and build sequence.

## Pipeline and Current Status

| Page | File | Status | Input Dependencies | Human Check Gate |
|---|---|---|---|---|
| 01 Home | [index.html](index.html) | Draft v5 complete: team posters, the 45-second ad in a native player, six Christmas posters, VIVI in two gutters (none in the Christmas section), and shapes clear of all content | `assets/`, `brand-spec.md`, `direction-approved.md` | Gian / Client review of hero, posters, and video layout |
| 02 About Us | [about.html](about.html) | Draft v3 complete: the friends' founding story, a large VIVI on a white star with Motion pause, and six untinted team cutouts with rising sun name plates | Founding story, team roster, and team photos | Verify complete names, company roles, and photo look |
| 03 Product | [product.html](product.html) | Draft v1 complete | Can renders, flavor specifications, and nutritional facts | Verify one variant per strip, zero posters, and zero merch |
| 04 Shop | [shop.html](shop.html) | Draft v5 complete: VIVI's "I need more VIVE" sticker in the hero, 13 merch mockup photos (jersey cut out of its checkerboard, keychain, and scarf added), can renders, and a poster hover reveal | Merch catalog, bundle definitions, and pricing | Verify quantity inputs, cart count behavior, zero checkout |
| Share card | [design-demos/og-card.html](design-demos/og-card.html) → `assets/og-card.png` | Chosen: VIVI's Pick (2026-11-19), 1200×630, referenced by the OG and Twitter tags on all four pages | Wordmark, cans, VIVI, `star-10pt-white.svg` | After a change, re-render with headless Brave at 1200×630 (see the file's header comment) |
| Favicon and app icons | `favicon.ico` and `assets/icons/`, built by `scripts/sync_assets.py` from `Mascot/VIVI pointing.png` | Chosen: VIVI on sun (2026-11-19), linked on all four pages | VIVI mascot source | Rebuilds with the other assets when the mascot source changes |
| Web portal poster | [router.html](router.html) → `VIVE.pdf` on Drive | Locked: Three Columns (2026-11-18), see [direction-approved.md](direction-approved.md) | Can renders, `site.css` tokens | Change only when the client asks; rebuild by hand with `scripts/build_router_pdf.py` |

**Next action:** Get the corrected Classic poster export from the team, run `python3 scripts/sync_assets.py` after any source change in `ponce-advertising/`, and decide whether the lone 13th merch card needs a different layout.

**Open checks (as of 2026-11-19):**
- The Shop merch grid holds 13 items in four columns, so the knit scarf sits alone on the last row.
- The team's Classic poster headline reads "Your dose of radiant vibes" (the Glow line); a corrected export is needed (see [brand-spec.md](brand-spec.md)). It now shows on Home and in the Shop Classic can reveal.
- Not yet seen in Firefox or Safari: the cart panel exit fallback and the Christmas viewer's outside-click close.
- `source/deck-extract/brand-assets-contact-sheet.png` still shows the old outline shapes; its build script needs headless Brave.

---

## Canonical Page Specifications

### 1. Homepage (`index.html`)
- **Hero section:** Bold brand statement, 10-point burst, Classic can visual, a vitamin-led paragraph, and clear calls to action. No price in the hero.
- **Posters section:** Present one poster per variant (VIVE Glow, VIVE Classic, and VIVE Focus) at slight angles under the tilted "Pick your vibe" label. Each poster carries the variant name, its tagline, its vitamins, and a "Grab VIVE …" button to `shop.html`. The posters are the team's 1024×1636 Classic, Glow, and Focus posters (see [brand-spec.md](brand-spec.md)).
- **Video section:** The team's 45-second ad (`assets/video/vive-ad.mp4`, synced from `video-recordings/draft12.mov`) plays in a native `<video controls>` element at 16:9, with its "Sip the vibe now" end card as the poster image.
- **Additional posters:** Feature campaign extensions and introductory ads (including the courtside volleyball poster and street mockups).
- **Seasonal poster footer:** "Christmas with VIVE" at the end of the page shows the six team Christmas posters (Czar, Louie, Venson, Warren, Aya, and Madrid) in one row at equal height. Selecting a poster opens it full size in a native modal `<dialog>` (`showModal()` and a Close button). A click outside the poster closes it in every browser: a script closes the dialog when both the press and the release land on its backdrop, and `closedby="any"` covers the same case natively.
- **All ads created live here:** The homepage acts as the comprehensive advertising showcase for the brand.

### 2. About Us (`about.html`)
- **Founding story:** A group of friends unwinding after work asks, "What if this cola had vitamins in it?" The story then explains the brand name origin (the ending letters of *revive* and *survive*).
- **The team:** Complete names and company roles for the six team members.
- **Brand-aligned photos:** Transparent team cutouts (`assets/team/*.webp`) stand on alternating orange, sun, and cream 10-point stars, three per row in two rows. `sync_assets.py` frames every cutout on a 1000×1250 canvas with the face (found by `scripts/face_boxes.swift`, macOS Vision) 420px wide, centered, and 250px from the top, so every head shares one size and eye line. The portrait is sized by card height and centered. The hero carries a large VIVI on a turning white 10-point star that reaches halfway into the right gutter, with the shared Motion pause button. `sync_assets.py` cuts out any team photo without transparency first (`scripts/cutout.swift`, macOS Vision foreground mask);
- **Visual mechanic:** Six equal cards, three per row. Each portrait stands untinted on its star, and a solid sun name plate with an angled top carries the role and name. On hover or focus the plate rises (`grid-template-rows` 0fr to 1fr, 260ms ease-out, 120ms leave delay) to reveal the bio and badge; the portrait never moves.

### 3. Product Page (`product.html`)
- **Brand product showcase:** Deep focus on the cans, vitamin formulation per variant (see the product line in [brand-spec.md](brand-spec.md)), stevia sweetening, and zero-calorie benefits.
- **Strip structure:** Exactly one product variation per strip, except where variants are showcased together as a cohesive family strip.
- **Strict negative constraints:**
  - **NO** product posters are allowed on this page.
  - **NO** merchandise items are allowed on this page.

### 4. Shop Page (`shop.html`)
- **E-commerce experience:** Browse and select items with quantity selectors and functional "Add to Cart" interactions.
- **Catalog range:** Individual cans/singles, curated multi-can bundles, and branded merchandise.
- **Cart count state:** Display a true, reactive numeric cart counter in the header navigation.
- **Strict negative constraints:**
  - Dedicated cart, checkout, and payment pages are **not needed** and are excluded.

---

## Operational Standards and Submission Rules

- **Copywriting standard (`/copywriting`, `/copy-editing`):** Follow the `/copywriting` skill for new copy and `/copy-editing` for tightening drafts. Copy must be clear, compelling, and grounded in customer benefits. Strictly ban all `ai-tells` (no contrast reveals like "not X, but Y", no negation lists like "no X, no Y, no Z", no trailing pile-on comma clauses, no rhetorical self-questions, and no empty buzzwords).
- **Web platform standard (`/modern-web-guidance`):** Follow Google Chrome's `modern-web-guidance` for semantic HTML5 structure, modern CSS layout (Grid, Subgrid, container queries, `:has()`, `@starting-style`), accessibility, and asset performance. Check `modern-web-guidance` before writing ad-hoc layout logic or script workarounds.
- **Prototyping and design standard (`/huashu-design`, `/snowe-ui-skill`):** Apply `/huashu-design` for high-fidelity HTML prototype creation, multi-directional exploration, and design presentation reviews. Use `/snowe-ui-skill` to safeguard brand visual balance, sharp cuts, star/triangle motifs, and typography hierarchy.
- **Motion and micro-interaction standard (`/animate`, `/emil-design-eng`, `/apple-design`):** Interactions must feel energetic, crisp, and physically grounded. Button hovers, poster tilts, the team name-plate reveal, and cart badge updates should use snappy easing curves with mandatory `prefers-reduced-motion` support.
- **Punctuation standard:** Mandatory Oxford comma in all lists of three or more items across copy, documentation, and interface text.
- **Interactive fidelity:** The site must feel like an authentic, finished web application. Every button, selector, and link must work. If an external link has no specific sub-page (such as social channels), wire it directly to the platform root (`https://facebook.com`, `https://instagram.com`, `https://tiktok.com`).
- **High-stakes grading:** Gian will grade all assets appearing across these pages (posters, video, product variations, and branding).
- **Asset integrity:** No placeholder photos and no placeholder texts (Lorem Ipsum). All content must be written and staged with genuine assets.
  - **Approved stand-ins (client, 2026-11-16):** until real assets exist, the site may use (1) merch mockups in `assets/merch/` (the team's mockup photos; the jersey photo is cut out of its baked-in checkerboard by the `cutout-square` sync recipe) and (2) sample shop prices. The three cans now use the team's own renders. Each is labeled on the page or in its alt text. Replace them when the real renders, product photos, and prices arrive.
- **Shared system:** Every page loads [site.css](site.css) and [site.js](site.js). `.wrap` gutters are at least 7vw, and on screens wider than about 1500px the content column holds at 1240px while the gutters take the rest. VIVI, the mascot (`.mascot.left` or `.mascot.right`), stands centered in a section's side gutter on screens 1280px and wider. Each hero keeps equal space above and below its content (112px at desktop widths). `site.js` renders the one global footer, whose base row carries the location and contact details (123 Street, Quezon City, Philippines; hello@vivecola.com; +63 922 000 1234) and the social links, adds the header cart button and cart panel to the primary nav, and keeps the cart count in `localStorage` so it persists across pages and visits. The primary nav sits in a sticky `.site-header` on every page, and in-page links scroll smoothly to a stop below it (`scroll-padding-top: 96px`; reduced motion jumps instantly). Page files keep only page-specific styles.
- **Shape placement:** A decorative triangle never overlaps text, a button, an image, a card, or a mascot at 1280 to 1920px wide. Place hero triangles in the band above the content (`top` under about 40px), anchor large edge triangles to the gutter (`left: calc(var(--gutter) - var(--s) - 28px)` bleeds them off the page), and center small ones in a gutter (`left: calc(var(--gutter) / 2 - <half size>)`). Re-check overlaps after any layout change.
- **Motion pause:** Any hero with always-turning stars carries `<button class="motion-toggle">`; `site.css` styles it and `site.js` toggles `.is-still` on its section, which pauses every `.burst.star` inside.
- **Brand shapes:** Stars and triangles load the SVG files from `assets/shapes/`, the web mirror of `source/deck-extract/` (`star-10pt-*.svg`, `triangle-equilateral-*.svg`, and `triangle-right-white.svg` for the play icon). A `.tri` takes its SVG through `--c:url(…)`, and a `.star` takes it through `background-image`. Section cuts, tilted labels, and button chamfers stay as CSS `clip-path` because they shape layout boxes, not standalone brand assets.
- **Cart panel motion:** The cart is a native popover. It scales in from its top-right trigger corner in 200ms (ease-out) and exits in 140ms on a plain ease, transitioning `display` and `overlay` so the column layout and top-layer position hold until the fade ends. Browsers that cannot transition `display` or `overlay` (Firefox and older Safari) play the same exit through a `data-closing` attribute set by `site.js` on the close and cart buttons; Esc and outside clicks close instantly there. Reduced motion keeps a 100ms fade without the scale.
- **Hover rule:** No hover effect may move its own hit area. Buttons show an offset shadow block behind them; tilting cards and images lift an inner `.lift` (with `pointer-events: none`) inside a static `.lift-zone`. Every hover also waits about 120ms before reversing when the pointer leaves. Together these prevent repeated hover toggling when the pointer rests on an edge.
- **Shop can reveal:** On the three single-can cards, hovering the image raises that can's poster (`assets/poster-*-hires.webp`, cropped to its headline, person, and can) from the bottom behind a row of three large triangles, modeled on Olipop's product-card wave: 700ms on an ease-out cubic curve in both directions, reversing from its current point. The triangles flatten into a straight edge over the last 16% of the rise. A registered `--reveal` property drives the clip-path. The reveal is armed only after the scene image has decoded (or 1.2s after it loads), the layer has `pointer-events: none`, it waits the usual 120ms before falling, and reduced motion swaps the rise for a fade.
- **Asset sync (`scripts/sync_assets.py`):** The team's working files (posters, video, mascot, team photos, and merch mockups) live outside this repository in `ponce-advertising/`. Never copy them by hand. Add each new output to the `ASSETS` list in the script and run `python3 scripts/sync_assets.py`; it converts and resizes each file into `assets/` and records its source size and time in `assets/asset-sources.json`. When a source file changes, rerun the script; `--check` lists stale outputs and exits 1.
- **Dynamic visual generosity:** Apply signature brand patterns generously (10-point star, triangles, diagonal cuts, and contrasting color grounds). Do not settle for plainness.
- **GitHub and Vercel publishing (`/deploy-with-vercel`):** The `vive-website/` directory will be published as a standalone repository on GitHub and deployed directly to Vercel. All relative asset links and inter-page navigations must function cleanly in this standalone root structure.
- **Out of scope:**
  - Dedicated cart, checkout, and payment pages.
  - Mobile responsive layouts (desktop presentation is the target).
- **Benchmark samples:**
  - [Chewla](https://pjconsing.wixsite.com/chewla)
  - [Collide](https://hpearlquinto.wixsite.com/collideyourwaynow)
- **Deadline:** Friday.

---

## Folder Map and Domain Authorities

| Path | Role | Domain Authority |
|---|---|---|
| `README.md` | Human overview | Welcome, live preview, submission tracking, and reference links |
| `AGENTS.md` | Agent contract | Execution invariants, strict constraints, and agent routing |
| `CONTEXT.md` | Canonical router | This file: pipeline status, page requirements, and system contracts |
| [brand-spec.md](brand-spec.md) | Brand reference | Palette (#F27A21, #2B3990, #F4BD6A, #F9F9F9), typography, cans, and assets |
| [direction-approved.md](direction-approved.md) | Design decision | Decision record for Direction C base + Direction A headings + Direction B panels |
| `index.html`, `about.html`, etc. | Product output | The canonical static HTML pages at root |
| `site.css`, `site.js` | Shared system | Tokens, nav, buttons, labels, cart, and the global footer |
| `assets/` | Asset library | High-resolution WebP posters, transparent can renders, logos, and mockups (`assets/merch/` holds the merch mockups) |
| `scripts/` | Tooling | Link checkers, `sync_assets.py` (the one path from the team's source files into `assets/`), and asset generators, including `generate_merch_mockups.py`, `build_scene_mockups.py`, and `outline_ring.py` (outline shapes as mitered rings) |
| `wix-assets/` | Source exports | Print exports and PDF materials for Wix migration |
| `source/` | Archival source | Original 8-page brand deck and raw asset extracts |
| `design-demos/` | Archive | Initial concept explorations (A: Sticker Pop, B: Three Moods, C: Charged Geometry) and `og-card.html`, the source of the share card. Earlier portal and OG drafts were removed on 2026-11-19 and remain in Git history |
| `router.html` | Print source | The locked Three Columns web portal poster, built into `VIVE.pdf`; never deployed |
| `.vercelignore` | Deploy boundary | Keeps everything except the four pages, `site.css`, `site.js`, `assets/`, and `vercel.json` off the live site |
