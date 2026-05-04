#!/usr/bin/env python3
import requests
import json

AUTH = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
BLOG_URL = "https://blog.flowrust.com"

def upload_image(filename, display_name):
    with open(filename, "rb") as f:
        response = requests.post(
            f"{BLOG_URL}/wp-json/wp/v2/media",
            auth=AUTH,
            headers={
                "Content-Type": "image/png",
                "Content-Disposition": f"attachment; filename={display_name}",
            },
            data=f.read(),
            timeout=60
        )
    if response.status_code not in (200, 201):
        print(f"Upload failed for {filename}: {response.status_code} {response.text}")
        return None, None
    data = response.json()
    return data["id"], data["source_url"]

# Upload poster
print("Uploading poster...")
poster_id, poster_url = upload_image("poster.png", "poster.png")
print(f"Poster: id={poster_id}, url={poster_url}")

# Upload cards
card_files = ["card-01.png", "card-02.png", "card-03.png"]
card_ids = {}
card_urls = {}
for cf in card_files:
    cid, curl = upload_image(cf, cf)
    card_ids[cf] = cid
    card_urls[cf] = curl
    print(f"Card {cf}: id={cid}, url={curl}")

# Save IDs
with open("wp-media-ids.json", "w") as f:
    json.dump({
        "poster_id": poster_id,
        "poster_url": poster_url,
        "card_ids": card_ids,
        "card_urls": card_urls
    }, f, indent=2)
print("\nSaved wp-media-ids.json")
print(json.dumps({
    "poster_id": poster_id,
    "card_ids": card_ids,
}, indent=2))
