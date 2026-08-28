# WP 6486 — accessibility-checker-field-guide

- Date: 2026-08-28T13:18:09 UTC
- date_gmt: 2026-08-28T13:18:09
- Post ID: 6486
- Status: publish
- Title: Accessibility Checker Field Guide: When WCAG 2.1 Compliance Should Not Be a Friday Night Audit
- Slug: accessibility-checker-field-guide-when-wcag-2-1-compliance-should-not-be-a-friday-night-audit-2026-08-28
- URL: https://blog.flowrust.com/2026/08/28/accessibility-checker-field-guide-when-wcag-2-1-compliance-should-not-be-a-friday-night-audit-2026-08-28/
- Tool: accessibility-checker (Validation category)
- Body: 0 H1 + 8 H2 + 3 highlight-card figures + 1 article-poster figure
- Anchors: 4 elysiatools links (3 tool + 1 samples)
- Audit findings: 0
- PATCH round-trips: 0
- Visual QA: 1 re-render cycle (subtitle overflow + tile body overflow + arrow tofu)

## Pitfalls hit
- WP 6390 PIL subtitle left-edge clip (>60 chars at F_MED on W=1080) — re-rendered with shortened subtitle (50 chars)
- WP 6358 5-tile body overflow on `tile_w=290` — split body into 2 lines via `\n`
- WP 6352 Unicode arrow tofu (→ U+2192) — replaced with ASCII `->`

## DOM verification
- 8 body H2 + 1 theme nav H2 = 9 in DOM (canonical WP 6323 lesson)
- 1 theme H1 (`entry-title`) — NOT a body content defect
- 3 highlight-card figures, 1 article-poster figure
- 4 elysiatools anchors (all 200 OK, all validated as real tools)
- 0 nested p-in-h2, 0 empty code tags
- 1 occurrence of lead phrase (no WP 6163 duplicate-intro pattern)
- All 3 card images confirmed 1600×900 via fresh Image() load + curl -sI
- LiteSpeed/native `loading="lazy"` initially reports naturalW=0 — confirmed WP 6197/6323 expected behavior
