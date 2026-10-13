# publish-log.md — Elysia Tools → WordPress (blog.flowrust.com) cron publish log

| WP ID | Date (UTC) | Slug | Tool | 1-POST? | Notes |
|---|---|---|---|---|---|
| 8208 | 2026-10-12 03:11 | bls-threshold-signature-dkg-field-guide-when-one-rogue-key-can-forge-the-whole-aggregate-2026-10-12 | BLS Boneh–Lynn–Shacham Threshold Signature Aggregation + DKG Simulator | 1-POST + 1-PATCH | EM_IN_CODE: 5 (md_to_html italic regex on math `*` inside backticks) — patched via POST back. 0 issues post-PATCH. |
| 8215 | 2026-10-12 07:34 | geocache-letterbox-munzee-stage-cache-puzzle-hunt-coordinate-validator-field-guide-when-five-encodings-one-input-box-and-the-30-meter-checker-threshold-decide-whether-the-hunt-2026-10-12 | Geocache Letterbox Munzee Stage-Cache Puzzle-Hunt Coordinate Validator | 1-POST 0-PATCH | Custom dark-navy+cyan-teal Playwright poster (umbrella's `article_poster_creator.py` defaults to zh-CN — bypassed via direct HTML). 3 forest-theme editorial-dense cards via umbrella `render_card.py`. 16/16 post-publish checks PASS (0 H1, 8 H2, 3 highlight-card, 1 article-poster, 4 imgs, 3 elysia anchors, 0 wpautop strip, 0 backslash strip, 0 merged bullets, 0 placeholder). |
| 8222 | 2026-10-12 11:47 | mvt-mapbox-vector-tile-pmtiles-google-mvt-projection-and-tilelive-encoding-auditor-field-guide-when-moveto-lineto-and-closepath-lie-about-topology-2026-10-12 | MVT Mapbox Vector Tile PMTiles Auditor | 1-POST + 1-PATCH | Patched MERGED_NUMBERED_LIST (2 blocks: H2 #2 "three layers" + H2 #8 "Tippecanoe/Tilelive/Tile/MapLibre") → rebuilt into `<ol><li>...`. PIL poster + 3 cards via umbrella PIL templates (deep-navy + cyan-teal theme) with `vision_analyze` pre-POST QA. safe_md_to_html wrapper (10 `*`-in-backticks spans; WP 5805/6370 lesson). 0 audit findings post-PATCH. 17th clean umbrella-PIL run of cadence. Cron-prompt inline credentials returned 500 on urllib POST (Cycle #54 SSL EOF class) — fell back to curl subprocess for all REST + media uploads.
| 8230 | 2026-10-12 16:04 | xlsx-csv-batch-converter-field-guide-when-delimiter-encoding-and-date-system-decide-whether-the-batch-lands-clean-or-corrupts-a-week-of-monkey-work | XLSX CSV Batch Converter | 1-POST + 1-PATCH | Patched MERGED_BULLET_LIST (5 blocks: H2 #1 Direction A/B/C; H2 #3 BOM/Win1252/Mixed; H2 #5 Combine/Numbered/Named; H2 #7 Pass-through/Descriptive/Manifest; H2 #8 pandas/Power Query/DuckDB/SQL Server/Snowflake) + MERGED_NUMBERED_LIST (1 block: H2 #2 Eight Decisions 1-8) → rebuilt into `<ul><li>...</li></ul>` HTML. Custom dark-navy + cyan-teal poster (1280×800, Playwright full-page); 3 highlight cards: card1 cyan-teal 8-tile Eight Settings; card2 orange 3-panel Encoding Pitfalls (BOM, Win-1252, Mixed); card3 purple 3-column Naming Conventions (Pass-through, Descriptive, Manifest.json). vision_analyze pre-POST QA on all 4 PNGs — clean (no tofu, no overflow). 0 audit findings post-PATCH.
| 8237 | 2026-10-12 20:21 | thyroid-index-field-guide-when-six-patterns-hide-inside-one-tsh-result-and-the-unit-trap-tells-you-2026-10-12 | Thyroid Index (TSH/FT4/FT3 Interpretation) | 1-POST + 1-PATCH | Patched MERGED_BULLET_LIST (2 blocks: H2 #2 "Why the pattern matters" + H2 #6 "The clinical moves") → rebuilt into <ul><li>...</li></ul> HTML (WP 5676/6212 recipe; en-dash &#8211; split). 3 highlight-card (5-tile six-patterns / 5-tile unit-conversions / audit five-moves) + 1 article-poster (PIL, deep-navy + cyan-teal) via umbrella templates. vision_analyze pre-POST QA clean. 0 audit findings post-PATCH. Cron-prompt inline credentials held via canonical creds + curl subprocess (5-retry backoff, --http1.1, UA, Expect: empty header on POST). |

## 2026-10-13 00:30 UTC — WP 8246 — corrected-qt-bazett-fridericia

- Title: Corrected QT (QTc) Field Guide: When Three Formulae on the Same Strip Disagree by 80 ms
- Tool: Corrected QT (QTc) Calculator (Bazett/Fridericia/Framingham) — id=corrected-qt-bazett-fridericia
- Link: https://blog.flowrust.com/2026/10/13/corrected-qt-bazett-fridericia-field-guide-when-three-formulae-on-one-strip-disagree-by-up-to-80-ms-2026-10-13/
- date_gmt: 2026-10-13T00:30:55
- Asset: poster (1080x800) + 3 highlight cards (1600x900 each)
- Anchors (post + public): 4× `/en/tools/corrected-qt-bazett-fridericia` (real ID) + 1× `/en/tools` kind-root
- Result: 1-POST 0-PATCH clean
- Notes: umbrella PIL fallback (article-poster-creator + article-highlight-cards missing on disk)

## 2026-10-13 04:42 UTC — WP 8252 — regression-analyzer

- Title: Regression Lives in the Browser Now
- Tool: Regression Analyzer — id=regression-analyzer (Data Analysis)
- Link: https://blog.flowrust.com/2026/10/13/regression-analyzer-field-guide-when-four-numbers-per-csv-decide-whether-the-line-holds-2026-10-13/
- date_gmt: 2026-10-13T04:42:15
- Asset: poster (1080x800) + 3 highlight cards (1600x900 each, PIL)
- Anchors: 4× `/en/tools/regression-analyzer` (real ID) + 1× `/en/tools` kind-root
- Result: 1-POST + 1-PATCH (or 1-POST + 1-trash + 1-PATCH to fix content defects)
- Notes: First POST (8252) had MERGED_BULLET_LIST (2) + MERGED_NUMBERED_LIST (1) from ` – **bold** — body` en-dash itemized lists (WP 5676/5683/6212 family). Rebuild source MD with explicit `<ul><li>` + `<ol><li>` HTML; re-substitute URLs. Second run created dup post 8254 (slug collision `-2`); trashed and PATCHed WP 8252 with corrected content via POST endpoint. Audit clean: 0 findings, 3 cards, 1 poster, 4 anchors all 200, 4 imgs all 200. Umbrella PIL fallback. vision_analyze pre-POST QA clean.

## 2026-10-13T08:52:25 — regex-linter-field-guide-when-five-redos-shapes-hide-inside-one-line-of-regex-2026-10-13 (WP 8268)
- Title: Regex Linter Field Guide: When Five ReDoS Shapes Hide Inside One Line of Regex
- URL: https://blog.flowrust.com/2026/10/13/regex-linter-field-guide-when-five-redos-shapes-hide-inside-one-line-of-regex-2026-10-13/
- Status: publish, featured_media=0
- Shape: 0 H1 / 8 H2 / 0 H3 / 1 poster / 3 cards / 62 codes / 24 strongs / 7 uls
- Elysia anchors: 6 unique (3 samples + 2 tool + 1 root)
- All 4 image URLs + 6 elysia URLs HEAD 200
- Audit: 0 findings after 1 PATCH (POSSIBLE_BACKSLASH_STRIPPED on `d+d+` -> `&#92;d+&#92;d+`)
- Total round-trips: 1 POST + 1 PATCH
- Skill fallback: umbrella PIL stack (article-poster-creator + article-highlight-cards missing per WP 6206/6352)
2026-10-13 2026-10-13T13:07:07 | WP 8275 | isin-validator-field-guide-when-twelve-characters-traverse-three-validation-layers-2026-10-13 | ISIN Validator Field Guide: When Three Layers Hide Behind One Luhn Check

## 2026-10-14 - WP 8281 - audio-melody-contour-extractor
- slug: audio-melody-contour-extractor-field-guide-when-five-knobs-decide-which-polyphonic-voice-becomes-the-midi-line-2026-10-13
- url: https://blog.flowrust.com/2026/10/14/audio-melody-contour-extractor-field-guide-when-five-knobs-decide-which-polyphonic-voice-becomes-the-midi-line-2026-10-13/
- date_gmt: 2026-10-13T17:10:42
- title: Audio Melody Contour Extractor Field Guide
- 1-POST 0-PATCH clean
- poster + 3 highlight cards (5tile / 4tile compact / 2col input-output)
- 0 audit findings, 0 placeholder leaks, 0 phantom anchors
- 8 H2 / 0 H1 / 0 H3

## 2026-10-13 — WP 8287 (structured-log-analyzer)

- **Title**: Structured Log Analyzer Field Guide: When Three Log Formats Hide Inside One Paste
- **Slug**: structured-log-analyzer-field-guide-when-three-log-formats-hide-inside-one-paste-and-the-export-format-decides-whether-the-pipeline-2026-10-13
- **Link**: https://blog.flowrust.com/2026/10/13/structured-log-analyzer-field-guide-when-three-log-formats-hide-inside-one-paste-and-the-export-format-decides-whether-the-pipeline-2026-10-13/
- **Status**: publish
- **Tool**: Structured Log Analyzer (structured-log-analyzer)
- **Category**: Data Processing
- **Description**: Detect common log formats, extract core fields, infer field types, and export parsed logs as JSON, CSV, or SQL inserts
- **Anchors**: 1 tool + 4 samples + 1 kind-root = 6 elysiatools.com links
- **Assets**: 1 poster (1080x800) + 3 cards (1600x900)
- **Audit**: All checks PASS — 8 H2, 0 H1, 1 poster, 3 cards, 4 imgs, 6 anchors, no md_links, no backslash strips
- **Path**: /Users/quyue/www/blog/2026-10-13-structured-log-analyzer-field-guide-when-three-log-formats-hide-inside-one-paste-and-the-export-format-decides-whether-the-pipeline
