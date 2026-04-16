import json
import urllib.request
import base64

# WordPress credentials
username = "bted2k@gmail.com"
app_password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
blog_url = "https://blog.flowrust.com"
credentials = f"{username}:{app_password}"
auth = base64.b64encode(credentials.encode()).decode()

post_id = 1357

# Step 1: Get the post with ?context=edit to see all fields
url = f"{blog_url}/wp-json/wp/v2/posts/{post_id}?context=edit"
req = urllib.request.Request(url, method='GET')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

with urllib.request.urlopen(req, timeout=20) as resp:
    post = json.loads(resp.read().decode())
    print(f"Status: {post.get('status')}")
    print(f"Date: {post.get('date')}")
    print(f"DateGMT: {post.get('date_gmt')}")
    print(f"Modified: {post.get('modified')}")
    print(f"ModifiedGMT: {post.get('modified_gmt')}")
    print(f"URL: {post.get('link')}")
    print(f"Slug: {post.get('slug')}")
    print(f"Type: {post.get('type')}")

# Step 2: Try to force publish by updating status
# The issue might be that future + past date still keeps it scheduled
# Let's try setting date to null or using a different status trick
data = json.dumps({
    "status": "publish",
    "date_gmt": "2026-04-16T12:00:00",
    "modified": "2026-04-16T20:30:00",
    "modified_gmt": "2026-04-16T12:30:00"
}).encode()

url2 = f"{blog_url}/wp-json/wp/v2/posts/{post_id}"
req2 = urllib.request.Request(url2, data=data, method='POST')
req2.add_header('Authorization', 'Basic ' + auth)
req2.add_header('Content-Type', 'application/json')
req2.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req2, timeout=20) as resp:
        result = json.loads(resp.read().decode())
        print(f"\nUpdate result:")
        print(f"Status: {result.get('status')}")
        print(f"URL: {result.get('link')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
