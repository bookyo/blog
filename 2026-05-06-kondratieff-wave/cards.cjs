const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-06-kondratieff-wave';

// Theme: ocean
const cards = [
  {
    num: '01',
    eyebrow: 'THE PATTERN',
    title: '50-Year Economic Waves',
    dek: 'Every major technological revolution — steam, electricity, the internet — follows the same 50-60 year wave pattern. Prosperity, recession, depression, recovery. The dates shift. The shape holds.',
    quote: '"The waves keep appearing even in countries Kondratieff never studied."',
    bullets: ['1792: Steam & Textile', '1845: Steel & Railways', '1892: Electricity & Chemicals', '1948: Automobile & Computer', '1991: Information Technology'],
    theme: 'ocean'
  },
  {
    num: '02',
    eyebrow: 'WHERE WE ARE',
    title: 'The Depression Phase',
    dek: 'Every wave ends with a structural depression — not a 2-quarter recession, but a decade-scale reckoning where old technology stops generating growth. The indicators are now familiar.',
    quote: '"Old technology benefits are exhausted. The economy needs something new."',
    bullets: ['Global productivity growth at post-war lows', 'Trade volumes and capital flows declining', 'Tech giants facing saturation', 'Climate disruption accelerating costs'],
    theme: 'ocean'
  },
  {
    num: '03',
    eyebrow: 'THE FORECAST',
    title: 'Wave 6: AI + New Energy + Life Sciences',
    dek: 'If the framework holds, the trough is 2025-2028. The projected sixth wave runs 2028-2050+, driven by three converging technology clusters.',
    quote: '"The waves don\'t care whether you believe in them."',
    bullets: ['Artificial Intelligence: general-purpose infrastructure', 'New Energy: storage unlocking full electrification', 'Life Sciences: AI-accelerated drug discovery'],
    theme: 'ocean'
  }
];

const THEMES = {
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' }
};

(async () => {
  const browser = await chromium.launch();
  for (const c of cards) {
    const t = THEMES[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + t.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + t.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + t.accent + '] italic mb-6">"' + c.quote + '"</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  await browser.close();
})();
