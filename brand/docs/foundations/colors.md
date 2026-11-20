---
title: Colors
summary: Four core colors and four supporting grounds, each with a token and a tested text pairing.
order: 2
---
# Colors

Orange, navy, sun, and off-white are the core four. Deep navy, ink, and mist give the grounds their range. Every color has a token in `site.css`; use the token, never the hex.

<!-- specimen: colors -->

## Tokens

| Token | Hex | Role |
| --- | --- | --- |
| `--orange` | #FF9447 | The main web color: the header, accents, buttons, and display words |
| `--navy` | #2B3990 | The primary dark ground, labels, and body text on light grounds |
| `--sun` | #F4BD6A | Triangles, stars, name plates, and warm grounds |
| `--white` | #F9F9F9 | Light grounds, and text on navy |
| `--deep` | #1D2766 | The footer, the header's base line, and text on orange |
| `--ink` | #14183F | The darkest ground, behind the team portraits |
| `--mist` | #F1F2F8 | A quiet light ground for long reading sections |

Print pieces, the deck, and the can art keep the client's original orange, #F27A21. The web uses the lighter #FF9447 so navy text on it passes contrast (4.58:1).

## Text pairings

| Ground | Text | Contrast |
| --- | --- | --- |
| Orange | Deep navy | 6.24:1 |
| Sun | Navy | 5.9:1 |
| Navy | Off-white | 9.54:1 |
| Off-white | Navy | 9.54:1 |

## Rules

- Never put white text on orange.
- Do not use the deck's purple (#2A2882) as a page ground.
- On blue grounds, patterns switch to blue-toned tiles at full strength instead of fading orange tiles.
