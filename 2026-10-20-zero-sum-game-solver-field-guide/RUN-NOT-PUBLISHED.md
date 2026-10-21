# NOT PUBLISHED — origin down 2026-10-20

This tick produced a complete, verified article and asset set but could NOT publish.

**Cause:** blog.flowrust.com returned `HTTP/1.1 502 Bad Gateway` (Server: cloudflare)
on every route — frontend and REST — continuously from 04:36 UTC for the whole run
(~35 min). Control host example.com returned 200 throughout, so the origin server
(LiteSpeed) is down, not the local network.

**State:** everything is ready to publish as-is. Run, from this directory:

```
python3 publish_driver.py     # waits for origin 200, uploads 4 assets, POSTs the post
python3 post_audit.py         # after publish: content audit + HEAD probes
```

`article_body.html` already has POSTER_URL / CARD1_URL / CARD2_URL / CARD3_URL
placeholders that `publish_driver.py` substitutes from the upload responses.

**Tool:** game-theory-zero-sum (Zero-Sum Game Solver (Saddle Point / Linear Programming))
**Dedup:** verified absent from state file + all 1119 archive dirs. No slug collision
with anything published (last post was WP 8492 on 2026-10-18).

**Verification already done on this content:**
- `validate_anchors` -> ok=True, phantoms=[] (all 3 tool slugs real in tool-manifest.json)
- `audit_post_content` -> 0 findings
- 8 H2 / 0 H1 / 0 H3 / 0 pre / 0 pipe-table leak / 0 merged bullets
- 3 highlight-card figures + 1 article-poster figure asserted pre-build
- all 4 assets passed `vision_analyze`
- all worked examples numerically verified with numpy

## Files

- `article.md` — markdown source (8 H2, 0 H1/H3)
- `article_body.html` — built HTML with figures inserted and URL placeholders
- `poster.png` (1080x800), `card1.png`, `card2.png`, `card3.png` (1600x900)
- `build_body.py` — rebuilds article_body.html from article.md
- `publish_driver.py` — origin wait + 4 uploads + post create (with force-publish step)
- `post_audit.py` — post-publish content audit + anchor/image/permalink HEAD probes
- `verify_math.py` / `verify_math2.py` — numpy verification of every worked example
- `origin-down-502-publish-abort-2026-10-20.md` — the operational lessons from this run