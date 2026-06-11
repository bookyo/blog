"""Screenshot poster + 3 cards via Python Playwright CLI."""
import subprocess
import os

ARTICLE_DIR = '/Users/quyue/www/blog/2026-06-11-slug-validator-the-rules-behind-every-clean-url'
PW = '/Library/Frameworks/Python.framework/Versions/3.9/bin/playwright'

targets = ['poster', 'card1', 'card2', 'card3']
for name in targets:
    result = subprocess.run(
        [PW, 'screenshot', '--browser', 'chromium', '--full-page',
         f'file://{ARTICLE_DIR}/{name}.html',
         f'{ARTICLE_DIR}/{name}.png'],
        capture_output=True, text=True, timeout=90,
    )
    rc = result.returncode
    out = (result.stdout or result.stderr).strip()[:120]
    size = os.path.getsize(f'{ARTICLE_DIR}/{name}.png') if os.path.exists(f'{ARTICLE_DIR}/{name}.png') else 0
    print(f'{name}: returncode={rc} size={size} output={out}')
