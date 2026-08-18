#!/usr/bin/env python3.11
"""Render poster + 3 highlight cards for the Cursive Text field-guide article.

Per the cron-mode PIL pitfall notes (umbrella SKILL.md):
- Pre-measure poster subtitle; shorten if wider than W-40.
- Pre-measure card value bands; split long tokens across 2 lines.
- Use render_card_4tile_compact for multi-word short count strings.
- Use vision_analyze after rendering to catch tofu / clipping / overlap.
"""
import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
from pil_poster_and_cards_network_theme import (
    BG, BG_CARD, ACCENT, ACCENT2, TEXT_MAIN, TEXT_DIM, TEXT_MUTED,
    PANEL_BORDER, GREEN, RED,
    F_HUGE, F_TITLE, F_H2, F_BIG, F_MED, F_SMALL, F_MONO, F_MONO_BIG, F_MONO_SM,
    text_w, wrap_text, draw_centered,
    render_poster, render_card_5tile,
)
from PIL import Image, ImageDraw, ImageFont

OUT = '/Users/quyue/www/blog/2026-08-18-cursive-text'

# ---------------------------------------------------------------------------
# Pre-flight measurement helpers (per umbrella SKILL.md PIL pitfalls)
# ---------------------------------------------------------------------------
def measure(s, font):
    img = Image.new('RGB', (10, 10))
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]

def shorten_to_width(s, font, max_w):
    if measure(s, font) <= max_w:
        return s
    # Binary-ish shrink by trimming words or chars
    out = s
    while out and measure(out, font) > max_w:
        out = out[:-1]
    return out.rstrip(',.;: ') + '...'

# ---------------------------------------------------------------------------
# Poster
# ---------------------------------------------------------------------------
POSTER_TITLE_1 = 'Cursive Unicode,'
POSTER_TITLE_2 = 'No Font File'
POSTER_SUB = 'A Cursive Text tool field guide: from ASCII to script glyphs'
POSTER_CALLOUT = ('Paste any ASCII string and copy a run of',
                  'Mathematical Script or Bold Script glyphs')
POSTER_URL = 'elysiatools.com/en/tools/cursive-text'

# Pre-measure subtitle (umbrella SKILL.md PIL pitfall: subtitle clipping)
sub_w = measure(POSTER_SUB, F_MED)
if sub_w > 1080 - 40:
    POSTER_SUB = shorten_to_width(POSTER_SUB, F_MED, 1080 - 40)
print(f'Poster subtitle width: {measure(POSTER_SUB, F_MED)} / 1040')

render_poster(
    OUT + '/poster.png',
    eyebrow='TYPOGRAPHY · UNICODE',
    title_lines=(POSTER_TITLE_1, POSTER_TITLE_2),
    subtitle=POSTER_SUB,
    callout_lines=POSTER_CALLOUT,
    url_bar=POSTER_URL,
)

# ---------------------------------------------------------------------------
# Card 1 — 5-tile: "What the tool actually emits" (U+1D49C/U+1D4D0 ranges)
# ---------------------------------------------------------------------------
render_card_5tile(
    OUT + '/card1.png',
    title='Five Code Points the Cursive Tool Maps',
    subtitle='Mathematical Script and Bold Script sit in two distinct SMP ranges',
    items=(
        ('01', 'U+1D49C', 'A'),
        ('02', 'U+1D4B6', 'a'),
        ('03', 'U+1D4D0', 'A'),
        ('04', 'U+1D4EA', 'a'),
        ('05', 'output', 'Hello'),
    ),
    notes=('Script cap', 'Script low', 'Bold cap', 'Bold low', 'preserves case'),
    takeaway='Total range: 104 letters  |  Bijection: 1-to-1 with ASCII A-Z / a-z',
)

# ---------------------------------------------------------------------------
# Card 2 — comparison 2-col (script unicode vs CSS webfont)
# Use a custom 2-column renderer since render_card_audit is pre-commit
# checklist oriented. Build it inline.
# ---------------------------------------------------------------------------
W, H = 1600, 900
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), (W, 6)], fill=ACCENT)
draw_centered(d, (0, 50), W, 'Script Unicode vs CSS Webfont', F_H2, TEXT_MAIN)
draw_centered(d, (0, 130), W, 'Pick by whether your text crosses a system boundary', F_MED, TEXT_DIM)

col_w, gap = 700, 60
left_x = (W - (col_w * 2 + gap)) // 2
right_x = left_x + col_w + gap
col_y, col_h = 200, 600

