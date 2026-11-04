# Wording & Claims Review — Catalog Showcase V4 (locked v1.0.0)

Reviewed 2026-11-03 against the locked build (artifact v10 / tag v1.0.0).
Method: every visible string extracted from the page (105 static strings +
dynamic labels), every quantitative claim re-checked against
`public-products.json` and the catalog facts on record. Mandate for this
pass, per Nico: judge copy by the *best* way to say it, not merely the most
historically accurate way.

## Verdict

The page makes **no false claims** — unusual and worth keeping. Every
number checks out. The problems are positioning problems: the copy is
engineer-honest to a fault. It leads with caveats and provenance, repeats
its privacy disclaimer until it dilutes, name-drops three famous brands
before establishing its own, never says Nico's name, and leaves its single
most impressive true claim — that this is a *connected graph*, not a list —
completely unstated.

## Accuracy audit (all verified against the data)

| Claim on page | Truth |
|---|---|
| 85 products | ✅ exactly 85 |
| 30 shipped / 47 experimental / 8 deprecated | ✅ exact |
| "Just 2 of the 85 products carry [a public URL]" | ✅ exactly 2 |
| "roughly 2,250 entities across about 40 surfaces" (private index) | ✅ ~2,257 records, 40 surfaces on record |
| "All 85 products on this page have [a summary]" | ✅ 0 missing; max summary 319 bytes (≤320 rule) |
| Tags copy: "manual" was on all 85; "product" repeats the kind; sidebar lists tags used by ≥3 | ✅ all true (299 distinct tags post-hygiene; 42 facet tags) |
| Connection kinds listed: bridges_to, affiliated_with, replaces, supports | ✅ exactly the 4 kinds present (41/2/1/1 = **45 typed connections**) |
| Explorer "running on synthetic data"; engine Apache-2.0 | ✅ per engine repo/docs on record |
| Status = engineering maturity, not runtime state | ✅ per catalog's own docs |

## Findings

### A. Inconsistencies to fix regardless of taste
1. **Title tag vs H1 mismatch.** Browser title: "Software Catalog — Every
   project, one index". H1: "Every project I build, in one place." Two
   different headlines for the same page (the title is a leftover of the
   rejected v1). Pick one line and use it in both.
2. **"85 products, shown in full"** (hero stat). "Shown in full" fights the
   page's own core message — records are *projections*, deliberately not
   full. It means "all 85 are shown"; say that instead.
3. **Sidebar footnote says "Each record below…"** — the records are beside
   the sidebar, not below it. Spatial copy written for a different layout.
4. **Lexicon drift:** title/H1 say "project", body says "products", the
   sort control's aria-label says "Sort projects". The catalog's own kind
   is `product`. One lexicon: *products* for the things, *catalog/index*
   for the system; "projects" only as loose prose, never in labels.

