const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-coriolis-force-earth-rotation';

const cards = [
  {
    num: '01',
    eyebrow: 'HISTORICAL REVELATION',
    title: 'The Pendulum That Showed Earth Spinning',
    dek: 'Foucault hung a 28kg brass bob from the Paris Panthéon dome in 1851. The swing plane rotated — not the pendulum, but the Earth beneath it.',
    quote: '"The first direct, visible proof from the surface of the Earth that our planet rotates."',
    bullets: ['28kg brass bob, 67-meter wire', '11° rotation per minute at Paris latitude', 'No electronics — just match smoke and sand'],
    theme: 'ocean'
  },
  {
    num: '02',
    eyebrow: 'EVERYDAY PHYSICS',
    title: 'Why Every Hurricane Spins the Same Way',
    dek: 'The Coriolis force shapes all large-scale motion on Earth. In the Northern Hemisphere, air deflects right — making all cyclones counterclockwise.',
    quote: '"Without the Coriolis effect, air would simply flow into the low-pressure center and equalize."',
    bullets: ['No hurricanes within 5° of the equator', 'Gulf Stream and jet stream both Coriolis-shaped', 'Trade winds deflect into predictable patterns'],
    theme: 'forest'
  },
  {
    num: '03',
    eyebrow: 'SURPRISING APPLICATION',
    title: 'Why WWI Artillery Consistently Missed',
    dek: 'A half-degree Coriolis deflection at 10km range means an 87-meter miss. The Paris Gun had to aim degrees off-target just to hit the city.',
    quote: '"Pull the plug straight up and the water may not rotate noticeably. Your toilet is not a laboratory."',
    bullets: ['WWI French artillery off by ~87m', 'Paris Gun aimed ~1° off to compensate', 'GPS-guided munitions compute this in real time'],
    theme: 'ember'
  }
];

const THEMES = {
  ocean:  { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' },
  ember:  { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
};

(async () => {
  const browser = await chromium.launch();
  for (const c of cards) {
    const t = THEMES[c.theme];
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + t.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + t.accent + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[68px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + t.accent + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' screenshot saved');
  }
  await browser.close();
  console.log('All cards done');
})();
