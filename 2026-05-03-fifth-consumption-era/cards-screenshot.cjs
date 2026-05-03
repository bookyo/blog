
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const workDir = '/Users/quyue/www/blog/2026-05-03-fifth-consumption-era';

// Card data - 3 highlight cards
const cards = [
  {
    slug: 'card-01',
    eyebrow: 'THE CONSUMPTION SHIFT',
    title: 'From Three Sacred Treasures to Meditation Apps',
    dek: 'The Japanese family of 1975 measured wealth in appliances. The family of 2025 measures it in air quality and community belonging.',
    quote: null,
    bullets: ['TV + fridge + washing machine → mindfulness + social connection', 'Five distinct consumption eras tracked since 1912', 'Fifth era (2021–2043): From having to being'],
    theme: 'ocean'
  },
  {
    slug: 'card-02',
    eyebrow: 'THE DEMOGRAPHIC FACT',
    title: '52% of Households Will Be Single-Person by 2040',
    dek: 'The population structure driving fifth-era consumption is not a prediction — it is already embedded in the birthrate and household data of every wealthy nation.',
    quote: null,
    bullets: ['Single households: 23% (1990) → 52% (2040)', 'Population over 65: 12% (1990) → 39% (2040)', 'Birthrate: 1.54 (1990) → 1.15 (2040)'],
    theme: 'ocean'
  },
  {
    slug: 'card-03',
    eyebrow: 'THE BUSINESS IMPERATIVE',
    title: 'The Question Is No Longer What People Want to Own',
    dek: 'Emotional architecture — the design of experiences that create well-being — is replacing brand engineering as the core competitive advantage.',
    quote: 'Why own a drill when you need a hole?',
    bullets: ['Wellness economy: $5.6 trillion annually', 'Product-as-a-service models are fifth-era adaptations', 'Sustainability is baseline, not premium'],
    theme: 'ember'
  }
];

const themeColors = {
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8', text: '#FFFFFF' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529', text: '#FFFFFF' },
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77', text: '#FFFFFF' }
};

(async () => {
  const browser = await chromium.launch();
  
  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const colors = themeColors[card.theme];
    
    const bulletsHtml = card.bullets.map(b => `<li style="color:${colors.text};font-size:22px;line-height:1.6;margin-bottom:12px;">${b}</li>`).join('');
    const quoteHtml = card.quote 
      ? `<blockquote style="border-left:4px solid ${colors.accent};padding-left:20px;margin:24px 0;font-size:28px;font-weight:700;color:${colors.accent};font-style:italic;">${card.quote}</blockquote>`
      : '';
    
    const cardHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>body { font-family: 'Outfit', sans-serif; }</style>
</head>
<body style="background-color:${colors.bg};min-height:100vh;display:flex;align-items:center;justify-content:center;">
  <div style="width:1080px;padding:60px 80px;">
    <p style="color:${colors.accent};font-size:16px;font-weight:700;letter-spacing:3px;margin-bottom:16px;text-transform:uppercase;">${card.eyebrow}</p>
    <h2 style="color:${colors.text};font-size:56px;font-weight:900;line-height:1.1;margin-bottom:20px;">${card.title}</h2>
    <p style="color:${colors.text};font-size:24px;line-height:1.5;margin-bottom:28px;opacity:0.85;">${card.dek}</p>
    ${quoteHtml}
    <ul style="list-style:none;padding:0;margin:0;">${bulletsHtml}</ul>
  </div>
</body>
</html>`;
    
    const cardPath = path.join(workDir, `${card.slug}.html`);
    fs.writeFileSync(cardPath, cardHtml);
    
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(cardHtml, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(workDir, `${card.slug}.png`), fullPage: true });
    await page.close();
    
    console.log(`Card ${i+1} saved: ${card.slug}.png`);
  }
  
  await browser.close();
  console.log('All cards done.');
})();
