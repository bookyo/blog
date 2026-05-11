import re, requests

work_dir = "/Users/quyue/www/blog/2026-05-09-audio-lufs-meter"
auth = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
wp_url = "https://blog.flowrust.com"
post_id = 2437

session = requests.Session()
session.trust_env = False

with open(f"{work_dir}/article_raw.html") as f:
    html = f.read()

# ─── Table converters ──────────────────────────────────────────────────────────
def convert_markdown_tables(html):
    """Multi-line table: one row per <p>"""
    table_pattern = re.compile(
        r'(<p>\|([^\n]+)\|</p>\s*<p>\|[-:\s|]+\|</p>(?:\s*<p>\|[^\n]+\|</p>)*)',
        re.DOTALL
    )
    def build_table(m):
        full = m.group(0)
        lines = re.findall(r'<p>(.+?)</p>', full, re.DOTALL)
        rows = []
        for line in lines:
            stripped = line.strip()
            if re.match(r'\||[-: ]+\|', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|') if c.strip()]
            rows.append(cells)
        if len(rows) < 1:
            return full
        header = rows[0]
        thead = '<thead><tr>' + ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{cell}</th>'
            for cell in header
        ) + '</tr></thead>'
        tbody_rows = ''
        for row in rows[1:]:
            cells_html = ''.join(f'<td style="padding:8px;">{cell}</td>' for cell in row)
            tbody_rows += f'<tr style="border-bottom:1px solid #333;">{cells_html}</tr>'
        return f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}<tbody>{tbody_rows}</tbody></table>'
    return table_pattern.sub(build_table, html)

def convert_all_tables(html):
    """Convert all table variants: multi-line + single-p-tag."""
    # Pattern 2: Single-p-tag table — all rows in one <p>
    single_pattern = re.compile(
        r'<p>\s*(\|[^|]+\|[^|]*\|)\s*</p>\s*<p>\s*\|[-:\s| ]+\|\s*</p>(.*?)(?=<p>[^<]|<h[23])',
        re.DOTALL
    )
    def build_single(m):
        header_block = m.group(1)
        body_block = m.group(2)
        header_cells = [c.strip() for c in header_block.split('|') if c.strip()]
        body_cells = re.findall(r'\|([^|]+)\|', body_block)
        body_cells = [c.strip() for c in body_cells if c.strip() and not re.match(r'^[-: ]+$', c)]
        col_count = len(header_cells)
        rows = [header_cells] + [body_cells[i:i+col_count] for i in range(0, len(body_cells), col_count)]
        thead = '<thead><tr>' + ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{c}</th>'
            for c in header_cells
        ) + '</tr></thead>'
        tbody = '<tbody>'
        for row in rows[1:]:
            tbody += '<tr style="border-bottom:1px solid #333;">' + ''.join(
                f'<td style="padding:8px;">{c}</td>' for c in row
            ) + '</tr>'
        tbody += '</tbody>'
        return f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}{tbody}</table>'
    
    html = convert_markdown_tables(html)
    html = single_pattern.sub(build_single, html)
    return html

# ─── Apply table fix ──────────────────────────────────────────────────────────
html_fixed = convert_all_tables(html)

# Verify no raw table text remains
if re.search(r'<p>\s*\|[^|]+\|[^|]*\|</p>', html_fixed):
    print("WARNING: single-p-tag table still present after fix!")
else:
    print("Table fix applied — no raw single-p-tag table found")

# Save fixed HTML
with open(f"{work_dir}/article_fixed.html", "w") as f:
    f.write(html_fixed)

# Find insertion points (on article_raw.html before ANY insertions)
def find_para_end_after(html, phrase):
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4

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

# Card URLs from earlier
card1_url = "https://blog.flowrust.com/wp-content/uploads/2026/05/card-01-35.png"
card2_url = "https://blog.flowrust.com/wp-content/uploads/2026/05/card-02-36.png"
card3_url = "https://blog.flowrust.com/wp-content/uploads/2026/05/card-03-35.png"

positions = {
    'card1': find_h2_section_insert(html, 'What LUFS Actually Measures'),
    'card2': find_h2_section_insert(html, 'The Loudness Wars'),
    'card3': find_h2_section_insert(html, 'The Three Numbers'),
}
print("Insert positions:", positions)

positions = {k: v for k, v in positions.items() if v is not None}
sorted_cards = sorted(positions.items(), key=lambda x: x[1], reverse=True)

card_imgs = {
    'card1': f'<br/><img src="{card1_url}" alt="Card 1: Perceived Loudness" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card2': f'<br/><img src="{card2_url}" alt="Card 2: Loudness Wars" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
    'card3': f'<br/><img src="{card3_url}" alt="Card 3: Platform Standards" style="width:100%;max-width:1080px;margin:2rem 0;display:block;"/><br/>',
}

for name, pos in sorted_cards:
    html_fixed = html_fixed[:pos] + '\n' + card_imgs[name] + html_fixed[pos:]

with open(f"{work_dir}/article_with_cards_fixed.html", "w") as f:
    f.write(html_fixed)

# Update post
resp = session.post(
    f"{wp_url}/wp-json/wp/v2/posts/{post_id}",
    auth=auth,
    headers={"Content-Type": "application/json"},
    json={"content": html_fixed},
    timeout=30
)
print(f"\nUpdate response: {resp.status_code}")
print(f"Updated post URL: {resp.json().get('link')}")
