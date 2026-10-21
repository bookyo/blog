# NOT PUBLISHED — origin 502 outage

**Status:** staged, validated, ready to publish. NOT published.
**Last attempt:** 2026-10-21 11:34 UTC (tick 5; origin down ~39h continuous, 5th tick)
**Poll budget this tick:** 300 real seconds, then abort (aborted cleanly, exit 2).

## Why it is not published

`blog.flowrust.com` origin returns HTTP 502 from the Cloudflare edge. Diagnostic
ladder confirms the origin, not the edge and not the credentials. Tick 5 ladder,
all re-probed this run:

| probe | result |
|---|---|
| `https://blog.flowrust.com/` | 502 (`CF-RAY: a4dff3f1...-AMS`, `Server: cloudflare`) |
| `/wp-json/` unauthenticated | 502 |
| `/wp-json/wp/v2/posts?per_page=1` authenticated | 502 |
| `/wp-json/` × 3 retries, 3s apart | 502 / 502 / 502 (not intermittent) |
| `https://example.com/` | **200** |
| `https://elysiatools.com/` | 307 |

The edge is answering (real `CF-RAY`, real Cloudflare headers); the origin behind
it is not. Credentials are not implicated — they are never exercised because
the 502 precedes any auth.

## What IS ready

Re-verified from disk this tick (not trusted from the prior session's self-report):

- `audit_post_content(body_final.html)` → **0 findings**
- anchor validation → **4/4 real** (`markdown-table-to-csv-json-schema`,
  `json-schema-validator`, `csv-samples`, `markdown-samples`)
- structure → 8 `<h2>`, 0 `<h1>`, 0 `<h3>`, 3 `figure.highlight-card`,
  1 `figure.article-poster`
- assets → `poster.png` 1080×800, `card1/2/3.png` 1600×900
- placeholders → exactly `POSTER_URL`, `CARD1_URL`, `CARD2_URL`, `CARD3_URL`
  (substituted at publish time; WP 7163 leak defense asserts 0 remain)
- 1979 words

## How to publish once the origin is back

```bash
DATE_GMT=NOW WAIT_SECS=300 \
  /Users/quyue/.hermes/hermes-agent/venv/bin/python3.11 /tmp/wp_r1/driver.py
```

**Keep `WAIT_SECS` below the terminal tool's own cap (420s as of tick 5).** A
`WAIT_SECS=540` budget gets the driver SIGKILLed by the caller at ~332s, *before*
its abort branch runs — the run then exits with no state record at all, which is
indistinguishable from a crash. Tick 5 hit this; `WAIT_SECS=300` aborts cleanly
with `exit 2`. Reserve headroom: `WAIT_SECS <= 300`.

`driver.py` (in this directory) polls until the REST API answers 200, then
uploads 4 assets with 3-retry backoff, substitutes the full `source_url`
(preserving the `/uploads/YYYY/MM/` prefix), asserts 0 placeholder leaks and
exactly 3 card figures, and POSTs with `status: publish`, `featured_media: 0`,
and a `date_gmt` computed at POST time.

Slug is deliberately **not** in `wp_cron_state.json`'s `covered_slugs`, so the
next cron tick will pick this tool up again rather than skipping it as done.
Re-verified tick 5: `markdown-table-to-csv-json-schema` still absent from
`covered_slugs` (39 entries).

## Tick-5 additions to the outage runbook

1. **Aborting is not "logged" — it is "recorded."** Tick 4 logged
   `origin never recovered ... -- aborting` and then wrote no state file, because
   `save_state()` still carried `json.dump(st, indent=2)` (missing `fp`). The
   fixed shape was on disk but *unexercised*. Tick 5 smoke-tested the abort
   branch against a scratch path (`/tmp/wp_r1/tick5_smoke_abort.py`) — reproducing
   the `TypeError`, then asserting the fixed shape writes and reads back — and
   then ran the real driver, which persisted
   `{"status": "aborted_origin_still_down", "published": false, "waited_real": 301}`.
   **If the abort branch is the only thing your tick exercises, test it against a
   scratch path and then at the real path.** A `driver.log` tail is not evidence
   the run completed.
2. **The caller's timeout is part of the abort contract.** The driver's abort is
   only meaningful if it runs; a `WAIT_SECS` above the tool cap converts a clean
   abort into a silent kill. Keep the poll budget under the cap with margin.
3. **Verify parked artifacts by hash, not by self-report.** Tick 5 confirmed
   `article_final.html` and all 4 PNGs are byte-identical between the archive dir
   and `/tmp/wp_r1/` before re-running the full verification suite.

## Operator note

Five ticks and ~39h of continuous 502 is past the point where this is a cron
problem, and it is now the second consecutive tick where the deliverable is
blocked on host state rather than anything the job can do. Repeated 502s from a
LiteSpeed origin with no partial responses, while Cloudflare still answers with
a real `CF-RAY`, usually means the origin is being OOM-killed or has run out of
disk — not that it is refusing connections. Worth checking the host's memory,
disk and PHP-FPM error log before the next tick. Nothing in this repository can
clear it.