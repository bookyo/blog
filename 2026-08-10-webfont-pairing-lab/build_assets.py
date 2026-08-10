#!/usr/bin/env python3
"""Build poster + 3 highlight cards for Web Font Pairing Lab field guide."""
import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
from pil_poster_and_cards_network_theme import (
    render_poster, render_card_5tile, render_card_audit
)
from render_card_4tile_compact import render_card_4tile_compact
from PIL import Image, ImageDraw, ImageFont
import pil_poster_and_cards_network_theme as pil
import os

ASSETS = '/tmp/webfont_assets'
os.makedirs(ASSETS, exist_ok=True)

# POSTER
p1 = render_poster(
    out_path=f'{ASSETS}/poster.png',
    eyebrow='DESIGN / TYPOGRAPHY',
    title_lines=('Web Font Pairing', 'Is a System Problem'),
    subtitle='A Google Fonts pairing field guide for the lab you keep rebuilding in your head',
    callout_lines=('Two faces, four families, seven presets,',
                   'one copy-paste CSS @import at the end'),
    url_bar='elysiatools.com/en/tools/webfont-pairing-lab',
)

# CARD 1 — 5-tile: 4 font families + 1 set of 7 presets
p2 = render_card_5tile(
    out_path=f'{ASSETS}/card1.png',
    title='Four Font Families That Pair',
    subtitle='The 22-face registry spans the four families that share x-height and rhythm',
    items=(
        ('01', 'GEOMETRIC SANS', 'Poppins, Montserrat'),
        ('02', 'HUMANIST SANS', 'Inter, Source Sans 3'),
        ('03', 'TRANSITIONAL SERIF', 'Playfair, Lora'),
        ('04', 'SLAB', 'Roboto Slab, Bitter'),
        ('05', '7 PRESETS', 'Editorial, UI, marketing'),
    ),
    notes=('x-height ~555', 'x-height ~525', 'contrast HIGH', 'contrast LOW', 'all one click'),
    takeaway='7 presets ship pre-configured heading weight + body weight + line-height',
    highlight_last=True,
)

