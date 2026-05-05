const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
    await page.goto('file:///tmp/card-infinitely-complicated-boundaries.html');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-28-attractor-basin-fractal-chaos/card-infinitely-complicated-boundaries.png', fullPage: true });
    await browser.close();
    console.log('Screenshot saved: card-infinitely-complicated-boundaries.png');
})();
