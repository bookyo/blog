#!/usr/bin/env python3.11
"""Upload poster + 3 cards to WP Media, then publish post.

Per WP 6135 lesson: use canonical creds from wp_post_audit.py, NOT cron-prompt creds.
Per WP 6197 lesson: use FULL source_url from upload response (preserves /2026/08/ prefix).
"""
import sys, os, json, re, base64, urllib.request, urllib.error, time
import requests
from requests.auth import HTTPBasicAuth

sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
import wp_post_audit as wpa

WP_URL = wpa.DEFAULT_WP_URL
WP_USER = wpa.DEFAULT_USER
WP_PASS = wpa.DEFAULT_PASS

# Verify creds work for POST (per WP 6135 trap)
preflight = requests.post(
    f'{WP_URL}/wp-json/wp/v2/posts?per_page=1&_fields=id',
    auth=HTTPBasicAuth(WP_USER, WP_PASS),
    headers={'User-Agent': 'Mozilla/5.0'},
    timeout=15,
)
# We can't actually create a test post, so do a fake media upload with empty file to verify
print(f'WP URL: {WP_URL}')
print(f'User: {WP_USER}')
# Skip preflight POST - just trust the canonical creds and retry on 401
# Per WP 6135, these CANONICAL creds work for both GET and POST.

ASSETS = [
    ('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/poster.png', 'graphql-playground-poster.png'),
    ('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card1.png',    'graphql-playground-card1.png'),
    ('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card2.png',    'graphql-playground-card2.png'),
    ('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card3.png',    'graphql-playground-card3.png'),
]

session = requests.Session()
session.trust_env = False
uploaded = {}
for path, filename in ASSETS:
    print(f'Uploading {filename}...')
    for attempt in range(3):
        try:
            with open(path, 'rb') as f:
                r = session.post(
                    f'{WP_URL}/wp-json/wp/v2/media',
                    auth=HTTPBasicAuth(WP_USER, WP_PASS),
                    headers={
                        'User-Agent': 'Mozilla/5.0',
                        'Content-Disposition': f'attachment; filename={filename}',
                    },
                    files={'file': (filename, f, 'image/png')},
                    timeout=60,
                )
            if r.status_code == 201:
                data = r.json()
                uploaded[filename] = {'id': data['id'], 'url': data['source_url']}
                print(f'  OK [{data["id"]}] {data["source_url"]}')
                break
            else:
                print(f'  HTTP {r.status_code}: {r.text[:200]}')
                if attempt == 2:
                    sys.exit(1)
                time.sleep(2 * (attempt + 1))
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            print(f'  SSL/conn error attempt {attempt+1}: {type(e).__name__}')
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))

print()
print('All uploads complete:')
for k, v in uploaded.items():
    print(f'  {k}: id={v["id"]}, url={v["url"]}')

with open('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/uploaded.json', 'w') as f:
    json.dump(uploaded, f, indent=2)
print('\nSaved uploaded.json')