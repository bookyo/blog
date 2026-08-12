#!/usr/bin/env python3
"""ANOVA Calculator field guide — render poster + 3 cards."""
import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
from pil_poster_and_cards_network_theme import (
    render_poster, render_card_5tile, render_card_audit, render_card_4tile
)

OUT = '/Users/quyue/www/blog/2026-08-12-anova-calculator-field-guide-2026-08-12'

# POSTER — 1080x800
p1 = render_poster(
    out_path=f'{OUT}/poster.png',
    eyebrow='STATISTICAL ANALYSIS',
    title_lines=('ANOVA Calculator', 'Field Guide'),
    subtitle="One-way ANOVA without the spreadsheet",
    callout_lines=('SSB, SSW, F, and p-value', 'in a single browser pass'),
    url_bar='elysiatools.com/en/tools/anova-calculator',
)
print(f'Poster: {p1}  size={__import__("os").path.getsize(p1)} bytes')

# CARD 1 — 5-tile: the ANOVA table rows (one tile per row)
p2 = render_card_5tile(
    out_path=f'{OUT}/card1.png',
    title='The Six-Row ANOVA Table',
    subtitle='Every number is recomputable from the raw data',
    items=(('01','SSB','64.5'),
           ('02','SSW','39.2'),
           ('03','SST','103.7'),
           ('04','MSB','21.5'),
           ('05','F','10.96')),
    notes=('between grp','within grp','SSB+SSW','per k-1 df','p < 0.001'),
    takeaway='F = MSB / MSW  |  The omnibus test for "all groups equal"',
    highlight_last=True,
)
print(f'Card 1: {p2}  size={__import__("os").path.getsize(p2)} bytes')

# CARD 2 — audit layout: assumptions checklist
p3 = render_card_audit(
    out_path=f'{OUT}/card2.png',
    title='Assumptions You Cannot Skip',
    subtitle='Three checks before the F statistic means anything',
    header_left='ANOVA PRE-FLIGHT',
    header_right='PASS WHEN',
    checks=(('01','Normality',     'Shapiro-Wilk on residuals returns p > 0.05'),
            ('02','Homoscedastic', 'Levene test across groups is non-significant'),
            ('03','Independence',  'Replicates are independent draws, not paired'),
            ('04','Balanced',      'Largest group <= 1.5x the smallest group'),
            ('05','Continuous',    'Response is measured, not counted or ranked')),
    stamp='F = 10.96',
    verdict=(('df1','3'),('df2','20'),('p-value','<0.001'),('eta-sq','0.622')),
    bad_label='FAIL: counts used as response',
    bad_note='Counts need Poisson/NB models, not ANOVA. Wrong tool for the data type.',
)
print(f'Card 2: {p3}  size={__import__("os").path.getsize(p3)} bytes')

# CARD 3 — 4-tile compact (multi-word count needs 1-row variant per WP 5755/5798)
from render_card_4tile_compact import render_card_4tile_compact
p4 = render_card_4tile_compact(
    out_path=f'{OUT}/card3.png',
    title='Post-Hoc Tests After a Significant F',
    subtitle='Which pair is the difference? ANOVA only opens the door',
    tiles=(('Tukey HSD',     'BEST',  'Equal sizes, controls family-wise error', 'q-stat'),
           ('Bonferroni',    'OK',    'Few groups, conservative safety net',     'p / n'),
           ('Scheffe',       'HIGH',  'Complex contrasts, most conservative',   'F-stat'),
           ('Holm-Bonferr.', 'GOOD',  'Step-down, less power loss than Bonf.',   'p / rank')),
    takeaway='Pick the post-hoc test BEFORE you look at the data and stick to it',
)
print(f'Card 3: {p4}  size={__import__("os").path.getsize(p4)} bytes')

print('All 4 assets rendered')
