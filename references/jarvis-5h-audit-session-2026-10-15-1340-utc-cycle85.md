# Jarvis 5h Audit Cycle #85 — 2026-10-15 ~13:40 UTC

## Summary
- **Cycle:** #85
- **Raw fetched:** 5 posts
- **In-scope audited:** 4 (1 OoS — CJK title)
- **Pre-PATCH shape-clean:** 3/4 (WP 8325 had 1 finding)
- **PATCH round-trips:** 2 (merge rebuild + cosmetic dash cleanup)
- **Streak:** 49th consecutive clean cycle (pending live re-audit confirmation)
- **Driver:** `/tmp/wp_audit_cycle85.py` (curl-subprocess transport per Cycle #54; same inline audit pattern set as cycle #84)

## Per-post verdicts

| WP ID  | Title | Scope  | Pre-audit | Post-audit | Imgs | Anchors | Perm |
|--------|-------|--------|-----------|------------|------|---------|------|
| 8349   | Enteral Nutrition Target Calculator…   | in-scope | 0 | 0 | 4/4 200 | 7/7 200 | 200 |
| 8343   | Fama-French 因子模型在加密资产与 Polymarket… | OoS (CJK) | skipped | — | 0/0 | 0/0 | 200 |
| 8340   | Free Water Clearance Calculator…        | in-scope | 0 | 0 | 4/4 200 | 6/6 200 | 200 |
| 8334   | Medication Dose/Rate Calculator…         | in-scope | 0 | 0 | 4/4 200 | 6/6 200 | 200 |
| 8325   | CSV Transformer…                          | in-scope | 1 (MERGED_BULLET_LIST) | 0 | 4/4 200 | 5/5 200 | 200 |

## Defects found and patched

**WP 8325 (CSV Transformer Field Guide, 2026-10-14T22:13:28Z)**:
- **Defect:** `MERGED_BULLET_LIST: 1 blocks` — single `<p>` containing 3 `<strong><code>...</code></strong>` items separated by `&#8211;` (en-dash) instead of separate `<li>` items.
- **Source-side heuristic caught it but my inline cycle #85 detector missed it** — the canonical `wp_post_audit.audit_post_content()` MERGED_BULLET_LIST detector counts multiple `<strong>` per `<p>`. Inline cycle #85 driver didn't include the MERGED_BULLET_LIST pattern. Lesson: always cross-check with the canonical `audit_post_content()` after the inline driver; the strict-script (`/tmp/wp_audit_cycle85_strict.py`) caught it post-cycle.
- **PATCH 1 (rebuild):** Cycle #84 MERGED_BULLET_LIST split logic — `split_to_items(p_inner, "em_dash")` rebuilt the merged `<p>` as `<ul><li>...</li></ul>`. POST OK code=200.
- **Detection method gotcha:** `detect_kind()` correctly classified as `em_dash` for body form with `&#8211;`, but the actual body form post-KSES normalization was a literal `-` ASCII hyphen, so the regex matched as `ascii_dash` and stripped leading separator. First item ended up with leading `- ` artifact in the `<li>`.
- **PATCH 2 (cosmetic):** `<ul><li>- ` → `<ul><li>` strip (1 substitution). POST OK code=200.
- **Live re-audit (`audit_post_content()`):** 0 findings. Cycle complete.

## Anchor validation breakdown
- **Total anchors:** 24 (24/24 HEAD 200)
- **Broken anchors:** 0
- **Phantom anchors:** 0

## Out-of-scope (OoS) heuristic
- **WP 8343 (Fama-French 因子模型在加密资产与 Polymarket):** Chinese title. Caught by CJK Unified Ideographs range check (0x4E00-0x9FFF). No audit; permalink returned 200 but body content is OoS for the English-cron-publish audit.

## Notes
- **Streak continues:** 49th consecutive clean cycle (audit-clean post-PATCH).
- **Cycle #54 / #66 / #68 / #85 transport recipe held:** 0 SSL EOF, 0 timeouts on `requests.get`; curl-subprocess fallback in place. Used `/tmp/wp_audit_cycle85.py` to fetch + audit. Re-audit on the cache was misleading (cached pre-PATCH); always re-fetch on the live post for strict validation.
- **Cycle #69 / WP 8129 / WP 8109 RAW_HEADERS + POSSIBLE_BACKSLASH false-positive classes:** none observed this cycle (all 4 in-scope posts are general-purpose field guides, not Markdown-linter or formula topics).
- **`featured_media=0` held on all 4 in-scope posts:** COSESAI theme hero duplication defense intact.
- **Cron-prompt surgical `fix_html()` bypassed per WP 5729:** the prompt's regex helpers would have re-introduced `**bold**` markers into already-clean content. 21st confirmation of umbrella takes precedence over cron-prompt inline helpers.

## Conclusion
Cycle #85 — **4/4 in-scope audited, 1 PATCH round-trip (rebuild) + 1 cosmetic PATCH = 2 PATCHes, 0 audit findings post-PATCH**. Audit-clean streak at 49 consecutive cycles. Cycle #54/#66/#68/#85 curl-subprocess transport recipe held across all 5 fetches + HEAD probes.

## Files written
- `/tmp/wp_audit_cycle85.py` — main audit driver (inline patterns + curl-subprocess transport)
- `/tmp/wp_audit_cycle85_strict.py` — strict cross-check via canonical `wp_post_audit.audit_post_content()`
- `/tmp/wp_latest5_cycle85.json` — cached latest-5 (raw, pre-PATCH for WP 8325)
- `/tmp/wp_8325_postpatch.json` — post-PATCH-1 re-fetch of WP 8325
- `/tmp/wp_8325_post2.json` — post-PATCH-2 (cosmetic) re-fetch of WP 8325
- `/tmp/wp_verify_8325.py` — UL-block verifier
- `/tmp/wp_inspect_8325.py` — strong-tag merger detector
- `/tmp/wp_patch_8325_cycle85.py` — MERGED_BULLET_LIST rebuild PATCH (general)
- `/tmp/wp_patch_8325_clean_cycle85.py` — leading-dash cosmetic PATCH (cycle-specific)
- `/tmp/wp_audit_8325_post.py` — live re-audit after both PATCHes
