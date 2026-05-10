const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Duffing Oscillator Poster</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; }
.equation { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="bg-black flex items-center justify-center min-h-screen">
  <div class="w-[1080px] text-center px-[108px] py-16">
    <p class="text-[14px] text-[#666666] font-semibold tracking-[0.3em] mb-8 uppercase">Nonlinear Dynamics · Chaos Theory · Interactive Visualization</p>
    
    <h1 class="text-[88px] font-black text-white tracking-tight leading-[0.9] mb-6">
      ÿ + δẏ + αy + βy³<br/>
      <span class="text-[#00FF94]">= γ cos(ωt)</span>
    </h1>
    
    <p class="text-[52px] font-bold text-white mt-8 tracking-tight leading-tight">
      The Equation That<br/>
      <span class="text-[#00FF94]">Proves Deterministic Systems</span><br/>
      Can Be Fundamentally Unpredictable
    </p>
    
    <p class="text-[18px] text-[#666666] mt-10 leading-relaxed max-w-[700px] mx-auto">
      Double-well potential · Period doubling · Strange attractors
    </p>
    
    <div class="mt-12 flex items-center justify-center gap-4">
      <span class="text-[13px] text-[#444444] tracking-widest uppercase">Explore on ElysiaTools</span>
      <span class="text-[#00FF94] text-[13px] tracking-widest">elysiatools.com</span>
    </div>
  </div>
</body>
</html>`;
  
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(__dirname, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster saved to poster.png');
})();
