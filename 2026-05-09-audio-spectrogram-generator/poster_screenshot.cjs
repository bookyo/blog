const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const html = fs.readFileSync('/Users/quyue/www/blog/2026-05-09-audio-spectrogram-generator/poster.html', 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-09-audio-spectrogram-generator/poster.png', fullPage: true });
  await browser.close();
  console.log('poster done');
})();