const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlPath = path.join(__dirname, 'poster.html');
  const screenshotPath = path.join(__dirname, 'poster.png');

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const fs = require('fs');
  const html = fs.readFileSync(htmlPath, 'utf8');
  
  await page.setContent(html);
  await page.waitForTimeout(3000);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  await browser.close();
  console.log('Poster saved to:', screenshotPath);
})();
