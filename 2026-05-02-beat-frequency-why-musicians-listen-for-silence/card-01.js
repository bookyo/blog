
const { chromium } = require('playwright');
const path = require('path');

// Card 1: The Formula
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; }
  .card-bg { background: #000D1A; }
  .accent { color: #00B4D8; }
  .accent-bg { background: #00B4D8; }
  .muted { color: #0090B8; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[20px] font-semibold tracking-[0.3em] accent uppercase mb-8">The Mathematics</p>
    <p class="text-[48px] font-bold text-white leading-tight mb-6">Beat Frequency Formula</p>
    <div class="inline-block bg-[#001a2e] rounded-2xl px-12 py-8 mb-8">
      <p class="text-[72px] font-bold text-[#00B4D8] font-mono tracking-tight">f_beat = |f₁ − f₂|</p>
    </div>
    <p class="text-[22px] text-[#4a7a8a] leading-relaxed">Two tones 2 Hz apart produce<br/>2 beats per second.</p>
  </div>
</body>
</html>`;
  
  await page.setContent(html);
  await page.waitForTimeout(1500);
  
  const outputPath = path.join(__dirname, 'card-01-formula.png');
  await page.screenshot({ path: outputPath, fullPage: true });
  await browser.close();
  console.log('Card 1 saved:', outputPath);
})();
