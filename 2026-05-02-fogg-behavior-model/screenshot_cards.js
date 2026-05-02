
const { chromium } = require('playwright');
const path = require('path');

const cards = ['card-01-core-equation', 'card-02-motivation-myth', 'card-03-tiny-habits'];

(async () => {
  const browser = await chromium.launch();
  
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const htmlPath = path.join(__dirname, card + '.html');
    await page.goto('file://' + htmlPath);
    await page.waitForTimeout(2000);
    const outputPath = path.join(__dirname, card + '.png');
    await page.screenshot({ path: outputPath, fullPage: true });
    console.log('Screenshot:', outputPath);
    await page.close();
  }
  
  await browser.close();
  console.log('All done');
})();
