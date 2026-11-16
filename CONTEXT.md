# VIVE Website — Canonical Router and Scope Contract

This document is the canonical router and functional contract for the VIVE four-page website prototype. It defines the page specifications, folder roles, quality constraints, and build sequence.

## Pipeline and Current Status

| Page | File | Status | Input Dependencies | Human Check Gate |
|---|---|---|---|---|
| 01 Home | [index.html](index.html) | Draft v2 complete | `assets/`, `brand-spec.md`, `direction-approved.md` | Gian / Client review of hero, posters, and video layout |
| 02 About Us | [about.html](about.html) | Draft v1 complete | Founding story, team roster, and team photos | Verify complete names, company roles, and photo look |
| 03 Product | [product.html](product.html) | Draft v1 complete | Can renders, flavor specifications, and nutritional facts | Verify one variant per strip, zero posters, and zero merch |
| 04 Shop | [shop.html](shop.html) | Draft v1 complete | Merch catalog, bundle definitions, and pricing | Verify quantity inputs, cart count behavior, zero checkout |

---

## Canonical Page Specifications

### 1. Homepage (`index.html`)
- **Hero section:** Bold brand statement, 10-point burst, Classic can visual, a vitamin-led paragraph, and clear calls to action. No price in the hero.
- **Posters section:** Present one poster per variant (VIVE Glow, VIVE Classic, and VIVE Focus) at slight angles under the tilted "Pick your vibe" label. Each poster carries the variant name, its tagline, its vitamins, and a "Grab VIVE …" button to `shop.html`. Glow and Focus borrow the deck-era relaxing vibes and grind vibes posters until their own posters exist (see [brand-spec.md](brand-spec.md)).
- **Video section:** Showcase the VIVE video commercial in 16:9 aspect ratio.
- **Additional posters:** Feature campaign extensions and introductory ads (including the courtside volleyball poster and street mockups).
- **Seasonal poster footer:** Additional posters at the very end of the page (such as seasonal or holiday editions).
- **All ads created live here:** The homepage acts as the comprehensive advertising showcase for the brand.

### 2. About Us (`about.html`)
- **Founding story:** Narrative explaining how the business and product started, rooted in the brand name origin (the ending letters of *revive* and *survive*).
- **The team:** Complete names and company roles for the six team members.
- **Brand-aligned photos:** Team photography styled to match the energetic, charged brand aesthetic.
- **Visual mechanic:** Utilizes the expanding panel hover interaction (reserved from Direction B) to showcase the team.

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
- **Motion and micro-interaction standard (`/animate`, `/emil-design-eng`, `/apple-design`):** Interactions must feel energetic, crisp, and physically grounded. Button hovers, poster tilts, Direction B expanding photo panels, and cart badge updates should use snappy easing curves with mandatory `prefers-reduced-motion` support.
- **Punctuation standard:** Mandatory Oxford comma in all lists of three or more items across copy, documentation, and interface text.
- **Interactive fidelity:** The site must feel like an authentic, finished web application. Every button, selector, and link must work. If an external link has no specific sub-page (such as social channels), wire it directly to the platform root (`https://facebook.com`, `https://instagram.com`, `https://tiktok.com`).
- **High-stakes grading:** Gian will grade all assets appearing across these pages (posters, video, product variations, and branding).
- **Asset integrity:** No placeholder photos and no placeholder texts (Lorem Ipsum). All content must be written and staged with genuine assets.
  - **Approved stand-ins (client, 2026-11-16):** until real assets exist, the site may use (1) the VIVE Glow and VIVE Focus concept can renders recolored from the Classic can, (2) the flat merch mockups in `assets/merch/`, and (3) sample shop prices. Each is labeled on the page or in its alt text. Replace them when the real renders, product photos, and prices arrive.
- **Shared system:** Every page loads [site.css](site.css) and [site.js](site.js). `site.js` renders the one global footer, adds the header cart button and cart panel to the primary nav, and keeps the cart count in `localStorage` so it persists across pages and visits. The primary nav sits in a sticky `.site-header` on every page, and in-page links scroll smoothly to a stop below it (`scroll-padding-top: 96px`; reduced motion jumps instantly). Page files keep only page-specific styles.
- **Hover rule:** No hover effect may move its own hit area. Buttons show an offset shadow block behind them; tilting cards and images lift an inner `.lift` (with `pointer-events: none`) inside a static `.lift-zone`. Every hover also waits about 120ms before reversing when the pointer leaves. Together these prevent repeated hover toggling when the pointer rests on an edge.
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
| `assets/` | Asset library | High-resolution WebP posters, can cutouts, logos, and mockups (`assets/merch/` holds the merch mockups) |
| `scripts/` | Tooling | Link checkers and asset generators, including `generate_merch_mockups.py` |
| `wix-assets/` | Source exports | Print exports and PDF materials for Wix migration |
| `source/` | Archival source | Original 8-page brand deck and raw asset extracts |
| `design-demos/` | Archive | Initial concept explorations (A: Sticker Pop, B: Three Moods, C: Charged Geometry) |
