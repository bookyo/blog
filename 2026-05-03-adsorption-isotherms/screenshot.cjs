const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const workDir = path.join(process.env.HOME || '/Users/quyue', 'www/blog/2026-05-03-adsorption-isotherms');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });

  const posterHtml = fs.readFileSync(path.join(workDir, 'poster.html'), 'utf8');
  await page.setContent(posterHtml, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  const outPath = path.join(workDir, 'poster.png');
  await page.screenshot({ path: outPath, fullPage: true });
  console.log('Screenshot saved to:', outPath);

  await browser.close();
})();
