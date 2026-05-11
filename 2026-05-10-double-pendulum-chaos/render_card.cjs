const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'CORE INSIGHT',
      title: 'No Two Runs Ever Repeat',
      dek: 'The second bob traces patterns of breathtaking complexity. No two runs ever repeat. Yet the system is entirely deterministic—there is no randomness, no noise, no quantum uncertainty.',
      quote: '"The equations are perfectly known. The initial conditions are fixed. And yet the outcome is fundamentally unpredictable."',
      theme: 'forest'
    },
    {
      num: '02',
      eyebrow: 'THE BUTTERFLY EFFECT',
      title: '0.001° Changes Everything',
      dek: 'For the double pendulum, this sensitivity is extreme. Change the starting angle of the first arm by just 0.001°—a difference too small to see—and within seconds the trajectories will have diverged completely.',
      quote: '"A gentle tap on the first arm at the start produces an entirely different dance."',
      theme: 'forest'
    },
    {
      num: '03',
      eyebrow: 'DETERMINISTIC CHAOS',
      title: 'Predictability Has a Horizon',
      dek: 'A system with well-defined rules, fixed constants, conserved quantities—and absolutely no predictability beyond a short time horizon. Determinism does not imply predictability.',
      quote: '"Knowing the equations perfectly does not mean we can predict the outcome."',
      theme: 'forest'
    }
  ];

  const themeColors = {
    forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
  };

  for (const c of cards) {
    const colors = themeColors[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + colors.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + colors.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + colors.accent + '] italic mb-6">' + c.quote + '</p>' +
      '</div></body></html>';
    
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(__dirname, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  
  await browser.close();
  console.log('All cards created');
})();
