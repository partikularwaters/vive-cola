---
title: Cart button
summary: The header's cart button with a live item count, and the panel it opens.
order: 3
---
# Cart button

The cart button sits at the end of the primary navigation on every page. Its badge shows a live count of the items in the cart, kept in `localStorage` so it carries across pages and visits.

<!-- specimen: cart-button -->

## Using it

Ship the button in each page's nav markup, after the link list. `site.js` wires it and builds the panel it opens, so the nav never shifts when the script runs.

```html
<nav class="wrap" aria-label="Primary">
  …
  <button type="button" class="cart-btn" popovertarget="cart-panel"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 7V6a5 5 0 0 1 10 0v1h3.2l-1.3 15H5.1L3.8 7H7Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg>Cart <span class="cart-count">0</span><span class="vh"> items</span></button>
</nav>
```

## Behavior

- The panel is a native popover. It scales in from the button's corner in 200ms and exits in 140ms.
- The count badge pops (`.bump`) when an item is added.
- Any `<button data-add>` inside an element with `data-id`, `data-name`, and `data-price` adds that item, using the nearest quantity input.

## Rules

- There are no cart, checkout, or payment pages. The panel lists items, a total, "Keep shopping," and "Clear cart."
- The button has a fixed size, so a count change never shifts the nav.
