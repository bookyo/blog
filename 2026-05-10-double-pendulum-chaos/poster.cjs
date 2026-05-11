const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 800 } });
  
  const html = '<!DOCTYPE html><html lang="en"><head>' +
    '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script>' +
    '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">' +
    '<style>body{font-family:"Outfit",sans-serif;background:#000000;}</style>' +
    '</head><body class="bg-black flex items-center justify-center min-h-screen">' +
    '<div class="w-[1080px] text-center px-[108px] py-24">' +
    '<p class="text-[18px] text-[#00FF94] font-semibold tracking-[0.3em] mb-6">DETERMINISTIC CHAOS</p>' +
    '<h1 class="text-[110px] font-black text-white tracking-tight leading-none">0.001°</h1>' +
    '<p class="text-[48px] font-bold text-[#00FF94] mt-6 tracking-tight">Changes Everything</p>' +
    '<p class="text-[18px] text-[#666666] mt-10 leading-relaxed">The double pendulum proves that perfect knowledge of rules<br/>does not guarantee predictability</p>' +
    '</div></body></html>';
  
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(__dirname, 'poster.png'), fullPage: true });
  await browser.close();
  console.log('Poster saved to poster.png');
})();
