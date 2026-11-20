---
title: Posters and ads
summary: The intro poster, the three variant posters, the ad, and the share card.
order: 2
---
# Posters and ads

The posters and the ad are the team's own work, synced into `assets/` by `scripts/sync_assets.py` from the team's Drive folder.

<!-- specimen: posters -->

| File | What it is | Where it runs |
| --- | --- | --- |
| `assets/poster-intro-hires.webp` | Intro poster, "Your dose of good vibes," 1350×1800 | Home, after the hero |
| `assets/poster-classic-hires.webp`, `-glow-`, `-focus-` | Variant posters, 1024×1636 | Home's [poster row](../blocks/poster-row.md) |
| `assets/model-classic-web.webp`, `-glow-`, `-focus-` | The poster photos without headlines, cropped square with matched head sizes | The Shop can reveal |
| `assets/mockup-intro-bus-shelter.webp`, `-street-wall.webp` | The intro poster in place | Home, "Spotted around town" |
| `assets/video/vive-ad.mp4` and `vive-ad-cover.webp` | The 45-second ad and its cover | Home's video strip |
| `assets/og-card.png` | The 1200×630 share card | Link previews for every page |

## Rules

- Never crop a poster's headline in a full poster view.
- Alt text names the variant and describes the scene: "VIVE Glow poster: a woman in pink closes her eyes and holds up a pink VIVE Glow can."
- New or corrected posters enter through `scripts/sync_assets.py`, never by hand.
