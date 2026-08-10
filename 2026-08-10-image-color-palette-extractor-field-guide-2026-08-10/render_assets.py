#!/usr/bin/env python3
"""
Image Color Palette Extractor — PIL assets build script.
Theme: DESIGN / deep navy + cyan accent.

Card 1: 5-tile numbered list (5 export formats: JSON, CSS variables, Tailwind, ASE, ACO)
Card 2: audit card (5 checks to verify contrast & code-readiness)
Card 3: 4-tile grid (palette sizes 5/6/8/10 — what each delivers)
"""
import os, sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
from pil_poster_and_cards_network_theme import (
    render_poster, render_card_5tile, render_card_audit
)
from render_card_4tile_compact import render_card_4tile_compact

ASSETS = '/Users/quyue/www/blog/2026-08-10-image-color-palette-extractor-field-guide-2026-08-10'

# POSTER
p = render_poster(
    out_path=f'{ASSETS}/poster.png',
    eyebrow='DESIGN TOKENS',
    title_lines=('Five Colors Are', 'Hiding in Your Hero Image'),
    subtitle='A field guide to extracting code-ready palettes',
    callout_lines=('Drop a JPG, get JSON, CSS variables,',
                   'Tailwind config, ASE, and ACO in one pass'),
    url_bar='elysiatools.com/en/tools/image-color-palette-extractor'
)
print(f'poster: {p}  size={os.path.getsize(p)} bytes')

# CARD 1 — 5-tile export formats
p = render_card_5tile(
    out_path=f'{ASSETS}/card1.png',
    title='Five Exports From One Image',
    subtitle='Drop a single PNG and the tool emits every format a design team needs',
    items=(('01','JSON','tokens'),
           ('02','CSS VARS',':root { ... }'),
           ('03','TAILWIND','extend'),
           ('04','ASE','Photoshop'),
           ('05','ACO','Illustrator')),
    notes=('design-tokens','.brand-primary','colors.brand','binary swap','binary swap'),
    takeaway='One upload -> five handoff-ready files (JSON, CSS, Tailwind, ASE, ACO)',
    highlight_last=False
)
print(f'card1: {p}  size={os.path.getsize(p)} bytes')

# CARD 2 — audit card (5 checks)
p = render_card_audit(
    out_path=f'{ASSETS}/card2.png',
    title='Five Checks Before You Ship',
    subtitle='Run these on every palette you commit to a brand token system',
    header_left='PRE-SHIP AUDIT',
    header_right='PALETTE REPORT',
    checks=(('01','Contrast WCAG','Does the lightest pair clear AA on body text?'),
            ('02','Range spread','Is the lightness delta wide enough to read as a system?'),
            ('03','Color cast','Are two grays hiding in the palette as chroma drift?'),
            ('04','Brand bias','Do the warm hues match the brand mood, not just the photo?'),
            ('05','Naming','Are the token names stable across design and code?')),
    stamp='landing-brand / 6',
    verdict=(('Tokens','6'),('Contrast','AA'),('Tones','6 / 6'),('Names','7')),
    bad_label='WATCH: chroma-clashing reds',
    bad_note='Camera white balance can shift every red by 10-15 percent without telling you.'
)
print(f'card2: {p}  size={os.path.getsize(p)} bytes')

# CARD 3 — 4-tile compact 1-row (large count numbers + body descriptions don't collide)
p = render_card_4tile_compact(
    out_path=f'{ASSETS}/card3.png',
    title='Palette Size Changes The Output',
    subtitle='Pick 5, 6, 8, or 10 colors and the export package retunes to match',
    tiles=(('SIZE 5','5',  'hero + accent + 3 neutrals','minimal brand'),
           ('SIZE 6','6',  'primary scale start, default','web apps'),
           ('SIZE 8','8',  'primary + secondary, full','design system'),
           ('SIZE 10','10','full tonal scale','enterprise')),
    takeaway='Default 6 covers 80 percent of brand palettes; go higher for design systems'
)
print(f'card3: {p}  size={os.path.getsize(p)} bytes')
