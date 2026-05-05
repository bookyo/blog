const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = '/tmp/logistic-poster.html';
  await page.goto(`file://${htmlPath}`);
  await page.waitForTimeout(3000);
  
  const outputPath = '/Users/quyue/www/blog/2026-05-02-logistic-map/poster.png';
  await page.screenshot({ path: outputPath, fullPage: true });
  
  await browser.close();
  console.log('Screenshot saved to:', outputPath);
})();
