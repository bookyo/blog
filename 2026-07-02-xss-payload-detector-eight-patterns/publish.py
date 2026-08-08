#!/usr/bin/env python3
"""Upload poster + cards to WordPress and create a published post."""
import sys, os, json, subprocess, time
from datetime import datetime, timezone

sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
import wp_post_audit as wpa

import requests

ARTICLE_DIR = '/Users/quyue/www/blog/2026-07-02-xss-payload-detector-eight-patterns'

session = requests.Session()
session.trust_env = False
auth = (wpa.DEFAULT_USER, wpa.DEFAULT_PASS)

MEDIA_FILES = [
    ('poster.png', 'XSS Payload Detector poster - 8 patterns'),
    ('card1.png', 'Critical XSS patterns'),
    ('card2.png', 'High risk XSS patterns'),
    ('card3.png', 'Medium risk XSS patterns'),
]

uploaded_ids = {}
for fname, desc in MEDIA_FILES:
    fpath = os.path.join(ARTICLE_DIR, fname)
    if not os.path.exists(fpath):
        print(f'  MISSING {fpath}')
        continue
    with open(fpath, 'rb') as f:
        data = f.read()
    r = session.post(
        f"{wpa.DEFAULT_WP_URL}/wp-json/wp/v2/media",
        auth=auth,
        headers={
            'Content-Type': 'image/png',
            'Content-Disposition': f'attachment; filename={fname}',
        },
        data=data,
        timeout=60,
    )
    if r.status_code not in (200, 201):
        print(f'  UPLOAD FAILED {fname}: HTTP {r.status_code} {r.text[:300]}')
        sys.exit(1)
    info = r.json()
    mid = info['id']
    uploaded_ids[fname] = mid
    print(f'  Uploaded {fname} -> media ID {mid}')

with open(os.path.join(ARTICLE_DIR, 'wp-media-ids.json'), 'w') as f:
    json.dump(uploaded_ids, f, indent=2)
print(f'Saved media IDs to wp-media-ids.json')

# Read article HTML
with open(os.path.join(ARTICLE_DIR, 'article.html')) as f:
    html_content = f.read()

# Build post
now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
print(f'Using date_gmt: {now_utc}')

# Replace image src with WordPress media URLs
# First, fetch media URLs for each uploaded ID
def get_media_url(mid):
    r = session.get(
        f"{wpa.DEFAULT_WP_URL}/wp-json/wp/v2/media/{mid}",
        auth=auth,
        timeout=30,
    )
    if r.status_code == 200:
        return r.json().get('source_url', '')
    return ''

url_map = {}
for fname, mid in uploaded_ids.items():
    url = get_media_url(mid)
    if url:
        url_map[fname] = url
        print(f'  Media URL: {fname} -> {url}')

# Replace in HTML
modified_html = html_content
for fname, url in url_map.items():
    modified_html = modified_html.replace(f'src="{fname}"', f'src="{url}"')

post_data = {
    'title': '8 Patterns That Make an XSS String',
    'slug': 'xss-payload-detector-the-eight-patterns',
    'status': 'publish',
    'content': modified_html,
    'date_gmt': now_utc,
    'featured_media': uploaded_ids.get('poster.png'),
}

r = session.post(
    f"{wpa.DEFAULT_WP_URL}/wp-json/wp/v2/posts",
    auth=auth,
    headers={'Content-Type': 'application/json'},
    json=post_data,
    timeout=30,
)
print(f'POST status: {r.status_code}')
if r.status_code not in (200, 201):
    print(f'  ERROR: {r.text[:500]}')
    sys.exit(1)

post = r.json()
post_id = post['id']
post_status = post['status']
post_link = post['link']
print(f'Post ID: {post_id}')
print(f'Status: {post_status}')
print(f'Link: {post_link}')

# If status is future (date_gmt got mangled), PATCH to publish
if post_status == 'future':
    r2 = session.post(
        f"{wpa.DEFAULT_WP_URL}/wp-json/wp/v2/posts/{post_id}",
        auth=auth,
        headers={'Content-Type': 'application/json'},
        json={'status': 'publish', 'date_gmt': now_utc},
        timeout=30,
    )
    print(f'PATCH status: {r2.status_code}')
    if r2.status_code in (200, 201):
        post = r2.json()
        post_status = post['status']
        print(f'After PATCH status: {post_status}')

# Save final post info
with open(os.path.join(ARTICLE_DIR, 'publish_summary.json'), 'w') as f:
    json.dump({
        'post_id': post_id,
        'status': post_status,
        'link': post_link,
        'date_gmt': now_utc,
        'title': post_data['title'],
        'slug': post_data['slug'],
        'media_ids': uploaded_ids,
        'media_urls': url_map,
    }, f, indent=2)
print(f'\nFinal post: {post_link}')