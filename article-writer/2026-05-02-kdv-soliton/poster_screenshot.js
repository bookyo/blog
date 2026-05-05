const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const htmlPath = path.resolve('/Users/quyue/www/blog/article-writer/2026-05-02-kdv-soliton/poster.html');
  await page.goto(`file://${htmlPath}`);
  await page.waitForTimeout(2000);
  const outputPath = path.resolve('/Users/quyue/www/blog/article-writer/2026-05-02-kdv-soliton/poster.png');
  await page.screenshot({ path: outputPath, fullPage: false });
  console.log('Screenshot saved to:', outputPath);
  await browser.close();
})();
