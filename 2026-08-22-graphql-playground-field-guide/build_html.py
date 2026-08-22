#!/usr/bin/env python3
"""Build final HTML for WP GraphQL Playground article — simplified.

Strategy: source MD already has inline <figure class="highlight-card"> blocks at the
correct anchor positions (after the 2nd, 4th, and 7th H2). Just convert MD -> HTML,
unwrap the close-first lead (raw <strong>...</strong> form), and strip <p> wrappers
from <figure class="article-poster"> and <figure class="highlight-card">.
"""
import sys, re
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
import md_to_html

MD_PATH = '/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/article.md'
OUT_PATH = '/Users/quyue/www/blog/2026-08-22-graphql-playground-field-guide/article_final.html'

md = open(MD_PATH).read()
html = md_to_html.md_to_html(md)

# 1. Unwrap lead: replace <p>Close-first draft: skip the five-minute setup, ...</p> with raw <strong>...</strong>
lead_pattern = re.compile(r'^<p>Close-first draft: skip the five-minute setup,\s*skip the desktop app download, skip the eight-tab-browser ritual\s*—\s*(.*?)</p>', re.DOTALL)
m = lead_pattern.match(html)
if m:
    rest = m.group(1).lstrip()
    html = '<strong>Skip the setup, the desktop app, and the eight-tab-browser ritual.</strong> ' + rest + html[m.end():]
    print('Lead unwrapped.')
else:
    print('Lead pattern did not match!')

# 2. Strip <p> wrapper from <figure class="article-poster">
new = re.sub(r'<p>(<figure class="article-poster">.*?</figure>)</p>', r'\1', html, count=1)
print(f'Figure-poster <p> stripped: {html != new}')
html = new

# 3. Strip <p> wrapper from all <figure class="highlight-card">
new = re.sub(r'<p>(<figure class="highlight-card">.*?</figure>)</p>', r'\1', html)
print(f'Highlight-card <p> wrappers stripped: count={new.count("highlight-card") - html.count("highlight-card")}')
html = new

# Verify counts
print()
print('Final stats:')
print('  len:', len(html))
print('  h1:', html.count('<h1>'))
print('  h2:', html.count('<h2>'))
print('  h3:', html.count('<h3>'))
print('  highlight-card figures:', len(re.findall(r'<figure class="highlight-card">', html)))
print('  article-poster figures:', len(re.findall(r'<figure class="article-poster">', html)))

# Sanity
md_links = re.findall(r'\[[^\]]+\]\([^\)]+\)', html)
print('  markdown links remaining:', len(md_links))
name_in_code = re.findall(r'<code>[^<]*<name>[^<]*</code>', html)
print('  <name> in code:', len(name_in_code))
backslash_in_code = re.findall(r'<code>[^<]*\\[^<]*</code>', html)
print('  literal \\ in code:', len(backslash_in_code))
br_in_p = re.findall(r'<p>[^<]*<br />', html)
print('  <br /> inside <p>:', len(br_in_p))

# Check H2s for nested <p>
h2_spans = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
has_p_in_h2 = [h for h in h2_spans if '<p' in h.lower()]
print('  <p> inside <h2>:', len(has_p_in_h2))

# Check 8 H2s
h2_list = re.findall(r'<h2>(.*?)</h2>', html)
print('  H2 text list:')
for h in h2_list:
    print('   -', h[:80])

with open(OUT_PATH, 'w') as f:
    f.write(html)
print(f'\nWrote {OUT_PATH}')