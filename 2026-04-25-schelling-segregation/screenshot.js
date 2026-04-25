const { chromium } = require('/Users/quyue/.hermes/hermes-agent/node_modules/playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto('file:///Users/quyue/www/blog/2026-04-25-schelling-segregation/poster.html');
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-25-schelling-segregation/poster.png', type: 'png' });
  await browser.close();
})();
