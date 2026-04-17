#!/usr/bin/env python3
import sys
# Try different SSL approaches
import ssl

API_KEY = "YLAoSq6MdnbmRk26QZkvc2mx"

# Read article
with open("2026-04-18-why-broken-things-never-fix-themselves-entropy-explained/article.md", "r") as f:
    article = f.read()

lines = article.strip().split("\n")
title = lines[0].lstrip("# ")
body = "\n".join(lines[1:]).strip()

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

import json
payload_bytes = json.dumps(payload).encode("utf-8")

# Approach 1: Try with urllib and proxy settings
import os
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1081'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1081'

try:
    import urllib.request
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        "https://api.dev.to/articles",
        data=payload_bytes,
        headers={
            "Content-Type": "application/json",
            "Api-Key": API_KEY,
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("SUCCESS via urllib!")
        print("URL:", result.get("url"))
        print("ID:", result.get("id"))
except Exception as e:
    print(f"urllib failed: {e}")

# Approach 2: Try with httpx using environment proxy
try:
    import httpx
    
    # Try with trusted env
    os.environ['SSL_CERT_FILE'] = '/private/etc/ssl/cert.pem'
    
    with httpx.Client(verify='/private/etc/ssl/cert.pem', timeout=60.0, proxy='http://127.0.0.1:1081') as client:
        resp = client.post(
            "https://api.dev.to/articles",
            json=payload,
            headers={"Api-Key": API_KEY, "Content-Type": "application/json"}
        )
        print(f"httpx status: {resp.status_code}")
        print(f"httpx body: {resp.text[:500]}")
        if resp.status_code in (200, 201):
            data = resp.json()
            print(f"SUCCESS! URL: {data.get('url')}")
except Exception as e:
    print(f"httpx failed: {type(e).__name__}: {e}")

# Approach 3: Try with requests
try:
    import requests
    
    resp = requests.post(
        "https://api.dev.to/articles",
        json=payload,
        headers={"Api-Key": API_KEY, "Content-Type": "application/json"},
        proxies={"http": "http://127.0.0.1:1081", "https": "http://127.0.0.1:1081"},
        timeout=60,
        verify='/private/etc/ssl/cert.pem'
    )
    print(f"requests status: {resp.status_code}")
    print(f"requests body: {resp.text[:500]}")
    if resp.status_code in (200, 201):
        data = resp.json()
        print(f"SUCCESS! URL: {data.get('url')}")
except Exception as e:
    print(f"requests failed: {type(e).__name__}: {e}")
