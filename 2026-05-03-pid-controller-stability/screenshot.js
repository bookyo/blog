import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const html = readFileSync(join(__dirname, 'poster.html'), 'utf8');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
await page.setContent(html);
await page.waitForTimeout(3000);
await page.screenshot({ path: join(__dirname, 'poster.png'), fullPage: true });
await browser.close();
console.log('Poster saved.');
