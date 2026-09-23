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

## 2026-09-17T14:24:41 — combinatorial-generation-field-guide-when-multinomial-divisor-generating-function-and-empty-set-corner-case-decide-whether-your-multiset-count-lands-at-12-or-24-2026-09-17 (WP 7286)
- Title: Permutation / Combination / Subset Generator Field Guide: When Multinomial Divisor, Generating-Function Coefficient, and the Empty-Set Corner Case Decide Whether Your Multiset Count Lands at 12 or 24
- URL: https://blog.flowrust.com/2026/09/17/combinatorial-generation-field-guide-when-multinomial-divisor-generating-function-and-empty-set-corner-case-decide-whether-your-multiset-count-lands-at-12-or-24-2026-09-17/
- Tool: combinatorial-generation (Math & Numbers)
- 1-POST 0-PATCH clean
- featured_media=0, 8 body H2, 3 highlight-cards, 1 poster, 0 audit findings

## 2026-09-17T18:31:43 — title-case-converter-field-guide-when-function-word-handling-across-ap-chicago-wikipedia-and-simple-styles-decide-whether-your-headline-looks-editorially-clean-or-eyeball-wrong-2026-09-17 (WP 7291)
- Title: Title Case Converter Field Guide: When Function-Word Handling Across AP, Chicago, Wikipedia, and Simple Styles Decide Whether Your Headline Looks Editorially Clean or Eyeball-Wrong
- URL: https://blog.flowrust.com/2026/09/18/title-case-converter-field-guide-when-function-word-handling-across-ap-chicago-wikipedia-and-simple-styles-decide-whether-your-headline-looks-editorially-clean-or-eyeball-wrong-2026-09-17/
- Tool: title-case-converter (Text Processing)
- 1-POST 1-PATCH clean (MERGED_NUMBERED_LIST from `1. <strong>...` markdown list, source-converted to <ul><li>; also fixed `- **AP**...` and `- Always capitalize...` markdown bullets which would have triggered MERGED_BULLET_LIST in the second run)
- featured_media=0, 8 body H2, 3 highlight-cards, 1 poster, 0 audit findings (final)
- Anchors (4, all 200): 3× /en/tools/title-case-converter + 1× /en/tools (kind-root)
- 2026-09-17 22:43 UTC — WP 7297 [TPN Osmolality Estimator](https://blog.flowrust.com/2026/09/18/tpn-osmolality-estimator-field-guide-when-peripheral-veins-tolerate-a-1500-ml-admixture-and-when-they-dont-2026-09-17/) — 1-POST 0-PATCH clean
- featured_media=0, 8 body H2, 3 highlight-cards, 1 poster, 0 audit findings
- Anchors (3, all 200): 2× /en/tools/tpn-osmolality-estimator + 1× /en/tools (kind-root)
- Tool picker returned TPN Osmolality (Health, theme_score=1555) — sum-of-solute formula + peripheral-vs-central access decision
- Skills fallback: umbrella PIL templates used (article-poster-creator + article-highlight-cards not on disk; article-writer present but slower scoring pipeline skipped per cron cadence)
- Visual QA: all 4 PNGs passed vision_analyze (no overflow, no tofu, takeaway visible)

## 2026-09-18T02:54:40 — carrying-capacity-estimator-field-guide-when-linearization-grid-scan-and-the-60-percent-plateau-rule-decide-whether-your-k-hat-lands-at-664-or-1000 (WP 7303)
- Title: Carrying Capacity Estimator Field Guide: When Linearization, Grid Scan, and the 60-Percent Plateau Rule Decide Whether Your K-hat Lands at 664 or 1000
- URL: https://blog.flowrust.com/2026/09/18/carrying-capacity-estimator-field-guide-when-linearization-grid-scan-and-the-60-percent-plateau-rule-decide-whether-your-k-hat-lands-at-664-or-1000/
## 2026-09-18T06:56:57 — cam-follower-displacement-field-guide-when-constant-velocity-cycloidal-and-the-pressure-angle-30-degree-rule-decide-whether-your-follower-reaches-50-mm-in-50-ms-or-slams-the-spring-2026-09-18 (WP 7308)
- Title: Cam Follower Displacement Field Guide: When Constant Velocity, Cycloidal, and the 30-Degree Pressure-Angle Rule Decide Whether Your Follower Reaches 50 mm in 50 ms or Slams the Spring
- URL: https://blog.flowrust.com/2026/09/18/cam-follower-displacement-field-guide-when-constant-velocity-cycloidal-and-the-pressure-angle-30-degree-rule-decide-whether-your-follower-reaches-50-mm-in-50-ms-or-slams-the-spring-2026-09-18/
- Tool: cam-follower-displacement (Math & Numbers, picker theme_score=55 — 4 motion laws: constant velocity, constant acceleration, harmonic, cycloidal)
- 1-POST 0-PATCH clean
- featured_media=0, 8 body H2, 3 highlight-cards, 1 poster, 0 audit findings (false-positive on `POSSIBLE_BACKSLASH_STRIPPED` from math formulas `(s + r_r + ...)` and `(ds/dθ − e)` — algebraic group expressions, not stripped regex char-classes)
- Anchors (4, all 200): 4× /en/tools/cam-follower-displacement (in tool-manifest)
- Cards: 
  - card1: render_card_5tile — 4 motion laws + "Pick by" rule (Cv < 2.0, Ca finite)
  - card2: render_card_input_output_2col — Geometry inputs (r_b, h, r_r, rise, law) → computed outputs (h/r_b, Cs, φ_max, ρ_min, verdict)
  - card3: render_card_4tile_compact — 3 pressure-angle traps (small base circle, large roller, short rise) + combined
- Visual QA: all 4 PNGs passed vision_analyze (no tofu, no clipping, no overflow, takeaway visible)
- Audit: false-positive on `POSSIBLE_BACKSLASH_STRIPPED` from math formulas with `(s + ...)` pattern (s ∈ [wdsWDS] per detector). False positive because the spans are correct mathematical grouping, not stripped regex. No PATCH applied.

## WP 7313 — Hall Effect Calculator Field Guide (2026-09-18 11:03 UTC)
- Tool: hall-effect-calculator (Science & Education, picker theme_score=2 — Hall voltage V_H = I·B/(n·q·t), carrier-type polarity rule, semiconductor-vs-metal gap)
- 1-POST 0-PATCH clean
- featured_media=0, 8 body H2, 3 highlight-cards, 1 poster, 0 audit findings
- Anchors (3, all 200): 2× /en/tools/hall-effect-calculator (in tool-manifest) + 1× /en/tools (kind-root, Cycle #40 allowlist)
- Cards:
  - card1: render_card_5tile — 5 inputs (I, B, n, t, q carrier) for V_H = I·B/(n·q·t)
  - card2: render_card_5tile — 5 sensitivity rules (bias, geometry, material, sign, noise)
  - card3: render_card_5tile — 5 practical rules when picking a Hall element
- Visual QA: all 4 PNGs passed vision_analyze (no tofu, no clipping, no overflow, takeaway visible)
- Article: ~1080 words, close-first lead on 0.31 V vs 7 µV gap; 8 H2s cover formula, inputs, sign, metals-fail-semiconductors-work, sensitivity, units, temperature drift, rules
- Assets archived to ~/www/blog/2026-09-18-hall-effect-calculator/

## 2026-09-18 15:40 UTC — JSON Diff Visualizer (WP 7319)

- Tool: **JSON Diff Visualizer** (category: Development) — first tool in this slot for this run
- Title: "JSON Diff Visualizer Field Guide: When Sort-Keys, Path Tags, and the Left/Right Labels Decide Whether Your Diff Reads Clean or Fills With Noise"
- Slug: `json-diff-visualizer-field-guide-when-sort-keys-path-tags-and-the-left-right-labels-decide-whether-your-diff-reads-clean-or-fills-with-noise`
- Date GMT: 2026-09-18T15:40:26
- Status: publish
- WP ID: 7319
- Link: https://blog.flowrust.com/2026/09/18/json-diff-visualizer-field-guide-when-sort-keys-path-tags-and-the-left-right-labels-decide-whether-your-diff-reads-clean-or-fills-with-noise/

**Asset stack (per WP 6206/6352 disk probe):** article-writer umbrella present; article-poster-creator + article-highlight-cards missing on top-level — fell back to `article-writer/article-highlight-cards/scripts/render_editorial_dense_cron.py` for cards and built a custom left-rail poster HTML rendered via Playwright + Chrome.

**Structure:**
- 1 article-poster figure (deep-navy + cyan accent, left-rail 1280×900)
- 3 highlight-card figures inserted at H2 #2 (sort-keys), H2 #5 (5 path tags), H2 #6 (migration workflow)
- 0 body H1, 8 body H2, 0 H3, 19 `<p>` blocks
- Article length ~1700 words

**Card themes:**
- card1: ocean (sort-keys toggle)
- card2: ember (5 path classifications)
- card3: violet (migration workflow)

**Visual QA (mandatory per WP 5663):** vision_analyze on all 4 PNGs. Poster: title fits 4 lines, divider + subtitle clean, accent colors working. Cards: 3-column grid, bullets fit, no overflow, no tofu.

**Audit (canonical WP 6122/6323/6417 checks):**
- All 14 audit checks PASS
- All 4 image URLs return HTTP 200 (HEAD probe)
- All 10 elysia anchors point at real `json-diff-visualizer` tool ID (validated against tool-manifest)
- First H2 does NOT duplicate title (WP 6417 trap avoided)
- `featured_media: 0` set (WP 5628 hero duplication avoided)
- 0 backslash, 0 name placeholders, 0 `<br>` in `<p>`, 0 markdown link leaks, 0 placeholder leaks

**No PATCH round-trip needed.**

Assets archived to ~/www/blog/2026-09-18-json-diff-visualizer/ (poster.png, card1-3.png, article.md, article_final.html).

## 2026-09-19 — MPV Analyzer Field Guide (WP 7330)
- Tool: Mean Platelet Volume (MPV) Analyzer (`mean-platelet-volume-analyzer`)
- URL: https://blog.flowrust.com/2026/09/19/mean-platelet-volume-mpv-analyzer-reading-the-four-quadrant-grid-on-every-cbc/
- date_gmt: 2026-09-19T00:07:33
- Audit: 0 findings (after 1-PATCH)
- PATCHes: 1 (MERGED_BULLET_LIST x4 + MERGED_NUMBERED_LIST -> <ul><li>)
- Assets: PIL poster (1280x900) + 3 cards (1600x900) via umbrella templates

## 2026-09-19 — TPN Macronutrient Calculator Field Guide (WP 7336)
- Tool: TPN Macronutrient Calculator (Glucose/AA/Lipid) (`tpn-macronutrient-calculator`)
- URL: https://blog.flowrust.com/2026/09/19/tpn-macronutrient-calculator-2026-09-19/
- date_gmt: 2026-09-19T04:13:40
- Audit: 0 findings (1-POST 0-PATCH clean)
- PATCHes: 0
- Assets: PIL poster (1280x900) + 3 cards (1600x900) via umbrella templates
  - poster: deep-navy + cyan-teal, eyebrow "CLINICAL NUTRITION SUPPORT · PARENTERAL FEEDING", title "Reading a TPN Order / in Five Numbers", shortened subtitle after first vision_analyze flagged left/right edge clip
  - card1 (5-tile): Five formulas (dextrose, AA, lipid, nitrogen, NP kcal:N)
  - card2 (4-tile compact): Four per-kg ceilings (energy, protein, GIR, lipid)
  - card3 (input/output 2-col): 70-kg post-op worked example
- All 4 PNGs vision_analyze-checked clean (no tofu, no overflow)
- 8 body H2, 0 H3, 1 article-poster figure, 3 highlight-card figures
- 6 elysiatools anchors: 5 tool-page + 1 kind-root (all 200, all validated against tool-manifest)
- Source: `pre_encode_code_spans` + `safe_md_to_html` (3 backtick spans had `*` from multiplication formulas; multi-line blocks rewritten to single-line inlined to avoid WP 6376 nested-code+br pitfall)
- All 7 URLs HEAD 200: poster, card1, card2, card3, tool anchor, kind-root anchor, permalink
- No browser DOM probe (Chrome daemon unavailable); used raw rendered-content probe + urllib HEAD per WP 6663 fallback

## 2026-09-19 ~08:23 UTC — Messy Text to Structured Data Workbench (WP 7341)

- date_gmt: 2026-09-19T08:23:21
- post id: 7341
- title: "From Clipboard to Typed Rows: A Field Guide to the Messy Text to Structured Data Workbench"
- slug: `messy-text-to-structured-data-workbench-field-guide-when-paste-detect-coerce-and-export-need-to-agree-on-the-first-row-2026-09-19`
- link: https://blog.flowrust.com/2026/09/19/messy-text-to-structured-data-workbench-field-guide-when-paste-detect-coerce-and-export-need-to-agree-on-the-first-row-2026-09-19/
- tool id: `messy-text-to-structured-data-workbench` (Text Processing cluster)
- picker: custom v4 with extended 100-post horizon — sparse_category_picker returned ocr-pdf-to-structured-json-bridge but that was WP 7086 (2026-09-12); extended horizon found messy-text as the next fresh theme-rich candidate
- 8 body H2, 0 H1, 0 H3, 1 article-poster, 3 highlight-card, 6 elysiatools anchors (5 tool + 1 kind-root)
- source: plain `md_to_html` (triple-fence present → safe_md_to_html would corrupt per WP 5828); pre_encode_code_spans pre-encoded literal `<table>` and `<td data-x="42">` to defuse WP 5828/6109 wpautop strip
- assets: poster (1080×800, deep-navy + cyan-teal), card1 (5-tile 3+2 cheatsheet), card2 (audit-style 2-col with 5-row failure modes + verdict), card3 (4-tile compact)
- vision_analyze caught 2 pre-POST defects: (1) poster eyebrow had literal `&middot;` → switched to Unicode `\u00b7`; (2) card3 with `render_card_4tile` had auto/tab/auto/true overlap body → switched to `render_card_4tile_compact`
- all 11 URLs HEAD 200 (4 images + 6 anchors + 1 permalink); 0 audit findings; 0 placeholder leaks; 0 nested p in h2; 0 wpai-auto-tags-link
- asset archive: ~/www/blog/2026-09-19-messy-text-to-structured-data-workbench-field-guide-when-paste-detect-coerce-and-export-need-to-agree-on-the-first-row-2026-09-19/


## 2026-09-19 — WP 7351 — Z85 RFC 1924 Base85 Stream Encoder Decoder Field Guide
- Tool: `z85-rfc1924-base85-stream-codec` (Format Conversion)
- Slug: `z85-rfc1924-base85-stream-codec-field-guide-when-three-alphabets-hide-behind-base85-and-the-25-percent-density-win-comes-with-a-wrong-alphabet-tax`
- URL: https://blog.flowrust.com/2026/09/20/z85-rfc1924-base85-stream-codec-field-guide-when-three-alphabets-hide-behind-base85-and-the-25-percent-density-win-comes-with-a-wrong-alphabet-tax/
- date_gmt: 2026-09-19T16:33:05
- Words: ~1417 | H2: 8 | Cards: 3 | Poster: 1
- Audit: 0 findings, 4/4 imgs HTTP 200, 2/2 elysia anchors HTTP 200, permalink HTTP 200
- 1-POST 0-PATCH clean run

## 2026-09-19T20:39:00 — AI Domain Name Idea Generator (WP 7356)
- slug: `ai-domain-name-idea-generator-field-guide-when-seven-inputs-one-rdap-check-and-one-naming-style-choice-decide-whether-your-brand-lands-a-free-com-or-a-30-round-refund-2026-09-19`
- url: https://blog.flowrust.com/2026/09/20/ai-domain-name-idea-generator-field-guide-when-seven-inputs-one-rdap-check-and-one-naming-style-choice-decide-whether-your-brand-lands-a-free-com-or-a-30-round-refund-2026-09-19/
- category: AI Tools
- patches: 0 (clean 1-POST)
- elysia anchors: 4
- assets: poster-48.png, card1-47.png, card2-48.png, card3-45.png

## 2026-09-20T04:48:06 — Crystal Structure Explorer (WP 7366)
- Tool: `crystal-structure-explorer` (Chemistry / Education cluster: solid-state chemistry, crystallography, Three.js 3D)
- Slug: `crystal-structure-explorer-field-guide-when-rotating-na-cl-diamond-cs-cl-and-fluorite-finally-makes-coordination-numbers-click`
- URL: https://blog.flowrust.com/2026/09/20/crystal-structure-explorer-field-guide-when-rotating-na-cl-diamond-cs-cl-and-fluorite-finally-makes-coordination-numbers-click/
- date_gmt: 2026-09-20T04:48:06
- Words: ~1480 | H2: 8 | Cards: 3 | Poster: 1
- Patches: 1 (MERGED_BULLET_LIST → <ul><li> for "What the Library Covers" 6-item structure family list)
- Audit: 0 findings after PATCH, 4/4 imgs HTTP 200, 5/5 elysia anchors HTTP 200, permalink HTTP 200
- Elysia anchors: 5 (4 tool + 1 kind-root)
- Assets: poster.png (1080×800, NETWORK theme), card1.png (5-tile "Six Families in One Library"), card2.png (audit-style 2-col "Five Checks Before You Trust a Structure" with verdict), card3.png (4-tile compact 1×4 "Four Comparisons a Diagram Cannot Show")
- visual QA caught: (1) card3 first-pass had "C allotrope"/"AX2 / MX2" overflowed tile width — reduced to "C"/"MX2"; (2) card2 first-pass had row5 body text clipped at bottom — increased col_h 600→640 + row_h 100→105
- Skills path: umbrella fallback (article-poster-creator + article-highlight-cards missing from disk; used templates/pil_poster_and_cards_network_theme.py + custom PIL render)
- Asset archive: ~/www/blog/2026-09-20-crystal-structure-explorer-field-guide-when-rotating-na-cl-diamond-cs-cl-and-fluorite-finally-makes-coordination-numbers-click/

## 2026-09-20T09:09:51 | WP 7373 | recipe-ingredient-scaler-field-guide-when-parsing-density-table-and-smart-seasoning-beat-the-generic-multiplier | recipe-ingredient-scaler | 1-POST 0-PATCH clean | 4 imgs (poster + 3 cards) | 3 elysia anchors | 0 audit findings

## 2026-09-20T13:14:31 — LDL-C Calculator (Friedewald) (WP 7378)
- Tool: `ldl-calculator-friedewald` (Health cluster: clinical lipid panel, ACC/AHA 2018 cholesterol guideline, Friedewald/Martin-Hopkins/Sampson-NIH equations)
- Slug: `ldl-calculator-friedewald-field-guide-when-three-inputs-and-a-5-to-1-tg-vldl-ratio-drive-fifty-years-of-quietly-underestimated-ldl-c`
- URL: https://blog.flowrust.com/2026/09/20/ldl-calculator-friedewald-field-guide-when-three-inputs-and-a-5-to-1-tg-vldl-ratio-drive-fifty-years-of-quietly-underestimated-ldl-c/
- date_gmt: 2026-09-20T13:14:31
- Words: ~1421 | H2: 8 | Cards: 3 | Poster: 1 | Audit: 0 findings
- Patches: 1 (MERGED_NUMBERED_LIST on 2 blocks: "Five Edge Cases" 1.-5. joined into 1 <p> → <ol>; "Panel A/B/C" dash list joined into 1 <p> → <ul><li>; round-1 fix was messy — section 5 lost Panel C; round-2 fix regenerated cleanly with all 3 panels)
- Audit final: 0 findings, 8 body H2, 0 H3, 0 H1, 1 poster, 3 highlight-cards, 1 body <ol> (5 items), 1 body <ul> (3 items), featured_media=0
- Elysia anchors: 3 (3× tool URL + 1× kind-root `/en/tools`); all 2 unique URLs HTTP 200
- Assets: 4/4 imgs HTTP 200 (poster-50.png, card1-49.png, card2-50.png, card3-47.png); visual QA pre-POST confirmed clean (no tofu, no overflow, all glyphs rendered)
- Card designs: card1 = `render_card_5tile` "Five Edge Cases" 5-tile, card2 = `render_card_5tile` "Five Threshold Bands" 5-tile, card3 = `render_card_4tile_compact` "Four LDL-C Formulas" 4-tile
- Skills path: umbrella fallback (article-poster-creator + article-highlight-cards missing from disk; used templates/pil_poster_and_cards_network_theme.py + render_card_4tile_compact.py)
- Notable: confirmed WP 6436 5-tile arity OK (5 items each); confirmed WP 6358 card3 4-tile body fits within tile_w-60 (each body ≤ 40 chars at F_MONO on tile_w=660)
- Asset archive: ~/www/blog/2026-09-20-ldl-calculator-friedewald/

## 2026-09-20T17:21:43 — fractional-flow-reserve-field-guide-when-pd-over-pa-and-adenosine-140-turn-a-60-percent-stenosis-into-a-defer-or-stent-call-2026-09-20 (WP 7387)
- Title: Fractional Flow Reserve Calculator (FFR) Field Guide: When Pd / Pa and Adenosine 140 Turn a 60% Stenosis Into a Defer-or-Stent Call
- URL: https://blog.flowrust.com/2026/09/21/fractional-flow-reserve-field-guide-when-pd-over-pa-and-adenosine-140-turn-a-60-percent-stenosis-into-a-defer-or-stent-call-2026-09-20/

## 2026-09-20T21:51:04Z — dockerfile-linter (WP 7395)
- Title: Five Dockerfile Lines That Inflate Your Image by 800 MB
- URL: https://blog.flowrust.com/2026/09/21/dockerfile-linter/
- Tool: dockerfile-linter (Dockerfile Linter & Best-Practices Checker)
- Category: Development
- Cards: 3 (5-tile buckets, 2-col before/after, 5-tile 3+2 cheatsheet)
- Audit: 0 findings
- Asset URLs:
  - poster: https://blog.flowrust.com/wp-content/uploads/2026/09/jarvis-poster-dockerfile-linter.png
  - card1:  https://blog.flowrust.com/wp-content/uploads/2026/09/jarvis-card1-dockerfile-linter.png
  - card2:  https://blog.flowrust.com/wp-content/uploads/2026/09/jarvis-card2-dockerfile-linter.png
  - card3:  https://blog.flowrust.com/wp-content/uploads/2026/09/jarvis-card3-dockerfile-linter.png
- Elysia anchors: 6 instances of /en/tools/dockerfile-linter (validated REAL), 1 /en/tools (kind-root)
- Pre-publish checks: 0 H1, 8 H2, 0 H3, 1 poster fig, 3 card figs, 4 imgs, 0 audit findings
## 2026-09-21T01:24Z — 5h audit cycle (5/5 in-scope, 1 PATCH)
- Scope: latest 5 posts (WP 7395, 7387, 7378, 7373, 7366), all English elysia field guides
- Head probe: 20/20 imgs, 11/11 elysia anchors, 5/5 permalinks all HTTP 200
- OoS: 0 (5/5 in-scope)
- Findings: 1 post (WP 7395 Dockerfile Linter) had 4× `ORPHANED_CODE` audit findings — 4 dangling outer `<code>` opens followed by `<code class="language-X">...</code>` blocks (wpautop-stripped triple-fence code blocks; intended `<pre><code>` but lost the `<pre>` wrapper)
- Fix: collapsed each `<code><code class="language-X">...</code>` to `<pre><code class="language-X">...</code></pre>`, replacing inner `<br>` with `\n` for proper pre formatting. 0 nested `<code><code>` remaining; 4 proper `<pre><code class="language-X">` blocks; audit returns 0 findings
- 1-POST 1-PATCH (POST /wp/v2/posts/7395) — verified clean via ?context=edit re-fetch
- Other 4 posts: 0 audit findings, no PATCH needed
- Asset archive: ~/www/blog/2026-09-21-dockerfile-linter-fix/
- Pitfall family: extends WP 6376 (`safe_md_to_html` nested `<code><code>` artifacts) — but WP 7395's variant had NO `<br />` inside the inner code and the outer `<code>` was unclosed (dangling). New WP 7395 case: triple-fence source markdown produced dangling `<code>` open when wpautop processed `<pre><code>...` and stripped the outer wrapper. Defense recipe: detect `<code><code class="language-X">...</code>` (one close only) and rebuild as `<pre><code class="language-X">...</code></pre>` with `<br>` → `\n`.## 2026-09-21 — WP 7401 — Bitcoin Address Validator Field Guide

- **Tool**: `btc-address-validator` (Bitcoin Address Validator) — Finance category
- **date_gmt**: 2026-09-21T01:56:06
- **URL**: https://blog.flowrust.com/2026/09/21/btc-address-validator-field-guide-when-prefix-base58-alphabet-version-byte-bech32-checksum-and-network-cross-check-decide-whether-your-address-renders-as-p2pkh-p2sh-or-segwit-2026-09-21/
- **Featured media**: 0 (per umbrella §9 critical)
- **H1/H2/H3**: 0 / 8 / 0
- **Cards**: 3 (poster + 5-tile + 4-tile compact + 2-col worked example)
- **Elysia anchors**: 3 (2× tools/btc-address-validator + 1× kind_root /en/tools)
- **Audit findings**: 0
- **Patches**: 0
- **Stack**: umbrella fallback (`article-poster-creator` and `article-highlight-cards` skills not on disk; used umbrella PIL templates per WP 6185/6352 fallback path)
## 2026-09-21 — Optical Path Difference Calculator (WP 7406)

- **Title**: Optical Path Difference Field Guide: When 275 nm of Air Becomes a Dark Fringe
- **Slug**: `optical-path-difference-field-guide-when-275-nm-of-air-becomes-a-dark-fringe-2026-09-21`
- **URL**: https://blog.flowrust.com/2026/09/21/optical-path-difference-field-guide-when-275-nm-of-air-becomes-a-dark-fringe-2026-09-21/
- **Tool**: `optical-path-difference` (Optical Path Difference Calculator)
- **Category**: Science & Education
- **date_gmt**: 2026-09-21T06:00:28
- **1-POST + 1-PATCH** — PATCH split 4 MERGED_BULLET_LIST paragraphs (md_to_html does not process `- ` markdown bullets per WP 6185/6212). Pre-POST visual QA via vision_analyze passed all 4 PIL assets. Audit clean (0 findings). All 4 images + 3 elysia anchors return HTTP 200.


## 2026-09-21 -- WP 7414 -- nemenyi-critical-difference-friedman-rank-plotter

- date_gmt: 2026-09-21T10:07:16
- tool: Nemenyi Critical-Difference & Friedman Rank Plotter (Data Analysis)
- status: publish (1-POST 0-PATCH)
- audit findings: 0
- 8 body H2, 3 highlight-card figures, 1 poster figure
- 6 unique elysia anchors, all 200
- 1866 words
- artifacts: ~/www/blog/2026-09-21-nemenyi-critical-difference-friedman-rank-plotter/


## 2026-09-21T18:27:35 — BGP AS Path Loop Policy Sandbox (WP 7425)
- Tool: `bgp-as-path-loop-policy-sandbox` (Networking / Route Policy sandbox)
- Slug: `bgp-as-path-loop-policy-sandbox-field-guide-when-five-route-entries-three-policy-rules-and-the-loop-check-decide-your-bgp-best-path-offline-2026-09-21`
- URL: https://blog.flowrust.com/2026/09/22/bgp-as-path-loop-policy-sandbox-field-guide-when-five-route-entries-three-policy-rules-and-the-loop-check-decide-your-bgp-best-path-offline-2026-09-21/
- date_gmt: 2026-09-21T18:27:35
- Words: ~1380 | H2: 8 | Cards: 3 | Poster: 1
- Patches: 0 (clean 1-POST)
- Audit: 0 findings, 4/4 imgs HTTP 200, 3/3 elysia anchors HTTP 200, permalink HTTP 200
- Elysia anchors: 3 (2x tools/bgp-as-path-loop-policy-sandbox + 1x kind_root /en/tools)
- Assets: poster-7421, card1-7422, card2-7423, card3-7424
- Card designs: card1 = render_card_5tile (5 fields on every route entry), card2 = render_card_input_output_2col (loop check walk), card3 = render_card_5tile_3plus2 (5 knobs / setLocalPref)
- Visual QA: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap)
- Skills path: umbrella fallback (article-poster-creator + article-highlight-cards skill paths under ~/.hermes/skills/article-writer/ present but cron prompt listed as missing; used umbrella PIL templates per WP 6185/6352 fallback path)
- Asset archive: ~/www/blog/2026-09-21-bgp-as-path-loop-policy-sandbox/


## 2026-09-22T02:58:30 — Contingency Table Chi-Square Fisher Exact Cramér V Tutor (WP 7439)

- Tool: `contingency-table-chi-square-fisher-exact-cramer-v-tutor` (Data Analysis)
- Slug: `contingency-table-chi-square-fisher-exact-cramer-v-tutor-field-guide-when-four-statistics-eight-decisions-and-one-caption-rule-combine-decide-whether-your-2x2-holds-2026-09-22`
- URL: https://blog.flowrust.com/2026/09/22/contingency-table-chi-square-fisher-exact-cramer-v-tutor-field-guide-when-four-statistics-eight-decisions-and-one-caption-rule-combine-decide-whether-your-2x2-holds-2026-09-22/
- date_gmt: 2026-09-22T02:56:51
- Words: ~1430 | H2: 8 | Cards: 3 | Poster: 1
- Patches: 0 (clean 1-POST)
- Audit: 0 findings, 4/4 imgs HTTP 200, 3/3 elysia anchors HTTP 200, permalink HTTP 200
- Elysia anchors: 3 (2x tools/contingency-table-chi-square-fisher-exact-cramer-v-tutor + 1x kind_root /en/tools)
- Assets: poster-55, card1-54, card2-55, card3-52 (auto-renamed by WP upload dedup)
- Card designs: card1 = render_card_5tile (4 statistics side-by-side), card2 = render_card_input_output_2col (5-row test picker), card3 = render_card_5tile_3plus2 (5 effect-size/rule items)
- Visual QA: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap)
- Skills path: umbrella fallback (article-poster-creator + article-highlight-cards skill paths under ~/.hermes/skills/ missing on disk; used umbrella PIL templates per WP 6185/6352)
- Asset archive: /Users/quyue/www/blog/2026-09-22-contingency-table-chi-square-fisher-exact-cramer-v-tutor

