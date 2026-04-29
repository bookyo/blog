const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const htmlPath = '/Users/quyue/www/blog/2026-04-29-turing-pattern-reaction-diffusion/cards.html';
  
  for (let i = 1; i <= 4; i++) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(1000);
    
    // Show card i, hide others
    await page.evaluate((cardNum) => {
      document.querySelectorAll('.card').forEach((c, idx) => {
        c.classList.toggle('active', idx === cardNum - 1);
      });
    }, i);
    
    await page.waitForTimeout(500);
    
    const outputPath = `/Users/quyue/www/blog/2026-04-29-turing-pattern-reaction-diffusion/card${i}.png`;
    await page.screenshot({ path: outputPath, fullPage: false });
    console.log(`Card ${i} saved`);
    await page.close();
  }
  
  await browser.close();
  console.log('All cards generated');
})();
