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

## 2026-09-16 mtu-mss-path-calculator-field-guide-when-gre-vxlan-wireguard-and-the-20-byte-ipsec-header-decide-whether-your-tcp-mss-lands-at-1380-or-1330-2026-09-16
- WP post ID: 7247
- Link: https://blog.flowrust.com/2026/09/17/mtu-mss-path-calculator-field-guide-when-gre-vxlan-wireguard-and-the-20-byte-ipsec-header-decide-whether-your-tcp-mss-lands-at-1380-or-1330-2026-09-16/
- Tool: MTU / MSS Path Calculator (id=mtu-and-mss-path-calculator, category=Network)
- date_gmt: 2026-09-16T17:39:35
- 0 PATCH round-trips
- 4 assets uploaded (1 poster + 3 highlight cards)
- Elysia anchors: /en/tools/mtu-and-mss-path-calculator, /en/tools/ipv4-to-ipv6, /en/tools/wireguard-openvpn-to-clash-singbox-bridge, /en/tools
- PIL: render_poster + render_card_5tile + render_card_audit + render_card_4tile_compact (card 3 needed compact to avoid F_HUGE 150pt overlap on 4-digit numeric counts)
- Pre-POST checks: 0 audit findings; 0 phantom anchors; 11/11 pre-publish checks pass
- DOM verify (raw + content.rendered): 8 H2 body / 0 H1 / 0 H3 / 3 highlight-cards / 1 poster / 4 imgs with alt
- Public page check: HTTP 200, 8 body H2 + 1 nav H2 = 9 in DOM (per WP 6323); 4 figures; 6 imgs (4 article + 2 theme chrome per WP 6323)

## 2026-09-16 — OD600 Cell Density Calculator Field Guide (1-POST 0-PATCH clean)

- WP ID: 7254
- Tool: od600-cell-density (OD600 Cell Density Calculator (E. coli))
- Category: Education
- date_gmt: 2026-09-16T21:48:02
- URL: https://blog.flowrust.com/2026/09/17/od600-cell-density-field-guide-when-path-length-the-cells-per-od-default-and-the-linear-range-decide-whether-your-turbidity-reading-lands-as-a-cell-count-or-a-story-you-tell-yourself-2026-09-16/
- 8 body H2 + 1 nav H2 = 9 in DOM (rendered via context=edit shows 8 body H2)
- 4 assets uploaded (poster 1080x800, 3x cards 1600x900), all HEAD=200
- 4 elysia anchors all HEAD=200 (2x /tools/od600-cell-density + 2x /tools kind-root)
- audit_post_content: 0 findings
- PIL visual QA: all 4 assets clean (vision_analyze)


## 2026-09-17 01:50 UTC — WP 7261 — Contingency Table Chi-Square Fisher Exact Cramér V Tutor Field Guide

- **Tool**: Contingency Table Chi-Square Fisher Exact Cramér V Tutor ()
- **Category**: Data Analysis
- **Slug**: 
- **URL**: https://blog.flowrust.com/2026-09-17/contingency-table-chi-square-fisher-exact-cramer-v-tutor-field-guide-when-seven-decisions-2x2-fisher-cramer-v-and-cochran-rule/
- **date_gmt**: 2026-09-17T01:50:25
- **Word count**: 1427
- **Structure**: 0 H1, 8 H2, 0 H3, 1 article-poster, 3 highlight-cards
- **Elysia anchors**: 5 (3 unique tool + 2 sibling tool + 1 kind-root)
- **Audit findings**: 0 (after 1 PATCH for MERGED_NUMBERED_LIST + orphan </p> cleanup)
- **Patches**: 2 (split 7-item numbered list + remove orphan </p> after split)
- **Status**: ✅ 1-POST + 2-PATCH, audit clean, all 4 imgs + 5 anchors HTTP 200

## 2026-09-17 01:50 UTC — WP 7261 — Contingency Table Chi-Square Fisher Exact Cramér V Tutor Field Guide