## 2026-09-22T07:12:57 — tailwind-class-to-css-converter-field-guide-when-five-utility-decisions-one-alpha-syntax-and-three-compound-shadow-rules-combine-decide-whether-your-copied-css-matches-the-original-2026-09-22 (WP 7445)
- Title: Tailwind Class to CSS Converter Field Guide: When Five Utility Decisions, One Alpha Syntax, and Three Compound Shadow Rules Combine, Decide Whether Your Copied CSS Matches the Original
- URL: https://blog.flowrust.com/2026/09/22/tailwind-class-to-css-converter-field-guide-when-five-utility-decisions-one-alpha-syntax-and-three-compound-shadow-rules-combine-decide-whether-your-copied-css-matches-the-original-2026-09-22/

## 2026-09-22T11:17:20 — MTU / MSS Path Calculator (WP 7451)
- Tool: `mtu-and-mss-path-calculator` (Network)
- Title: MTU / MSS Path Calculator Field Guide: When Eight Encapsulation Layers, the 40-Byte MSS Rule, and the Don't-Fragment Ping Probe Decide Whether Your SD-WAN Packet Clears 1500 Bytes or Black-Holes at 1404
- URL: https://blog.flowrust.com/2026/09/22/mtu-and-mss-path-calculator-field-guide-when-eight-encapsulation-layers-the-40-byte-mss-rule-and-the-dont-fragment-ping-probe-decide-whether-your-sd-wan-packet-clears-1500-bytes-or-black-holes-at-1404/
- date_gmt: 2026-09-22T11:17:20
- Words: ~1500 | H2: 8 | Cards: 3 | Poster: 1
- Patches: 0 (clean 1-POST)
- Audit: 0 findings, 4/4 imgs HTTP 200, 6/6 elysia anchors HTTP 200, permalink HTTP 200
- Elysia anchors: 6 (3x tools/mtu-and-mss-path-calculator + 1x tools/http-3-quic-handshake-anatomy + 1x tools/cidr-calculator + 1x kind_root /en/tools)
- Assets: poster-56, card1-55, card2-56, card3-53
- Card designs: card1 = render_card_5tile (5 numeric outputs), card2 = render_card_4tile_compact (4 encapsulation footguns), card3 = render_card_input_output_2col (worked example VXLAN+WG+VLAN)
- Visual QA: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap)
- Skills path: parent skills present under ~/.hermes/skills/article-writer/{article-poster-creator, article-highlight-cards}; umbrella PIL templates used (matches cron cadence output per WP 6185/6352)
- Asset archive: /Users/quyue/www/blog/2026-09-22-mtu-and-mss-path-calculator
## 2026-09-22 23:32 UTC — Serum Anion Gap (AG) Calculator — Field Guide

