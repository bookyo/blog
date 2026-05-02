const { chromium } = require('playwright');
const path = require('path');

const cards = [
  {
    name: 'card-01-formula',
    eyebrow: 'The Core Equation',
    title: 'Three Terms, One Summation',
    dek: 'u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt',
    bullets: ['Kp — Proportional: respond to current error', 'Ki — Integral: eliminate steady-state error', 'Kd — Derivative: predict and dampen'],
    theme: 'forest'
  },
  {
    name: 'card-02-tuning',
    eyebrow: 'PID Tuning',
    title: 'Every Knob Is a Compromise',
    dek: 'You cannot simultaneously minimize rise time and overshoot',
    bullets: ['Kp governs rise time', 'Kd controls overshoot', 'Ki eliminates steady-state error but inflates settling time'],
    theme: 'ocean'
  },
  {
    name: 'card-03-why',
    eyebrow: 'Why It Endures',
    title: 'Minimalism as Engineering Philosophy',
    dek: 'Robust · Interpretable · Simple to implement',
    bullets: ['Works without an exact plant model', 'Every engineer can read it', 'Runs on the cheapest microcontroller'],
    theme: 'ember'
  }
];

const themes = {
  forest: { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77', accentText: '#001A0D' },
  ocean:  { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8', accentText: '#000D1A' },
  ember:  { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529', accentText: '#0D0D0D' }
};

async function renderCard(card, theme) {
  const t = themes[theme];
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .dek { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="bg-black flex items-center justify-center min-h-screen">
  <div style="background:${t.bg}" class="w-[1080px] px-[80px] py-20">
    <p style="color:${t.accent}" class="text-[16px] font-semibold tracking-[0.3em] uppercase mb-6">${card.eyebrow}</p>
    <h2 class="text-[72px] font-black text-white leading-none mb-6">${card.title}</h2>
    <p class="dek text-[28px] font-bold mb-10" style="color:${t.accent}">${card.dek}</p>
    <div class="space-y-3">
      ${card.bullets.map(b => `
        <div class="flex items-center gap-4">
          <span style="color:${t.accent}" class="text-[22px]">▸</span>
          <span class="text-[20px] text-[#AAAAAA] font-medium">${b}</span>
        </div>
      `).join('')}
    </div>
  </div>
</body>
</html>`;

  return html;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  
  for (const card of cards) {
    const theme = card.theme;
    const t = themes[theme];
    const html = await renderCard(card, theme);
    
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html);
    await page.waitForTimeout(2000);
    await page.screenshot({ 
      path: `/Users/quyue/www/blog/2026-05-03-pid-controller-stability/${card.name}.png`, 
      fullPage: true 
    });
    await page.close();
    console.log(`Saved ${card.name}.png`);
  }
  
  await browser.close();
  console.log('All cards done.');
})();
