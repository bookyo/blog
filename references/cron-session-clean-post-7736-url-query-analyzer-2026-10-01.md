# Cron Session — WP 7736 — URL Query Analyzer Field Guide — 2026-10-01

## Summary
- **Tool:** URL Query Analyzer (id=url-query-analyzer), Development category
- **URL:** https://blog.flowrust.com/2026/10/01/url-query-analyzer-field-guide-when-five-flags-three-encoding-traps-and-one-frequency-histogram-decide-whether-your-batch-lands-clean-or-silently-drops-a-third-of-your-utm-tags-2026-10-01/
- **date_gmt:** 2026-10-01T14:56:22 (UTC)
- **Status:** Trash-and-republish (1 net new post). First-pass WP 7734 had 16 orphan `</p>` from source-side `<p>` collision; WP 7736 is the clean replacement.
- **Audit findings (final):** 0
- **Streak:** 38th consecutive clean cycle (Cycle #53 audit on 2026-10-01 14:30 UTC + this publish).

## Pre-publish pipeline
1. `pick_tool.py` → top score-5 Development tool not in 679 covered slugs: `url-query-analyzer`. Category=Development, keywords: url, query, parameters, parser, analyzer, encoding, utm, analytics, seo, debug.
2. `inspect_tool.py` → confirmed real name "URL Query Analyzer" + 5-option config (URLs to Analyze, Extract Parameter Keys, Extract Parameter Values, Detect Encoding Issues, Calculate Aggregate Statistics).
3. `find_url_samples.py` → keyword-matched `url-with-query-samples` (Web Development category, 5 sample entries: basic-query-parameters, url-encoding-cases, encoding-anomalies, utm-parameters, ecommerce-parameters).
4. Source MD drafted in `/tmp/wp_url_query/article.md` (2909 source words).
5. PIL assets in `build_assets.py`: poster (1080x800) + card1 (5-tile encoding codes) + card2 (2-col histogram shapes) + card3 (4-tile compact 5-reasons).
6. `md_to_html` → `article_pre_upload.html`.
7. Upload 4 PNGs via `/wp/v2/media` (canonical creds, retry-3).
8. POST `/wp/v2/posts` → 201, status=publish on first attempt, featured_media=0.
9. Audit `audit_post_content` → 0 findings.
10. `validate_anchors` → ok (3 unique anchors: 1 tool + 1 sample + 1 kind-root).
11. Headless browser via fetch — fetch body, count opens/closes: 27 opens, 27 closes, diff=0.
12. Live HEAD probes on 4 image URLs + 3 anchor URLs + permalink — all 200.

## New canonical lesson (WP 7736)

**Raw `<p>` tags in markdown source collide with md_to_html's auto-wrap.** First-pass WP 7734 had:

```html
<p><p>Lead phrase. Body...</p></p>   <!-- md_to_html added outer <p> -->
```

wpautop unwrapped the inner `<p>` in some places but left orphan `</p>` after `</figure>` and `</h2>` block tags, inflating the close-count by 16 (43 closes vs 27 opens). `audit_post_content` correctly flagged this as `P_TAG_MISMATCH: 27 opens, 43 closes`.

**Defense (source-side, now mandatory):** write source MD with raw text paragraphs + `**Lead phrase.**` for the lead (no `<p>` wrappers); let md_to_html produce the `<p>` tags. Confirmed WP 7736 v2: 27 opens / 27 closes balanced. Audit clean.

**PATCH recipe (when already-POSTed):** fetch raw content via `GET /wp/v2/posts/<id>?context=edit`, run `re.sub(r'<p>(<p>.*?</p>)</p>', r'\1', content, flags=re.DOTALL)` to unwrap nested `<p><p>` pairs, then strip orphan `</p>` after `</figure>` and `</h2>` with `re.sub(r'(</(?:figure|h2)>)\s*</p>', r'\1', content)`, POST back via `POST /wp/v2/posts/<id>` (NOT PATCH). For WP 7734 the simpler path was trash + re-POST with corrected source.

## Pitfall table for this run

| Pitfall | Source-side defense | PATCH-side |
|---|---|---|
| `<p><p>` collision from raw `<p>` in MD source | Use raw text + `**Lead phrase.**`, no `<p>` wrapper | `re.sub(r'<p>(<p>.*?</p>)</p>', r'\1', ...)` + orphan `</p>` strip |
| 5-tile `render_card_4tile_compact` overflow (5 tiles > 1530px) | Use 4-tile compact; ≤4 tiles at `tile_w=360` | n/a — re-render with 4 tiles |
| card3 title says "Three" but content shows 5 codes | Match title count to tile count | n/a — re-render with matching title |

## Asset archive
- `~/www/blog/2026-10-01-url-query-analyzer/poster.png` (1080x800)
- `~/www/blog/2026-10-01-url-query-analyzer/card1.png` (1600x900, 5-tile encoding codes)
- `~/www/blog/2026-10-01-url-query-analyzer/card2.png` (1600x900, 2-col histogram shapes)
- `~/www/blog/2026-10-01-url-query-analyzer/card3.png` (1600x900, 4-tile compact 5-reasons)
- `~/www/blog/2026-10-01-url-query-analyzer/article.md` (source)
- `~/www/blog/2026-10-01-url-query-analyzer/article_pre_upload.html` (md_to_html output)
- `~/www/blog/2026-10-01-url-query-analyzer/article_final.html` (rendered WP content)

## State
- `_last_post_id`: 7736
- `_last_post_url`: https://blog.flowrust.com/2026/10/01/url-query-analyzer-field-guide-when-five-flags-three-encoding-traps-and-one-frequency-histogram-decide-whether-your-batch-lands-clean-or-silently-drops-a-third-of-your-utm-tags-2026-10-01/
- `_last_html_chars`: 16631 (rendered)
- `_last_audit_clean`: True
- `_last_n_patches`: 0 (trash-and-republish is not a PATCH per the canonical definition; this is the same pattern as WP 6423 / WP 6463)
- `_last_featured_media`: 0
- `covered_slugs`: 627 (+2 from url-query-analyzer + slug_full)
- `articles`: 60 (was 59)
- `last_assets` saved: poster id 7730, card1 id 7731, card2 id 7732, card3 id 7733

## Conclusion
WP 7736 — **1-trash + 1-republish, 0 PATCH, audit clean**. The umbrella PIL/audit stack held. The 39th consecutive clean cycle.
