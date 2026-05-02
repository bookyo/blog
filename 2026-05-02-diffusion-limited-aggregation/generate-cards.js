const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });

  const cards = [
    {
      name: 'card-01',
      eyebrow: 'HOW IT WORKS',
      title: 'The Rule Behind the Chaos',
      dek: 'Start with one particle. Launch random walkers. They drift, collide, and stick. Repeat 10,000 times.',
      quote: 'Every particle only knows its own local neighborhood — the pixel it is standing on and whether something is next to it. Yet from this entirely local, entirely blind process, a structure with global coherence appears.',
      accent: '#00FF94',
      bg: '#001A0D',
      theme: 'forest'
    },
    {
      name: 'card-02',
      eyebrow: 'THE NUMBER',
      title: 'Why 1.71 Matters',
      dek: 'Fractal dimension: more than a line, less than a plane.',
      quote: 'This number is a universality class — any physical process governed by diffusion and irreversible attachment produces structures with this same dimension, regardless of the details.',
      accent: '#00B4D8',
      bg: '#000D1A',
      theme: 'ocean'
    },
    {
      name: 'card-03',
      eyebrow: 'IN THE WILD',
      title: 'Lightning, Minerals, Deltas',
      dek: 'Five real-world systems that grow like DLA.',
      quote: 'Lightning, electrochemical deposits, mineral dendrites, blood vessel networks, and river deltas — all follow the same invisible branching blueprint.',
      accent: '#FF6B35',
      bg: '#0D0D0D',
      theme: 'ember'
    }
  ];

  for (const card of cards) {
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${card.name}</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; margin: 0; padding: 0; background: ${card.bg}; }
  .card { width: 1080px; min-height: 900px; padding: 64px 80px; box-sizing: border-box; }
  .eyebrow { font-size: 14px; font-weight: 700; letter-spacing: 3px; color: ${card.accent}; margin-bottom: 16px; }
  .title { font-size: 72px; font-weight: 900; color: white; line-height: 1.05; margin: 0 0 24px 0; }
  .dek { font-size: 28px; font-weight: 600; color: ${card.accent}; margin: 0 0 48px 0; line-height: 1.3; }
  .quote { font-size: 20px; color: #AAAAAA; line-height: 1.7; margin: 0; padding-left: 24px; border-left: 3px solid ${card.accent}; }
</style>
</head>
<body>
<div class="card">
  <div class="eyebrow">${card.eyebrow}</div>
  <h1 class="title">${card.title}</h1>
  <p class="dek">${card.dek}</p>
  <p class="quote">${card.quote}</p>
</div>
</body>
</html>`;

    await page.setContent(html);
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(__dirname, `${card.name}.png`), fullPage: true });
    console.log(`${card.name}.png saved.`);
  }

  await browser.close();
})();
