---
title: Product shelf
summary: A shelf of product cards with tilted photos, a price, a quantity stepper, and an add-to-cart button.
order: 6
---
# Product shelf

A shelf is a section of product cards: the Shop's cans, packs, and merch. Each card has a tilted photo, a name, one line of description, a price, a quantity stepper, and **Add to cart**.

[See it live on the Shop](https://vive-cola.vercel.app/shop#merch)

## Markup

```html
<article class="item" data-item data-id="merch-headband" data-name="Sport headband" data-price="249">
  <div class="art lift-zone" style="--g:var(--orange)"><div class="lift"><img class="photo" src="assets/merch/headband.webp" alt="Sport headband mockup: white band with navy edges, the orange VIVE wordmark, and sun triangles" width="900" height="900" loading="lazy"></div></div>
  <h3>Sport headband</h3>
  <p class="desc">Match VIVI's look. A stretch-knit sweatband with the wordmark up front.</p>
  <div class="buy">
    <p class="price">₱249</p>
    <div class="qty">
      <button type="button" data-step="-1" aria-label="Decrease quantity for Sport headband">−</button>
      <label class="vh" for="q-merch-headband">Quantity for Sport headband</label>
      <input id="q-merch-headband" type="number" inputmode="numeric" min="1" max="99" value="1">
      <button type="button" data-step="1" aria-label="Increase quantity for Sport headband">+</button>
    </div>
  </div>
  <button class="btn navy add" type="button" data-add>Add to cart<span class="vh">: Sport headband</span></button>
</article>
```

The card styles live in `shop.html`. `site.js` wires the stepper and the button for any element with `data-id`, `data-name`, and `data-price`.

## Featured item

The Merch shelf opens with one featured item before its grid: the VIVI plushie, the best seller. It is the same `.item` with a `.feature` class on a navy panel, the photo at twice the grid size, a sun 10-point star seal reading "#1," a **Best seller** label, and an orange button. Keep one featured item per shelf.

## Rules

- `--g` sets the tilted frame's color. Frames cycle orange, sun, and navy only.
- Shelves that hold cards stay plain: no pattern behind product cards.
- Prices are sample prototype prices, and merch photos are mockups; the page says so in a note.
- The three single-can cards reveal their model photo on hover; see the Shop can reveal in the project decisions.
