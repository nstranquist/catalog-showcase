# Catalog Showcase — V4 (locked)

Public showcase page for Nico's personal software catalog: the V4 design
(product-led, Linear/Raycast-style, near-monochrome + one accent, color only
for status), populated with the real 85 products projected through the
public-safe `PublicEntity` DTO only.

## Lock-in record

- **Locked:** 2026-11-03 (America/Chicago), at Nico's direction after his
  verdict on the final build: "literally PERFECT".
- **Git tag:** `v1.0.0` — this commit.
- **Source of truth at lock time:** Muse artifact
  `software-catalog-tool-v4`, saved version **v10** (live-DOM facade build).
  `index.html` in this repo is the artifact's self-contained export of that
  exact version.
- **Published (2026-11-03):** this repo lives at
  https://github.com/nstranquist/catalog-showcase (public, tags v1.0.0 /
  v1.1.0 / v1.2.0), and the page itself is live on GitHub Pages at
  **https://nstranquist.github.io/catalog-showcase/** — it rebuilds
  automatically from `main` on every push. (An earlier Muse share link
  was retired the same day at Nico's direction: publish on real pages
  hosting, not Muse artifacts.)
- **v1.2 notes:** hero wording settled in a plain, human voice (H1 "A list
  of the software I make.", eyebrow removed), and a QA pass (SEO meta/OG,
  WCAG AA contrast, heading order, drawer focus trap, 40px touch targets,
  plus a fixed List-view bug) was applied with no copy or data changes
  beyond the footer version string.
- **v1.3 notes:** data refresh only — the catalog gained
  `product.catalog-gallery` (the showcase cataloging itself), so the page
  now shows 86 products (31 shipped), 47 connections, and 3 public URLs,
  re-verified end to end; no design or wording changes.

## What's here

- `index.html` — the locked page (self-contained export; data embedded).
- `public-products.json` — the exact projected dataset embedded in the page
  (85 products; shipped 30 / experimental 47 / deprecated 8; 2 public URLs;
  299 tags after hygiene; every product has a summary).
- `pipeline.py` — the repeatable pipeline that regenerates the dataset from
  the private catalog corpus (fetch → project → hygiene → validate →
  report). Working files and the raw corpus cache live outside this repo in
  `~/workspace/catalog-mapping/`.
- `IMPLEMENTATION.md` — the full implementation record: design decision and
  its sources, the hard data boundary, hygiene rules, and the
  Gallery/Explorer relationship decision.

## Interaction model (as locked)

- Fixed-height app window on desktop; sidebar and results panes scroll
  internally; toolbar pinned. Mobile flows with the page.
- Scroll is gated behind a live-DOM facade: the real frame renders inert
  under a tint with a centered "Try It" affordance; page scroll passes over
  it. Click/Enter/Space activates (focus lands in search); Esc or an
  outside click re-covers, preserving filters, search, and scroll state.
- Opening a product record activates the gate in the same action.

## Data boundary (non-negotiable)

Public output is a projection through the closed `PublicEntity` DTO only:
ID, Name, Kind, Status, Summary (≤320 bytes), Tags, allowlisted public URL,
and Connections between included entities. Never publish the private index,
launch stage, entrypoints/paths, pricing/business fields, or telemetry.
Source summaries were fixed in `nstranquist/nicos-tools` commit `917aae7`
so all 85 products project a clean public summary.
