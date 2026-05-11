import re, json, requests
from requests import post as requests_post
import os

work_dir = "/Users/quyue/www/blog/2026-05-09-audio-lufs-meter"

# ─── 1. md_to_html (fixed version) ───────────────────────────────────────────
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
    
    # 4. Headers — before paragraph splitting
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

# ─── 2. fix_md_to_html_output ────────────────────────────────────────────────
def convert_markdown_tables(html):
    """Convert raw markdown tables (|<col>|<col>|) in <p> tags to proper <table>."""
    table_pattern = re.compile(
        r'(<p>\|([^\n]+)\|</p>\s*<p>\|[-:\s|]+\|</p>(?:\s*<p>\|[^\n]+\|</p>)*)',
        re.DOTALL
    )
    def build_table(m):
        full = m.group(0)
        lines = re.findall(r'<p>(.+?)</p>', full, re.DOTALL)
        rows = []
        for line in lines:
            stripped = line.strip()
            if re.match(r'\||[-: ]+\|', stripped):
                continue
            cells = [c.strip() for c in stripped.split('|') if c.strip()]
            rows.append(cells)
        if len(rows) < 1:
            return full
        header = rows[0]
        thead = '<thead><tr>' + ''.join(
            f'<th style="text-align:left;padding:8px;color:#00B4D8;font-weight:700;">{cell}</th>'
            for cell in header
        ) + '</tr></thead>'
        tbody_rows = ''
        for row in rows[1:]:
            cells_html = ''.join(f'<td style="padding:8px;">{cell}</td>' for cell in row)
            tbody_rows += f'<tr style="border-bottom:1px solid #333;">{cells_html}</tr>'
        return f'<table style="width:100%;border-collapse:collapse;margin:2rem 0;">{thead}<tbody>{tbody_rows}</tbody></table>'
    return table_pattern.sub(build_table, html)

def fix_md_to_html_output(html):
    """Apply to md_to_html output before publishing to fix known bugs."""
    # Fix 0: TABLE — md_to_html does NOT convert markdown tables
    if re.search(r'<p>\|[^|]+\|[^|]*\|</p>', html):
        html = convert_markdown_tables(html)
    # Fix 1: Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Fix 2: Broken code blocks (3-piece)
    html = re.sub(
        r'<p><code>`</code></p>\s*<p>(.+?)</p>\s*<p><code>`</code></p>',
        r'<pre><code>\1</code></pre>',
        html,
        flags=re.DOTALL
    )
    # Fix 3: Standalone <code class="language-"> without <pre> wrapper
    if '<pre><code' not in html and '<code class="language-' in html:
        html = html.replace('<code class="language-">', '<pre><code class="language-">').replace('</code>\n</p>', '</code></pre>\n</p>')
    # Fix 4: Restore from double-<pre> wrapper
    if '<pre><pre><code' in html:
        html = html.replace('<pre><pre><code', '<pre><code')
    return html

# ─── 3. Read article and convert ─────────────────────────────────────────────
with open(f"{work_dir}/article.md") as f:
    raw_md = f.read()

html = md_to_html(raw_md)
html = fix_md_to_html_output(html)

print("HTML preview (first 500 chars):")
print(html[:500])
print("\nChecking for issues...")
print("  ** remaining:", '**' in html)
print("  orphan </h2>:", html.count('</h2>') != html.count('<h2>') if '<h2>' in html else False)
print("  orphan </h3>:", html.count('</h3>') != html.count('<h3>') if '<h3>' in html else False)

# Save intermediate
with open(f"{work_dir}/article_raw.html", "w") as f:
    f.write(html)
print(f"\nSaved: {work_dir}/article_raw.html")
