
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = process.cwd();
const cardFiles = ['card-01.html', 'card-02.html', 'card-03.html'];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cardFiles.length; i++) {
    const cardHtml = fs.readFileSync(path.join(workDir, cardFiles[i]), 'utf8');
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(cardHtml, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    const outputName = cardFiles[i].replace('.html', '.png');
    await page.screenshot({ path: outputName, fullPage: true });
    console.log('Screenshot:', outputName);
    await page.close();
  }
  await browser.close();
  console.log('All cards done!');
})();
