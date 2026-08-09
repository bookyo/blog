#!/usr/bin/env python3
"""Render poster + 3 cards for Resume Bullet STAR Rewriter field guide.

Card 1 (5-tile numbered): 4 STAR axes + 1 example (uses tile-h padding)
Card 2 (audit): 5 weak-opener categories vs. their STAR-score impact
Card 3 (4-tile compact): before/after STAR scores per axis
"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')

from pil_poster_and_cards_network_theme import (
    BG, BG_CARD, ACCENT, ACCENT2, TEXT_MAIN, TEXT_DIM, TEXT_MUTED,
    PANEL_BORDER, GREEN, RED,
    HELV, HELV_NEU, load,
    F_HUGE, F_TITLE, F_H2, F_H3, F_BIG, F_MED, F_SMALL, F_TINY,
    F_MONO_BIG, F_MONO, F_MONO_SM, F_MONO_TINY,
    text_w, text_h, wrap_text, draw_centered,
    render_poster, render_card_5tile, render_card_audit,
)

OUT_DIR = '/Users/quyue/www/blog/2026-08-09-resume-bullet-star-rewriter'
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# POSTER
# ---------------------------------------------------------------------------
poster_path = render_poster(
    out_path=f'{OUT_DIR}/poster.png',
    eyebrow='AI CAREER TOOLS',
    title_lines=('From "Responsible For"', 'To a STAR Bullet'),
    subtitle='A field guide to resume bullets the STAR method actually defends',
    callout_lines=('Five axes. Four diagnostics.',
                   'One rewrite a hiring manager can defend.'),
    url_bar='elysiatools.com/en/tools/resume-bullet-star-rewriter',
)
print(f'Poster: {poster_path} size={os.path.getsize(poster_path)} bytes')

# ---------------------------------------------------------------------------
# CARD 1 — 5-tile: 4 STAR axes + verdict
# ---------------------------------------------------------------------------
# We use a custom 5-tile for the 4 axes + the rewrite as 5th tile
W, H = 1600, 900
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), (W, 6)], fill=ACCENT)

draw_centered(d, (0, 50), W, 'The Four STAR Axes (and Why They Score Separately)', F_H2, TEXT_MAIN)
draw_centered(d, (0, 130), W, 'Each axis is graded 0-25 by deterministic heuristics — strong verbs, scale, numbers, context', F_MED, TEXT_DIM)

n = 4
tile_w, tile_h, gap_x = 360, 540, 24
total_w = n * tile_w + (n - 1) * gap_x
start_x = (W - total_w) // 2
y0 = 200

items = (
    ('01', 'SITUATION',  'Q2 2024, the welcome email flow at Acme'),
    ('02', 'TASK',       'Grow MAU from 12k to 18k in one quarter'),
    ('03', 'ACTION',     'Redesigned 4 emails, added 2 in-app prompts'),
    ('04', 'RESULT',     'MAU +18%, week-1 retention +6pp'),
)

for i, (num, label, val) in enumerate(items):
    x = start_x + i * (tile_w + gap_x)
    d.rectangle([(x, y0), (x + tile_w, y0 + tile_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
    d.rectangle([(x, y0), (x + tile_w, y0 + 4)], fill=ACCENT)
    # Number
    draw_centered(d, (x, y0 + 30), tile_w, num, F_BIG, ACCENT)
    # Divider
    d.line([(x + 50, y0 + 110), (x + tile_w - 50, y0 + 110)], fill=PANEL_BORDER, width=2)
    # Label
    draw_centered(d, (x, y0 + 140), tile_w, label, F_MED, ACCENT)
    # Value
    vlines = wrap_text(d, val, F_MONO_BIG, tile_w - 60)
    vy = y0 + 220
    for ln in vlines:
        draw_centered(d, (x, vy), tile_w, ln, F_MONO_BIG, TEXT_MAIN)
        vy += 46
    # Bottom rule
    d.line([(x + 30, y0 + tile_h - 50), (x + tile_w - 30, y0 + tile_h - 50)], fill=PANEL_BORDER, width=1)

# Takeaway
draw_centered(d, (0, y0 + tile_h + 30), W,
              'A 25 on every axis is a STAR bullet.  Most originals score 4-15.  Rewrites reach 60-85.',
              F_MED, ACCENT)
img.save(f'{OUT_DIR}/card1.png', 'PNG', optimize=True)
print(f'Card 1: {OUT_DIR}/card1.png size={os.path.getsize(OUT_DIR + "/card1.png")} bytes')

# ---------------------------------------------------------------------------
# CARD 2 — audit: 5 weak-openers vs. their STAR-score
# ---------------------------------------------------------------------------
# Use the audit card variant
card2_path = render_card_audit(
    out_path=f'{OUT_DIR}/card2.png',
    title='Five Openers That Cost You the Recruiter',
    subtitle='The weak-verb detector runs before the AI rewrite — these five get flagged every time',
    header_left='WEAK OPENER',
    header_right='WHAT IT COSTS YOU',
    checks=(
        ('01', 'Responsible for',
         'Hides the action.  STAR Action axis scores 0.'),
        ('02', 'Worked on',
         'Hides the deliverable AND the date.  Situation axis 0.'),
        ('03', 'Helped / Assisted',
         'No actor.  The recruiter can not picture you doing it.'),
        ('04', 'Involved in',
         'Six seconds is not enough to read past it.'),
        ('05', 'Was / Were',
         'Passive voice.  Actor disappears from the sentence.'),
    ),
    stamp='STAR SCORE: 4 / 100',
    verdict=(
        ('Original', '4'),
        ('Rewrite', '72'),
        ('Verb', 'SHIPPED'),
        ('Number', '18%'),
    ),
    bad_label='WEAK: "Responsible for user growth"',
    bad_note='No company, no product, no quarter, no number.  Six seconds = skipped.',
)
print(f'Card 2: {card2_path} size={os.path.getsize(card2_path)} bytes')

# ---------------------------------------------------------------------------
# CARD 3 — 4-tile compact (1-row): before/after STAR scores per axis
# ---------------------------------------------------------------------------
# Use single-row variant from WP 5676/5683
W, H = 1600, 900
img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([(0, 0), (W, 6)], fill=ACCENT)

draw_centered(d, (0, 50), W, 'Before and After, Axis by Axis', F_H2, TEXT_MAIN)
draw_centered(d, (0, 130), W, 'Same input, two passes through the tool: original score vs. rewrite score on each STAR axis', F_MED, TEXT_DIM)

# Single-row 4-tile variant
tile_w, tile_h, gap_x = 360, 540, 30
n = 4
total_w = n * tile_w + (n - 1) * gap_x
start_x = (W - total_w) // 2
y0 = 200

tiles = (
    ('SITUATION', '2 -> 22', 'No context -> Q2 2024, Acme welcome flow'),
    ('TASK',      '0 -> 19', 'No scale -> MAU 12k to 18k in one Q'),
    ('ACTION',    '0 -> 24', '"Responsible for" -> "Redesigned 4 emails"'),
    ('RESULT',    '2 -> 23', 'No number -> "+18% MAU, +6pp retention"'),
)

for i, (label, count, body) in enumerate(tiles):
    x = start_x + i * (tile_w + gap_x)
    d.rectangle([(x, y0), (x + tile_w, y0 + tile_h)], fill=BG_CARD, outline=PANEL_BORDER, width=2)
    d.rectangle([(x, y0), (x + 6, y0 + tile_h)], fill=ACCENT)
    # Label at y0+24
    draw_centered(d, (x, y0 + 24), tile_w, label, F_H3, ACCENT)
    # Count at y0+100 with auto-shrink for "2 -> 22" - it has 6 chars
    val_font = F_HUGE
    if text_w(d, count, F_HUGE) > tile_w - 60:
        val_font = F_BIG
        if text_w(d, count, F_BIG) > tile_w - 60:
            val_font = F_MONO_BIG
    draw_centered(d, (x, y0 + 100), tile_w, count, val_font, TEXT_MAIN)
    # Body description at y0+250 capped at 2 lines
    body_lines = wrap_text(d, body, F_SMALL, tile_w - 40)[:2]
    by = y0 + 250
    for line in body_lines:
        draw_centered(d, (x, by), tile_w, line, F_SMALL, TEXT_DIM)
        by += 30
    # Divider rule at y0 + tile_h - 100
    d.line([(x + 30, y0 + tile_h - 100), (x + tile_w - 30, y0 + tile_h - 100)], fill=PANEL_BORDER, width=2)
    # Sub-label at y0 + tile_h - 80 capped to 2 lines
    notes_map = {
        'SITUATION': 'Context: company + product + quarter',
        'TASK': 'Scale: users, dollars, requests/sec',
        'ACTION': 'Verb: built, shipped, cut, fixed',
        'RESULT': 'Number: percent, dollars, latency',
    }
    sub = notes_map[label]
    sub_lines = wrap_text(d, sub, F_TINY, tile_w - 40)[:2]
    sy = y0 + tile_h - 80
    for line in sub_lines:
        draw_centered(d, (x, sy), tile_w, line, F_TINY, TEXT_MUTED)
        sy += 22

# Takeaway at y0 + tile_h + 30
draw_centered(d, (0, y0 + tile_h + 30), W,
              'Original: 4 / 100   ->   Rewrite: 88 / 100   |   One input, four axes, a defensible bullet',
              F_MED, ACCENT)
img.save(f'{OUT_DIR}/card3.png', 'PNG', optimize=True)
print(f'Card 3: {OUT_DIR}/card3.png size={os.path.getsize(OUT_DIR + "/card3.png")} bytes')
