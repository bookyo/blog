const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 675 });

  const filePath = 'file:///tmp/poster.html';
  await page.goto(filePath, { waitUntil: 'networkidle' });

  await page.evaluate(() => {
    document.querySelectorAll('*').forEach(el => {
      const style = window.getComputedStyle(el);
      if (style.animationName && style.animationName !== 'none') {
        el.style.animationPlayState = 'paused';
      }
    });
  });

  await page.waitForTimeout(500);

  const posterPath = '/Users/quyue/www/blog/2026-04-23-why-free-users-subsidize-your-product-two-sided-market-economics/poster.png';
  await page.screenshot({ path: posterPath, type: 'png', omitBackground: false });

  console.log('Poster saved to:', posterPath);
  await browser.close();
})();
