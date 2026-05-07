const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-08-hydrogen-atom-wave-function';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE REVELATION',
      title: 'Electrons Don\'t Have Addresses',
      dek: 'An electron in a hydrogen atom isn\'t orbiting — it exists as a probability cloud. There\'s no fixed path, no definite location until you measure it.',
      quote: '"The electron exists everywhere and nowhere simultaneously."',
      bullets: ['Wave function ψ encodes all possibilities', '|ψ|² gives probability density', 'Measurement collapses the cloud to one outcome'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'THE THREE NUMBERS',
      title: 'n, l, m — A Complete Address System',
      dek: 'Three integers specify every possible state of the electron. n sets the energy level. l determines the shape. m fixes the orientation.',
      quote: '"Together, these three numbers specify exactly which quantum state the electron occupies."',
      bullets: ['n: principal quantum number (energy level)', 'l: azimuthal (orbital shape: sphere, dumbbell, cloverleaf)', 'm: magnetic (spatial orientation)'],
      theme: 'ocean'
    },
    {
      num: '03',
      eyebrow: 'THE UNIVERSAL CONSTANT',
      title: 'The Bohr Radius Emerges Naturally',
      dek: 'a₀ ≈ 0.529 × 10⁻¹⁰ m — not a fitted constant, but the natural balance point where kinetic energy and Coulomb attraction meet.',
      quote: '"This isn\'t arbitrary. It emerges from the competition that defines the atom itself."',
      bullets: ['Kinetic energy wants to spread the electron', 'Coulomb attraction wants to collapse it', 'The balance defines a₀ — a universal length scale'],
      theme: 'ocean'
    }
  ];

  const themes = {
    ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8', light: '#E0F4FF' },
    forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77', light: '#E0FFF4' },
    ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529', light: '#FFE0D4' }
  };

  for (const c of cards) {
    const t = themes[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + t.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + t.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[' + t.muted + '] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + t.accent + '] italic mb-6">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#a0a0b0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  await browser.close();
})();
