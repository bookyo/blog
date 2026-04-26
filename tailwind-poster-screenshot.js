
const { chromium } = require('/Users/quyue/.hermes/hermes-agent/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });

  await page.goto('file:///tmp/tailwind-poster.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  const posterPath = '/Users/quyue/www/blog/2026-04-26-tailwind-css-samples/poster.png';
  await page.screenshot({ path: posterPath, type: 'png', omitBackground: false });

  console.log('Poster saved to:', posterPath);
  await browser.close();
})();
