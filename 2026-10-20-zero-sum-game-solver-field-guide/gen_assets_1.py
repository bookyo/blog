import importlib.util
import os
import re
import sys

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
sys.path.insert(0, f'{SKILL}/templates')

OUT_DIR = '/tmp/wp_assets'
if os.path.isdir(OUT_DIR):
    import shutil
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pil = load(f'{SKILL}/templates/pil_poster_and_cards_network_theme.py', 'pil_poster_and_cards_network_theme')
custom = load(f'{SKILL}/templates/custom_pil_card_layouts.py', 'custom_pil_card_layouts')

# ---- ASCII / tofu guard (WP 5699 / 6135 / 6178 / 6352 families) ----
BAD_RANGES = [(0x2460, 0x24FF), (0x2776, 0x2793), (0x1F150, 0x1F1FF),
              (0x2100, 0x214F), (0x1D00, 0x1D5A), (0x2190, 0x21FF),
              (0x2260, 0x22FF)]


def tofu_scan(label, text):
    hits = []
    for ch in text:
        o = ord(ch)
        for lo, hi in BAD_RANGES:
            if lo <= o <= hi:
                hits.append((ch, hex(o)))
    if hits:
        print(f'  TOFU RISK in {label}: {hits[:10]}')
    else:
        print(f'  {label}: clean')
    return hits


# ---------------------------------------------------------------- POSTER
EYEBROW = 'GAME THEORY ' + chr(0x00B7) + ' OPERATIONS RESEARCH'
TITLE = ('When Pure Play Fails,', 'Mixing Is the Only Answer')
SUBTITLE = 'Saddle points, shifted simplex, and verified equilibria'
CALLOUT = ('max(row minima) < min(column maxima)', 'means no cell is an equilibrium')
URLBAR = 'elysiatools.com/en/tools/game-theory-zero-sum'

for t in [EYEBROW, *TITLE, SUBTITLE, *CALLOUT, URLBAR]:
    tofu_scan('poster', t)

# subtitle must be <= 60 chars (WP 6390 left-edge clip)
print('  subtitle len:', len(SUBTITLE))
for line in TITLE:
    print('  title line len:', len(line), repr(line))

pil.render_poster(
    f'{OUT_DIR}/poster.png',
    eyebrow=EYEBROW,
    title_lines=TITLE,
    subtitle=SUBTITLE,
    callout_lines=CALLOUT,
    url_bar=URLBAR,
)
print('poster written')

# measure title widths against canvas 1080 (WP 7144 pre-measure)
from PIL import Image, ImageDraw
img = Image.new('RGB', (1080, 800))
d = ImageDraw.Draw(img)
for line in TITLE:
    w = pil.text_w(d, line, pil.F_TITLE)
    print(f'  title width {w:5d}px / 1080  {"OK" if w <= 1080 else "OVERFLOW"}  {line!r}')
sw = pil.text_w(d, SUBTITLE, pil.F_MED)
print(f'  subtitle width {sw}px / 1080  {"OK" if sw <= 1080 else "OVERFLOW"}')

# ---------------------------------------------------------------- CARD 1
# 5-tile: the saddle test on the two worked matrices
c1_title = 'The Saddle Test Decides Which Game You Are In'
c1_sub = 'max(row minima) versus min(column maxima) on two near-identical matrices'
items1 = (
    ('01', 'MAXIMIN', 'A1: 0'),
    ('02', 'MINIMAX', 'A1: 0'),
    ('03', 'VERDICT', 'A1: pure'),
    ('04', 'MAXIMIN', 'A2: -1'),
    ('05', 'MINIMAX', 'A2: 0'),
)
notes1 = ('ties -> pure', 'ties -> pure', 'bid Low', 'gap of one', 'mixed only')
take1 = 'One entry flips from +1 to -1 and the pure equilibrium disappears entirely'

# body <= 16 chars at F_MONO on 290px tiles
for n, lab, val in items1:
    print(f'  c1 body {val!r} len={len(val)} {"OK" if len(val) <= 16 else "TOO LONG"}')
    print(f'  c1 note {notes1[items1.index((n,lab,val))]!r} len={len(notes1[items1.index((n,lab,val))])}')
for t in [c1_title, c1_sub, take1, *notes1]:
    tofu_scan('card1', t)

pil.render_card_5tile(
    f'{OUT_DIR}/card1.png',
    title=c1_title,
    subtitle=c1_sub,
    items=items1,
    notes=notes1,
    takeaway=take1,
    highlight_last=True,
)
print('card1 written')

# ---------------------------------------------------------------- CARD 2
# dual recovery: one solve, two strategies
import inspect
print('  render_card_input_output_2col signature:',
      inspect.signature(custom.render_card_input_output_2col))

for f in ['card1.png', 'card2.png', 'card3.png', 'poster.png']:
    p = f'{OUT_DIR}/{f}'
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f'  {f}: {im.size}  {os.path.getsize(p)} bytes')
print('OUT_DIR:', OUT_DIR, os.listdir(OUT_DIR))