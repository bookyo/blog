const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE PROBLEM',
      title: 'Syntax ≠ Deliverability',
      dek: 'A regex check only confirms a string looks like an email. It says nothing about whether the domain exists, the mailbox is real, or the address is a disposable that will vanish tomorrow.',
      quote: '"A 15% bounce rate gets you flagged. A 20% bounce rate gets you blocked."',
      bullets: ['Format validation catches nothing', 'Domain structure goes unchecked', 'Disposable domains slip through', 'Role accounts look valid'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'THE SILENT KILLER',
      title: 'Disposable Emails',
      dek: 'tempmail.org, 10minutemail.com, guerrillamail.com — these services produce legitimate-looking addresses that accept mail briefly then disappear, taking your sender reputation with them.',
      quote: '"Gmail and Outlook flag you as a list buyer or a spammer. Both get the same result."',
      bullets: ['500 disposable bounces = reputation damage', 'Addresses expire in minutes to hours', 'Flagged automatically by quality scanner', 'Segment or remove before sending'],
      theme: 'ember'
    },
    {
      num: '03',
      eyebrow: 'WHAT\'S NEXT',
      title: 'Beyond Pattern Matching',
      dek: 'The current tool catches structural issues and disposable domains. The next layer — MX lookup, SMTP verification, and catch-all detection — would close the remaining 10-20% gap.',
      quote: '"SMTP verification is the gold standard. Most free tools won\'t do it because it\'s a great way to get your IP blacklisted."',
      bullets: ['MX lookup: confirm mail server exists', 'SMTP verify: ask server if mailbox exists', 'Catch-all detection: identify accept-all domains', 'Pattern matching has reached its limit'],
      theme: 'forest'
    }
  ];

  const themeColors = {
    ocean:   { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8' },
    ember:   { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529' },
    forest:  { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77' }
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
      '<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:' + colors.accent + ';">' + c.eyebrow + '</p>' +
      '<h2 class="text-[72px] font-black leading-[1.0] mb-6" style="color:#ffffff;">' + c.title + '</h2>' +
      '<p class="text-[22px] leading-relaxed mb-8" style="color:#a0a0b0;">' + c.dek + '</p>' +
      '<p class="text-[18px] italic mb-6" style="color:' + colors.accent + ';">' + c.quote + '</p>' +
      '<ul class="space-y-2">' +
      c.bullets.map(b => '<li class="text-[16px]" style="color:#d0d0e0;">• ' + b + '</li>').join('') +
      '</ul></div></body></html>';
    
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    
    const outPath = path.join(__dirname, 'card-' + c.num + '.png');
    await page.screenshot({ path: outPath, fullPage: true });
    console.log('Card', c.num, 'saved to:', outPath);
    await page.close();
  }
  
  await browser.close();
  console.log('All cards done.');
})();