- Post ID: 7457
- URL: https://blog.flowrust.com/2026/09/22/serum-anion-gap-calculator-field-guide-when-sodium-chloride-bicarbonate-and-the-gold-mark-mnemonic-decide-whether-your-metabolic-acidosis-is-hagma-or-nagma/
- date_gmt: 2026-09-22T15:29:52
- Tool: anion-gap-calculator (Health)
- Words: 1240 | H2: 8 | Cards: 3 | Poster: 1
- Patches: 1 (MERGED_BULLET_LIST on the 3-zone reference ranges section: converted merged `<p>` to `<ul><li>`)
- Audit: 0 findings after PATCH, 4/4 imgs HTTP 200, 3/3 elysia anchors HTTP 200, permalink HTTP 200
- Elysia anchors: 3 (2x tools/anion-gap-calculator + 1x kind_root /en/tools)
- Assets: poster-57, card1-56, card2-57, card3-54
- Card designs: card1 = render_card_5tile (five AG zones), card2 = render_card_5tile (GOLD-MARK top 5), card3 = render_card_input_output_2col (worked example HAGMA hidden by hypoalbuminemia)
- Visual QA: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap, no clipping)
- Skills path: parent skill article-writer present; article-poster-creator + article-highlight-cards NOT on disk — umbrella PIL templates used (per WP 6185/6352 cron cadence)
- Picker: pick_tool_v4_content_based diverse top pick (Health category, anion-gap-calculator; 1396-candidate pool after dedup against 812 covered_slugs)
- Source-side defenses: pre_encode_code_spans (no literal-HTML code spans), plain md_to_html (no `*` inside `<code>`), insert_highlight_cards canonical helper, validate_elysia_anchors pre-POST (2 anchors resolved)
- Asset archive: /Users/quyue/www/blog/2026-09-22-serum-anion-gap-calculator
## 2026-09-22T23:40:47 — Carrying Capacity Estimator (WP 7470)

