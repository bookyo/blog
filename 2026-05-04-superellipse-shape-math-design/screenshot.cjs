const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = '/Users/quyue/www/blog/2026-05-04-superellipse-shape-math-design';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const htmlPath = path.join(workDir, 'poster.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(workDir, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster screenshot done');
})();
