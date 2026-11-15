# VIVE website

A four-page website for VIVE, the vitamin-charged cola: Home, About Us, Product, and Shop.
The HTML here is the design draft. The final site will be built in Wix.

## Contents

- [Status](#status)
- [Folder map](#folder-map)
- [The brief](#the-brief)
- [Design decisions](#design-decisions)
- [Preview the pages](#preview-the-pages)
- [Build the next page](#build-the-next-page)
- [Missing content](#missing-content)
- [Wix and publishing](#wix-and-publishing)
- [Before submission](#before-submission)
- [Related files outside this folder](#related-files-outside-this-folder)
- [Working rules](#working-rules)

## Status

Last updated 2026-11-15. Home shows your sharper `wix-assets/` flavor posters.

| Page | File | State |
|---|---|---|
| Home | [site/index.html](site/index.html) | Draft v1 done. Uses the approved direction. Placeholders for the ad video and seasonal posters. Nav links still point to `#`. |
| About Us | `site/about.html` | Not started |
| Product | `site/product.html` | Not started |
| Shop | `site/shop.html` | Not started |

Checked: the homepage at 1280 px and 375 px (no sideways scrolling, all images load).
Not checked yet: links between pages (they don't exist yet) and a full proofread.

## Folder map

| Path | What it is | Edit it? |
|---|---|---|
| `README.md` | This file. Start here. | Yes, keep the status current |
| [brand-spec.md](brand-spec.md) | Colors, type, visual language, product facts, asset list, and what's missing | Yes, when the brand changes |
| [direction-approved.md](direction-approved.md) | Which design direction was chosen, in your own words | Only for a new decision |
| [site/](site/) | **The website draft.** One HTML file per page. | Yes, the main work |
| [design-demos/](design-demos/) | The three homepage directions shown before the choice: A Sticker Pop, B Three Moods, C Charged Geometry | No, kept for reference |
| [assets/](assets/) | Images the pages use: logos, cans, posters, mockups, scenes, and textures. Most come from the brand deck; the `-hires.webp` posters are copies of your `wix-assets/` exports. | Add files; don't rename (pages link to them) |
| [wix-assets/](wix-assets/) | Your exports for Wix: the three flavor posters at 1587×2245 (`10`, `11`, `12` = Good, Grind, Relaxing) in PNG and WebP, plus `vive-posters-pdf/alternative-poster.pdf` ("Want more?", landscape) | Yes |
| [source/](source/) | Source material: `VIVE! - Cola Brand.pdf` (the current 8-page brand deck, where most of `assets/` came from) and `deck-extract/` (raw dump of every image in the deck, 41 files, 89 MB, not used by any page) | No |

Pages in `site/` and `design-demos/` load images with `../assets/...`, so those three folders must stay side by side.

## The brief

From the assignment:

1. **Home:** hero section, all ads, posters, and the video. Other posters (for example, a Christmas poster) go at the bottom.
2. **About Us:** the story of how the business started; the team of six, each with their position; team photos and a background photo that match the brand's feel.
3. **Product:** one product per strip. No posters in the strips. No merchandise on this page.
4. **Shop:** merchandise, bundles, and other items. No checkout page needed.

Before submission: every link and button works, and all text is proofread.

## Design decisions

Full details are in [brand-spec.md](brand-spec.md) and [direction-approved.md](direction-approved.md). In short:

- **Look:** sharp and energetic, vibrant and optimistic, intense but sweet, charged and playful.
- **Shapes:** the 10-point star and triangles. Edges are cut on a diagonal; no rounded corners.
- **Colors:** orange `#F27A21`, navy `#2B3990`, sun `#F4BD6A`, and off-white `#F9F9F9`. Orange is the main background. Don't use the deck's purple for pages.
- **Type:** Montserrat (Google Fonts), bold and regular. The logo is an image, never live text.
- **Direction:** C's hero and shapes, plus A's tilted label headings and slightly slanted posters after the hero.
- **Saved for later:** B's expanding panels (one photo widens on hover while the others shrink). The best fit is the team on About Us.

## Preview the pages

From this folder, start a local server, then open http://localhost:8767/site/index.html:

```bash
python3 -m http.server 8767
```

Opening the HTML file directly also works for most things. The server is closer to how a real host behaves.
In Claude Code's desktop app, the `vive-site` entry in the repo's `.claude/launch.json` starts the same server.

## Build the next page

1. Copy `site/index.html` to the new page name (`about.html`, `product.html`, or `shop.html`). It already holds the shared header, footer, colors, shapes, and heading styles in its `<style>` block.
2. Point the nav links at the real files: `index.html`, `about.html`, `product.html`, and `shop.html`. Mark the current page with `aria-current="page"`. Update the nav on **every** page.
3. Replace the body sections with the new page's content. Reuse the existing pieces:
   - `.label` for tilted headings
   - `.star` for the 10-point star
   - `.tri` for triangles
   - `.cut-down` for a diagonal bottom edge
   - `.btn` for buttons
4. Keep the Product page free of posters and merchandise; those belong on Home and Shop.
5. Check the page at desktop and phone widths: no sideways scrolling, and every image loads.
6. Update the [Status](#status) table.

Once there are two or more pages, consider moving the shared `<style>` into `site/site.css` so a change applies everywhere.

## Missing content

These are honest placeholders in the drafts. Each needs a real file or text from you:

| Needed for | What | Where it goes |
|---|---|---|
| Home | VIVE ad video | Video section (16:9) |
| Home | Christmas and other seasonal posters | "More from VIVE" at the bottom. The "Want more?" poster in `wix-assets/` could fill one spot. |
| About Us | Founding story: who, when, why | Story section. Known so far: the name comes from the end of *revive* and *survive*. |
| About Us | Six team members: names, positions, photos | Team section |
| About Us | A background photo | Page background |
| Shop | Merchandise and bundles: items, photos, prices | Product grid. Only the can price (₱67) is known. |

## Wix and publishing

The plan is: build the site in Wix, capture it, refine it, then publish it.
A test of that pipeline on another Wix site is in [../wix-pipeline/README.md](../wix-pipeline/README.md). Its findings:

- A Wix site can be captured as static HTML, on desktop and phone, with `wix_to_static.py`.
- Wix-run features stop working once captured: the phone menu, shop filters, and cart.
- The recommended route is to treat the HTML here as the design reference. Build in Wix from it, or hand-build clean pages from it and deploy those.
- Publishing to Vercel needs a signed-in Vercel connection.

## Before submission

- [ ] All four pages exist and link to each other from the nav
- [ ] Every button and link goes somewhere real (no `href="#"`)
- [ ] All placeholders replaced with real content
- [ ] Product page has one product per strip, with no posters or merchandise
- [ ] Shop page has merchandise and bundles, with no checkout
- [ ] Text proofread
- [ ] Checked on desktop and phone

## Related files outside this folder

| File | Note |
|---|---|
| [../vive-copy.md](../vive-copy.md), [../vive-brand-explainer.md](../vive-brand-explainer.md) | Earlier brand copy. It describes an older purple can, a leaf logo, and different vitamins (C, B2, folic acid, A). The deck in this folder supersedes it; the naming story still holds. |
| `../VIVE! - Cola Brand.pdf` | An older version of the brand deck. Use the copy in `source/`. |
| [../../vive-posters/](../../vive-posters/) | Earlier poster design work (directions, plates, logo extraction). |
| [../wix-pipeline/](../wix-pipeline/) | The Wix capture tool and its test results. |

## Working rules

- Keep earlier versions. Save new work beside the old (for example, `index-v2.html`) instead of overwriting or deleting it.
- Use your supplied assets as they are. Don't redraw or recolor the logo, cans, or posters.
- Keep personal files out of commits. The repo's `.gitignore` lists them.
