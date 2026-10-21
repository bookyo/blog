"""Post-publish audit: REST fetch, content audit, URL HEAD probes."""
import importlib.util
import json
import re
import subprocess
import sys
import time

SKILL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing'
WP = 'https://blog.flowrust.com'
USER = 'bted2k@gmail.com'
PWD = 'zVlf aCkm vB79 GjXc zVrJ dSuH'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


wpa = load(f'{SKILL}/scripts/wp_post_audit.py', 'wp_post_audit')


def curl(args, timeout=60, extra=None):
    cmd = ['curl', '-sS', '-m', str(timeout), '--http1.1',
           '-w', '\n%{http_code}'] + (extra or []) + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout
    m = re.findall(r'^(\d{3})\s*$', out, flags=re.MULTILINE)
    code = m[-1] if m else ''
    out = re.sub(r'^\d{3}\s*$', '', out, flags=re.MULTILINE)
    return out.strip(), code


def head(url, retries=3):
    for i in range(retries):
        _, code = curl(['-o', '/dev/null', '-I', '-w', '\n%{http_code}', url],
                       timeout=25)
        m = re.findall(r'^(\d{3})\s*$', code, flags=re.MULTILINE)
        c = m[-1] if m else '000'
        if c != '000':
            return c
        time.sleep(2 * (i + 1))
    return '000'


def main():
    info = json.load(open('/tmp/wp_run103/published.json'))
    pid = info['id']
    print('auditing post', pid, info['link'])

    body_txt, code = curl(['-u', f'{USER}:{PWD}',
                           f'{WP}/wp-json/wp/v2/posts/{pid}?context=edit'])
    print('fetch:', code)
    post = json.loads(body_txt)
    raw = post['content']['raw']
    rendered = post['content']['rendered']

    print()
    print('=== post meta ===')
    print('  id:', post['id'])
    print('  status:', post['status'])
    print('  date_gmt:', post['date_gmt'])
    print('  slug:', post['slug'])
    print('  link:', post['link'])
    print('  featured_media:', post['featured_media'], '(must be 0)')

    print()
    print('=== audit_post_content (raw) ===')
    findings = wpa.audit_post_content(raw)
    print('  findings:', len(findings))
    for f in findings:
        print('   ', f)

    print()
    print('=== structure (raw) ===')
    print('  H1:', len(re.findall(r'<h1', raw)))
    print('  H2:', len(re.findall(r'<h2[^>]*>', raw)))
    print('  H3:', len(re.findall(r'<h3', raw)))
    print('  highlight-card figures:', len(re.findall(r'<figure class="highlight-card">', raw)))
    print('  article-poster figures:', len(re.findall(r'<figure class="article-poster">', raw)))
    print('  tables:', len(re.findall(r'<table', raw)))
    print('  ul/li:', len(re.findall(r'<ul>', raw)), '/', len(re.findall(r'<li>', raw)))
    ph = re.findall(r'(?:POSTER_URL|CARD\d?_URL)', raw)
    print('  placeholder leak:', len(ph), sorted(set(ph)))

    # body H2 must not duplicate the post title
    h2s = [re.sub(r'<[^>]+>', '', h).strip()
           for h in re.findall(r'<h2[^>]*>(.*?)</h2>', raw, flags=re.DOTALL)]
    title_txt = re.sub(r'<[^>]+>', '', post['title']['raw'])
    print()
    print('=== H2s ===')
    for i, h in enumerate(h2s, 1):
        print(f'  {i}. {h}')
    print('  first H2 == title?', bool(h2s and h2s[0].strip() == title_txt.strip()))

    print()
    print('=== link + image probes ===')
    anchors = re.findall(r'<a href="(https?://[^"]+)"', raw)
    imgs = re.findall(r'<img[^>]*src="([^"]+)"', raw)
    print(f'  {len(anchors)} external anchors, {len(imgs)} images')

    ok = True
    for u in sorted(set(anchors)):
        c = head(u)
        flag = 'OK' if c == '200' else '**CHECK**'
        if c != '200':
            ok = False
        print(f'   anchor {c} {flag}  {u}')
    for u in sorted(set(imgs)):
        c = head(u)
        flag = 'OK' if c == '200' else '**BROKEN**'
        if c != '200':
            ok = False
        print(f'   image  {c} {flag}  {u}')
    permalink = post['link']
    c = head(permalink)
    print(f'   permalink {c} {"OK" if c == "200" else "**CHECK**"}  {permalink}')
    if c != '200':
        ok = False

    print()
    print('AUDIT:', 'ALL PROBES OK' if ok and not findings else 'ISSUES ABOVE')


if __name__ == '__main__':
    main()