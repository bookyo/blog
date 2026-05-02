const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 800 });
  
  const htmlPath = '/Users/quyue/www/blog/2026-05-02-n-body-gravity/poster.html';
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  const outPath = '/Users/quyue/www/blog/2026-05-02-n-body-gravity/poster.png';
  await page.screenshot({ path: outPath, fullPage: false });
  
  await browser.close();
  console.log('Screenshot saved to:', outPath);
})();
