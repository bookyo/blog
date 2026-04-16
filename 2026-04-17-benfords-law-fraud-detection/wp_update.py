import json
import urllib.request
import base64
from datetime import datetime, timezone

# WordPress credentials
username = "bted2k@gmail.com"
app_password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
blog_url = "https://blog.flowrust.com"
credentials = f"{username}:{app_password}"
auth = base64.b64encode(credentials.encode()).decode()

post_id = 1357
url = f"{blog_url}/wp-json/wp/v2/posts/{post_id}"

# Try publishing with a past date
data = json.dumps({
    "status": "publish",
    "date": "2026-04-16T20:00:00"
}).encode()

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('Content-Type', 'application/json')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode())
        print(f"Status: {result.get('status')}")
        print(f"URL: {result.get('link')}")
        print(f"Slug: {result.get('slug')}")
        print(f"Date: {result.get('date')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
