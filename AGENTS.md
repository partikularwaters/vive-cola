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
| Website edit surface (HTML/CSS) | [index.html](index.html), `about.html`, `product.html`, and `shop.html` at root |
| Image assets (logos, cans, posters, mockups) | [assets/](assets/) |
| Agent skills and web standards | `~/.agents/skills/`, `~/.gemini/config/skills/`, and `~/.claude/skills/` |

## Invariants and Execution Rules

1. **Follow `/copywriting` and eliminate `ai-tells`:** Every draft must adhere to conversion copywriting principles. Strictly eliminate AI tells: no contrast reveals ("not X, but Y"), no negation lists ("no X, no Y, no Z"), no trailing pile-on comma clauses, no rhetorical self-questions, and no machine puffery buzzwords ("delve", "streamline", "game-changer", "plethora", "elevate"). Write plain, declarative sentences with concrete customer benefits.
2. **Follow `/modern-web-guidance` for HTML/CSS and client-side interactions:** Treat Google Chrome's modern web guidance as the baseline for markup and styles. Use native semantic HTML elements (`<header>`, `<main>`, `<article>`, `<section>`, `<footer>`, `<dialog>`), modern CSS layouts (CSS Grid, Subgrid, container queries, `:has()`, `@starting-style`), accessible interactive controls (native buttons, forms, video containers), high-performance WebP media loading, and Core Web Vitals guardrails. Search and retrieve modern patterns via `modern-web-guidance` before writing non-trivial components or introducing complex scripts.
3. **Use `/huashu-design` for high-fidelity prototyping and design reviews:** Apply high-fidelity HTML/CSS prototyping principles. For major new layout additions or promotional modules, explore distinct visual directions before settling, and verify visual contrast and presentation quality against the approved brand direction.
4. **Follow `/animate`, `/emil-design-eng`, and `/apple-design` for motion and micro-interactions:** Implement crisp, purposeful interactions. Button hovers, poster tilts, the team name-plate reveal on `about.html`, and cart counter badge updates must feel snappy and energetic rather than floaty. Always include `prefers-reduced-motion` fallbacks.
5. **Follow `/snowe-ui-skill` for brand visual hierarchy:** Enforce brand visual generosity: 10-point stars, triangle cuts, angled header labels, bold color grounds (#F27A21, #2B3990, #F4BD6A, #F9F9F9), and clear typographic hierarchy (Montserrat Bold/Regular with display headings) across all desktop views.
6. **Oxford comma mandatory:** Use the Oxford comma consistently across all newly authored copy, lists, documentation, and headings.
7. **Working links only:** Every link and button must function. Internal navigation links must point to existing site pages (`index.html`, `about.html`, `product.html`, and `shop.html`). External and social links must target the platform root (such as `https://facebook.com` or `https://instagram.com`), never `#`.
8. **Zero placeholders:** Do not use placeholder photos or lorem ipsum text. Use actual brand imagery and copy. The only exceptions are the labeled stand-ins the client approved on 2026-11-16 (merch mockups and sample prices), listed in [CONTEXT.md](CONTEXT.md).
9. **Dynamic visual generosity:** Apply the brand visual language (10-point stars, triangles, angled cuts, and bold color grounds). Avoid plain layouts; implement brand patterns generously.
10. **Scope boundaries:**
   - Dedicated cart, checkout, and payment pages are **out of scope**. Use a live numeric cart count in the header navigation instead.
   - Mobile responsive layout is **out of scope**. Design for desktop presentation.
11. **Standalone deployment readiness:** Ensure all asset paths and links are cleanly resolved when `vive-website/` is pushed as its own root to GitHub and deployed on Vercel. Follow `/deploy-with-vercel` for clean routing and build configuration.
12. **Grading standard:** Gian evaluates all assets appearing here (posters, video, product variations, and branding). Treat all public-facing markup as final grading material.
13. **One place per truth:** When editing or extending requirements, update the canonical owner rather than introducing conflicting copies.
