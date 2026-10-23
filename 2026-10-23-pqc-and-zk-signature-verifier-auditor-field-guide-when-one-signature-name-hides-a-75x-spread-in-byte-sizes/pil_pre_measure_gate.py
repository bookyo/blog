"""PIL pre-measure GATE for the PQC/ZK post (WP run 2026-10-23 ~14:30 UTC).

Measures every string against each template's REAL budget before a single PNG is
written. Exits non-zero on overflow so no render cycle is wasted.
"""
import sys
from PIL import Image, ImageDraw

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, SKILL + '/templates')
import pil_poster_and_cards_network_theme as pil

W = 1080
CARD_W = 1600
TILE_W_5 = 290
TILE_W_4 = 360
COL_W = 700
CALLOUT_W = W - 160

fails = []


def check(label, text, font, budget, hard=True):
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    tw = pil.text_w(d, text, font)
    ok = tw <= budget
    print(f'  [{"ok " if ok else "OVER"}] {label:<34} {tw:>5}px / {budget:>5}px   {text[:52]!r}')
    if not ok and hard:
        fails.append((label, tw, budget, text))
    return tw


print('=' * 78)
print('POSTER  (render_poster: W=1080 H=800)')
print('=' * 78)
EYEBROW = 'CRYPTOGRAPHY  .  POST-QUANTUM MIGRATION AUDIT'
TITLE = ('One Signature Name,', '75x of Signature Bytes')
SUBTITLE = 'Why the byte count decides your 2030 signing deadline'
CALLOUT = ('13 schemes, 4 families, one byte table', 'and the 2027 gate that arrives first')
URLBAR = 'elysiatools.com/en/tools/ml-dsa-slh-dsa-fn-dsa-pqc-bbs-plus-plonk-halo2-zk-verifier'

check('poster eyebrow', EYEBROW, pil.F_MED, W)
check('poster title line 0', TITLE[0], pil.F_TITLE, W)
check('poster title line 1', TITLE[1], pil.F_TITLE, W)
check('poster subtitle', SUBTITLE, pil.F_MED, W)
check('poster callout 0', CALLOUT[0], pil.F_MED, CALLOUT_W)
check('poster callout 1', CALLOUT[1], pil.F_MED, CALLOUT_W)
check('poster url bar', URLBAR, pil.F_SMALL, W)

print()
print('=' * 78)
print('CARD 1 — render_card_5tile  (tile_w=290)')
print('=' * 78)
C1_TITLE = 'Five Standardized Signature Sizes'
C1_SUB = 'The spread your envelope budget has to survive'
C1_ITEMS = (
    ('01', 'FALCON-512', '666 B'),
    ('02', 'ML-DSA-44', '2420 B'),
    ('03', 'ML-DSA-65', '3309 B'),
    ('04', 'ML-DSA-87', '4627 B'),
    ('05', 'SLH-256f', '49856 B'),
)
C1_NOTES = ('FN-DSA 206', 'FIPS 204', 'FIPS 204', 'FIPS 204', 'FIPS 205')
C1_TAKE = '75x spread between the smallest and largest standardized signature'
check('card1 title', C1_TITLE, pil.F_H2, CARD_W)
check('card1 subtitle', C1_SUB, pil.F_MED, CARD_W)
for i, (num, label, body) in enumerate(C1_ITEMS):
    check(f'card1 item{i} label', label, pil.F_MED, TILE_W_5)
    for line in body.split('\n'):
        check(f'card1 item{i} value', line, pil.F_MONO_BIG, TILE_W_5 - 24)
    check(f'card1 item{i} note', C1_NOTES[i], pil.F_MONO_SM, TILE_W_5)
