#!/usr/bin/env python3.11
"""Render poster + 3 cards with a pre-measure GATE (WP 8557 recipe).

No PNG is written until every string is measured against its template budget.
"""
import os, shutil, sys
from PIL import Image, ImageDraw

TPL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates'
sys.path.insert(0, TPL)
import pil_poster_and_cards_network_theme as pil
from render_card_4tile_compact import render_card_4tile_compact
from custom_pil_card_layouts import render_card_input_output_2col

OUT_DIR = '/tmp/wp_jt2600_assets'
shutil.rmtree(OUT_DIR, ignore_errors=True)
os.makedirs(OUT_DIR, exist_ok=True)

d = ImageDraw.Draw(Image.new('RGB', (10, 10)))

# ── budgets (derived from the templates' own geometry) ───────────────────
POSTER_W = 1080
POSTER_CALLOUT_W = POSTER_W - 160      # render_poster callout box inner width
TILE5_W = 290                          # render_card_5tile tile_w
TILE5_BODY_W = TILE5_W - 24            # wrap width for the value
TILE4_W = 360                          # render_card_4tile_compact tile_w
TILE4_LABEL_W = TILE4_W - 60           # label drawn LEFT-aligned at x+30
TILE4_BODY_W = TILE4_W - 60
COL2_W = 700                           # render_card_input_output_2col col_w
COL2_ROW_W = COL2_W - 60               # row budget (30px inset each side)
CARD_W = 1600                          # card title/subtitle/takeaway budget

errors = []
def gate(label, s, font, budget, extra=''):
    w = pil.text_w(d, s, font)
    ok = w <= budget
    print(f"  {'ok ' if ok else 'FAIL'} {label:34s} {w:5.0f}px / {budget}px  {extra}")
    if not ok:
        errors.append(f'{label}: {w:.0f}px > {budget}px')

# ══════════════════════════════════════════════════════════════════════════
# POSTER
# ══════════════════════════════════════════════════════════════════════════
EYEBROW = 'PHOTO REVIEW & PRINT PROOFING'
TITLE_LINES = ('A Contact Sheet Is', 'a Print Viewport')
SUBTITLE = 'What the 4:3 grid does to your frames'
CALLOUT = ('Cover crops 43.75% of a portrait', 'and never says so')
URL_BAR = 'elysiatools.com/en/tools/pdf-photo-contact-sheet'

print('POSTER measurements:')
gate('poster title line 1', TITLE_LINES[0], pil.F_TITLE, POSTER_W)
gate('poster title line 2', TITLE_LINES[1], pil.F_TITLE, POSTER_W)
gate('poster subtitle', SUBTITLE, pil.F_MED, POSTER_W)
gate('poster eyebrow', EYEBROW, pil.F_MED, POSTER_W)
gate('poster callout 1', CALLOUT[0], pil.F_MED, POSTER_CALLOUT_W)
gate('poster callout 2', CALLOUT[1], pil.F_MED, POSTER_CALLOUT_W)
gate('poster url bar', URL_BAR, pil.F_SMALL, POSTER_W)

# ══════════════════════════════════════════════════════════════════════════
# CARD 1 — 4-tile compact: the crop maths, four frame shapes
# ══════════════════════════════════════════════════════════════════════════
C1_TITLE = 'What Cover Mode Removes From Four Frame Shapes'
C1_SUB = 'A 4:3 thumbnail box decides how much of your picture survives'
C1_TILES = (
    ('3:4 PORTRAIT', '43.75%', 'Height trimmed, 21.9% off each end', 'loses half the frame'),
    ('1:1 SQUARE', '25%', 'Height trimmed, 12.5% off each end', 'a quarter disappears'),
    ('16:9 WIDE', '25%', 'Width trimmed, 12.5% off each side', 'edges are cut'),
    ('4:3 NATIVE', '0%', 'Nothing trimmed, it matches the box', 'the only safe shape'),
)
C1_TAKEAWAY = 'Only a 4:3 frame survives cover intact; every other shape loses a quarter or more'

