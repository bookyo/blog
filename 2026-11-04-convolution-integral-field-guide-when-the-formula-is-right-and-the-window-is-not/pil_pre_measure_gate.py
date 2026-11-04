#!/usr/bin/env python3.11
"""Render the convolution-tool poster + 3 highlight cards, with a pre-measure GATE.

Pre-measure gate (WP 8557 lesson): measure every string BEFORE rendering and
exit non-zero on overflow. Budgets derived from the template SOURCE:
  poster title   -> W = 1080
  poster subtitle-> W = 1080 (F_MED); keep <= 60 chars
  poster callout -> W - 160 = 920
  poster url bar -> W = 1080 (F_SMALL); the real slug is 33 chars
  5-tile label   -> tile_w = 290 (centered)
  5-tile body    -> tile_w - 24 = 266 (F_MONO, no shrink chain)
  5-tile note    -> tile_w = 290 (F_MONO_SM centered)
  4-tile label   -> tile_w - 60 = 300 (LEFT-aligned at x+30)
  4-tile body    -> tile_w - 60 = 300, capped to 2 LINES
  4-tile sub     -> tile_w - 60 = 300, capped to 2 LINES
  2-col row     -> col_w - 60 = 640 (F_MONO)
  2-col header  -> col_w = 700
  card title     -> W = 1600
"""
import os
import shutil
import sys

TPL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates'
sys.path.insert(0, TPL)

import pil_poster_and_cards_network_theme as pil          # noqa: E402
import custom_pil_card_layouts as custom                     # noqa: E402
from render_card_4tile_compact import render_card_4tile_compact  # noqa: E402

