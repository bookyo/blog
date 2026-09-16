## 2026-09-15T16:44:12 UTC — WP 7203 — Permutation / Combination / Subset Generator (With Repeats) Field Guide

- Title: Permutation / Combination / Subset Generator (With Repeats) Field Guide: When Five Items, Six Rows, Three Modes, and One Display Cap Decide Whether Your Multiset Count Lands at n! or n!/Π(mᵢ!)
- URL: https://blog.flowrust.com/2026/09/16/permutation-combination-subset-generator-with-repeats-field-guide-when-five-items-six-rows-three-modes-and-one-display-cap-decide-whether-your-multiset-count-lands-at-n-or-n-%cf%80m/
- Tool: combinatorial-generation (Math & Numbers) — Permutation / Combination / Subset Generator (With Repeats): permutations via next_permutation with exact multiset count n!/Π(mᵢ!), combinations as generating-function coefficient Π(1+x+…+x^mᵢ) at x^k, subsets with exact count Π(mᵢ+1) including the empty set; display caps at 200 entries but counts stay exact; 1–12 items, combinations mode requires 1 ≤ k ≤ n.
- date_gmt: 2026-09-15T16:44:12
- Mode: 1-POST 0-PATCH clean
- Assets: 1 poster (1080×800) + 3 cards (1600×900: 1×5-tile "Five Counting Formulas on One Input", 1×5-tile "Three Modes, Three Formulas, One Engine", 1×4-tile compact "Four Places Multiset Math Matters")
- vision_analyze: poster subtitle clipped left+right on first pass (90 chars at F_MED on W=1080 → per WP 6390 lesson); shortened to "Why [A, A, B] yields 3 perms, 2 combinations, 6 subsets" (54 chars) — re-rendered clean. All 4 PNGs clean final.
- elysia anchors: 8 total — 5× /en/tools/combinatorial-generation + 1× /en/tools/assignment-problem-solver + 1× /en/tools/boolean-algebra-simplifier + 1× /en/tools (kind-root) — all 200 OK, validate_anchors=True
- Pre-flight: 0 md-link-leak, 0 placeholder, 0 backslash-in-code, 0 br-in-p, 0 p-in-h2, 0 H1, 0 H3, 1 poster, 3 cards, 8 elysia anchors (no phantom — sample anchor dropped per WP 6116/6390 sample-manifest has no toolId)
- Audit findings: 0 on raw content
- DOM: H1=0 H2=8 H3=0 posters=1 cards=3 imgs=4 anchors=8
- URL check: 9/9 HEAD 200 (4 images + 4 elysia anchors + permalink)
- Picker: sparse_category_picker (canonical pick_tool_v4 returns <5 diverse past 775 covered); top pick combinatorial-generation (Math & Numbers, theme_score=2, score=160.0)
- Skill path: umbrella fallback (article-poster-creator + article-highlight-cards missing from ~/.hermes/skills/ root per WP 6185/6352; bundled PIL templates + cron publish driver used)
- State: covered_slugs 775→776, covered_tool_ids 48→49 (added combinatorial-generation)
## 2026-09-15T20:58:00 UTC — AHU Coil Capacity Calculator (Cooling / Heating) (Field Guide)

- **WP ID:** 7211
- **Slug:** `ahu-coil-capacity-calculator-field-guide-2026-09-15`
- **URL:** https://blog.flowrust.com/2026/09/16/ahu-coil-capacity-calculator-field-guide-2026-09-15/
- **Tool ID:** `ahu-capacity-calculator`
- **Category:** Math & Numbers
- **date_gmt:** 2026-09-15T20:58:00
- **Outcome:** Clean 1-POST 0-PATCH
- **Audit:** 0 findings, 10/10 HEAD 200
- **Covered slugs:** 777


## 2026-09-16T01:00:00 — font-file-inspector (WP 7217)
- Title: Font File Inspector Field Guide: When Five Containers, Four Variable Axes, and One OpenType Feature Toggle Decide Whether Your Font Lands as a Brand Asset or a Mystery Box
- URL: https://blog.flowrust.com/2026/09/16/font-file-inspector-field-guide-when-five-containers-four-variable-axes-and-one-opentype-feature-toggle-decide-whether-your-font-lands-as-a-brand-asset-or-a-mystery-box-2026-09-16/
- Tool: font-file-inspector (Design)
- Cards: 3 (sfnt containers / fvar axes / GSUB features)
- Anchors: 4 (2 tool page + 1 /en/tools + 1 closing)
- Verdict: 1-POST 0-PATCH clean

## 2026-09-16T05:04:25 UTC — WP 7228 — AsciiMath / LaTeX / MathML Equation Converter

- Title: AsciiMath / LaTeX / MathML Equation Converter Field Guide: When Three Equation Dialects, Five Output Layers, and One Auto-Detect Pass Decide Whether Your Math Markup Ships as One Canonical String or Three Fragments
- URL: https://blog.flowrust.com/2026/09/16/asciimath-latex-mathml-equation-converter-field-guide-when-three-equation-dialects-five-output-layers-and-one-auto-detect-pass-decide-whether-your-math-markup-ships-as-one-canonical-string-or-three-fr/
- Tool: asciimath-latex-mathml-equation-converter (Format Conversion) — AsciiMath LaTeX MathML Equation Converter: auto-detect input format (AsciiMath / LaTeX / MathML), produce canonical LaTeX hub, presentation MathML with embedded TeX annotation in <semantics>, best-effort AsciiMath back-translation, role=math aria-label snippet for screen readers, server-side KaTeX HTML preview; conversion chain via asciimath2tex / temml / mathml-to-latex.
- date_gmt: 2026-09-16T05:04:25
- Mode: 1-POST + 1-PATCH (MERGED_NUMBERED_LIST false-positive on canonical md_to_html collapse of "1. ... 2. ... 3. ..." into single <p> — per WP 6185/6212 lesson)
- Assets: 1 poster (1080×800) + 3 cards (1600×900: 2×5-tile "Five Outputs From One Source String" + "Three Parsers, Three Detection Rules", 1×input-output-2col "A Worked Example: MathML -> LaTeX + aria-label")
- vision_analyze: caught U+2192 → tofu on cards 1 & 3 first-pass; replaced with ASCII -> (per WP 5699 family). All 4 PNGs clean final.
- elysia anchors: 4 total — 3× /en/tools/asciimath-latex-mathml-equation-converter + 1× /en/samples (kind-root) — all 200 OK, validate_anchors=True
- Source-side defenses: pre_encode_backslash + pre_encode_code_spans (4 backslash + 14 literal-HTML-in-code-span repairs) before md_to_html. Post-PATCH clean: 0 audit findings.

## 2026-09-16 09:15:54 UTC — Two Proportion Z Test Calculator (two-proportion-z-test-calculator)

- Post ID: 7235
- Slug: `two-proportion-z-test-calculator-field-guide-when-five-counts-three-numbers-and-one-pooled-se-decide-whether-your-a-b-test-2026-09-16`
- URL: https://blog.flowrust.com/2026/09/16/two-proportion-z-test-calculator-field-guide-when-five-counts-three-numbers-and-one-pooled-se-decide-whether-your-a-b-test-2026-09-16/
- date_gmt: 2026-09-16T09:15:13
- Tool: Two Proportion Z Test Calculator (Math & Numbers)
- Anchor links: 3 tool + 1 kind-root
- PATCH round-trips: 0
- Audit: clean (0 findings)
