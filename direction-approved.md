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

---

# Web Portal Poster Approved (2026-11-18)

Supersedes the router poster above. The client called the earlier poster "too complicated".

Shown: `design-demos/portal-dir-1.html` (Sun Burst Trio), `portal-dir-2.html` (Three Columns), and `portal-dir-3.html` (Night Stage), side by side in `design-demos/portal-thumbs.png`.

Client's words:
> Let's change the "Official Digital Router" to "Official Web Portal"
> Remove the stores, no logos, no store names.
> website should be one-line.
> Three bottles should be the dominant.
> Three Columns.

## What that means for the build
- `router.html` is now Three Columns: an off-white page, the navy V!VE wordmark, the "Official Web Portal" tag, three full-height color columns (sun, orange, and navy) with one upright can each (Glow, Classic, and Focus), and `vive-cola.vercel.app` on one line under a "Tap anywhere to visit" hint.
- No stores, store names, or retailer logos. No vitamin lists or price.
- Brand shapes are SVG images, because WeasyPrint ignores CSS `clip-path`.
- The whole page links to `https://vive-cola.vercel.app`. The final file in the Drive `Website` folder is `VIVE.pdf`, built by `scripts/build_router_pdf.py`.
- The previous `router.html` is kept as `design-demos/router-before-portal.html`.

**Drafts removed (2026-11-19).** The `router-dir-*`, `portal-dir-*`, and `simple-dir-*` drafts, their comparison sheets, and `router-before-portal.html` were deleted once Three Columns was locked. The tracked files remain in Git history through commit `1100eae`; the `simple-dir-*` drafts were never committed.

**Locked (2026-11-18).** Client's words:
> We should settle with this design until I decide otherwise

Do not redesign `router.html` or rebuild `VIVE.pdf` with a different design until the client asks. The automatic PDF rebuild in the pre-commit hook is off; run `python3 scripts/build_router_pdf.py` by hand when a rebuild is wanted.

---

# Brand Repeating Pattern (shown 2026-11-19, awaiting choice)

The user asked for a repeating pattern from the `!`, the `!V` monogram, or the V with other brand shapes. The `!V` shapes are traced as vectors from `assets/logo-vive-navy-tagline.png`.

Candidates (`design-demos/pattern-candidates.html` and `.png`): A Bang Rows, B Monogram Canvas, C Charged Chevron, D Confetti Kit, E Star Seal, and F Exclaim Stripe.

Full directions, each with three colorways, a tone-on-tone page background, and a six-pack sleeve:
- `design-demos/pattern-dir-1.html` (Monogram Canvas, from B)
- `design-demos/pattern-dir-2.html` (Charged Chevron, from C)
- `design-demos/pattern-dir-3.html` (Confetti Kit, from D)

`design-demos/pattern-directions-build.py` regenerates the three pages.

Client's choice: pending.

## Batch 2: shapes only (shown 2026-11-19, awaiting choice)

The user kept batch 1 as reference and asked for a new batch with no logo characters, using only the brand shape library.

Candidates (`design-demos/shape-pattern-candidates.html` and `.png`): G Triangle Mosaic, H Star Lattice, I Star Halftone, J Chamfer Checker, K Energy Shards, and L Angled Tape.

Full directions, each with three colorways, a tone-on-tone page background, and a six-pack sleeve:
- `design-demos/shape-pattern-dir-1.html` (Triangle Mosaic, from G)
- `design-demos/shape-pattern-dir-2.html` (Star Halftone, from I)
- `design-demos/shape-pattern-dir-3.html` (Angled Tape, from L)

`design-demos/shape-patterns-build/` regenerates the sheet and the three pages.

Client's choice: pending.

### Confetti Toss (shown 2026-11-19, chosen 2026-11-20)

The user asked to try batch 1's Confetti Kit without the logo characters. `design-demos/shape-pattern-dir-4.html` keeps its layout and angles: each V became a 10-point star, a spiky star, a concentric star badge, or a chamfered square; each `!` became the slim acute triangle; 4-point sparkles, diamonds, and short angled-banner strips fill the gaps.

### Choice (2026-11-20)

User, on Confetti Toss: "Yes. Let's apply that with these notes". Mid-turn the user added: "E. Star Seal is also acceptable for a pattern, but strictly no Vive logo."

- `scripts/build_patterns.py` writes both patterns to `assets/patterns/`: Confetti Toss tiles (`confetti-*.svg`) and Star Seal tiles (`seal-*.svg`). Star Seal stamps a 4-point sparkle in each 10-point star where batch 1 used the !V mark.
- `site.css` `.pat` puts a tile on a section through a `::before` layer with its own opacity.

# Lighter Orange (2026-11-20)

The instructor suggested a lighter orange against the brand navy; the user asked to apply it everywhere if an experiment worked. `design-demos/orange-experiment.html` and `.png` compare the print orange #F27A21 with #F98A3A, #FF9447, and #FF9D52 in the navbar, the hero accent, beside sun, and on a patterned ground.

Applied: #FF9447 (option B). Navy text on it is 4.58:1 (from 3.63:1), deep navy is 6.24:1, and it still separates from sun. The lighter options C and above start to merge with sun. `build_patterns.py` recolors the shape SVGs in `assets/shapes/` to match.

# Pattern restraint (2026-11-20)

User: "the brand patterns have been applied excessively and feels suffocating. We should apply them more strategically." Then, for the three variant posters: "create a new pattern with less population to create more breathing room." `build_patterns.py` adds Confetti Sparse (`sparse-*.svg`): nine Confetti Toss shapes on a 640px tile.
