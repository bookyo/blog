
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const htmlPath = path.join(process.cwd(), 'poster.html');
  await page.setContent(require('fs').readFileSync(htmlPath, 'utf8'), { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'poster.png', fullPage: true });
  await browser.close();
  console.log('Poster screenshot saved.');
})();
