const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-13-solar-lunar-eclipse';

const cards = [
  { html: path.join(articleDir, 'rarest-darkness.html'), output: path.join(articleDir, 'card-01-rarest-darkness.png') },
  { html: path.join(articleDir, 'shadow-geometry.html'), output: path.join(articleDir, 'card-02-shadow-geometry.png') },
  { html: path.join(articleDir, 'orbital-tilt.html'), output: path.join(articleDir, 'card-03-orbital-tilt.png') },
];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.goto('file://' + card.html);
    await page.waitForTimeout(2500);
    await page.screenshot({ path: card.output, fullPage: true });
    await page.close();
    console.log(`Card ${i+1} done: ${card.output}`);
  }
  await browser.close();
  console.log('All cards done');
})();
