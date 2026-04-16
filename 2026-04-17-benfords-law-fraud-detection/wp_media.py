import json
import urllib.request
import base64
import os

# WordPress credentials
username = "bted2k@gmail.com"
app_password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
blog_url = "https://blog.flowrust.com"
credentials = f"{username}:{app_password}"
auth = base64.b64encode(credentials.encode()).decode()

def wp_api(endpoint, method='GET', data=None, json_response=True):
    url = f"{blog_url}/wp-json/wp/v2/{endpoint}"
    headers = {
        'Authorization': 'Basic ' + auth,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    }
    if data:
        if isinstance(data, str):
            encoded = data.encode()
            headers['Content-Type'] = 'text/plain'
        else:
            encoded = json.dumps(data).encode()
            headers['Content-Type'] = 'application/json'
    else:
        encoded = None

    req = urllib.request.Request(url, data=encoded, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if json_response:
                return json.loads(resp.read().decode())
            return resp.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:300]}")
        return None

# 1. Upload poster as featured image
poster_path = '/Users/quyue/www/blog/2026-04-17-benfords-law-fraud-detection/poster.png'
poster_filename = 'benfords-law-poster.png'

with open(poster_path, 'rb') as f:
    poster_data = f.read()

import mimetypes
mime_type = mimetypes.guess_type(poster_path)[0] or 'image/png'

# Upload media
boundary = '----WordPressBoundary' + os.urandom(16).hex()
body_parts = [
    f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{poster_filename}"\r\nContent-Type: {mime_type}\r\n\r\n'.encode(),
    poster_data,
    f'\r\n--{boundary}--\r\n'.encode(),
]
body = b''.join(body_parts)

url = f"{blog_url}/wp-json/wp/v2/media"
from urllib.request import Request
req = Request(url, data=body, method='POST')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        poster_id = result.get('id')
        poster_url = result.get('source_url')
        print(f"Poster uploaded: ID={poster_id}")
        print(f"URL: {poster_url}")
except Exception as e:
    print(f"Poster upload failed: {e}")
    poster_id = None

if poster_id:
    # 2. Set featured image and update post
    post_id = 1357
    update = wp_api(f"posts/{post_id}", method='POST', data={
        "featured_media": poster_id,
        "status": "publish"
    })
    if update:
        print(f"Post {post_id} updated with featured image {poster_id}")
        print(f"Post URL: {update.get('link')}")
        print(f"Post slug: {update.get('slug')}")
    else:
        print(f"Post update failed")
