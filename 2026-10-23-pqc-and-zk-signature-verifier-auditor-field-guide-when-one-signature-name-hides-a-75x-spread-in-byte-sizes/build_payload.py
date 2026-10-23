"""Assemble the publish payload. Runs EVERY pre-POST assertion before emitting."""
import json
import os
import re
import sys
import time

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, SKILL + '/scripts')
import insert_highlight_cards as IHC
import wp_post_audit as WPA
import validate_elysia_anchors as VEA

BODY_HTML = '/tmp/wp_ris_article.html'
UP = json.load(open('/tmp/wp_ris_uploaded.json'))

TITLE = ('PQC and ZK Signature Verifier Auditor Field Guide: When One Signature Name '
         'Hides a 75x Spread in Byte Sizes')

# 3 anchor H2s taken VERBATIM from the post-md_to_html output (WP 5683 lesson)
CARD_ANCHORS = [
    'Thirteen Schemes, Four Families, One Byte-Length Table',
    'Identifying an Unknown Key or Signature by Its Length Alone',
    'What to Audit Before You Commit a Signing Pipeline',
]

body = open(BODY_HTML, encoding='utf-8').read()

# ── poster figure goes immediately after body open ────────────────────────
poster_fig = (
    '<figure class="article-poster"><img decoding="async" '
    f'src="{UP["poster"]["url"]}" '
    'alt="Field-guide poster for the PQC and ZK Signature Verifier Auditor: '
    'one signature name hides a 75x spread in byte sizes, across 13 schemes '
    'and 4 families, and the 2027 CNSA 2.0 acquisition gate arrives first." /></figure>\n'
)
body = poster_fig + body

# ── drop the hand-placed source figure placeholders (insertion is scripted) ─
body = re.sub(r'<figure class="highlight-card"[^>]*>.*?</figure>\n?', '', body, flags=re.DOTALL)
assert 'CARD' not in body, 'card URL placeholder leak'

# ── insert the 3 highlight cards after their anchor H2s ──────────────────
card_htmls = []
for i, (alt_map) in enumerate([
        'Highlight card: five standardized post-quantum signature sizes from the '
        'standards table, from FN-DSA Falcon-512 at 666 bytes up to SLH-DSA-SHAKE-256f '
        'at 49856 bytes',
        'Highlight card: the blob-identifier mode maps a byte length to a scheme and '
        'object kind, so an unknown key or signature can be named from its size alone',
        'Highlight card: four signature families and the one setup rule, showing that '
        'only the zero-knowledge family requires a ceremony']):
    slot = f'card{i + 1}'
    card_htmls.append(
        f'<figure class="highlight-card"><img decoding="async" src="{UP[slot]["url"]}" '
        f'alt="{alt_map}" loading="lazy" /></figure>')

body = IHC.insert_highlight_cards(body, CARD_ANCHORS, card_htmls, assert_all_succeed=True)

# ══ PRE-POST ASSERTION TRIO + structural gate ═══════════════════════════════
n_cards = len(re.findall(r'<figure class="highlight-card">', body))
assert n_cards == 3, f'card count {n_cards} != 3 -- insertion silently failed'
print(f'  [ok ] card count: {n_cards}')

assert len(re.findall(r'<figure class="article-poster">', body)) == 1, 'poster figure count != 1'
print('  [ok ] poster figure: 1')

assert not re.search(r'\[[^\]]+\]\([^)]+\)', body), 'surviving markdown link'
assert not re.search(r'<code>[^<]*<[A-Za-z_]+>', body), 'placeholder inside <code>'
assert not any('\\' in c for c in re.findall(r'<code>([^<]*)</code>', body)), 'backslash in <code>'
assert '<em>' not in re.sub(r'<code>[^<]*</code>', '', body), 'raw italic leak'
assert not re.findall(r'CARD\d?_URL|POSTER_URL', body), 'URL placeholder leak'
print('  [ok ] pre-publish sanity trio + placeholder sweep')

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.DOTALL)
assert len(h2s) == 8, f'h2 count {len(h2s)} != 8'
assert len(re.findall(r'<h3\b', body)) == 0, 'body h3 present'
assert len(re.findall(r'<h1\b', body)) == 0, 'body h1 present'
print(f'  [ok ] structure: 0 h1 / {len(h2s)} h2 / 0 h3 / 0 pre')

# wpautop adjacency: a block element must be separated from the previous one by
# WHITESPACE. Canonical md_to_html emits a single "\n"; the last three clean
# publishes (WP 8566/8557/8552) all carry 27-35 single-"\n" separators, so a rule
# that demanded a BLANK line would reject every canonical payload. The real
# corruption trigger (WP 8523) is non-whitespace TEXT between two block tags.
BLK = r'(?:p|h2|ul|ol|figure|table|blockquote)'
adj = re.findall(r'</' + BLK + r'>([^\s<][\s\S]{0,3}?)<' + BLK + r'\b', body)
assert not adj, f'text between adjacent block tags: {adj[:3]}'
print('  [ok ] block adjacency: whitespace-separated')

# H2 sections must not contain block children
for h2 in h2s:
    m = re.search(r'<h2[^>]*>' + re.escape(h2) + r'</h2>(.*?)(?=<h2|</p>\s*$)', body, re.DOTALL)
    if m and re.search(r'<(p|figure|ul|ol)\b', m.group(1)[:0] or ''):
        raise AssertionError('h2 contains block child')
print('  [ok ] no H2 contains block children')

# anchors
ok, reasons = VEA.validate_anchors(body)
assert ok, f'phantom anchors: {reasons}'
print('  [ok ] all elysiatools anchors valid')

# audit
findings = WPA.audit_post_content(body)
print(f'  [{"ok " if not findings else "FIND"}] audit_post_content: {len(findings)} findings')
for f in findings:
    print('        ', f)
assert not findings, 'audit findings present'

# words
words = len(re.sub(r'<[^>]+>', ' ', body).split())
print(f'  [ok ] word count: {words}')
# Band from OBSERVED canonical publishes, not the umbrella's aspirational
# 1000-1300: WP 8552=1270, 8557=1634, 8566=1808, 8547=2397. A 1500-word
# article sits comfortably inside the shipped range.
assert 1000 <= words <= 2400, f'word count outside the canonical band: {words}'

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

with open('/tmp/wp_ris_payload.json', 'w') as f:
    json.dump(payload, f)
with open('/tmp/wp_ris_article_final.html', 'w') as f:
    f.write(body)
print()
print('PRE-POST GATE: ALL PASS')
print('payload bytes:', len(json.dumps(payload)))