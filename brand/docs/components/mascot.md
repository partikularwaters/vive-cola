---
title: VIVI
summary: The VIVE mascot, its three poses, and where it stands on a page.
order: 6
---
# VIVI

VIVI is the VIVE mascot: the V from the wordmark with a sweatband, arms, and legs. It stands in the side gutters beside section titles, and on a turning star in a hero.

<!-- specimen: mascot -->

## Files

| File | Pose | Typical spot |
| --- | --- | --- |
| `assets/mascot/vivi-pointing.webp` | Pointing | Beside a section title, pointing at it (mirror it with `.flip` on the left) |
| `assets/mascot/vivi-running.webp` | Running | Beside a shelf or a call to action |
| `assets/mascot/vivi-dizzy.webp` | Dizzy | Playful moments: "I need more VIVE" |
| `assets/mascot/vivi-need-more-vive.webp` | Dizzy, with the line | The Shop hero sticker |

All four are the team's outlined versions, with a white sticker edge built in.

## Using it

```html
<section class="shelf wrap">
  <img class="mascot left" src="assets/mascot/vivi-running.webp" alt="" width="606" height="720" loading="lazy" style="top:38%">
  …
</section>
```

`.mascot.left` or `.mascot.right` centers VIVI in that side's gutter. It shows only at 1280px and wider, where the gutter can hold it.

## Rules

- VIVI is decoration beside content: `alt=""`, and never on top of text or cards.
- One VIVI per section.
- VIVI faces the title it stands beside.
