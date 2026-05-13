const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-14-archimedes-principle-buoyancy/';

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Users/quyue/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const posterPath = path.join(articleDir, 'poster.html');
  await page.setContent(fs.readFileSync(posterPath, 'utf8'), { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(articleDir, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster screenshot saved');
})();
