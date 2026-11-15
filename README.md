# VIVE Website Prototype

A four-page website prototype for **VIVE**, the vitamin-charged cola brand, spanning Home, About Us, Product, and Shop pages. This prototype establishes the visual language, typography, interactions, and content architecture in static HTML and CSS before final production in Wix.

---

## Live Preview

To preview the prototype in a local browser:

```bash
cd training/vive-website
python3 -m http.server 8767
```

Then visit [http://localhost:8767/site/index.html](http://localhost:8767/site/index.html).

If you are using the desktop editor environment, the launch profile `vive-site` starts this preview server automatically.

---

## Deliverables and Status

| Page | File | Status | Highlights |
|---|---|---|---|
| **Home** | [site/index.html](site/index.html) | Draft v1 complete | Hero section with ₱67 price burst, flavor posters, ad mockups, and video player container |
| **About Us** | `site/about.html` | In progress | Founding story (*revive* and *survive*), six-person team roster, and expanding panel cards |
| **Product** | `site/product.html` | Planned | One product variant per strip, zero posters, and zero merchandise |
| **Shop** | `site/shop.html` | Planned | E-commerce catalog with singles, bundles, merchandise, and live header cart count |

---

## Project Context and Benchmarks

- **Evaluation:** Gian will grade all assets appearing across these pages (posters, video, product variations, and branding).
- **Quality standards:** Every button and link is functional (with external social links pointing to platform homepages), all copy and photos are production-ready, and brand geometry patterns are implemented generously.
- **Copywriting rules:** Adheres to the `/copywriting` skill and enforces the Oxford comma. Strictly eliminates machine `ai-tells` (no contrast reveals, no negation lists, no trailing pile-on clauses, and no artificial hype).
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

When importing the newly created standalone GitHub repository into Vercel:
1. **Framework Preset:** Other / None.
2. **Root Directory:** `./` (the root of the new repo, which directly holds `site/`, `assets/`, and configuration).
3. **Routing Configuration:** A [`vercel.json`](vercel.json) rewrites the root path `/` to `/site/index.html` and cleans URL paths.

---

## Documentation and Canonical Truths

Following the principle of one place per truth, specific domains are maintained in dedicated reference documents:

- **[CONTEXT.md](CONTEXT.md):** The canonical router for the project, detailing stage contracts, pipeline inputs/outputs, and comprehensive page requirements.
- **[AGENTS.md](AGENTS.md):** The authoritative rules and execution invariants for AI coding assistants.
- **[brand-spec.md](brand-spec.md):** Brand color codes, typography standards, flavor formulations, and asset manifests.
- **[direction-approved.md](direction-approved.md):** The approved visual direction combining Direction C's geometry, Direction A's tilted headings, and Direction B's expanding panels.
