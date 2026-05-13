const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-14-archimedes-principle-buoyancy/';

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Users/quyue/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
  });
  
  const cards = [
    { html: 'two-forces.html', output: 'card-01-two-forces.png' },
    { html: 'density-wins.html', output: 'card-02-density-wins.png' },
    { html: 'equilibrium.html', output: 'card-03-equilibrium.png' },
  ];
  
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardPath = path.join(articleDir, card.html);
    await page.setContent(fs.readFileSync(cardPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: path.join(articleDir, card.output), fullPage: true });
    await page.close();
    console.log('Screenshot saved:', card.output);
  }
  
  await browser.close();
  console.log('All cards done');
})();
