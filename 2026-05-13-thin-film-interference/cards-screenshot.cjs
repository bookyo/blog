const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-13-thin-film-interference';

(async () => {
  const browser = await chromium.launch();
  const cards = [
    { html: 'card-01-formula.html', output: 'card-01-formula.png' },
    { html: 'card-02-newtons-rings.html', output: 'card-02-newtons-rings.png' },
    { html: 'card-03-lens-coatings.html', output: 'card-03-lens-coatings.png' },
  ];
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(fs.readFileSync(path.join(articleDir, card.html), 'utf8'), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, card.output), fullPage: true });
    await page.close();
    console.log('Saved:', card.output);
  }
  await browser.close();
  console.log('All cards done');
})();
