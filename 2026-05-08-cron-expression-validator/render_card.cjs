const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE PROBLEM',
      title: 'One Character,\nSix Months of Chaos',
      dek: 'A single 6 instead of 0 in the hour field. A backup job that ran at noon instead of midnight. No error logs. No warnings. Just silent misbehavior costing bandwidth and sanity.',
      quote: '"The job ran exactly as specified."',
      bullets: ['Silent failure — cron accepts it without error', '3 AM became 6 PM for 6 months', 'No logs, no alerts, just wrong behavior'],
      bgColor: '#0a0a1a',
      accentColor: '#FF6B35'
    },
    {
      num: '02',
      eyebrow: 'COMMON MISTAKES',
      title: 'Six Ways Your\nCron Expression Lies',
      dek: 'Off-by-one weekdays. Conflicting day fields. 24-hour vs 12-hour confusion. These bugs look correct and deploy cleanly, then silently destroy your schedule.',
      quote: '"0 0 * * 0 — Sunday or Monday?"',
      bullets: ['Sunday is both 0 and 7', 'Day-of-month + day-of-week = OR, not AND', '6-field vs 5-field — copy-paste disaster'],
      bgColor: '#0a1a0a',
      accentColor: '#00FF94'
    },
    {
      num: '03',
      eyebrow: 'VALIDATION',
      title: 'Two Seconds to\nPrevent a Crisis',
      dek: 'Before deployment, validate: parsed field breakdown, human-readable translation, next 5 run times, and warnings for dangerous patterns. The step that costs nothing and saves everything.',
      quote: '"Cron accepted it without error."',
      bullets: ['Parsed field breakdown per unit', 'Next 5 execution timestamps', 'Conflicting field warnings'],
      bgColor: '#0a0a1a',
      accentColor: '#00B4D8'
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      '<style>body{font-family:"Outfit",sans-serif;background:' + c.bgColor + ';}</style>' +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + c.accentColor + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6" style="white-space:pre;">' + c.title + '</h2>' +
      '<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + c.accentColor + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0]">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(__dirname, 'card-' + c.num + '.png'), fullPage: true });
    await page.close();
    console.log('Card', c.num, 'rendered');
  }
  
  await browser.close();
  console.log('All cards done');
})();
