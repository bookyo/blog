# 2026-08-05 — AI Prompt A/B Variant Generator (WP 5643)

**Tool:** AI Prompt A/B Variant Generator
**Slug:** ai-prompt-ab-variant-generator-field-guide-2026-08-05
**Post ID:** 5643
**Date (UTC):** 2026-08-05T04:02:52
**URL:** https://blog.flowrust.com/2026/08/05/ai-prompt-ab-variant-generator-field-guide-2026-08-05/

## Asset URLs
- poster: https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-poster-ai-prompt-ab-variant-generator-field-guide-2026-08-05.png
- card1:  https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card1-ai-prompt-ab-variant-generator-field-guide-2026-08-05.png
- card2:  https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card2-ai-prompt-ab-variant-generator-field-guide-2026-08-05.png
- card3:  https://blog.flowrust.com/wp-content/uploads/2026/08/jarvis-card3-ai-prompt-ab-variant-generator-field-guide-2026-08-05.png

## Stats
- Body words: ~2420
- Closing words: 105
- H2 sections: 8 (3 with highlight-card anchors)
- Elysiatools links: 9 (4 unique tool slugs)
- Audit: 0 findings (after PATCH)
- All HEAD checks: PASS (5/5 elysia links, 4/4 images)
- Score: 0.7752 (B+) before publish; 0 issues after
- Round-trips: 1 POST + 1 PATCH (body-H1 strip — COSESAI theme duplicate-H1 recipe)

## PATCH log
1. POST: published with `featured_media: 0` ✓
2. Browser DOM check: `article.querySelectorAll('h1').length === 2` → CONFIRMED COSESAI theme duplicate-H1 bug
3. PATCH: stripped body `<h1>` matching post title (87 chars), re-audited: 0 findings
4. Re-verified: `h1_count=1` (theme entry-title only), `h2_count=9` (8 body + 1 wpai-auto-tags-link wrapper), `card_count=3`, `poster_count=1`, `img_no_alt=0` (article-scoped)
