---
title: Button
summary: The angled button with an offset shadow block, in four colors.
order: 2
---
# Button

The button has a chamfered right edge and a shadow block that slides out on hover. Hover the samples to see it; press one to see the squeeze.

<!-- specimen: button -->

## Using it

Use `<a class="btn">` for navigation and `<button class="btn">` for actions. Add one color class.

```html
<a class="btn orange" href="shop.html">Grab a VIVE!</a>
<a class="btn white" href="product.html">See the flavors</a>
<button class="btn navy add" type="button" data-add>Add to cart</button>
```

## Variants

| Class | Ground, text, and shadow | Use it on |
| --- | --- | --- |
| `.btn.navy` | Navy, off-white text, orange shadow | Light and sun grounds |
| `.btn.orange` | Orange, deep navy text, sun shadow | Navy and light grounds: the primary call to action |
| `.btn.white` | Off-white, navy text, orange shadow | Navy and orange grounds: the second action |
| `.btn.sun` | Sun, navy text, orange shadow | Navy and light grounds |

`.btn.is-added` fills the button sun for a beat after an item goes into the cart; `site.js` sets it.

## Rules

- One primary button per section. A second action uses a quieter color beside it.
- Labels are short and say what happens: "Grab a VIVE!", "See the flavors," or "Add to cart."
- The hover never moves the button's hit area; only the shadow block moves.
- On navy and deep grounds, add `.on-dark` to the section so the focus ring turns sun.
