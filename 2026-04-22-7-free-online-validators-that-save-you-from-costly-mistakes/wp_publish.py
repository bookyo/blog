#!/usr/bin/env python3
"""Publish: 7 Free Online Validators That Save You From Costly Mistakes"""
import json
import urllib.request
import urllib.error
import base64
import re
import sys

# Read article
article_path = '/Users/quyue/www/blog/2026-04-22-7-free-online-validators-that-save-you-from-costly-mistakes/article.md'
with open(article_path, 'r') as f:
    raw = f.read()

# Strip frontmatter (lines between --- markers at top)
if raw.startswith('---'):
    parts = raw.split('---', 2)
    raw = parts[2].strip()

lines = raw.strip().split('\n')
title = lines[0].strip() if lines else 'Untitled'
body_lines = lines[1:]

# Convert markdown to HTML
content = '\n'.join(body_lines)
content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
paras = content.split('\n\n')
content = '</p><p>'.join(paras)
content = '<p>' + content + '</p>'
content = re.sub(r'<p>(<h[123]>.*?</h[123]>)</p>', r'\1', content)
content = re.sub(r'(<h[123]>.*?</h[123]>)<br><br>', r'\1', content)
content = re.sub(r'<br><p>', r'<p>', content)
content = re.sub(r'</p><br>', r'</p>', content)

slug = "7-free-online-validators-that-save-you-from-costly-mistakes"
password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
credentials = f"bted2k@gmail.com:{password}"
auth = base64.b64encode(credentials.encode()).decode()

print(f"Title: {title}")
print(f"Slug: {slug}")

# Step 1: Upload poster as media
poster_path = '/Users/quyue/www/blog/2026-04-22-7-free-online-validators-that-save-you-from-costly-mistakes/poster.png'
with open(poster_path, 'rb') as f:
    image_data = f.read()

media_url = "https://blog.flowrust.com/wp-json/wp/v2/media"
media_req = urllib.request.Request(media_url, data=image_data, method='POST')
media_req.add_header('Content-Type', 'image/png')
media_req.add_header('Authorization', 'Basic ' + auth)
media_req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
media_req.add_header('Content-Disposition', 'attachment; filename="poster.png"')

try:
    with urllib.request.urlopen(media_req, timeout=30) as resp:
        media_result = json.loads(resp.read().decode())
        media_id = media_result.get('id')
        media_url_ret = media_result.get('source_url')
        print(f'Media uploaded! ID: {media_id}, URL: {media_url_ret}')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'Media upload HTTP {e.code}: {body[:500]}')
    sys.exit(1)
except Exception as ex:
    print(f'Media upload exception: {ex}')
    sys.exit(1)

# Step 2: Create post
post_url = "https://blog.flowrust.com/wp-json/wp/v2/posts"
post_data = json.dumps({
    "title": title,
    "content": content,
    "status": "publish",
    "slug": slug,
    "date": "2026-04-22T09:20:00",
    "featured_media": media_id
}).encode()

post_req = urllib.request.Request(post_url, data=post_data, method='POST')
post_req.add_header('Content-Type', 'application/json')
post_req.add_header('Authorization', 'Basic ' + auth)
post_req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(post_req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        post_id = result.get('id')
        post_url_ret = result.get('link')
        print(f'Post published! ID: {post_id}')
        print(f'URL: {post_url_ret}')

        # Write to publish log
        log_entry = f"""
## 2026-04-22 09:20 UTC — {title}
- **WP Post ID**: {post_id}
- **WP URL**: {post_url_ret}
- **Featured Image**: poster (WP ID {media_id})
- **Highlight Cards**: none
- **Slug**: {slug}
- **Tools**: credit-card-validator, iban-swift-validator, eu-vat-validator, btc-address-validator, eth-address-validator, vin-validator, global-postal-code-validator
- **Category**: Validation / Security
- **Asset Dir**: /Users/quyue/www/blog/2026-04-22-7-free-online-validators-that-save-you-from-costly-mistakes
"""
        with open('/Users/quyue/www/blog/publish-log.md', 'a') as f:
            f.write(log_entry)
        print('Publish log updated.')

except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'Post creation HTTP {e.code}: {body[:500]}')
    sys.exit(1)
except Exception as ex:
    print(f'Post creation exception: {ex}')
    sys.exit(1)
