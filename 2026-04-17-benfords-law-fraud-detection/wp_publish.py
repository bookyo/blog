import json
import urllib.request
import base64

# Read article content
with open('/Users/quyue/www/blog/2026-04-17-benfords-law-fraud-detection/article.md', 'r') as f:
    article_content = f.read()

# Convert markdown to HTML
import re
content = article_content
content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
paras = content.split('\n\n')
content = '</p><p>'.join(paras)
content = '<p>' + content + '</p>'
content = re.sub(r'<p>(<h[123]>.*?</h[123]>)</p>', r'\1', content)
content = re.sub(r'(<h[123]>.*?</h[123]>)<br><br>', r'\1', content)
content = re.sub(r'<br><p>', r'<p>', content)
content = re.sub(r'</p><br>', r'</p>', content)

title = "The Math Law Behind Every Fraud Detection Tool You've Ever Used"

# WordPress Application Passwords auth - try with and without spaces
passwords_to_try = [
    "zVlf aCkm vB79 GjXc zVrJ dSuH",  # with spaces
    "zVlfACkmvB79GjXczVrJdSuH",  # without spaces
]

url = "https://blog.flowrust.com/wp-json/wp/v2/posts"
results = []

for pwd in passwords_to_try:
    credentials = f"bted2k@gmail.com:{pwd}"
    auth = base64.b64encode(credentials.encode()).decode()

    data = json.dumps({
        "title": title,
        "content": content,
        "status": "publish",
        "date": "2026-04-17T08:00:00"
    }).encode()

    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Basic ' + auth)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode())
            print(f'SUCCESS with password variant')
            print('Post ID:', result.get('id'))
            print('URL:', result.get('link'))
            print('Status:', result.get('status'))
            results.append(('success', result))
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'HTTP {e.code} with password variant: {body[:200]}')
        results.append(('error', e.code, body[:200]))
    except Exception as ex:
        print(f'Exception: {ex}')
        results.append(('exception', str(ex)))

if not any(r[0] == 'success' for r in results):
    print('\nAll password attempts failed.')
