const { chromium } = require('playwright');
const path = require('path');
const cards = [
  { html: 'card1.html', output: 'card1.png' },
  { html: 'card2.html', output: 'card2.png' },
  { html: 'card3.html', output: 'card3.png' },
];
(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const htmlPath = path.resolve(__dirname, card.html);
    await page.goto('file://' + htmlPath);
    await page.waitForTimeout(2500);
    const outPath = path.resolve(__dirname, card.output);
    await page.screenshot({ path: outPath, fullPage: true });
    console.log('Done:', card.output);
    await page.close();
  }
  await browser.close();
  console.log('All cards done');
})();
