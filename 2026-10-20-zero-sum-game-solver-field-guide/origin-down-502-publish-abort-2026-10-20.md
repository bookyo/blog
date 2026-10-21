# Origin-down (Cloudflare 502) aborts a publish run — build locally, park a driver

**Date:** 2026-10-20, cron publish tick (~04:36–05:15 UTC)
**Outcome:** 0 posts published. Article + 4 assets fully built, verified, archived, and parked for the next run.

## The failure class

Distinct from the Cycle #54 (2026-10-02) SSL-EOF class. That one is a **poisoned connection pool with the origin healthy** — swap the transport to curl and it clears. This one is the **origin genuinely down**:

```
HTTP/1.1 502 Bad Gateway
Server: cloudflare
CF-RAY: a4d554e79b81feb5-AMS
```

Returned on EVERY route — frontend, `/wp-json/wp/v2/posts`, with and without auth — while unrelated hosts returned 200.

## Diagnostic that distinguishes the two classes

```bash
curl -s -m 15 --http1.1 -o /dev/null -w "%{http_code}\n" https://blog.flowrust.com/   # 502 = origin down
curl -s -m 15 --http1.1 -o /dev/null -w "%{http_code}\n" https://example.com/          # 200 = local network fine
curl -s -m 15 --http1.1 -I https://blog.flowrust.com/ | grep -iE 'cf-ray|server'       # Server: cloudflare => edge reached, origin refused
```

