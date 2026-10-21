#!/usr/bin/env python3
"""Parked publish driver: polls until origin returns, then uploads + publishes.

Per references/origin-down-502-publish-abort-2026-10-20.md:
  - curl helper MUST pass -w '\\n%{http_code}' or code is always blank
  - POST (not PATCH) for post updates
  - featured_media MUST be 0
  - substitute full source_url to preserve /uploads/YYYY/MM/ prefix
"""
import json, os, re, subprocess, sys, time

USER = 'bted2k@gmail.com'
PWD = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
WP = 'https://blog.flowrust.com'
STATE = '/tmp/wp_r1/publish_state.json'
ASSETS = '/tmp/wp_r1/assets'
BODY = open('/tmp/wp_r1/body_final.html').read()
META = json.load(open('/tmp/wp_r1/post_meta.json'))
LOG = '/tmp/wp_r1/driver.log'


def log(msg):
    line = f'[{time.strftime("%H:%M:%S")}] {msg}'
    print(line, flush=True)
    with open(LOG, 'a') as f:
        f.write(line + '\n')


def curl(args, timeout=60):
    """Returns (body, code). The -w flag lives INSIDE the helper (origin-down lesson)."""
    p = subprocess.run(['curl', '-sS', '-m', str(timeout), '--http1.1',
                        '-w', '\n%{http_code}'] + args,
                       capture_output=True, text=True)
    out = p.stdout or ''
    m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    code = m[-1] if m else ''
    return re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE).strip(), code


def save_state(**kw):
    st = {}
    if os.path.exists(STATE):
        st = json.load(open(STATE))
    st.update(kw)
    # json.dump needs (obj, fp). Passing only indent= wrote nothing and raised
    # TypeError, killing the abort path exactly when a record matters most.
    with open(STATE, 'w') as f:
        json.dump(st, f, indent=2)
    return st


def origin_up(attempts=1):
    for _ in range(attempts):
        b, c = curl(['-u', f'{USER}:{PWD}',
                     f'{WP}/wp-json/wp/v2/posts?per_page=1&_fields=id'])
        if c == '200':
            return True
    return False


def upload(path, filename):
    """3-retry exponential backoff per WP 5683/5738 SSL-EOF lesson."""
    last = ''
    for attempt in range(3):
        cmd = ['curl', '-sS', '-m', '90', '--http1.1',
               '-u', f'{USER}:{PWD}', '-X', 'POST',
               f'{WP}/wp-json/wp/v2/media',
               '-H', f'Content-Disposition: attachment; filename={filename}',
               '-F', f'file=@{path};type=image/png',
               '-w', '\n%{http_code}']
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = p.stdout or ''
        m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
        code = m[-1] if m else ''
        payload = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE).strip()
        if code in ('200', '201'):
            return json.loads(payload)
        last = f'{code} {payload[:200]}'
        log(f'  upload {filename} attempt {attempt + 1} failed: {last}')
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f'upload failed for {filename}: {last}')


def main():
    wait_secs = int(os.environ.get('WAIT_SECS', '600'))
    log(f'driver start; will wait up to {wait_secs}s for origin')

    # NOTE: wait on REAL elapsed time. A counter incremented per-iteration with a
    # sleep only every Nth iteration under-waits badly (900 "s" was ~225 s real).
    deadline = time.monotonic() + wait_secs
    start = time.monotonic()
    reported = 0
    while True:
        if origin_up():
            log(f'origin is UP after {int(time.monotonic() - start)}s')
            break
        if time.monotonic() >= deadline:
            log(f'origin never recovered within {wait_secs}s real -- aborting, nothing published')
            save_state(status='aborted_origin_still_down', published=False,
                       waited_real=int(time.monotonic() - start))
            return 2
        time.sleep(15)
        elapsed = int(time.monotonic() - start)
        if elapsed - reported >= 60:
            reported = elapsed
            log(f'  still down after {elapsed}s')

    # ---- uploads ----
    slots = [('POSTER_URL', f'{ASSETS}/poster.png', 'poster.png'),
             ('CARD1_URL', f'{ASSETS}/card1.png', 'card1.png'),
             ('CARD2_URL', f'{ASSETS}/card2.png', 'card2.png'),
             ('CARD3_URL', f'{ASSETS}/card3.png', 'card3.png')]
    urls = {}
    for slot, path, fname in slots:
        data = upload(path, fname)
        su = data['source_url']
        urls[slot] = su
        log(f'  uploaded {fname} -> id={data["id"]} {su}')

    body = BODY
    for slot, url in urls.items():
        body = body.replace(slot, url)

    # WP 6191/6197: substitute the FULL source_url (preserves /uploads/YYYY/MM/)
    for slot in urls:
        assert slot not in body, f'placeholder leak: {slot}'
    n_cards = len(re.findall(r'<figure class="highlight-card">', body))
    assert n_cards == 3, f'card count {n_cards} != 3 after substitution'
    log(f'  substitution verified: 0 placeholders left, {n_cards} card figures')

    # date_gmt is computed at POST time, not at park time: if the origin takes an
    # hour to come back, a date_gmt captured at park time would post a stale hour.
    dg = os.environ.get('DATE_GMT', 'NOW')
    if dg == 'NOW':
        dg = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    log(f'  date_gmt at publish time: {dg}')
    payload = {
        'title': META['title'],
        'slug': META['slug'],
        'content': body,
        'status': 'publish',
        'featured_media': 0,
        'date_gmt': dg,
    }
    json.dump(payload, open('/tmp/wp_r1/payload.json', 'w'))

    p = subprocess.run(['curl', '-sS', '-m', '90', '--http1.1',
                        '-u', f'{USER}:{PWD}', '-X', 'POST',
                        f'{WP}/wp-json/wp/v2/posts',
                        '-H', 'Content-Type: application/json',
                        '--data-binary', '@/tmp/wp_r1/payload.json',
                        '-w', '\n%{http_code}'],
                       capture_output=True, text=True)
    out = p.stdout or ''
    m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    code = m[-1] if m else ''
    resp = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE).strip()
    log(f'  POST /wp/v2/posts -> {code}')
    if code not in ('200', '201'):
        log(f'  FAILED: {resp[:400]}')
        save_state(status='post_failed', code=code, response=resp[:2000])
        return 1

    post = json.loads(resp)
    pid = post['id']
    log(f'  PUBLISHED id={pid} status={post.get("status")} link={post.get("link")}')

    # cron prompt step 6: force publish if it landed as future
    if post.get('status') != 'publish':
        b2, c2 = curl(['-u', f'{USER}:{PWD}', '-X', 'POST',
                       f'{WP}/wp-json/wp/v2/posts/{pid}',
                       '-H', 'Content-Type: application/json',
                       '-d', json.dumps({'status': 'publish'})])
        log(f'  force-publish POST -> {c2} status={json.loads(b2).get("status") if c2=="200" else "?"}')
        post = json.loads(b2)

    save_state(status='published', published=True, post_id=pid,
               link=post.get('link'), urls=urls,
               featured_media=post.get('featured_media'))
    log('driver complete')
    return 0


if __name__ == '__main__':
    sys.exit(main())