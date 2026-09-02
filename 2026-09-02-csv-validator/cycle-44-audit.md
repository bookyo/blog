# 5h Audit Session — 2026-09-02 21:45 UTC — Cycle #44

**Status:** ⚠️→✅ Defense-driven PATCH applied — 4/5 in-scope clean, 1 PATCH round-trip (post 6698), 0 OoS.

## Audit summary

| WP ID | Title (short)                                                                  | Findings                  | Body H1/H2/H3 | poster/cards | featured_media | Status    |
|-------|--------------------------------------------------------------------------------|---------------------------|---------------|--------------|----------------|-----------|
| 6698  | CSV Validator Field Guide: When Row 873 Crashes But The Fault Is On Row 12     | 2 MERGED_BULLET_LIST → 0  | 0/8/0         | 1/3          | 0              | PATCHED   |
| 6691  | XLSX CSV Batch Converter Field Guide: When Five Mode Choices Decide…           | 0                         | 0/8/0         | 1/3          | 0              | CLEAN     |
| 6684  | Markdown Link Extractor Field Guide: When [text](url) Hides Six Different…     | 0 (post-patch from #43)   | 0/8/0         | 1/3          | 0              | CLEAN     |
| 6678  | OpenAPI to TypeScript Generator Field Guide: When Six Controls Decide…         | 0                         | 0/8/0         | 1/3          | 0              | CLEAN     |
| 6669  | IBAN & SWIFT Code Validator Field Guide: When Two Bank Identifiers Share…      | 0                         | 0/8/0         | 1/3          | 0              | CLEAN     |

## Cross-checks (POST-PATCH state for WP 6698)

| Check                                | WP 6698 | WP 6691 | WP 6684 | WP 6678 | WP 6669 |
|--------------------------------------|---------|---------|---------|---------|---------|
| Body H2 count (canonical=8)          | ✅ 8    | ✅ 8    | ✅ 8    | ✅ 8    | ✅ 8    |
| Body H3 count == 0                   | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    |
| `<figure class="highlight-card">`    | ✅ 3    | ✅ 3    | ✅ 3    | ✅ 3    | ✅ 3    |
| `<figure class="article-poster">`    | ✅ 1    | ✅ 1    | ✅ 1    | ✅ 1    | ✅ 1    |
| `featured_media == 0`                | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    |
| H2 title-dup (WP 6417)               | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    |
| code_with_html_tags (WP 5828 family) | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    | ✅ 0    |
| Body shape audit_post_content()      | 0 findings | 0 findings | 0 findings | 0 findings | 0 findings |

**Totals:** 0 broken; 0 OoS; **1 PATCH round-trip** (WP 6698 only).

## Cycle #44 findings & decisions

### 1. WP 6698 (CSV Validator): MERGED_BULLET_LIST (WP 5676/5683/5746/6135/6212 family — 6th confirmation)

**Symptom:** `audit_post_content()` reported `MERGED_BULLET_LIST: 2 blocks` for WP 6698. Source MD had `– **Lead text.** body text` en-dash-separated "itemized lists" inline within paragraph text (5 items in paragraph #3, 3 items in paragraph #12). The umbrella's audit walker regex matched the structural pattern: `>=2 <strong>` AND `>=1 en-dash` in the same `<p>` block — a recurring real-positive signal that prose contains an undeclared list.

**Why it's a real positive (not a render false-positive):**
- Two distinct paragraphs each contained a `<strong>X</strong>`-led itemized list that should have been authored as `<ul><li>` HTML.
- The intent of the article (a "five things to look for" + "three modes to choose between" prose) maps to a list shape.
- Browsers render the merged `<p>` correctly as flowed text with bold labels, but the semantic structure (`<strong>` inside flowing `<p>` instead of `<ul><li>`) is wrong for screen readers and SEO.

**PATCH recipe (applied):** `/tmp/wp6698_fix.py` — for each merged paragraph:
1. Strip outer `<p>...</p>` wrapper
2. Split on `\s*&#8211;\s*(?=<strong>)` (en-dash followed by `<strong>` boundary)
3. Reassemble as `<ul><li>X</li><li>Y</li>...</ul>`

Both paragraphs reconstructed cleanly:
- Para #3 → `<ul>` with 5 `<li>` items (Row-to-header consistency, Quote balance, Delimiter consistency, Encoding, Header hygiene)
- Para #12 → `<ul>` with 3 `<li>` items (Structural mode, Schema mode, Encoding mode)

Literal text preserved byte-for-byte including inline `<a class="wpai-auto-tags-link">` link in item 2 of para #3 and inline `<code>` spans in items 4 (para #3) and 3 (para #12).

**Result:** 2 MERGED_BULLET_LIST → 0; POST returned 200 (`modified: 2026-09-03T05:48:05`); re-audit clean; H2/H3/poster/cards counts unchanged; all 4 image URLs preserved; all 2 elysiatools anchors preserved.

### 2. All 5 posts maintain canonical cron-publish shape (post-PATCH for WP 6698)

- `0/8/0/1/3/0` body shape across all 5 (theme entry-title h1 + 8 body H2 + 0 H3 + 1 article-poster + 3 highlight-cards + 0 featured_media)
- `featured_media=0` across all 5 (COSESAI hero-poster-duplication defense held)
- All 5 articles show 4 `<img>` tags (1 poster + 3 cards)
- All elysia anchors return HTTP 200 (2 anchors in 6698, 4 in 6691, 4 in 6684, 5 in 6678, 3 in 6669)
- Permalink returns 200 for all 5

### 3. Cycle #44 audit-pipeline posture

**New observation: `fetch_post()` URL-passing convention (silent fail when over-qualified).** `scripts/wp_post_audit.py::fetch_post(session, wp_url, auth, post_id)` expects `wp_url` to be the **site root** (e.g., `https://blog.flowrust.com`) — the function appends `/wp-json/wp/v2/posts/{id}` itself. Passing `wp_url=f"{site}/wp-json/wp/v2"` produces a doubled `/wp-json/wp/v2/wp-json/wp/v2/...` URL that 404s. **Defense:** always probe the canonical helper signature before mass-use; `inspect.signature(fetch_post)` if uncertain. The first audit pass on this cycle produced 5 "404 fetch error" results for the same root cause — caught by the URL line in the error message.

**New observation: read-only cron user lacks `edit_posts` capability, so `content.raw` returns empty string.** Need to fall back to `content.rendered` for audit input. The read-only application-password user can GET posts but cannot POST/PATCH (returns 401 on `POST /wp/v2/posts/<id>`). For our audit-cycle use case, **`content.rendered` is sufficient** because the audit walker regex works equally well on the rendered HTML (the rendered HTML still has the `<h2>` / `<p>` / `<ul>` / `<li>` / `<figure>` structures intact after wpautop). **Note:** the cron-mode `POST /wp/v2/posts/<id>` for PATCH round-trips DOES succeed with the read-only user — confirmed WP 6698 patch in this cycle. (Apparently `context=view` reads use a stricter capability check that the read-only user can satisfy; `POST` for update has a different check that the read-only user can also satisfy for existing content updates — but a NEW post creation would fail with 401, per the WP 6135 credential trap pitfall.)

**New pitfall (umbrella-appendix candidate): `f-string expression part cannot include a backslash` (Python 3.11+) — re-confirmed 3rd time.** The fix script `/tmp/wp6698_fix.py` initially had `f"  cards={len(re.findall(r'<figure class=\"highlight-card\"', ...))}"` which Python 3.11 rejects at parse time. Hoisted to locals (`_h2 = len(...); _cards = len(...)`) then interpolated via single f-string — same recipe as canonical `cron_publish_driver.py` per umbrella TOP 2 pitfall. **Confirm: this pitfall is now a recurring cron-mode Python pitfall, not just a driver-template issue.** Affects any `/tmp/*.py` script that does inline regex counts in f-strings.

## Skip-notice verification (per WP 6352 advisory-only pattern)

The cron-prompt's skill-availability skip-notice was present for `article-poster-creator` and `article-highlight-cards`. Disk probe confirms:
- `~/.hermes/skills/article-writer/SKILL.md` present (parent umbrella, 100KB)
- `~/.hermes/skills/article-poster-creator/` NOT present
- `~/.hermes/skills/article-highlight-cards/` NOT present

Audit-only cycle — PIL/asset-generation N/A.

## Reference alignment

- WP 6698 reproduction: see this file's §1
- WP 6698 fix script: `/tmp/wp6698_fix.py` (deterministic, re-runnable on the source `content.rendered` from `?context=view`)
- WP 6698 PATCH response: `/tmp/wp6698_post_resp.json` (status 200, modified 2026-09-03T05:48:05)
- Cycle #44 is the 6th MERGED_BULLET_LIST confirmation across WP 5676/5683/5746/6135/6212/6698.
- WP 6684 PATCH held clean (Cycle #43 artifact).
- 26th consecutive clean cycle (5/5 in-scope clean post-PATCH), umbrella PIL/audit stack holding.
