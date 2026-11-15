# VIVE Website — Agent Authority

You are building the four-page website prototype for VIVE (vitamin-charged cola) in static HTML/CSS. This prototype serves as the visual and structural reference for implementation in Wix, and will be published as a standalone GitHub repository deployed on Vercel.

Built on ICM principles: one place per truth, folders carry structure, and plain files carry state. Do not duplicate specifications; read and respect each document's designated ownership.

## Where Things Live

| Task or Question | Source of Truth |
|---|---|
| Page specifications, stage contracts, and pipeline status | [CONTEXT.md](CONTEXT.md) |
| Brand colors, typography, shapes, product facts, and assets | [brand-spec.md](brand-spec.md) |
| Approved visual direction and motion decisions | [direction-approved.md](direction-approved.md) |
| Human project overview, preview instructions, and samples | [README.md](README.md) |
| Website edit surface (HTML/CSS) | [site/](site/) |
| Image assets (logos, cans, posters, mockups) | [assets/](assets/) |

## Invariants and Execution Rules

1. **Follow `/copywriting` and eliminate `ai-tells`:** Every draft must adhere to conversion copywriting principles. Strictly eliminate AI tells: no contrast reveals ("not X, but Y"), no negation lists ("no X, no Y, no Z"), no trailing pile-on comma clauses, no rhetorical self-questions, and no machine puffery buzzwords ("delve", "streamline", "game-changer", "plethora", "elevate"). Write plain, declarative sentences with concrete customer benefits.
2. **Oxford comma mandatory:** Use the Oxford comma consistently across all newly authored copy, lists, documentation, and headings.
3. **Working links only:** Every link and button must function. Internal navigation links must point to existing site pages (`index.html`, `about.html`, `product.html`, and `shop.html`). External and social links must target the platform root (such as `https://facebook.com` or `https://instagram.com`), never `#`.
4. **Zero placeholders:** Do not use placeholder photos or lorem ipsum text. Use actual brand imagery and copy.
5. **Dynamic visual generosity:** Apply the brand visual language (10-point stars, triangles, angled cuts, and bold color grounds). Avoid plain layouts; implement brand patterns generously.
6. **Scope boundaries:**
   - Dedicated cart, checkout, and payment pages are **out of scope**. Use a live numeric cart count in the header navigation instead.
   - Mobile responsive layout is **out of scope**. Design for desktop presentation.
7. **Standalone deployment readiness:** Ensure all asset paths and links are cleanly resolved when `vive-website/` is pushed as its own root to GitHub and deployed on Vercel.
8. **Grading standard:** Gian evaluates all assets appearing here (posters, video, product variations, and branding). Treat all public-facing markup as final grading material.
9. **One place per truth:** When editing or extending requirements, update the canonical owner rather than introducing conflicting copies.
