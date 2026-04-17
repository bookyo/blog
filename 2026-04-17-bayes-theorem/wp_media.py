import json
import urllib.request
import urllib.error
import base64
import sys

# Upload poster as media
with open('/Users/quyue/www/blog/2026-04-17-bayes-theorem/poster.png', 'rb') as f:
    image_data = f.read()

url = "https://blog.flowrust.com/wp-json/wp/v2/media"

password = "zVlf aCkm vB79 GjXc zVrJ dSuH"
credentials = f"bted2k@gmail.com:{password}"
auth = base64.b64encode(credentials.encode()).decode()

req = urllib.request.Request(url, data=image_data, method='POST')
req.add_header('Content-Type', 'image/png')
req.add_header('Authorization', 'Basic ' + auth)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
req.add_header('Content-Disposition', 'attachment; filename="poster.png"')

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        media_id = result.get('id')
        media_url = result.get('source_url')
        print(f'Media uploaded!')
        print(f'Media ID: {media_id}')
        print(f'Media URL: {media_url}')

        # Update post with featured image
        post_id = 1394
        update_url = f"https://blog.flowrust.com/wp-json/wp/v2/posts/{post_id}"
        
        update_data = json.dumps({
            "featured_media": media_id
        }).encode()
        
        update_req = urllib.request.Request(update_url, data=update_data, method='POST')
        update_req.add_header('Content-Type', 'application/json')
        update_req.add_header('Authorization', 'Basic ' + auth)
        update_req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        with urllib.request.urlopen(update_req, timeout=30) as resp:
            update_result = json.loads(resp.read().decode())
            print(f'Post updated with featured image!')
            print(f'Post URL: {update_result.get("link")}')
            
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code}: {body[:500]}')
    sys.exit(1)
except Exception as ex:
    print(f'Exception: {ex}')
    sys.exit(1)
