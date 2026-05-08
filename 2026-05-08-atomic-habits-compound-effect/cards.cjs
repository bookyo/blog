const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-atomic-habits-compound-effect';

const CARDS = [
  {
    num: '01',
    eyebrow: 'THE COMPOUND FORMULA',
    title: '1.01^365 = 37.78x',
    dek: 'A 1% daily improvement rate compounds into 37x growth over one year. The reverse — 1% decline — approaches zero. Small rates, massive outcomes.',
    quote: '"Habits are the compound interest of self-improvement." — James Clear',
    bullets: ['f(n) = (1 + r)^n', 'Day 100: 2.70x', 'Day 365: 37.78x', '0.99^365 ≈ 0'],
    theme: 'forest'
  },
  {
    num: '02',
    eyebrow: 'THE INVISIBLE PHASE',
    title: 'The Plateau of Latent Potential',
    dek: 'Days 0–100 feel like nothing is happening. That\'s the plateau — effort is highest, visible results are lowest. The math says this is the most critical phase.',
    quote: '"You are building potential energy. Results haven\'t appeared yet."',
    bullets: ['Plateau: 0–100 days', 'Breakthrough: ~Day 100', 'Exponential: 100+ days', 'y = A(1 - e^(-kx))'],
    theme: 'ocean'
  },
  {
    num: '03',
    eyebrow: 'IDENTITY TRANSFORMATION',
    title: 'Every Action Is a Vote',
    dek: 'I_n = I_0 · (1 + α)^n. Each action casts a ballot for the identity you want. Cast enough votes and the evidence becomes undeniable — to everyone.',
    quote: '"It\'s not goal achievement that changes identity. Identity change enables goal achievement."',
    bullets: ['Stranger → Believer', 'α = 0.1–0.2', 'Exponential accumulation', 'Social proof compounds first'],
    theme: 'ember'
  }
];

const THEMES = {
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77', bg2: '#0a1a0f' },
  ocean:  { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8', bg2: '#0a1420' },
  ember:  { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529', bg2: '#1a0f0a' }
};

(async () => {
  const browser = await chromium.launch();
  for (const c of CARDS) {
    const t = THEMES[c.theme];
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:#0a0a1a;}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + t.accent + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black leading-[1.0] mb-6" style="color:white;">' + c.title + '</h2>' +
      '<p class="text-[22px] leading-relaxed mb-8" style="color:#a0a0b0;">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-8" style="color:' + t.accent + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px]" style="color:#d0d0e0;">' + b + '</li>').join('') +
      '</ul></div></body></html>';

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card', c.num, 'saved');
  }
  await browser.close();
})();
