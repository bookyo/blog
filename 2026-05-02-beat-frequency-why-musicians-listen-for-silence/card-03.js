
const { chromium } = require('playwright');
const path = require('path');

// Card 3: The Threshold
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
  .card-bg { background: #001A0D; }
  .accent { color: #00FF94; }
  .accent-bg { background: #00FF94; }
  .muted { color: #00CC77; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[20px] font-semibold tracking-[0.3em] accent uppercase mb-8">The Threshold</p>
    <p class="text-[44px] font-bold text-white leading-tight mb-8">Where Beats Become a New Sound</p>
    <div class="flex justify-center gap-8 mb-8">
      <div class="text-center">
        <p class="text-[56px] font-black text-[#00FF94]">15 Hz</p>
        <p class="text-[16px] text-[#446655] mt-2">Individual beats<br/>still audible</p>
      </div>
      <div class="text-center flex items-center">
        <div class="w-1 h-20 bg-[#333333]"></div>
      </div>
      <div class="text-center">
        <p class="text-[56px] font-black text-[#666666]">20+ Hz</p>
        <p class="text-[16px] text-[#446655] mt-2">Phantom tone<br/>emerges</p>
      </div>
    </div>
    <p class="text-[18px] text-[#446655] leading-relaxed">Above ~20 Hz, your ear stops counting beats<br/>and starts hearing a new, lower pitch.</p>
  </div>
</body>
</html>`;
  
  await page.setContent(html);
  await page.waitForTimeout(1500);
  
  const outputPath = path.join(__dirname, 'card-03-threshold.png');
  await page.screenshot({ path: outputPath, fullPage: true });
  await browser.close();
  console.log('Card 3 saved:', outputPath);
})();