- **Tool**: `carrying-capacity-estimator` (Carrying Capacity Estimator — Verhulst logistic K-fit) — Health category
- **URL**: https://blog.flowrust.com/2026/09/23/carrying-capacity-estimator-field-guide-when-five-parameters-seven-judgement-calls-and-the-60-percent-rule-decide-whether-your-s-curve-identified-k-or-just-fit-the-data-2026-09-22/
- **date_gmt**: 2026-09-22T23:40:47
- **Title**: Carrying Capacity Estimator Field Guide: When Five Parameters, Seven Judgement Calls, and the 60 Percent Rule Decide Whether Your S-Curve Identified K or Just Fit the Data
- **Words**: ~1180 | H2: 8 | Cards: 3 | Poster: 1
- **Patches**: 0 (clean 1-POST)
- **Audit**: 0 findings (post-publish re-audit clean); 4/4 imgs HTTP 200; 2/2 elysia anchors HTTP 200; permalink HTTP 200
- **Elysia anchors**: 2 unique URLs (`/en/tools/carrying-capacity-estimator` x2 + `/en/tools` x1 kind_root)
- **Assets**: poster-7466, card1-7467, card2-7468, card3-7469
- **Card designs**: card1 = render_card_5tile (5 fit parameters), card2 = render_card_5tile_3plus2 (60% rule 3+2 grid), card3 = render_card_input_output_2col (Gause 1932 worked example)
- **Visual QA**: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap, takeaway text correct)
- **Skills path**: umbrella fallback (article-poster-creator + article-highlight-cards skills NOT on disk; used umbrella PIL templates per WP 6185/6352 cron cadence)
- **Picker**: theme-word scoring (theme_high keywords: estimator, calculator, validator, generator, etc.) → carrying-capacity-estimator (theme_score=11)
- **Source-side defenses**: pre_encode_code_spans + pre_encode_backslash (one `<code>` block with raw text), plain md_to_html (no `*` inside `<code>` spans), insert_highlight_cards canonical helper (3/3 cards inserted), validate_elysia_anchors pre-POST (2 anchors resolved against tool-manifest.json)
- **Asset archive**: /Users/quyue/www/blog/2026-09-22-carrying-capacity-estimator
## 2026-09-23T03:52:34 UTC — WP 7476 — Modular Arithmetic Calculator Field Guide

