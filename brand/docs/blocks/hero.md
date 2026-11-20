---
title: Hero
summary: How each page opens, and the parts every hero shares.
order: 2
---
# Hero

Every page opens with a hero that states one idea in display type, backs it with a short paragraph, and offers one or two buttons. Each page's hero looks different on purpose.

[See the Home hero live](https://vive-cola.vercel.app/)

## The four heroes

| Page | Ground | What it shows |
| --- | --- | --- |
| Home | Navy, warm Confetti Toss, cut down | Split: "Your dose of good vibes" with the Classic can on two turning stars |
| About Us | Off-white, Confetti Sparse | Centered story opener, with VIVI rising from two counter-turning stars |
| Product | Off-white, Confetti Toss | A navy headline over three color panels, one per can |
| Shop | Navy, deep Star Seal, cut down | A storefront: VIVI's sticker and three aisle tiles |

## Shared parts

```html
<section class="hero cut-down on-dark pat pat-confetti-warm">
  <i class="tri" aria-hidden="true" style="--s:120px;--c:url(assets/shapes/triangle-equilateral-sun.svg);--r:18deg;left:calc(var(--gutter) - var(--s) - 28px);top:120px"></i>
  <div class="grid wrap">
    <div>
      <h1>Your dose of <em>good vibes</em></h1>
      <p>The vitamin-charged cola. A convenient, refreshing way to get your vitamins A, B9, B12, and C from a cold can of cola.</p>
      <a class="btn orange" href="shop.html">Grab a VIVE!</a>
      <a class="btn white" href="product.html">See the flavors</a>
    </div>
    <div class="stage"><div class="burst back star"></div><div class="burst star"></div><img class="can" src="assets/can-classic-web.webp" alt="VIVE Classic can, 12 oz" width="600" height="1569" fetchpriority="high"></div>
  </div>
  <button class="motion-toggle" type="button"><span class="vh">Pause </span>Motion <span class="icon" aria-hidden="true"></span></button>
</section>
```

The hero's layout styles live in its page's own `<style>` block; the shared parts (`.cut-down`, `.pat`, `.tri`, `.btn`, and `.motion-toggle`) come from `site.css`.

## Rules

- No price in a hero.
- Equal space above and below the content: 112px at desktop widths.
- Turning stars need a [motion toggle](../components/motion-toggle.md).
- The hero's main image loads with `fetchpriority="high"`; nothing else on the page does.
