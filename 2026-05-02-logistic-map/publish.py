#!/usr/bin/env python3
import re

def md_to_html(md):
    html = md
    
    # 1. Strip YAML frontmatter if present
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2].strip()
    
    # 2. Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', 
                  lambda m: f'<pre><code class="language-{m.group(1)}">{m.group(2)}</code></pre>', 
                  html, flags=re.DOTALL)
    
    # 3. Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 4. Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 5. Bold/italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 6. Images FIRST (before links)
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
                text = re.sub(r'  +', ' ', text)
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

# Read article
with open('/Users/quyue/www/blog/2026-05-02-logistic-map/article.md', 'r') as f:
    article_md = f.read()

# Convert to HTML
html = md_to_html(article_md)

# Apply post-processing fixes
# Fix 1: Bold not converted
html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
# Fix 2: Broken code blocks
html = re.sub(
    r'<p><code>`</code></p>\s*<p>(.+?)</p>\s*<p><code>`</code></p>',
    r'<pre><code>\1</code></pre>',
    html,
    flags=re.DOTALL
)

# Save HTML for review
with open('/Users/quyue/www/blog/2026-05-02-logistic-map/article.html', 'w') as f:
    f.write(html)

print("HTML saved to article.html")
print("\n=== HTML Preview (first 3000 chars) ===")
print(html[:3000])
