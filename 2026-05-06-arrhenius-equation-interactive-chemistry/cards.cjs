const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-06-arrhenius-equation-interactive-chemistry';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE EQUATION',
      title: 'k = A · e\u207B\u1D07\u02B8\u207F\u1D1B',
      dek: 'The pre-exponential factor A is the collision frequency. The exponential term is the Boltzmann factor — the fraction of molecules with enough energy to react.',
      quote: '"Svante Arrhenius, 1889"',
      bullets: ['A = pre-exponential factor', 'Ea = activation energy (kJ/mol)', 'R = gas constant (8.314 J/mol\u00B7K)', 'T = absolute temperature (K)'],
      bg: '#0a0a1a',
      accent: '#00FF94'
    },
    {
      num: '02',
      eyebrow: 'TEMPERATURE SENSITIVITY',
      title: '2–3× Faster\nEvery 10°C',
      dek: 'Reactions double or triple their rate for every 10°C increase. High activation energy reactions are the most temperature-sensitive.',
      quote: '"The van\'t Hoff rule"',
      bullets: ['Ea = 75 kJ/mol typical organic reaction', 'Small T changes \u2192 huge rate changes', 'High Ea = steeper Arrhenius slope'],
      bg: '#0a0a1a',
      accent: '#00B4D8'
    },
    {
      num: '03',
      eyebrow: 'HOW CATALYSTS WORK',
      title: 'Lower the Hill,\nNot the Destination',
      dek: 'A catalyst provides an alternative reaction path with lower activation energy. Same products, different route — thermodynamics unchanged.',
      quote: '"10\u2076 to 10\u00B2\u00B2 times faster with enzymes"',
      bullets: ['Parallel lines in Arrhenius plot', 'Same intercept, smaller slope', 'Enzymes: ultimate biological catalysts'],
      bg: '#0a0a1a',
      accent: '#FF6B35'
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      `<style>body{font-family:"Outfit",sans-serif;background:${c.bg};}</style>` +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      `<div class="w-[1080px] px-16 py-20">` +
      `<p class="text-[13px] text-[${c.accent}] font-semibold tracking-[0.2em] mb-4">${c.eyebrow}</p>` +
      `<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">${c.title.replace(/\n/g, '<br>')}</h2>` +
      `<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">${c.dek}</p>` +
      `<p class="text-[18px] text-[${c.accent}] italic mb-6">${c.quote}</p>` +
      `<ul class="space-y-2">` +
      c.bullets.map(b => `<li class="text-[16px] text-[#d0d0e0]">• ${b}</li>`).join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  await browser.close();
  console.log('All cards done');
})();