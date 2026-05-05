const { chromium } = require('playwright');
const path = require('path');

const cards = [
  {
    slug: 'logistic-map-formula',
    eyebrow: 'The Equation',
    title: 'Three Variables. One Multiplication. Infinite Surprises.',
    dek: 'The logistic map: x_{n+1} = r · x_n · (1 − x_n)',
    quote: 'Three variables. One multiplication. No excuse for complexity. Yet this equation produces period-doubling bifurcations, chaos windows threaded with sudden islands of order, and a universal constant.',
    bullets: ['Robert May, 1976', 'Population dynamics model', 'Chaos from deterministic rules'],
    theme: 'forest',
    output: '/Users/quyue/www/blog/2026-05-02-logistic-map/card-01-formula.png'
  },
  {
    slug: 'bifurcation-cascade',
    eyebrow: 'The Pattern',
    title: 'One River That Keeps Branching Until It Disappears',
    dek: 'How simple rules produce the bifurcation diagram',
    quote: 'At r = 3, something shifts. The fixed point loses its grip. Instead of settling, the population oscillates between two values. Push r higher and the two lines split again. Then again. Until the lines blur into chaos.',
    bullets: ['r < 1: Extinction', '1 ≤ r < 3: Stable point', 'r ≥ 3: Period doubling → Chaos'],
    theme: 'ocean',
    output: '/Users/quyue/www/blog/2026-05-02-logistic-map/card-02-bifurcation.png'
  },
  {
    slug: 'feigenbaum-constant',
    eyebrow: 'The Discovery',
    title: 'δ ≈ 4.669 — A Number That Connects Everything',
    dek: 'The universal Feigenbaum constant',
    quote: 'The same ratio — δ ≈ 4.669201609 — governs the approach to chaos in electronic circuits, fluid jets, cardiac oscillations, and the logistic map. This is universality: the same mathematics in fundamentally different physical systems.',
    bullets: ['Mitchell Feigenbaum, 1978', 'Universal constant δ ≈ 4.669', 'Appears across physics, biology, engineering'],
    theme: 'ember',
    output: '/Users/quyue/www/blog/2026-05-02-logistic-map/card-03-feigenbaum.png'
  },
  {
    slug: 'chaos-with-windows',
    eyebrow: 'The Paradox',
    title: 'Chaos Contains Islands of Order',
    dek: 'Li-Yorke chaos and the period-3 window',
    quote: 'Mathematician Jim Yorke proved: the existence of a period-3 orbit in a deterministic system implies chaotic dynamics. The period-3 window is not a break from chaos — it is a symptom of it.',
    bullets: ['Li-Yorke theorem (1975)', 'Period-3 window at r ≈ 3.83', 'Chaos and order are not opposites'],
    theme: 'forest',
    output: '/Users/quyue/www/blog/2026-05-02-logistic-map/card-04-chaos.png'
  }
];

const themeColors = {
  forest: { accent: '#00FF94', bg: '#001A0D', text: '#FFFFFF', muted: '#00CC77' },
  ocean:  { accent: '#00B4D8', bg: '#000D1A', text: '#FFFFFF', muted: '#0090B8' },
  ember:  { accent: '#FF6B35', bg: '#0D0D0D', text: '#FFFFFF', muted: '#CC5529' }
};

function buildCardHTML(card) {
  const c = themeColors[card.theme];
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${card.title}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; margin: 0; background: ${c.bg}; }
  .accent { color: ${c.accent}; }
  .card-bg { background: ${c.bg}; }
  .mono { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Eyebrow -->
    <p class="text-[16px] font-semibold tracking-[0.2em] uppercase accent mb-6">${card.eyebrow}</p>
    
    <!-- Title -->
    <h1 class="text-[64px] font-black text-[${c.text}] leading-[1.05] tracking-tight">${card.title}</h1>
    
    <!-- Dek -->
    <p class="text-[22px] text-[${c.muted}] mt-6 leading-relaxed">${card.dek}</p>
    
    <!-- Quote -->
    <blockquote class="border-l-4 pl-6 mt-8" style="border-color: ${c.accent}">
      <p class="text-[20px] text-[${c.text}] leading-relaxed italic">"${card.quote}"</p>
    </blockquote>
    
    <!-- Bullets -->
    <div class="mt-8 space-y-3">
      ${card.bullets.map(b => `
      <div class="flex items-center gap-3">
        <span style="color: ${c.accent}">◆</span>
        <span class="text-[18px] text-[${c.muted}]">${b}</span>
      </div>`).join('')}
    </div>
  </div>
</body>
</html>`;
}

(async () => {
  const browser = await chromium.launch();
  
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    
    const html = buildCardHTML(card);
    await page.setContent(html);
    await page.waitForTimeout(2000);
    
    await page.screenshot({ path: card.output, fullPage: true });
    console.log(`Card ${i+1} saved: ${card.output}`);
    await page.close();
  }
  
  await browser.close();
  console.log('All cards done!');
})();
