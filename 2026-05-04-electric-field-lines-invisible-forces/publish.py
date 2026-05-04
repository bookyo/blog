#!/usr/bin/env python3
import re
import requests
import json
import base64

def md_to_html(md):
    html = md

    # 1. Strip YAML frontmatter if present
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2].strip()

    # 2. Code blocks
    html = re.sub(
        r'```(\w*)\n(.*?)```',
        lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2)}</code></pre>',
        html, flags=re.DOTALL
    )

    # 3. Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # 4. Headers (before paragraph splitting)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # 5. Bold/italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 6. Images (before links)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', html)

    # 7. Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # 8. Horizontal rules
    html = re.sub(r'^---$', '<hr/>', html, flags=re.MULTILINE)

    # 9. Paragraphs
    paragraphs = []
    current_para = []
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            if current_para:
                text = ' '.join(current_para)
                paragraphs.append(f'<p>{text}</p>')
                current_para = []
            continue
        is_block = (
            line.startswith('<h') or
            line.startswith('<pre') or
            line.startswith('<hr') or
            line.startswith('<ul') or
            line.startswith('<ol') or
            line.startswith('<li') or
            line.startswith('<img') or
            line.startswith('<blockquote')
        )
        if is_block:
            if current_para:
                text = ' '.join(current_para)
                paragraphs.append(f'<p>{text}</p>')
                current_para = []
            paragraphs.append(line)
        else:
            current_para.append(line)
    if current_para:
        text = ' '.join(current_para)
        paragraphs.append(f'<p>{text}</p>')
    return '\n'.join(paragraphs)


def fix_md_to_html_output(html):
    """Apply to md_to_html output before publishing to fix known bugs."""
    # Fix 1: Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Fix 2: Broken code blocks (3-piece)
    html = re.sub(
        r'<p><code>`</code></p>\s*<p>(.+?)</p>\s*<p><code>`</code></p>',
        r'<pre><code>\1</code></pre>',
        html, flags=re.DOTALL
    )
    # Fix 3: Standalone <code class="language-"> without <pre> wrapper
    if '<pre><code' not in html and '<code class="language-' in html:
        html = html.replace('<code class="language-">', '<pre><code class="language-">').replace('</code>\n</p>', '</code></pre>\n</p>')
    # Fix 4: Restore from double-<pre> wrapper
    if '<pre><pre><code' in html:
        html = html.replace('<pre><pre><code', '<pre><code')
    return html


def find_para_end_after(html, phrase):
    """Return position after the closing </p> of the paragraph containing phrase."""
    idx = html.find(phrase)
    if idx == -1:
        return None
    end_para = html.find('</p>', idx)
    return end_para + 4


# Read article
with open("article.md") as f:
    article_md = f.read()

# Convert to HTML
html = md_to_html(article_md)
html = fix_md_to_html_output(html)

# Read card URLs from uploaded images (we'll get them from the upload step)
# For now, store the HTML and card image references
print("=== ARTICLE HTML (first 500 chars) ===")
print(html[:500])
print()
print("=== HTML LENGTH ===")
print(len(html))

# Save HTML for reference
with open("article.html", "w") as f:
    f.write(html)

print("\nSaved article.html")
