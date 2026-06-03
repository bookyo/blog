#!/usr/bin/env python3
import json, re, sys
from datetime import datetime
import requests

article_dir = '/Users/quyue/www/blog/2026-06-03-fermat-principle'
article_path = f'{article_dir}/article.md'
wp_url = 'https://blog.flowrust.com'

session = requests.Session()
session.trust_env = False
auth = ('bted2k@gmail.com', 'zVlf aCkm vB79 GjXc zVrJ dSuH')

# Get media URLs
media_urls = {}
for mid, name in [(3355,'poster'),(3356,'card1'),(3357,'card2'),(3358,'card3')]:
    r = session.get(f'{wp_url}/wp-json/wp/v2/media/{mid}', auth=auth, timeout=30)
    data = r.json()
    media_urls[name] = data['source_url']
    print(f'{name}: {media_urls[name]}', flush=True)

# Read article
with open(article_path) as f:
    md = f.read()

# Extract title
parts = md.split('---', 2)
for line in parts[1].split('\n'):
    if line.startswith('title:'):
        title = line.split(':',1)[1].strip()
        break
else:
    title = 'Untitled'

print(f'Title: {title}', flush=True)

# md_to_html function
def md_to_html(md):
    html = md
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2].strip()
    # Tables pre-processing
    table_pattern = re.compile(
        r'(?:^|\n)([^\n]*\n)?(\|(?:[^\n]*?)\|(?:\n\|[^\n]*?)*)(\n[^\n]*)?(?=\n\n|\n#|\Z)',
        re.MULTILINE
    )
    def replace_table(m):
        before = m.group(1) or ''
        table_content = m.group(2)
        after = m.group(3) or ''
        lines = [l.strip() for l in table_content.strip().split('\n') if l.strip()]
        data_lines = []
        for line in lines:
            if re.match(r'^\|?[\s:\-]*\|[\s:\-]*\|[\s:\-]*$', line):
                continue
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                data_lines.append(cells)
        if len(data_lines) < 2:
            return m.group(0)
        header = data_lines[0]
        tbody_rows = data_lines[1:]
        thead_cols = ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{c}</th>'
            for c in header
        )
        thead = f'<thead><tr>{thead_cols}</tr></thead>'
        tbody = '<tbody>'
        for row in tbody_rows:
            cells_html = ''.join(f'<td style="padding:8px;">{c}</td>' for c in row)
            tbody += f'<tr style="border-bottom:1px solid #333;">{cells_html}</tr>'
        tbody += '</tbody>'
        table_html = f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}{tbody}</table>'
        result = ''
        if before.strip():
            result += f'<p>{before.strip()}</p>'
        result += table_html
        if after.strip():
            result += f'<p>{after.strip()}</p>'
        return result
    html = table_pattern.sub(replace_table, html)
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```',
                  lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2).strip()}</code></pre>',
                  html, flags=re.DOTALL)
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold/italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # Images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', html)
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    # HR
    html = re.sub(r'^---$', '<hr/>', html, flags=re.MULTILINE)
    # Paragraphs
    paragraphs = []
    current_para = []
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(f'<p>{" ".join(current_para)}</p>')
                current_para = []
            continue
        is_block = (
            line.startswith('<h') or line.startswith('<pre') or
            line.startswith('<hr') or line.startswith('<ul') or
            line.startswith('<ol') or line.startswith('<li') or
            line.startswith('<img') or line.startswith('<blockquote') or
            line.startswith('<table') or line.strip() == '</code></pre>'
        )
        if is_block:
            if current_para:
                paragraphs.append(f'<p>{" ".join(current_para)}</p>')
                current_para = []
            paragraphs.append(line)
        else:
            current_para.append(line)
    if current_para:
        paragraphs.append(f'<p>{" ".join(current_para)}</p>')
    return '\n'.join(paragraphs)

def find_h2_section_insert(html, h2_text_contains):
    search_start = 0
    while True:
        h2_open = html.find('<h2>', search_start)
        if h2_open == -1:
            return None
        h2_close = html.find('</h2>', h2_open)
        if h2_close == -1:
            return None
        heading_text = html[h2_open + 4:h2_close]
        if h2_text_contains.lower() in heading_text.lower():
            first_p = html.find('<p>', h2_open)
            if first_p == -1:
                return None
            end_p = html.find('</p>', first_p)
            return end_p + 4
        search_start = h2_open + 1

# Convert article
body = parts[2].strip()
html = md_to_html(body)
html_original = html

print(f'HTML length: {len(html)}', flush=True)

# Find H2 headings
h2s = re.findall(r'<h2>([^<]+)</h2>', html_original)
print(f'H2 headings: {h2s}', flush=True)

# Find card positions
positions = {
    'card1': find_h2_section_insert(html_original, "Snell's Law Emerges"),
    'card2': find_h2_section_insert(html_original, "What Fermat's Principle Explains"),
    'card3': find_h2_section_insert(html_original, "The Technology Running on Fermat"),
}
print(f'Card positions: {positions}', flush=True)

# Check for None
missing = [k for k, v in positions.items() if v is None]
if missing:
    print(f'WARNING: missing positions for: {missing}', flush=True)
else:
    print('All card positions found!', flush=True)

# Insert cards bottom-to-top
sorted_cards = sorted([(k,v) for k,v in positions.items() if v is not None], key=lambda x: x[1], reverse=True)
card_imgs = {
    'card1': f'<br/><img src="{media_urls["card1"]}" alt="Snells Law visualization showing light bending at a boundary" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card2': f'<br/><img src="{media_urls["card2"]}" alt="Fermat Principle unifies refraction, total internal reflection, and dispersion" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card3': f'<br/><img src="{media_urls["card3"]}" alt="Fiber optics and GPS rely on minimum-time path optimization" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
}
html = html_original
for name, pos in sorted_cards:
    html = html[:pos] + '\n' + card_imgs[name] + html[pos:]

print(f'Final HTML length: {len(html)}', flush=True)

# Publish
slug = 'fermat-principle-light-fastest-path'
now = datetime.utcnow()
date_gmt = now.strftime('%Y-%m-%dT%H:%M:%S')
print(f'date_gmt: {date_gmt}', flush=True)

post_data = {
    "title": title,
    "slug": slug,
    "status": "publish",
    "content": html,
    "featured_media": 3355,
    "date_gmt": date_gmt,
}

resp = session.post(
    f'{wp_url}/wp-json/wp/v2/posts',
    auth=auth,
    headers={'Content-Type': 'application/json'},
    json=post_data,
    timeout=30
)
print(f'Publish status: {resp.status_code}', flush=True)
resp_data = resp.json()
post_id = resp_data.get('id')
post_url = resp_data.get('link')
post_status = resp_data.get('status')
print(f'Post ID: {post_id}', flush=True)
print(f'URL: {post_url}', flush=True)
print(f'Status: {post_status}', flush=True)
if resp.status_code != 201:
    print(f'Full response: {resp_data}', flush=True)
else:
    print('PUBLISH SUCCESS!', flush=True)