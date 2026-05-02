
const { chromium } = require('playwright');
const path = require('path');

// Card 2: The Target is Silence
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
  .card-bg { background: #0D0D0D; }
  .accent { color: #FF6B35; }
  .accent-bg { background: #FF6B35; }
  .muted { color: #CC5529; }
</style>
</head>
<body class="card-bg flex items-center justify-center min-h-screen">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[20px] font-semibold tracking-[0.3em] accent uppercase mb-8">The Goal</p>
    <p class="text-[48px] font-bold text-white leading-tight mb-6">Zero Beats.</p>
    <p class="text-[28px] text-[#666666] leading-relaxed mb-8">The target is not a pitch.<br/>It is the silence between them.</p>
    <p class="text-[18px] text-[#444444] leading-relaxed">When the pulsing stops,<br/>the instrument is in tune.</p>
  </div>
</body>
</html>`;
  
  await page.setContent(html);
  await page.waitForTimeout(1500);
  
  const outputPath = path.join(__dirname, 'card-02-silence.png');
  await page.screenshot({ path: outputPath, fullPage: true });
  await browser.close();
  console.log('Card 2 saved:', outputPath);
})();
