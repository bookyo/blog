"""Cron publish driver — WP post + 4 media uploads, with retry.

Transport: curl subprocess (Cycle #54 lesson — requests/urllib3 can die with
SSL EOF on the LiteSpeed edge; curl is the fallback transport).
Credentials: canonical from scripts/wp_post_audit.py (WP 6135 lesson — the
cron-prompt inline creds return 401 rest_cannot_create on POST).
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone

WP = 'https://blog.flowrust.com'
USER = 'bted2k@gmail.com'
PWD = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
ASSETS = '/tmp/wp_assets'
BODY_FILE = '/tmp/wp_run103/article_body.html'

TITLE = ('Zero-Sum Game Solver Field Guide: When Pure Play Fails, '
         'Mixing Is the Only Answer')
EXCERPT = ('Saddle points, shifted simplex, and verified equilibria: how a '
           'saddle-point test decides whether a payoff matrix has a pure '
           'answer, and how one simplex pass returns both players.')


def curl(args, timeout=60):
    """Run curl and return (body, http_code)."""
    p = subprocess.run(['curl', '-sS', '-m', str(timeout), '--http1.1',
                        '-w', '\n%{http_code}'] + args,
                       capture_output=True, text=True)
    out = p.stdout
    code = ''
    m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    if m:
        code = m[-1]
        out = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE)
    return out.strip(), code, p.stderr.strip()


def wait_for_origin(attempts=120, sleep=15):
    print('waiting for origin to return 200 ...', flush=True)
    for i in range(attempts):
        _, code, _ = curl(['-u', f'{USER}:{PWD}',
                           f'{WP}/wp-json/wp/v2/posts?per_page=1&_fields=id'], timeout=30)
        print(f'  probe {i+1}: {code}', flush=True)
        if code == '200':
            print('  ORIGIN UP', flush=True)
            return True
        time.sleep(sleep)
    return False


def upload(slot, filename):
    path = f'{ASSETS}/{slot}.png'
    for attempt in range(1, 4):
        cmd = ['curl', '-sS', '-m', '90', '--http1.1',
               '-u', f'{USER}:{PWD}',
               '-X', 'POST',
               '-H', f'Content-Disposition: attachment; filename={filename}',
               '-F', f'file=@{path};type=image/png',
               f'{WP}/wp-json/wp/v2/media',
               '-w', '\n%{http_code}']
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = p.stdout.strip()
        code = ''
        m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
        if m:
            code = m[-1]
            out = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE)
        print(f'  {slot} -> {filename} attempt {attempt}: HTTP {code}', flush=True)
        if code in ('200', '201'):
            d = json.loads(out)
            return d['id'], d['source_url']
        if code == '401':
            print('  *** 401 rest_cannot_create — credentials rejected ***', flush=True)
            return None, None
        time.sleep(3 * attempt)
    return None, None


def main():
    if not wait_for_origin():
        print('ORIGIN NEVER RECOVERED — aborting, nothing published')
        return 1

    body = open(BODY_FILE).read()

    print('uploading assets ...', flush=True)
    urls = {}
    for slot, filename in [('poster', 'zero-sum-game-solver-poster.png'),
                           ('card1', 'zero-sum-game-solver-card1-saddle-test.png'),
                           ('card2', 'zero-sum-game-solver-card2-one-solve.png'),
                           ('card3', 'zero-sum-game-solver-card3-six-lines.png')]:
        mid, url = upload(slot, filename)
        if not url:
            print(f'  FAILED to upload {slot} — aborting')
            return 1
        urls[slot] = url
        print(f'  {slot}: id={mid} {url}', flush=True)

    # substitute using the FULL source_url so the /uploads/YYYY/MM/ prefix survives
    for ph, slot in [('POSTER_URL', 'poster'), ('CARD1_URL', 'card1'),
                     ('CARD2_URL', 'card2'), ('CARD3_URL', 'card3')]:
        assert ph in body, f'placeholder {ph} missing'
        body = body.replace(ph, urls[slot])
    assert 'POSTER_URL' not in body and 'CARD1_URL' not in body, 'placeholder leak'
    print('  URL substitution complete, no placeholders left', flush=True)

    date_gmt = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    print('date_gmt:', date_gmt, flush=True)

    payload = {
        'title': TITLE,
        'excerpt': EXCERPT,
        'content': body,
        'status': 'publish',
        'date_gmt': date_gmt,
        'featured_media': 0,          # WP 5628 — COSESAI hero duplication
        'categories': [],
    }
    json.dump(payload, open('/tmp/wp_run103/payload.json', 'w'))
    json.dump(urls, open('/tmp/wp_run103/uploaded.json', 'w'), indent=1)

    cmd = ['curl', '-sS', '-m', '120', '--http1.1',
           '-u', f'{USER}:{PWD}',
           '-X', 'POST',
           '-H', 'Content-Type: application/json',
           '--data-binary', '@/tmp/wp_run103/payload.json',
           f'{WP}/wp-json/wp/v2/posts',
           '-w', '\n%{http_code}']
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout.strip()
    code = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    code = code[-1] if code else ''
    out = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE)
    print('POST /wp/v2/posts -> HTTP', code, flush=True)

    if code not in ('200', '201'):
        print('CREATE FAILED:', out[:800])
        return 1

    post = json.loads(out)
    pid = post['id']
    print('published id:', pid, flush=True)
    print('link:', post['link'], flush=True)
    print('status:', post['status'], flush=True)
    print('date_gmt:', post['date_gmt'], flush=True)
    print('featured_media:', post.get('featured_media'), flush=True)

    # Step 2 of the two-step publish: force publish if WP returned 'future'
    if post['status'] != 'publish':
        print('status was not publish -> forcing', flush=True)
        cmd = ['curl', '-sS', '-m', '60', '--http1.1',
               '-u', f'{USER}:{PWD}', '-X', 'POST',
               '-H', 'Content-Type: application/json',
               '--data-binary', '{"status":"publish"}',
               f'{WP}/wp-json/wp/v2/posts/{pid}',
               '-w', '\n%{http_code}']
        p = subprocess.run(cmd, capture_output=True, text=True)
        o2 = p.stdout.strip()
        c2 = re.findall(r'^(\d{3})\s*$', o2, flags=re.MULTILINE)
        print('force-publish -> HTTP', c2[-1] if c2 else '?')
        post = json.loads(re.sub(r'^\d{3}\s*$', '', o2, flags=re.MULTILINE))

    json.dump({'id': pid, 'link': post['link'], 'date_gmt': post['date_gmt'],
               'status': post['status'], 'urls': urls},
              open('/tmp/wp_run103/published.json', 'w'), indent=1)
    print('DONE', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())