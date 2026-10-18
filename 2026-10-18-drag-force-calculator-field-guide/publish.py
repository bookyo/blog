#!/usr/bin/env python3.11
"""Build final HTML body with poster + 3 highlight-card figures, then publish."""
import sys, os, json, re, time
import requests
from requests.auth import HTTPBasicAuth

sys.path.insert(0, '/Users/quyue/.hermes/skills/article-writer/scripts')
from md_to_html import md_to_html, fix_md_to_html_output

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'

OUT_DIR = '/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide'

# Load article markdown -> HTML
md = open(f'{OUT_DIR}/article.md').read()
body_html = md_to_html(md)
body_html = fix_md_to_html_output(body_html)

# Load uploaded.json for media IDs/URLs
uploaded = json.load(open(f'{OUT_DIR}/uploaded.json'))
poster_url = uploaded['drag-force-calculator-poster.png']['url']
card1_url  = uploaded['drag-force-calculator-card1.png']['url']
card2_url  = uploaded['drag-force-calculator-card2.png']['url']
card3_url  = uploaded['drag-force-calculator-card3.png']['url']

# 1. Inject poster figure immediately after first <p> (which contains the lead phrase)
poster_fig = (
    f'<figure class="article-poster"><img decoding="async" src="{poster_url}" '
    f'alt="Drag force calculator field guide cover" /></figure>'
)

# Insert poster at top of body (before first <p>)
first_p_idx = body_html.find('<p>')
body_html = body_html[:first_p_idx] + poster_fig + '\n' + body_html[first_p_idx:]

# 2. Insert 3 highlight-card figures AFTER chosen H2 anchors
# Canonical recipe (WP 6122): anchor on H2 followed by opening <p>...</p>
def insert_card_after_h2(body, anchor_text, card_url, alt_text):
    card_fig = (
        f'<figure class="highlight-card"><img decoding="async" src="{card_url}" '
        f'alt="{alt_text}" loading="lazy" /></figure>'
    )
    pattern = re.compile(
        r'(<h2>' + re.escape(anchor_text) + r'</h2>\s*\n?\s*<p>.*?</p>)',
        re.DOTALL
    )
    new_body, n = pattern.subn(r'\1\n' + card_fig, body, count=1)
    assert n == 1, f'card insertion failed for {anchor_text}'
    return new_body

# Choose 3 of the 8 H2s as card anchors
body_html = insert_card_after_h2(
    body_html,
    'Why the Drag Coefficient Lives in a Library, Not a Lookup Table',
    card1_url,
    'Five drag coefficient values for common shapes',
)
body_html = insert_card_after_h2(
    body_html,
    'Common Failure Modes and How to Catch Them',
    card2_url,
    'Five validation checks for drag force calculations',
)
body_html = insert_card_after_h2(
    body_html,
    'Unit Conversions Make or Break the Plug-In Calculation',
    card3_url,
    'Same sphere in air water seawater glycerin',
)

# Save final HTML
open(f'{OUT_DIR}/article_final.html', 'w').write(body_html)

# Pre-POST checks (WP 6122 + WP 6197 lessons)
assert len(re.findall(r'<figure class="article-poster">', body_html)) == 1, 'poster count != 1'
n_cards = len(re.findall(r'<figure class="highlight-card">', body_html))
assert n_cards == 3, f'card count {n_cards} != 3'
n_h2 = len(re.findall(r'<h2[^>]*>', body_html))
assert n_h2 == 8, f'H2 count {n_h2} != 8'
n_h1 = len(re.findall(r'<h1[^>]*>', body_html))
assert n_h1 == 0, f'H1 count {n_h1} != 0'
n_h3 = len(re.findall(r'<h3[^>]*>', body_html))
assert n_h3 == 0, f'H3 count {n_h3} != 0'
# Anchor link check
elysia_anchors = re.findall(r'<a href="(https://elysiatools.com/[^"]+)"', body_html)
print(f'  elysia anchors: {len(elysia_anchors)}: {elysia_anchors}')
# No phantom placeholders
for tok in ('POSTER_URL', 'CARD_URL', 'CARD1_URL', 'CARD2_URL', 'CARD3_URL'):
    assert tok not in body_html, f'placeholder leak: {tok}'
print('All pre-POST assertions passed')

# Build POST payload (WP 5628: featured_media MUST be 0)
date_gmt = '2026-10-18T14:30:00'
title = (
    'Drag Force Calculator Field Guide: When Four Numbers Decide '
    'Whether a Clean Formula Returns a Clean Lie (2026-10-18)'
)
slug = (
    'drag-force-calculator-field-guide-when-four-numbers-stack-on-top-of-one-formula-and-a-reynolds-check-decides-whether-the-answer-is-right-2026-10-18'
)

payload = {
    'title': title,
    'slug': slug,
    'status': 'publish',
    'date_gmt': date_gmt,
    'featured_media': 0,
    'content': body_html,
}

print()
print('POSTing article...')
session = requests.Session()
session.trust_env = False

for attempt in range(3):
    try:
        r = session.post(
            f'{WP_URL}/wp-json/wp/v2/posts',
            auth=HTTPBasicAuth(WP_USER, WP_PASS),
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
            json=payload,
            timeout=60,
        )
        if r.status_code in (200, 201):
            data = r.json()
            post_id = data['id']
            post_link = data['link']
            post_status = data['status']
            post_slug = data['slug']
            print(f'  POST OK [{post_id}] status={post_status} slug={post_slug}')
            print(f'  Link: {post_link}')
            break
        else:
            print(f'  HTTP {r.status_code}: {r.text[:300]}')
            if attempt == 2:
                sys.exit(1)
            time.sleep(2 * (attempt + 1))
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print(f'  SSL/conn error attempt {attempt+1}: {type(e).__name__}')
        if attempt == 2:
            raise
        time.sleep(2 * (attempt + 1))

# Save posted.json
with open(f'{OUT_DIR}/posted.json', 'w') as f:
    json.dump({
        'post_id': post_id,
        'post_link': post_link,
        'post_status': post_status,
        'post_slug': post_slug,
        'date_gmt': date_gmt,
    }, f, indent=2)

# If status came back as 'future', PATCH to 'publish'
if post_status != 'publish':
    print(f'POST returned status={post_status}; PATCHing to publish...')
    r = session.post(
        f'{WP_URL}/wp-json/wp/v2/posts/{post_id}',
        auth=HTTPBasicAuth(WP_USER, WP_PASS),
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
        json={'status': 'publish'},
        timeout=60,
    )
    print(f'  PATCH HTTP {r.status_code}: status={r.json().get("status")}')

print()
print('=' * 70)
print('PUBLISHED')
print(f'  ID: {post_id}')
print(f'  Slug: {post_slug}')
print(f'  Link: {post_link}')
print(f'  Date GMT: {date_gmt}')
