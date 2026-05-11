#!/usr/bin/env python3
"""Extract paragraphs from article markdown for highlight card creation."""
import sys

article_path = sys.argv[1] if len(sys.argv) > 1 else "article.md"

with open(article_path, "r") as f:
    content = f.read()

# Remove frontmatter
if content.startswith("---"):
    parts = content.split("---", 2)
    content = parts[2].strip()

# Split into paragraphs (lines separated by blank lines)
paragraphs = []
current = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        if current:
            para = " ".join(current)
            if para:
                paragraphs.append(para)
            current = []
    else:
        current.append(line)

if current:
    para = " ".join(current)
    if para:
        paragraphs.append(para)

# Print with index
for i, p in enumerate(paragraphs):
    preview = p[:120] + "..." if len(p) > 120 else p
    print(f"[{i}] {preview}")
    print()
