const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-08-youngs-double-slit';

(async () => {
  const browser = await chromium.launch();
  const cards = [
    {
      num: '01',
      eyebrow: 'CORE FORMULA',
      title: 'I(θ) = I₀ · cos²(πd · sin θ / λ)',
      dek: 'The intensity distribution across the screen is a cos² function — two equal-amplitude waves superposed produce the characteristic interference pattern.',
      quote: '"The cos² function is the mathematical signature of two equal-amplitude waves superposed."',
      bullets: ['Bright fringes: Δ = mλ', 'Dark fringes: Δ = (m+½)λ', 'Central fringe (m=0) is brightest'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'KEY RELATIONSHIP',
      title: 'Δx = λL / d',
      dek: 'Fringe spacing is directly proportional to wavelength and screen distance, but inversely proportional to slit separation — closer slits produce wider fringes.',
      quote: '"Red light produces wider fringes than blue light, since Δx ∝ λ."',
      bullets: ['Longer λ → wider fringes', 'Larger L → wider fringes', 'Larger d → narrower fringes'],
      theme: 'forest'
    },
    {
      num: '03',
      eyebrow: 'QUANTUM CONNECTION',
      title: 'Wave-Particle Duality',
      dek: 'Run the double slit with individual electrons or photons — each particle passes through one slit or the other, yet the collective still produces an interference pattern.',
      quote: '"This lies at the heart of wave-particle duality."',
      bullets: ['Single-particle interference', 'Quantum superposition', 'Basis for LIGO gravitational wave detectors'],
      theme: 'ember'
    }
  ];

  const themes = {
    ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
    forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' },
    ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
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
      '<h2 class="text-[64px] font-black text-white leading-[1.05] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[' + t.muted + '] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + t.accent + '] italic mb-6">"' + c.quote + '"</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
  }
  await browser.close();
  console.log('Cards generated successfully');
})();