# CARD 2 — audit: 5 checks for shipping a pair (custom render with shorter verdict values)
def render_card_audit_short_verdict(out_path, title, subtitle, header_left, header_right,
                                    checks, stamp, verdict, bad_label, bad_note):
    """Same as render_card_audit but uses F_MONO_SM (22pt) for verdict values
    so longer identifiers like 'PLAYFAIR' do not overflow into the OK badge column.
    """
    W, H = 1600, 900
    img = Image.new('RGB', (W, H), pil.BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 6)], fill=pil.ACCENT)

    pil.draw_centered(d, (0, 50), W, title, pil.F_H2, pil.TEXT_MAIN)
    pil.draw_centered(d, (0, 130), W, subtitle, pil.F_MED, pil.TEXT_DIM)

    col_w, gap = 700, 60
    left_x = (W - (col_w * 2 + gap)) // 2
    right_x = left_x + col_w + gap
    col_y, col_h = 200, 640

    # Left column (checks)
    d.rectangle([(left_x, col_y), (left_x + col_w, col_y + col_h)], fill=pil.BG_CARD, outline=pil.PANEL_BORDER, width=2)
    d.rectangle([(left_x, col_y), (left_x + col_w, col_y + 4)], fill=pil.ACCENT2)
    pil.draw_centered(d, (left_x, col_y + 22), col_w, header_left, pil.F_MED, pil.ACCENT2)

    row_h = 100
    row_y0 = col_y + 80
    for idx, (num, label, body) in enumerate(checks):
        ry = row_y0 + idx * row_h
        badge_size = 56
        bx = left_x + 30
        by_ = ry + 8
        d.rectangle([(bx, by_), (bx + badge_size, by_ + badge_size)], fill=pil.ACCENT2, outline=None)
        ntw = pil.text_w(d, num, pil.F_BIG)
        nth = pil.text_h(d, num, pil.F_BIG)
        d.text((bx + (badge_size - ntw) // 2, by_ + (badge_size - nth) // 2 - 4), num, fill=pil.BG, font=pil.F_BIG)
        d.text((bx + badge_size + 20, ry + 12), label, fill=pil.TEXT_MAIN, font=pil.F_H3)
        body_lines = pil.wrap_text(d, body, pil.F_SMALL, col_w - badge_size - 80)
        body_y = ry + 60
        for line in body_lines:
            d.text((bx + badge_size + 20, body_y), line, fill=pil.TEXT_DIM, font=pil.F_SMALL)
            body_y += 26

    # Right column (result)
    d.rectangle([(right_x, col_y), (right_x + col_w, col_y + col_h)], fill=pil.BG_CARD, outline=pil.PANEL_BORDER, width=2)
    d.rectangle([(right_x, col_y), (right_x + col_w, col_y + 4)], fill=pil.ACCENT)
    pil.draw_centered(d, (right_x, col_y + 22), col_w, header_right, pil.F_MED, pil.ACCENT)

    pil.draw_centered(d, (right_x, col_y + 80), col_w, stamp, pil.F_MONO_BIG, pil.TEXT_MAIN)

    vy = col_y + 180
    for label, val in verdict:
        d.text((right_x + 40, vy), label, fill=pil.TEXT_DIM, font=pil.F_MED)
        # Use F_MONO_SM (22pt) to keep long values inside the verdict column
        d.text((right_x + 240, vy), val, fill=pil.TEXT_MAIN, font=pil.F_MONO_SM)
        d.rectangle([(right_x + col_w - 110, vy + 4), (right_x + col_w - 50, vy + 40)], fill=pil.GREEN)
        tw_ok = pil.text_w(d, 'OK', pil.F_SMALL)
        d.text((right_x + col_w - 110 + (60 - tw_ok) // 2, vy + 9), 'OK', fill=pil.BG, font=pil.F_SMALL)
        vy += 56

    d.line([(right_x + 30, col_y + col_h - 110), (right_x + col_w - 30, col_y + col_h - 110)], fill=pil.PANEL_BORDER, width=2)
    d.text((right_x + 40, col_y + col_h - 90), bad_label, fill=pil.RED, font=pil.F_MONO)
    bad_lines = pil.wrap_text(d, bad_note, pil.F_SMALL, col_w - 80)
    by_ = col_y + col_h - 56
    for line in bad_lines:
        d.text((right_x + 40, by_), line, fill=pil.TEXT_DIM, font=pil.F_SMALL)
        by_ += 26

    img.save(out_path, 'PNG', optimize=True)
    return out_path

p3 = render_card_audit_short_verdict(
    out_path=f'{ASSETS}/card2.png',
    title='Five Checks Before You Ship',
    subtitle='The audit you run on every font pair, in the order you run it',
    header_left='PRE-SHIP AUDIT',
    header_right='EXPORT YOU WANT',
    checks=(
        ('01', 'X-height match', 'Do heading and body share the eye-trip threshold?'),
        ('02', 'Weight contrast', 'Is the 300-pt gap between heading and body?'),
        ('03', 'Family contrast', 'Are they same-system but different-family?'),
        ('04', 'Fallback stack', 'Georgia / system-ui / serif in the var?'),
        ('05', 'font-display', 'Does the @import URL say swap, not block?'),
    ),
    stamp='@import + :root',
    verdict=(
        ('--font-heading', 'PLAYFAIR'),
        ('--font-body', 'SOURCE SANS 3'),
        ('font-display', 'swap'),
        ('line-height', '1.6'),
    ),
    bad_label='WRONG: Times New Roman',
    bad_note='No fallback stack.  User sees TNR if Google Fonts is blocked.',
)

# CARD 3 — 4-tile compact (1-row) with multi-word count strings
p4 = render_card_4tile_compact(
    out_path=f'{ASSETS}/card3.png',
    title='The Three Sliders That Decide',
    subtitle='Heading weight, body weight, body line-height — the knobs that decide the pair',
    tiles=(
        ('HEADING WEIGHT', '700',   '300-900 range', 'display serif default'),
        ('BODY WEIGHT',    '400',   '300-700 range', 'humanist sans default'),
        ('LINE-HEIGHT',    '1.6',   '1.3-1.8 range', '16-18px body default'),
        ('WEIGHT GAP',     '300pt', 'sans + sans rule', 'minimum contrast'),
    ),
    takeaway='Use a 300-point weight gap between heading and body for hierarchy that reads',
)

for f in ['poster.png', 'card1.png', 'card2.png', 'card3.png']:
    full = f'{ASSETS}/{f}'
    print(f'{f}: {os.path.getsize(full)} bytes')
