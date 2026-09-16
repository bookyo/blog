# 5h audit cycle — 2026-09-16 ~08:42 UTC (Cycle #44)

**Status:** clean — 5/5 in-scope, 0 PATCH round-trips, 0 false positives.

## Posts audited (raw fetched 5, in-scope 5, OoS 0)

| ID | Slug | Title (truncated) | H2 | Cards | Poster | Imgs | Anchors | Findings |
|----|------|-------------------|----|----|--------|------|----------|----------|
| 7228 | asciimath-latex-mathml-equation-converter-field-guide... | AsciiMath / LaTeX / MathML Equation Converter | 8 | 3 | 1 | 4 | 4 | clean |
| 7217 | font-file-inspector-field-guide... | Font File Inspector | 8 | 3 | 1 | 4 | 4 | clean |
| 7211 | ahu-coil-capacity-calculator-field-guide-2026-09-15 | AHU Coil Capacity Calculator | 8 | 3 | 1 | 4 | 9 | clean |
| 7203 | permutation-combination-subset-generator-with-repeats-field-guide... | Permutation / Combination / Subset Generator | 8 | 3 | 1 | 4 | 8 | clean |
| 7197 | rydberg-formula-calculator-field-guide... | Rydberg Formula Calculator | 8 | 3 | 1 | 4 | 5 | clean |

## Pipeline

1. **REST fetch** — `curl -s -m 30 -u "bted2k:..." ".../wp/v2/posts?per_page=5&orderby=date&order=desc&status=publish&_fields=..."` → `/tmp/wp_latest5.json`
2. **Content audit** — `/private/tmp/wp_build/wp_post_audit.py::audit_post_content()` on each post's rendered content. 0 findings on all 5.
3. **DOM-side probe** — GET `?context=edit` for `content.raw`, count body H2 (DOTALL for nested wpai-auto-tags-link `<a>`, WP 7163 lesson), `<figure class="article-poster">`, `<figure class="highlight-card">`, `<img>`, missing-alt, elysiatools anchors; urllib HEAD on all image src + first 12 anchor URLs + permalink per Cycle #27 recipe.
4. **OoS heuristic** — Cycle #23 CJK-only range check (`0x3040-0x30FF`, `0x4E00-0x9FFF`, `0xAC00-0xD7AF`, `0xFF00-0xFFEF`, `0x3400-0x4DBF`). Greek letters in legitimate math titles (WP 7203 has U+03A0 Π) NOT excluded.

## Notes / observations

- **WP 7203 title contains U+03A0 (Greek capital Pi)** — used legitimately as the multiset-counting formula symbol "N Π M". The Cycle #23 OoS heuristic explicitly excludes Greek (per WP 6163 lesson — false-positive risk on BMP punctuation). Confirmed: title is English-language cron-publish field guide; full audit + DOM probe both clean.
- **WP 7197 title contains U+2081, U+2082, U+221E, U+208F** — subscript/regular digits + infinity symbol (n₁, n₂, R∞). Same family as WP 7203 — non-ASCII but legitimate math typography. Already in-scope, clean.
- **All 5 posts: 8 body H2 + 1 article-poster + 3 highlight-cards + 4 imgs + 0 missing-alt** — canonical cron-publish shape holds across all 5.
- **30 unique elysiatools anchors across 5 posts** (4+4+9+8+5) — all HEAD 200. Sample-capped at 12 per post to stay under 5-min total runtime.

## New lessons

None this cycle. The umbrella's pipeline held cleanly. Browser DOM review was bypassed due to cron-mode Chrome remote-debugging-popup block (WP 6663 fallback); REST + urllib HEAD recipe from Cycle #27 + Cycle #38 + WP 6663 covered all the defects that DOM probes historically caught (LiteSpeed lazy-load false-positive, broken image src, broken anchors, missing-alt).

**30th consecutive cron-mode clean cycle.**
