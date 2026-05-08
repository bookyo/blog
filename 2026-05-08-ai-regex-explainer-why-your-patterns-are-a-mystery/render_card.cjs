const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CATCH',
      title: 'Your Regex Works in Python, Fails in JS',
      dek: 'Lookbehinds, named groups, and atomic quantifiers behave differently across JavaScript, Python, PCRE, Go, and Java. A pattern that passes tests in your local environment can silently break in production.',
      quote: '"The same pattern — five different results."',
      bullets: ['Lookbehind (?<=...) requires ES2018+ in JavaScript', 'Go RE2 doesn\'t support lookbehind at all', 'Named groups use (?P<name>...) in Python vs (?<name>...) in JavaScript'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'PRODUCTION RISK',
      title: 'The Regex That Can Crash Your Server',
      dek: 'Catastrophic backtracking occurs when poorly constructed patterns cause exponential computation. A malicious or accidental input can hang a Node.js process indefinitely.',
      quote: '"A pattern like (a+)+b matched against a string of a\'s with no trailing b."',
      bullets: ['Nested quantifiers with backreferences are dangerous', 'AI Regex Explainer flags these patterns before deployment', 'Real-world: has caused major company outages'],
      theme: 'ember'
    },
    {
      num: '03',
      eyebrow: 'IN ACTION',
      title: 'Decoding a Real Email Validator',
      dek: 'The pattern ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$ breaks down into anchor, character classes, quantifiers, and literal separators — all explained position by position.',
      quote: '"Simple on the surface. Never understood — until now."',
      bullets: ['Segment-by-segment breakdown with exact positions', 'Complexity rating: moderate (no lookarounds)', 'Confirmed working across JS, Python, and PCRE'],
      theme: 'forest'
    }
  ];

  const themeStyles = {
    ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
    ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' },
    forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
  };

  for (const c of cards) {
    const style = themeStyles[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + style.bg + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] text-[' + style.accent + '] font-semibold tracking-[0.2em] mb-4">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[\#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] text-[' + style.accent + '] italic mb-6">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[\#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
      
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(__dirname, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card ' + c.num + ' saved');
  }
  
  await browser.close();
  console.log('All cards rendered');
})();
