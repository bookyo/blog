#!/usr/bin/env python3
"""Publish: Solstice & Equinox Calculator article"""
import json
import urllib.request
import urllib.error
import base64
import re

# Read article
article_path = '/Users/quyue/www/blog/2026-04-23-solstice-equinox-calculator/article.md'
with open(article_path, 'r') as f:
    raw = f.read()

# Strip frontmatter
if raw.startswith('---'):
    parts = raw.split('---', 2)
    raw = parts[2].strip()

lines = raw.strip().split('\n')
title = lines[0].strip() if lines else 'Untitled'
body_lines = lines[1:]

# Convert markdown to HTML
content = '\n'.join(body_lines)
# Images first
content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', content)
# Headers
content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
# Bold
content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
# Links
content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
# HR
content = re.sub(r'^---$', '<hr/>', content, flags=re.MULTILINE)
# Tables - convert to HTML table
table_lines = []
in_table = False
table_html = ''
for line in content.split('\n'):
    if '|' in line and line.strip().startswith('|'):
        if not in_table:
            in_table = True
            table_html = '<table>'
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        if all(c.replace('-','').replace(':','').replace(' ','') == '' for c in cols):
            # header separator - skip
            continue
        is_header = all(c.replace('-','').replace(':','').replace(' ','') != '' for c in cols)
        tag = 'th' if is_header else 'td'
        table_html += '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cols) + '</tr>'
    else:
        if in_table:
            table_html += '</table>'
            content = content.replace(table_html.replace('<table>', '').replace('</table>', ''), table_html)
            table_html = ''
            in_table = False
if in_table:
    table_html += '</table>'
    content = content.replace(table_html.replace('<table>', '').replace('</table>', ''), table_html)

# Paragraphs
paras = []
for block in re.split(r'\n\n+', content):
    block = block.strip()
    if not block:
        continue
    if block.startswith('<h') or block.startswith('<pre') or block.startswith('<hr') or block.startswith('<ul') or block.startswith('<ol') or block.startswith('<img') or block.startswith('<table'):
        paras.append(block)
    else:
        block = re.sub(r'(?<!\n)\n(?!\n)', '<br/>', block)
        paras.append(f'<p>{block}</p>')
content = '\n'.join(paras)

slug = "solstice-equinox-calculator-why-it-should-be-your-new-favorite-astronomy-tool"
password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
credentials = f"bted2k@gmail.com:{password}"
auth = base64.b64encode(credentials.encode()).decode()

print(f"Title: {title}")
print(f"Slug: {slug}")

# Step 1: Upload poster
poster_path = '/Users/quyue/www/blog/2026-04-23-solstice-equinox-calculator/poster.png'
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
    raise
except Exception as ex:
    print(f'Media upload exception: {ex}')
    raise

# Step 2: Create post
post_url = "https://blog.flowrust.com/wp-json/wp/v2/posts"
post_data = json.dumps({
    "title": title,
    "content": content,
    "status": "publish",
    "slug": slug,
    "date_gmt": "2026-04-23T09:30:00",
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
        post_status = result.get('status')
        print(f'Post created! ID: {post_id}, Status: {post_status}')
        print(f'URL: {post_url_ret}')

        if post_status == 'future':
            print("Status is future, patching to publish...")
            update_data = json.dumps({
                "status": "publish",
                "date_gmt": "2026-04-23T09:30:00"
            }).encode()
            update_req = urllib.request.Request(f"{post_url}/{post_id}", data=update_data, method='POST')
            update_req.add_header('Content-Type', 'application/json')
            update_req.add_header('Authorization', 'Basic ' + auth)
            update_req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            with urllib.request.urlopen(update_req, timeout=30) as resp2:
                result2 = json.loads(resp2.read().decode())
                print(f"Patched! Final status: {result2.get('status')}, URL: {result2.get('link')}")

        # Write to publish log
        log_entry = f"""
## 2026-04-23 09:30 UTC — {title}
- **WP Post ID**: {post_id}
- **WP URL**: {post_url_ret}
- **Featured Image**: poster (WP ID {media_id})
- **Highlight Cards**: none
- **Slug**: {slug}
- **Tools Featured**: solstice-equinox
- **Category**: Astronomy
- **Asset Dir**: /Users/quyue/www/blog/2026-04-23-solstice-equinox-calculator
"""
        with open('/Users/quyue/www/blog/publish-log.md', 'a') as f:
            f.write(log_entry)
        print('Publish log updated.')

except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'Post creation HTTP {e.code}: {body[:500]}')
    raise
except Exception as ex:
    print(f'Post creation exception: {ex}')
    raise
