#!/usr/bin/env python3
"""Extract key paragraphs from article for highlight cards."""

import re

with open('/Users/quyue/www/blog/2026-05-09-audio-dialog-isolation/article.md', 'r') as f:
    content = f.read()

# Split by sections
# Find H2 headings and their content
sections = re.split(r'^## ', content, flags=re.MULTILINE)

for i, s in enumerate(sections[:10]):
    print(f"--- Section {i} ---")
    print(s[:300])
    print()
