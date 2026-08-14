# Upside-Down Text Field Guide: How the Unicode Flip Actually Works

**Post ID:** 5986
**URL:** https://blog.flowrust.com/2026/08/14/upside-down-text-field-guide-2026-08-14/
**Slug:** upside-down-text-field-guide-2026-08-14
**Date (UTC):** 2026-08-14T02:51:02
**Featured media:** 0 (COSESAI theme defense)
**Status:** publish

## Audit summary
- 0 body H1, 8 body H2 + 1 theme H2 = 9 total
- 1 article-poster + 3 highlight-card figures
- 4/4 image URLs HTTP 200
- 2/2 elysia anchor URLs HTTP 200
- p_opens/closes balanced (21/21 in DOM, 24/24 pre-POST)
- 4 <ul>, 1 <ol>, 15 <li>
- audit_post_content clean post-PATCH (0 findings)
- DOM check: H1=1 (theme entry-title), H2=9, 0 duplicate body H1, all elysia anchors valid

## Round-trips
1 POST + 1 PATCH

## PATCH reason
MERGED_NUMBERED_LIST: 1 block — "Three properties fall out of this design:" section had three numbered list items (1./2./3.) joined into one <p>. Fixed via inline <ol><li> PATCH (WP 5717 lesson).

## elysia links embedded
- https://elysiatools.com/en/tools/upside-down-text (1)
- https://elysiatools.com/en/tools (1)
