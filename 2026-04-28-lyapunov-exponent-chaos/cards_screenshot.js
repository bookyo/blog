const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  
  const cards = [
    { name: 'card1', html: 'card1.html', output: 'card1.png' },
    { name: 'card2', html: 'card2.html', output: 'card2.png' },
    { name: 'card3', html: 'card3.html', output: 'card3.png' },
  ];
  
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const htmlPath = path.join(__dirname, card.html);
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(1500);
    const outputPath = path.join(__dirname, card.output);
    await page.screenshot({ path: outputPath, fullPage: true });
    console.log(`Saved: ${card.output}`);
    await page.close();
  }
  
  await browser.close();
})();