const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
  
  const htmlPath = path.join(process.cwd(), 'poster.html');
  const fs = require('fs');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');
  
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  await page.screenshot({ path: 'poster.png', fullPage: true });
  
  await browser.close();
  console.log('Poster screenshot saved to poster.png');
})();
