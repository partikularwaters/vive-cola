---
title: Footer
summary: The global footer, rendered once by site.js on every page.
order: 7
---
# Footer

The footer sits on ink with blue Confetti Sparse and a top edge tilted against the page cuts. Four columns sit under tilted sun labels: the brand with a Shop button, the pages, where to find VIVE, and how to say hi. Social links and the copyright line run along the base.

<!-- specimen: footer -->

## Using it

Every page ends with an empty footer. `site.js` fills it, so the footer is defined in one place.

```html
<footer class="site-footer"></footer>
<script src="site.js" defer></script>
```

## Rules

- Edit the footer in `site.js`, never on a page.
- Retailer logos (Lawson, 7-Eleven, SM, and Ayala Malls) stack on 28px rows.
- Social links go to each platform's root: Facebook, Instagram, and TikTok.
