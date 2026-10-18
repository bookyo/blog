#!/usr/bin/env python3
"""Generate PIL assets for Drag Force Calculator field guide article.

- poster.png  (1080x800): deep navy + cyan-teal accent
- card1.png   (1600x900): 5-tile numbered list — Five Things That Decide Drag Force
- card2.png   (1600x900): 2-col audit — Five Checks Before You Trust A Drag Number
- card3.png   (1600x900): 4-tile — Same Speed, Different Fluid (drag values)
"""
import sys, os
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
import pil_poster_and_cards_network_theme as theme
from PIL import ImageDraw

OUT_DIR = '/Users/quyue/www/blog/2026-10-18-drag-force-calculator-field-guide'

# ===== POSTER =====
# Pre-measure subtitle for WP 5683/6109/6129/6149 pitfall
subtitle = "When the same sphere at the same speed pulls 20 N in water and 115 N in air"
from PIL import ImageFont
F_MED = theme.load(theme.HELV_NEU, 0, 30)
img_tmp = ImageDraw.Draw(theme.Image.new('RGB', (1080, 800)))
w = img_tmp.textbbox((0, 0), subtitle, font=F_MED)[2]
if w > 1040:
    while w > 1040:
        sp = subtitle.rfind(' ')
        if sp < 1:
            break
        subtitle = subtitle[:sp]
        w = img_tmp.textbbox((0, 0), subtitle, font=F_MED)[2]
    print(f'Trimmed subtitle to: {subtitle!r} ({w}px)')
else:
    print(f'Subtitle fits: {w}px')

# Pre-measure title lines (WP 7144 pitfall)
title_lines = ('Drag Force', 'Is A Regime')
F_TITLE = theme.load(theme.HELV_NEU, 0, 70)
for tl in title_lines:
    tw = img_tmp.textbbox((0, 0), tl, font=F_TITLE)[2]
    print(f'  title line {tl!r}: {tw}px (max 1040)')

p1 = theme.render_poster(
    out_path=f'{OUT_DIR}/poster.png',
    eyebrow='FLUID MECHANICS · DRAG FORCE',
    title_lines=title_lines,
    subtitle=subtitle,
    callout_lines=('Four choices stacked on top of one formula,',
                   'and a Reynolds number to confirm the regime'),
    url_bar='elysiatools.com/en/tools/drag-force-calculator',
)
print(f'Poster: {p1}  size={os.path.getsize(p1)} bytes')

# ===== CARD 1 — 5-tile: Five Things That Decide Drag Force =====
p2 = theme.render_card_5tile(
    out_path=f'{OUT_DIR}/card1.png',
    title='Five Things That Decide Drag Force',
    subtitle='Four inputs and one regime check — get any one wrong and the answer is wrong',
    items=(
        ('01', 'FLUID', 'ρ\nkg/m³'),
        ('02', 'VELOCITY', 'v\nm/s'),
        ('03', 'DRAG COEFF', 'C_D\n0.04-1.17'),
        ('04', 'FRONTAL AREA', 'A\nm²'),
        ('05', 'REYNOLDS', 'Re\nρvL/μ'),
    ),
    notes=('air 1.225', 'v squared', 'shape dep.', 'silhouette', 'regime chk'),
    takeaway='F_D = ½ · ρ · v² · C_D · A    P = F_D · v',
    highlight_last=True,
)
print(f'Card 1: {p2}  size={os.path.getsize(p2)} bytes')

# ===== CARD 2 — 2-col audit: Five Checks Before You Trust A Drag Number =====
p3 = theme.render_card_audit(
    out_path=f'{OUT_DIR}/card2.png',
    title='Five Checks Before You Trust A Drag Number',
    subtitle='The audit you run on every drag value, in the order you run it',
    header_left='VALIDATION CHECK',
    header_right='RESULT YOU WANT',
    checks=(
        ('01', 'Re regime', 'Confirm Re is in the Newton plateau (Re > 10³) for the C_D you picked'),
        ('02', 'Area convention', 'Use frontal projected area for bluff bodies, planform for wings'),
        ('03', 'C_D source', 'Match the C_D value to the same regime and reference-area convention'),
        ('04', 'Velocity units', 'km/h to m/s conversion is a v² error — do not skip it'),
        ('05', 'Density medium', 'Air vs water makes a 817× difference — confirm the medium'),
    ),
    stamp='Sphere, v=20 m/s, A=1 m²',
    verdict=(
        ('Air (ρ=1.225)', '115.15 N'),
        ('Water (ρ=1000)', '94,000 N'),
        ('Regime Re', '> 10³'),
        ('Power (air)', '2,303 W'),
    ),
    bad_label='WRONG: density 1.225 with v in km/h',
    bad_note='50² = 2500 m²/s² vs 13.89² ≈ 193 m²/s² — a 13× silent error before any other consideration.',
)
print(f'Card 2: {p3}  size={os.path.getsize(p3)} bytes')

# ===== CARD 3 — 4-tile: Same Sphere, Different Fluid =====
# Sphere at v=2 m/s, A=0.1 m², C_D=0.47
# Air ρ=1.225 → F_D = 0.5*1.225*4*0.47*0.1 = 0.115 N
# Water ρ=1000 → F_D = 0.5*1000*4*0.47*0.1 = 94 N
# Seawater ρ=1025 → F_D = 0.5*1025*4*0.47*0.1 = 96.35 N
# Glycerin ρ=1260 → F_D = 0.5*1260*4*0.47*0.1 = 118.4 N
p4 = theme.render_card_4tile(
    out_path=f'{OUT_DIR}/card3.png',
    title='Same Sphere, Different Fluid',
    subtitle='Sphere, C_D=0.47, v=2 m/s, A=0.1 m² — only ρ changes, drag moves two orders of magnitude',
    tiles=(
        ('AIR', '0.12 N', theme.load(theme.HELV_NEU, 0, 110), 'ρ = 1.225 kg/m³', 'F_D ≈ ½·1.225·4·0.47·0.1'),
        ('WATER', '94 N', theme.load(theme.HELV_NEU, 0, 110), 'ρ = 1000 kg/m³', 'F_D ≈ ½·1000·4·0.47·0.1'),
        ('SEAWATER', '96 N', theme.load(theme.HELV_NEU, 0, 110), 'ρ = 1025 kg/m³', 'F_D ≈ ½·1025·4·0.47·0.1'),
        ('GLYCERIN', '118 N', theme.load(theme.HELV_NEU, 0, 110), 'ρ = 1260 kg/m³', 'F_D ≈ ½·1260·4·0.47·0.1'),
    ),
)
print(f'Card 3: {p4}  size={os.path.getsize(p4)} bytes')

print()
print('=== ALL ASSETS GENERATED ===')
for f in ['poster.png', 'card1.png', 'card2.png', 'card3.png']:
    fp = f'{OUT_DIR}/{f}'
    import subprocess
    info = subprocess.run(['file', fp], capture_output=True, text=True).stdout
    print(f'  {f}: {os.path.getsize(fp)} bytes  |  {info.strip()}')
