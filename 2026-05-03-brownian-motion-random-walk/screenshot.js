
import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const htmlPath = path.join(__dirname, 'poster.html');
  const htmlContent = require('fs').readFileSync(htmlPath, 'utf8');
  
  await page.setContent(htmlContent);
  await page.waitForTimeout(3000);
  
  const screenshotPath = path.join(__dirname, 'poster.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  
  console.log('Screenshot saved to:', screenshotPath);
  await browser.close();
})();
