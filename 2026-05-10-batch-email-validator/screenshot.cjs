const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 800 });

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

  await page.waitForTimeout(2000);

  const posterPath = '/Users/quyue/www/blog/2026-05-10-batch-email-validator/poster.png';
  await page.screenshot({ path: posterPath, type: 'png', omitBackground: false, fullPage: true });

  console.log('Poster saved to:', posterPath);
  await browser.close();
})();
