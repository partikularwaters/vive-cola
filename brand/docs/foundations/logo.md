---
title: Logo
summary: The VIVE wordmark, where the middle letters read as an exclamation mark and IV for the four vitamins.
order: 1
---
# Logo

The VIVE wordmark sets its middle letters as a bold exclamation mark and **IV**, the Roman numeral for the four vitamins in every can. The logo is an image drawn in Gardin Bold Rounded. Never set it as live text.

<!-- specimen: logo -->

## Colorways

The "!" and the second V are always a different color from the other letters. Use the colorway made for the ground, as set in the Brand Guidelines (page 6).

| File | Letters and !V | Use it on |
| --- | --- | --- |
| `assets/logo/vive-wordmark-on-orange.webp` | White, with a navy !V | Orange: the site header and this kit's top bar |
| `assets/logo/vive-wordmark-on-blue.webp` | White, with an orange !V | Navy and blue grounds |
| `assets/logo/vive-wordmark-on-dark.webp` | Orange, with a white !V | Black and the darkest grounds: the footer on ink |
| `assets/logo/vive-wordmark-on-light.webp` | Orange, with a navy !V | White and off-white grounds |
| `assets/logo-vive-navy-tagline.png` | The monogram with "The vitamin-charged cola" | Reference |
| `assets/icons/icon-512.png` and `favicon.ico` | App icon and favicon: VIVI on a deep navy tile | Browser tabs and home screens |

All four colorways come from the official files in the team's Drive (`Group 1 - (VIVE)/Logo/`) through `scripts/sync_assets.py`.

## Rules

- Never use a one-color wordmark. A logo that is all navy or all white breaks the brand rule.
- Keep the wordmark's proportions. Scale it by height only.
- Give it clear space at least the height of its exclamation mark on every side.
- Do not recolor it, outline it, add a drop shadow or glow, or rearrange its letters.
- Never place it inside a pattern tile, and never rebuild its letters from shapes.

```html
<a href="index.html"><img src="assets/logo/vive-wordmark-on-orange.webp" alt="VIVE home" width="119" height="32"></a>
```