print()
print('CARD 1 measurements (4-tile compact):')
gate('c1 title', C1_TITLE, pil.F_H2, CARD_W)
gate('c1 subtitle', C1_SUB, pil.F_MED, CARD_W)
for i, (label, count, body, sub) in enumerate(C1_TILES):
    gate(f'c1 t{i} label', label, pil.F_H3, TILE4_LABEL_W)
    # effective width after the 150 -> 84 -> 64 shrink chain
    eff = pil.text_w(d, count, pil.F_HUGE)
    if eff > TILE4_W - 60:
        eff = pil.text_w(d, count, pil.load(pil.HELV_NEU, 0, 84))
        if eff > TILE4_W - 60:
            eff = pil.text_w(d, count, pil.load(pil.HELV_NEU, 0, 64))
    print(f"  {'ok ' if eff <= TILE4_W - 60 else 'FAIL'} c1 t{i} count (effective)      {eff:5.0f}px / {TILE4_W - 60}px  {count}")
    if eff > TILE4_W - 60:
        errors.append(f'c1 t{i} count')
    for ln in pil.wrap_text(d, body, pil.F_SMALL, TILE4_BODY_W)[:2]:
        gate(f'c1 t{i} body line', ln, pil.F_SMALL, TILE4_BODY_W)
    for ln in pil.wrap_text(d, sub, pil.F_MONO_SM, TILE4_BODY_W)[:2]:
        gate(f'c1 t{i} sub line', ln, pil.F_MONO_SM, TILE4_BODY_W)
gate('c1 takeaway', C1_TAKEAWAY, pil.F_MED, CARD_W)

# ══════════════════════════════════════════════════════════════════════════
# CARD 2 — 2-col input/output: the worked example grid arithmetic
# ══════════════════════════════════════════════════════════════════════════
C2_TITLE = 'The Bundled Example, Cell by Cell'
C2_SUB = 'Ten sample images at 4 columns by 3 rows, with EXIF switched on'
C2_LEFT = (
    'columns: 4    rows: 3',
    'fitMode: cover',
    'includeExif: true',
    'pageSize: A4',
    'landscape: true',
    'imageFiles: 10 images',
)
C2_RIGHT = (
    'cells per sheet = 4 x 3',
    'cells used = 10',
    'cells empty = 2',
    'header: Sheet 1, items 1-10',
    'source: earth1..earth4 JPGs',
    'aspect mix: 4 square, 3 portrait, 3 wide',
)
C2_TAKEAWAY = '12 cells, 10 photos, and the grid ends half-empty with no filler'

print()
print('CARD 2 measurements (2-col input/output):')
gate('c2 title', C2_TITLE, pil.F_H2, CARD_W)
gate('c2 subtitle', C2_SUB, pil.F_MED, CARD_W)
gate('c2 left header', 'THE INPUT', pil.F_MED, COL2_W)
gate('c2 right header', 'WHAT THE SHEET DOES', pil.F_MED, COL2_W)
for i, row in enumerate(C2_LEFT):
    gate(f'c2 left row {i}', row, pil.F_MONO, COL2_ROW_W)
for i, row in enumerate(C2_RIGHT):
    gate(f'c2 right row {i}', row, pil.F_MONO, COL2_ROW_W)
gate('c2 takeaway', C2_TAKEAWAY, pil.F_MED, CARD_W)

# ══════════════════════════════════════════════════════════════════════════
# CARD 3 — 4-tile compact: the seven EXIF fields vs the four printed lines
# ══════════════════════════════════════════════════════════════════════════
C3_TITLE = 'Seven EXIF Fields, Four Printed Lines'
C3_SUB = 'The truncation is unconditional, and it always drops the same three'
C3_TILES = (
    ('CAMERA', 'ALWAYS', 'Model and lens lead the list', 'printed, lines 1-2'),
    ('EXPOSURE', 'ALWAYS', 'Aperture and ISO follow them', 'printed, lines 3-4'),
    ('SHUTTER', 'CUT', 'Exposure time and focal length', 'fields 5 and 6, both cut'),
    ('CAPTURED', 'CUT', 'Timestamp is the last field', 'field 7, also cut'),
)
C3_TAKEAWAY = 'The line that says when the frame was shot is the one line that never appears'

print()
print('CARD 3 measurements (4-tile compact):')
gate('c3 title', C3_TITLE, pil.F_H2, CARD_W)
gate('c3 subtitle', C3_SUB, pil.F_MED, CARD_W)
for i, (label, count, body, sub) in enumerate(C3_TILES):
    gate(f'c3 t{i} label', label, pil.F_H3, TILE4_LABEL_W)
    eff = pil.text_w(d, count, pil.F_HUGE)
    if eff > TILE4_W - 60:
        eff = pil.text_w(d, count, pil.load(pil.HELV_NEU, 0, 84))
        if eff > TILE4_W - 60:
            eff = pil.text_w(d, count, pil.load(pil.HELV_NEU, 0, 64))
    print(f"  {'ok ' if eff <= TILE4_W - 60 else 'FAIL'} c3 t{i} count (effective)      {eff:5.0f}px / {TILE4_W - 60}px  {count}")
    if eff > TILE4_W - 60:
        errors.append(f'c3 t{i} count')
    for ln in pil.wrap_text(d, body, pil.F_SMALL, TILE4_BODY_W)[:2]:
        gate(f'c3 t{i} body line', ln, pil.F_SMALL, TILE4_BODY_W)
    for ln in pil.wrap_text(d, sub, pil.F_MONO_SM, TILE4_BODY_W)[:2]:
        gate(f'c3 t{i} sub line', ln, pil.F_MONO_SM, TILE4_BODY_W)
