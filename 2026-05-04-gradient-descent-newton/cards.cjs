const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const workDir = process.cwd();

const cards = [
  {
    name: 'card-01',
    theme: 'forest',
    eyebrow: 'Optimization Theory',
    title: 'O(n²) vs O(n)',
    dek: 'Newton method needs full Hessian matrix inversion',
    quote: '"Newton\'s method uses second-order information — the Hessian matrix — to predict the shape of the valley before it gets there."',
    bullets: ['Hessian: O(n²) space', 'Matrix inversion: O(n³)', 'Gradient descent: O(n) per step']
  },
  {
    name: 'card-02',
    theme: 'ocean',
    eyebrow: 'ML Trade-off',
    title: 'Why GD Won',
    dek: 'The math doesn\'t work at scale',
    quote: '"A model with 1 million parameters has a Hessian with 1 trillion entries."',
    bullets: ['LLMs: 100B+ params', 'Hessian: 10²⁰ entries', 'Gradient descent scales linearly']
  },
  {
    name: 'card-03',
    theme: 'ember',
    eyebrow: 'The Takeaway',
    title: 'The Valley Is Out There',
    dek: 'Different tools for different scales',
    quote: '"Gradient descent just walks there one step at a time. Newton\'s method flies — when it can afford the fuel."',
    bullets: ['Small models: try L-BFGS', 'Control theory: Newton still wins', 'Visualize the trade-off online']
  }
];

const themes = {
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' },
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' }
};

(async () => {
  const browser = await chromium.launch();
  for (const card of cards) {
    const t = themes[card.theme];
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Outfit', sans-serif; background: ${t.bg}; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
  .card { width: 1080px; padding: 80px; }
  .eyebrow { font-size: 14px; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; color: ${t.accent}; margin-bottom: 24px; }
  .title { font-size: 96px; font-weight: 900; color: white; line-height: 0.95; margin-bottom: 20px; }
  .dek { font-size: 22px; color: ${t.muted}; font-weight: 400; margin-bottom: 40px; line-height: 1.4; }
  .quote { font-size: 20px; color: white; font-style: italic; line-height: 1.6; border-left: 4px solid ${t.accent}; padding-left: 24px; margin-bottom: 40px; }
  .bullets { list-style: none; }
  .bullets li { font-size: 18px; color: ${t.muted}; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
  .bullets li:last-child { border-bottom: none; }
</style>
</head>
<body>
<div class="card">
  <div class="eyebrow">${card.eyebrow}</div>
  <div class="title">${card.title}</div>
  <div class="dek">${card.dek}</div>
  <div class="quote">${card.quote}</div>
  <ul class="bullets">${card.bullets.map(b => `<li>${b}</li>`).join('')}</ul>
</div>
</body>
</html>`;

    const cardPath = path.join(workDir, `${card.name}.html`);
    fs.writeFileSync(cardPath, html);

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(workDir, `${card.name}.png`), fullPage: true });
    await page.close();
    fs.unlinkSync(cardPath);
    console.log(`Created ${card.name}.png`);
  }
  await browser.close();
})();
