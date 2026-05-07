const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-rlc-circuit-oscillation';
const cardFiles = ['card-01.html', 'card-02.html', 'card-03.html'];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cardFiles.length; i++) {
    const cardPath = path.join(articleDir, cardFiles[i]);
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(fs.readFileSync(cardPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, `card-0${i+1}.png`), fullPage: true });
    await page.close();
    console.log(`Card ${i+1} screenshot saved`);
    fs.unlinkSync(cardPath); // clean up temp HTML
  }
  await browser.close();
  console.log('All cards generated.');
})();
