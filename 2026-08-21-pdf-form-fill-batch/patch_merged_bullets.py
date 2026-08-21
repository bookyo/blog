#!/usr/bin/env python3.11
"""PATCH WP 6212 to fix merged-bullet defect and convert H3 to <strong>."""
import json, base64, urllib.request, urllib.error, re

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
basic = base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
AUTH = f'Basic {basic}'

# Fetch current content via context=edit (so we get raw HTML)
req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts/6212?context=edit&_fields=id,content',
    headers={'Authorization': AUTH, 'User-Agent': 'Jarvis-Cron/1.0'}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read().decode())

content = post['content']['raw']
print('Raw content length:', len(content))
print()

# === Fix 1: Convert all body <h3>...</h3> to <strong>...</strong> ===
# Per umbrella: "No body <h3> (use <strong> for sub-headings)"
before_h3 = len(re.findall(r'<h3[^>]*>', content))
content = re.sub(r'<h3[^>]*>([^<]+)</h3>', r'<strong>\1</strong>', content)
after_h3 = len(re.findall(r'<h3[^>]*>', content))
print(f'H3 conversion: {before_h3} -> {after_h3}')

# === Fix 2: Split merged-bullet <p> blocks into <ul><li> ===
# Pattern: <p>– <strong>X</strong> ... – <strong>Y</strong> ... </p>
# Use .*? DOTALL for the body between dashes (WP 5738 recipe)
merged_pat = re.compile(
    r'<p>((?:&#8211;|&#8212;|–|—)\s*<strong>.*?</strong>(?:.*?)(?:&#8211;|&#8212;|–|—)\s*<strong>.*?</strong>.*?)</p>',
    re.DOTALL
)

def split_merged_para(m):
    inner = m.group(1)
    # Split on dash + <strong> boundary
    parts = re.split(r'\s*(?:&#8211;|&#8212;|–|—)\s*(?=<strong>)', inner)
    items = []
    for p in parts:
        p = p.strip()
        if p:
            items.append(f'<li>{p}</li>')
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

new_content, n = merged_pat.subn(split_merged_para, content)
print(f'Merged-bullet splits: {n}')

# === Sanity ===
print()
print('=== POST-PATCH CHECKS ===')
print(f'H1 count: {len(re.findall(r"<h1[^>]*>", new_content))} (expect 0)')
print(f'H2 count: {len(re.findall(r"<h2[^>]*>", new_content))} (expect 8)')
print(f'H3 count: {len(re.findall(r"<h3[^>]*>", new_content))} (expect 0)')
print(f'UL count: {len(re.findall(r"<ul>", new_content))}')
print(f'Highlight cards: {len(re.findall(r"figure class=.highlight-card.", new_content))} (expect 3)')

# === POST back via POST (NOT PATCH per WP REST API) ===
print()
print(f'New content length: {len(new_content)}')
req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts/6212',
    data=json.dumps({'content': new_content}).encode(),
    method='POST',
    headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Jarvis-Cron/1.0'}
)
with urllib.request.urlopen(req, timeout=60) as r:
    resp = json.loads(r.read().decode())
print(f'PATCH OK — status: {resp["status"]}, content length: {len(resp["content"]["rendered"])}')

# Save patched HTML to archive
open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_final_patched.html', 'w').write(new_content)
print('Saved patched HTML')