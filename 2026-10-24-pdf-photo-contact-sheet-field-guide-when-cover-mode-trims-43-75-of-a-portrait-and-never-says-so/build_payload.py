#!/usr/bin/env python3.11
"""Build the publish payload: poster + 3 cards, every pre-POST gate asserted."""
import json, os, re, sys, time

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, SKILL + '/scripts')
import insert_highlight_cards as IHC
import wp_post_audit as WPA
import validate_elysia_anchors as VEA

BODY_HTML = '/tmp/wp_jt2600_article.html'
UP = json.load(open('/tmp/wp_jt2600_uploaded.json'))

TITLE = ('PDF Photo Contact Sheet Field Guide: When Cover Mode Trims 43.75% '
         'of a Portrait and Never Says So')

# 3 anchor H2s taken VERBATIM from the post-md_to_html output (WP 5683 lesson).
# Ordered by DOCUMENT POSITION so the cards appear in reading order.
CARD_ANCHORS = [
    'Cover Crops 43.75% Off a Portrait Frame',
    'Twelve Cells, Ten Photos, Two Empty Ones',
    'Seven EXIF Fields, Four Printed Lines',
]

body = open(BODY_HTML, encoding='utf-8').read()

# ── poster figure goes immediately after body open ───────────────────────
poster_fig = (
    '<figure class="article-poster"><img decoding="async" '
    f'src="{UP["poster"]["url"]}" '
    'alt="Field-guide poster for the PDF Photo Contact Sheet: a 4:3 thumbnail '
    'grid where cover mode trims 43.75 percent of a portrait frame." /></figure>\n'
)
body = poster_fig + body

# ── clean the md_to_html '<p></ul></p>' artifact ─────────────────────────
before = body.count('<p></ul></p>')
body = body.replace('<p></ul></p>', '</ul>').replace('<p></ol></p>', '</ol>')
print(f'  [ok ] cleaned <p></ul></p> artifacts: {before}')

# ── drop any hand-placed source figure placeholders (insertion is scripted)
body = re.sub(r'<figure class="highlight-card"[^>]*>.*?</figure>\n?', '', body, flags=re.DOTALL)
assert 'CARD' not in re.sub(r'card[123]-72\.png', '', body), 'card placeholder leak'

# ── insert the 3 highlight cards after their anchor H2s ──────────────────
CARD_SPECS = [
    ('card1', 'Highlight card: what cover mode removes from four frame shapes - '
              '43.75 percent of a 3:4 portrait height, 25 percent of a square, '
              '25 percent of a 16:9 width, and 0 percent from a native 4:3 frame.'),
    ('card2', 'Highlight card: the bundled example cell by cell - ten sample '
              'images at 4 columns by 3 rows give 12 cells per sheet, 10 cells '
              'used and 2 empty, with the header reading Sheet 1, items 1 to 10.'),
    ('card3', 'Highlight card: seven EXIF fields are read but only four lines '
              'are printed - camera, lens, aperture and ISO always print, while '
              'shutter speed, focal length and the capture timestamp are always cut.'),
]
card_htmls = []
for slot, alt in CARD_SPECS:
    card_htmls.append(
        f'<figure class="highlight-card"><img decoding="async" src="{UP[slot]["url"]}" '
        f'alt="{alt}" loading="lazy" /></figure>')

body = IHC.insert_highlight_cards(body, CARD_ANCHORS, card_htmls, assert_all_succeed=True)

# ══ PRE-POST ASSERTION TRIO + structural gate ═══════════════════════════
n_cards = len(re.findall(r'<figure class="highlight-card">', body))
assert n_cards == 3, f'card count {n_cards} != 3 -- insertion silently failed'
print(f'  [ok ] card count: {n_cards}')

assert len(re.findall(r'<figure class="article-poster">', body)) == 1, 'poster figure count != 1'
print('  [ok ] poster figure: 1')

