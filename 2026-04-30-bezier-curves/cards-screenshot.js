const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    { html: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card1.html', output: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card1.png' },
    { html: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card2.html', output: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card2.png' },
    { html: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card3.html', output: '/Users/quyue/www/blog/2026-04-30-bezier-curves/card3.png' },
  ];
  
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.goto('file://' + card.html);
    await page.waitForTimeout(2500);
    await page.screenshot({ path: card.output, fullPage: true });
    await page.close();
    console.log('Done:', card.output);
  }
  
  await browser.close();
  console.log('All cards done');
})();
