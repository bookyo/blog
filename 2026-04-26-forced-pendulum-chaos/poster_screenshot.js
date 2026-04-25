const { chromium } = require('/Users/quyue/.hermes/hermes-agent/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });
  const filePath = 'file://' + path.resolve('/tmp/forced-pendulum-poster.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/tmp/forced-pendulum-poster.png' });
  await browser.close();
})();