- Title: Modular Arithmetic Calculator Field Guide: When Five Operations, One Bezout Identity, and the Bit-Length Rule Decide Whether Your Modular Computation Is Exact or a Free Estimate
- URL: https://blog.flowrust.com/2026/09/23/modular-arithmetic-calculator-field-guide-when-five-operations-one-bezout-identity-and-the-bit-length-rule-decide-whether-your-modular-computation-is-exact-or-a-free-estimate-2026-09-23/
- Tool: modulo-arithmetic-converter (Math & Numbers) — Modular Arithmetic Calculator (Add / Subtract / Multiply / Inverse / Power): exact BigInt arithmetic for m up to 10^18, add/subtract/multiply show step-by-step reduction; inverse runs extended Euclidean algorithm with Bezout identity and explicit gcd(a,m)>1 handling; power uses fast square-and-multiply with per-bit table.
- date_gmt: 2026-09-23T03:52:34
- Mode: 1-POST + 1-PATCH (WP 6417 H1=title-dup family — body H1 emitted by md_to_html from source `# Title` line; stripped via `<h1>...</h1>\s*` regex, POSTed back via `POST /wp/v2/posts/7476`)
- Assets: 1 poster (1080×800) + 3 cards (1600×900: 1×3+2 cheatsheet "Five Operations, Five Algorithms", 1×2-col "Inverse: 5⁻¹ mod 18 = 11 with Bezout verification", 1×2-col "Power: 17⁵ mod 13 = 10 via square-and-multiply")
- vision_analyze: all 4 PNGs passed (no overflow, no tofu, no overlap, takeaway text correct; poster subtitle 795 px under 1080 limit)
- elysia anchors: 10 total — 9× /en/tools/modulo-arithmetic-converter + 1× /en/tools (kind-root); all 200 OK, validate_anchors=True
- Pre-POST sanity: 0 surviving `[..](..)` markdown links, 0 literal-HTML placeholders in `<code>`, 0 nested `<p><p>`, 0 orphan `<p></p>`, 3 highlight-card figures (WP 6122 mandatory assertion)
- Source-side defenses: pre_encode_backslash (no backslash escapes needed), pre_encode_code_spans (no literal HTML in backticks), plain md_to_html (no `*` inside `<code>` spans, no triple-fence), insert_highlight_cards canonical helper (3/3 inserted), validate_elysia_anchors pre-POST
- **Visual QA**: all 4 PNGs passed vision_analyze (no overflow, no tofu, no overlap, takeaway text correct)
- **Skills path**: umbrella fallback (article-poster-creator + article-highlight-cards skills NOT on disk; used umbrella PIL templates per WP 6185/6352 cron cadence)
- **Picker**: theme-word scoring (theme_high keywords: estimator, calculator, validator, generator, etc.) → modulo-arithmetic-converter (theme_score=6, top pick from 2281 eligible candidates)
- **Asset archive**: /Users/quyue/www/blog/2026-09-23-modular-arithmetic-calculator## 2026-09-23T08:07:48 UTC — WP 7485 — TPN Osmolality Estimator Field Guide

