# NOT PUBLISHED — origin 502 outage

**Status:** staged, validated, ready to publish. NOT published.
**Last attempt:** 2026-10-21 15:49 UTC (tick 7; origin down ~42h continuous, 7th tick)
**Poll budget this tick:** 300 real seconds, then abort (aborted cleanly, exit 2).
**Abort receipt:** `publish_state.json` mtime `23:54:54` == final log line; `waited_real: 304`.

## Why it is not published

`blog.flowrust.com` origin returns HTTP 502 from the Cloudflare edge. Diagnostic
ladder confirms the origin, not the edge and not the credentials. Tick 7 ladder,
all re-probed this run:

| probe | result |
|---|---|
| `https://blog.flowrust.com/` | 502 (`CF-RAY: a4e168fd0bc6e7b9-FRA`, `Server: cloudflare`, `Content-Length: 16`) |
| `/wp-json/` unauthenticated | 502 |
| `/wp-json/wp/v2/posts?per_page=1&_fields=id` authenticated | 502 |
| same URL × 3 retries, 4s apart | 502 / 502 / 502 |
| `https://example.com/` | **200** |
| `https://elysiatools.com/en/tools` | **200** |

The edge is answering (real `CF-RAY`, real Cloudflare headers); the origin behind
it is not. Credentials are not implicated — they are never exercised because
the 502 precedes any auth.

Note: the `CF-RAY` datacenter suffix rotates between ticks (`-AMS` on tick 6,
`-FRA` on tick 7) because the edge PoP serving the probe varies. A changing
suffix is **not** evidence the origin moved or partially recovered.

## Tick-7 methodology (the re-verify-then-repark loop)

Three commands, ~60s, no rebuild:

1. **Ladder probe** — establish origin state before touching anything.
2. **Derive this tick's verifier by string substitution on the previous one**,
   never by hand:
   `python3 -c "src=open('tick6_reverify.py').read(); open('tick7_reverify.py','w').write(src.replace('tick6','tick7'))"`.
   The hash-checked assertions carry over unchanged, so the hash comparison is
   what guards against a stale or mis-copied verifier.
3. **Launch the parked driver with `terminal(background=true)`**, not
   `nohup … &` — the shell rejects `&`-backgrounding explicitly. `notify=true`
   is unavailable in cron (no async completion), so poll with
   `process(action='poll')` and confirm the exit code (`2` = clean abort).

**Cosmetically alarming, harmless:** zsh rc noise (`compinit: initialization
aborted`, `compdef: command not found`, missing `openclaw.zsh`) appears in the
background-process output preview. That is the login shell's rc, not the driver.

**Doubled log lines are not a double-run.** `log()` both `print()`s (stdout,
which the shell redirects into `driver.log`) *and* appends to `driver.log`, so
every line appears twice. Confirm with `ps -o pid,ppid,lstart,command -p …`
before assuming two drivers are running: here PID 87480 was simply the child of
the zsh wrapper 87143 — one driver, two log writers. A genuine double-publish
hazard would show two independent python PIDs with no parent/child relation.

## What IS ready

