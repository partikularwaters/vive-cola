---
title: Site header
summary: The sticky orange navigation bar with the wordmark, four page links, and the cart.
order: 1
---
# Site header

The header is an orange bar with a deep navy base line, pinned to the top of every page. It holds the wordmark in its on-orange colorway (white, with a navy !V), the four page links, and the [cart button](../components/cart-button.md).

<!-- specimen: site-header -->

## Markup

```html
<header class="site-header">
<nav class="wrap" aria-label="Primary">
  <a href="index.html"><img src="assets/logo/vive-wordmark-on-orange.webp" alt="VIVE home" width="119" height="32"></a>
  <ul>
    <li><a href="index.html" aria-current="page">Home</a></li>
    <li><a href="about.html">About Us</a></li>
    <li><a href="product.html">Product</a></li>
    <li><a href="shop.html">Shop</a></li>
  </ul>
  <button type="button" class="cart-btn" popovertarget="cart-panel">…</button>
</nav>
</header>
```

## Rules

- Mark the current page with `aria-current="page"`. It gets a color and an inset underline only, so no tab changes size.
- The header is orange on every page, so it always stands apart from the hero below it.
- Once the page scrolls, the bar gains a soft shadow (a `scroll-state` container query).
