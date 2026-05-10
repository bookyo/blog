const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-11-scanning-tunneling-microscope';

const cards = [
  { html: 'card-01-core-equation.html', output: 'card-01-core-equation.png' },
  { html: 'card-02-quantum-manipulation.html', output: 'card-02-quantum-manipulation.png' },
  { html: 'card-03-interactive-tool.html', output: 'card-03-interactive-tool.png' },
];

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(fs.readFileSync(path.join(articleDir, card.html), 'utf8'), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, card.output), fullPage: true });
    await page.close();
    console.log('Screenshot:', card.output);
  }
  await browser.close();
  console.log('All cards done');
})();
