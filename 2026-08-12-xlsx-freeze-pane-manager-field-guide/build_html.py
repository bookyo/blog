"""Build article HTML by inserting figures at H2 anchors."""
import re

WORKDIR = '/Users/quyue/www/blog/2026-08-12-xlsx-freeze-pane-manager-field-guide'
html = open(f'{WORKDIR}/article_raw.html').read()

# Card 1 -> after H2 #2 "How the tool reads your intent"
card1_fig = '<figure class="highlight-card"><img decoding="async" src="CARD1_URL" alt="XLSX Freeze Pane Manager: five settings the manager exposes (top row, first column, both, outline, collapse)" loading="lazy" /></figure>'
# Card 2 -> after H2 #3 "Why outline groups change how a workbook reads"
card2_fig = '<figure class="highlight-card"><img decoding="async" src="CARD2_URL" alt="XLSX Freeze Pane Manager: five pre-freeze audit checks (top row, first column, both axes, outline groups, collapsed export)" loading="lazy" /></figure>'
# Card 3 -> after H2 #7 "A few realistic settings worth knowing"
card3_fig = '<figure class="highlight-card"><img decoding="async" src="CARD3_URL" alt="XLSX Freeze Pane Manager: same workbook, four shapes (headers only, labels only, both anchors, +outline)" loading="lazy" /></figure>'

# Insert after H2 #2
h2_2 = '<h2>How the tool reads your intent</h2>'
html = html.replace(h2_2, h2_2 + chr(10) + card1_fig, 1)

# Insert after H2 #3
h2_3 = '<h2>Why outline groups change how a workbook reads</h2>'
html = html.replace(h2_3, h2_3 + chr(10) + card2_fig, 1)

# Insert after H2 #7
h2_7 = '<h2>A few realistic settings worth knowing</h2>'
html = html.replace(h2_7, h2_7 + chr(10) + card3_fig, 1)

# Now prepend the article-poster figure right before the first <p> (close-first lead)
first_p = html.find('<p><strong>Lock the headers')
poster_fig = '<figure class="article-poster"><img decoding="async" src="POSTER_URL" alt="XLSX Freeze Pane Manager: lock the headers, freeze the panes field guide" /></figure>'
html = html[:first_p] + poster_fig + chr(10) + html[first_p:]

open(f'{WORKDIR}/article_with_figures.html', 'w').write(html)

# Verify counts
print('H1 count:', len(re.findall(r'<h1[^>]*>', html)))
print('H2 count:', len(re.findall(r'<h2[^>]*>', html)))
print('article-poster count:', html.count('<figure class="article-poster">'))
print('highlight-card count:', html.count('<figure class="highlight-card">'))
print('p opens:', html.count('<p>'))
print('p closes:', html.count('</p>'))
print('Total length:', len(html))