gate('c3 takeaway', C3_TAKEAWAY, pil.F_MED, CARD_W)

# ══════════════════════════════════════════════════════════════════════════
# ASCII-only check (PIL tofu): every char must be renderable in Helvetica
# ══════════════════════════════════════════════════════════════════════════
ALL_STRINGS = [EYEBROW, *TITLE_LINES, SUBTITLE, *CALLOUT, URL_BAR,
                C1_TITLE, C1_SUB, C1_TAKEAWAY, C2_TITLE, C2_SUB, C2_TAKEAWAY,
                C3_TITLE, C3_SUB, C3_TAKEAWAY]
for lbl, cnt, body, sub in C1_TILES: ALL_STRINGS += [lbl, cnt, body, sub]
for lbl, cnt, body, sub in C3_TILES: ALL_STRINGS += [lbl, cnt, body, sub]
ALL_STRINGS += list(C2_LEFT) + list(C2_RIGHT)

# Build the bad-codepoint class with chr() loops (memory pitfall #82)
BAD = ''.join(chr(c) for c in
               list(range(0x2460, 0x2500)) + list(range(0x2776, 0x2794)) +
               list(range(0x1F150, 0x1F200)) + list(range(0x1D00, 0x1D60)) +
               list(range(0x2100, 0x2150)) + list(range(0x2E80, 0x2F00)))
assert not BAD.isascii(), 'bad class must contain non-ASCII'
assert [c for c in 'ascii probe' if c in BAD] == [], 'bad class matches ASCII -- broken class'
assert chr(0x2460) in BAD and chr(0x1D00) in BAD, 'class builder broken'
assert chr(0x41) not in BAD, 'class builder leaked ASCII'
bad_hits = []
for s in ALL_STRINGS:
    for ch in s:
        if ch in BAD or (ord(ch) >= 0x1D00 and ord(ch) <= 0x1DFF) or (ord(ch) >= 0x2100 and ord(ch) <= 0x214F):
            bad_hits.append((s, ch, hex(ord(ch))))
print()
if bad_hits:
    for s, ch, cp in bad_hits:
        print(f'  FAIL tofu-risk char {cp} in {s!r}')
    errors.append('tofu-risk characters present')
else:
    print('  [ok ] no tofu-risk characters in any rendered string (ASCII/Latin-1 only)')

if errors:
    print()
    print('GATE FAILED — no PNG written:')
    for e in errors:
        print('   -', e)
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════
print()
p = pil.render_poster(out_path=f'{OUT_DIR}/poster.png',
                      eyebrow=EYEBROW, title_lines=TITLE_LINES,
                      subtitle=SUBTITLE, callout_lines=CALLOUT, url_bar=URL_BAR)
c1 = render_card_4tile_compact(out_path=f'{OUT_DIR}/card1.png',
                               title=C1_TITLE, subtitle=C1_SUB,
                               tiles=C1_TILES, takeaway=C1_TAKEAWAY)
c2 = render_card_input_output_2col(out_path=f'{OUT_DIR}/card2.png',
                                   title=C2_TITLE, subtitle=C2_SUB,
                                   left_header='THE INPUT',
                                   left_rows=C2_LEFT,
                                   right_header='WHAT THE SHEET DOES',
                                   right_rows=C2_RIGHT,
                                   takeaway=C2_TAKEAWAY)
c3 = render_card_4tile_compact(out_path=f'{OUT_DIR}/card3.png',
                               title=C3_TITLE, subtitle=C3_SUB,
                               tiles=C3_TILES, takeaway=C3_TAKEAWAY)

from PIL import Image as I
for path, want in [(p, (1080, 800)), (c1, (1600, 900)), (c2, (1600, 900)), (c3, (1600, 900))]:
    sz = I.open(path).size
    print(f'  {path}: {sz}  {os.path.getsize(path)} bytes')
    assert sz == want, f'{path} is {sz}, expected {want}'
print('ASSETS RENDERED OK')
