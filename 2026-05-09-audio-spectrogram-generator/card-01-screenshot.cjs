const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
  const html = fs.readFileSync('/Users/quyue/www/blog/2026-05-09-audio-spectrogram-generator/card-01.html', 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-09-audio-spectrogram-generator/card-01.png', fullPage: true });
  await browser.close();
  console.log('card-01 done');
})();