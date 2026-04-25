const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  
  await page.goto('file:///Users/quyue/www/blog/2026-04-26-photoelectric-effect-quantum-light/poster.html', { waitUntil: 'networkidle' });
  
  // Wait for animations to start
  await page.waitForTimeout(500);
  
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-26-photoelectric-effect-quantum-light/poster.png', fullPage: false });
  
  await browser.close();
  console.log('Screenshot saved to poster.png');
})();
