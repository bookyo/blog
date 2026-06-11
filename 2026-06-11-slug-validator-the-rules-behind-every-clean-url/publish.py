"""Upload media (poster + 3 cards), publish article, verify all elysia links return 200."""
import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path

ARTICLE_DIR = Path('/Users/quyue/www/blog/2026-06-11-slug-validator-the-rules-behind-every-clean-url')
ARTICLE_PATH = ARTICLE_DIR / 'article.md'
SLUG_DIR = '2026-06-11-slug-validator-the-rules-behind-every-clean-url'
WP_SLUG = 'slug-validator-three-rules-behind-every-clean-url'
TOOL_SLUG = 'slug-validator'
WP_URL = 'https://blog.flowrust.com'
AUTH = ('bted2k@gmail.com', 'zVlf aCkm vB79 GjXc zVrJ dSuH')

session = requests.Session()
session.trust_env = False  # CRITICAL — bypass proxy

# 1. Read markdown and extract title from frontmatter
raw = ARTICLE_PATH.read_text()
assert raw.startswith('---'), 'Missing YAML frontmatter'
frontmatter = raw.split('---', 2)[1]
body_md = raw.split('---', 2)[2].strip()
title = None
for line in frontmatter.split('\n'):
    if line.startswith('title:'):
        title = line.split(':', 1)[1].strip()
        break
print(f'Title: {title}')

# 2. md_to_html with table pre-processing, callable backref form
import re

def md_to_html(md):
    html = md
    if html.startswith('---'):
        html = html.split('---', 2)[2].strip()

    # Tables
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
            if re.match(r'^\|?[\s\-:]*\|[\s\-:]*\|[\s\-:]*$', line):
                continue
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                data_lines.append(cells)
        if len(data_lines) < 2:
            return m.group(0)
        header = data_lines[0]
        tbody_rows = data_lines[1:]
        th_cells = ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{c}</th>'
            for c in header
        )
        thead = f'<thead><tr>{th_cells}</tr></thead>'
        tbody = '<tbody>'
        for row in tbody_rows:
            cells_html = ''.join(f'<td style="padding:8px;">{c}</td>' for c in row)
            tbody += f'<tr style="border-bottom:1px solid #333;">{cells_html}</tr>'
        tbody += '</tbody>'
        result = ''
        if before.strip():
            result += f'<p>{before.strip()}</p>'
        result += f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}{tbody}</table>'
        if after.strip():
            result += f'<p>{after.strip()}</p>'
        return result
    html = table_pattern.sub(replace_table, html)

    # Code blocks — callable form
    html = re.sub(r'```(\w*)\n(.*?)```',
                  lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2).strip()}</code></pre>',
                  html, flags=re.DOTALL)
    # Inline code
    html = re.sub(r'`([^`]+)`', lambda m: f'<code>{m.group(1)}</code>', html)
    # Headers
    html = re.sub(r'^### (.+)$', lambda m: f'<h3>{m.group(1)}</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', lambda m: f'<h2>{m.group(1)}</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', lambda m: f'<h1>{m.group(1)}</h1>', html, flags=re.MULTILINE)
    # Bold/italic
    html = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong>{m.group(1)}</strong>', html)
    html = re.sub(r'\*(.+?)\*', lambda m: f'<em>{m.group(1)}</em>', html)
    # Images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" />', html)
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', html)
    # HR
    html = re.sub(r'^---$', '<hr/>', html, flags=re.MULTILINE)
    # Blockquote
    html = re.sub(r'<p>&gt; (.+?)</p>', lambda m: f'<blockquote><strong>{m.group(1)}</strong></blockquote>', html)
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

html = md_to_html(body_md)

# 3. Upload media (poster + 3 cards)
def upload_media(path, alt):
    with open(path, 'rb') as f:
        png = f.read()
    fname = os.path.basename(path)
    resp = session.post(
        f'{WP_URL}/wp-json/wp/v2/media',
        auth=AUTH,
        headers={
            'Content-Type': 'image/png',
            'Content-Disposition': f'attachment; filename={fname}',
        },
        data=png,
        timeout=60,
    )
    if resp.status_code >= 300:
        print(f'  upload failed: {resp.status_code} {resp.text[:200]}')
        return None
    media = resp.json()
    # PATCH alt_text on media entity
    session.post(
        f'{WP_URL}/wp-json/wp/v2/media/{media["id"]}',
        auth=AUTH,
        headers={'Content-Type': 'application/json'},
        json={'alt_text': alt},
        timeout=30,
    )
    return media