- Tool: Contingency Table Chi-Square Fisher Exact Cramér V Tutor (id: contingency-table-chi-square-fisher-exact-cramer-v-tutor)
- Category: Data Analysis
- Slug: contingency-table-chi-square-fisher-exact-cramer-v-tutor-field-guide-when-seven-decisions-2x2-fisher-cramer-v-and-cochran-rule
- URL: https://blog.flowrust.com/2026/09/17/contingency-table-chi-square-fisher-exact-cramer-v-tutor-field-guide-when-seven-decisions-2x2-fisher-cramer-v-and-cochran-rule/
- date_gmt: 2026-09-17T01:50:25
- Word count: 1427
- Structure: 0 H1, 8 H2, 0 H3, 1 article-poster, 3 highlight-cards
- Elysia anchors: 5 (3 unique tool pages + 1 sibling + 1 kind-root)
- PIL: poster 1080x800 + 3 cards 1600x900, vision_analyze clean on all 4
- Patches: 2 (split 7-item numbered list + remove orphan closing p)
- Final audit_post_content findings: 0
- All 4 imgs HTTP 200, all 5 elysia anchors HTTP 200
- Status: clean publish

## 2026-09-17 06:09 UTC — secure-random-generator-field-guide-when-64-hex-chars-beat-a-24-char-password (WP 7270)

- **Tool**: Secure Random Generator (Security / CSPRNG / Key Generation)
- **Slug**: `secure-random-generator-field-guide-when-64-hex-chars-beat-a-24-char-password`
- **Link**: https://blog.flowrust.com/2026/09/17/secure-random-generator-field-guide-when-64-hex-chars-beat-a-24-char-password/
- **date_gmt**: 2026-09-17T06:09:27
- **Status**: publish (1-POST + 2-PATCH clean)
- **Article structure**: 0 body H1 + 8 body H2 + 1 article-poster figure + 3 highlight-card figures + 4 images
- **Patches applied**:
  1. Convert 5 `<h3>` to `<strong>` (WP 6212 lesson — body must have 0 H3s)
  2. Add meaningful alts to 3 highlight-card figures (audit IMG_MISSING_ALT)
- **Anchors** (9 total, 0 phantom):
  - 7× `https://elysiatools.com/en/tools/secure-random-generator` (in tool-manifest)
  - 1× `https://elysiatools.com/en/samples/jwt-samples` (in sample-manifest)
  - 1× `https://elysiatools.com/en/samples/cryptography` (in sample-manifest)
  - 1× `https://elysiatools.com/en/tools` (kind-root whitelist, Cycle #40)
- **Cards**: 
  - card1: `render_card_5tile` — 5 Decisions (entropy, CSPRNG, encoding, alphabet, audit)
  - card2: `render_card_input_output_2col` — JWT HS256 step-by-step
  - card3: `render_card_5tile` — 5 production bugs (seed-time, modulo, off-by-one, in-logs, reused)
- **Visual QA**: All 4 PNGs verified via vision_analyze — no tofu, no clipping, no overflow
- **Audit**: 0 findings post-PATCH (canonical `audit_post_content`)


## 2026-09-17 10:18 UTC — WP 7281 — Enteral Nutrition Target Calculator Field Guide

- **Tool:** `enteral-nutrition-target` (Health, picker v4 score=1632)
- **Title:** Enteral Nutrition Target Calculator Field Guide: When kcal/kg/day, g/kg/day, and a 1.5 kcal/mL Formula Decide Whether Your Pump Rate Lands at 54 mL/hr or 41 mL/hr
- **URL:** https://blog.flowrust.com/2026/09/17/enteral-nutrition-target-calculator-field-guide-when-kcal-per-kg-and-protein-g-per-kg-decide-whether-your-pump-rate-lands-at-54-or-41-ml-per-hr/
- **date_gmt:** 2026-09-17T10:18:30
- **Assets:** poster (1080×800) + 3 cards (1600×900) — vision-analyzed clean
- **Anchors (6, all 200):** 5× /en/tools/enteral-nutrition-target + 1× /en/tools (kind-root)
- **Audit:** 0 findings (canonical `audit_post_content`)
- **Status:** 1-POST 0-PATCH clean. Browser DOM probe unavailable in cron (Chromium install 404); used WP 6663 fallback: regex audit + urllib HEAD on 4 images + 6 anchors + permalink, all 200.
