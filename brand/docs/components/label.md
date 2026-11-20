---
title: Label
summary: The tilted color strip that carries every section heading.
order: 1
---
# Label

A label is a tilted strip of color behind a heading's words. It is VIVE's heading style: a section title is one or two labels stacked, never plain text.

<!-- specimen: label -->

## Using it

Wrap each line of a heading in `<span class="label">`. A second label tilts less than the first, so the pair reads as one stacked heading.

```html
<h2 id="vibe-title"><span class="label">Pick your vibe</span></h2>

<h2>
  <span class="label sun">The team</span>
  <span class="label white">behind the can</span>
</h2>
```

## Variants

| Class | Ground and text | Use it on |
| --- | --- | --- |
| `.label` | Navy, off-white text | Light, sun, and orange grounds |
| `.label.orange` | Orange, deep navy text | Light and navy grounds |
| `.label.sun` | Sun, navy text | Navy and light grounds |
| `.label.white` | Off-white, navy text | Navy and orange grounds |

## Rules

- Inside `h1` to `h3`, labels become blocks, one per line. Keep a heading to two labels.
- Pick a label color that differs from the ground it sits on.
- Keep heading copy short: two to four words per label.