### B. Positioning — where the best version differs from the accurate one
5. **The hero spends its subhead on a caveat.** "…shown through a
   public-safe projection. Status here is engineering maturity, not whether
   something happens to be running right now." True, and explained again in
   two later sections. The hero's job is the value: one person built and
   maintains this much software, and built the index that keeps it
   coherent. Move the maturity caveat down (it already lives in "How the
   index stays true" and the sidebar heading); let the hero sell scale +
   system.
6. **The strongest claim on the page is missing.** Nowhere does the copy
   say the products form a typed graph: **45 connections** (bridges_to,
   affiliated_with, replaces, supports) between the 85 — that's what makes
   this an index rather than a portfolio grid, and the drawer/sort already
   expose it ("Most connected"). Add it as a hero stat or subhead clause.
7. **Nico's name appears nowhere.** A personal front door whose author is
   an anonymous "I". For visitors evaluating the work, a name is the
   smallest possible trust anchor. Add "— Nico" framing (byline, footer,
   or H1 subline) somewhere deliberate.
8. **Borrowed brands lead the design story.** The Design notes paragraph
   opens with Linear/Vercel/Raycast and claims the grid is "dense enough
   to feel like hundreds of projects" — the page shows 85; "feel like
   hundreds" is vibe copy that undercuts the page's otherwise perfect
   factual record. Keep the citations (they're honest sourcing, in the
   sources list where they belong), rewrite the paragraph to lead with
   what the design does for *this* catalog.
9. **Privacy copy repeats ~10 times** (public-safe ×many, projection,
   private…). It is a genuine differentiator — most portfolios can't prove
   a boundary — but at this density it reads defensive. Keep two strong
   statements (hero-adjacent short form + "Public means projected"
   section), trim the echoes (sidebar footnote, results meta, footer can
   each drop their restatement).
10. **Insider process language on a public page:** "Direction locked —
    V4" (hero badge) and "V4 · locked Nov 2026" (footer) mean nothing to a
    visitor. Now that the build is genuinely versioned, the footer can say
    something real instead: "Showcase v1.0.0". Drop the hero badge or
    replace it with a visitor-meaningful one (e.g. "The public slice —
    updated from the live index" only if/when refresh cadence is real; do
    not claim a cadence the pipeline doesn't yet run on a schedule).
11. **"keep track of" undersells the tool.** Subhead: "Catalog is the tool
    I use to keep track of the software I develop, maintain, and deploy."
    The catalog validates, connects, and projects — "keep track of" is
    spreadsheet language for a graph database with a privacy boundary.

## Proposed rewrites (for approval; nothing applied yet)

Hero:
- Eyebrow: "85 real products, one index" → keep, or fold into H1 (see
  redundancy note: "one index / in one place" currently appears 3× in the
  hero — eyebrow, H1, and the slice sentence).
- H1 options (pick one, use in title tag too):
  a) "Every project I build, in one place." (current — fine, personalize)
  b) "Everything I've built. One index." (stronger claim; true at index
     level — the index holds ~2,250 entities; page must keep making clear
     the *shown slice* is the 85 products)
  c) "85 products. One index. Zero curation." — no; "zero curation" is
     false-adjacent (projection is a form of curation). Rejected in-review.
- Subhead → "I build a lot of software. This is the index I built to hold
  it all — every product I develop, maintain, and deploy, connected to
  everything it touches. Below is the public slice: all 85 products, with
  the private detail projected out." (maturity caveat moves down-page,
  where it already exists twice)
- Stats row → `85 products — the full set` · `30 shipped` · `47
  experimental` · `8 deprecated` · `45 typed connections` · `~2,250
  entities in the private index` · `~40 surfaces` (drop one if the row
  crowds; connections earns its place more than surfaces does)

Sections:
- Sidebar footnote → "Real products, public-safe fields only. Each record
  carries just ID, name, kind, status, summary, tags, a public URL where
  one exists, and connections to other products on this page." (delete
  "below", one word shorter, same truth)
- Design notes paragraph → lead with function: "Built to be scanned, not
  admired: a dense grid, filters with counts, and color that only ever
  means status. The design follows published research and teardowns —
  sources below — rather than decoration." (citations stay in the list)
- Footer → "— the personal index of software by Nico S…, products shown
  here; ~2,250 entities in the full private index. Showcase v1.0.0 · 85
  real products · public-safe projection." (name in; version real;
  V4-insider language out)
- Hero badge "Direction locked — V4 · Nov 2026" → remove (footer carries
  the version now).

## What NOT to change
- Every number. The factual record is perfect; the rewrites above preserve
  each verified claim or state it more strongly without overstating.
- "Public means projected" section — the best-written passage on the page;
  it turns a privacy constraint into proof of rigor. Keep verbatim.
- The status definitions in "Status means maturity" — precise and human.
- No cadence/freshness claims ("updated daily", "live data") unless the
  pipeline gets scheduled; the page is a snapshot and says so implicitly —
  keep it that way.
