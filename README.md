# VIVE Website Prototype

A four-page website prototype for **VIVE**, the vitamin-charged cola brand, spanning Home, About Us, Product, and Shop pages. This prototype establishes the visual language, typography, interactions, and content architecture in static HTML and CSS before final production in Wix.

---

## Live Preview

To preview the prototype in a local browser:

```bash
python3 -m http.server 8767
```

Then visit [http://localhost:8767/](http://localhost:8767/) (or `http://localhost:8767/index.html`).

---

## Deliverables and Status

The site has four pages: [Home](index.html), [About Us](about.html), [Product](product.html), and [Shop](shop.html). Page status, open checks, and the next action live in [CONTEXT.md](CONTEXT.md).

---|---|---|---|
| **Home** | [index.html](index.html) | Draft v1 complete | Canonical homepage with vitamin-led burst hero, Glow, Classic, and Focus posters with buttons, ad mockups, and video player container |
| **About Us** | [about.html](about.html) | Draft v1 complete | The friends' founding story, six-person team roster, and expanding panel cards |
| **Product** | [product.html](product.html) | Draft v1 complete | Animated hero, one strip each for Classic, Glow, and Focus, an "In every can" strip, and a vitamin comparison table |
| **Shop** | [shop.html](shop.html) | Draft v1 complete | Single cans, packs, and 11 merch items with quantity selectors, plus a header cart count that persists on every page |

---

## Project Context and Benchmarks

- **Evaluation:** Gian will grade all assets appearing across these pages (posters, video, product variations, and branding).
- **Quality standards:** Every button and link is functional (with external social links pointing to platform homepages), all copy and photos are production-ready, and brand geometry patterns are implemented generously.
- **Copywriting rules (`/copywriting`, `/copy-editing`):** Adheres to the `/copywriting` skill and enforces the Oxford comma. Strictly eliminates machine `ai-tells` (no contrast reveals, no negation lists, no trailing pile-on clauses, and no artificial hype).
- **Modern web standards (`/modern-web-guidance`):** Follows Google Chrome's `modern-web-guidance` for semantic HTML5 structure, modern CSS Grid/Subgrid layouts, native interactive controls, and web performance.
- **Visual prototyping and motion (`/huashu-design`, `/animate`, `/snowe-ui-skill`):** Uses `/huashu-design` for high-fidelity HTML prototypes, `/snowe-ui-skill` for brand visual consistency, and `/animate` with `/emil-design-eng` for snappy, charged micro-interactions.
- **Reference samples:**
  - [Chewla](https://pjconsing.wixsite.com/chewla)
  - [Collide](https://hpearlquinto.wixsite.com/collideyourwaynow)
- **Out of scope:** Dedicated cart or checkout pages (a numeric counter in the header suffices) and mobile responsive styling (the project targets desktop display).
- **Deadline:** Friday.

---

## Standalone GitHub Publishing and Vercel Deployment

This `vive-website/` directory is designed to be extracted and published as its own standalone GitHub repository without including the rest of the parent workspace.

### Publishing to a new GitHub repository

You can isolate and push this folder directly to a new GitHub repository using Git's built-in subtree command:

```bash
# Push only the training/vive-website directory to your new GitHub repo's main branch
git subtree push --prefix=training/vive-website <NEW_GITHUB_REPO_URL> main
```

Alternatively, you can split it into a local deployment branch first:

```bash
git subtree split --prefix=training/vive-website -b deploy-vive
git push <NEW_GITHUB_REPO_URL> deploy-vive:main
```

### Deploying to Vercel

When importing this repository into Vercel:
1. **Framework Preset:** Other / None.
2. **Root Directory:** `./` (the repository root).
3. **Deploy boundary:** [`.vercelignore`](.vercelignore) keeps project material (`design-demos/`, `source/`, `wix-assets/`, `scripts/`, the Markdown docs, and the `router.html` poster source) off the live site. Only the four pages, `site.css`, `site.js`, and `assets/` are served.
4. **Clean URL Routing:** With [`vercel.json`](vercel.json) enabling clean URLs, Vercel natively serves `index.html` at `/`, `about.html` at `/about`, `product.html` at `/product`, and `shop.html` at `/shop` without URL redirects.

---

## Documentation and Canonical Truths

Following the principle of one place per truth, specific domains are maintained in dedicated reference documents:

- **[CONTEXT.md](CONTEXT.md):** The canonical router for the project, detailing stage contracts, pipeline inputs/outputs, and comprehensive page requirements.
- **[AGENTS.md](AGENTS.md):** The authoritative rules and execution invariants for AI coding assistants.
- **[brand-spec.md](brand-spec.md):** Brand color codes, typography standards, flavor formulations, and asset manifests.
- **[direction-approved.md](direction-approved.md):** The approved visual direction combining Direction C's geometry, Direction A's tilted headings, and Direction B's expanding panels.
