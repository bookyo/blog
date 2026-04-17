import json
import urllib.request
import urllib.error
import base64
import sys

# Read article content
with open('/Users/quyue/www/blog/2026-04-17-bayes-theorem/article.md', 'r') as f:
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

title = "Why a Positive Medical Test Doesn't Mean What You Think It Does"
slug = "why-a-positive-medical-test-doesnt-mean-what-you-think-it-does"

# WordPress Application Passwords auth
password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
url = "https://blog.flowrust.com/wp-json/wp/v2/posts"

credentials = f"bted2k@gmail.com:{password}"
auth = base64.b64encode(credentials.encode()).decode()

data = json.dumps({
    "title": title,
    "content": content,
    "status": "publish",
    "slug": slug,
    "date": "2026-04-17T12:00:00"
}).encode()

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        print(f'SUCCESS!')
        print(f'Post ID: {result.get("id")}')
        print(f'URL: {result.get("link")}')
        print(f'Status: {result.get("status")}')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code}: {body[:500]}')
    sys.exit(1)
except Exception as ex:
    print(f'Exception: {ex}')
    sys.exit(1)
