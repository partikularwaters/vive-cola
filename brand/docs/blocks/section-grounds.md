---
title: Section grounds
summary: How a content section picks its ground, its one layer of detail, and its cuts.
order: 4
---
# Section grounds

Every content section is a full-width color ground with one layer of background detail and diagonal cuts where it meets its neighbors. Alternate grounds so neighboring sections never share a color.

<!-- specimen: section-grounds -->

## Recipe

```html
<section class="posters wrap cut-up pat pat-sparse" aria-labelledby="vibe-title">
  <h2 id="vibe-title"><span class="label">Pick your vibe</span></h2>
  …
</section>
```

1. **Ground:** off-white, mist, sun, orange, navy, deep navy, or ink. Set it in the page's styles with a color token.
2. **One layer of detail:** a [pattern](../foundations/patterns.md) (`.pat .pat-…`) or a `.deco` layer of large [shapes](../foundations/shapes.md). Never both.
3. **Cuts:** `.cut-up`, `.cut-down`, or `.cut-both` where the section meets a different ground.
4. **Heading:** one or two [labels](../components/label.md).
5. **On dark grounds:** add `.on-dark` so focus rings turn sun.

## Ground pairings used on the site

| Ground | Detail | Example |
| --- | --- | --- |
| Off-white | Confetti Sparse | Home's poster row, Product's "In every can" |
| Sun | Star Seal | Home's intro poster and video |
| Navy | Blue Star Seal at full strength | Product's comparison table |
| Ink | Blue Star Seal | About's team |
| Off-white | Confetti Toss | Closing calls to action |
