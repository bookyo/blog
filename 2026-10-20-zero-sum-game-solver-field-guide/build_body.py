import importlib.util
import json
import re
import sys

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, f'{SKILL}/templates')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mdt = load(f'{SKILL}/scripts/md_to_html.py', 'md_to_html')
ihc = load(f'{SKILL}/scripts/insert_highlight_cards.py', 'insert_highlight_cards')
va = load(f'{SKILL}/scripts/validate_elysia_anchors.py', 'validate_elysia_anchors')

md = open('/tmp/wp_run103/article.md').read()
body = mdt.md_to_html(md)

# --- poster figure goes first, immediately after body open ---
POSTER = (
    '<figure class="article-poster">'
    '<img decoding="async" src="POSTER_URL" '
    'alt="Poster: when pure play fails, mixing is the only answer" />'
    '</figure>'
)

CARD1 = (
    '<figure class="highlight-card">'
    '<img decoding="async" src="CARD1_URL" loading="lazy" '
    'alt="The saddle test on two near-identical payoff matrices: A1 maximin 0 equals minimax 0 '
    'so a pure equilibrium exists, A2 maximin -1 is below minimax 0 so only a mixed equilibrium '
    'remains" />'
    '</figure>'
)
CARD2 = (
    '<figure class="highlight-card">'
    '<img decoding="async" src="CARD2_URL" loading="lazy" '
    'alt="One simplex solve returns both players: row mix x = (0.5, 0.5, 0) guarantees v = -0.5 '
    'with x transpose A above v, column mix y = (0.5, 0.5, 0) caps v = -0.5 with A y below v, '
    'and the shift K = 3 moves the value by exactly 3 without changing either mix" />'
    '</figure>'
)
CARD3 = (
    '<figure class="highlight-card">'
    '<img decoding="async" src="CARD3_URL" loading="lazy" '
    'alt="Six-line reference: saddle test maximin versus minimax, equilibrium cell is max in its '
    'column and min in its row, row floor x transpose A above v, and column ceiling A y below v, '
    'both componentwise" />'
    '</figure>'
)

# card anchors = literal post-md_to_html H2 text
h2s = [re.sub(r'<[^>]+>', '', h).strip() for h in
       re.findall(r'<h2[^>]*>(.*?)</h2>', body, flags=re.DOTALL)]
print('H2s available:', len(h2s))
for i, h in enumerate(h2s, 1):
    print(f'  {i}. {h}')

anchors = [h2s[0], h2s[3], h2s[4]]   # 1) matrix, 2) shift trick, 3) one solve two strategies
print()
print('card anchors:', anchors)
for a in anchors:
    assert a in h2s, f'anchor not a real H2: {a}'

body = POSTER + '\n' + body

# canonical helper returns a plain str (WP 6390 lesson) - do NOT tuple-unpack
body = ihc.insert_highlight_cards(body, anchors, [CARD1, CARD2, CARD3],
                                  assert_all_succeed=True)
print('insert_highlight_cards returned OK')

# orphan </p> cleanup (WP 6370)
body = re.sub(r'(<figure class="highlight-card">[^<]*<img[^/]+/></figure>)\s*</p>', r'\1', body)

# ---- MANDATORY pre-POST assertions ----
n_cards = len(re.findall(r'<figure class="highlight-card">', body))
assert n_cards == 3, f'card count {n_cards} != 3 -- insertion silently failed'
print(f'  card count: {n_cards} -- PASS')
assert len(re.findall(r'<figure class="article-poster">', body)) == 1, 'poster figure count != 1'
print('  poster figure: 1 -- PASS')

checks = {
    'md links surviving': len(re.findall(r'\[[^\]]+\]\([^)]+\)', body)),
    'placeholder in code': len(re.findall(r'<code>[^<]*\{[^<]*\}[^<]*</code>', body)),
    'literal backslash in code': len(re.findall(r'<code>[^<]*\\\\[^<]*</code>', body)),
    'br in p': len(re.findall(r'<br\s*/?>', body)),
    'en-dash merged bullets': len(re.findall(r'\u2013\s*<strong>', body)),
    'code>em nesting': len(re.findall(r'<code>[^<]*<em>', body)),
    'code<code> nesting': len(re.findall(r'<code><code>', body)),
    'H1': len(re.findall(r'<h1', body)),
    'H3': len(re.findall(r'<h3', body)),
    'pre blocks': len(re.findall(r'<pre', body)),
    'pipe-table leak': len(re.findall(r'<p>[^<]*\|[^<]*\|[^<]*</p>', body)),
}
print()
print('=== pre-publish checks ===')
fail = False
for k, v in checks.items():
    ok = v == 0
    print(f'  {k}: {v}  {"PASS" if ok else "FAIL"}')
    if not ok:
        fail = True

# p inside h2 (correct check: inner content only)
h2_spans = re.findall(r'<h2[^>]*>(.*?)</h2>', body, flags=re.DOTALL)
bad = [h for h in h2_spans if '<p' in h.lower()]
print(f'  h2 containing <p>: {len(bad)}  {"PASS" if not bad else "FAIL"}')
if bad:
    fail = True

# URL placeholder leak (WP 7163) - expect exactly the 4 placeholders we intend
leftover = re.findall(r'(?:POSTER_URL|CARD\d?_URL)', body)
print(f'  placeholders present: {sorted(set(leftover))}  (expect POSTER_URL, CARD1_URL, CARD2_URL, CARD3_URL)')
assert set(leftover) == {'POSTER_URL', 'CARD1_URL', 'CARD2_URL', 'CARD3_URL'}, f'unexpected placeholders {set(leftover)}'

# anchors re-validated on FINAL body
ok, phantoms = va.validate_anchors(body)
print(f'  validate_anchors: ok={ok} phantoms={phantoms}')
if not ok:
    fail = True

# H2 count final
print(f'  final H2 count: {len(re.findall(r"<h2[^>]*>", body))} (expect 8)')

open('/tmp/wp_run103/article_body.html', 'w').write(body)
print()
print('wrote /tmp/wp_run103/article_body.html  len:', len(body))
print('RESULT:', 'ALL CHECKS PASS' if not fail else '*** FAILURES PRESENT ***')