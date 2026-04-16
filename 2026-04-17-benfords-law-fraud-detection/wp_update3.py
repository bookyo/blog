import json
import urllib.request
import base64
from datetime import datetime, timezone, timedelta

# WordPress credentials
username = "bted2k@gmail.com"
app_password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
blog_url = "https://blog.flowrust.com"
credentials = f"{username}:{app_password}"
auth = base64.b64encode(credentials.encode()).decode()

post_id = 1357

# Try with timezone-aware datetime
now = datetime.now(timezone.utc)
# Set to 1 hour ago to ensure it's in the past
past = now - timedelta(hours=1)
date_str = past.isoformat()
date_gmt_str = past.isoformat()

print(f"Setting date to: {date_str}")

data = json.dumps({
    "status": "publish",
    "date": date_str,
    "date_gmt": date_gmt_str
}).encode()

url = f"{blog_url}/wp-json/wp/v2/posts/{post_id}"
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('Content-Type', 'application/json')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode())
        print(f"Status: {result.get('status')}")
        print(f"URL: {result.get('link')}")
        print(f"Date: {result.get('date')}")
        print(f"Slug: {result.get('slug')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
