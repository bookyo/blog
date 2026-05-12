const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-13-huygens-principle';

const cards = [
  { html: 'card-01-core-insight.html', output: 'card-01-core-insight.png' },
  { html: 'card-02-three-phenomena.html', output: 'card-02-three-phenomena.png' },
  { html: 'card-03-interactive.html', output: 'card-03-interactive.png' },
];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cards.length; i++) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardPath = path.join(articleDir, cards[i].html);
    await page.goto('file://' + cardPath);
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(articleDir, cards[i].output), fullPage: true });
    await page.close();
    console.log(`Card ${i+1} done: ${cards[i].output}`);
  }
  await browser.close();
  console.log('All cards done');
})();
