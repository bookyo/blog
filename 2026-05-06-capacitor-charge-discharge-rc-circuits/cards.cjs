const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-06-capacitor-charge-discharge-rc-circuits';

(async () => {
  const browser = await chromium.launch();
  const cards = [
    {
      num: '01',
      eyebrow: 'KEY INSIGHT',
      title: 'τ = RC: The One Number That Predicts Everything',
      dek: 'At t = τ, a capacitor reaches 63.2% of full charge. At t = 5τ, it\'s at 99.3%. This isn\'t an approximation — it\'s pure exponential math.',
      quote: '"The time constant τ = RC is the heartbeat of every RC circuit."',
      bullets: ['τ = R × C (resistance × capacitance)', '63.2% charge at one time constant', '5τ = 99.3% (engineers treat as complete)'],
      theme: 'forest'
    },
    {
      num: '02',
      eyebrow: 'COUNTERINTUITIVE',
      title: 'Why Current Is Maximum When the Capacitor Is Empty',
      dek: 'The moment you connect a capacitor to a voltage source, current peaks — because an empty capacitor acts like a short circuit. As it fills, current decreases until it stops entirely.',
      quote: '"The capacitor starts as a short and ends as an open circuit."',
      bullets: ['Initial current = V₀/R (maximum)', 'Current decreases as voltage builds', 'At full charge, current = 0'],
      theme: 'ocean'
    },
    {
      num: '03',
      eyebrow: 'REAL WORLD',
      title: 'Where RC Circuits Show Up in Daily Life',
      dek: 'Your phone\'s battery management, a camera flash, a defibrillator, your touchscreen — all rely on the same exponential RC dynamics.',
      quote: '"A defibrillator capacitor delivers energy in a single pulse, instantly."',
      bullets: ['Smartphone charging circuits', 'Camera flash (instantaneous energy release)', 'Touchscreen capacitance sensors'],
      theme: 'ember'
    }
  ];

  const themes = {
    forest: { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77' },
    ocean: { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8' },
    ember: { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529' }
  };

  for (const c of cards) {
    const t = themes[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + t.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + t.accent + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + t.accent + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
  }
  await browser.close();
  console.log('Cards generated');
})();
