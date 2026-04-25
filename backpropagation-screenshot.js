const { chromium } = require('/Users/quyue/.hermes/hermes-agent/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  
  const htmlPath = '/tmp/backpropagation-poster.html';
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
  
  const screenshotPath = '/Users/quyue/www/blog/2026-04-25-backpropagation-deep-dive/poster.png';
  await page.screenshot({ path: screenshotPath, fullPage: false });
  
  console.log('Screenshot saved to:', screenshotPath);
  await browser.close();
})();
