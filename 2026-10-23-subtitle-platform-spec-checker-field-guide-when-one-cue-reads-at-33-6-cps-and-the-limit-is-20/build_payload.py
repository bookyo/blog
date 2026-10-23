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

BODY_HTML = '/tmp/wp_subtitle_article.html'
UP = json.load(open('/tmp/wp_sub_uploaded.json'))

TITLE = ('Subtitle Platform Spec Checker Field Guide: When One Cue Reads at '
         '33.6 CPS and the Limit Is 20')

# 3 anchor H2s taken VERBATIM from the post-md_to_html output (WP 5683 lesson).
# Ordered by DOCUMENT POSITION so the cards appear in reading order.
CARD_ANCHORS = [
	'Reading Speed Is the Rule That Actually Breaks Files',
	'Fail Versus Warn: What Each Grade Actually Means',
	'The Platform Profiles Side by Side',
]

body = open(BODY_HTML, encoding='utf-8').read()

# ── poster figure goes immediately after body open ────────────────────────
poster_fig = (
	'<figure class="article-poster"><img decoding="async" '
	f'src="{UP["poster"]["url"]}" '
	'alt="Field-guide poster for the Subtitle Platform Spec Checker: one file '
	'measured against four delivery specs, where a cue of 84 characters over '
	'2.5 seconds reads at 33.6 CPS against a 20 CPS limit." /></figure>\n'
)
body = poster_fig + body

# ── clean the md_to_html '<p></ul></p>' artifact (empty <p> around </ul>) ──
before = body.count('<p></ul></p>')
body = body.replace('<p></ul></p>', '</ul>').replace('<p></ol></p>', '</ol>')
print(f'  [ok ] cleaned <p></ul></p> artifacts: {before}')

# ── drop any hand-placed source figure placeholders (insertion is scripted) ─
body = re.sub(r'<figure class="highlight-card"[^>]*>.*?</figure>\n?', '', body, flags=re.DOTALL)
assert 'CARD' not in body, 'card URL placeholder leak'

# ── insert the 3 highlight cards after their anchor H2s ──────────────────
# slot order follows DOCUMENT order: CPS card -> checks card -> profiles card
CARD_SPECS = [
	('card3', 'Highlight card: the one number that fails a subtitle file - a cue '
	          'of 84 characters over 2.5 seconds reads at 33.6 CPS against the 20 '
	          'CPS adult limit, and extending the same cue to 4.2 seconds makes it '
	          'pass at 20.0 CPS without changing a word'),
	('card2', 'Highlight card: five checks that run on every platform profile - '
	          'reading speed at 20 CPS, 42-character line width, a two-line maximum, '
	          'a 7 second duration ceiling and a 2-frame gap between cues'),
	('card1', 'Highlight card: four platform profiles and their headline limits - '
	          'Netflix adult at 20 CPS, Netflix children at 17 CPS, BBC television at '
	          '37 characters per line and 160-180 wpm, and YouTube as plain UTF-8 '
	          'with markup reported as a warning'),
]
card_htmls = []
for slot, alt in CARD_SPECS:
	card_htmls.append(
		f'<figure class="highlight-card"><img decoding="async" src="{UP[slot]["url"]}" '
		f'alt="{alt}" loading="lazy" /></figure>')

body = IHC.insert_highlight_cards(body, CARD_ANCHORS, card_htmls, assert_all_succeed=True)

# ══ PRE-POST ASSERTION TRIO + structural gate ═══════════════════════════════
n_cards = len(re.findall(r'<figure class="highlight-card">', body))
assert n_cards == 3, f'card count {n_cards} != 3 -- insertion silently failed'
print(f'  [ok ] card count: {n_cards}')

assert len(re.findall(r'<figure class="article-poster">', body)) == 1, 'poster figure count != 1'
print('  [ok ] poster figure: 1')

assert not re.search(r'\[[^\]]+\]\([^)]+\)', body), 'surviving markdown link'
assert not re.search(r'<code>[^<]*<[A-Za-z_]+>', body), 'placeholder inside <code>'
assert not any(chr(92) in c for c in re.findall(r'<code>([^<]*)</code>', body)), 'backslash in <code>'
assert '<em>' not in re.sub(r'<code>[^<]*</code>', '', body), 'raw italic leak'
assert not re.findall(r'CARD\d?_URL|POSTER_URL', body), 'URL placeholder leak'
print('  [ok ] pre-publish sanity trio + placeholder sweep')

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.DOTALL)
assert len(h2s) == 8, f'h2 count {len(h2s)} != 8'
assert len(re.findall(r'<h3\b', body)) == 0, 'body h3 present'
assert len(re.findall(r'<h1\b', body)) == 0, 'body h1 present'
print(f'  [ok ] structure: 0 h1 / {len(h2s)} h2 / 0 h3')

# wpautop adjacency: a block element must be separated from the previous one by
# WHITESPACE. Canonical md_to_html emits a single "\n"; the last clean publishes
# all carry single-"\n" separators, so a rule demanding a BLANK line would reject
# every canonical payload. The real corruption trigger is non-whitespace TEXT
# between two block tags.
BLK = r'(?:p|h2|ul|ol|figure|table|blockquote)'
adj = re.findall(r'</' + BLK + r'>([^\s<][\s\S]{0,3}?)<' + BLK + r'\b', body)
assert not adj, f'text between adjacent block tags: {adj[:3]}'
print('  [ok ] block adjacency: whitespace-separated')

# p balance (WP 8572: use <p\b, never <p -- <pre>/<path> inflate the count)
p_open = len(re.findall(r'<p\b', body))
p_close = len(re.findall(r'</p>', body))
assert p_open == p_close, f'p imbalance {p_open}/{p_close}'
assert not re.findall(r'<p></p>', body), 'empty <p></p> shells present'
print(f'  [ok ] p balance: {p_open}/{p_close}, 0 empty p')

# list balance: token-stream walk, 0 <li> outside any list (Cycle #64 rule).
# NOTE: </li> closes an ITEM, not a container -- popping the container stack on
# </li> makes every subsequent <li> look "outside" its list (4 false positives).
stack = []
outside = 0
for m in re.finditer(r'<(/?)(ul|ol|li)\b[^>]*>', body):
	closing, tag = m.group(1), m.group(2)
	if tag in ('ul', 'ol'):
		if closing:
			if stack and stack[-1] == tag:
				stack.pop()
		else:
			stack.append(tag)
	else:  # li -- closes an item, never a container
		if not closing and not stack:
			outside += 1
assert not stack, f'unclosed list containers: {stack}'
assert outside == 0, f'{outside} <li> outside any list'
li_open = len(re.findall(r'<li\b', body))
print(f'  [ok ] list balance: {li_open} li, 0 outside, 0 unclosed')

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
# Band from OBSERVED canonical publishes: WP 8552=1270, 8557=1634, 8566=1808,
# 8547=2397, 8572=1503.
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

with open('/tmp/wp_sub_payload.json', 'w') as f:
	json.dump(payload, f)
with open('/tmp/wp_sub_article_final.html', 'w', encoding='utf-8') as f:
	f.write(body)
print()
print('PRE-POST GATE: ALL PASS')
print('payload bytes:', len(json.dumps(payload)))
