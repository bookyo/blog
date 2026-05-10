const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const articleDir = '/Users/quyue/www/blog/2026-05-10-double-slit-quantum-trajectory';

// Card specs
const cards = [
  {
    slug: 'card-01-measurement-creation',
    html: 'card-01-measurement-creation.html',
    eyebrow: 'Core Insight',
    label: 'Key Paragraph',
    title: 'Observation\nCreates Reality',
    quote: '"The detector changed what kind of question you were allowed to ask."',
    bullets: [
      'Detector OFF: interference pattern emerges from both paths',
      'Detector ON: two classical clusters, no interference',
      'Same electrons, same slits — only knowledge changed'
    ],
    bg: '#000D1A',
    accent: '#00B4D8'
  },
  {
    slug: 'card-02-de-broglie',
    html: 'card-02-de-broglie.html',
    eyebrow: 'The Formula',
    label: 'Quantum Math',
    title: 'λ = h / p',
    quote: '"For electrons at 100V, de Broglie wavelength ≈ 0.12 nm."',
    bullets: [
      'h = 6.626 × 10⁻³⁴ J·s (Planck constant)',
      'Larger wavelength → wider interference fringes',
      'Electron microscopes: wavelength enables resolution'
    ],
    bg: '#0D0D0D',
    accent: '#FF6B35'
  },
  {
    slug: 'card-03-interpretation',
    html: 'card-03-interpretation.html',
    eyebrow: 'Interpretation',
    label: 'Beyond the Physics',
    title: 'Bohmian vs\nCopenhagen',
    quote: '"Both interpretations make identical predictions — they differ on what reality is."',
    bullets: [
      'Bohmian: particles have definite paths guided by wave function',
      'Copenhagen: "which path?" is meaningless until measured',
      'The visualization shows Bohmian trajectories'
    ],
    bg: '#001A0D',
    accent: '#00FF94'
  }
];

function buildCardHTML(card) {
  const bulletsHTML = card.bullets.map(b =>
    `<div class="bullet"><div class="bullet-dot"></div><span>${b}</span></div>`
  ).join('\n');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: ${card.bg};
  font-family: 'Outfit', sans-serif;
  width: 1080px;
  min-height: 900px;
  padding: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: ${card.accent};
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 16px;
}
.label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #555;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.title {
  font-size: 88px;
  font-weight: 900;
  color: ${card.accent};
  line-height: 0.92;
  letter-spacing: -2px;
  margin-bottom: 32px;
}
.quote {
  font-size: 20px;
  color: #ccc;
  line-height: 1.5;
  border-left: 3px solid ${card.accent};
  padding-left: 24px;
  margin-bottom: 36px;
}
.bullets {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.bullet {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 17px;
  color: #ddd;
}
.bullet-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${card.accent};
  flex-shrink: 0;
}
</style>
</head>
<body>
<div>
  <div class="eyebrow">${card.eyebrow}</div>
  <div class="label">${card.label}</div>
  <h1 class="title">${card.title.replace('\n', '<br>')}</h1>
  <p class="quote">${card.quote}</p>
  <div class="bullets">
${bulletsHTML.split('\n').map(l => '    ' + l).join('\n')}
  </div>
</div>
</body>
</html>`;
}

(async () => {
  const browser = await chromium.launch();

  for (const card of cards) {
    const htmlPath = path.join(articleDir, card.html);
    fs.writeFileSync(htmlPath, buildCardHTML(card));

    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(fs.readFileSync(htmlPath, 'utf8'), { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    const screenshotPath = path.join(articleDir, `${card.slug}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    await page.close();
    console.log(`Screenshot saved: ${screenshotPath}`);

    // Clean up HTML
    fs.unlinkSync(htmlPath);
  }

  await browser.close();
  console.log('All cards done');
})();
