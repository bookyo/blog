#!/usr/bin/env python3
"""Generate PIL assets for GraphQL Playground article (Cron WP post).

Asset plan:
- poster.png  (1080x800): deep navy + cyan accent
- card1.png   (1600x900): 5-tile numbered list — "Five GraphQL request building blocks"
- card2.png   (1600x900): 2-col audit — "Five introspection-driven schema checks"
- card3.png   (1600x900): 4-tile compact — "Five pre-flight checks before shipping a mutation"
"""
import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
import pil_poster_and_cards_network_theme as theme
from PIL import ImageDraw

# Poster — pre-measure subtitle for WP 5683/6109/6129/6149 pitfall
subtitle = "An in-browser GraphQL client that handles queries, mutations, variables, headers, fragments, and introspection in one tab"
# Pre-measure
from PIL import ImageFont
F_MED = theme.load(theme.HELV_NEU, 0, 30)
img_tmp = ImageDraw.Draw(theme.Image.new('RGB', (1080, 800)))
w = img_tmp.textbbox((0, 0), subtitle, font=F_MED)[2]
if w > 1040:
    # Walk back word-by-word to last full word that fits
    while w > 1040:
        sp = subtitle.rfind(' ')
        if sp < 1:
            break
        subtitle = subtitle[:sp]
        w = img_tmp.textbbox((0, 0), subtitle, font=F_MED)[2]
    print(f'Trimmed to: {subtitle!r} ({w}px)')
else:
    print(f'Subtitle fits: {w}px')

p1 = theme.render_poster(
    out_path='/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/poster.png',
    eyebrow='DEVELOPMENT TOOLS',
    title_lines=('GraphQL Playground', 'When One Tab Beats curl'),
    subtitle=subtitle,
    callout_lines=('Queries, mutations, variables, fragments,',
                   'and live introspection in a single browser tab'),
    url_bar='elysiatools.com/en/tools/graphql-playground',
)
print(f'Poster: {p1}  size={__import__("os").path.getsize(p1)} bytes')

# Card 1 — 5-tile: Five request building blocks sent on every call
p2 = theme.render_card_5tile(
    out_path='/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card1.png',
    title='Five Building Blocks Sent On Every Request',
    subtitle='The three body fields plus the two header fields that travel with every GraphQL call',
    items=(
        ('01', 'QUERY',     'query string'),
        ('02', 'VARIABLES', 'JSON object'),
        ('03', 'OPERATION', 'operationName'),
        ('04', 'CONTENT-TYPE', 'application/json'),
        ('05', 'AUTH',      'Bearer token'),
    ),
    notes=(
        'typed in editor',
        'editable JSON',
        'optional but greps',
        'always required',
        'header pane',
    ),
    takeaway='Total request shape: 3 body fields + 2 header fields = 5 things to keep straight',
    highlight_last=True,
)
print(f'Card 1: {p2}  size={__import__("os").path.getsize(p2)} bytes')

# Card 2 — 2-col audit: Five introspection checks
p3 = theme.render_card_audit(
    out_path='/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card2.png',
    title='Five Introspection Checks Before You Wire The Client',
    subtitle='The five questions a playground answers faster than any docs page',
    header_left='CHECK',
    header_right='WHAT IT TELLS YOU',
    checks=(
        ('01', 'Field name',   'Is the field actually exposed by the live schema?'),
        ('02', 'Variable type', 'Nullable? List? Enum? What values does the enum accept?'),
        ('03', 'Return shape',  'Is the response wrapped, paginated, or null on empty?'),
        ('04', 'Deprecated',    'Does the schema mark this field as deprecated?'),
        ('05', 'Description',   'Is there a doc string the playground renders inline?'),
    ),
    stamp='POST /graphql',
    verdict=(
        ('Query', 'typed'),
        ('Vars', 'JSON'),
        ('OpName', 'string'),
        ('Errors', 'data'),
    ),
    bad_label='SKIP: docs site from 2024',
    bad_note='Renamed fields do not show up. Autocomplete still lies about them.',
)
print(f'Card 2: {p3}  size={__import__("os").path.getsize(p3)} bytes')

# Card 3 — 4-tile compact (per WP 5755/6068/6122/6149/6206 decision tree)
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
import render_card_4tile_compact as compact
p4 = compact.render_card_4tile_compact(
    out_path='/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/card3.png',
    title='Five Pre-Flight Checks Before Shipping A Mutation',
    subtitle='The minimum set you verify in the playground before the mutation lands in production code',
    tiles=(
        ('Return',     'type',    'Define the return type so callers can confirm success',     'null is a smell'),
        ('Variables',  'minimal', 'Only require the fields the mutation actually needs',       'less is safer'),
        ('Errors',     'data',    'Business errors belong in the data payload, not in errors',  'never fatal'),
        ('Op name',    'greps',   'Add operationName so server logs can find this mutation',    'no alias = lost'),
    ),
    takeaway='A mutation that returns the right shape, requires the minimum inputs, and logs by name is ready to ship',
)
print(f'Card 3: {p4}  size={__import__("os").path.getsize(p4)} bytes')

print('\nAll 4 assets generated.')