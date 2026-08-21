#!/usr/bin/env python3.11
"""PATCH WP 6212 (round 2): convert 4 merged-bullet <p> to <ul><li>."""
import json, base64, urllib.request, re, html as htmllib

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
basic = base64.b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
AUTH = f'Basic {basic}'

# Fetch current content (post round-1 PATCH already applied)
req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts/6212?context=edit&_fields=id,content',
    headers={'Authorization': AUTH, 'User-Agent': 'Jarvis-Cron/1.0'}
)
with urllib.request.urlopen(req, timeout=30) as r:
    post = json.loads(r.read().decode())

content = post['content']['raw']
print(f'Raw content length: {len(content)}')

# Find all <p> with >= 2 en-dash + strong patterns and split
para_pat = re.compile(r'<p>(.*?)</p>', re.DOTALL)

def split_para(m):
    inner = m.group(1)
    n_dashes = len(re.findall(r'&#8211;', inner))
    n_strong = len(re.findall(r'<strong>', inner))
    if n_dashes < 2 or n_strong < 2:
        return m.group(0)  # unchanged
    # Split on en-dash + lookahead for <strong>
    parts = re.split(r'\s*&#8211;\s*(?=<strong>)', inner)
    items = []
    for p in parts:
        p = p.strip()
        if p:
            items.append(f'<li>{p}</li>')
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

new_content, n = para_pat.subn(split_para, content)
print(f'Merged-bullet <p> splits: {n}')

# === Sanity checks ===
print()
print('=== POST-PATCH CHECKS ===')
print(f'H1 count: {len(re.findall(r"<h1[^>]*>", new_content))} (expect 0)')
print(f'H2 count: {len(re.findall(r"<h2[^>]*>", new_content))} (expect 8)')
print(f'H3 count: {len(re.findall(r"<h3[^>]*>", new_content))} (expect 0)')
print(f'UL count: {len(re.findall(r"<ul>", new_content))}')
print(f'Highlight cards: {len(re.findall(r"figure class=.highlight-card.", new_content))} (expect 3)')

# === POST back ===
req = urllib.request.Request(
    f'{WP_URL}/wp-json/wp/v2/posts/6212',
    data=json.dumps({'content': new_content}).encode(),
    method='POST',
    headers={'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Jarvis-Cron/1.0'}
)
with urllib.request.urlopen(req, timeout=60) as r:
    resp = json.loads(r.read().decode())
print(f'PATCH OK — status: {resp["status"]}, content length: {len(resp["content"]["rendered"])}')

open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_final_patched2.html', 'w').write(new_content)
print('Saved patched HTML round 2')

# === Re-run audit ===
import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
from wp_post_audit import audit_post_content
findings = audit_post_content(resp['content']['rendered'])
print()
print(f'AUDIT FINDINGS: {len(findings)}')
for f in findings:
    print(f'  - {f}')