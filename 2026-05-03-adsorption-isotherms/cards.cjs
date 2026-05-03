const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const workDir = path.join(process.env.HOME || '/Users/quyue', 'www/blog/2026-05-03-adsorption-isotherms');

// Card data
const cards = [
  {
    name: 'card-01',
    eyebrow: 'Langmuir Isotherm',
    title: 'q = qmax × (KL × C) / (1 + KL × C)',
    dek: 'From four assumptions to three parameters — how a 1918 equation still governs modern carbon capture design',
    quote: 'Every adsorption site is identical, each site holds exactly one molecule, no interaction between neighbors, dynamic equilibrium.',
    bullets: ['qmax = monolayer capacity', 'KL = binding affinity', 'C = concentration']
  },
  {
    name: 'card-02',
    eyebrow: 'IUPAC Classification',
    title: 'Six Types, Six Pore Structures',
    dek: 'The shape of an isotherm reveals whether your material has micropores, mesopores, or slit-shaped channels — without a microscope',
    quote: 'Type IV hysteresis is the signature of mesoporous materials where capillary condensation occurs.',
    bullets: ['Type I: microporous fill', 'Type IV: hysteresis loops', 'H2: ink-bottle pores']
  },
  {
    name: 'card-03',
    eyebrow: 'BET Surface Area',
    title: '1 Gram = 3 Football Fields',
    dek: 'Activated carbon surface areas of 500–1500 m²/g, measured using nitrogen at 77 K — the standard of modern materials science',
    quote: 'One gram of activated carbon has the internal surface area of roughly three football fields.',
    bullets: ['77 K N₂ adsorption', '0.162 nm² molecular cross-section', '1000–2000 m²/g typical']
  },
  {
    name: 'card-04',
    eyebrow: 'Carbon Capture',
    title: 'The Equation Running on Climate',
    dek: 'Solid sorbents in direct air capture facilities worldwide are selected, optimized, and deployed using these same equations from 1909–1938',
    quote: 'There is no carbon capture optimization that doesn\'t start with understanding whether your material follows Langmuir, Freundlich, or BET.',
    bullets: ['Flue gas: 15% CO₂, 85% N₂', 'Selectivity determines efficiency', 'Regeneration energy = operating cost']
  }
];

const theme = {
  accent: '#00B4D8',
  bg: '#000D1A',
  accentMuted: '#0090B8',
  textMuted: '#4a7a8a'
};

(async () => {
  const browser = await chromium.launch();

  for (const card of cards) {
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .mono { font-family: 'Courier New', monospace; }
</style>
</head>
<body class="bg-[${theme.bg}] flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Top: eyebrow -->
    <p class="text-[16px] text-[${theme.accent}] font-semibold tracking-[0.2em] uppercase mb-4">${card.eyebrow}</p>

    <!-- Title: large, bold -->
    <h1 class="text-[56px] font-black text-white leading-tight tracking-tight">${card.title}</h1>

    <!-- Dek -->
    <p class="text-[22px] text-[${theme.textMuted}] mt-6 leading-relaxed">${card.dek}</p>

    <!-- Quote block -->
    <blockquote class="mt-8 border-l-4 border-[${theme.accent}] pl-6 py-2">
      <p class="text-[20px] text-white italic leading-relaxed">"${card.quote}"</p>
    </blockquote>

    <!-- Bullets -->
    <ul class="mt-8 space-y-3">
      ${card.bullets.map(b => `
      <li class="flex items-center gap-4">
        <span class="text-[${theme.accent}] text-[20px]">›</span>
        <span class="text-[18px] text-[#a0c0d0]">${b}</span>
      </li>`).join('')}
    </ul>
  </div>
</body>
</html>`;

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const outPath = path.join(workDir, `${card.name}.png`);
    await page.screenshot({ path: outPath, fullPage: true });
    console.log(`Saved: ${card.name}.png`);

    await page.close();
  }

  await browser.close();
})();
