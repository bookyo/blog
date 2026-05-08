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
<title>Article Poster</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>body { font-family: 'Outfit', sans-serif; }</style>
</head>
<body class="bg-black flex items-center justify-center min-h-screen">
  <div class="w-[1080px] text-center px-[108px] py-24">
    <h1 class="text-[96px] font-black text-white tracking-tight leading-none">^(?=.*\\d).{8,}$</h1>
    <p class="text-[48px] font-bold text-[#00FF94] mt-6 tracking-tight">???</p>
    <p class="text-[18px] text-[#666666] mt-10 leading-relaxed">AI Regex Explainer — Turn any pattern into plain English</p>
    <p class="text-[14px] text-[#444444] mt-4 tracking-widest uppercase">ElysiaTools</p>
  </div>
</body>
</html>`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(__dirname, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster saved to poster.png');
})();
