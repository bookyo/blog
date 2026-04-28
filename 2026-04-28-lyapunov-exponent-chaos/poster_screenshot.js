const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = path.join(__dirname, 'poster.html');
  await page.goto(`file://${htmlPath}`);
  await page.waitForTimeout(2000);
  
  const outputPath = path.join(__dirname, 'poster.png');
  await page.screenshot({ path: outputPath, fullPage: false });
  
  console.log('Poster saved to:', outputPath);
  await browser.close();
})();