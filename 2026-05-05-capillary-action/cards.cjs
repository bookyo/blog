const CARDS = [
  {
    slug: 'meniscus',
    theme: 'forest',
    eyebrow: 'The Core Mechanism',
    title: 'Surface Tension Is the Engine',
    dek: 'The curved water surface creates an upward component of force along the tube circumference',
    quote: 'The meniscus is not just an interface. It\'s a mechanical structure — a membrane trying to minimize its area while the tube wall pulls it upward.',
    bullets: [
      'Water molecules at the surface have fewer neighbors, creating asymmetric bonds',
      'Surface tension acts along the circumference, with upward component when θ < 90°',
      'Smaller radius → larger upward component relative to liquid weight'
    ]
  },
  {
    slug: 'jurin',
    theme: 'ocean',
    eyebrow: 'Jurin\'s Law · 1718',
    title: 'h = 2γ·cos(θ) / (ρ·g·r)',
    dek: 'Rise height is inversely proportional to tube radius — halve the radius, double the height',
    quote: 'James Jurin formulated the relationship in 1718. The equation balances three forces: surface tension upward, gravity downward, and contact angle determining the wetting geometry.',
    bullets: [
      'γ (surface tension) pulls upward along meniscus circumference',
      'Gravity (ρ·g·r) pulls the liquid column downward',
      'θ (contact angle) determines whether liquid rises or falls'
    ]
  },
  {
    slug: 'applications',
    theme: 'ember',
    eyebrow: 'Real-World Impact',
    title: 'From Plant Xylem to Pregnancy Tests',
    dek: 'The same physics that raises water 3 cm in a lab tube moves water 100 meters up a redwood',
    quote: 'No pump circulates water in a redwood tree. Capillary tension — transmitted through the continuous water column from roots to crown — does the job.',
    bullets: [
      'Xylem vessels: 10–100 μm diameter, water rises via evaporation-induced tension',
      'Lateral flow diagnostics: capillary wicking moves fluid without external power',
      'Microfluidics: engineered capillary flow enables complete blood analysis without pumps'
    ]
  }
];

const THEMES = {
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77', text: '#FFFFFF', dim: '#006633' },
  ocean:  { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8', text: '#FFFFFF', dim: '#005577' },
  ember:  { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529', text: '#FFFFFF', dim: '#662211' }
};

const fs = require('fs');

CARDS.forEach((card, i) => {
  const t = THEMES[card.theme];
  const n = String(i + 1).padStart(2, '0');
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card ${n}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
</style>
</head>
<body class="bg-[${t.bg}] min-h-screen flex items-center justify-center">
  <div class="w-[1080px] px-[80px] py-[60px]">
    <p class="text-[14px] tracking-[0.3em] uppercase text-[${t.muted}] mb-6">${card.eyebrow}</p>
    <h2 class="text-[72px] font-black text-[${t.text}] leading-[1.0] tracking-tight mb-4">${card.title}</h2>
    <p class="text-[22px] text-[${t.accent}] font-semibold mb-8 leading-tight">${card.dek}</p>
    <blockquote class="border-l-4 border-[${t.accent}] pl-6 mb-8">
      <p class="text-[18px] text-[#AAAAAA] italic leading-relaxed">"${card.quote}"</p>
    </blockquote>
    <ul class="space-y-3">
      ${card.bullets.map(b => `
      <li class="flex items-start gap-4">
        <span class="text-[${t.accent}] text-[20px] mt-[-2px]">›</span>
        <span class="text-[16px] text-[#CCCCCC] leading-relaxed">${b}</span>
      </li>`).join('')}
    </ul>
  </div>
</body>
</html>`;
  
  fs.writeFileSync(`card-${n}.html`, html);
  console.log(`Created card-${n}.html`);
});
