---
title: Patterns
summary: Three approved repeating tiles, used sparingly, one per section.
order: 6
---
# Patterns

Three patterns turn a color ground into a branded surface: Confetti Toss, Confetti Sparse, and Star Seal. They are SVG tiles in `assets/patterns/`, built by `scripts/build_patterns.py`.

<!-- specimen: patterns -->

## Using a pattern

Add `.pat` and one pattern class to a section. The tile sits on a layer between the section's ground and its content.

```html
<section class="intro wrap pat pat-seal">…</section>
```

| Class | Tile |
| --- | --- |
| `.pat-confetti`, `-warm`, `-white`, `-deep`, `-navy` | Confetti Toss, 312px |
| `.pat-sparse`, `-light`, `-blue` | Confetti Sparse, 640px |
| `.pat-seal`, `-sun`, `-white`, `-blue`, `-deep` | Star Seal, 140px |

`--pat-op` sets the strength (default 0.16), and `--pat-mask` can fade the tile with a gradient.

## Rules

- Use patterns sparingly. A heavier first pass felt suffocating.
- One pattern per section, and never on a section that already carries large shapes.
- On navy, deep, or ink grounds, use the blue-toned tiles (`-blue`, `-deep`, `-navy`) at full strength.
- A pattern tile never contains the VIVE logo or its letters.
- Keep patterns off product cards: shelves that hold cards stay plain.
