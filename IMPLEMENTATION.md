# Software Catalog — Public Showcase: Implementation Record

Locked decisions and end-to-end implementation notes for the public showcase
of Nico's software catalog. Owner: Nico (nstranquist). Date locked: 2026-11-03.

## 1. Design decision (locked)

- **V4 is the chosen design** ("Direction locked — V4 · Nov 2026" marker on page).
  Product-led, Linear/Raycast-style: the real catalog app is the hero,
  near-monochrome + one indigo accent, color only for status meaning.
  Vetted against: Studio Maydit on the Linear/Vercel/Raycast aesthetic
  (clarity over decoration, restraint, typography first, product as hero);
  NN/g research on search, filters and listing/routing pages;
  spell-ui teardowns of Linear and Raycast.
- Rejected and not to be revived for this product: generic editorial ledger (v1),
  maker's logbook/scrapbook (v2), Swiss brutalist (V3a), dark lab instrument (V3b),
  warm studio editorial (V3c).
- The showcase lives (for now) as Muse artifact `software-catalog-tool-v4`
  (static web artifact, saved versions restorable; not in any GitHub repo,
  not publicly shared unless Nico explicitly shares it).

## 2. Data boundary (hard rule)

- Source of truth is the private corpus in `nstranquist/nicos-tools`:
  `nicos-dev/docs/feature-catalog/<surface>/<id>.md` (Markdown + YAML frontmatter),
  indexed by `ndev catalog`. The full private index is ~2,250 entities across
  ~40 surfaces. **The private index is never published.**
- Public output is a projection through the closed `PublicEntity` DTO defined
  in the public `nstranquist/nicos-catalog` repo (`projection.go`):
  allowed fields ONLY — `id`, `name`, `kind`, `status`, `summary` (≤320 bytes),
  `tags`, `url` (clean public HTTPS only), `connections` (between included
  entities only).
- Never projected: launch stage, entrypoint/owner paths, homepage values that
  are not clean public HTTPS URLs, persona/JTBD, pricing, business/valuation,
  telemetry, `since`/dates, stack, health scores.
- Every emitted text field is scanned with the same prohibited-content
  patterns as `projection.go` (home paths, `~/`, file://, drive paths,
  internal path markers, credential pairs, token shapes). A field that trips
  a scan is dropped, never sanitized into publishing.
- Current public slice: **products surface only — 85 products**
  (status = engineering maturity: shipped 30, experimental 47, deprecated 8).

## 3. Repeatable pipeline

Implemented in this folder (`~/workspace/catalog-mapping/`):

1. `pipeline.py` — one command, end to end:
   - Fetch: lists `product.*` files in the corpus via the GitHub connector
     and downloads each file (sequential with retries; parallel fetching
     dropped ~half the files in testing).
   - Project: parses frontmatter, keeps only PublicEntity fields, builds the
     summary from the first prose paragraph, bounds it to 320 bytes, keeps
     connections only where both endpoints are included products.
   - Hygiene: applies the tag rules in §4.
   - Validate: re-scans the finished JSON for prohibited content and
     non-DTO fields; fails the run if anything leaks.
   - Report: writes `public-products.json` + `projection-audit.md`
     (dropped fields and reasons, counts, tag stats).
2. Then the artifact is updated from `public-products.json` (single data
   input; the page embeds exactly that array).

Note: this runner is a faithful host-side implementation of the DTO rules.
The long-term home for it is in-repo, next to the corpus, ideally delegating
to `nicos-catalog`'s `ProjectPublic` once the native corpus format is adapted
to its `Index` type (see ADR-0012 boundary in nicos-tools).

## 4. Tag hygiene (public projection only; corpus unchanged)

Measured on the 85 products (301 distinct tags):

- Drop `manual` (85/85 — provenance marker, not a topic).
- Drop `product` (80/85 — duplicates `kind: product`).
- All other authored tags pass through.
- Presentation rule for the UI: the tag *filter* only lists tags appearing
  on ≥3 products (usable facet); a product's record still shows all of its
  remaining tags.

## 5. Summary repairs at source

16 product records had no public summary because their first prose paragraph
contains a local path (the projection drops the field, fail-closed).
Fix = a minimal edit to that first paragraph in the corpus file: remove only
the path-bearing clause/sentence, keep the product meaning. Exact per-file
patches are in `summary-patches.md`, applied via GitHub to
`nicos-tools` (each file write is an approved GitHub operation), then the
pipeline (§3) is re-run and the artifact refreshed so the summaries appear.

Products: product.elevated, product.grok-viewer, product.jobkit,
product.nicos-career-profile, product.nicos-crypto-platform,
product.nicos-docs-rn, product.nicos-editor, product.nicos-hidden-menubar,
product.nicos-host, product.nicos-ide, product.nicos-scratchpad,
product.nicos-slot-dock, product.nicos-window-switcher, product.nicos-zed,
product.nvr, product.saas-platform-svelte.

Known non-issue: a demo login mentioned in the Guidelines Demo record was
reviewed by Nico on 2026-11-03 and confirmed fine. It is not published in
the showcase summary for that product in any case.

## 6. Relationship to Catalog Gallery and the Explorer (decided)

- **This V4 showcase sits above both**: it is the public front door for the
  catalog story (what the catalog is, the 85 products, how the boundary works).
- **The Nicos Catalog Explorer** (https://nicos-catalog-explorer.nstranquist.workers.dev/)
  is the live demo of the portable engine on synthetic data — linked from the
  showcase as "try the engine", not replaced by it.
- **Catalog Gallery** remains the intended name/frame for the public,
  privacy-safe portfolio inside Nico's own docs/site; the showcase's product
  slice is the Gallery's data, rendered standalone here. If/when the Gallery
  ships in the user site, it should consume the same `public-products.json`
  projection rather than a second hand-made list.
- **Atlas (v3/v4, internal)** is operator tooling over the private index and
  is out of scope for the public surface; the showcase never links to it.

## 7. Status / next

- [x] Design locked, real data live in the artifact.
- [x] Pipeline implemented and validated (this record).
- [x] Tag hygiene applied + artifact refreshed (2026-11-03).
- [x] 16 source summary patches applied to nicos-tools in one commit
      (917aae764ee8b06c4a2ef517e4c53efebb1a83ac, 2026-11-04) + pipeline
      re-run (85 products, 0 without summary) + final artifact refresh
      verified: embedded array deep-equals public-products.json exactly,
      "No public summary" state removed, locked marker and surfaces
      section intact.
- [x] Locked in as a git commit (2026-11-03): exported artifact v10 (the
      live-DOM facade build Nico called "literally PERFECT") into a local
      repo at ~/workspace/catalog-showcase (index.html + dataset + pipeline
      + this record + README), annotated tag v1.0.0 (see `git log` there
      for the commit hash). Local only, no remote.
- [x] Wording and claims review done (WORDING-REVIEW.md); after two
      rejected rewrites the hero was settled in a plain human voice chosen
      by Nico (H1 "A list of the software I make.", eyebrow removed).
- [x] QA pass (v1.2): SEO meta/OG/theme-color, WCAG AA contrast fix,
      heading-order cleanup, drawer focus trap, 40px touch targets, and a
      real List-view bug fixed (wrong column class threw and left the list
      empty). Copy/data/interactions otherwise unchanged.
- [x] Published (2026-11-03, Nico's go): artifact shared publicly
      (muse.ai link, serves v1.2) and the lock-in repo pushed to
      https://github.com/nstranquist/catalog-showcase with tags v1.0.0,
      v1.1.0, v1.2.0 (normal git push via gh login, per Nico's workflow
      rule — no per-file API edits).
