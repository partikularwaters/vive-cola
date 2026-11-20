---
title: How to use
summary: Two ways in. Describe a page to an agent, or build it yourself with site.css and site.js.
order: 2
---
# How to use

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

- **Use tokens, never raw values.** Write `var(--navy)`, not `#2B3990`. The tokens are listed in [Colors](../foundations/colors.md) and [Layout](../foundations/layout.md).
- **Compose; do not fork.** Build new sections from existing classes. Do not add a variant to `.btn` or `.label` for one page.
- **One layer of background detail per section.** A section carries a pattern or large shapes, not both.
- **Copy rules:** follow [Voice](../foundations/voice.md). Use the Oxford comma. Avoid contrast reveals ("not X, but Y"), negation lists, and buzzwords.
- **Assets come from `assets/`.** Never hotlink, and never invent an image. New team files enter through `scripts/sync_assets.py`.
- **Desktop first.** The site targets desktop widths from 1280 to 1920px. Mobile layouts are out of scope.
- **Every link works.** Internal links go to the four pages; social links go to the platform root.

## Files an agent can fetch

| File | What it is |
| --- | --- |
| `brand/llms.txt` | An index of every doc, with links and one-line summaries |
| `brand/vive-brand-kit.md` | The entire system in one Markdown file |
| `brand/docs/<section>/<page>.md` | One doc per page, the source of this catalog |
