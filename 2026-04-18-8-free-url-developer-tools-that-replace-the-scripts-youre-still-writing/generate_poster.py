from playwright.sync_api import sync_playwright
import os

def generate_url_devtools_poster(output_path):
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>body { font-family: 'Outfit', sans-serif; }</style>
</head>
<body class="bg-black flex items-center justify-center min-h-screen">
  <div class="w-[1080px] text-center px-[108px] py-24">
    <h1 class="text-[96px] font-black text-white tracking-tight leading-none">8 URL DEV TOOLS</h1>
    <p class="text-[48px] font-bold text-[#00FF94] mt-6 tracking-tight text-center">FREE • BROWSER-BASED</p>
    <p class="text-[18px] text-[#666666] mt-10 leading-relaxed text-center">Encode • Decode • Validate • Parse • Build • Shorten • Expand • User-Agent</p>
    <div class="mt-16 mx-auto w-16 h-1 bg-[#00FF94] opacity-80"></div>
    <p class="text-[24px] text-[#444444] mt-8 font-mono">elysiatools.com</p>
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

output = "/tmp/url-devtools-poster.png"
generate_url_devtools_poster(output)
print(f"Poster saved to {output}")