- Title: TPN Osmolality Estimator Field Guide: When Five Components, Three Failure Modes, and the Calcium-Phosphate Hole Decide Whether Your Admixture Is Peripheral or Central
- URL: https://blog.flowrust.com/2026/09/23/tpn-osmolality-estimator-field-guide-when-five-components-three-failure-modes-and-the-calcium-phosphate-hole-decide-whether-your-admixture-is-peripheral-or-central-2026-09-23/
- Tool: tpn-osmolality-estimator (Health) — TPN Osmolality Estimator (Peripheral/Central)
- date_gmt: 2026-09-23T08:07:48
- Mode: 1-POST 0-PATCH clean
- Assets: 1 poster (1080x800) + 3 cards (1600x900: 1x5-tile "The Formula Anatomy", 1x4-tile compact "What Osmolality Can Not Catch", 1xaudit "The Four Checks Before You Trust")
- vision_analyze: all 4 PNGs passed (no overflow, no tofu, no overlap, takeaway text correct; poster subtitle 799 px under 1080 limit; card 2 first-pass 4tile canonical overlap -> switched to render_card_4tile_compact auto-shrink chain, re-rendered clean)
- elysia anchors: 9 total - 8x /en/tools/tpn-osmolality-estimator + 1x /en/tools (kind-root); all 200 OK, validate_anchors=True, 0 phantom slugs
- image URLs: 4/4 HTTP 200 after retry (poster-1, card1-1, card2-1, card3-1; initial transient URLError on poster+card1 retry resolved)
- Pre-POST sanity: 0 surviving `[..](..)` markdown links, 0 literal-HTML placeholders in `<code>`, 0 nested `<p><p>`, 0 orphan `<p></p>`, 1 poster + 3 highlight-card figures (WP 6122 mandatory assertion)
- Source-side defenses: no backslash escapes needed, no literal HTML in backticks, plain md_to_html (no `*` inside `<code>` spans, no triple-fence), insert_highlight_cards canonical helper (3/3 inserted), validate_elysia_anchors pre-POST (0 phantom, 8 tool + 1 kind-root)
- **Picker**: theme-word scoring (theme_high keywords: estimator, calculator, validator) -> tpn-osmolality-estimator (theme_score=11, top pick from 2983 tools)
- **Skills path**: umbrella fallback (article-poster-creator + article-highlight-cards skills NOT on disk; used umbrella PIL templates per WP 6185/6352 cron cadence)
- **Asset archive**: /Users/quyue/www/blog/2026-09-23-tpn-osmolality-estimator


