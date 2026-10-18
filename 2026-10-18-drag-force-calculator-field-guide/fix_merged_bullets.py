#!/usr/bin/env python3.11
"""PATCH post 8492 — find merged-bullet paragraphs (with literal `- <strong>`)
and convert them to proper <ul><li> lists.
"""
import sys, re, time
import requests
from requests.auth import HTTPBasicAuth

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
POST_ID = 8492

session = requests.Session()
session.trust_env = False

# Fetch raw content
print('Fetching raw content...')
r = session.get(
    f'{WP_URL}/wp-json/wp/v2/posts/{POST_ID}?context=edit',
    auth=HTTPBasicAuth(WP_USER, WP_PASS),
    headers={'User-Agent': 'Mozilla/5.0'},
    timeout=30,
)
raw = r.json()['content']['raw']
print(f'  raw length: {len(raw)}')

# Find paragraphs that contain multiple `- <strong>` markers
# Pattern: a paragraph that starts with text (no `<ul>`) and has 2+ occurrences of `- <strong>`
def find_merged_paragraphs(content):
    """Find <p> blocks with 2+ occurrences of `- <strong>` that aren't already in a <ul>."""
    matches = []
    for p_match in re.finditer(r'<p>(.*?)</p>', content, re.DOTALL):
        inner = p_match.group(1)
        # Count leading-hyphen + <strong> pairs
        leads = re.findall(r'(?:^|\s)-\s*<strong>', inner)
        if len(leads) >= 2:
            matches.append(p_match)
    return matches

merged = find_merged_paragraphs(raw)
print(f'Found merged paragraphs: {len(merged)}')

# Convert each merged paragraph to <ul><li>
def convert_to_list(p_match):
    inner = p_match.group(1)
    # Split on `- <strong>` markers
    parts = re.split(r'(?:^|(?<=\s))-\s*(?=<strong>)', inner)
    items = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not part.startswith('<strong>'):
            # Could be a leading sentence
            continue
        items.append(f'<li>{part}</li>')
    if not items:
        return p_match.group(0)
    return '<ul>' + ''.join(items) + '</ul>'

# Apply fix
def fix_merged(content):
    out = []
    last_end = 0
    for p_match in re.finditer(r'<p>(.*?)</p>', content, re.DOTALL):
        inner = p_match.group(1)
        leads = re.findall(r'(?:^|\s)-\s*<strong>', inner)
        if len(leads) >= 2:
            out.append(content[last_end:p_match.start()])
            out.append(convert_to_list(p_match))
            last_end = p_match.end()
    out.append(content[last_end:])
    return ''.join(out)

fixed = fix_merged(raw)
print(f'After fix: len {len(fixed)} (was {len(raw)})')

# Verify no merged remain
remaining = find_merged_paragraphs(fixed)
print(f'Remaining merged: {len(remaining)}')
print(f'<ul> count: {fixed.count("<ul>")}')
print(f'<li> count: {fixed.count("<li>")}')

open('/tmp/wp_8492_fixed.html', 'w').write(fixed)

# POST back
print()
print('POSTing back...')
r = session.post(
    f'{WP_URL}/wp-json/wp/v2/posts/{POST_ID}',
    auth=HTTPBasicAuth(WP_USER, WP_PASS),
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
    json={'content': fixed, 'status': 'publish'},
    timeout=60,
)
print(f'  HTTP {r.status_code}')
print(f'  status={r.json().get("status")}')
