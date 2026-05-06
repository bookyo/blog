const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-07-entropy-second-law';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'KEY INSIGHT',
      title: 'Entropy Is About Probability, Not Mischief',
      dek: 'A broken glass doesn\'t "want" to be broken. It simply has more possible arrangements when the pieces are scattered than when they\'re together.',
      quote: '— Given enough time, any system will tend toward its most probable state.',
      bullets: ['S = k·ln(Ω) — Boltzmann entropy formula', 'Ω = number of possible microstates', 'More microstates = higher entropy = more probable'],
      theme: '#00FF94',
      bg: '#001A0D'
    },
    {
      num: '02',
      eyebrow: 'PHYSICS PRINCIPLE',
      title: "Landauer's Principle",
      dek: 'Erasing one bit of information dissipates kT·ln(2) joules of energy as heat. Information is physical, and erasing it always costs entropy.',
      quote: '"The demon\'s memory fills up. Eventually, it must erase what it knows — and that erasure releases enough heat to compensate."',
      bullets: ['Bit erasure = thermodynamic heat', 'Maxwell\'s demon paradox resolved', 'Information has an unavoidable entropy cost'],
      theme: '#00B4D8',
      bg: '#000D1A'
    },
    {
      num: '03',
      eyebrow: 'TIME & MEMORY',
      title: "We Don't Experience Time Flowing",
      dek: 'We experience entropy increasing. The asymmetry of information is what we call the passage of time. Memory formation itself increases entropy.',
      quote: '"Yesterday\'s state is correlated with today\'s in a way tomorrow\'s isn\'t."',
      bullets: ['Time-symmetric physics, but time- asymmetric entropy', 'Memory formation increases entropy', 'The arrow of time emerges from the Second Law'],
      theme: '#FF6B35',
      bg: '#0D0D0D'
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + c.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + c.theme + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + c.theme + ';">' + c.quote + '</p>' +
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
