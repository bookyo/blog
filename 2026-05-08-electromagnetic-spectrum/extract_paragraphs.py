import re

with open("/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum/article.md") as f:
    content = f.read()

# Split into paragraphs
paragraphs = re.split(r'\n\n+', content)
for i, p in enumerate(paragraphs):
    p = p.strip()
    if len(p) > 100:
        print(f"[{i}] ({len(p)} chars)")
        print(p[:300])
        print("---")
