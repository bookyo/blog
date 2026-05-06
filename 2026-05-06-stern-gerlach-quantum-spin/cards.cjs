const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-06-stern-gerlach-quantum-spin';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE RESULT',
      title: 'Two Dots,\nNot a Smear',
      dek: 'Classical physics predicted atoms would form a continuous band on the detector. Instead, Stern and Gerlach found two sharp, discrete bands — proof that nature is quantized, not continuous.',
      quote: '"They expected a smear. Nature gave them two dots."',
      bullets: ['Silver atoms in a hot furnace (1000°C)', 'Narrow slit creates collimated beam', 'Passes through inhomogeneous magnetic field', 'Two discrete spots on the detector'],
      theme: '#000D1A',
      accent: '#00B4D8'
    },
    {
      num: '02',
      eyebrow: 'THE FORMULA',
      title: 'Why Exactly\nTwo Bands?',
      dek: 'The number of output bands follows 2s + 1, where s is the spin quantum number. For spin-½ particles (s = ½), this always equals 2 — no matter which axis you measure.',
      quote: '"Electrons are not spinning tops. Yet they carry angular momentum."',
      bullets: ['Spin quantum number s = ½ for electrons', '2s + 1 = 2 output states always', 'm_s = +½ (spin up) or -½ (spin down)', 'Same result regardless of measurement axis'],
      theme: '#001A0D',
      accent: '#00FF94'
    },
    {
      num: '03',
      eyebrow: 'MODERN IMPACT',
      title: 'The Experiment\nThat Built MRI',
      dek: 'The spin-manipulation principle discovered in 1922 now underpins MRI scanners, atomic clocks, and the quantum computers being built by Google and IBM today.',
      quote: '"Otto Stern received his Nobel Prize 21 years later, in exile from Nazi Germany."',
      bullets: ['MRI machines: nuclear magnetic resonance', 'Atomic clocks: spin-state selection', 'Quantum computers: qubits as spin-½ systems', 'Hard drive read heads: spin-dependent tunneling'],
      theme: '#0D0D0D',
      accent: '#FF6B35'
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + c.theme + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + c.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.05] mb-6">' + c.title.replace(/\n/g, '<br>') + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + c.accent + '] italic mb-6">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
  }
  
  await browser.close();
  console.log('Cards saved');
})();
