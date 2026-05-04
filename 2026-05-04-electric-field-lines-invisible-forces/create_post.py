#!/usr/bin/env python3
import json
import requests
from datetime import datetime, timedelta

AUTH = ("bted2k@gmail.com", "zVlf aCkm vB79 GjXc zVrJ dSuH")
BLOG_URL = "https://blog.flowrust.com"

# Read HTML with embedded cards
with open("article_with_cards.html") as f:
    content = f.read()

# Title
title = "Why You Can't Touch Anything — And Why That's the Most Important Fact in Physics"

# Create post - Step 1: create with past date
past_date = "2026-05-03T12:00:00"
post_data = {
    "title": title,
    "slug": "electric-field-lines-invisible-forces",
    "status": "publish",
    "content": content,
    "featured_media": 2247,
    "date_gmt": past_date,
    "tags": [172],  # physics tag
}

resp = requests.post(
    f"{BLOG_URL}/wp-json/wp/v2/posts",
    auth=AUTH,
    headers={"Content-Type": "application/json"},
    json=post_data,
    timeout=30
)
print(f"Step 1 status: {resp.status_code}")
result = resp.json()
post_id = result.get("id")
print(f"Post ID: {post_id}")
print(f"Status returned: {result.get('status')}")

if post_id:
    # Step 2: force publish
    update_data = {
        "status": "publish",
        "date_gmt": past_date,
    }
    resp2 = requests.post(
        f"{BLOG_URL}/wp-json/wp/v2/posts/{post_id}",
        auth=AUTH,
        headers={"Content-Type": "application/json"},
        json=update_data,
        timeout=30
    )
    print(f"Step 2 status: {resp2.status_code}")
    result2 = resp2.json()
    print(f"Final status: {result2.get('status')}")
    print(f"Post URL: {result2.get('link')}")

    # Save post info
    with open("wp-post-id.json", "w") as f:
        json.dump({"post_id": post_id, "url": result2.get('link')}, f)
