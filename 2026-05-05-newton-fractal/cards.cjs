
const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-05-newton-fractal';

const cards = [
  {
    num: '01',
    eyebrow: 'HISTORICAL CONTEXT',
    title: 'The Algorithm Nobody Associated With Fractals',
    dek: 'Newton wrote down his method in 1669. Raphson refined it in 1690. For 300 years, nobody thought to ask what happened when you ran it on complex numbers.',
    quote: '"z_{n+1} = z_n - f(z_n)/f\'(z_n)"',
    bullets: ['Developed 1669 by Newton', 'Refined 1690 by Raphson', 'Works identically on complex plane'],
    theme: 'forest'
  },
  {
    num: '02',
    eyebrow: 'KEY INSIGHT',
    title: 'The Fractal Boundary Problem',
    dek: 'Two points incredibly close to each other can converge to completely different roots. The boundaries between basins of attraction are infinitely intricate — at every scale.',
    quote: '"Sensitive dependence on initial conditions"',
    bullets: ['Infinite complexity at every zoom level', 'Boundaries exceed 1D fractal dimension', 'Same mechanism as chaos theory'],
    theme: 'ocean'
  },
  {
    num: '03',
    eyebrow: 'MATHEMATICAL CONTRAST',
    title: 'Not a Single Fractal — An Infinite Family',
    dek: 'The Mandelbrot set is one object. Newton fractals are parameterized by the polynomial itself. Every choice of f(z) produces a different fractal with its own character.',
    quote: '"z^4 - 1 produces four-way symmetry"',
    bullets: ['z^3 - 1: three basins', 'z^4 - 1: four basins', 'z^4 + 1: entirely different patterns'],
    theme: 'ember'
  }
];

const THEMES = {
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' },
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
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
      '<h2 class="text-[68px] font-black text-white leading-[1.05] mb-6">' + c.title + '</h2>' +
      '<p class="text-[20px] text-[' + t.muted + '] leading-relaxed mb-6">' + c.dek + '</p>' +
      '<p class="text-[16px] text-[' + t.accent + '] font-mono mb-6">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[15px] text-[#a0a0b0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  await browser.close();
  console.log('All cards done');
})();
