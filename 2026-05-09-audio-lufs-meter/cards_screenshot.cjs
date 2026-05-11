const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'THE CORE PROBLEM',
      title: 'You Hear With Your Brain, Not Your Ears',
      dek: 'LUFS measures perceived loudness — not physics. A 50Hz bass note can be 15dB louder than a 1kHz tone and sound equally loud. That is why two files with identical dB readings can feel dramatically different.',
      quote: '"Our ears are not equally sensitive to all frequencies"',
      bullets: ['2kHz–5kHz: most sensitive range', 'Low frequencies: require +15dB to match perceived loudness', 'LUFS applies K-weighting to match human hearing'],
      theme: 'ocean'
    },
    {
      num: '02',
      eyebrow: 'HISTORICAL LESSON',
      title: 'The Loudness Wars Are Over',
      dek: 'For decades the audio industry competed to make recordings louder. By the 1990s, albums were so compressed that dynamic range had collapsed — music with no quiet moments sounds quieter, not louder.',
      quote: '"A classical recording at -20dBFS sounds louder than a brick-walled pop track at -3dBFS"',
      bullets: ['Peak dB ≠ perceived loudness', 'Heavy compression kills dynamic range', 'LUFS ended the war by measuring the right thing'],
      theme: 'ember'
    },
    {
      num: '03',
      eyebrow: 'PLATFORM STANDARDS',
      title: 'Every Major Platform Has a LUFS Target',
      dek: 'Spotify and YouTube normalize to -14 LUFS. Netflix sits at -27. Apple Podcasts targets -16. These are not arbitrary numbers — they ensure perceptually consistent volume when switching between content.',
      quote: '"Your phone\'s volume slider is a lie — it applies a simple gain multiplier, not LUFS-normalized adjustment"',
      bullets: ['Spotify / YouTube: -14 LUFS', 'Netflix: -27 LUFS', 'Apple Podcasts: -16 LUFS'],
      theme: 'forest'
    }
  ];

  const themeColors = {
    ocean: { bg: '#000D1A', accent: '#00B4D8', muted: '#0090B8', card_accent: '#00B4D8' },
    ember: { bg: '#0D0D0D', accent: '#FF6B35', muted: '#CC5529', card_accent: '#FF6B35' },
    forest: { bg: '#001A0D', accent: '#00FF94', muted: '#00CC77', card_accent: '#00FF94' }
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
      '<h2 class="text-[68px] font-black text-white leading-[1.05] mb-6">' + c.title + '</h2>' +
      '<p class="text-[21px] text-[#a0a0b0] leading-relaxed mb-8">' + c.dek + '</p>' +
      '<p class="text-[17px] text-[' + colors.accent + '] italic mb-8 leading-relaxed">' + c.quote + '</p>' +
      '<ul class="space-y-3">' +
      c.bullets.map(b => '<li class="text-[16px] text-[#d0d0e0] flex items-start gap-3"><span class="text-[' + colors.accent + '] mt-1">•</span>' + b + '</li>').join('') +
      '</ul></div></body></html>';
    
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);
    
    const outPath = path.join(__dirname, 'card-' + c.num + '.png');
    await page.screenshot({ path: outPath, fullPage: true });
    console.log('Saved:', outPath);
    await page.close();
  }
  await browser.close();
})();
