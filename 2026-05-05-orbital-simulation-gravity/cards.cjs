const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-05-orbital-simulation-gravity';

const CARDS = [
  {
    slug: 'card-01',
    theme: 'forest',
    eyebrow: 'The Puzzle',
    title: 'Why Planets Don\'t Fall Into the Sun',
    dek: 'Gravity pulls inward. There\'s no friction in space. So why doesn\'t the planet spiral in?',
    quote: 'In a stable two-body system, gravity is a conservative force — it conserves mechanical energy.',
    bullets: [
      'Planet speeds up as it falls toward the Sun',
      'Slows down as it climbs away',
      'Total energy stays exactly constant'
    ]
  },
  {
    slug: 'card-02',
    theme: 'ocean',
    eyebrow: 'Kepler\'s Laws',
    title: 'T² ∝ a³ — The Equation That Revealed Gravity',
    dek: '30 years of work. One shock: orbits are ellipses, not circles.',
    quote: 'Every single ratio of T²/a³ = 1.00. That\'s not a coincidence. That\'s a law of nature.',
    bullets: [
      'Ellipses — not circles',
      'Equal areas in equal times',
      'T² proportional to a³'
    ]
  },
  {
    slug: 'card-03',
    theme: 'ember',
    eyebrow: 'Multi-body Chaos',
    title: 'Three Bodies, No Prediction',
    dek: 'The solar system is, in a precise mathematical sense, chaotic.',
    quote: 'Small perturbations accumulate. The system that looked stable turns out to be living on borrowed time.',
    bullets: [
      'Mercury has nonzero instability probability',
      'Tiny differences → completely different outcomes',
      'Only numerical simulation reveals the future'
    ]
  }
];

const THEMES = {
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' },
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
};

(async () => {
  const browser = await chromium.launch();

  for (let i = 0; i < CARDS.length; i++) {
    const card = CARDS[i];
    const theme = THEMES[card.theme];

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Outfit', sans-serif;
    background: ${theme.bg};
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 48px;
  }
  .card {
    width: 1080px;
    padding: 72px 80px;
    position: relative;
  }
  .eyebrow {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: ${theme.accent};
    margin-bottom: 20px;
  }
  .title {
    font-size: 72px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.05;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
  }
  .dek {
    font-size: 22px;
    color: #999999;
    line-height: 1.5;
    margin-bottom: 36px;
    max-width: 800px;
  }
  .quote {
    font-size: 26px;
    font-style: italic;
    color: ${theme.accent};
    line-height: 1.5;
    margin-bottom: 36px;
    padding-left: 24px;
    border-left: 3px solid ${theme.accent};
    max-width: 880px;
  }
  .bullets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .bullets li {
    font-size: 18px;
    color: #888888;
    padding-left: 20px;
    position: relative;
  }
  .bullets li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: ${theme.muted};
  }
</style>
</head>
<body>
<div class="card">
  <div class="eyebrow">${card.eyebrow}</div>
  <h1 class="title">${card.title}</h1>
  <p class="dek">${card.dek}</p>
  <blockquote class="quote">"${card.quote}"</blockquote>
  <ul class="bullets">
    ${card.bullets.map(b => `<li>${b}</li>`).join('\n    ')}
  </ul>
</div>
</body>
</html>`;

    const outputPath = path.join(articleDir, `${card.slug}.png`);
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: outputPath, fullPage: true });
    await page.close();
    console.log(`Saved: ${outputPath}`);
  }

  await browser.close();
  console.log('All cards generated.');
})();
