# Fertilizer N-P-K Blend Calculator Field Guide

**Post ID:** 5676
**URL:** https://blog.flowrust.com/2026/08/06/fertilizer-blend-calculator-field-guide-2026-08-06/
**Date (UTC):** 2026-08-06T01:14:11
**Tool:** fertilizer-blend-calculator (Utilities)
**Slug:** fertilizer-blend-calculator-field-guide-2026-08-06

## Outcome

| Defense | Held? | Detail |
|---|---|---|
| featured_media=0 | ✅ | WP API confirmed featured_media=0 after POST + PATCH |
| 0 body H1 | ✅ | DOM check shows h1=1 (theme entry-title only), no body H1 |
| 8 body H2 | ✅ | DOM check shows h2=9 = 8 body + 1 theme Post navigation |
| 1 article-poster + 3 highlight-card | ✅ | All 4 figures rendered with alt text |
| elysiatools link types | ✅ | All 3 links are /en/tools/* (correct for tool article) |
| No fabricated slugs | ✅ | All 3 elysiatools URLs return HTTP 200 |
| Pre-publish sanity trio | ✅ | 0 markdown links, 0 placeholders, 0 backslashes, 0 <br/> in <p> |
| Visual QA via vision_analyze | ✅ | 2 PIL defects caught+fixed (cards 2&3 2-row layout) |

## Round-trips

- **1 POST** — initial publish with featured_media=0, 4 inline figures
- **1 PATCH** — fix MERGED_BULLET_LIST (3 merged blocks → 0)

## Pitfalls hit (defended)

1. **PIL 4-tile 2-row layout clipping**: First render of card2 and card3 used
   `tile_h=580, gap_y=30` → 2-row height was 1390 > canvas H=900. vision_analyze
   caught the second row completely cut off. **Fixed:** switched to single-row
   4-tile layout with `tile_h=540, gap_x=30`. New `render_card_4tile_1row` and
   `render_card_4tile_parts_1row` variants in `/tmp/render_assets.py`.

2. **MERGED_BULLET_LIST (3 blocks)**: Three paragraphs in the article used
   en-dash + strong pattern (`- **Urea** at **46-0-0** - **DAP**...`) which
   the audit flags as merged bullet lists. **Fixed via
   `wp_fix_merged_bullets.py`** which splits each `<p>` containing 2+
   `– <strong>` pairs into separate `<p>` blocks. Post-fix: 0 merged blocks.

## Asset summary

- `poster.png` (1080x800, 53161 bytes) — eyebrow "UTILITY / AGRONOMY", title
  "Blend Your Own 10-10-10 in 3 Bags", callout about 4-component bag mix.
- `card1.png` (1600x900, 53582 bytes) — 5-tile 10-10-10 recipe: UREA/DAP/POTASH/
  FILLER/TOTAL with their N-P-K and kg/100kg notes.
- `card2.png` (1600x900, 64853 bytes) — 4-tile single-row "unreachable" card:
  TARGET 10-30-20, BASES 3 salts, ACHIEVED 6.50-30.74-20.00, BATCH 50 kg.
- `card3.png` (1600x900, 63106 bytes) — 4-tile single-row parts-ratio card:
  UREA 1.0/13.23/46-0-0, DAP 1.6/21.74/18-46-0, POTASH 1.3/16.67/0-0-60,
  FILLER 3.7/48.36/inert carrier.

## Elysiatools anchors

- https://elysiatools.com/en/tools/fertilizer-blend-calculator (anchor: "Fertilizer N-P-K Blend Calculator", intro paragraph)
- https://elysiatools.com/en/tools/fertilizer-blend-calculator (anchor: "N-P-K blend calculator", section 2)
- https://elysiatools.com/en/tools (anchor: "Elysia Tools utilities hub", section 8)