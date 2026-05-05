#!/usr/bin/env python3
"""Extract key paragraphs from article markdown for highlight card generation."""
import re
import sys

def extract_paragraphs(md_path):
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Strip frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        content = parts[2].strip()
    
    # Remove markdown syntax for analysis
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove horizontal rules
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    
    # Split into paragraphs
    paragraphs = []
    current = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current:
                para_text = ' '.join(current)
                if len(para_text) > 50:  # Skip very short paragraphs
                    paragraphs.append(para_text)
                current = []
        else:
            current.append(line)
    
    if current:
        para_text = ' '.join(current)
        if len(para_text) > 50:
            paragraphs.append(para_text)
    
    # Print paragraphs with index
    print(f"Found {len(paragraphs)} paragraphs:\n")
    for i, p in enumerate(paragraphs):
        preview = p[:120] + '...' if len(p) > 120 else p
        print(f"[{i}] {preview}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_paragraphs.py <article.md>")
        sys.exit(1)
    extract_paragraphs(sys.argv[1])
