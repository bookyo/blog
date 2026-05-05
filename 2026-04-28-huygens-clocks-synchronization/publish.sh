#!/bin/bash
# Upload poster and create WordPress post for Huygens Clocks article
set -e

WORKDIR="/Users/quyue/www/blog/2026-04-28-huygens-clocks-synchronization"
WP_URL="https://blog.flowrust.com"
CREDS="bted2k@gmail.com:zVlf aCkm vB79 GjXc zVrJ dSuH"

echo "=== Step 1: Get latest post date ==="
curl -s -u "$CREDS" \
  "$WP_URL/wp-json/wp/v2/posts?per_page=1&orderby=date&order=desc" \
  -o /tmp/latest_post.json
LATEST_DATE=$(python3 -c "import json; d=json.load(open('/tmp/latest_post.json')); print(d[0]['date_gmt'])" 2>/dev/null)
echo "Latest post date: $LATEST_DATE"

# Calculate a date before latest (needed for immediate publish)
LATEST_SECONDS=$(python3 -c "
from datetime import datetime, timezone, timedelta
dt = datetime.fromisoformat('$LATEST_DATE'.replace('Z','+00:00'))
# Go back 1 second
prev = dt - timedelta(seconds=1)
print(prev.strftime('%Y-%m-%dT%H:%M:%S'))
")
echo "Using date_gmt: $LATEST_SECONDS"

echo ""
echo "=== Step 2: Upload poster.png ==="
curl -s -X POST \
  "$WP_URL/wp-json/wp/v2/media" \
  -u "$CREDS" \
  -H "Content-Type: image/png" \
  -H "Content-Disposition: attachment; filename=poster.png" \
  --data-binary "@$WORKDIR/poster.png" \
  -o /tmp/wp_media.json

MEDIA_ID=$(python3 -c "import json; print(json.load(open('/tmp/wp_media.json'))['id'])")
MEDIA_URL=$(python3 -c "import json; print(json.load(open('/tmp/wp_media.json'))['source_url'])")
echo "Media uploaded: ID=$MEDIA_ID"
echo "Media URL: $MEDIA_URL"

echo ""
echo "=== Step 3: Create article ==="
# Convert markdown to HTML
ARTICLE_HTML=$(python3 << 'PYEOF'
import re

md = open("/Users/quyue/www/blog/2026-04-28-huygens-clocks-synchronization/article.md").read()

# Remove the # title (we'll use WordPress title field)
lines = md.split('\n')
body_lines = []
in_frontmatter = False
for line in lines:
    if line.startswith('# '):
        continue  # skip H1 title line
    body_lines.append(line)

html_parts = []
in_code = False
for para in '\n\n'.join(body_lines).split('\n\n'):
    para = para.strip()
    if not para:
        continue
    if para.startswith('```') or para.startswith('    '):
        # code block
        lang = ''
        if para.startswith('```'):
            lang_line = para.split('\n')[0]
            lang = lang_line[3:].strip()
            para = '\n'.join(para.split('\n')[1:])
            if para.endswith('```'):
                para = para[:-3]
        escaped = para.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        html_parts.append(f'<pre><code class="language-{lang}">{escaped}</code></pre>')
    elif para.startswith('## '):
        heading = re.sub(r'^##\s+', '', para)
        html_parts.append(f'<h2>{heading}</h2>')
    elif para.startswith('- ') or para.startswith('* '):
        items = []
        for line in para.split('\n'):
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                content = re.sub(r'^\*\s+', '', re.sub(r'^- ', '', line))
                items.append(f'<li>{content}</li>')
        html_parts.append(f'<ul>{"".join(items)}</ul>')
    elif re.match(r'^\d+\.\s', para):
        items = []
        for line in para.split('\n'):
            line = line.strip()
            m = re.match(r'^\d+\.\s+(.*)', line)
            if m:
                content = m.group(1)
                items.append(f'<li>{content}</li>')
        html_parts.append(f'<ol>{"".join(items)}</ol>')
    elif '**' in para:
        # Inline formatting
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
        para = re.sub(r'\*(.+?)\*', r'<em>\1</em>', para)
        para = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', para)
        html_parts.append(f'<p>{para}</p>')
    else:
        para = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para)
        para = re.sub(r'\*(.+?)\*', r'<em>\1</em>', para)
        para = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', para)
        html_parts.append(f'<p>{para}</p>')

print('\n'.join(html_parts))
PYEOF
)

