---
title: Motion toggle
summary: The pause button every section with always-turning stars must carry.
order: 4
---
# Motion toggle

Any section whose stars turn without stopping carries a **Motion** button, so a visitor can pause it (WCAG 2.2.2).

<!-- specimen: motion-toggle -->

## Using it

Place the button inside the section. `site.js` toggles `.is-still` on the section, which pauses every `.burst.star` inside it.

```html
<section class="hero cut-down on-dark pat pat-confetti-warm">
  …
  <div class="burst star"></div>
  <button class="motion-toggle" type="button"><span class="vh">Pause </span>Motion <span class="icon" aria-hidden="true"></span></button>
</section>
```

## Rules

- Every hero with turning stars has one, in the same corner on each page.
- Under `prefers-reduced-motion: reduce`, the stars do not turn, so the button is not needed.
