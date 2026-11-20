---
title: Hover lift
summary: How cards and images tilt and rise on hover without flickering at their edges.
order: 5
---
# Hover lift

Cards and images sit at a slight tilt and straighten and rise on hover. The moving part is an inner `.lift`; the hover belongs to its static parent, `.lift-zone`.

<!-- specimen: hover-lift -->

## Using it

```html
<div class="art lift-zone" style="--tilt:-1.5deg">
  <div class="lift"><img src="assets/merch/cap.webp" alt="VIVE cap mockup" width="900" height="900"></div>
</div>
```

| Property | Default | What it does |
| --- | --- | --- |
| `--tilt` | `0deg` | The resting angle. The hover straightens it to 0 |
| `--rise` | `0px` | The resting offset. The hover lifts it 6px |

## Why it works this way

The `.lift` layer has `pointer-events: none`, so its tilted corners cannot start or end a hover. Only the static zone can. The lift also waits 120ms before falling back, so a pointer resting on an edge never makes it flicker.
