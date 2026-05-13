
const { chromium } = require('/Users/quyue/.nvm/versions/node/v24.13.0/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-13-angular-momentum-conservation';

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/homebrew/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  const posterPath = path.join(articleDir, 'poster.html');
  await page.setContent(fs.readFileSync(posterPath, 'utf8'), { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(articleDir, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster screenshot saved');
})();
