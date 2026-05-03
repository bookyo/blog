const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const workDir = '/Users/quyue/www/blog/2026-05-03-fifth-consumption-era';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const posterHtml = fs.readFileSync(path.join(workDir, 'poster.html'), 'utf8');
  await page.setContent(posterHtml, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  await page.screenshot({ path: path.join(workDir, 'poster.png'), fullPage: true });
  
  await browser.close();
  console.log('Poster screenshot saved.');
})();
