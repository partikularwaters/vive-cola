---
title: Layout
summary: Full-bleed color grounds, a centered content column, wide side gutters, and diagonal cuts between sections.
order: 4
---
# Layout

A section paints its ground across the full width of the screen and keeps its content inside generous side gutters. Sections meet at diagonal cuts instead of straight lines.

<!-- specimen: cuts -->

## Gutters and the content column

| Token or class | Value | What it does |
| --- | --- | --- |
| `--gutter` | `max(clamp(16px, 7vw, 120px), calc((100% - 1240px) / 2))` | Side padding: at least 7vw, and on wide screens the content holds at 1240px |
| `.wrap` | `padding-inline: var(--gutter)` | Puts a section's content inside the gutters |
| `--cut` | `clamp(28px, 5vw, 72px)` | Depth of every diagonal cut |

## Cuts

| Class | Shape |
| --- | --- |
| `.cut-down` | The bottom edge slopes down to the left |
| `.cut-up` | The top edge slopes, and the section tucks under the one above |
| `.cut-both` | Both edges slope |

```html
<section class="posters wrap cut-up pat pat-sparse">…</section>
```

## Rules

- Each hero keeps equal space above and below its content (112px at desktop widths).
- The sticky header sits above every page; in-page links stop 96px below the top (`scroll-padding-top`).
- VIVI stands in a gutter only at 1280px and wider. See [VIVI](../components/mascot.md).
- Decorative shapes never overlap text, buttons, images, cards, or VIVI between 1280 and 1920px.
