#!/usr/bin/env python3
"""Publish Young's Double Slit article to WordPress."""
import re, json, requests, base64, os

# --- Config ---
article_dir = '/Users/quyue/www/blog/2026-05-08-youngs-double-slit'
article_slug = 'youngs-double-slit'
auth = ('bted2k@gmail.com', 'zVlf aCkm vB79 GjXc zVrJ dSuH')
wp_url = 'https://blog.flowrust.com'

# --- Read article ---
md = open(f'{article_dir}/article.md').read()

# --- md_to_html (fixed version) ---
def md_to_html(md):
    html = md
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2].strip()
    html = re.sub(r'```(\w*)\n(.*?)```', 
                  lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2)}</code></pre>', 
                  html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', html)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    html = re.sub(r'^---$', '<hr/>', html, flags=re.MULTILINE)
    paragraphs = []
    current_para = []
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            if current_para:
                text = ' '.join(current_para)
                paragraphs.append(f'<p>{text}</p>')
                current_para = []
            continue
        is_block = (
            line.startswith('<h') or line.startswith('<pre') or line.startswith('<hr') or
            line.startswith('<ul') or line.startswith('<ol') or line.startswith('<li') or
            line.startswith('<img') or line.startswith('<blockquote')
        )
        if is_block:
            if current_para:
                text = ' '.join(current_para)
                paragraphs.append(f'<p>{text}</p>')
                current_para = []
            paragraphs.append(line)
        else:
            current_para.append(line)
    if current_para:
        text = ' '.join(current_para)
        paragraphs.append(f'<p>{text}</p>')
    return '\n'.join(paragraphs)

def fix_md_to_html_output(html):
    if re.search(r'<p>\|[^|]+\|[^|]*\|</p>', html):
        print("WARNING: Table detected, but skipping conversion for this article")
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'<p><code>`</code></p>\s*<p>(.+?)</p>\s*<p><code>`</code></p>',
                  r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    if '<pre><code' not in html and '<code class="language-' in html:
        html = html.replace('<code class="language-">', '<pre><code class="language-">')
        html = html.replace('</code>\n</p>', '</code></pre>\n</p>')
    if '<pre><pre><code' in html:
        html = html.replace('<pre><pre><code', '<pre><code')
    return html

html = md_to_html(md)
html = fix_md_to_html_output(html)
html_original = html  # Keep original for card position finding

# --- Extract title from first h1 ---
title_match = re.search(r'<h1>(.+?)</h1>', html)
article_title = title_match.group(1) if title_match else "Young's Double Slit Experiment"
print(f"Article title: {article_title}")

# --- Find card insertion positions (on ORIGINAL html) ---
def find_para_end_after(html, phrase):
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4 if end_para != -1 else None

def find_h2_section_insert(html, h2_text_contains):
    h2_idx = html.find(f'<h2>{h2_text_contains}</h2>')
    if h2_idx == -1:
        search_start = 0
        while True:
            h2_open = html.find('<h2>', search_start)
            if h2_open == -1:
                break
            h2_close = html.find('</h2>', h2_open)
            if h2_close == -1:
                break
            heading_text = html[h2_open + 4:h2_close]
            if h2_text_contains.lower() in heading_text.lower():
                h2_idx = h2_open
                break
            search_start = h2_open + 1
    if h2_idx == -1:
        return None
    first_p = html.find('<p>', h2_idx)
    if first_p == -1:
        return None
    end_p = html.find('</p>', first_p)
    return end_p + 4 if end_p != -1 else None

positions = {}
positions['card1'] = find_para_end_after(html_original, 'The complete intensity distribution across the screen is:')
positions['card2'] = find_para_end_after(html_original, 'On the screen itself, the linear fringe spacing is:')
positions['card3'] = find_para_end_after(html_original, 'Run the double slit with individual electrons or photons')
print("Insert positions:", positions)

positions = {k: v for k, v in positions.items() if v is not None}
missing = set(['card1', 'card2', 'card3']) - set(positions.keys())
if missing:
    print(f"WARNING: phrases not found: {missing}")
