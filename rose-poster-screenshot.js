const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1200, height: 630 });
    
    await page.goto('file:///tmp/rose-poster.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    
    const buffer = await page.screenshot({ type: 'png' });
    require('fs').writeFileSync('/tmp/rose-poster.png', buffer);
    
    await browser.close();
    console.log('Screenshot saved to /tmp/rose-poster.png');
})();
