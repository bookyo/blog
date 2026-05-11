const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const posterPath = path.join(articleDir, 'poster.html');
  await page.setContent(fs.readFileSync(posterPath, 'utf8'), { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(articleDir, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster screenshot saved to', path.join(articleDir, 'poster.png'));
})();
