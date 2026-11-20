/* ==========================================================================
   VIVE Brand Kit catalog (brand/kit.js), loaded with `defer` on every kit page.
   1. "Copy for agents" copies this page's Markdown; "Copy entire system" copies
      brand/vive-brand-kit.md.
   2. Search filters the sidebar by title and summary; "/" focuses it, and Enter
      opens the first match.
   3. Motion toggles inside specimens pause their stars, as site.js does on the site.
   4. On the footer page, re-points the footer's site links and logos at the site
      root after site.js renders it, because the kit pages sit two folders deep.
   ========================================================================== */
(() => {
  const root = document.body.dataset.root || '';

  /* ---------- Copy ---------- */
  const copyText = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.cssText = 'position:fixed;opacity:0';
      document.body.append(area);
      area.select();
      const ok = document.execCommand('copy');
      area.remove();
      return ok;
    }
  };

  const flash = (btn, ok) => {
    const label = btn.dataset.label || btn.textContent;
    btn.dataset.label = label;
    btn.textContent = ok ? 'Copied' : 'Copy failed';
    btn.classList.toggle('is-done', ok);
    clearTimeout(btn._t);
    btn._t = setTimeout(() => {
      btn.textContent = label;
      btn.classList.remove('is-done');
    }, 1600);
  };

  const pageMd = document.getElementById('doc-md');
  document.querySelector('[data-copy-page]')?.addEventListener('click', async (e) => {
    flash(e.currentTarget, await copyText(JSON.parse(pageMd.textContent)));
  });

  document.querySelector('[data-copy-system]')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    try {
      const res = await fetch(btn.dataset.copySystem);
      if (!res.ok) throw new Error(res.status);
      flash(btn, await copyText(await res.text()));
    } catch {
      flash(btn, false);
    }
  });

  /* ---------- Search ---------- */
  const input = document.querySelector('.kit-search input');
  const links = [...document.querySelectorAll('.kit-nav li a')];
  const empty = document.querySelector('.kit-empty');
  const filter = () => {
    const q = input.value.trim().toLowerCase();
    let shown = 0;
    links.forEach((a) => {
      const hit = !q || (a.textContent + ' ' + a.dataset.summary).toLowerCase().includes(q);
      a.parentElement.hidden = !hit;
      if (hit) shown += 1;
    });
    document.querySelectorAll('.kit-nav details').forEach((d) => {
      const any = [...d.querySelectorAll('li')].some((li) => !li.hidden);
      d.hidden = !any;
      if (q && any) d.open = true;
    });
    empty.hidden = shown > 0;
  };
  input?.addEventListener('input', filter);
  input?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const first = links.find((a) => !a.parentElement.hidden);
      if (first) location.href = first.href;
    } else if (e.key === 'Escape') {
      input.value = '';
      filter();
      input.blur();
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t.closest('input, textarea, select, [contenteditable]')) return;
    e.preventDefault();
    input?.focus();
  });

  /* ---------- Motion toggles inside specimens ---------- */
  document.querySelectorAll('.specimen .motion-toggle').forEach((btn) => {
    const box = btn.closest('.demo');
    const verb = btn.querySelector('.vh');
    btn.addEventListener('click', () => {
      const still = box.classList.toggle('is-still');
      if (verb) verb.textContent = still ? 'Play ' : 'Pause ';
    });
  });

  /* ---------- Footer specimen: point site links at the site root ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    const foot = document.querySelector('.specimen footer.site-footer');
    if (!foot) return;
    const local = (v) => v && !/^(https?:|mailto:|tel:|#|\/)/.test(v);
    foot.querySelectorAll('a[href]').forEach((a) => {
      const href = a.getAttribute('href');
      if (local(href)) a.setAttribute('href', root + href);
    });
    foot.querySelectorAll('img[src]').forEach((img) => {
      const src = img.getAttribute('src');
      if (local(src)) img.setAttribute('src', root + src);
    });
  });
})();
