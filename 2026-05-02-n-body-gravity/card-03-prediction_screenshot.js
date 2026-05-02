
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
<title>card-03-prediction</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center" style="background-color: #0D0D0D">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Eyebrow -->
    <p class="text-[14px] font-bold tracking-[0.2em] mb-4" style="color: #FF6B35">THE DEEPER IMPLICATION</p>
    
    <!-- Title -->
    <h2 class="text-[52px] font-black leading-tight mb-6" style="color: #FFFFFF">Chaos Is Not Randomness — It's Sensitivity</h2>
    
    <!-- Dek -->
    <p class="text-[20px] leading-relaxed mb-8" style="color: #CC5529">Deterministic systems can be unpredictable in principle, not just in practice. The universe is simultaneously deterministic and surprising.</p>
    
    <!-- Divider -->
    <div class="h-[1px] w-full mb-8" style="background-color: #442200"></div>
    
    <!-- Bullets -->
    <ul class="space-y-1 mb-8"><li class="text-[16px] text-[#CC5529] mb-2 flex items-start"><span class="text-[#FF6B35] mr-3">→</span>Tiny differences in initial conditions compound exponentially</li><li class="text-[16px] text-[#CC5529] mb-2 flex items-start"><span class="text-[#FF6B35] mr-3">→</span>Same laws + slightly different start = completely different outcome</li><li class="text-[16px] text-[#CC5529] mb-2 flex items-start"><span class="text-[#FF6B35] mr-3">→</span>Climate, markets, and neural networks are all chaotic systems</li></ul>
    
    <!-- Quote -->
    <blockquote class="border-l-4 pl-6 py-2" style="border-color: #FF6B35">
      <p class="text-[22px] font-medium leading-relaxed" style="color: #FFFFFF">"The equation is on one page. The consequences take centuries to fully understand."</p>
    </blockquote>
  </div>
</body>
</html>`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-02-n-body-gravity/card-03-prediction.png', fullPage: true });
  await browser.close();
  console.log('Generated: card-03-prediction.png');
})();
