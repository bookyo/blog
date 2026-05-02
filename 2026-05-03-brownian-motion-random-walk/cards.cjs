const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Card 1: Einstein relation
const card1Html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card 1</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .card-bg { background: #001A0D; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20">
    <p class="text-[16px] tracking-[0.3em] text-[#00CC77] uppercase mb-6">The Einstein Relation</p>
    <h2 class="text-[72px] font-black text-white leading-[1.05] tracking-tight">⟨x²⟩ = 2Dt</h2>
    <p class="text-[22px] text-[#00CC77] mt-6 leading-relaxed">Mean squared displacement grows linearly with time —<br>this single equation explains diffusion, heat flow,<br>and why atoms must exist.</p>
    <p class="text-[14px] text-[#005522] mt-10 tracking-widest uppercase">Brownian Motion & Random Walk · ElysiaTools</p>
  </div>
</body>
</html>`;

// Card 2: √n scaling
const card2Html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card 2</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .card-bg { background: #000D1A; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20">
    <p class="text-[16px] tracking-[0.3em] text-[#0090B8] uppercase mb-6">The √n Scaling Law</p>
    <h2 class="text-[80px] font-black text-white leading-[1.0] tracking-tight">4×</h2>
    <p class="text-[28px] font-bold text-[#00B4D8] mt-6 leading-relaxed">To double how far you wander,<br>you need four times as many steps.</p>
    <p class="text-[18px] text-[#006688] mt-8 leading-relaxed">Random walks are extraordinarily slow explorers.<br>This is why smells spread slowly, pollution lingers for decades,<br>and short-term market predictions are always noisy.</p>
    <p class="text-[14px] text-[#003344] mt-10 tracking-widest uppercase">Brownian Motion & Random Walk · ElysiaTools</p>
  </div>
</body>
</html>`;

// Card 3: Central Limit Theorem
const card3Html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card 3</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .card-bg { background: #0D0D0D; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20">
    <p class="text-[16px] tracking-[0.3em] text-[#CC5529] uppercase mb-6">The Central Limit Theorem</p>
    <h2 class="text-[72px] font-black text-white leading-[1.05] tracking-tight">±1 + ±1 + ±1...</h2>
    <p class="text-[22px] text-[#FF6B35] mt-6 leading-relaxed">Start with binary coin flips. After 1,000 steps,<br>the result is a perfect Gaussian bell curve.<br>The most orderly shape in mathematics<br>emerges from pure randomness.</p>
    <p class="text-[14px] text-[#442211] mt-10 tracking-widest uppercase">Brownian Motion & Random Walk · ElysiaTools</p>
  </div>
</body>
</html>`;

// Card 4: Bachelier's forgotten work
const card4Html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card 4</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .card-bg { background: #001A0D; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20">
    <p class="text-[16px] tracking-[0.3em] text-[#00CC77] uppercase mb-6">The Mathematician History Forgot</p>
    <h2 class="text-[56px] font-black text-white leading-[1.1] tracking-tight">Louis Bachelier,<br>1900</h2>
    <p class="text-[20px] text-[#00CC77] mt-6 leading-relaxed">He modeled stock prices as a random walk — five years<br>before Einstein explained Brownian motion in physics.<br>His dissertation founded mathematical finance.<br>It received a passing grade and was forgotten for 60 years.</p>
    <p class="text-[14px] text-[#005522] mt-10 tracking-widest uppercase">Brownian Motion & Random Walk · ElysiaTools</p>
  </div>
</body>
</html>`;

const cards = [
  { name: 'card-01-einstein', html: card1Html },
  { name: 'card-02-scaling', html: card2Html },
  { name: 'card-03-clt', html: card3Html },
  { name: 'card-04-bachelier', html: card4Html },
];

(async () => {
  const browser = await chromium.launch();
  
  for (const card of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    await page.setContent(card.html);
    await page.waitForTimeout(2000);
    const outPath = path.join(__dirname, `${card.name}.png`);
    await page.screenshot({ path: outPath, fullPage: true });
    console.log(`Saved: ${card.name}.png`);
    await page.close();
  }
  
  await browser.close();
  console.log('All cards generated.');
})();
