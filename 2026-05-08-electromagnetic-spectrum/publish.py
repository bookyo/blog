import re
import requests
import json
import base64

# ============================================================
# STEP 1: Read and convert markdown to HTML
# ============================================================
with open("/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/article.md") as f:
    md = f.read()

def md_to_html(md):
    html = md
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2].strip()
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```',
                  lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2)}</code></pre>',
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
    # Images FIRST
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
                text = ' '.join(current_para)
                paragraphs.append(f'<p>{text}</p>')
                current_para = []
            continue
        is_block = (
            line.startswith('<h') or
            line.startswith('<pre') or
            line.startswith('<hr') or
            line.startswith('<ul') or
            line.startswith('<ol') or
            line.startswith('<li') or
            line.startswith('<img') or
            line.startswith('<blockquote')
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
    """Apply to md_to_html output before publishing to fix known bugs."""
    # Fix 0: TABLE
    if re.search(r'<p>\|[^|]+\|[^|]*\|</p>', html):
        html = convert_markdown_tables(html)
    # Fix 1: Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Fix 2: Broken code blocks
    html = re.sub(
        r'<p><code>`</code></p>\s*<p>(.+?)</p>\s*<p><code>`</code></p>',
        r'<pre><code>\1</code></pre>',
        html, flags=re.DOTALL)
    # Fix 3: Standalone code without pre
    if '<pre><code' not in html and '<code class="language-' in html:
        html = html.replace('<code class="language-">', '<pre><code class="language-">').replace('</code>\n</p>', '</code></pre>\n</p>')
    # Fix 4: Restore from double-pre
    if '<pre><pre><code' in html:
        html = html.replace('<pre><pre><code', '<pre><code')
    # Fix 5: Blockquote escaping
    html = re.sub(r'<p>&gt; (.+?)</p>', r'<blockquote><strong>\1</strong></blockquote>', html)
    return html

def convert_markdown_tables(html):
    """Convert raw markdown tables in <p> tags to proper <table>."""
    table_pattern = re.compile(
        r'(<p>\|([^\n]+)\|</p>\s*<p>\|[-:\s|]+\|</p>(?:\s*<p>\|[^\n]+\|</p>)*)',
        re.DOTALL)
    def build_table(m):
        full = m.group(0)
        lines = re.findall(r'<p>([^<]+)</p>', full)
        rows = []
        for line in lines:
            if re.match(r'\||[-: ]+\|', line.strip()):
                continue
            cells = [c.strip() for c in line.split('|') if c.strip()]
            rows.append(cells)
        if len(rows) < 1:
            return full
        header = rows[0]
        thead = '<thead><tr>' + ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{cell}</th>'
            for cell in header) + '</tr></thead>'
        tbody_rows = ''
        for row in rows[1:]:
            cells_html = ''.join(f'<td style="padding:8px;">{cell}</td>' for cell in row)
            tbody_rows += f'<tr style="border-bottom:1px solid #333;">{cells_html}</tr>'
        tbody = f'<tbody>{tbody_rows}</tbody>'
        return f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}{tbody}</table>'
    return table_pattern.sub(build_table, html)

html = md_to_html(md)
html = fix_md_to_html_output(html)
html_original = html  # Keep for card position finding

# ============================================================
# STEP 2: Find card positions and embed cards
# ============================================================
def find_para_end_after(html, phrase):
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4

# Card 1: "15 orders of magnitude" section
pos1 = find_para_end_after(html_original, '15 orders of magnitude')
# Card 2: "UV problem for space colonies" section
pos2 = find_para_end_after(html_original, "UV radiation than any human evolved to handle")
# Card 3: "gamma-ray bursts" section
pos3 = find_para_end_after(html_original, 'most violent events in the observable universe')

positions = {
    'card1': pos1,
    'card2': pos2,
    'card3': pos3,
}
print("Insert positions:", positions)

positions = {k: v for k, v in positions.items() if v is not None}
missing = set(['card1', 'card2', 'card3']) - set(positions.keys())
if missing:
    print(f"WARNING: phrases not found: {missing}")

# Card URLs - these will be replaced after upload
card_urls = {
    'card1': 'https://blog.flowrust.com/wp-content/uploads/placeholder-card1.png',
    'card2': 'https://blog.flowrust.com/wp-content/uploads/placeholder-card2.png',
    'card3': 'https://blog.flowrust.com/wp-content/uploads/placeholder-card3.png',
}

# Embed cards
sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)
for name, pos in sorted_cards:
    img_tag = f'<br/><img src="{card_urls[name]}" alt="Highlight Card" style="width:100%;max-width:1080px;margin:2rem 0;"/><br/>'
    html = html[:pos] + '\n' + img_tag + html[pos:]

# ============================================================
# STEP 3: Upload images to WordPress
# ============================================================
auth = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
wp_url = "https://blog.flowrust.com"

def upload_image(filename, display_name):
    with open(filename, "rb") as f:
        response = requests.post(
            f"{wp_url}/wp-json/wp/v2/media",
            auth=auth,
            headers={
                "Content-Type": "image/png",
                "Content-Disposition": f"attachment; filename={display_name}",
            },
            data=f.read(),
            timeout=30
        )
    if response.status_code not in (200, 201):
        print(f"Upload failed for {filename}: {response.status_code} {response.text}")
        return None, None
    return response.json()["id"], response.json()["source_url"]

# Upload poster
poster_id, poster_url = upload_image(
    "/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/poster.png",
    "poster.png"
)
print(f"Poster: ID={poster_id}, URL={poster_url}")

# Upload cards
card_files = [
    ("/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/card-01.png", "card-01.png"),
    ("/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/card-02.png", "card-02.png"),
    ("/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/card-03.png", "card-03.png"),
]
card_ids = []
card_uploaded_urls = []
for filepath, name in card_files:
    cid, curl = upload_image(filepath, name)
    if cid:
        card_ids.append(cid)
        card_uploaded_urls.append(curl)
        print(f"Card {name}: ID={cid}, URL={curl}")

# Replace placeholder URLs with actual URLs
for i, (name, placeholder_url) in enumerate(card_urls.items()):
    if i < len(card_uploaded_urls):
        html = html.replace(placeholder_url, card_uploaded_urls[i])

# ============================================================
# STEP 4: Create WordPress post
# ============================================================
import datetime
past_date = "2026-05-07T12:00:00"  # One day before today

post_data = {
    "title": "The Invisible Rainbow That Runs Everything: A Journey Through the Electromagnetic Spectrum",
    "slug": "electromagnetic-spectrum-15-orders-of-magnitude",
    "status": "publish",
    "content": html,
    "date_gmt": past_date,
    "featured_media": poster_id,
}

resp = requests.post(
    f"{wp_url}/wp-json/wp/v2/posts",
    auth=auth,
    headers={"Content-Type": "application/json"},
    json=post_data,
    timeout=30
)
print(f"Create post status: {resp.status_code}")
if resp.status_code not in (200, 201):
    print(f"Response: {resp.text[:500]}")

result = resp.json()
post_id = result.get("id")
print(f"Post ID: {post_id}, Status: {result.get('status')}")

# ============================================================
# STEP 5: Update last-used file
# ============================================================
with open("/Users/quyue/www/blog/elysia-tools-last-used", "a") as f:
    f.write("\nelectromagnetic-spectrum-done\n")

# Update PUBLISHED_ARTICLES.md
publish_entry = f"""
## 2026-05-08 — Electromagnetic Spectrum: 15 Orders of Magnitude
- **Topic**: electromagnetic-spectrum (visualization)
- **Status**: PUBLISHED — WP ID {post_id}
- **Asset Dir**: /Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum
- **Poster**: poster.png (WP media ID {poster_id})
- **Cards**: {len(card_ids)} cards uploaded (IDs: {card_ids})
- **URL**: {result.get('link', 'N/A')}
"""
with open("/Users/quyue/www/blog/PUBLISHED_ARTICLES.md", "a") as f:
    f.write(publish_entry)

print("Done! Post URL:", result.get('link', 'N/A'))
