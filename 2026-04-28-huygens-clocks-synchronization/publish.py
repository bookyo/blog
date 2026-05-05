#!/usr/bin/env python3
import json, subprocess, re, os

WORKDIR = "/Users/quyue/www/blog/2026-04-28-huygens-clocks-synchronization"
WP_URL = "https://blog.flowrust.com"
CREDS = "bted2k@gmail.com:zVlf aCkm vB79 GjXc zVrJ dSuH"

# Step 1: Get latest post date
print("=== Step 1: Get latest post date ===")
result = subprocess.run([
    "curl", "-s", "-u", CREDS,
    f"{WP_URL}/wp-json/wp/v2/posts?per_page=1&orderby=date&order=desc",
    "-o", "/tmp/latest_post.json"
], check=True)
latest = json.load(open("/tmp/latest_post.json"))
latest_date = latest[0]["date_gmt"]
print(f"Latest post date: {latest_date}")

from datetime import datetime, timezone, timedelta
dt = datetime.fromisoformat(latest_date.replace("Z", "+00:00"))
prev = dt - timedelta(seconds=1)
date_gmt = prev.strftime("%Y-%m-%dT%H:%M:%S")
print(f"Using date_gmt: {date_gmt}")

# Step 2: Upload poster
print("\n=== Step 2: Upload poster.png ===")
result = subprocess.run([
    "curl", "-s", "-X", "POST",
    f"{WP_URL}/wp-json/wp/v2/media",
    "-u", CREDS,
    "-H", "Content-Type: image/png",
    "-H", "Content-Disposition: attachment; filename=poster.png",
    "--data-binary", "@/Users/quyue/www/blog/2026-04-28-huygens-clocks-synchronization/poster.png",
    "-o", "/tmp/wp_media.json"
], check=True)
media = json.load(open("/tmp/wp_media.json"))
media_id = media["id"]
media_url = media["source_url"]
print(f"Media ID: {media_id}")
print(f"Media URL: {media_url}")

# Step 3: Convert markdown to HTML
print("\n=== Step 3: Convert markdown to HTML ===")
md = open(f"{WORKDIR}/article.md").read()
lines = md.split('\n')
title = ''
body_lines = []
for line in lines:
    if line.startswith('# '):
        title = line[2:].strip()
    else:
        body_lines.append(line)

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

body_text = '\n\n'.join(body_lines)
body_text = re.sub(r'\n\s*\n', '\n\n', body_text)
body_html = md_to_html(body_text)
print(f"Title: {title}")
print(f"HTML length: {len(body_html)} chars")

# Step 4: Create post
print("\n=== Step 4: Create WordPress post ===")
payload = json.dumps({
    "title": title,
    "slug": "2026-04-28-huygens-clocks-synchronization",
    "status": "publish",
    "content": body_html,
    "featured_media": media_id,
    "date_gmt": date_gmt,
    "categories": [1]
}, ensure_ascii=False)

with open("/tmp/wp_post_payload.json", "w") as f:
    f.write(payload)

result = subprocess.run([
    "curl", "-s", "-X", "POST",
    f"{WP_URL}/wp-json/wp/v2/posts",
    "-u", CREDS,
    "-H", "Content-Type: application/json",
    "-d", "@/tmp/wp_post_payload.json",
    "-o", "/tmp/wp_post.json"
], check=True)

post = json.load(open("/tmp/wp_post.json"))
post_id = post.get("id", "ERROR")
post_url = post.get("link", "ERROR")
print(f"Post ID: {post_id}")
print(f"Post URL: {post_url}")

# Step 5: Save result
result_data = {
    "media_id": media_id,
    "media_url": media_url,
    "post_id": post_id,
    "post_url": post_url,
    "date_gmt": date_gmt
}
with open(f"{WORKDIR}/wp-media-ids.json", "w") as f:
    json.dump(result_data, f, indent=2)

print(f"\n=== DONE ===")
print(f"Post: {post_url}")
