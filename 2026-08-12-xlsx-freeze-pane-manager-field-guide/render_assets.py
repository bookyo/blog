#!/usr/bin/env python3
"""Per-tool PIL renderer: XLSX Freeze Pane Manager field guide."""
import os, sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing')
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
from templates.pil_poster_and_cards_network_theme import (
    render_poster, render_card_5tile, render_card_audit,
    load, text_w, wrap_text, draw_centered,
    HELV, HELV_NEU,
    BG, BG_CARD, ACCENT, ACCENT2, TEXT_MAIN, TEXT_DIM, TEXT_MUTED, PANEL_BORDER,
    GREEN, RED,
    F_TITLE, F_H2, F_H3, F_BIG, F_MED, F_SMALL, F_MONO, F_MONO_BIG, F_MONO_SM, F_HUGE, F_TINY,
)
from render_card_4tile_compact import render_card_4tile_compact
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = '/Users/quyue/www/blog/2026-08-12-xlsx-freeze-pane-manager-field-guide'
os.makedirs(OUT_DIR, exist_ok=True)

# Subtitle width pre-check per WP 5683
subtitle = 'A field guide to freezing panes, outline groups, collapsed exports'
W = 1080
d_tmp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
sw = text_w(d_tmp, subtitle, F_MED)
print(f'Subtitle width: {sw}px (canvas {W}px, limit {W-40}px)')
if sw > W - 40:
    # Shorten
    while sw > W - 40 and len(subtitle) > 10:
        subtitle = subtitle[:-1]
        sw = text_w(d_tmp, subtitle, F_MED)
    print(f'Shortened to: {subtitle!r} ({sw}px)')

# POSTER
p1 = render_poster(
    out_path=os.path.join(OUT_DIR, 'poster.png'),
    eyebrow='FORMAT CONVERSION  /  XLSX PRODUCTIVITY',
    title_lines=('Lock the Headers,', 'Freeze the Panes'),
    subtitle=subtitle,
    callout_lines=('Five settings make a wide workbook',
                   'read like a finished report.'),
    url_bar='elysiatools.com/en/tools/xlsx-freeze-pane-manager',
)
print(f'Poster: {p1}  size={os.path.getsize(p1)} bytes')

# CARD 1 - 5-tile pane options (top row / first col / both / outline / collapse)
items_5 = (
    ('01', 'TOP ROW',     'rows[0]'),
    ('02', 'FIRST COL',   'col A'),
    ('03', 'BOTH',        'r1 + A'),
    ('04', 'OUTLINE',     'JSON'),
    ('05', 'COLLAPSE',    'export'),
)
notes_5 = (
    'one click',
    'left anchor',
    'two anchors',
    'range spec',
    'hidden detail',
)
p2 = render_card_5tile(
    out_path=os.path.join(OUT_DIR, 'card1.png'),
    title='Five Settings the Manager Exposes',
    subtitle='Each maps onto Excel\'s pane and outline model directly',
    items=items_5,
    notes=notes_5,
    takeaway='Top row + first column covers ~80% of real workbook cases  |  Outline groups cover the rest',
    highlight_last=True,
)
print(f'Card 1: {p2}  size={os.path.getsize(p2)} bytes')

# CARD 2 - audit layout (checks + verdict)
p3 = render_card_audit(
    out_path=os.path.join(OUT_DIR, 'card2.png'),
    title='Five Checks Before You Freeze',
    subtitle='The audit you run on every workbook you intend to share',
    header_left='PRE-FREEZE AUDIT',
    header_right='RESULT YOU WANT',
    checks=(
        ('01', 'Top row only',     'When the first row holds headers and nothing else matters'),
        ('02', 'First col only',   'When column A is the row label every reader needs'),
        ('03', 'Both axes',        'When readers scroll both vertically and horizontally'),
        ('04', 'Outline groups',   'When the detail can collapse into summary rows or columns'),
        ('05', 'Collapsed export', 'When stakeholders should see only the rolled-up numbers'),
    ),
    stamp='Sheet1',
    verdict=(
        ('Freeze',  'r1 + A'),
        ('Groups',  'JSON'),
        ('Export',  'collapsed'),
        ('Default', 'off'),
    ),
    bad_label='WRONG: freeze on row 5',
    bad_note='Mid-sheet freeze hides the actual header row. Always freeze on row 2.',
)
print(f'Card 2: {p3}  size={os.path.getsize(p3)} bytes')

# CARD 3 - 4-tile compact variant (single-row, auto-shrink for short counts)
p4 = render_card_4tile_compact(
    out_path=os.path.join(OUT_DIR, 'card3.png'),
    title='Same Workbook, Four Shapes',
    subtitle='What the manager produces for the four most common configurations',
    tiles=(
        ('HEADERS ONLY', '1', 'Top row locked, column A scrolls',       'rows[0]'),
        ('LABELS ONLY',  '1', 'Column A locked, top scrolls',           'col A'),
        ('BOTH ANCHORS', '2', 'Top row + col A locked together',        'r1 + A'),
        ('+OUTLINE',     '4', 'Groups layered on the freeze',            'JSON spec'),
    ),
    takeaway='Single-digit anchors (1-4) for the four common cases; outline groups add on top',
)
print(f'Card 3: {p4}  size={os.path.getsize(p4)} bytes')
