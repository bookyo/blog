const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto('file:///tmp/schelling-poster/index.html');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/tmp/schelling-poster/poster.png' });
  await browser.close();
})();
