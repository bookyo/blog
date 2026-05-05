const { chromium } = require('playwright');

const cards = [
  { html: '/tmp/mandelbrot-poster.html', output: '/Users/quyue/www/blog/2026-04-30-mandelbrot-set/poster.png', width: 1080, height: 800 },
  { html: '/tmp/card-01-mandelbrot-self-similarity.html', output: '/Users/quyue/www/blog/2026-04-30-mandelbrot-set/card-01-self-similarity.png', width: 1080, height: 900 },
  { html: '/tmp/card-02-mandelbrot-equation.html', output: '/Users/quyue/www/blog/2026-04-30-mandelbrot-set/card-02-equation.png', width: 1080, height: 900 },
];

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: card.width, height: card.height } });
    await page.goto('file://' + card.html);
    await page.waitForTimeout(3000);
    await page.screenshot({ path: card.output, fullPage: false });
    await page.close();
    console.log('Done:', card.output);
  }
  await browser.close();
  console.log('All done');
})();
