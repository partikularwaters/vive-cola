# VIVE Website — Canonical Router and Scope Contract

This document is the canonical router and functional contract for the VIVE four-page website prototype. It defines the page specifications, folder roles, quality constraints, and build sequence.

## Pipeline and Current Status

| Page | File | Status | Input Dependencies | Human Check Gate |
|---|---|---|---|---|
| 01 Home | [site/index.html](site/index.html) | Draft v1 complete | `assets/`, `brand-spec.md`, `direction-approved.md` | Gian / Client review of hero, posters, and video layout |
| 02 About Us | `site/about.html` | Not started | Founding story, team roster, and team photos | Verify complete names, company roles, and photo look |
| 03 Product | `site/product.html` | Not started | Can renders, flavor specifications, and nutritional facts | Verify one variant per strip, zero posters, and zero merch |
| 04 Shop | `site/shop.html` | Not started | Merch catalog, bundle definitions, and pricing | Verify quantity inputs, cart count behavior, zero checkout |

---

## Canonical Page Specifications

### 1. Homepage (`site/index.html`)
- **Hero section:** Bold brand statement, price point (₱67), 10-point burst, Original can visual, and clear calls to action.
- **Posters section:** Present the three core flavor posters (`Good Vibes`, `Relaxing Vibes`, and `Grind Vibes`) at slight angles with tilted labels.
- **Video section:** Showcase the VIVE video commercial in 16:9 aspect ratio.
- **Additional posters:** Feature campaign extensions and introductory ads (including the courtside volleyball poster and street mockups).
- **Seasonal poster footer:** Additional posters at the very end of the page (such as seasonal or holiday editions).
- **All ads created live here:** The homepage acts as the comprehensive advertising showcase for the brand.

### 2. About Us (`site/about.html`)
- **Founding story:** Narrative explaining how the business and product started, rooted in the brand name origin (the ending letters of *revive* and *survive*).
- **The team:** Complete names and company roles for the six team members.
- **Brand-aligned photos:** Team photography styled to match the energetic, charged brand aesthetic.
- **Visual mechanic:** Utilizes the expanding panel hover interaction (reserved from Direction B) to showcase the team.

### 3. Product Page (`site/product.html`)
- **Brand product showcase:** Deep focus on the cans, vitamin formulation (Vitamins A, C, B9, and B12), stevia sweetening, and zero-calorie benefits.
- **Strip structure:** Exactly one product variation per strip, except where variants are showcased together as a cohesive family strip.
- **Strict negative constraints:**
  - **NO** product posters are allowed on this page.
  - **NO** merchandise items are allowed on this page.

### 4. Shop Page (`site/shop.html`)
- **E-commerce experience:** Browse and select items with quantity selectors and functional "Add to Cart" interactions.
- **Catalog range:** Individual cans/singles, curated multi-can bundles, and branded merchandise.
- **Cart count state:** Display a true, reactive numeric cart counter in the header navigation.
- **Strict negative constraints:**
  - Dedicated cart, checkout, and payment pages are **not needed** and are excluded.

---

## Operational Standards and Submission Rules

- **Copywriting standard:** Follow the `/copywriting` skill. Copy must be clear, compelling, and grounded in customer benefits. Strictly ban all `ai-tells` (no contrast reveals like "not X, but Y", no negation lists like "no X, no Y, no Z", no trailing pile-on comma clauses, no rhetorical self-questions, and no empty buzzwords).
- **Punctuation standard:** Mandatory Oxford comma in all lists of three or more items across copy, documentation, and interface text.
- **Interactive fidelity:** The site must feel like an authentic, finished web application. Every button, selector, and link must work. If an external link has no specific sub-page (such as social channels), wire it directly to the platform root (`https://facebook.com`, `https://instagram.com`, `https://tiktok.com`).
- **High-stakes grading:** Gian will grade all assets appearing across these pages (posters, video, product variations, and branding).
- **Asset integrity:** No placeholder photos and no placeholder texts (Lorem Ipsum). All content must be written and staged with genuine assets.
- **Dynamic visual generosity:** Apply signature brand patterns generously (10-point star, triangles, diagonal cuts, and contrasting color grounds). Do not settle for plainness.
- **GitHub and Vercel publishing:** The `vive-website/` directory will be published as a standalone repository on GitHub and deployed directly to Vercel. All relative asset links and inter-page navigations must function cleanly in this standalone root structure.
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
| `site/` | Product output | The static HTML and CSS deliverable |
| `assets/` | Asset library | High-resolution WebP posters, can cutouts, logos, and mockups |
| `wix-assets/` | Source exports | Print exports and PDF materials for Wix migration |
| `source/` | Archival source | Original 8-page brand deck and raw asset extracts |
| `design-demos/` | Archive | Initial concept explorations (A: Sticker Pop, B: Three Moods, C: Charged Geometry) |
