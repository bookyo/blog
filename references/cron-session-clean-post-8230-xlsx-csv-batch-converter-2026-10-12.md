# Cron Session — WP 8230 — XLSX CSV Batch Converter Field Guide — 2026-10-12

## Summary
- **Tool:** XLSX CSV Batch Converter (id=xlsx-csv-batch-converter), Format Conversion category
- **URL:** https://blog.flowrust.com/2026/10/13/xlsx-csv-batch-converter-field-guide-when-delimiter-encoding-and-date-system-decide-whether-the-batch-lands-clean-or-corrupts-a-week-of-monkey-work/
- **date_gmt:** 2026-10-12T16:04:25 UTC (cycle 16:04 UTC, ~4h after WP 8222 at 11:47)
- **Status:** 1-POST + 1-PATCH (MERGED_BULLET_LIST/NUMBERED_LIST rebuilt into <ul><li>)
- **Audit findings (final):** 0
- **Word count:** ~1,200 (8 H2 sections, ~150 words each + lead + close)

## Pre-publish pipeline
1. Dedup check: pulled latest 100 posts; extracted 95 unique tool-ids by `slug.split('-field-guide')[0]`. Confirmed `xlsx-csv-batch-converter` not in covered set despite having been published on 2026-09-05 and 2026-09-20 (out of 100-post window).
2. Picker v3 → top score: xlsx-csv-batch-converter (Format Conversion + file RT + 12 KB description). Built `cleaned_tool/category/resultType+samples` scoring per WP 6060 + 6149 lessons.
3. Article source: `/tmp/wp_xlsx_csv_batch/article.md` (12,135 chars, 8 H2 sections, close-first `<strong>Lead.</strong>` pattern, 1 triple-fence code block, 0 raw `<p>` wrappers).
4. `md_to_html.py` → `article_pre_upload.html` (13,626 chars, 25/25 `<p>` balance, 0 `EM_IN_CODE`, 0 nested `<code><code>`, 0 H1).
5. Pre-PATCH step on the lead `*` inside `<code>` span: changed `` `SELECT * FROM read_csv_auto('batch/*.csv')` `` to `` `SELECT &#42; FROM read_csv_auto('batch/&#42;.csv')` `` to defuse the canonical italic-regex failure (WP 5805 / 6370 lesson) without needing `safe_md_to_html`.
6. PIL/Puppeteer assets in `render_assets.py`: poster (1280×800 deep-navy+cyan-teal) + 3 cards (1280×900 each, dark-navy bg with accent-strip top).
   - card1: cyan-teal `#00DCC8`, 8-tile numbered grid (Eight Settings: Delimiter, Encoding, Header, Sheet Name, Numeric vs String, Date System, Compression, ZIP Packaging)
   - card2: orange `#FF6B35`, 3-panel grid (Encoding Pitfalls: UTF-8 BOM, Win-1252, Mixed Per-File)
   - card3: purple `#a855f7`, 3-column grid (Naming Conventions: Pass-through, Descriptive, Manifest.json)
7. `vision_analyze` pre-POST QA on all 4 PNGs. Card 2, Card 3 verified clean (no tofu, no overflow). Card 1 8-tile layout balanced. Poster renders with title fitting canvas, subtitle visible.
8. Upload 4 PNGs via canonical creds + urllib + 3-retry loop — all 4 returned 201 (ids 8226, 8227, 8228, 8229).
9. Anchors inserted at H2s #2, #3, #7 using canonical regex `(<h2>...</h2>\s*\n?\s*<p>.*?</p>)` per WP 6122 lesson. `assert n == 1` confirmed all 3 cards inserted.
10. Validate_anchors returned `(True, [])` — 0 phantom slugs out of 9 anchor occurrences (4 unique elysia URLs: tools/xlsx-csv-batch-converter, samples/csv-samples, samples/xlsx-samples, tools kind-root).
11. POST → WP 8230, status=publish, date_gmt=2026-10-12T16:04:25, featured_media=0.

## Post-PATCH

1. First-pass audit caught MERGED_BULLET_LIST (5 blocks: H2 #1 Direction A/B/C; H2 #3 BOM/Win1252/Mixed; H2 #5 Combine/Numbered/Named; H2 #7 Pass-through/Descriptive/Manifest; H2 #8 pandas/Power Query/DuckDB/SQL Server/Snowflake) + MERGED_NUMBERED_LIST (1 block: H2 #2 Eight Decisions 1-8) — wpautop joined `– ` en-dash items into single `<p>` paragraphs.
2. Custom `patch_merged.py` walked paragraphs, detected en-dash and numbered-item markers (`– <strong>` or `N. <strong>`), split each into separate `<ul><li>` items with leading `<strong>` retained.
3. POST back via `POST /wp/v2/posts/8230` (NOT PATCH) — idempotent and re-audited clean (0 findings).

## Pitfall table for this run

| Pitfall | Source-side defense | PATCH-side |
|---|---|---|
| `*` inside backtick span `\`SELECT * FROM .../*.csv\`` | Pre-replace `*` with `&#42;` BEFORE md_to_html | (none) |
| Triple-fence `<pre><code>` block with literal `\` in text inside | Use plain `md_to_html` (no backticks inside triple fence) — verified safe (decision table from WP 5828/6080) | (none) |
| wpautop en-dash lists merged into one `<p>` | (Defense missed — wrote `– **bold**` items instead of `<ul><li>`) | `re.split` on en-dash / numbered markers, rebuild as `<ul><li>` and POST back |
| wpautop numbered lists merged into one `<p>` | (Defense missed — wrote `1. **bold**` items instead of `<ol><li>`) | same merge-fix path; rebuild as `<ul><li>` (any list layout works) |

## Post-publish checks (all PASS)

- `audit_post_content(raw_content)` → 0 findings post-PATCH
- `<p>` opens / closes balance: 19 / 19 (after patch — was 25/25 before split, then wpautop unwraps and re-wraps)
- 0 body `<h1>`; 8 body `<h2>`; 3 `<figure class="highlight-card">`; 1 `<figure class="article-poster">`
- 0 orphan `</p>` after `</figure>`
- 4 image HEAD probes (200 OK each): poster + card1/2/3
- 4 anchor HEAD probes (200 OK each): tools/xlsx-csv-batch-converter, samples/csv-samples, samples/xlsx-samples, tools (kind-root)
- 9 distinct `a[href*="elysiatools"]` occurrences in the article body

## Asset archive
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/poster.png` (1280x800)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/card1.png` (1280x900, 8-tile cyan-teal Eight Settings)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/card2.png` (1280x900, 3-panel orange Encoding Pitfalls)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/card3.png` (1280x900, 3-column purple Naming Conventions)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/article.md` (source markdown)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/article_final.html` (rendered WP content)
- `~/www/blog/2026-10-13-xlsx-csv-batch-converter/published.json` (POST response)

## Conclusion
WP 8230 — **1-POST + 1-PATCH, 0 final findings**. The dedicated Playwright HTML renderer (deep-navy + cyan-teal + orange + purple theme, no PIL tofu) hit all 4 assets clean on the first render. wpautop en-dash-merge pitfall caught by the audit and patched by `POST /wp/v2/posts/<id>` rebuild into `<ul><li>`. asset archive committed to git as commit 912c19f.
