#!/usr/bin/env python3
import re

with open("/Users/quyue/www/blog/2026-05-08-ai-regex-explainer-why-your-patterns-are-a-mystery/article.md") as f:
    content = f.read()

# Remove YAML frontmatter
if content.startswith('---'):
    parts = content.split('---', 2)
    content = parts[2].strip()

# Split into paragraphs
paragraphs = []
for block in re.split(r'\n\n+', content):
    block = block.strip()
    if not block:
        continue
    # Skip markdown headers
    if block.startswith('#'):
        continue
    paragraphs.append(block)

for i, p in enumerate(paragraphs):
    print(f"[{i}] {p[:120]}...")
