const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  const filePath = 'file://' + path.resolve(__dirname, 'poster.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for animation to run a bit
  await page.waitForTimeout(1500);

  await page.screenshot({ path: path.resolve(__dirname, 'poster.png'), fullPage: false });

  await browser.close();
  console.log('Screenshot saved to poster.png');
})();