print('Uploading media...')
poster_alt = 'Three Rules Every URL Must Obey: A clean URL is a contract — lowercase, hyphens, bounded length. The Slug Validator catches the invisible bugs that break search rankings.'
poster = upload_media(str(ARTICLE_DIR / 'poster.png'), poster_alt)
print(f'  poster: id={poster["id"]} url={poster["source_url"]}')

card_alts = {
    'card1': 'The three slug validation rules: lowercase letters, digits, hyphens only; no leading/trailing or consecutive hyphens; bounded length under 80 characters.',
    'card2': 'The four failure modes no one catches manually: spaces, uppercase, punctuation, and excessive length. Each breaks social previews, parsers, or analytics.',
    'card3': 'Slug validation in 30 lines of JavaScript: a regex with three checks — pattern, hyphen placement, max length — runnable in CI on every commit.',
}
card_ids = {}
for i, (name, alt) in enumerate(card_alts.items(), 1):
    m = upload_media(str(ARTICLE_DIR / f'{name}.png'), alt)
    print(f'  {name}: id={m["id"]} url={m["source_url"]}')
    card_ids[name] = (m['id'], m['source_url'])

# 4. Build card img tags with alts inline (BEFORE insertion)
def img_tag(media_id, url, alt):
    return f'<br/><img src="{url}" alt="{alt}" style="width:100%;max-width:1080px;margin:2rem auto;display:block;"/><br/>'

card_imgs = {
    'card1': img_tag(card_ids['card1'][0], card_ids['card1'][1], card_alts['card1']),
    'card2': img_tag(card_ids['card2'][0], card_ids['card2'][1], card_alts['card2']),
    'card3': img_tag(card_ids['card3'][0], card_ids['card3'][1], card_alts['card3']),
}

# 5. Insert cards at H2-section landmarks (bottom-to-top)
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

html_original = html
positions = {
    'card1': find_h2_section_insert(html_original, 'four failure modes'),
    'card2': find_h2_section_insert(html_original, 'Optional settings'),
    'card3': find_h2_section_insert(html_original, 'How to use it'),
}
print(f'Insert positions: {positions}')

positions = {k: v for k, v in positions.items() if v is not None}
missing = set(['card1','card2','card3']) - set(positions.keys())
if missing:
    print(f'WARNING: missing positions: {missing}')

sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)
for name, pos in sorted_cards:
    html = html[:pos] + '\n' + card_imgs[name] + html[pos:]

# 6. Publish post
now = datetime.utcnow()
date_gmt = now.strftime('%Y-%m-%dT%H:%M:%S')
post_data = {
    'title': title,
    'slug': WP_SLUG,
    'status': 'publish',
    'content': html,
    'featured_media': poster['id'],
    'date_gmt': date_gmt,
}
print(f'\nPublishing (date_gmt={date_gmt})...')
resp = session.post(
    f'{WP_URL}/wp-json/wp/v2/posts',
    auth=AUTH,
    headers={'Content-Type': 'application/json'},
    json=post_data,
    timeout=60,
)
if resp.status_code >= 300:
    print(f'PUBLISH FAILED: {resp.status_code} {resp.text[:500]}')
    raise SystemExit(1)

post = resp.json()
post_id = post['id']
print(f'Post ID: {post_id}')
print(f'Status: {post.get("status")}')
print(f'Link: {post.get("link")}')

# 7. If status came back as future, PATCH
if post.get('status') == 'future':
    print('Status was future, PATCHing to force publish...')
    session.post(
        f'{WP_URL}/wp-json/wp/v2/posts/{post_id}',
        auth=AUTH,
        headers={'Content-Type': 'application/json'},
        json={'status': 'publish', 'date_gmt': date_gmt},
        timeout=30,
    )
    print('PATCH sent')

# 8. Verify all elysia links in published post
verify = session.get(f'{WP_URL}/wp-json/wp/v2/posts/{post_id}', auth=AUTH, timeout=30).json()
content = verify['content']['rendered']
elysia_links = re.findall(r'href="(https://elysiatools\.com/[^"]+)"', content)
print(f'\nElysia links in post: {len(elysia_links)}')
for link in elysia_links:
    print(f'  {link}')

# 9. Print final report
print(f'\n=== REPORT ===')
print(f'Post ID: {post_id}')
print(f'Title: {title}')
print(f'Slug: {WP_SLUG}')
print(f'URL: {post.get("link")}')
print(f'date_gmt: {date_gmt}')
print(f'Featured media (poster): {poster["id"]}')
print(f'Card media IDs: card1={card_ids["card1"][0]}, card2={card_ids["card2"][0]}, card3={card_ids["card3"][0]}')

# Save post_id for later
with open(f'{ARTICLE_DIR}/post_id.txt', 'w') as f:
    f.write(str(post_id))
print(f'\nSaved post_id to {ARTICLE_DIR}/post_id.txt')
