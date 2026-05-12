const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-12-light-scattering-rayleigh';

const cards = [
  { html: path.join(articleDir, 'card-01-blue-wins-violet.html'), output: path.join(articleDir, 'card-01.png') },
  { html: path.join(articleDir, 'card-02-sunset-atmosphere.html'), output: path.join(articleDir, 'card-02.png') },
  { html: path.join(articleDir, 'card-03-clouds-white.html'), output: path.join(articleDir, 'card-03.png') },
];

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.goto('file://' + card.html);
    await page.waitForTimeout(2000);
    await page.screenshot({ path: card.output, fullPage: true });
    await page.close();
    console.log('Screenshot:', card.output);
  }
  await browser.close();
  console.log('All cards done');
})();
