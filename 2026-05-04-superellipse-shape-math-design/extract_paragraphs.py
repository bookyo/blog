#!/usr/bin/env python3
"""Extract key paragraphs from article for highlight cards."""

import sys
import re

def extract_paragraphs(md_path):
    with open(md_path) as f:
        content = f.read()
    
    # Remove YAML frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        content = parts[2].strip()
    
    # Split into lines
    lines = content.split('\n')
    
    paragraphs = []
    current = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                text = ' '.join(current)
                if len(text) > 80:  # Skip very short paragraphs
                    paragraphs.append(text)
                current = []
        elif not line.startswith('#') and not line.startswith('**') and not line.startswith('|'):
            current.append(line)
        else:
            if current:
                text = ' '.join(current)
                if len(text) > 80:
                    paragraphs.append(text)
                current = []
    
    if current:
        text = ' '.join(current)
        if len(text) > 80:
            paragraphs.append(text)
    
    for i, p in enumerate(paragraphs):
        print(f"[{i}] {p[:120]}...")

if __name__ == '__main__':
    extract_paragraphs(sys.argv[1])
