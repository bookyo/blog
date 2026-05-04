const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = process.cwd();

// Theme: ocean (blue)
const theme = {
  accent: '#00B4D8',
  bg: '#000D1A',
  muted: '#0090B8',
  light: '#FFFFFF'
};

const cards = [
  {
    name: 'card-01',
    eyebrow: 'THE CORE INSIGHT',
    title: 'You Never Actually Touch Anything',
    dek: 'The electrons on your fingertip repel the electrons on every surface. What you feel as "solid" is electromagnetic repulsion — an invisible force, not a physical contact.',
    quote: 'The reason solid things feel solid is invisible. It is a force you cannot see, only feel.',
    bullets: [
      'Electrons repel electrons',
      'No atoms ever truly meet',
      'Touch is electromagnetic force',
      'Solidity is an illusion'
    ]
  },
  {
    name: 'card-02',
    eyebrow: 'THE GOLDEN RULE',
    title: 'Field Lines Never Cross',
    dek: 'This single constraint produces the most elegant diagrams in physics. Where field lines cross, the field would have two directions at once — which is mathematically impossible.',
    quote: 'At any point in space, the electric field has exactly one direction.',
    bullets: [
      'Non-crossing → elegance',
      'Lines diverge from + charge',
      'Lines converge at − charge',
      'Density = field strength'
    ]
  },
  {
    name: 'card-03',
    eyebrow: 'THE UNIVERSAL PATTERN',
    title: 'The Dipole Is Everywhere',
    dek: 'Water molecules, radio antennas, chemical bonds, your heartbeat — all are dipoles. One positive, one negative, and the field lines between them shape the modern world.',
    quote: 'A water molecule is a dipole. Without water\'s dipole character, life as we know it would be impossible.',
    bullets: [
      'H₂O: partial + and − charges',
      'Dissolves NaCl via attraction',
      'Enables hydrogen bonding',
      'Foundation of biochemistry'
    ]
  }
];

(async () => {
  const browser = await chromium.launch();
  for (let i = 0; i < cards.length; i++) {
    const c = cards[i];
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${c.name}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .bullet-item::before { content: '→'; margin-right: 8px; color: ${theme.accent}; }
</style>
</head>
<body class="bg-[${theme.bg}] flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20">
    <p class="text-[13px] font-bold tracking-[0.35em] uppercase mb-6" style="color: ${theme.accent}">${c.eyebrow}</p>
    <h2 class="text-[72px] font-black leading-[0.95] mb-6" style="color: ${theme.light}">${c.title}</h2>
    <p class="text-[22px] leading-relaxed mb-8" style="color: ${theme.muted}">${c.dek}</p>
    <blockquote class="border-l-4 pl-6 mb-10 py-2" style="border-color: ${theme.accent}">
      <p class="text-[20px] italic leading-relaxed" style="color: ${theme.light}">"${c.quote}"</p>
    </blockquote>
    <div class="space-y-2">
      ${c.bullets.map(b => `<p class="text-[16px] bullet-item" style="color: ${theme.muted}">${b}</p>`).join('\n      ')}
    </div>
  </div>
</body>
</html>`;

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: `${c.name}.png`, fullPage: true });
    await page.close();
  }
  await browser.close();
})();
