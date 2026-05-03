const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const html = fs.readFileSync(path.join(__dirname, 'poster.html'), 'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(__dirname, 'poster.png'), fullPage: true });
  
  await browser.close();
  console.log('Poster screenshot done');
})();
