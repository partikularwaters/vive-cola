# Direction approved (2026-11-15)

Shown: `design-demos/A-sticker-pop.html`, `B-three-moods.html`, `C-charged-geometry.html`.

Client's words:
> Direction C has the best look and feel, especially the hero section. But Direction A has some good ideas after the hero section, including the tilted headers and slightly slanted posters. The sliding-emphasis effect of the photos (what's the right term?) in the hero section of Direction B may be useful in other parts of the website.

## What that means for the build
- **Base:** C. Orange ground, 10-point star, triangles, diagonal section cuts, snap-in motion, and the C hero as-is.
- **From A, after the hero:** tilted label headings (the slanted color bars behind section titles) and posters set at slight angles.
- **From B, kept in reserve:** the expanding panels (on hover, one photo panel widens while the others shrink). Candidate: the six-person team on About Us.

---

# Router Poster Approved (2026-11-17)

Shown: `design-demos/router-dir-1.html` (Charged Burst Hero), `router-dir-2.html` (The Flavor Trio), and `router-dir-3.html` (Editorial Billboard).

Client's words:
> Direction 3. But it should have the three variants.
> Let's not make Stevia front-facing. Just say zero calories, naturally sweetened. Mention the vitamins for each can then. Final file in the target location is VIVE.pdf
> Let's follow the style of `/product` page.
> And do not save anything extra in the target location. Just the PDF

## What that means for the build
- **Base Visual Language:** Follows the `/product` page architecture:
  - Deep Navy hero ground with floating brand triangles (`var(--sun)`, `var(--orange)`, and `var(--white)`).
  - Headline hierarchy directly matching `/product`: "Three cans. *Four vitamins each.*" with "Zero Calories • Naturally Sweetened" badge.
  - Signature fanned trio (`.trio`) centered over concentric 10-point stars in sun and white.
  - Three distinct variant strip cards styled after the `/product` variant sections (VIVE Glow in Sun ground, VIVE Classic in Orange ground, and VIVE Focus in Deep Navy ground), each bearing watermark numeral `IV` and chamfered `.v-chip` vitamin listings.
  - "In Every Can" facts row directly from `/product` line 237 (4 Vitamins, 0 Calories, 100% Naturally Sweetened, 12 oz Cold Can).
  - Bottom launchpad router with full-width button, live beacon `vive-cola.vercel.app`, and retailer badges.
- **Nutritional & Vitamin Breakdown:**
  - VIVE Glow (Radiant Vibes · Skin Health): Vitamins A, B7, C, and E.
  - VIVE Classic (Good Vibes · The Original): Vitamins A, B9, B12, and C.
  - VIVE Focus (Sharp Vibes · Mental Edge): Vitamins B6, B9, B12, and C.
- **Interactive Routing:** Single-page PDF with 100% full-surface click target routing to `https://vive-cola.vercel.app`.
- **Target Deliverable Constraint:** Exactly one file in the target location (`VIVE.pdf`), with zero extra files or preview images in that folder. Master HTML maintained at `router.html` and compiled via `scripts/build_router_pdf.py`.
