
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-05-quantum-tunneling-physics';

const cards = [
  {
    slug: 'card-01',
    eyebrow: 'The Equation',
    title: 'T ≈ e⁻²ᵏᵃ',
    dek: 'Transmission falls exponentially with barrier width — double the width, and tunneling probability drops by e²',
    bullets: ['κ = √(2m(V₀-E)/ℏ', 'Planck constant ℏ suppresses macroscopic tunneling', 'At nanometer scales, electrons tunnel routinely'],
    theme: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
  },
  {
    slug: 'card-02',
    eyebrow: 'Nobel Prize Application',
    title: 'Scanning Tunneling Microscopy',
    dek: '1986 Nobel Physics — an STM images individual atoms using the exponential sensitivity of tunneling current to distance',
    bullets: ['Tip within few angstroms of surface', 'Current falls over 0.1 nm distance change', 'First instrument to show atoms directly'],
    theme: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' }
  },
  {
    slug: 'card-03',
    eyebrow: 'Inside Your Phone',
    title: 'Flash Memory Runs on Tunneling',
    dek: 'Every NAND flash cell writes and erases by forcing electrons through nanometer-thin oxide barriers',
    bullets: ['~10²² atoms in a phone processor', 'Flash gates only a few nanometers thick', 'Industry approaching physical scaling limits'],
    theme: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
  }
];

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const { slug, eyebrow, title, dek, bullets, theme } = card;
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; background-color: ${theme.bg}; }
.eyebrow { color: ${theme.accent}; }
.title { color: #ffffff; }
.dek { color: #aaaaaa; }
.bullet { color: ${theme.muted}; }
.accent-bar { background-color: ${theme.accent}; }
</style>
</head>
<body class="flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-16">
    <p class="eyebrow text-[18px] font-700 tracking-[0.2em] uppercase mb-6">${eyebrow}</p>
    <h1 class="title text-[100px] font-black leading-none tracking-tight mb-6">${title}</h1>
    <p class="dek text-[28px] leading-relaxed mb-10 max-w-[800px]">${dek}</p>
    <div class="accent-bar h-[3px] w-[120px] mb-8"></div>
    <ul class="space-y-3">
      ${bullets.map(b => `<li class="bullet text-[20px] font-mono">• ${b}</li>`).join('\n      ')}
    </ul>
  </div>
</body>
</html>`;

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    const outPath = path.join(articleDir, `${slug}.png`);
    await page.screenshot({ path: outPath, fullPage: true });
    await page.close();
    console.log(`Saved ${slug}.png`);
  }
  await browser.close();
  console.log('All cards done');
})();
