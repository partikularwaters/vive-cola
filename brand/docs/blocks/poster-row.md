---
title: Poster row
summary: One poster per variant, each tilted on its own color block with its name, line, vitamins, and a button.
order: 5
---
# Poster row

The poster row shows the three variant posters side by side, each tilted on a block of its color, with the variant's name, line, vitamins, and a button to the Shop.

[See it live on Home](https://vive-cola.vercel.app/#vibe-title)

## Markup

```html
<figure style="--b:var(--sun)">
  <div class="art lift-zone"><div class="lift"><img src="assets/poster-glow-hires.webp" alt="VIVE Glow poster: a woman in pink closes her eyes and holds up a pink VIVE Glow can" width="1024" height="1636" loading="lazy"></div></div>
  <figcaption>
    <h3>VIVE Glow</h3>
    <p class="tagline">Your dose of radiant vibes</p>
    <p class="vits">Vitamins A, B7, C, and E to support skin health.</p>
    <a class="btn navy" href="shop.html">Grab VIVE Glow</a>
  </figcaption>
</figure>
```

The row's layout lives in `index.html`; the [hover lift](../components/hover-lift.md) and [button](../components/button.md) come from `site.css`.

## Rules

- Order: Glow, Classic, and Focus, so Classic sits in the middle.
- `--b` sets the block behind each poster: sun for Glow, orange for Classic, and navy for Focus.
- Posters are the team's 1024×1636 files from `assets/`. See [Posters and ads](../assets/posters.md).
