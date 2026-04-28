const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = 'file://' + path.resolve('poster.html');
  await page.goto(htmlPath);
  await page.waitForTimeout(2000);
  
  await page.screenshot({ path: 'poster.png', fullPage: false });
  await browser.close();
  console.log('Screenshot saved to poster.png');
})();
