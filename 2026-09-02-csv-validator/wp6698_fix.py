"""Fix WP 6698 MERGED_BULLET_LIST: 2 paragraphs at indices 3 and 12.
Each merged paragraph contains items separated by &#8211; (en-dash), each item
starting with <strong>...</strong>. Convert into proper <ul><li> HTML.

WP convention: WP wpautop strips literal HTML written inline in markdown source,
BUT a manually POSTed content rendered string with explicit <ul><li> survives
because it's already part of the rendered tree (not flowing through wpautop).
This was the WP 5676 approach (c) in the umbrella pitfall — accept 1-PATCH round-trip.
"""
import json, re, requests, sys
from requests.auth import HTTPBasicAuth

AUTH = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
WP_URL = "https://blog.flowrust.com"

session = requests.Session()
session.auth = HTTPBasicAuth(*AUTH)
session.headers.update({"User-Agent": "Jarvis-Cron-Audit/1.0", "Content-Type": "application/json"})

# Load view
with open('/tmp/wp6698_view.json') as f:
    d = json.load(f)
content = d['content']['rendered']
post_id = d['id']


def split_merged_paragraph(p_html):
    """Given a <p>...</p> block whose items are separated by &#8211; <strong>X</strong>,
    split into <ul><li> items. Each item is `<strong>X</strong> body...`."""
    # Strip outer <p>...</p>
    inner = re.sub(r'^<p>|</p>$', '', p_html, flags=re.DOTALL)
    # Split on the en-dash separators — but only those that introduce a new <strong> lead
    # The pattern is: ` &#8211; <strong>X</strong> ...`
    # Use a non-greedy split on the en-dash boundary that precedes a <strong>
    parts = re.split(r'\s*&#8211;\s*(?=<strong>)', inner)
    # parts[0] is the LEAD of the first item (typically empty if it starts with &#8211;)
    # Actually parts[0] = "" because the paragraph begins with " &#8211; " — let me check
    # The paragraph starts with "&#8211; <strong>...</strong>" — so the first &#8211; is at pos 0
    # Splitting on that pattern yields ["", "x strong body", ...]
    # Drop empty leading
    parts = [p.strip() for p in parts if p.strip()]
    # Each part is already a complete <strong>X</strong> body... fragment
    li_items = ''.join(f'<li>{p}</li>' for p in parts)
    return f'<ul>{li_items}</ul>'


# Find all merged paragraphs (the ones matching the umbrella rule)
paras = list(re.finditer(r'<p>.*?</p>', content, re.DOTALL))
merged_indices = []
for i, m in enumerate(paras):
    p = m.group(0)
    n_strong = len(re.findall(r'<strong>', p))
    n_dash = len(re.findall(r'&#8211;', p))
    if n_strong >= 2 and n_dash >= 1:
        merged_indices.append(i)
print(f"Merged-paragraph indices: {merged_indices}", file=sys.stderr)

# Reconstruct content: replace each merged <p> with <ul>...</ul>, keep everything else identical.
new_content = content
n_replaced = 0
for idx in sorted(merged_indices, reverse=True):
    m = paras[idx]
    p_html = m.group(0)
    replacement = split_merged_paragraph(p_html)
    new_content = new_content[:m.start()] + replacement + new_content[m.end():]
    n_replaced += 1
print(f"Replaced {n_replaced} merged paragraphs with <ul>...</ul>", file=sys.stderr)

# Sanity: ensure the literal text of each item is preserved
# Re-run the audit on the new content
sys.path.insert(0, '/private/tmp/wp_build')
from wp_post_audit import audit_post_content
post_audit_findings = audit_post_content(new_content)
print(f"Audit findings AFTER fix: {len(post_audit_findings)}", file=sys.stderr)
for f in post_audit_findings:
    print(f"  - {f}", file=sys.stderr)

# Verify counts unchanged (must remain 8 H2 + 3 cards + 1 poster + 4 imgs)
_h2 = len(re.findall(r'<h2', new_content))
_h3 = len(re.findall(r'<h3', new_content))
_poster = len(re.findall(r'<figure class="article-poster"', new_content))
_cards = len(re.findall(r'<figure class="highlight-card"', new_content))
_imgs = len(re.findall(r'<img', new_content))
print(f"  H2={_h2} H3={_h3} poster={_poster} cards={_cards} imgs={_imgs}", file=sys.stderr)

# Save the new content for review
with open('/tmp/wp6698_fixed.html', 'w') as f:
    f.write(new_content)
print(f"Wrote /tmp/wp6698_fixed.html ({len(new_content)} chars)", file=sys.stderr)

# Print the 2 new <ul> blocks to stdout for inspection
print("\n=== NEW UL BLOCKS ===\n")
for m in re.finditer(r'<ul>.*?</ul>', new_content, re.DOTALL):
    s = m.group(0)
    if len(s) > 200:  # skip tiny accidental matches
        print(s)
        print("\n---\n")