else:
    print("All card positions found!")

# --- Upload images to WordPress ---
def upload_image(filename, display_name):
    filepath = f'{article_dir}/{filename}'
    if not os.path.exists(filepath):
        print(f"WARNING: {filepath} not found, skipping")
        return None, None
    with open(filepath, 'rb') as f:
        response = requests.post(
            f'{wp_url}/wp-json/wp/v2/media',
            auth=auth,
            headers={
                'Content-Type': 'image/png',
                'Content-Disposition': f'attachment; filename={display_name}',
            },
            data=f.read(),
            timeout=60
        )
    if response.status_code in (200, 201):
        data = response.json()
        print(f"Uploaded {filename}: media ID {data['id']}, URL {data['source_url']}")
        return data['id'], data['source_url']
    else:
        print(f"ERROR uploading {filename}: {response.status_code} {response.text}")
        return None, None

cover_id, cover_url = upload_image('poster.png', 'poster.png')
card1_id, card1_url = upload_image('card-01.png', 'card-01.png')
card2_id, card2_url = upload_image('card-02.png', 'card-02.png')
card3_id, card3_url = upload_image('card-03.png', 'card-03.png')

# --- Build card_imgs dict ---
card_imgs = {}
if card1_url:
    card_imgs['card1'] = f'<br/><img src="{card1_url}" alt="Intensity Formula" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>'
if card2_url:
    card_imgs['card2'] = f'<br/><img src="{card2_url}" alt="Fringe Spacing" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>'
if card3_url:
    card_imgs['card3'] = f'<br/><img src="{card3_url}" alt="Wave-Particle Duality" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>'

# --- Insert cards bottom-to-top ---
sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)
for name, pos in sorted_cards:
    if name in card_imgs:
        html = html[:pos] + '\n' + card_imgs[name] + html[pos:]
        print(f"Inserted {name} at position {pos}")

# --- Create post ---
post_data = {
    'title': article_title,
    'slug': article_slug,
    'status': 'publish',
    'content': html,
    'featured_media': cover_id,
}

resp = requests.post(
    f'{wp_url}/wp-json/wp/v2/posts',
    auth=auth,
    headers={'Content-Type': 'application/json'},
    json=post_data,
    timeout=30
)
print(f"Create post status: {resp.status_code}")
result = resp.json()
post_id = result.get('id')
print(f"Post ID: {post_id}, Status: {result.get('status')}, URL: {result.get('link')}")

# --- Force publish if status is future ---
if result.get('status') == 'future' and post_id:
    print("Post is scheduled, forcing publish...")
    import datetime
    past_date = '2026-05-07T04:00:00'
    patch_data = {
        'status': 'publish',
        'date_gmt': past_date
    }
    patch_resp = requests.post(
        f'{wp_url}/wp-json/wp/v2/posts/{post_id}',
        auth=auth,
        headers={'Content-Type': 'application/json'},
        json=patch_data,
        timeout=30
    )
    print(f"Force publish PATCH status: {patch_resp.status_code}")
    print(f"Force publish result: {patch_resp.json()}")

# --- Update elysia-tools-last-used ---
with open('/Users/quyue/www/blog/elysia-tools-last-used', 'a') as f:
    f.write(f'\nyoungs-double-slit-done\n')

# --- Update PUBLISHED_ARTICLES.md ---
published_path = '/Users/quyue/www/blog/PUBLISHED_ARTICLES.md'
entry = f'''
## 2026-05-08 — Young's Double Slit: Why Light Behaves Like a Wave
- **Topic**: Young's Double Slit Experiment (youngs-double-slit)
- **Status**: PUBLISHED
- **WP ID**: {post_id}
- **URL**: {result.get('link', 'N/A')}
- **Article Dir**: {article_dir}
'''
with open(published_path, 'a') as f:
    f.write(entry)

print("\n=== PUBLICATION COMPLETE ===")
print(f"URL: {result.get('link')}")
