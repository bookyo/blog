# Secure Random Generator Field Guide: Entropy, Three Encodings, and Why Math.random() Fails

**Post ID:** 5683
**URL:** https://blog.flowrust.com/2026/08/06/secure-random-generator-field-guide-2026-08-06/
**Date (UTC):** 2026-08-06T05:24:41
**Tool:** secure-random-generator (Security)

## Run summary

- 1 POST + 3 PATCH round-trips (fix merged bullet, strip stray asterisks, remove duplicate lead-in)
- 4 PIL assets rendered + vision_analyze pre-POST QA
- featured_media=0 verified (COSESAI theme hero defense)
- 8 body H2s + 3 highlight cards + 1 article-poster
- 6/6 elysia anchors HTTP 200, 4/4 image URLs HTTP 200
- h1=1 (theme entry-title only), h2=9 (8 body + 1 theme nav)

## Assets

- poster.png (1080x800): "Stop Generating Secrets with Math.random()"
- card1.png (1600x900): One 256-bit Secret, Five Views (hex/base64/base64url/custom/length)
- card2.png (1600x900): Two Branches, One CSPRNG (audit card: byte encoding vs custom alphabet)
- card3.png (1600x900): Where the Entropy Actually Comes From (Linux/macOS/Windows/Browser)

## Defenses applied

- slug pre-validated against tool-manifest.json
- featured_media=0 in payload (COSESAI theme)
- 0 body H1 (theme renders entry-title)
- 0 fabricated slugs (security category URL whitelisted)
- all 4 assets passed vision_analyze visual QA before POST

## Defects caught and fixed

- poster subtitle was 1102px wide on 1080 canvas (clipped at left edge); shortened to 943px
- card3 was 2x2 grid with tile_h=320 — values like /dev/urandom overflowed at 150pt; switched to single-row 4-tile variant with auto-shrink (per WP 5676 recipe)
- The "three concrete places" bullets (JWT/API/Session) merged into one <p> with stray asterisks (RAW_ITALIC + MERGED_BULLET pattern from WP 5656/5676); replaced with real <ul><li>
- Single stray "*" in "may be less* than" — restored to <em>less</em>
- Duplicate lead-in paragraph after PATCH merge (one of the merged-bullet residues); removed
