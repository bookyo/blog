# 2026-08-08 — WP 5762 — Data Deduplicator Field Guide

- **Post ID**: 5762
- **Date GMT**: 2026-08-08T11:46:59
- **Status**: publish
- **Slug**: data-deduplicator-field-guide-2026-08-08
- **URL**: https://blog.flowrust.com/2026/08/08/data-deduplicator-field-guide-2026-08-08/
- **Tool ID**: data-deduplicator (manifest member; category: Data Processing)
- **Tool name**: Data Deduplicator
- **Featured media**: 0 (TOP PITFALL defense held)
- **Body H1 count**: 0 (no duplicate theme H1)
- **Body H2 count**: 8 + 1 theme "Post navigation" = 9 total
- **Article-poster figures**: 1
- **Highlight-card figures**: 3
- **Elysia anchors** (4 unique): data-deduplicator (×2), array-analyzer, column-remover, /en/tools root — all HTTP 200
- **Image URLs** (4 unique): poster.png, card1.png, card2.png, card3.png — all HTTP 200
- **Word count**: 1140
- **Audit findings** (audit_post_content): 0
- **Patches**: 0 — clean 1-POST run

## Defense layer held end-to-end

- `featured_media: 0` in payload (COSESAI theme hero-duplication avoided)
- 0 body H1 (theme `<h1 class="entry-title">` is the only H1)
- 0 raw markdown links in source HTML
- 0 `<p>` inside `<h2>` (false-positive-safe inner-content check)
- 0 backslash inside `<code>` spans (no KSES strip risk)
- 0 RAW_ITALIC after stripping `<code>` blocks first (all italics dropped in source — `*post-hoc*`, `*keep longest*`, `*exact equality*`, `*keep last*`, `*intra-key collisions*`, `*normalizer → deduplicator → sorter*` rewritten as **bold** before md_to_html)
- 0 MERGED_BULLET (all bullet lists used `- **bold lead**` markdown not en-dash bullet pattern; no PATCH trip needed)
- p_opens/p_closes balanced: 14/14 (md_to_html) → 15/15 (rendered post-WP-autop, browser_console)
- DOM check (browser_console): h1=1, h2=9 (8 body + 1 theme), article-poster=1, highlight-card=3, p=15, all 4 of my body imgs have valid alt text (2 missing-alt images are theme sidebar assets outside article content)
- Visual QA (`vision_analyze`): poster subtitle measured before render (1040 cap); all 4 PNGs passed overflow / tofu / overlap checks
- 3 elysia slugs pre-validated against `tool-manifest.json` (`data-deduplicator`, `array-analyzer`, `column-remover`) — all manifest members, no phantom URLs
- `featured_media=0` confirmed via separate REST list-query after publish

## Per-card design choices

- `card1` = `render_card_5tile` — 5 workflow inputs (paste rows / key columns / strategy / fuzzy / statistics)
- `card2` = `render_card_4tile_compact` 1-row — 4 survivor strategies (KEEP FIRST/LAST/COMPLETE/LONGEST) with OLDEST/NEWEST/DENSEST/LONGEST count strings — extends the WP 5755 / WP 5676 short-multi-word-count fix
- `card3` = `render_card_audit` 2-column — 4 numbered metric checks on left, run output (1200 → 1108) on right with verdict table + HIDDEN-cluster warning

## State update

- `covered_slugs` to add: `data-deduplicator`

## Tools referenced

- /en/tools/data-deduplicator (primary)
- /en/tools/array-analyzer
- /en/tools/column-remover
- /en/tools (root)