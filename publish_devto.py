#!/usr/bin/env python3
import httpx
import json

API_KEY = "YLAoSq6MdnbmRk26QZkvc2mx"

# Read article
with open("2026-04-18-why-broken-things-never-fix-themselves-entropy-explained/article.md", "r") as f:
    article = f.read()

# Extract title from first line
lines = article.strip().split("\n")
title = lines[0].lstrip("# ")
body = "\n".join(lines[1:]).strip()

# Poster URL
poster_url = "https://raw.githubusercontent.com/bookyo/blog/main/2026-04-18-why-broken-things-never-fix-themselves-entropy-explained/poster.png"

payload = {
    "article": {
        "title": title,
        "body_markdown": body,
        "published": True,
        "tag_list": "physics,mathematics,visualization,thermodynamics,entropy",
        "canonical_url": "https://elysiatools.com/en/visualizations/entropy",
        "main_image": poster_url
    }
}

# Try with httpx, following redirects, with SSL verification disabled
with httpx.Client(verify=False, timeout=60.0) as client:
    resp = client.post(
        "https://api.dev.to/articles",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Api-Key": API_KEY,
            "User-Agent": "ElysiaTools/1.0"
        }
    )
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"SUCCESS! URL: {data.get('url')}")
        print(f"ID: {data.get('id')}")
    else:
        print("FAILED")
        exit(1)
