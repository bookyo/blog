const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = path.join(__dirname, 'poster.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');
  
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  const outputPath = path.join(__dirname, 'poster.png');
  await page.screenshot({ path: outputPath, fullPage: true });
  
  await browser.close();
  console.log('Screenshot saved to:', outputPath);
})();
