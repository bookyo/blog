
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CARDS = [
  {
    name: 'card1',
    theme: 'ocean',
    eyebrow: 'The Core Chemistry',
    title: 'HIn ⇌ H⁺ + In⁻',
    dek: 'Two molecular forms, one color equilibrium. The acidic form (HIn) and basic form (In⁻) each report the pH of their surroundings through color.',
    bullets: ['pH = pKa + log([In⁻]/[HIn])', 'At pH = pKa, exactly 50/50 blend', 'Indicator is a weak acid in equilibrium'],
    accent: '#00B4D8',
    bg: '#000D1A'
  },
  {
    name: 'card2',
    theme: 'ember',
    eyebrow: 'The Two-Unit Window',
    title: 'Color Over a Range, Not a Point',
    dek: 'Most students think indicators flip at one pH. The truth: each indicator has a ~2 pH unit transition window where you see a gradient, not a switch.',
    bullets: ['Human eye needs 10:1 ratio to see complete shift', 'Phenolphthalein: pH 8.2 to 10.0', 'Methyl Orange: pH 3.1 to 4.4'],
    accent: '#FF6B35',
    bg: '#0D0D0D'
  },
  {
    name: 'card3',
    theme: 'forest',
    eyebrow: 'Choosing the Right Indicator',
    title: 'Match the Range to the Endpoint',
    dek: 'Strong acid + strong base: equivalence at pH 7, use bromothymol blue. Weak acid + strong base: pH > 7, use phenolphthalein. Wrong match = missed endpoint.',
    bullets: ['Strong acid + strong base: pH 7 → bromothymol blue', 'Weak acid + strong base: pH > 7 → phenolphthalein', 'Strong acid + weak base: pH < 7 → methyl orange'],
    accent: '#00FF94',
    bg: '#001A0D'
  }
];

const THEMES = {
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' },
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
};

(async () => {
  const browser = await chromium.launch();
  for (const card of CARDS) {
    const t = THEMES[card.theme];
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; background: ${t.bg}; }
.accent { color: ${t.accent}; }
.bg-accent { background-color: ${t.accent}; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center p-12">
<div class="max-w-[900px] w-full">
  <p class="text-[14px] font-semibold tracking-[0.2em] uppercase accent mb-6">${card.eyebrow}</p>
  <h2 class="text-[64px] font-black text-white leading-[1.0] mb-6">${card.title}</h2>
  <p class="text-[22px] text-[#AAAAAA] leading-relaxed mb-10 max-w-[800px]">${card.dek}</p>
  <div class="space-y-3">
    ${card.bullets.map(b => `
    <div class="flex items-start gap-4">
      <div class="w-2 h-2 rounded-full bg-accent mt-2 flex-shrink-0"></div>
      <p class="text-[18px] text-[#CCCCCC] leading-snug">${b}</p>
    </div>`).join('')}
  </div>
</div>
</body>
</html>`;
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: `${card.name}.png`, fullPage: true });
    await page.close();
    console.log(`${card.name}.png saved`);
  }
  await browser.close();
})();