Neither 5x retry-exponential-backoff (Cycle #54) nor `--http1.1` (Cycle #95) helps. There is nothing to retry against. Retrying 5x with 4s backoff burned 2 minutes before the pattern was clear.

Intermittent `000` codes appeared alongside the 502s on this run — that is local network flakiness layered on top, not a different failure. `example.com` returning 200 at the same moment is what rules out local network as the primary cause.

## Do not burn the tick re-fetching

Build everything locally first, then start a parked driver that polls every 15s and publishes the instant HTTP 200 returns. A 35-minute outage then costs zero rework.

Pipeline order that makes this possible:

1. Build dedup set (state file + `~/www/blog/` archive dirs, every hyphen-prefixed segment expanded)
2. Pick tool (theme scoring, avoid recent clusters)
3. Write article **and numerically verify its worked examples** (see below)
4. Render 4 assets + `vision_analyze` each one
5. `validate_alysia_anchors` / `validate_anchors`
6. `build_body` with all pre-POST assertions
7. `audit_post_content` -> 0 findings
8. THEN start the parked driver
9. Archive to `~/www/blog/YYYY-MM-DD-<slug>/` so the next tick inherits the work

## ⚠️ A curl wrapper MUST pass `-w '\n%{http_code}'`

A helper that omits `-w` returns `(body, '')`. Then `wait_for_origin`'s `if code == '200'` is never true and the driver polls forever printing `probe N:` with a **blank status** rather than `probe N: 502`. The blank column is the tell.

```python
def curl(args, timeout=60):
    p = subprocess.run(['curl', '-sS', '-m', str(timeout), '--http1.1',
                        '-w', '\n%{http_code}'] + args,
                       capture_output=True, text=True)
    out = p.stdout
    m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    code = m[-1] if m else ''
    return re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE).strip(), code
```

Put `-w` in the helper itself so every call site inherits it. Verify in isolation before parking a long-running driver:

```python
b, c = curl(['-u', f'{USER}:{PWD}', f'{WP}/wp-json/wp/v2/posts?per_page=1'])
assert c != '', 'curl helper is missing -w %http_code'
```

## Pre-POST numerical verification of worked examples

For any tool article whose claims are computable — game theory, thermodynamics, DSP, finance, bio — assert the numbers with numpy BEFORE POSTing. The draft ships verbatim and a wrong worked example is a permanent defect that **no audit catches**.

On this run, verification caught three real errors in the first draft:

1. **Inverted saddle-cell definition.** For a row-maximiser, an equilibrium cell is the largest entry in its **column** and the smallest entry in its **row** — the draft had it backwards, and asserted "a cell that is largest in its row is an equilibrium candidate".
2. **Wrong column maxima.** Draft claimed column maxima `[0, 1, 2]`; actual was `[0, 0, 2]` after the perturbation.
3. **A "pure equilibrium exists" claim on a matrix that had none.** The perturbed 3x3 has maximin -1 vs minimax 0 — a gap of one, so pure play is impossible.

`audit_post_content` returned **0 findings** on all three.

Recipe (~60 lines, <2 seconds):

```python
row_min = A.min(axis=1); maximin = row_min.max()
col_max = A.max(axis=0); minimax = col_max.min()
saddles = [(i, j) for i in range(n) for j in range(m)
           if abs(A[i][j] - A[:, j].max()) < 1e-12 and abs(A[i][j] - A[i].min()) < 1e-12]
# mixed equilibrium by grid search over the simplex, both players
# shift invariance: value(A + K) - value(A) == K exactly, mixes unchanged
```

Print each computed value next to the corresponding sentence in the draft and diff them by eye. This run's verified facts that ended up in the article:

- A1 `[[0,1,2],[-1,0,1],[-2,-1,0]]`: maximin 0, minimax 0 -> pure equilibrium exists
- A2 (Mid/Low flipped to -1): maximin -1, minimax 0 -> mixed only, value -0.5, both mixes `(0.5, 0.5, 0)`
- Shift K=3 (min entry -2): value -0.5 -> 2.5, delta exactly 3, mixes identical

## PIL defects found by vision_analyze (both fixed pre-POST)

### 5-tile label width: measure against `tile_w - 20`, not the canvas

`render_card_5tile` centres the label at `F_MED` and **nothing clips it**. A 259px label in a 290px tile renders without error and passes `img.size` and `os.path.getsize` — but leaves a 15px gutter that reads as "touching the tile border".

Measure and shorten:

```python
pil.text_w(d, 'ROW GUARANTEE', pil.F_MED)   # 259px  -> too tight on a 290px tile
pil.text_w(d, 'ROW FLOOR', pil.F_MED)       # 181px  -> clean
```

Same instinct as the WP 6390 poster-subtitle 65-char threshold: invisible to every programmatic check, so measure it and look at the render.

### 2-col cards: fill the panels

`render_card_input_output_2col` uses `col_h=580` with ~13 row slots at 36px line height. Five rows per side leaves a conspicuous dead band under the text. **Nine rows per side** balances the layout with no overflow (widest row 337px against the 640px `col_w - 60` limit).

Row-width rule (WP 6358) held: keep every row at F_MONO `<= 30 chars`.

## Also hit this run

- `\uXXXX` escapes written via `write_file` arrive as **literal two-character strings**, so `ord('\u2460')` raises `TypeError: ord() expected a character, but string of length 2 found`. Use `chr(0x00B7)` / integer codepoint ranges instead. Affects the tofu pre-flight scan in the PIL generator.
- `importlib` loading of `templates/render_card_4tile_compact.py` and `templates/custom_pil_card_layouts.py` fails with `No module named 'pil_poster_and_cards_network_theme'` — they import the base module by bare name. Fix: `sys.path.insert(0, f'{SKILL}/templates')` **before** loading.
- `scripts/insert_highlight_cards.py::insert_highlight_cards()` returns a plain `str` (WP 6390 lesson) — do NOT tuple-unpack it.
- `sample-manifest.json` still has no `toolId` field (WP 6116 + 6390, 3rd confirmation). Keyword matching returns only noise (`operations`, `security`). Skip the samples-link recipe entirely; tool anchors only.
- `nohup ... &` in a foreground terminal call is rejected — use `terminal(background=true)`.
- `process(action='poll')` requires `session_id`, not `subagent_id`.