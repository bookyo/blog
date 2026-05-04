#!/usr/bin/env python3
import sys

with open("article.md") as f:
    content = f.read()

# Extract paragraphs between headings
paragraphs = []
current_heading = ""
current_text = []

for line in content.split("\n"):
    line = line.strip()
    if line.startswith("## "):
        if current_text and current_heading:
            paragraphs.append({
                "heading": current_heading,
                "text": " ".join(current_text)
            })
        current_heading = line[3:].strip()
        current_text = []
    elif line and not line.startswith("#") and not line.startswith("---") and not line.startswith("**"):
        current_text.append(line)

if current_text and current_heading:
    paragraphs.append({
        "heading": current_heading,
        "text": " ".join(current_text)
    })

for i, p in enumerate(paragraphs):
    print(f"[{i}] {p['heading']}")
    print(f"    {p['text'][:200]}...")
    print()
