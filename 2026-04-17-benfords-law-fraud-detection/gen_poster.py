from playwright.sync_api import sync_playwright

html_path = '/Users/quyue/www/blog/2026-04-17-benfords-law-fraud-detection/poster.html'
output_path = '/Users/quyue/www/blog/2026-04-17-benfords-law-fraud-detection/poster.png'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1080, 'height': 800})
    with open(html_path, 'r') as f:
        html_content = f.read()
    page.set_content(html_content)
    page.wait_for_timeout(3000)
    page.screenshot(path=output_path, full_page=True)
    browser.close()
print(f"Saved poster to {output_path}")
