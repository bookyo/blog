const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-11-neutron-stars';

(async () => {
  const browser = await chromium.launch();
  const cards = [
    { html: 'card-01-core-density.html', output: 'card-01-core-density.png' },
    { html: 'card-02-pulsar-discovery.html', output: 'card-02-pulsar-discovery.png' },
    { html: 'card-03-tov-limit.html', output: 'card-03-tov-limit.png' },
  ];
  for (let i = 0; i < cards.length; i++) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardPath = path.join(articleDir, cards[i].html);
    await page.setContent(fs.readFileSync(cardPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, cards[i].output), fullPage: true });
    await page.close();
    console.log(`Card ${i+1} screenshot saved`);
  }
  await browser.close();
  console.log('All cards done');
})();