OUT_DIR = '/tmp/wp_assets_conv'
# WP 6185/6320: always clear the asset dir first — stale files leak into the run.
if os.path.isdir(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- tofu scan
BAD = ''.join(chr(c) for c in (
    list(range(0x2460, 0x2500)) + list(range(0x2776, 0x2794)) +
    list(range(0x1F150, 0x1F200)) + list(range(0x1D00, 0x1D5B)) +
    list(range(0x2100, 0x2200))
))
# Self-test: the class must NOT match plain ASCII (WP pitfall #82).
assert not any(ch in BAD for ch in 'abcdefgXYZ0123'), 'tofu class matches ASCII!'

PROBLEMS = []


def gate(label, value, budget, font=None, draw=None):
    """Measure a string against a pixel budget."""
    if draw is None:
        return
    w = pil.text_w(draw, value, font)
    if w > budget:
        PROBLEMS.append(f'{label}: {w}px > {budget}px  ({value!r})')
    return w


def measure_all():
    """Pre-measure every string before any render happens."""
    from PIL import Image, ImageDraw
    probe = Image.new('RGB', (10, 10))
    d = ImageDraw.Draw(probe)

    # ---- POSTER ----
    poster = dict(
        eyebrow='SIGNAL PROCESSING',
        title_lines=('The Formula Is Right', 'The Window Is Not'),
        subtitle='A convolution field guide to truncation error',
        callout_lines=('One bound decides every number',
                       'and it never warns you when it bites'),
        url_bar='elysiatools.com/en/tools/convolution-integral-calculator',
    )
    gate('poster.eyebrow', poster['eyebrow'], 1080, pil.F_MED, d)
    for i, t in enumerate(poster['title_lines']):
        gate(f'poster.title[{i}]', t, 1080, pil.F_TITLE, d)
    gate('poster.subtitle', poster['subtitle'], 1080, pil.F_MED, d)
    for i, c in enumerate(poster['callout_lines']):
        gate(f'poster.callout[{i}]', c, 920, pil.F_MED, d)
    gate('poster.url_bar', poster['url_bar'], 1080, pil.F_SMALL, d)

    # ---- CARD 1: 5-tile numbered list ----
    c1_items = (
        ('01', 'T = 10', '3.6788'),
        ('02', 'T = 20', '2.7067'),
        ('03', 'T = 25', '1.6417'),
        ('04', 'T = 30', '0.9957'),
        ('05', 'T = 40', '0.3663'),
    )
    c1_notes = ('0% error', '0% error', '20% low', '33% low', '50% low')
    c1_title = 'One Window, Five Answers'
    c1_sub = 'Default tauMax 20 truncates the tail as t grows past the bound'
    c1_takeaway = 'Error ratio = (t - tauMax) / t  |  Exact at t = 10, half the answer at t = 40'

    gate('card1.title', c1_title, 1600, pil.F_H2, d)
    gate('card1.subtitle', c1_sub, 1600, pil.F_MED, d)
    for i, (num, label, val) in enumerate(c1_items):
        gate(f'card1.item[{i}].num', num, 290, pil.F_BIG, d)
        gate(f'card1.item[{i}].label', label, 290, pil.F_MED, d)
        # body: F_MONO_BIG with wrap to tile_w - 24; gate the LONGEST line
        for ln in pil.wrap_text(d, val, pil.F_MONO_BIG, 290 - 24):
            gate(f'card1.item[{i}].body', ln, 266, pil.F_MONO_BIG, d)
        gate(f'card1.item[{i}].note', c1_notes[i], 290, pil.F_MONO_SM, d)
    gate('card1.takeaway', c1_takeaway, 1600, pil.F_MED, d)

    # ---- CARD 2: 2-col worked example ----
    c2_left_rows = (
        'mode = causal',
        'f = exp(-x/10)',
        'g = exp(-x/10)',
        'tauMin = 0',
        'tauMax = 20',
        'intervals = 2000',
        '',
        't = 25  ->  1.6417',
        'exact   ->  2.052125',
        'error   ->  -20.0%',
    )
    c2_right_rows = (
        'mode = causal',
        'f = exp(-x/10)',
        'g = exp(-x/10)',
        'tauMin = 0',
        'tauMax = 60',
        'intervals = 2000',
        '',
        't = 25  ->  2.052125',
        'exact   ->  2.052125',
        'error   ->  0.0%',
    )
    c2_title = 'One Number Fixes Everything'
    c2_sub = 'Same expressions, same intervals, wider window: the error vanishes'
    c2_takeaway = 'Change tauMax and watch the answer move  |  If it moves, you were window-limited'
    c2_left_header = 'WINDOW TOO NARROW'
    c2_right_header = 'WINDOW WIDE ENOUGH'

    gate('card2.title', c2_title, 1600, pil.F_H2, d)
    gate('card2.subtitle', c2_sub, 1600, pil.F_MED, d)
    gate('card2.left_header', c2_left_header, 700, pil.F_MED, d)
    gate('card2.right_header', c2_right_header, 700, pil.F_MED, d)
    for i, r in enumerate(c2_left_rows):
        gate(f'card2.left_row[{i}]', r, 640, pil.F_MONO, d)
    for i, r in enumerate(c2_right_rows):
        gate(f'card2.right_row[{i}]', r, 640, pil.F_MONO, d)
    gate('card2.takeaway', c2_takeaway, 1600, pil.F_MED, d)

    # ---- CARD 3: 4-tile compact (four limits of one run) ----
    c3_tiles = (
        ('ROUNDING', '0.0000',
         'Value rounded away at dp = 4',
         'raise decimal places to 8'),
        ('EMPTY RANGE', '0',
         'Empty integration interval',
         'causal mode, t <= 0'),
        ('TRULY ZERO', '0',
         'Genuine cancellation',
         'the honest answer'),
        ('WINDOW CLIP', '0.3663',
         'Tail cut at tauMax = 20',
         'true value is 0.7326'),
    )
    c3_title = 'Four Limits of One Run'
    c3_sub = 'The same output line can hide three different meanings'
    c3_takeaway = 'Zero can mean rounding, an empty range, or a real zero  |  And 0.3663 can mean half the answer'

    gate('card3.title', c3_title, 1600, pil.F_H2, d)
    gate('card3.subtitle', c3_sub, 1600, pil.F_MED, d)
    for i, (label, count, body, sub) in enumerate(c3_tiles):
        gate(f'card3.tile[{i}].label', label, 300, pil.F_H3, d)
        # count: auto-shrink chain 150 -> 84 -> 64, gated on tile_w - 60
        cf = pil.F_HUGE
        if pil.text_w(d, count, cf) > 300:
            cf = pil.load(pil.HELV_NEU, 0, 84)
        if pil.text_w(d, count, cf) > 300:
            cf = pil.load(pil.HELV_NEU, 0, 64)
        gate(f'card3.tile[{i}].count(after shrink)', count, 300, cf, d)
        # body: WRAPS to tile_w - 60 and is capped at 2 LINES — a LINE-COUNT gate
        body_lines = pil.wrap_text(d, body, pil.F_SMALL, 300)
        if len(body_lines) > 2:
            PROBLEMS.append(
                f'card3.tile[{i}].body wraps to {len(body_lines)} lines (cap 2): {body_lines!r}')
        for ln in body_lines[:2]:
            gate(f'card3.tile[{i}].body', ln, 300, pil.F_SMALL, d)
        sub_lines = pil.wrap_text(d, sub, pil.F_MONO_SM, 300)
        if len(sub_lines) > 2:
            PROBLEMS.append(
                f'card3.tile[{i}].sub wraps to {len(sub_lines)} lines (cap 2): {sub_lines!r}')
        for ln in sub_lines[:2]:
            gate(f'card3.tile[{i}].sub', ln, 300, pil.F_MONO_SM, d)
    gate('card3.takeaway', c3_takeaway, 1600, pil.F_MED, d)

    # ---- tofu scan on every string that will be drawn ----
    all_strings = [poster['eyebrow'], poster['subtitle'], poster['url_bar'], c1_title,
                   c1_sub, c1_takeaway, c2_title, c2_sub, c2_takeaway, c3_title,
                   c3_sub, c3_takeaway]
    all_strings += list(poster['title_lines']) + list(poster['callout_lines'])
    all_strings += [s for t in c1_items for s in t] + list(c1_notes)
    all_strings += list(c2_left_rows) + list(c2_right_rows)
    all_strings += [s for t in c3_tiles for s in t]
    for s in all_strings:
        hit = [ch for ch in s if ch in BAD]
        if hit:
            PROBLEMS.append(f'tofu glyph(s) {hit!r} in {s!r}')

    return poster, c1_items, c1_notes, c1_title, c1_sub, c1_takeaway, \
        c2_left_rows, c2_right_rows, c2_title, c2_sub, c2_takeaway, \
        c2_left_header, c2_right_header, c3_tiles, c3_title, c3_sub, c3_takeaway


def main():
    (poster, c1_items, c1_notes, c1_title, c1_sub, c1_takeaway,
     c2_left_rows, c2_right_rows, c2_title, c2_sub, c2_takeaway,
     c2_left_header, c2_right_header, c3_tiles, c3_title, c3_sub,
     c3_takeaway) = measure_all()

    if PROBLEMS:
        print('=== PRE-MEASURE GATE: FAILED ===')
        for p in PROBLEMS:
            print('  FAIL', p)
        sys.exit(1)
    print('=== PRE-MEASURE GATE: PASS ===')

    poster_path = os.path.join(OUT_DIR, 'poster.png')
    pil.render_poster(
        poster_path,
        eyebrow=poster['eyebrow'],
        title_lines=poster['title_lines'],
        subtitle=poster['subtitle'],
        callout_lines=poster['callout_lines'],
        url_bar=poster['url_bar'],
    )

    c1_path = os.path.join(OUT_DIR, 'card1.png')
    pil.render_card_5tile(
        c1_path,
        title=c1_title,
        subtitle=c1_sub,
        items=c1_items,
        notes=c1_notes,
        takeaway=c1_takeaway,
        highlight_last=True,
    )

    c2_path = os.path.join(OUT_DIR, 'card2.png')
    custom.render_card_input_output_2col(
        c2_path,
        title=c2_title,
        subtitle=c2_sub,
        left_header=c2_left_header,
        left_rows=c2_left_rows,
        right_header=c2_right_header,
        right_rows=c2_right_rows,
        takeaway=c2_takeaway,
    )

    c3_path = os.path.join(OUT_DIR, 'card3.png')
    render_card_4tile_compact(
        c3_path,
        title=c3_title,
        subtitle=c3_sub,
        tiles=c3_tiles,
        takeaway=c3_takeaway,
    )

    from PIL import Image
    for p in (poster_path, c1_path, c2_path, c3_path):
        with Image.open(p) as im:
            print(f'{os.path.basename(p)}: {im.size[0]}x{im.size[1]}  '
                  f'{os.path.getsize(p)} bytes')
    assert Image.open(poster_path).size == (1080, 800), 'poster size wrong'
    for p in (c1_path, c2_path, c3_path):
        assert Image.open(p).size == (1600, 900), f'{p} size wrong'
    print('ALL ASSETS RENDERED OK')


if __name__ == '__main__':
    main()
