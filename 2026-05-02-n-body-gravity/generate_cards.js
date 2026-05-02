const { chromium } = require('playwright');

const cards = [
  {
    name: 'card-01-chaos',
    theme: 'ocean',
    eyebrow: 'THE CONTRARIAN CLAIM',
    title: 'Newton Was Wrong About the Universe Being Predictable',
    dek: 'Three centuries later, mathematicians proved him right about the laws — and completely wrong about what those laws imply for prediction.',
    bullets: [
      'F = G·m₁·m₂/r² governs everything from baseballs to galaxies',
      'Poincaré proved the three-body problem is non-integrable in 1887',
      'Simple rules + three bodies = genuinely unpredictable outcomes',
    ],
    quote: 'Add one more body. Suddenly there is no general closed-form solution.',
  },
  {
    name: 'card-02-rk4',
    theme: 'forest',
    eyebrow: 'THE NUMERICAL INSIGHT',
    title: 'Why Your Browser Can Simulate a Galaxy',
    dek: 'RK4 integration keeps energy conservation honest where simpler methods catastrophically fail.',
    bullets: [
      'Euler integration: fast, but energy drifts until the system flies apart',
      'RK4 samples acceleration 4x per step with weighted precision',
      'Real-time energy tracking lets you validate accuracy visually',
    ],
    quote: 'Validated numerical accuracy is the only way to trust long-term simulations.',
  },
  {
    name: 'card-03-prediction',
    theme: 'ember',
    eyebrow: 'THE DEEPER IMPLICATION',
    title: 'Chaos Is Not Randomness — It\'s Sensitivity',
    dek: 'Deterministic systems can be unpredictable in principle, not just in practice. The universe is simultaneously deterministic and surprising.',
    bullets: [
      'Tiny differences in initial conditions compound exponentially',
      'Same laws + slightly different start = completely different outcome',
      'Climate, markets, and neural networks are all chaotic systems',
    ],
    quote: 'The equation is on one page. The consequences take centuries to fully understand.',
  },
];

const themeColors = {
  ocean:  { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8', text: '#FFFFFF', dim: '#004466' },
  forest: { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77', text: '#FFFFFF', dim: '#004422' },
  ember:  { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529', text: '#FFFFFF', dim: '#442200' },
};

async function generateCard(card) {
  const c = themeColors[card.theme];
  const bullets = card.bullets.map(b => `<li class="text-[16px] text-[${c.muted}] mb-2 flex items-start"><span class="text-[${c.accent}] mr-3">→</span>${b}</li>`).join('');
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${card.name}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center" style="background-color: ${c.bg}">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Eyebrow -->
    <p class="text-[14px] font-bold tracking-[0.2em] mb-4" style="color: ${c.accent}">${card.eyebrow}</p>
    
    <!-- Title -->
    <h2 class="text-[52px] font-black leading-tight mb-6" style="color: ${c.text}">${card.title}</h2>
    
    <!-- Dek -->
    <p class="text-[20px] leading-relaxed mb-8" style="color: ${c.muted}">${card.dek}</p>
    
    <!-- Divider -->
    <div class="h-[1px] w-full mb-8" style="background-color: ${c.dim}"></div>
    
    <!-- Bullets -->
    <ul class="space-y-1 mb-8">${bullets}</ul>
    
    <!-- Quote -->
    <blockquote class="border-l-4 pl-6 py-2" style="border-color: ${c.accent}">
      <p class="text-[22px] font-medium leading-relaxed" style="color: ${c.text}">"${card.quote}"</p>
    </blockquote>
  </div>
</body>
</html>`;

  const script = `
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 900 });
  await page.setContent(\`${html.replace(/\\/g, '\\\\')}\`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-02-n-body-gravity/${card.name}.png', fullPage: true });
  await browser.close();
  console.log('Generated: ${card.name}.png');
})();
`;

  const scriptPath = `/Users/quyue/www/blog/2026-05-02-n-body-gravity/${card.name}_screenshot.js`;
  require('fs').writeFileSync(scriptPath, script);
  
  const { execSync } = require('child_process');
  try {
    execSync('/Users/quyue/.nvm/versions/node/v24.13.0/bin/node ' + scriptPath, {
      env: { ...process.env, NODE_PATH: '/Users/quyue/.hermes/hermes-agent/node_modules' },
      timeout: 30000,
    });
    console.log('  -> Done:', card.name);
  } catch(e) {
    console.error('  -> Error:', e.message);
  }
}

(async () => {
  for (const card of cards) {
    await generateCard(card);
  }
  console.log('\nAll cards generated.');
})();
