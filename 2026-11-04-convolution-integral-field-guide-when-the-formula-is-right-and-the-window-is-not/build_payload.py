#!/usr/bin/env python3.11
"""Build the final POST payload with the real uploaded media URLs."""
import json
import re
import sys

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, f'{SKILL}/scripts')
sys.path.insert(0, f'{SKILL}/templates')

from safe_md_to_html import safe_md_to_html                      # noqa: E402
from pre_encode_backslash import pre_encode_backslash             # noqa: E402
from pre_encode_code_spans import pre_encode_code_spans           # noqa: E402
from insert_highlight_cards import insert_highlight_cards         # noqa: E402
from validate_elysia_anchors import validate_anchors             # noqa: E402

MD_PATH = '/tmp/wp_conv_article_20261104.md'
OUT_HTML = '/tmp/wp_conv_article_final_20261104.html'
OUT_PAYLOAD = '/tmp/wp_conv_payload_20261104.json'
MEDIA_JSON = '/tmp/wp_conv_media_20261104.json'

TITLE = ("Convolution Integral Field Guide: When the Formula Is Right "
         "and the Window Is Not")
SLUG = ('convolution-integral-field-guide-when-the-formula-is-right-and-the-window-is-not')
DATE_GMT = sys.argv[1] if len(sys.argv) > 1 else None
if not DATE_GMT:
    raise SystemExit('usage: build_payload.py <YYYY-MM-DDTHH:MM:SS>')

media = json.load(open(MEDIA_JSON))
URLS = {k: v['url'] for k, v in media.items()}
print('media URLs:', json.dumps(URLS, indent=2))

ALT = {
    'poster': 'Convolution integral field guide: the formula is right but the integration window is not',
    'card1': 'Five output points from one convolution run showing the error growing as t passes the window bound',
    'card2': 'Side by side comparison of the same convolution with a narrow window and a wide window',
    'card3': 'Four limits of one convolution run including rounding, empty range, true zero and window clipping',
}

CARD_ANCHORS = [
    'The 20 percent error hiding behind a correct formula',
    'Two windows, one expression',
    'When the output says zero',
]

md = open(MD_PATH).read()
md2 = pre_encode_backslash(pre_encode_code_spans(md))
html = safe_md_to_html(md2)
assert len(re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)) == 8

html = (
    f'<figure class="article-poster"><img decoding="async" src="{URLS["poster"]}" '
    f'alt="{ALT["poster"]}" /></figure>' + html
)

card_htmls = [
    f'<figure class="highlight-card"><img decoding="async" src="{URLS["card1"]}" '
    f'alt="{ALT["card1"]}" loading="lazy" /></figure>',
    f'<figure class="highlight-card"><img decoding="async" src="{URLS["card2"]}" '
    f'alt="{ALT["card2"]}" loading="lazy" /></figure>',
    f'<figure class="highlight-card"><img decoding="async" src="{URLS["card3"]}" '
    f'alt="{ALT["card3"]}" loading="lazy" /></figure>',
]
html = insert_highlight_cards(html, CARD_ANCHORS, card_htmls, assert_all_succeed=True)

n_cards = len(re.findall(r'<figure class="highlight-card">', html))
assert n_cards == 3, f'card count {n_cards} != 3'
print(f'card count: {n_cards} -- PASS')

problems = []
if re.findall(r'\[[^\]]+\]\((https?://[^\s\)]+)\)', html):
    problems.append('markdown links survive')
if re.findall(r'<code>[^<]*<[a-zA-Z/][^<]*</code>', html):
    problems.append('placeholder HTML inside <code>')
if [c for c in re.findall(r'<code>([^<]*)</code>', html) if '\\' in c]:
    problems.append('literal backslash in <code>')
if re.findall(r'<p[^>]*>[^<]*<br\s*/?>[^<]*</p>', html):
    problems.append('<br /> inside <p>')
if re.findall(r'<p>(?:(?!</p>).)*?(?:&#8211;|&ndash;|—)\s*<strong>', html, re.DOTALL):
    problems.append('merged bullet risk')
if re.findall(r'<p></p>', html):
    problems.append('empty <p></p> shells')
if len(re.findall(r'<p\b', html)) != len(re.findall(r'</p>', html)):
    problems.append('<p> imbalance')
for tok in ('CARD1_URL', 'CARD2_URL', 'CARD3_URL', 'CARD_URL', 'POSTER_URL'):
    if tok in html:
        problems.append(f'placeholder leak: {tok}')
if re.findall(r'<code>[^<]*<(?:h1|h2|h3|p|div|img|button|a|span)[^<]*</code>', html):
    problems.append('literal HTML in <code>')
if re.findall(r'<p>[^<]*\*[^*<]+\*[^<]*</p>', html):
    problems.append('raw italic markers')
if re.findall(r'<p>[^<]*\|[^<]*\|[^<]*</p>', html):
    problems.append('GFM pipe-table leak')
if re.findall(r'<code>[^<]*<em>[^<]*</em>[^<]*</code>', html):
    problems.append('<em> inside <code>')
for tag in ('h2', 'h3', 'ul', 'ol', 'li', 'figure', 'code', 'strong', 'em', 'a'):
    o = len(re.findall(rf'<{tag}\b', html))
    c = len(re.findall(rf'</{tag}>', html))
    if o != c:
        problems.append(f'<{tag}> imbalance: {o} vs {c}')
if len(re.findall(r'<h1\b', html)):
    problems.append('body H1 present')
if len(re.findall(r'<h3\b', html)):
    problems.append('body H3 present')
if len(re.findall(r'<pre\b', html)):
    problems.append('pre block present')

print('\n--- anchor validation ---')
ok, reasons = validate_anchors(html)
if not ok:
    problems.append(f'phantom anchors: {reasons}')

print('\n--- pre-POST gate ---')
if problems:
    for p in problems:
        print('  FAIL', p)
    sys.exit(1)
print('  ALL PRE-POST CHECKS PASS')

# every media URL must appear in the body
for slot, url in URLS.items():
    assert url in html, f'{slot} URL missing from body'
print('  all 4 media URLs present in body')

payload = {
    'title': TITLE,
    'content': html,
    'status': 'publish',
    'slug': SLUG,
    'date_gmt': DATE_GMT,       # ONLY date_gmt — never `date` (WP 8592)
    'featured_media': 0,        # COSESAI non-negotiable
}
assert payload['status'] == 'publish'
assert 'date' not in payload
json.dump(payload, open(OUT_PAYLOAD, 'w'), indent=2, ensure_ascii=False)
open(OUT_HTML, 'w').write(html)

print(f'\nHTML length: {len(html)}')
print(f'h2={len(re.findall(r"<h2", html))} h3={len(re.findall(r"<h3", html))} '
      f'cards={n_cards} poster=1')
print(f'Payload written: {OUT_PAYLOAD}')
print(f'date_gmt: {DATE_GMT}')
