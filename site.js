/* ==========================================================================
   VIVE shared behavior (site.js), loaded with `defer` on every page.
   1. Renders the global footer into <footer class="site-footer"></footer>.
   2. Adds the cart button and cart panel to the primary nav.
   3. Keeps the cart in localStorage so the count persists across pages and visits.
   4. Wires quantity steppers and "Add to cart" buttons ([data-add]) on any page.
   5. Wires any .motion-toggle to pause the motion in its section or aside.
   ========================================================================== */
(() => {
  const STORE_KEY = 'vive-cart-v1';
  /* Simple Icons v13.21.0 glyphs (CC0) */
  const ICONS = {
    facebook: 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z',
    instagram: 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077',
    tiktok: 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z'
  };
  const peso = new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP', maximumFractionDigits: 0 });

  /* ---------- Cart state ---------- */
  const read = () => {
    try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }
    catch { return {}; }
  };
  let cart = read();
  const save = () => {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(cart)); } catch { /* private mode: keep in memory */ }
  };
  const count = () => Object.values(cart).reduce((n, line) => n + line.qty, 0);
  const total = () => Object.values(cart).reduce((n, line) => n + line.qty * line.price, 0);

  /* ---------- One polite live region for announcements ---------- */
  const live = document.createElement('p');
  live.className = 'vh';
  live.setAttribute('aria-live', 'polite');
  document.body.append(live);
  const announce = (msg) => { live.textContent = ''; setTimeout(() => { live.textContent = msg; }, 60); };

  /* ---------- Cart button + panel ---------- */
  const nav = document.querySelector('nav[aria-label="Primary"]');
  let badge;
  if (nav) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cart-btn';
    btn.setAttribute('popovertarget', 'cart-panel');
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 7V6a5 5 0 0 1 10 0v1h3.2l-1.3 15H5.1L3.8 7H7Zm2 0h6V6a3 3 0 0 0-6 0v1Z"/></svg>Cart <span class="cart-count">0</span><span class="vh"> items</span>';
    nav.append(btn);
    badge = btn.querySelector('.cart-count');

    const panel = document.createElement('div');
    panel.id = 'cart-panel';
    panel.className = 'cart-panel';
    panel.setAttribute('popover', 'auto');
    panel.setAttribute('aria-labelledby', 'cart-title');
    panel.innerHTML = `
      <header><h2 id="cart-title">Your cart</h2><button class="close" type="button" popovertarget="cart-panel" popovertargetaction="hide" aria-label="Close cart">&times;</button></header>
      <ul class="cart-lines"></ul>
      <p class="cart-empty">Your cart is empty. Pick a can, a pack, or some merch in the shop.</p>
      <div class="cart-foot">
        <div class="cart-total"><span>Total</span><span class="cart-sum">₱0</span></div>
        <a class="btn navy" href="shop.html">Keep shopping</a>
        <button class="btn white clear-cart" type="button">Clear cart</button>
      </div>`;
    document.body.append(panel);

    /* Firefox and older Safari cannot transition display and overlay, so a plain hidePopover() cuts the
       exit short. There, the close button and the cart button set data-closing, wait for the exit
       transition, then hide. Light dismiss (Esc, outside click) cannot be intercepted and stays instant. */
    let displayTransitions;
    const canTransitionDisplay = () => {
      if (displayTransitions !== undefined) return displayTransitions;
      if (!window.CSS?.supports?.('transition-behavior', 'allow-discrete')) return (displayTransitions = false);
      const probe = document.createElement('div');
      probe.style.cssText = 'transition: display 1s allow-discrete !important; display: block;';
      document.body.append(probe);
      getComputedStyle(probe).display;
      probe.style.display = 'none';
      displayTransitions = getComputedStyle(probe).display === 'block';
      probe.remove();
      return displayTransitions;
    };
    const closeWithExit = async () => {
      panel.setAttribute('data-closing', '');
      const anims = panel.getAnimations();
      if (anims.length) {
        await Promise.race([Promise.allSettled(anims.map((a) => a.finished)), new Promise((r) => setTimeout(r, 600))]);
      }
      if (!panel.hasAttribute('data-closing')) return;
      panel.removeAttribute('data-closing');
      panel.hidePopover();
    };
    const interceptClose = (e) => {
      if (!panel.matches(':popover-open') || (window.CSS?.supports?.('overlay', 'auto') && canTransitionDisplay())) return;
      e.preventDefault();
      closeWithExit();
    };
    btn.addEventListener('click', interceptClose);
    panel.querySelector('.close').addEventListener('click', interceptClose);
    panel.addEventListener('toggle', (e) => { if (e.newState === 'open') panel.removeAttribute('data-closing'); });

    panel.addEventListener('click', (e) => {
      const remove = e.target.closest('[data-remove]');
      if (remove) {
        const { name } = cart[remove.dataset.remove] || {};
        delete cart[remove.dataset.remove];
        save(); render(); announce(`${name} removed from cart.`);
      }
      if (e.target.closest('.clear-cart')) {
        cart = {}; save(); render(); announce('Cart cleared.');
      }
    });
  }

  function render() {
    const n = count();
    if (badge) badge.textContent = n;
    const panel = document.getElementById('cart-panel');
    if (!panel) return;
    const lines = Object.entries(cart);
    panel.querySelector('.cart-lines').innerHTML = lines.map(([id, l]) =>
      `<li><span><b>${l.name}</b><small>${l.qty} × ${peso.format(l.price)}</small></span><span>${peso.format(l.qty * l.price)}</span><button class="remove" type="button" data-remove="${id}" aria-label="Remove ${l.name}">Remove</button></li>`
    ).join('');
    panel.querySelector('.cart-empty').hidden = lines.length > 0;
    panel.querySelector('.cart-foot').hidden = lines.length === 0;
    panel.querySelector('.cart-sum').textContent = peso.format(total());
  }

  const bump = () => {
    if (!badge) return;
    badge.classList.remove('bump');
    void badge.offsetWidth; // restart the keyframe on rapid adds
    badge.classList.add('bump');
  };

  /* ---------- Quantity steppers and Add to cart (any page) ---------- */
  document.addEventListener('click', (e) => {
    const step = e.target.closest('[data-step]');
    if (step) {
      const input = step.closest('.qty').querySelector('input');
      const next = Math.min(99, Math.max(1, (parseInt(input.value, 10) || 1) + Number(step.dataset.step)));
      input.value = next;
      return;
    }
    const add = e.target.closest('[data-add]');
    if (add) {
      const item = add.closest('[data-item]');
      const qtyInput = item.querySelector('.qty input');
      const qty = Math.min(99, Math.max(1, parseInt(qtyInput?.value, 10) || 1));
      const { id, name, price } = item.dataset;
      const line = cart[id] || { name, price: Number(price), qty: 0 };
      line.qty = Math.min(99, line.qty + qty);
      cart[id] = line;
      save(); render(); bump();
      add.classList.add('is-added');
      setTimeout(() => add.classList.remove('is-added'), 900);
      announce(`Added ${qty} ${name} to cart. ${count()} items in cart.`);
    }
  });

  // Keep every open tab in sync
  window.addEventListener('storage', (e) => {
    if (e.key === STORE_KEY) { cart = read(); render(); }
  });

  /* ---------- Global footer ---------- */
  const footer = document.querySelector('footer.site-footer');
  if (footer && !footer.children.length) {
    footer.innerHTML = `
  <div class="foot-cols wrap">
    <div class="foot-brand">
      <a href="index.html"><img src="assets/wordmark-vive-white.png" alt="VIVE home" width="203" height="52" loading="lazy"></a>
      <p>Real vitamins in the cola you already love. Four in every can.</p>
      <a class="btn sun" href="shop.html">Shop VIVE</a>
    </div>
    <nav class="foot-pages" aria-labelledby="foot-pages-h">
      <h2 id="foot-pages-h"><span class="label sun">Pages</span></h2>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="product.html">Product</a></li>
        <li><a href="shop.html">Shop</a></li>
      </ul>
    </nav>
    <div>
      <h2><span class="label sun">Find us at</span></h2>
      <ul class="retailers">
        <li><img src="assets/lawson-logo-white.png" alt="Lawson" width="1280" height="195" style="--h:15px" loading="lazy"></li>
        <li><img src="assets/seven-eleven-logo.svg" alt="7-Eleven" width="273" height="257" style="--h:28px" loading="lazy"></li>
        <li><img src="assets/sm-logo-white.svg" alt="SM Supermalls" width="44" height="44" style="--h:28px" loading="lazy"></li>
        <li><img src="assets/ayala-malls-logo-white.svg" alt="Ayala Malls" width="688" height="276" style="--h:28px" loading="lazy"></li>
      </ul>
    </div>
    <div>
      <h2><span class="label sun">Say hi</span></h2>
      <address class="foot-contact">
        <span><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>123 Street, Quezon City, Philippines</span>
        <a href="mailto:hello@vivecola.com"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 5h18v14H3V5Zm2 2v.5l7 4.6 7-4.6V7H5Zm14 2.9-7 4.6-7-4.6V17h14V9.9Z"/></svg>hello@vivecola.com</a>
        <a href="tel:+639220001234"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1L6.6 10.8Z"/></svg>+63 922 000 1234</a>
      </address>
    </div>
  </div>
  <div class="foot-base wrap">
    <nav class="social" aria-label="Social media">
      <ul>
        <li><a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${ICONS.facebook}"/></svg></a></li>
        <li><a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${ICONS.instagram}"/></svg></a></li>
        <li><a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="${ICONS.tiktok}"/></svg></a></li>
      </ul>
    </nav>
    <small>© 2026 VIVE. The vitamin-charged cola.</small>
  </div>`;
  }

  /* ---------- Motion pause for turning stars and drifting strips ---------- */
  document.querySelectorAll('.motion-toggle').forEach((toggle) => {
    const section = toggle.closest('section, aside');
    toggle.addEventListener('click', () => {
      const still = section.classList.toggle('is-still');
      toggle.querySelector('.vh').textContent = still ? 'Play ' : 'Pause ';
    });
  });

  render();
})();
