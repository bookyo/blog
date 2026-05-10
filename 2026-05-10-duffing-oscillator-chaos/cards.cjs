const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE CLAIM',
      title: 'Period Doubling:\nThe Road to Chaos',
      dek: 'Increase the drive amplitude in a Duffing oscillator and something remarkable happens: the period of oscillation suddenly doubles. Double it again, and it doubles again. At the third doubling, you enter chaos — aperiodic, unpredictable, sensitive to initial conditions.',
      quote: 'ÿ + δẏ + αy + βy³ = γ cos(ωt)',
      bullets: ['γ = 0.20: Period 1', 'γ = 0.27: Period 2', 'γ = 0.29: Period 4', 'γ = 0.32: Period 8', 'γ ≈ 0.37: Chaos'],
      theme: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
    },
    {
      num: '02',
      eyebrow: 'THE DETECTION METHOD',
      title: 'Poincaré Sections:\nA Strobe Light on Chaos',
      dek: 'To distinguish periodic from chaotic motion, look at the system only once per drive cycle. Periodic motion gives discrete points that repeat. Chaos gives a fractal cloud — points arranged in intricate patterns that never quite repeat, with structure at every scale.',
      quote: '"Stroboscopic sampling reveals the hidden geometry of dynamical systems."',
      bullets: ['Period 1 → 1 point', 'Period 2 → 2 points', 'Chaos → fractal attractor', 'Zoom in: lines become lines of lines', 'Fractal dimension ≈ 1.5'],
      theme: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' }
    },
    {
      num: '03',
      eyebrow: 'THE DRAMATIC CONSEQUENCE',
      title: 'The Double-Well Jump:\nEscaping the Impossible',
      dek: 'In the chaotic regime, a particle trapped in a double-well potential jumps between wells unpredictably. The wait time between jumps is not random — it is deterministically generated. But because the system is exponentially sensitive to initial conditions, you cannot predict when the next jump will occur.',
      quote: '"Two trajectories starting from nearly identical initial conditions will diverge exponentially and will not switch wells at the same time."',
      bullets: ['Two stable equilibrium points', 'Enough γ → barrier crossing', 'Wait time: deterministic but unpredictable', 'Same math in MEMS, circuits, neurons', 'Applies to Josephson junctions'],
      theme: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + c.theme.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + c.theme.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[68px] font-black text-white leading-[1.0] mb-6" style="white-space:pre-line;">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + c.theme.accent + '] italic mb-6">" ' + c.quote + ' "</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(__dirname, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  
  await browser.close();
  console.log('All cards done');
})();
