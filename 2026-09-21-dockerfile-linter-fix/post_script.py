"""POST the WP 7395 fix back to WordPress."""
import json, requests, sys

WP_URL = 'https://blog.flowrust.com'
WP_USER = 'bted2k@gmail.com'
WP_PASS = 'zVlf aCkm vB79 GjXc zVrJ dSuH'
POST_ID = 7395

with open(f'wp_{POST_ID}_fixed.json') as f:
    d = json.load(f)
fixed_content = d['content']

# Sanity assertions before POST
assert '<code><code' not in fixed_content, 'still has nested <code><code>'
import re
assert len(re.findall(r'<pre><code class="language-', fixed_content)) == 4, 'expected 4 <pre><code> blocks'

# POST (NOT PATCH — per WP 5692)
url = f'{WP_URL}/wp-json/wp/v2/posts/{POST_ID}'
resp = requests.post(
    url,
    auth=(WP_USER, WP_PASS),
    json={'content': fixed_content},
    timeout=60,
)
print(f'POST status: {resp.status_code}')
resp.raise_for_status()
result = resp.json()
print(f'Updated post {POST_ID}: {result.get("link")}')