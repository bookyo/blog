import importlib.util
import os
import sys

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, f'{SKILL}/templates')
OUT_DIR = '/tmp/wp_assets'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pil = load(f'{SKILL}/templates/pil_poster_and_cards_network_theme.py', 'pil_poster_and_cards_network_theme')
custom = load(f'{SKILL}/templates/custom_pil_card_layouts.py', 'custom_pil_card_layouts')
from PIL import Image, ImageDraw

BAD_RANGES = [(0x2460, 0x24FF), (0x2776, 0x2793), (0x1F150, 0x1F1FF),
              (0x2100, 0x214F), (0x1D00, 0x1D5A), (0x2190, 0x21FF), (0x2260, 0x22FF)]


def tofu_scan(label, text):
    hits = [(ch, hex(ord(ch))) for ch in text
            for lo, hi in BAD_RANGES if lo <= ord(ch) <= hi]
    print(f'  {label}: ' + (f'TOFU RISK {hits[:8]}' if hits else 'clean'))


img = Image.new('RGB', (1600, 900))
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- CARD 2 (v2)
# Fill the dead space: 9 rows per side, rows <= 30 chars (WP 6358 2-col rule)
c2_title = 'One Solve, Two Strategies'
c2_sub = 'The shifted simplex returns both players from a single LP pass'
c2_left = (
    'row mix   x = (0.5, 0.5, 0.0)',
    'guarantees v = -0.5',
    'x transpose A =',
    '   col Low  -0.5',
    '   col Mid  -0.5',
    '   col High +1.5',
    'all three above v  OK',
    'LP primal slack',
    'Bland pivot rule',
)
c2_right = (
    'col mix   y = (0.5, 0.5, 0.0)',
    'caps       v = -0.5',
    'A y =',
    '   row Low  -0.5',
    '   row Mid  -0.5',
    '   row High -1.5',
    'all three below v  OK',
    'LP dual shadow px',
    'duality ties them',
)
c2_take = 'Shift K=3 moves the value by exactly 3 and changes neither mix'

for t in [c2_title, c2_sub, c2_take]:
    tofu_scan('card2', t)
worst = 0
for r in c2_left + c2_right:
    w = pil.text_w(d, r, pil.F_MONO)
    worst = max(worst, w)
    if w > 640:
        print(f'  *** OVERFLOW {r!r} = {w}px')
print(f'  card2 widest row: {worst}px / 640 limit')
print(f'  card2 rows per side: {len(c2_left)} / {len(c2_right)}')

custom.render_card_input_output_2col(
    f'{OUT_DIR}/card2.png',
    title=c2_title,
    subtitle=c2_sub,
    left_header='ROW PLAYER (maximises)',
    left_rows=c2_left,
    right_header='COLUMN PLAYER (minimises)',
    right_rows=c2_right,
    takeaway=c2_take,
)
print('card2 v2 written')

# ---------------------------------------------------------------- CARD 3 (v2)
# shorter labels so they clear the tile border gutter (259px was too tight)
c3_title = 'Six Lines Worth Memorising'
c3_sub = 'The whole method compressed into checks you can run by hand'
items3 = (
    ('01', 'SADDLE TEST', 'maximin vs minimax'),
    ('02', 'EQ CELL', 'max in column'),
    ('03', 'EQ CELL', 'min in row'),
    ('04', 'ROW FLOOR', 'xTA above v'),
    ('05', 'COL CEILING', 'Ay below v'),
)
notes3 = ('equal -> pure', 'not in row!', 'not in col!', 'componentwise', 'componentwise')
c3_take = 'Both inequalities must hold, or the reported pair is not an equilibrium'

for n, lab, val in items3:
    wl = pil.text_w(d, lab, pil.F_MED)
    print(f'  c3 label {lab!r:14s} {wl:4d}px / 270  {"OK" if wl <= 270 else "*** tight ***"}')
    for ln in val.split(chr(10)):
        w = pil.text_w(d, ln, pil.F_MONO)
        if w > 266:
            print(f'  *** body OVERFLOW {ln!r} = {w}px')
for t in [c3_title, c3_sub, c3_take, *notes3]:
    tofu_scan('card3', t)

pil.render_card_5tile(
    f'{OUT_DIR}/card3.png',
    title=c3_title,
    subtitle=c3_sub,
    items=items3,
    notes=notes3,
    takeaway=c3_take,
    highlight_last=True,
)
print('card3 v2 written')

print()
for f in sorted(os.listdir(OUT_DIR)):
    p = f'{OUT_DIR}/{f}'
    with Image.open(p) as im:
        print(f'  {f}: {im.size[0]}x{im.size[1]}  {os.path.getsize(p)} bytes')