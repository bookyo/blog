const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  
  const cardFiles = ['card-01.html', 'card-02.html', 'card-03.html'];
  
  for (let i = 0; i < cardFiles.length; i++) {
    const cardHtml = fs.readFileSync(path.join(process.cwd(), cardFiles[i]), 'utf8');
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(cardHtml, { waitUntil: 'networkidle' });
    await page.screenshot({ path: `card-${String(i+1).padStart(2,'0')}.png`, fullPage: true });
    await page.close();
    fs.unlinkSync(path.join(process.cwd(), cardFiles[i])); // clean up temp HTML
    console.log(`Saved card-${String(i+1).padStart(2,'0')}.png`);
  }
  
  await browser.close();
  console.log('Done');
})();
