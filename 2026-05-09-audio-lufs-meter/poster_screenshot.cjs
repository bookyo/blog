const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = path.join(__dirname, 'poster.html');
  const fs = require('fs');
  const html = fs.readFileSync(htmlPath, 'utf8');
  
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  const screenshotPath = path.join(__dirname, 'poster.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  
  console.log('Screenshot saved:', screenshotPath);
  await browser.close();
})();