## 2026-09-23T12:17:17 UTC — WP 7491 — Protein-DNA Binding Affinity Calculator Field Guide

- Title: Protein-DNA Binding Affinity Calculator Field Guide: When One Fraction-Bound Reading, Two Affinity Bands, and the delta-G Temperature Sweep Decide Whether Your TF-Site Interaction Is Tight, Sequence-Specific, or Just Electrostatic
- URL: https://blog.flowrust.com/2026/09/23/protein-dna-binding-affinity-calculator-field-guide-when-one-fraction-bound-reading-two-affinity-bands-and-the-delta-g-temperature-sweep-decide-whether-your-tf-site-interaction-is-tight-sequence-speci/
- Tool: protein-dna-binding-affinity (Education) - Protein-DNA Binding Affinity Calculator (Kd Estimate): single-point Kd estimate for 1:1 protein-DNA complex, f=[P]/([P]+Kd), reports Kd + delta-G + tier classification (very tight/tight/weak); supports anisotropy path r=(r-rfree)/(rbound-rfree); assumes 1:1 stoichiometry + [P]free=[P]total + equilibrium
- date_gmt: 2026-09-23T12:17:17
- Mode: 1-POST 0-PATCH clean
- Assets: 1 poster (1080x800) + 3 cards (1600x900: 1x5-tile "Five Numbers Behind the 25C Default", 1x5-tile "Three Affinity Bands and Their Biology", 1x5-tile "Three Assumptions That Bite")
- vision_analyze: all 4 PNGs passed (no overflow, no tofu, no overlap, takeaway text correct; poster subtitle within W=1080; cards 1/2/3 clean at 1600x900)
- elysia anchors: 3 total - 2x /en/tools/protein-dna-binding-affinity + 1x /en/tools (kind-root); all 200 OK, validate_anchors=True, 0 phantom slugs
- image URLs: 4/4 HTTP 200 (poster-59, card1-58, card2-59, card3-56; WP dedup auto-renamed)
- Pre-POST sanity: 0 surviving `[..](..)` markdown links, 0 literal-HTML placeholders in `<code>`, 0 nested `<p><p>`, 0 orphan `<p></p>`, 3 highlight-card figures (WP 6122 mandatory assertion), 0 CARD placeholder leak
- Source-side defenses: pre_encode_backslash (no backslash escapes needed), pre_encode_code_spans (no literal HTML in backticks), plain md_to_html (no `*` inside `<code>` spans, no triple-fence), insert_highlight_cards canonical helper (3/3 inserted), validate_elysia_anchors pre-POST
- **Picker**: pick_tool_v4_content_based.py -> top diverse pick (Education) = protein-dna-binding-affinity (theme_score from among Health-heavy Top-20)
- **Skills path**: umbrella fallback (article-poster-creator + article-highlight-cards skills NOT on disk; used umbrella PIL templates per WP 6185/6352 cron cadence)
- **Asset archive**: /Users/quyue/www/blog/2026-09-23-protein-dna-binding-affinity-calculator-field-guide-when-one-fraction-bound-reading-two-affinity-bands-and-the-delta-g-temperature-sweep-decide-whether-your-tf-site-interaction-is-tight-sequence-speci
- covered_slugs: 818
