
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
<title>card-01-chaos</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center" style="background-color: #000D1A">
  <div class="w-[1080px] px-[80px] py-16">
    <!-- Eyebrow -->
    <p class="text-[14px] font-bold tracking-[0.2em] mb-4" style="color: #00B4D8">THE CONTRARIAN CLAIM</p>
    
    <!-- Title -->
    <h2 class="text-[52px] font-black leading-tight mb-6" style="color: #FFFFFF">Newton Was Wrong About the Universe Being Predictable</h2>
    
    <!-- Dek -->
    <p class="text-[20px] leading-relaxed mb-8" style="color: #0090B8">Three centuries later, mathematicians proved him right about the laws — and completely wrong about what those laws imply for prediction.</p>
    
    <!-- Divider -->
    <div class="h-[1px] w-full mb-8" style="background-color: #004466"></div>
    
    <!-- Bullets -->
    <ul class="space-y-1 mb-8"><li class="text-[16px] text-[#0090B8] mb-2 flex items-start"><span class="text-[#00B4D8] mr-3">→</span>F = G·m₁·m₂/r² governs everything from baseballs to galaxies</li><li class="text-[16px] text-[#0090B8] mb-2 flex items-start"><span class="text-[#00B4D8] mr-3">→</span>Poincaré proved the three-body problem is non-integrable in 1887</li><li class="text-[16px] text-[#0090B8] mb-2 flex items-start"><span class="text-[#00B4D8] mr-3">→</span>Simple rules + three bodies = genuinely unpredictable outcomes</li></ul>
    
    <!-- Quote -->
    <blockquote class="border-l-4 pl-6 py-2" style="border-color: #00B4D8">
      <p class="text-[22px] font-medium leading-relaxed" style="color: #FFFFFF">"Add one more body. Suddenly there is no general closed-form solution."</p>
    </blockquote>
  </div>
</body>
</html>`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-05-02-n-body-gravity/card-01-chaos.png', fullPage: true });
  await browser.close();
  console.log('Generated: card-01-chaos.png');
})();
