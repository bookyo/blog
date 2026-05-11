const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-11-quantum-wave-collapse';
const cards = [
  { html: 'card-01-core-concept.html', output: 'card-01-core-concept.png' },
  { html: 'card-02-collapse-measurement.html', output: 'card-02-collapse-measurement.png' },
  { html: 'card-03-tunneling-double-well.html', output: 'card-03-tunneling-double-well.png' },
];

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(fs.readFileSync(path.join(articleDir, card.html), 'utf8'), { waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(articleDir, card.output), fullPage: true });
    await page.close();
    console.log(`Screenshot saved: ${card.output}`);
  }
  await browser.close();
  console.log('All cards done');
})();
