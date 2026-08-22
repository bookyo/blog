#!/usr/bin/env python3.11
"""Substitute uploaded URLs into HTML, verify pre-publish checks, then POST to WP.

Per WP 6197: use FULL source_url from upload response (already includes /2026/08/ prefix).
Per WP 6122: assert exactly 3 highlight-card figures in final payload before POST.
Per WP 5683 lesson: featured_media MUST be 0.
Per WP 6261 (latest clean post): use current UTC date_gmt.
"""
import sys, os, re, json, subprocess, time
import requests
from requests.auth import HTTPBasicAuth

sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
import wp_post_audit as wpa

WP_URL = wpa.DEFAULT_WP_URL
WP_USER = wpa.DEFAULT_USER
WP_PASS = wpa.DEFAULT_PASS

HTML_PATH = '/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/article_final.html'
UPLOADED_PATH = '/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/uploaded.json'

html = open(HTML_PATH).read()
uploaded = json.load(open(UPLOADED_PATH))

# Substitute poster URL
poster_url = uploaded['graphql-playground-poster.png']['url']
html = html.replace('PLACEHOLDER_poster.png', poster_url)
# Substitute card URLs
for i, slot in enumerate(['graphql-playground-card1.png', 'graphql-playground-card2.png', 'graphql-playground-card3.png']):
    placeholder = f'PLACEHOLDER_card{i+1}.png'
    url = uploaded[slot]['url']
    html = html.replace(placeholder, url)

# Mandatory pre-POST check (WP 6122): exactly 3 highlight-card figures
n_cards = len(re.findall(r'<figure class="highlight-card">', html))
assert n_cards == 3, f'Must have exactly 3 highlight-card figures, got {n_cards}'
n_poster = len(re.findall(r'<figure class="article-poster">', html))
assert n_poster == 1, f'Must have exactly 1 article-poster figure, got {n_poster}'
assert 'PLACEHOLDER' not in html, 'Placeholder strings remain in HTML'

# Audit content one more time
findings = wpa.audit_post_content(html)
print(f'Audit findings: {len(findings)}')
for f in findings:
    print(f'  - {f}')
assert len(findings) == 0, 'Audit failed pre-POST'

# Build title and slug
TITLE = 'GraphQL Playground Field Guide: When One Tab Beats curl for Schema Iteration'
SLUG = 'graphql-playground-field-guide-when-one-tab-beats-curl-for-schema-iteration'

# Current UTC date_gmt
import datetime
now_utc = datetime.datetime.utcnow()
DATE_GMT = now_utc.strftime('%Y-%m-%dT%H:%M:%S')
print(f'date_gmt: {DATE_GMT}')

# Build payload
payload = {
    'title': TITLE,
    'slug': SLUG,
    'status': 'publish',
    'date_gmt': DATE_GMT,
    'featured_media': 0,  # COSESAI theme hero duplication prevention (WP 5628)
    'content': html,
    'excerpt': 'A field guide for GraphQL Playground: when an in-browser client beats curl and Postman for schema iteration, mutation pre-flight checks, and live introspection.',
}

# POST
session = requests.Session()
session.trust_env = False
print(f'POSTing to {WP_URL}/wp-json/wp/v2/posts ...')
for attempt in range(3):
    try:
        r = session.post(
            f'{WP_URL}/wp-json/wp/v2/posts',
            auth=HTTPBasicAuth(WP_USER, WP_PASS),
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
            json=payload,
            timeout=60,
        )
        print(f'  HTTP {r.status_code}')
        if r.status_code in (200, 201):
            data = r.json()
            print(f'  POST OK: id={data.get("id")}, slug={data.get("slug")}, link={data.get("link")}')
            print(f'  status={data.get("status")}, date_gmt={data.get("date_gmt")}')
            print(f'  featured_media={data.get("featured_media")}')
            with open('/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/posted.json', 'w') as f:
                json.dump({'id': data['id'], 'slug': data['slug'], 'link': data['link'], 'status': data.get('status'), 'date_gmt': data.get('date_gmt')}, f, indent=2)
            break
        else:
            print(f'  FAILED: {r.text[:500]}')
            sys.exit(1)
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
        print(f'  SSL/conn error attempt {attempt+1}: {type(e).__name__}')
        if attempt == 2:
            raise
        time.sleep(2 * (attempt + 1))

print('\nDONE.')