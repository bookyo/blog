const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  await page.goto('file:///Users/quyue/www/blog/2026-04-30-bezier-curves/poster.html');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-30-bezier-curves/poster.png', fullPage: true });
  
  await browser.close();
  console.log('Poster screenshot done');
})();
