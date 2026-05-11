const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-electromagnetic-spectrum';

const cards = [
  {
    num: '01',
    theme: 'ocean',
    eyebrow: 'KEY INSIGHT',
    title: '15 Orders of Magnitude',
    dek: 'Radio waves can be hundreds of kilometers long. Gamma rays can be smaller than an atom\'s nucleus. They all travel at the same speed.',
    quote: '"c = \u03BBf  \u00b7  E = hf"',
    bullets: ['Same phenomenon, different wavelengths', 'All travel at 299,792,458 m/s', 'Energy scales with frequency']
  },
  {
    num: '02',
    theme: 'ember',
    eyebrow: 'DANGER ZONE',
    title: 'The UV Problem for Space Colonies',
    dek: 'Earth\'s atmosphere blocks most ultraviolet radiation. Astronauts on the Moon or Mars receive far more UV than any human evolved to handle.',
    quote: '"The electromagnetic spectrum\'s most dangerous band arrives unfiltered."',
    bullets: ['UV breaks DNA bonds directly', 'Ozone layer is Earth\'s only shield', 'Every colony plan must account for this']
  },
  {
    num: '03',
    theme: 'forest',
    eyebrow: 'COSMIC SCALE',
    title: 'When a Star Dies in Seconds',
    dek: 'Gamma-ray bursts are the most violent events in the observable universe — a single burst can outshine an entire galaxy.',
    quote: '"More energy in seconds than the sun emits over 10 billion years."',
    bullets: ['NASA\'s Fermi telescope detects several per week', 'Outgamma-ray burstsshines entire galaxies', 'Produced by collapsing massive stars']
  }
];

const themes = {
  ocean: { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8', text: '#ffffff', dim: '#a0d4e8' },
  ember: { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529', text: '#ffffff', dim: '#d0a090' },
  forest: { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77', text: '#ffffff', dim: '#90e8b8' }
};

(async () => {
  const browser = await chromium.launch();
  for (const c of cards) {
    const t = themes[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + t.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + t.accent + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black leading-[1.0] mb-6" style="color:' + t.text + ';">' + c.title + '</h2>' +
      '<p class="text-[22px] leading-relaxed mb-8" style="color:' + t.dim + ';">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + t.accent + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px]" style="color:' + t.dim + ';">\u2022 ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Saved card-' + c.num + '.png');
  }
  await browser.close();
})();
