#!/usr/bin/env python3.11
"""Upload 4 assets + publish post to WordPress."""
import sys, os, json, time, urllib.request, urllib.error, base64
from datetime import datetime, timezone

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
ASSETS_DIR = '/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/assets'
HTML_IN = '/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_final.html'

# Build auth header (avoid Bash quoting issues)
basic = base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
AUTH = f'Basic {basic}'

# === Step 1: Upload 4 assets with retry on SSL EOF ===
def upload_media(filepath, filename):
    for attempt in range(3):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            boundary = '----WPFormFillBoundaryJarvis'
            parts = []
            parts.append(f'--{boundary}'.encode())
            parts.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
            parts.append(b'Content-Type: image/png')
            parts.append(b'')
            parts.append(data)
            parts.append(f'--{boundary}--'.encode())
            parts.append(b'')
            body = b'\r\n'.join(parts)
            req = urllib.request.Request(
                f'{WP_URL}/wp-json/wp/v2/media',
                data=body,
                method='POST',
                headers={
                    'Authorization': AUTH,
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'Content-Disposition': f'attachment; filename={filename}',
                    'User-Agent': 'Jarvis-Cron/1.0',
                }
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.loads(r.read().decode())
            return resp
        except (urllib.error.URLError, Exception) as e:
            if attempt == 2:
                raise
            print(f'  retry {attempt+1} after error: {e}')
            time.sleep(2 * (attempt + 1))

print('Uploading 4 assets...')
uploaded = {}
for slot, filename in [
    ('poster', 'poster.png'),
    ('card1', 'card1.png'),
    ('card2', 'card2.png'),
    ('card3', 'card3.png'),
]:
    path = f'{ASSETS_DIR}/{filename}'
    print(f'  uploading {filename}...')
    resp = upload_media(path, filename)
    uploaded[slot] = {'id': resp['id'], 'url': resp['source_url']}
    print(f'    id={resp["id"]} url={resp["source_url"]}')

# === Step 2: Substitute placeholders in HTML ===
html = open(HTML_IN).read()
for slot, info in uploaded.items():
    html = html.replace(f'PLACEHOLDER_{slot}.png', info['url'])

# Save substituted HTML for archive
open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_published.html', 'w').write(html)

# === Step 3: Verify no PLACEHOLDER remains ===
assert 'PLACEHOLDER' not in html, 'PLACEHOLDER leak!'
print('PLACEHOLDER check: OK')

# === Step 4: Publish post ===
TITLE = 'PDF Form Fill Batch — Field Guide: When One Template + One JSON Array Beats a Hundred Hand-Edits'
SLUG = 'pdf-form-fill-batch-field-guide-when-one-template-one-json-array-beats-a-hundred-hand-edits'

now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

payload = {
    'title': TITLE,
    'slug': SLUG,
    'status': 'publish',
    'date_gmt': now_utc,
    'featured_media': 0,
    'content': html,
    'excerpt': 'PDF Form Fill Batch fills one AcroForm template with an array of records and returns a ZIP of PDFs or one merged PDF — every fresh template load prevents cross-record contamination.',
}

print(f'\nPublishing post: {TITLE}')
print(f'date_gmt: {now_utc}')
print(f'content length: {len(html)}')

req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts',
    data=json.dumps(payload).encode(),
    method='POST',
    headers={
        'Authorization': AUTH,
        'Content-Type': 'application/json',
        'User-Agent': 'Jarvis-Cron/1.0',
    }
)

with urllib.request.urlopen(req, timeout=60) as r:
    resp = json.loads(r.read().decode())

post_id = resp['id']
post_link = resp['link']
post_status = resp['status']
post_date_gmt = resp['date_gmt']
print(f'\n=== POSTED ===')
print(f'id: {post_id}')
print(f'link: {post_link}')
print(f'status: {post_status}')
print(f'date_gmt: {post_date_gmt}')

# === Step 5: If status=future, force to publish ===
if post_status == 'future':
    print('Status is future — forcing to publish via POST update...')
    payload2 = dict(payload)
    payload2['status'] = 'publish'
    req2 = urllib.request.Request(
        f'{WP_URL}/wp-json/wp/v2/posts/{post_id}',
        data=json.dumps(payload2).encode(),
        method='POST',
        headers={
            'Authorization': AUTH,
            'Content-Type': 'application/json',
            'User-Agent': 'Jarvis-Cron/1.0',
        }
    )
    with urllib.request.urlopen(req2, timeout=60) as r:
        resp2 = json.loads(r.read().decode())
    print(f'After force-publish: status={resp2["status"]}, date_gmt={resp2["date_gmt"]}')

# === Step 6: Save post info for archive ===
post_info = {
    'id': post_id,
    'link': post_link,
    'slug': SLUG,
    'title': TITLE,
    'date_gmt': now_utc,
    'assets': uploaded,
    'covered_slug': 'pdf-form-fill-batch',
}
open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/post_info.json', 'w').write(json.dumps(post_info, indent=2))
print('\nSaved post_info.json')
print(f'\nDONE — post URL: {post_link}')