# Escape for JSON
ESCAPED_HTML=$(python3 -c "import json; print(json.dumps('''$ARTICLE_HTML'''))")

PAYLOAD=$(python3 << 'PYEOF'
import json, sys

article_html = """$ARTICLE_HTML"""

# The HTML gets replaced in bash, so read from file instead
md = open("/Users/quyue/www/blog/2026-04-28-huygens-clocks-synchronization/article.md").read()
lines = md.split('\n')
title = ''
body_lines = []
for line in lines:
    if line.startswith('# '):
        title = line[2:].strip()
    elif line.startswith('## '):
        body_lines.append(line)
    elif line.strip():
        body_lines.append(line)
    elif body_lines and body_lines[-1].strip():
        body_lines.append('')

# Build HTML properly
import re

def md_to_html(text):
    result = []
    paragraphs = re.split(r'\n\s*\n', text.strip())
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para.startswith('## '):
            heading = re.sub(r'^##\s+', '', para)
            result.append(f'<h2>{heading}</h2>')
        elif para.startswith('- ') or para.startswith('* '):
            items = []
            for line in para.split('\n'):
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    content = re.sub(r'^\*\s+', '', re.sub(r'^- ', '', line))
                    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
                    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
                    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
                    items.append(f'<li>{content}</li>')
            result.append(f'<ul>{"".join(items)}</ul>')
        elif re.match(r'^\d+\.\s', para):
            items = []
            for line in para.split('\n'):
                line = line.strip()
                m = re.match(r'^\d+\.\s+(.*)', line)
                if m:
                    content = m.group(1)
                    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
                    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
                    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
                    items.append(f'<li>{content}</li>')
            result.append(f'<ol>{"".join(items)}</ol>')
        else:
            html = para
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
            html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
            result.append(f'<p>{html}</p>')
    return '\n'.join(result)

body = '\n\n'.join(body_lines)
body = re.sub(r'\n\s*\n', '\n\n', body)
body_html = md_to_html(body)

# Escape for shell JSON
print(json.dumps({
    "title": title,
    "slug": "2026-04-28-huygens-clocks-synchronization",
    "status": "publish",
    "content": body_html,
    "featured_media": int("$MEDIA_ID"),
    "date_gmt": "$LATEST_SECONDS",
    "categories": [1]
}))
PYEOF
)

echo "$PAYLOAD" > /tmp/wp_post_payload.json

curl -s -X POST \
  "$WP_URL/wp-json/wp/v2/posts" \
  -u "$CREDS" \
  -H "Content-Type: application/json" \
  -d @" /tmp/wp_post_payload.json \
  -o /tmp/wp_post.json

POST_ID=$(python3 -c "import json; print(json.load(open('/tmp/wp_post.json'))['id'])" 2>/dev/null)
POST_URL=$(python3 -c "import json; print(json.load(open('/tmp/wp_post.json'))['link'])" 2>/dev/null)
echo "Post created: ID=$POST_ID"
echo "Post URL: $POST_URL"

echo ""
echo "=== Step 4: Save wp-media-ids.json ==="
echo "{\"media_id\": $MEDIA_ID, \"media_url\": \"$MEDIA_URL\", \"post_id\": $POST_ID, \"post_url\": \"$POST_URL\"}" > "$WORKDIR/wp-media-ids.json"
echo "Done!"