#!/usr/bin/env python3
"""Extract paragraphs from article.md for card generation."""
import sys, re

article_path = '/Users/quyue/www/blog/2026-05-08-youngs-double-slit/article.md'
md = open(article_path).read()

# Strip frontmatter
if md.startswith('---'):
    parts = md.split('---', 2)
    md = parts[2].strip()

# Split into paragraphs (double newline)
paragraphs = []
for block in re.split(r'\n\n+', md):
    block = block.strip()
    if not block:
        continue
    # Skip headings
    if block.startswith('#'):
        continue
    # Clean up: remove markdown formatting for readability
    clean = block
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
    clean = re.sub(r'\*(.+?)\*', r'\1', clean)
    clean = re.sub(r'`([^`]+)`', r'\1', clean)
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
    # Collapse whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 30:
        paragraphs.append(clean)

for i, p in enumerate(paragraphs):
    print(f"[{i}] {p[:120]}")
