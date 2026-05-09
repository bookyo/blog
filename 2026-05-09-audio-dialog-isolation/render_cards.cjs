const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const cards = [
  {
    num: '01',
    eyebrow: 'THE CORE PROBLEM',
    title: 'The Cocktail Party Problem',
    dek: 'For decades, pulling a single voice from a mixed recording was called unsolvable — a fundamental limitation of signal processing.',
    quote: '"No multitrack sessions. No isolated stems. Just the final stereo mix."',
    bullets: ['Single-channel separation was theoretically impossible', 'Human brains solve it unconsciously — but the algorithm was unknown', 'AI learned the statistics of what vocals look like inside a mix'],
    theme: 'ocean'
  },
  {
    num: '02',
    eyebrow: 'REAL-WORLD USE CASES',
    title: 'Beyond the Karaoke Machine',
    dek: 'Vocals and accompaniment isolation enables music education, forensic analysis, accessibility tools, and podcast production — not just party tricks.',
    quote: '"A student learning guitar can isolate the bass line and transcribe it note-for-note."',
    bullets: ['Music education: isolate any instrument from a finished track', 'Sound design: sample drum breaks without recording off vinyl', 'Accessibility: boost vocal clarity for hearing-impaired listeners'],
    theme: 'ember'
  },
  {
    num: '03',
    eyebrow: 'THE HONEST LIMITS',
    title: 'What the Demos Hide',
    dek: 'Current models still mangle vocal attacks, strip reverb, and blur harmonically aligned instruments. The "4-5 dB improvement" number hides more than it reveals.',
    quote: '"A vocal that sounds strangely dry — because the model stripped the reverb along with the room tone."',
    bullets: ['Transients (p, t consonants) get smeared or attenuated', 'Reverb baked into the recording is impossible to cleanly separate', 'Diffusion-based models are the next frontier'],
    theme: 'forest'
  }
];

const themeColors = {
  ocean: { accent: '#00B4D8', bg: '#000D1A', muted: '#0090B8' },
  ember: { accent: '#FF6B35', bg: '#0D0D0D', muted: '#CC5529' },
  forest: { accent: '#00FF94', bg: '#001A0D', muted: '#00CC77' }
};

(async () => {
  const browser = await chromium.launch();

  for (const c of cards) {
    const theme = themeColors[c.theme];
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });

    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      `<style>body{font-family:"Outfit",sans-serif;background:${theme.bg};}</style>` +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      `<p class="text-[13px] text-[${theme.accent}] font-semibold tracking-[0.2em] mb-4">${c.eyebrow}</p>` +
      `<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">${c.title}</h2>` +
      `<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">${c.dek}</p>` +
      `<p class="text-[18px] text-[${theme.accent}] italic mb-6">${c.quote}</p>` +
      '<ul class="space-y-2">' +
      c.bullets.map(b => `<li class="text-[16px] text-[#d0d0e0]">• ${b}</li>`).join('') +
      '</ul></div></body></html>';

    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);

    const outPath = path.join(__dirname, `card-${c.num}.png`);
    await page.screenshot({ path: outPath, fullPage: true });
    console.log(`Card ${c.num} saved to ${outPath}`);
    await page.close();
  }

  await browser.close();
  console.log('All cards done');
})();
