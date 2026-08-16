# 7Z Archive Preview Field Guide

**Post ID:** 6080
**URL:** https://blog.flowrust.com/2026/08/16/7z-archive-preview-field-guide-when-you-need-to-list-but-not-extract-2026-08-16/
**Date (UTC):** 2026-08-16T14:53:40
**Tool:** 7z-preview (7Z Archive Preview)
**Category:** Compression
**Tool URL:** https://elysiatools.com/en/tools/7z-preview

## Summary

Field guide on the 7Z Archive Preview tool — the difference between asking "is the right file in here?" and waiting minutes for a 4 GB extraction. ~1900 words, 8 body H2 sections, 3 highlight-card figures (4-tile compact + 5-tile + 4-tile compact), 1 article-poster figure, 5 unique elysia anchors / 11 occurrences.

## Run stats
- PATCH round-trips: 1
- Pre-POST visual QA caught card3 count/note overlap (canonical render_card_4tile with long values); switched to render_card_4tile_compact 1-row.
- WP 5828 safe_md_to_html wrapper corruption on triple-fence content avoided by using plain md_to_html.
- MERGED_BULLET_LIST real positive on `* **bold**` pattern (3 paragraphs in source merged into single `<p>` blocks with WP autop) — PATCH'd to 10 separate `<p>` blocks.

## Defense layer (post-PATCH)
- `featured_media`: 0 (COSESAI hero duplication defense)
- Body H1: 0 (theme `<h1 class="entry-title">` only — DOM h1_count = 1)
- Body H2: 8 (DOM h2_count = 9 = 8 body + 1 theme Post navigation)
- `<figure class="article-poster">`: 1
- `<figure class="highlight-card">`: 3
- PIL visual QA (4/4 passed pre-POST): poster, card1 (4-tile compact), card2 (5-tile), card3 (4-tile compact after re-render)
- Image URLs HTTP 200: 4/4
- Elysia anchor URLs HTTP 200: 5/5 unique
- Phantom-slug check (WP 5729): passed — all slugs verified in tool-manifest.json
- Placeholder-leak check (WP 6060): passed — no `POSTER_URL` / `CARD*_URL` literals
- `audit_post_content()`: clean (0 findings post-PATCH)
- Tag balance: p=34/34, h2=8/8 (canonical regex)