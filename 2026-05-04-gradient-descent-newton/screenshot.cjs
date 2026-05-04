const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = process.cwd();
const posterHtml = path.join(workDir, 'poster.html');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  await page.setContent(fs.readFileSync(posterHtml, 'utf8'), { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(workDir, 'poster.png'), fullPage: true });
  await page.close();
  await browser.close();
})();
