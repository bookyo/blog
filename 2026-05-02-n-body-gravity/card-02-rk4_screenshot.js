
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 900 });
  await page.setContent(`<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>card-02-rk4</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center" style="background-color: #001A0D">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Eyebrow -->
    <p class="text-[14px] font-bold tracking-[0.2em] mb-4" style="color: #00FF94">THE NUMERICAL INSIGHT</p>
    
    <!-- Title -->
    <h2 class="text-[52px] font-black leading-tight mb-6" style="color: #FFFFFF">Why Your Browser Can Simulate a Galaxy</h2>
    
    <!-- Dek -->
    <p class="text-[20px] leading-relaxed mb-8" style="color: #00CC77">RK4 integration keeps energy conservation honest where simpler methods catastrophically fail.</p>
    
    <!-- Divider -->
    <div class="h-[1px] w-full mb-8" style="background-color: #004422"></div>
    
    <!-- Bullets -->
    <ul class="space-y-1 mb-8"><li class="text-[16px] text-[#00CC77] mb-2 flex items-start"><span class="text-[#00FF94] mr-3">→</span>Euler integration: fast, but energy drifts until the system flies apart</li><li class="text-[16px] text-[#00CC77] mb-2 flex items-start"><span class="text-[#00FF94] mr-3">→</span>RK4 samples acceleration 4x per step with weighted precision</li><li class="text-[16px] text-[#00CC77] mb-2 flex items-start"><span class="text-[#00FF94] mr-3">→</span>Real-time energy tracking lets you validate accuracy visually</li></ul>
    
    <!-- Quote -->
    <blockquote class="border-l-4 pl-6 py-2" style="border-color: #00FF94">
      <p class="text-[22px] font-medium leading-relaxed" style="color: #FFFFFF">"Validated numerical accuracy is the only way to trust long-term simulations."</p>
    </blockquote>
  </div>
</body>
</html>`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-02-n-body-gravity/card-02-rk4.png', fullPage: true });
  await browser.close();
  console.log('Generated: card-02-rk4.png');
})();
