from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def generate_center_gravity_poster(core_text, secondary_text, description, output_path):
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>body {{ font-family: 'Outfit', sans-serif; }}</style>
</head>
<body class="bg-black flex items-center justify-center min-h-screen">
  <div class="w-[1080px] text-center px-[108px] py-24">
    <h1 class="text-[120px] font-black text-white tracking-tight leading-none">{core_text}</h1>
    <p class="text-[48px] font-bold text-[#00FF94] mt-6 tracking-tight text-center">{secondary_text}</p>
    <p class="text-[18px] text-[#666666] mt-10 leading-relaxed text-center">{description}</p>
    <div class="mt-16 mx-auto w-16 h-1 bg-[#00FF94] opacity-80"></div>
  </div>
</body>
</html>'''
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1080, 'height': 800})
        page.set_content(html)
        page.wait_for_timeout(3000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
    return output_path

output = "/tmp/elysia-array-tools-poster.png"
generate_center_gravity_poster(
    "8 ARRAY TOOLS",
    "FREE • BROWSER-BASED",
    "ElysiaTools.com",
    output
)
print(f"Poster saved to {output}")