assert not re.search(r'\[[^\]]+\]\([^)]+\)', body), 'surviving markdown link'
assert not re.search(r'<code>[^<]*<[A-Za-z_]+>', body), 'placeholder inside <code>'
assert not any(chr(92) in c for c in re.findall(r'<code>([^<]*)</code>', body)), 'backslash in <code>'
assert '<em>' not in re.sub(r'<code>[^<]*</code>', '', body), 'raw italic leak'
assert not re.findall(r'CARD[123]?_URL|POSTER_URL|PLACEHOLDER_', body), 'URL placeholder leak'
print('  [ok ] pre-publish sanity trio + placeholder sweep')

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.DOTALL)
assert len(h2s) == 8, f'h2 count {len(h2s)} != 8'
assert len(re.findall(r'<h3\b', body)) == 0, 'body h3 present'
assert len(re.findall(r'<h1\b', body)) == 0, 'body h1 present'
print(f'  [ok ] structure: 0 h1 / {len(h2s)} h2 / 0 h3')

BLK = r'(?:p|h2|ul|ol|figure|table|blockquote)'
adj = re.findall(r'</' + BLK + r'>([^\s<][\s\S]{0,3}?)<' + BLK + r'\b', body)
assert not adj, f'text between adjacent block tags: {adj[:3]}'
print('  [ok ] block adjacency: whitespace-separated')

p_open = len(re.findall(r'<p\b', body))
p_close = len(re.findall(r'</p>', body))
assert p_open == p_close, f'p imbalance {p_open}/{p_close}'
assert not re.findall(r'<p></p>', body), 'empty <p></p> shells present'
print(f'  [ok ] p balance: {p_open}/{p_close}, 0 empty p')

stack, outside = [], 0
for m in re.finditer(r'<(/?)(ul|ol|li)\b[^>]*>', body):
    closing, tag = m.group(1), m.group(2)
    if tag in ('ul', 'ol'):
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
        else:
            stack.append(tag)
    else:
        if not closing and not stack:
            outside += 1
assert not stack, f'unclosed list containers: {stack}'
assert outside == 0, f'{outside} <li> outside any list'
print('  [ok ] list balance: 0 outside, 0 unclosed')

# every <img> has an alt
for m in re.finditer(r'<img\b[^>]*>', body):
    tag = m.group(0)
    assert 'alt="' in tag, f'img without alt: {tag[:120]}'
print('  [ok ] every img has alt')

ok, reasons = VEA.validate_anchors(body)
assert ok, f'phantom anchors: {reasons}'
print('  [ok ] all elysiatools anchors valid')

findings = WPA.audit_post_content(body)
print(f'  [{"ok " if not findings else "FIND"}] audit_post_content: {len(findings)} findings')
for f in findings:
    print('        ', f)
assert not findings, 'audit findings present'

words = len(re.sub(r'<[^>]+>', ' ', body).split())
print(f'  [ok ] word count: {words}')
assert 1000 <= words <= 2400, f'word count outside the canonical band: {words}'

# every uploaded URL present in the body
for slot in ('poster', 'card1', 'card2', 'card3'):
    assert UP[slot]['url'] in body, f'{slot} url missing from body'
print('  [ok ] all 4 uploaded URLs present in body')

payload = {
    'title': TITLE,
    'content': body,
    'status': 'publish',
    'date_gmt': os.environ.get('DATE_GMT', 'NOW'),
    'featured_media': 0,
}
if payload['date_gmt'] == 'NOW':
    payload['date_gmt'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
print(f'  [ok ] date_gmt: {payload["date_gmt"]}')
print(f'  [ok ] featured_media: 0')

with open('/tmp/wp_jt2600_payload.json', 'w') as f:
    json.dump(payload, f)
with open('/tmp/wp_jt2600_article_final.html', 'w', encoding='utf-8') as f:
    f.write(body)
print()
print('PRE-POST GATE: ALL PASS')
print('payload bytes:', len(json.dumps(payload)))
print('title:', TITLE)
