#!/usr/bin/env python3.11
"""Upload poster + 3 cards to WP Media for drag-force-calculator article."""
import sys, os, json, time
import requests
from requests.auth import HTTPBasicAuth

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'

ASSETS = [
    ('/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide/poster.png', 'drag-force-calculator-poster.png'),
    ('/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide/card1.png',    'drag-force-calculator-card1.png'),
    ('/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide/card2.png',    'drag-force-calculator-card2.png'),
    ('/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide/card3.png',    'drag-force-calculator-card3.png'),
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

with open('/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide/uploaded.json', 'w') as f:
    json.dump(uploaded, f, indent=2)
print('\nSaved uploaded.json')
