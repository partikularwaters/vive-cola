---
title: Shapes
summary: The 10-point star, triangles, and their families, as SVG files in the brand colors.
order: 5
---
# Shapes

The 10-point star and the triangle are VIVE's signature shapes. The full library lives in `assets/shapes/` as SVG files in every brand color, mirrored from `source/deck-extract/`.

<!-- specimen: shapes -->

## Using shapes on a page

Triangles are `<i class="tri">` elements. Set the size, the SVG, and the angle with custom properties. They snap in on load.

```html
<i class="tri" aria-hidden="true"
   style="--s:58px;--c:url(assets/shapes/triangle-equilateral-sun.svg);--r:-24deg;left:42%;top:28px"></i>
```

Stars are elements with the `.star` class and a `background-image`. Large static shapes behind a section's content go in a `.deco` layer:

```html
<div class="deco" aria-hidden="true">
  <i style="--s:420px;--img:url(assets/shapes/star-10pt-sun.svg);--r:12deg;right:-80px;top:40px"></i>
</div>
```

## Rules

- Set shapes at sharp angles. Never straighten a triangle to 0°.
- Place hero triangles in the band above the content, anchor large edge triangles in the gutter, and center small ones in a gutter.
- One layer of background detail per section: shapes or a [pattern](patterns.md), not both.
- Every decorative shape gets `aria-hidden="true"`.
