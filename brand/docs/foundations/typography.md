---
title: Typography
summary: Montserrat in four weights, with uppercase Black for display and headings.
order: 3
---
# Typography

Montserrat carries every line of live text, self-hosted in `assets/fonts/` and set by the `--f` token. Black (900) does the shouting, ExtraBold (800) labels things, SemiBold (600) carries body copy, and Regular (400) holds long notes.

<!-- specimen: typography -->

## Roles

| Role | Weight and case | Size |
| --- | --- | --- |
| Display | Black 900, uppercase | 48 to 128px, line height 0.9 |
| Heading | Black 900, uppercase, usually inside a [Label](../components/label.md) | 32 to 72px |
| Eyebrow and button | Black or ExtraBold, uppercase, 0.04 to 0.12em tracking | 13 to 15px |
| Body | SemiBold 600 | 16 to 22px, line height 1.5 to 1.6 |
| Note | Regular 400 | 13 to 15px |

## Rules

- Set sizes with `clamp()` so type scales between 1280 and 1920px wide.
- Paragraphs use `text-wrap: pretty` (set in `site.css`) so none ends on a single word.
- A fallback face, "Montserrat Fallback," is Arial resized to Montserrat's widths, so text keeps its line breaks while the font loads. Keep it in the stack.
- The logo is an image. Never set "VIVE" in Montserrat to stand in for it.
