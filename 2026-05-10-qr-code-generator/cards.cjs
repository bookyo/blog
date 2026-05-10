const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-10-qr-code-generator';
const cards = ['card-01', 'card-02', 'card-03'];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardPath = path.join(articleDir, card + '.html');
    await page.setContent(fs.readFileSync(cardPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(articleDir, card + '.png'), fullPage: true });
    await page.close();
    console.log(card + '.png done');
  }
  await browser.close();
  console.log('All cards done');
})();
