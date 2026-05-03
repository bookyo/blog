const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const cardFiles = ['card-01.html', 'card-02.html', 'card-03.html', 'card-04.html'];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cardFiles.length; i++) {
    const cardHtml = fs.readFileSync(path.join(__dirname, cardFiles[i]), 'utf8');
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(cardHtml, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(__dirname, `card-0${i+1}.png`), fullPage: true });
    await page.close();
    console.log(`Card ${i+1} screenshot done`);
  }
  await browser.close();
  console.log('All cards done');
})();
