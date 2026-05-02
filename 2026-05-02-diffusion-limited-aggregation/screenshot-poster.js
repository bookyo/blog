const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });

  // Screenshot the poster HTML
  const posterPath = path.join(__dirname, 'poster.html');
  const htmlContent = fs.readFileSync(posterPath, 'utf-8');
  await page.setContent(htmlContent);
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(__dirname, 'poster.png'), fullPage: false });
  console.log('Poster screenshot saved.');

  // Now screenshot the DLA visualization
  const dlaPath = 'file:///Users/quyue/www/elysia-tools/public/math/diffusion-limited-aggregation/index.html';
  await page.goto(dlaPath, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(__dirname, 'dla-visual.png'), fullPage: false });
  console.log('DLA visualization screenshot saved.');

  await browser.close();
})();
