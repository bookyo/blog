# 5h audit cycle — 2026-09-17 ~15:38 UTC (Cycle #45)

**Status:** clean — 5/5 in-scope, 0 PATCH round-trips, 0 false positives.

## Posts audited (raw fetched 5, in-scope 5, OoS 0)

| ID | Slug | Title (truncated) | H2 | Cards | Poster | Imgs | Anchors | Findings |
|----|------|-------------------|----|----|--------|------|----------|----------|
| 7286 | combinatorial-generation-field-guide-... | Permutation / Combination / Subset Generator Field Guide: When Multinomial Divisor... | 8 | 3 | 1 | 4 | 6/6 | clean |
| 7281 | enteral-nutrition-target-calculator-... | Enteral Nutrition Target Calculator Field Guide: When kcal/kg/day, g/kg/day, and Pump Rate... | 8 | 3 | 1 | 4 | 6/6 | clean |
| 7270 | secure-random-generator-field-guide-... | Secure Random Generator Field Guide: When 64 Hex Chars Beat a 24-Char Password | 8 | 3 | 1 | 4 | 11/11 | clean |
| 7261 | contingency-table-chi-square-fisher-... | Contingency Table Chi-Square Fisher Exact Cramér V Tutor Field Guide: When Seven... | 8 | 3 | 1 | 4 | 5/5 | clean |
| 7254 | od600-cell-density-... | OD600 Cell Density Calculator Field Guide: When Path Length, the Cells-Per-OD Default... | 8 | 3 | 1 | 4 | 4/4 | clean |

## Pipeline

1. **REST fetch** — `curl -s -m 30 -u "$USER:$PASS" ".../wp/v2/posts?per_page=5&orderby=date&order=desc&status=publish&_fields=id,date,date_gmt,slug,title,link,featured_media"` → `/tmp/wp_latest5.json`
2. **Full-content fetch** — `GET /wp/v2/posts/<id>?context=edit` for both `content.raw` (audit) and `content.rendered` (DOM probe). 5 REST calls in single `requests.get` loop, 0 SSL EOF.
3. **Content audit** — `/private/tmp/wp_build/wp_post_audit.py::audit_post_content()` on each post's raw content. 0 findings on all 5.
4. **Rendered DOM probe** — count body H2 (DOTALL for nested wpai-auto-tags-link `<a>`, WP 7163 lesson), `<figure class="article-poster">`, `<figure class="highlight-card">`, `<img>`, missing-alt. All 5 = 8 body H2 + 1 article-poster + 3 highlight-cards + 4 imgs + 0 missing-alt. Canonical cron-publish shape holds.
5. **HEAD checks** — `urllib.request` HEAD on all 4 image src per post (20 total) + all elysiatools anchors per post (32 total: 6+6+11+5+4) + 5 permalinks (57 HEAD requests total). 0 failures.
6. **OoS heuristic** — Cycle #23 CJK-only range check on rendered title. 0 OoS this cycle.

## Notes / observations

- **WP 7286 title contains U+00D7 (multiplication sign ×)** — legitimate typography in the multinomial-divisor formula reference. Cycle #23 OoS heuristic correctly excludes BMP math symbols (per WP 7203 lesson — Greek letters also allowed). Confirmed in-scope.
- **WP 7286 title contains U+00F1 (Spanish ñ in "Combinación")** — already part of English/Spanish formula typography. In-scope. Heuristic ignores it correctly.
- **WP 7281 title contains U+2264, U+2265 (≤, ≥)** — typical range-notation symbols in clinical calculators. In-scope.
- **WP 7261 title contains U+00E9 (Cramér)** — accented Latin. In-scope, heuristic ignores.
- **All 5 posts: 8 body H2 + 1 article-poster + 3 highlight-cards + 4 imgs + 0 missing-alt** — canonical cron-publish shape holds across all 5.
- **32 unique elysiatools anchors across 5 posts** — all HEAD 200. Below 12-anchor sample cap on 4/5 posts (only WP 7270 with 11 needed full set).
- **WP 7270 secure-random-generator: 11 anchors** — most-anchored post this cycle (related tools: random number generator, UUID generator, hash generator, password generator, OTP generator, etc.). All 11 verified.

## New lessons

None this cycle. The umbrella's pipeline held cleanly. Browser DOM review was bypassed due to cron-mode Chrome remote-debugging-popup block (WP 6663 fallback); REST + urllib HEAD recipe from Cycle #27 + Cycle #38 + WP 6663 covered all the defects that DOM probes historically caught (LiteSpeed lazy-load false-positive, broken image src, broken anchors, missing-alt).

**31st consecutive cron-mode clean cycle.**

## Recipe notes

- `audit_pre_publish.py` and `wp_post_audit.py` work cleanly from `/private/tmp/wp_build/` — no path drift detected (Cycle #33 lesson holds).
- `requests` library available in venv; `urllib.request` HEAD-with-retry pattern from WP 5731 / Cycle #27 holds under load (32 elysiatools + 20 image + 5 permalink = 57 HEAD requests in one process, 0 SSL EOF).
- CJK range check `(0x3040-0x30FF, 0x4E00-0x9FFF, 0xAC00-0xD7AF, 0xFF00-0xFFEF, 0x3400-0x4DBF)` correctly excludes: U+00D7 ×, U+00F1 ñ, U+00E9 é, U+2264 ≤, U+2265 ≥, U+2081/U+2082 subscripts, U+221E ∞, U+03A0 Π, U+2014 em-dash, U+2013 en-dash, U+2018-201D smart quotes, U+2026 ellipsis.
- Cron-prompt-supplied `fix_html()` regex helpers correctly bypassed per WP 5729 lesson — would have introduced WP 5805/6135/6171/6323-class regressions.
- Cron-mode `execute_code` BLOCKED per umbrella §0; `terminal` + `python3 /tmp/<file>.py` workflow used throughout.