Re-verified from disk this tick (not trusted from the prior session's self-report):

- `audit_post_content(body_final.html)` → **0 findings**
- `validate_anchors(body_final.html)` → **ok=True, 0 reasons** (5 anchors, all real catalog IDs:
  `tools/markdown-table-to-csv-json-schema`, `tools/json-schema-validator`,
  `samples/csv-samples`, `samples/markdown-samples`)
- structure → 8 `<h2>`, 0 `<h1>`, 0 `<h3>`, 3 `figure.highlight-card`,
  1 `figure.article-poster`; source-MD `## ` count (8) == HTML h2 count (8)
- assets → `poster.png` 1080×800, `card1/2/3.png` 1600×900 each
- all 4 PNGs **sha256 MATCH** vs `/tmp/wp_r1/assets/`; `article.md`,
  `article_final.html`, `driver.py` sha256 MATCH as well
- no leak defects: 0 pipe-table leaks, 0 markdown links, 0 literal `**bold**`, 0 orphan closes
- 1979 words
- placeholders → exactly `POSTER_URL`, `CARD1_URL`, `CARD2_URL`, `CARD3_URL`
  (pre-upload staging tokens, substituted at publish time)

**Publish path proven executable without touching the network** (tick 6,
`tick6_dryrun.py`): replicated the driver's substitution block with dummy
`source_url`s → 0 placeholders left, 3 card figures, 4 img srcs under
`/uploads/2026/10/`, `featured_media: 0`, `date_gmt` resolved from `DATE_GMT=NOW`
at build time, and a re-audit of the *substituted* body → 0 findings, anchors ok=True.

## How to publish once the origin is back

```bash
DATE_GMT=NOW WAIT_SECS=300 \
  /Users/quyue/.hermes/hermes-agent/venv/bin/python3.11 /tmp/wp_r1/driver.py
```

**Keep `WAIT_SECS` below the terminal tool's own cap (420s as of tick 5).** A
`WAIT_SECS=540` budget gets the driver SIGKILLed by the caller at ~332s, *before*
its abort branch runs — the run then exits with no state record at all, which is
indistinguishable from a crash. Tick 4 hit this; `WAIT_SECS=300` aborts cleanly.
Reserve headroom: `WAIT_SECS <= 300`.

`driver.py` (in this directory) polls until the REST API answers 200, then
uploads 4 assets with 3-retry backoff, substitutes the full `source_url`
(preserving the `/uploads/YYYY/MM/` prefix), asserts 0 placeholder leaks and
exactly 3 card figures, and POSTs with `status: publish`, `featured_media: 0`,
and a `date_gmt` computed at POST time.

Slug is deliberately **not** in `wp_cron_state.json`'s `covered_slugs`, so the
next cron tick will pick this tool up again rather than skipping it as done.

## Tick-6 additions to the outage runbook

1. **Pre-upload placeholders are not the WP 7163 leak defect.** WP 7163's rule
   applies to a POSTed payload, never to a body that has not been uploaded yet.
   `CARDn_URL`/`POSTER_URL` in `body_final.html` are correct staging state. Prove
   substitution with a fake-URL dry run (see above) instead of either panicking or
   silently ignoring them — and re-audit the *substituted* body, not the staged one.
2. **`validate_anchors` returns `(ok, reasons)`.** `inspect.getsource(...)` shows
   `-> Tuple[bool, List[str]]`. Defensive "is it a tuple?" code that grabs `res[0]`
   gets the bool and then iterates it → `TypeError: 'bool' object is not iterable`.
3. **Don't reuse a variable name for two roles across sections of a verification
   script.** Reassigning `bad` (anchor reason list) to an int leak counter made a
   late `len(bad)` throw — after every real check had already printed, so the
   verdict file was silently never written. `phantom` for reasons, `leak_bad` for
   counters.
4. **The abort contract now holds end-to-end.** Tick 6 re-parked with
   `WAIT_SECS=300`: started 21:41:23, aborted 21:46:31 after 307 s, and the state
   file's mtime matches the log's final line. The tick-4 `json.dump(st, indent=2)`
   `TypeError` is gone — and was re-reproduced on a scratch path to prove the fixed
   form is the one that actually writes. **Keep checking the state mtime each
   tick; that is the receipt.**

## Operator note

Seven ticks and ~42h of continuous 502 is well past the point where this is a cron
problem, and it is now the fourth consecutive tick where the deliverable is
blocked on host state rather than anything this job can do. Repeated 502s from a
LiteSpeed origin with no partial responses, while Cloudflare still answers with
a real `CF-RAY`, usually means the origin is being OOM-killed or has run out of
disk — not that it is refusing connections. Worth checking the host's memory,
disk and PHP-FPM error log before the next tick. Nothing in this repository can
clear it.