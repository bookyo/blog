const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = process.cwd();
const cards = ['card1.html', 'card2.html', 'card3.html'];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cards.length; i++) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = fs.readFileSync(path.join(workDir, cards[i]), 'utf8');
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(workDir, `card-0${i+1}.png`), fullPage: true });
    await page.close();
    console.log(`Card ${i+1} done`);
  }
  await browser.close();
})();
