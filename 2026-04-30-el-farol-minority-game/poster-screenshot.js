const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const htmlPath = path.resolve(__dirname, 'poster.html');
  await page.goto('file://' + htmlPath);
  await page.waitForTimeout(3000);
  const pngPath = path.resolve(__dirname, 'poster.png');
  await page.screenshot({ path: pngPath, fullPage: true });
  await browser.close();
  console.log('Poster done:', pngPath);
})();
