import re

with open('/Users/quyue/www/blog/2026-05-08-cron-expression-validator/article.md', 'r') as f:
    content = f.read()

# Strip YAML frontmatter if present
if content.startswith('---'):
    parts = content.split('---', 2)
    content = parts[2].strip()

# Split into paragraphs by double newlines
paragraphs = re.split(r'\n\n+', content)

print(f"Total paragraphs: {len(paragraphs)}")
print("=" * 80)

for i, p in enumerate(paragraphs):
    p = p.strip()
    if not p:
        continue
    # Truncate for display
    preview = p[:120] + ('...' if len(p) > 120 else '')
    print(f"\n[{i}] {preview}")
