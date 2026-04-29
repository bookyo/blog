const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  await page.goto('file:///Users/quyue/www/blog/2026-04-29-turing-pattern-reaction-diffusion/poster.html');
  await page.waitForTimeout(2000);
  
  await page.screenshot({ 
    path: '/Users/quyue/www/blog/2026-04-29-turing-pattern-reaction-diffusion/poster.png',
    fullPage: false 
  });
  
  await browser.close();
  console.log('Poster screenshot saved');
})();
