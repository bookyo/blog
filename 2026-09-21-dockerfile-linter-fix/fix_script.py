"""
Fix WP 7395 (Dockerfile Linter) — strip dangling outer <code> in
<code><code class="language-X">...</code> artifacts. Wrap multi-line content
in <pre> for proper block rendering.

Per WP 6376 recipe: collapse nested <code><code> to single <code>, remove
<br /> inside code. Plus, since these are multi-line code blocks originally
written as triple-fence (lost in wpautop), wrap in <pre> for correct display.
"""
import json, re, sys, time

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
POST_ID = 7395

with open(f'wp_{POST_ID}_edit.json') as f:
    post = json.load(f)
content = post['content']['raw']

print(f'Original content: {len(content)} chars')

# Step 1: Find all <code><code class="language-X">...</code> blocks (dangling outer)
# These have 1 close only — the inner </code>. The outer <code> is never closed.
pattern = re.compile(r'<code>(<code class="language-[^"]*">.*?</code>)', re.DOTALL)
matches = list(pattern.finditer(content))
print(f'Found {len(matches)} dangling-outer <code> blocks')

# Step 2: For each, fix:
#   - Remove leading <code>
#   - Wrap in <pre>...</pre> (these are multi-line code blocks)
#   - Convert inner <br> to actual newlines (more semantic for <pre>)
def fix_block(match):
    inner = match.group(1)  # <code class="language-X">...</code>
    # Extract language
    lang_m = re.search(r'class="language-([^"]*)"', inner)
    lang = lang_m.group(1) if lang_m else ''
    # Get inner content (without the <code class="..."> wrapper)
    code_inner = re.sub(r'<code[^>]*>', '', inner, count=1)
    code_inner = re.sub(r'</code>$', '', code_inner)
    # Replace <br> with \n for proper pre formatting
    code_inner = re.sub(r'<br\s*/?>', '\n', code_inner)
    # Build proper <pre><code class="language-X">...</code></pre>
    return f'<pre><code class="language-{lang}">{code_inner}</code></pre>'

fixed = pattern.sub(fix_block, content)

# Step 3: Verify
remaining = re.findall(r'<code><code\b', fixed)
print(f'After fix: {len(remaining)} remaining <code><code>')

# Step 4: Re-audit
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/scripts')
import wp_post_audit as wpa

findings = wpa.audit_post_content(fixed)
print(f'\nAudit findings after fix: {len(findings)}')
for f in findings:
    print(f'  {f}')

# Step 5: Persist
with open(f'wp_{POST_ID}_fixed.json', 'w') as f:
    json.dump({'id': POST_ID, 'content': fixed, 'original_len': len(content), 'fixed_len': len(fixed)}, f, indent=2)
print(f'\nWrote wp_{POST_ID}_fixed.json (orig {len(content)} → fixed {len(fixed)} chars)')