check('card1 takeaway', C1_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
print('CARD 2 — render_card_4tile_compact  (tile_w=360, count budget tile_w-60=300)')
print('=' * 78)
C2_TITLE = 'Four Signature Families, One Setup Rule'
C2_SUB = 'What each post-quantum family needs before you can ship it'
C2_TILES = (
    ('LATTICE', 'NONE', 'ML-DSA, FN-DSA', 'FIPS 204 / 206'),
    ('HASH-BASED', 'NONE', 'SLH-DSA, XMSS', 'FIPS 205'),
    ('PAIRING', 'NONE', 'BBS signatures', 'BLS12-381'),
    ('ZK PROOFS', 'SETUP', 'Groth16, PLONK, Halo2', 'Powers of Tau SRS'),
)
C2_TAKE = 'Only the zero-knowledge family puts a ceremony on your critical path'
check('card2 title', C2_TITLE, pil.F_H2, CARD_W)
check('card2 subtitle', C2_SUB, pil.F_MED, CARD_W)
for i, (label, count, body, sub) in enumerate(C2_TILES):
    check(f'card2 tile{i} label', label, pil.F_H3, TILE_W_4 - 30)
    # replicate the 150 -> 84 -> 64 shrink chain for the EFFECTIVE width
    eff = pil.text_w(ImageDraw.Draw(Image.new('RGB', (10, 10))), count, pil.F_HUGE)
    eff_font = '150'
    if eff > TILE_W_4 - 60:
        eff = pil.text_w(ImageDraw.Draw(Image.new('RGB', (10, 10))), count, pil.load(pil.HELV_NEU, 0, 84))
        eff_font = '84'
    if eff > TILE_W_4 - 60:
        eff = pil.text_w(ImageDraw.Draw(Image.new('RGB', (10, 10))), count, pil.load(pil.HELV_NEU, 0, 64))
        eff_font = '64'
    print(f'  [{"ok " if eff <= TILE_W_4 - 60 else "OVER"}] card2 tile{i} count@{eff_font:<4}'
          f' {eff:>5}px / {TILE_W_4 - 60:>5}px   {count!r}')
    if eff > TILE_W_4 - 60:
        fails.append((f'card2 tile{i} count', eff, TILE_W_4 - 60, count))
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    for b in pil.wrap_text(d, body, pil.F_SMALL, TILE_W_4 - 60)[:2]:
        check(f'card2 tile{i} body', b, pil.F_SMALL, TILE_W_4 - 60)
    for s in pil.wrap_text(d, sub, pil.F_MONO_SM, TILE_W_4 - 60)[:2]:
        check(f'card2 tile{i} sub', s, pil.F_MONO_SM, TILE_W_4 - 60)
check('card2 takeaway', C2_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
print('CARD 3 — render_card_input_output_2col  (col_w=700, row budget 640, header 700)')
print('=' * 78)
C3_TITLE = 'Identify Mode: Length Gives the Answer'
C3_SUB = 'Paste a hex or base64 key or signature; measure it against the table'
C3_LH = 'BLOB LENGTH -> SCHEME'
C3_RH = 'WHAT THE AUDITOR REPORTS'
C3_LEFT = (
    '1312 B  ->  ML-DSA-44 public key',
    '3309 B  ->  ML-DSA-65 signature',
    '49856 B ->  SLH-DSA-256f signature',
    '',
    '666 B   ->  FN-DSA-512 signature',
    '80 B    ->  BBS signature',
)
C3_RIGHT = (
    'scheme + object kind',
    'matched byte length',
    'verdict: 1 known set',
    'verdict: N known sets',
    '0 matches = not standard',
    'length is a signal, not proof',
)
C3_TAKE = 'Length is a strong signal for PQC objects; weak for classical keys'
check('card3 title', C3_TITLE, pil.F_H2, CARD_W)
check('card3 subtitle', C3_SUB, pil.F_MED, CARD_W)
check('card3 left header', C3_LH, pil.F_MED, COL_W)
check('card3 right header', C3_RH, pil.F_MED, COL_W)
for r in C3_LEFT:
    if r:
        check('card3 left row', r, pil.F_MONO, COL_W - 60)
for r in C3_RIGHT:
    check('card3 right row', r, pil.F_MONO, COL_W - 60)
check('card3 takeaway', C3_TAKE, pil.F_MED, CARD_W)

print()
print('=' * 78)
if fails:
    print(f'GATE: FAIL -- {len(fails)} overflow(s), no PNG written')
    for f in fails:
        print('   ', f)
    sys.exit(1)
print('GATE: PASS -- every string fits its real budget')

print()
print('=' * 78)
print('TOFU PRE-FLIGHT (memory pitfall #82: build ranges with chr(), self-test)')
print('=' * 78)
bad_ranges = [(0x2460, 0x24FF), (0x2776, 0x2793), (0x1F150, 0x1F1FF),
              (0x1D00, 0x1D5A), (0x2100, 0x2BFF), (0x0378, 0x037F),
              (0xFEFF, 0xFEFF), (0x2E80, 0x9FFF)]
BAD = ''.join(chr(cp) for lo, hi in bad_ranges for cp in range(lo, hi + 1))
_TOFU_RE = __import__('re').compile('[' + BAD + ']')
assert _TOFU_RE.findall('<ascii probe ABC 123 ~!@#>') == [], 'tofu class matches ASCII -> broken'
print('  [ok ] tofu class self-test (ASCII probe returns [])')
ALL_TEXT = ' '.join([EYEBROW, ' '.join(TITLE), SUBTITLE, ' '.join(CALLOUT), URLBAR,
                      C1_TITLE, C1_SUB, ' '.join(x for t in C1_ITEMS for x in t), ' '.join(C1_NOTES), C1_TAKE,
                      C2_TITLE, C2_SUB, ' '.join(x for t in C2_TILES for x in t), C2_TAKE,
                      C3_TITLE, C3_SUB, C3_LH, C3_RH, ' '.join(C3_LEFT), ' '.join(C3_RIGHT), C3_TAKE])
hits = sorted(set(_TOFU_RE.findall(ALL_TEXT)))
print(f'  [{"ok " if not hits else "TOFU"}] tofu glyphs in asset text: {len(hits)} {hits if hits else ""}')
if hits:
    sys.exit(1)
print('GATE: ALL PASS')