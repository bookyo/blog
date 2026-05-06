const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-07-stellar-aberration';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE INSIGHT',
      title: 'The Rain Analogy',
      dek: 'Walking through rain feels the same as light through spacetime. Both shift angle based on your velocity — one because of rain, the other because of Einstein.',
      quote: '"At Earth\'s orbital speed, the shift is exactly 20 arcseconds — Bradley\'s measured value."',
      bullets: ['Starlight deflects forward as Earth moves', 'Same angle regardless of star distance', 'James Bradley discovered this in 1725'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'RELATIVISTIC EFFECT',
      title: 'The Headlight Effect',
      dek: 'At 0.99c, a full 180° field of view compresses to just 8°. The entire universe crowds into a forward cone.',
      quote: '"Everything behind you vanishes into darkness."',
      bullets: ['Lorentz factor γ = 7.09 at v=0.99c', 'At v=0.999c, only 2.5° of sky ahead', 'This is why near-light-speed travel would show darkness behind'],
      theme: 'ember'
    },
    {
      num: '03',
      eyebrow: 'REAL-WORLD APPLICATION',
      title: 'GPS Depends on This',
      dek: 'GPS satellites require nanosecond precision. At 14,000 km/h, stellar aberration shifts signal angles by 4 arcminutes. Without relativity corrections, GPS would drift 10 km per day.',
      quote: '"Your phone\'s location accuracy is a product of Einstein\'s relativity."',
      bullets: ['GPS satellites orbit at 14,000 km/h', 'Relativistic aberration: 4 arcminutes', 'Drift without correction: 10 km/day'],
      theme: 'forest'
    }
  ];

  const THEMES = {
    ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
    ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' },
    forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
  };

  for (const c of cards) {
    const theme = THEMES[c.theme];
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:#0a0a1a;}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + theme.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + theme.accent + '] italic mb-6">— ' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  await browser.close();
})();