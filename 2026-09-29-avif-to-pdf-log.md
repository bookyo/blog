## 2026-09-29 04:38 UTC — AVIF to PDF (WP 7635)

- **Post:** [AVIF to PDF Field Guide: When Six Page Sizes, Four Quality Bands, and Three Failure Modes Decide Whether Your AVIF Lands as Print-Ready or as a White Page](https://blog.flowrust.com/2026/09/29/avif-to-pdf-field-guide-when-six-page-sizes-four-quality-bands-and-three-failure-modes-decide-whether-your-avif-lands-as-print-ready-or-as-a-white-page/)
- **Tool:** Convert AVIF to PDF (`avif-to-pdf`, Media category)
- **WP ID:** 7635 (1-POST 0-PATCH clean)
- **Slug:** `avif-to-pdf-field-guide-when-six-page-sizes-four-quality-bands-and-three-failure-modes-decide-whether-your-avif-lands-as-print-ready-or-as-a-white-page`
- **date_gmt:** 2026-09-29T04:38:27
- **Assets:** 1 poster (1080×800) + 3 highlight cards (1600×900), PIL rendered
- **Anchors (3):** `/en/tools/avif-to-pdf` (tool), `/en/samples/avif-samples` (sample), `/en/tools` (kind-root)
- **Audit:** 0 findings (`audit_post_content`)
- **DOM check (REST):** 0 body H1, 8 body H2, 0 H3, 1 article-poster figure, 3 highlight-card figures, 23 `<p>` tags
- **Word count:** 1283 (target 1000-1300) ✓
- **Featured media:** 0 (COSESAI hero dup avoidance)
- **PIL pitfall caught pre-POST (WP 6122 + WP 6149 family):** first-pass card2 (4 quality bands) + card3 (failure modes) used `render_card_4tile` with F_HUGE counts colliding with multi-word body text; `vision_analyze` caught the overlap pre-POST; re-rendered both with `render_card_4tile_compact` (auto-shrink chain 150pt→84pt→64pt) — clean.
- **Skill path:** umbrella path used (cron-prompt listed `article-poster-creator` + `article-highlight-cards` as not-found; on-disk probe confirmed `article-poster-creator` lives inside `~/.hermes/skills/article-writer/article-poster-creator/`, PIL templates used per WP 6185/6206 protocol).
- **State:** covered_slugs 833→834, last_post_id=7635