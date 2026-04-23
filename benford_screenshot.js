const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto('file:///tmp/benford-poster.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/tmp/benford-poster.png', type: 'png', omitBackground: false });
  console.log('Poster saved to /tmp/benford-poster.png');
  await browser.close();
})();
