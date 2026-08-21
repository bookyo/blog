#!/usr/bin/env python3.11
"""PATCH WP 6212 (round 3): rebuild from source MD to fix merged-bullet + H3."""
import json, base64, urllib.request, re, sys, importlib.util

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
basic = base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
AUTH = f'Basic {basic}'

# Load md_to_html
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
from md_to_html import md_to_html

# === Step 1: Re-read source MD and rebuild content with proper HTML ===
md = open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article.md').read()
# Strip leading H1
md = re.sub(r'^# [^\n]+\n+', '', md, count=1)

# Replace `- **bold** — body` markdown bullets with explicit <ul><li>...</li></ul>
# to avoid WP 5676/6185/6135 MERGED_BULLET_LIST family
# Match a block of lines that all start with `- ` and wrap in <ul>
def md_bullet_block_to_ul(block):
    """block is a string of consecutive lines starting with '- '."""
    items = []
    for line in block.strip().split('\n'):
        # Try `- **bold** — body` first
        m2 = re.match(r'^- \*\*(.+?)\*\* — (.+)$', line.strip())
        if m2:
            items.append(f'<li><strong>{m2.group(1)}</strong> — {m2.group(2)}</li>')
        else:
            # Generic `- **bold** body` (no en-dash)
            m3 = re.match(r'^- \*\*(.+?)\*\*\s*(.+)$', line.strip())
            if m3:
                items.append(f'<li><strong>{m3.group(1)}</strong> {m3.group(2)}</li>')
            else:
                # Plain `- text`
                items.append(f'<li>{line.lstrip("- ").strip()}</li>')
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


# Find runs of lines starting with `- ` separated by blank lines from intro paragraphs
def replace_bullet_blocks(text):
    out_lines = []
    in_bullet_block = False
    bullet_lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            in_bullet_block = True
            bullet_lines.append(line)
        elif stripped == '' and in_bullet_block:
            # blank line inside bullet block — flush now
            if bullet_lines:
                out_lines.append(md_bullet_block_to_ul('\n'.join(bullet_lines)))
                bullet_lines = []
            in_bullet_block = False
            out_lines.append(line)
        else:
            if in_bullet_block:
                # flush, then emit this line
                if bullet_lines:
                    out_lines.append(md_bullet_block_to_ul('\n'.join(bullet_lines)))
                    bullet_lines = []
                in_bullet_block = False
            out_lines.append(line)
    if bullet_lines:
        out_lines.append(md_bullet_block_to_ul('\n'.join(bullet_lines)))
    return '\n'.join(out_lines)

# Strip H3 markers (### ...) entirely - we'll convert them to <strong>
md = re.sub(r'^### ([^\n]+)\n', r'<strong>\1</strong>\n', md, flags=re.MULTILINE)

md = replace_bullet_blocks(md)

html = md_to_html(md)

# === Step 2: Insert card placeholders (WP 6122 recipe + extended for H3 prefix) ===
card_anchors = [
    "Field types that work, and the failure modes that don't",
    "Three concrete workflows where this tool earns its keep",
    "How it fits into a larger PDF batch pipeline",
]

# Strip any H2 followed by <strong> then <p> pattern
for i, anchor in enumerate(card_anchors, start=1):
    pattern = re.compile(
        r'(<h2>' + re.escape(anchor) + r'</h2>\s*(?:<strong>[^<]+</strong>\s*)?<p>.*?</p>)',
        re.DOTALL
    )
    placeholder = f'\n<figure class="highlight-card"><img decoding="async" src="PLACEHOLDER_card{i}.png" alt="Card {i}: {anchor}" loading="lazy" /></figure>\n'
    new_html, n = pattern.subn(r'\1' + placeholder, html, count=1)
    assert n == 1, f'card {i} insertion failed for {anchor}'
    html = new_html

# === Step 3: Insert article-poster figure ===
poster_fig = '<figure class="article-poster"><img decoding="async" src="PLACEHOLDER_poster.png" alt="PDF Form Fill Batch field guide cover" /></figure>\n'
m = re.search(r'(<strong>[^<]+</strong>)', html)
assert m, 'lead strong not found'
html = html[:m.start()] + poster_fig + html[m.start():]

# === Step 4: Substitute the uploaded image URLs ===
# Use the existing post_info.json
post_info = json.load(open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/post_info.json'))
for slot, info in post_info['assets'].items():
    html = html.replace(f'PLACEHOLDER_{slot}.png', info['url'])
assert 'PLACEHOLDER' not in html

# === Step 5: Sanity checks ===
print(f'H1: {len(re.findall(r"<h1[^>]*>", html))} (expect 0)')
print(f'H2: {len(re.findall(r"<h2[^>]*>", html))} (expect 8)')
print(f'H3: {len(re.findall(r"<h3[^>]*>", html))} (expect 0)')
print(f'UL: {len(re.findall(r"<ul>", html))} (>=4 expected)')
print(f'LI: {len(re.findall(r"<li>", html))} (>=12 expected)')
print(f'highlight-card: {len(re.findall(r"figure class=.highlight-card.", html))} (expect 3)')

# === Step 6: POST back via WP REST ===
print()
print(f'New content length: {len(html)}')

req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts/6212',
    data=json.dumps({'content': html}).encode(),
    method='POST',
    headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Jarvis-Cron/1.0'}
)
with urllib.request.urlopen(req, timeout=60) as r:
    resp = json.loads(r.read().decode())
print(f'PATCH OK — status: {resp["status"]}, content length: {len(resp["content"]["rendered"])}')

open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_final_patched3.html', 'w').write(html)
print('Saved patched HTML round 3')

# === Step 7: Re-run audit ===
from wp_post_audit import audit_post_content
findings = audit_post_content(resp['content']['rendered'])
print()
print(f'AUDIT FINDINGS: {len(findings)}')
for f in findings:
    print(f'  - {f}')