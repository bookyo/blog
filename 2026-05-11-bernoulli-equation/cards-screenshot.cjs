const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-11-bernoulli-equation';

(async () => {
  const browser = await chromium.launch();
  const cards = [
    { html: 'card-01-core-principle.html', output: 'card-01-core-principle.png' },
    { html: 'card-02-applications.html', output: 'card-02-applications.png' },
    { html: 'card-03-visualization.html', output: 'card-03-visualization.png' },
  ];
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardPath = path.join(articleDir, card.html);
    await page.setContent(fs.readFileSync(cardPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, card.output), fullPage: true });
    await page.close();
    console.log('Card done:', card.output);
  }
  await browser.close();
  console.log('All cards done');
})();
