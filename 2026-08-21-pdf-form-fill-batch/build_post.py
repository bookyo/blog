#!/usr/bin/env python3.11
"""Build final HTML + render PIL assets for PDF Form Fill Batch field guide."""
import sys, os, re, json, importlib.util

sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
from md_to_html import md_to_html

ASSETS_DIR = '/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/assets'
HTML_OUT = '/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article_final.html'
os.makedirs(ASSETS_DIR, exist_ok=True)

# Load PIL network theme
spec = importlib.util.spec_from_file_location(
    'pn',
    '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates/pil_poster_and_cards_network_theme.py'
)
pn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pn)
sys.modules['pn'] = pn
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')
import render_card_4tile_compact as fc
import custom_pil_card_layouts as cl

# === Step 1: md -> html ===
md = open('/Users/quyue/www/blog/2026-08-21-pdf-form-fill-batch/article.md').read()
# Strip the leading H1 (per umbrella: 0 body H1 — theme renders entry-title)
md = re.sub(r'^# [^\n]+\n+', '', md, count=1)
html = md_to_html(md)

# === Step 2: Card anchors ===
card_anchors = [
    "Field types that work, and the failure modes that don't",
    "Three concrete workflows where this tool earns its keep",
    "How it fits into a larger PDF batch pipeline",
]

# === Step 3: Insert card placeholders ===
# WP 6122 recipe: capture the H2 + immediately-following block(s) (may include <h3> then <p>,
# or just <p>). Insert card figure AFTER the entire captured prefix.
for i, anchor in enumerate(card_anchors, start=1):
    # Try: H2 -> (optional H3) -> P
    pattern = re.compile(
        r'(<h2>' + re.escape(anchor) + r'</h2>\s*(?:<h3>[^<]+</h3>\s*)?<p>.*?</p>)',
        re.DOTALL
    )
    placeholder = f'\n<figure class="highlight-card"><img decoding="async" src="PLACEHOLDER_card{i}.png" alt="Card {i}: {anchor}" loading="lazy" /></figure>\n'
    new_html, n = pattern.subn(r'\1' + placeholder, html, count=1)
    assert n == 1, f'card {i} insertion failed for {anchor}'
    html = new_html

# === Step 4: Insert article-poster figure before the lead <strong> ===
poster_fig = '<figure class="article-poster"><img decoding="async" src="PLACEHOLDER_poster.png" alt="PDF Form Fill Batch field guide cover" /></figure>\n'
m = re.search(r'(<strong>[^<]+</strong>)', html)
assert m, 'lead strong not found'
html = html[:m.start()] + poster_fig + html[m.start():]

# === Step 5: Sanity checks ===
assert len(re.findall(r'<figure class="highlight-card">', html)) == 3
assert len(re.findall(r'<figure class="article-poster">', html)) == 1
assert len(re.findall(r'<h1[^>]*>', html)) == 0
assert len(re.findall(r'<h2[^>]*>', html)) == 8
assert html.count('PLACEHOLDER_card') == 3
assert 'PLACEHOLDER_poster.png' in html

open(HTML_OUT, 'w').write(html)
print(f'Saved {HTML_OUT} ({len(html)} bytes)')

# === Step 6: Render PIL assets ===

# Poster
print('Rendering poster...')
pn.render_poster(
    out_path=f'{ASSETS_DIR}/poster.png',
    eyebrow='PDF TOOLS / BATCH',
    title_lines=('PDF Form Fill', 'Batch'),
    subtitle='One template. One JSON array. Hundreds of filled PDFs in a single pass.',
    callout_lines=('Fill a template with an array of records,', 'return a ZIP of PDFs or one merged file'),
    url_bar='elysiatools.com/en/tools/pdf-form-fill-batch',
)
print(f'  -> poster.png')

# Card 1: Field types (5tile)
print('Rendering card 1 (Field types)...')
pn.render_card_5tile(
    out_path=f'{ASSETS_DIR}/card1.png',
    title='Five Field Types The Filler Handles',
    subtitle='AcroForm fields the loader can fill from your records JSON',
    items=(
        ('01', 'TEXT', 'string value written via setText on the field'),
        ('02', 'CHECKBOX', 'boolean: true checks, false leaves unchecked'),
        ('03', 'RADIO', 'string matching one of the option values'),
        ('04', 'DROPDOWN', 'string from the option list (same as radio)'),
        ('05', 'OPTION LIST', 'multi-select form, same shape as dropdown'),
    ),
    notes=('string', 'bool', 'enum', 'enum', 'enum'),
    takeaway='Anything else — extra keys, missing keys, typo in field name — is silently skipped. Canonicalize your data first.',
    highlight_last=False,
)
print(f'  -> card1.png')

# Card 2: Three workflows (5tile cheatsheet 3+2)
print('Rendering card 2 (Three workflows)...')
cl.render_card_5tile_3plus2(
    out_path=f'{ASSETS_DIR}/card2.png',
    title='Three Workflows Where Batch Form Filling Earns Its Keep',
    subtitle='Same template + JSON pattern, three different output shapes',
    items=(
        ('Certificates', '3 to 50 recipients, ZIP mode, nameField=name'),
        ('Invoices', '2 to 200 line items, merge mode, nameField=invoice_no'),
        ('Onboarding', 'dozens of hires per quarter, ZIP mode, nameField=employee_id'),
        ('Flatten ON', 'leave flatten true for any customer-facing output'),
        ('Validate', 'open template in a PDF viewer before generating JSON'),
    ),
    notes=('cert', 'invoice', 'hr', 'flatten', 'verify'),
    takeaway='Same template + JSON pattern in all three. Only the nameField changes.',
)
print(f'  -> card2.png')

# Card 3: PDF batch pipeline (4tile compact)
print('Rendering card 3 (Pipeline)...')
fc.render_card_4tile_compact(
    out_path=f'{ASSETS_DIR}/card3.png',
    title='The PDF Batch Pipeline',
    subtitle='Four passes that turn a template into a shipped deliverable',
    tiles=(
        ('FILL', 'step 1', 'fill template per record with PDF Form Fill Batch', 'one template, one array'),
        ('FLATTEN', 'step 2', 'lock each filled PDF so it is non-editable', 'built-in option'),
        ('WATERMARK', 'step 3', 'add DRAFT or CONFIDENTIAL overlay before distribution', 'optional pass'),
        ('DISTRIBUTE', 'step 4', 'email, upload to HRIS, or merge into a print queue', 'final destination'),
    ),
    takeaway='Each step is a separate tool. Combining them is the complexity batch filling was designed to avoid.',
)
print(f'  -> card3.png')

print()
print('Done.')
