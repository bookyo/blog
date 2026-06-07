# Publish Report: 2026-06-08 XSS Payload Detector Article

**Status:** ✅ Published
**Date published (UTC):** 2026-06-07T22:29:42
**Tool covered:** XSS Payload Detector
**Slug:** xss-payload-detector
**Article URL:** https://blog.flowrust.com/2026/06/08/xss-payload-detector-text-field-eight-characters/
**WP Post ID:** 3554

## Content Stats
- **Word count:** 1,726
- **H2 count:** 9
- **Composite score:** 0.7390 (Grade: B)
- **Weakest dimensions:** ending (0.40), voice (0.43), hook (0.55)

## Headlines (article structure)
1. The eight characters that started everything
2. What an XSS detector actually checks
3. The encoding trap
4. How detectors score risk
5. Why naive filters fail
6. What to do with a flagged payload
7. The frontier: DOM-based and mutation XSS
8. Try it before you ship it
9. Closing thought

## Media
- **Poster (WP ID 3550):** XSS Payload Detector: eight characters that run code in your browser
- **Card 1 (WP ID 3551):** What an XSS detector actually checks: 10 attack categories
- **Card 2 (WP ID 3552):** How detectors score risk: LOW / MEDIUM / HIGH / CRITICAL
- **Card 3 (WP ID 3553):** The encoding trap: URL/HTML/Unicode/polyglot detection

## Elysia-Tools Links Embedded
1. `https://elysiatools.com/en/tools/xss-payload-detector` (anchored "Elysia Tools") — ×2 in body
2. `https://elysiatools.com/en/samples/xss-payloads` (anchored "XSS payload samples collection") — ×1 in body
3. Footer "explore more tools" link not added (kept ending sharp)

All links verified HTTP/2 200.

## Fixes Applied
1. **Inline `<code>` literal HTML re-escape (post-publish PATCH):** Gutenberg's wpautop decoded `&lt;img&gt;`, `&lt;iframe&gt;`, `&lt;script&gt;`, `&lt;svg&gt;` entities inside `<code>` blocks back to real tags, then re-parsed them as block elements, breaking the surrounding `<p>` and injecting rogue `</p>` closes. POST-PATCH re-escaped 4 `<code></p>...</code>` blocks (also `<img>`, `<iframe>`, `<svg>` patterns).
2. **Samples URL fix (post-publish PATCH):** initial `/en/samples/xss-payload-samples` returned 404; corrected to `/en/samples/xss-payloads` (matches the actual directory).
3. **Trailing junk cleanup (post-publish PATCH):** article ended with `</div>` and stray `<p></code></p>` artifacts from Gutenberg's last-block processing; trimmed.
4. **YAML frontmatter** used to anchor title (avoiding the `lines[0]` ending-first extraction trap).

## Git Deployment
- **Commit:** `6490dc7`
- **Push status:** ✅ Pushed to `origin/main`
- **Files:** 10 changed, 206 insertions(+)

## Tool Selection Rationale
XSS Payload Detector was selected from the Security category (1672 unpublished tools available). Strong thematic cluster: follows the recent security/detector run (sql-injection, redos-regex, jwt-decoder, iban, isbn, postal-code). Adds a fresh angle (XSS — the original web attack, predating SQL injection) while staying in the "detector/validator" narrative arc. 998 lines of TS source with 10 attack categories and 4 risk levels provided rich source material for specificity.