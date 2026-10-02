# Publish Log

## 2026-10-02 ~07:47 UTC — WP 7761 — Corrected QT (QTc) Calculator

- **Tool:** corrected-qt-bazett-fridericia (Corrected QT (QTc) Calculator (Bazett/Fridericia/Framingham))
- **Category:** Health
- **Theme cluster:** cardiology, ECG, rate correction, QT prolongation
- **Post slug:** corrected-qt-bazett-fridericia-field-guide-when-three-formulae-one-rate-and-one-spread-decide-whether-your-repolarization-reserve-is-healthy
- **Date GMT:** 2026-10-02T07:47:17
- **Status:** publish (1-POST 0-PATCH clean)
- **Assets:** 1 poster (1080x800) + 3 cards (1600x900)
  - card1: 5-tile 3+2 cheatsheet (3 formulae + 2 rule-of-thumb tiles)
  - card2: 4-tile compact thresholds (450/480/460/500 ms)
  - card3: 2-column input/output worked example
- **Elysia anchors:** 3x `/en/tools/corrected-qt-bazett-fridericia` + 1x `/en/tools` (kind-root)
- **Audit findings:** 0
- **DOM checks:** 0 body H1, 8 H2, 1 article-poster, 3 highlight-card, 4 imgs
- **All URLs HTTP 200:** 6/6 (2 elysia + 4 image uploads)
- **Featured media:** 0 (COSESAI rule)
- **Fallback notice:** article-poster-creator + article-highlight-cards skills not on disk (per cron-prompt notice). Used umbrella `templates/pil_poster_and_cards_network_theme.py` + `templates/custom_pil_card_layouts.py` + `templates/render_card_4tile_compact.py` per WP 6135/6171/6185/6206 fallback pattern.

### Pitfall receipts honored
- WP 6135: canonical creds from `scripts/wp_post_audit.py` (NOT cron-prompt inline creds)
- WP 5683/5738: 3-retry backoff on SSL EOF (not triggered this run)
- WP 6191/6197: extracted full `/uploads/2026/10/<filename>-NN.png` URL from `source_url`
- WP 6122/6370: used `scripts/insert_highlight_cards.py::insert_highlight_cards()` (returns plain str, NOT tuple)
- WP 6197/6323: `featured_media=0` in payload (COSESAI hero dedup)
- WP 6417: pre-POST title-dup H2 check (none found)
- WP 7163: pre-POST `CARD*_URL` placeholder-leak assertion (none found)
- WP 5805/6370: source has no `*` inside `<code>` spans — used plain `md_to_html` (no `safe_md_to_html` needed)
- WP 6463: `render_card_5tile_3plus2` for card 1, 5 items passed
- WP 5755/6054/6068/6122: `render_card_4tile_compact` for card 2 (numeric counts)
- WP 6346: `render_card_input_output_2col` signature uses `left_header/right_header/left_rows/right_rows`
- WP 6390/7144: title and subtitle pre-measured — both fit at intended font sizes
- WP 5663/5699: `vision_analyze` ran on all 4 PNGs pre-POST — 0 defects caught
