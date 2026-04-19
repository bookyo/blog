#!/usr/bin/env python3
import requests
import base64
import json
import os

# Config
WP_API = "https://blog.flowrust.com/wp-json/wp/v2/"
AUTH_EMAIL="***"
AUTH_APP_PASSWORD="***"
ARTICLE_DIR = "/Users/quyue/www/blog/2026-04-19-double-slit-quantum-trajectory-visualization"

# Create Basic Auth header
credentials = f"{AUTH_EMAIL}:{AUTH_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()

def upload_image(filename):
    """Upload an image to WordPress and return its ID"""
    filepath = os.path.join(ARTICLE_DIR, filename)
    
    with open(filepath, 'rb') as f:
        image_data = f.read()
    
    # Determine mime type
    if filename.endswith('.png'):
        mime_type = 'image/png'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        mime_type = 'image/jpeg'
    else:
        mime_type = 'application/octet-stream'
    
    # Build headers for media upload - include Content-Disposition
    media_headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": mime_type,
        "Content-Disposition": f"attachment; filename=\"{filename}\"",
    }
    
    response = requests.post(
        f"{WP_API}media",
        headers=media_headers,
        data=image_data
    )
    
    if response.status_code in (200, 201):
        result = response.json()
        print(f"Uploaded {filename}: ID = {result.get('id')}, URL = {result.get('source_url')}")
        return result.get('id'), result.get('source_url')
    else:
        print(f"Failed to upload {filename}: {response.status_code} - {response.text}")
        return None, None

# Upload all images
images = [
    "poster.png",
    "highlight-1-opening-hook.png",
    "highlight-2-trajectories.png",
    "highlight-3-probability-current.png",
    "highlight-4-closing.png"
]

results = {}
for img in images:
    img_id, img_url = upload_image(img)
    if img_id:
        results[img] = {"id": img_id, "url": img_url}

# Save results
with open("/Users/quyue/.hermes/hermes-agent/wp_media_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(results, indent=2))
