const { chromium } = require('/Users/quyue/.hermes/hermes-agent/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto('file:///Users/quyue/www/blog/2026-04-25-landauer-principle/poster.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-25-landauer-principle/poster.png' });
  await browser.close();
  console.log('done');
})().catch(e => { console.error(e); process.exit(1); });