# Left column: SCRIPT UNICODE
d.rectangle([(left_x, col_y), (left_x + col_w, col_y + col_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
d.rectangle([(left_x, col_y), (left_x + col_w, col_y + 4)], fill=ACCENT)
draw_centered(d, (left_x, col_y + 22), col_w, 'SCRIPT UNICODE (portable)', F_MED, ACCENT)

rows_left = [
    ('Wins',  'crosses chat apps, email, README, JSON untouched'),
    ('Wins',  'plain text — no font file, no CSS, no CDN'),
    ('Wins',  'reversible: a 1-line decode recovers ASCII'),
    ('Cost',  'A-Z / a-z only — no digits, no punctuation in cursive'),
    ('Cost',  'older SMS gateways strip non-BMP characters'),
]
ry0 = col_y + 80
row_h = 88
for i, (label, body) in enumerate(rows_left):
    ry = ry0 + i * row_h
    badge_w = 130
    color = ACCENT if label == 'Wins' else (255, 130, 130)
    d.rounded_rectangle([(left_x + 30, ry + 10), (left_x + 30 + badge_w, ry + 50)], radius=8, fill=color)
    draw_centered(d, (left_x + 30, ry + 14), badge_w, label, F_SMALL, BG)
    wrapped = wrap_text(d, body, F_SMALL, col_w - 200)
    by = ry + 30
    for ln in wrapped[:2]:
        d.text((left_x + 180, by), ln, font=F_SMALL, fill=TEXT_MAIN)
        by += 22

# Right column: CSS WEBFONT
d.rectangle([(right_x, col_y), (right_x + col_w, col_y + col_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
d.rectangle([(right_x, col_y), (right_x + col_w, col_y + 4)], fill=ACCENT2)
draw_centered(d, (right_x, col_y + 22), col_w, 'CSS WEBFONT (polished)', F_MED, ACCENT2)

rows_right = [
    ('Wins',  'sharper kerning, real ligatures, italic stress'),
    ('Wins',  'covers Cyrillic, Greek, Han, Hiragana, digits'),
    ('Wins',  'typographically correct descenders on g, y, j'),
    ('Cost',  'requires recipient browser to load the font'),
    ('Cost',  'breaks the moment text crosses a system boundary'),
]
for i, (label, body) in enumerate(rows_right):
    ry = ry0 + i * row_h
    badge_w = 130
    color = ACCENT2 if label == 'Wins' else (255, 130, 130)
    d.rounded_rectangle([(right_x + 30, ry + 10), (right_x + 30 + badge_w, ry + 50)], radius=8, fill=color)
    draw_centered(d, (right_x + 30, ry + 14), badge_w, label, F_SMALL, BG)
    wrapped = wrap_text(d, body, F_SMALL, col_w - 200)
    by = ry + 30
    for ln in wrapped[:2]:
        d.text((right_x + 180, by), ln, font=F_SMALL, fill=TEXT_MAIN)
        by += 22

# Bottom takeaway
draw_centered(d, (0, col_y + col_h + 30), W, 'Use Script when text crosses a boundary.  Use a webfont when it does not.', F_MED, ACCENT)
img.save(OUT + '/card2.png', 'PNG', optimize=True)

# ---------------------------------------------------------------------------
# Card 3 — 4-tile checklist: "A short correctness checklist before you ship"
# Use render_card_4tile_compact (umbrella SKILL.md WP 5755/6068/6122)
# ---------------------------------------------------------------------------
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
try:
    from render_card_4tile_compact import render_card_4tile_compact
    HAS_COMPACT = True
except Exception as e:
    print('No compact renderer:', e)
    HAS_COMPACT = False

if HAS_COMPACT:
    render_card_4tile_compact(
        OUT + '/card3.png',
        title='Four Checks Before You Ship Cursive',
        subtitle='Three of these are byte-level; the fourth is the eyeball test',
        tiles=(
            ('01', 'Hex dump',  '0x210B', 'leading char is the script H'),
            ('02', 'Slack test',  '2 apps', 'paste in DM + GitHub issue'),
            ('03', 'Bytes count',  '5/char', '1 char in, 1 char out'),
            ('04', 'Fullwidth',  '0xFF0B', 'reject if leading is fullwidth'),
        ),
        takeaway='Total time: under 30 seconds per shipped string',
    )

print('Rendered:')
import os
for f in ['poster.png', 'card1.png', 'card2.png', 'card3.png']:
    p = OUT + '/' + f
    print(f'  {f}: {os.path.getsize(p)} bytes')
