const { chromium } = require('playwright');
const path = require('path');

const articleDir = '/Users/quyue/www/blog/2026-05-08-quantum-harmonic-oscillator';

(async () => {
  const browser = await chromium.launch();
  
  const cards = [
    {
      num: '01',
      eyebrow: 'CORE FORMULA',
      title: 'Eₙ = (n + ½)ħω',
      dek: 'Equally spaced energy levels — each quantum step costs exactly ħω. This single fact makes infrared spectroscopy work and quantum field theory possible.',
      quote: '"The harmonic oscillator is to quantum mechanics what the pendulum is to classical mechanics — the simplest system that contains all the essential physics."',
      bullets: ['Every step: exactly ħω apart', 'Infrared spectroscopy: molecular fingerprinting', 'Equal spacing → single-frequency absorption'],
      accent: '#00FF94'
    },
    {
      num: '02',
      eyebrow: 'ZERO-POINT ENERGY',
      title: 'Nothing Ever Comes to Rest',
      dek: 'Even at absolute zero, the ground state retains ½ħω of energy. This zero-point vibration keeps helium liquid, creates vacuum fluctuations, and is baked into the structure of reality.',
      quote: '"Δx · Δp ≥ ħ/2 — uncertainty forbids stillness."',
      bullets: ['Helium stays liquid to 0K', 'Vacuum seethes with virtual photons', 'Dark energy: sum of zero-point modes'],
      accent: '#00B4D8'
    },
    {
      num: '03',
      eyebrow: 'WAVE FUNCTIONS',
      title: 'Hermite Polynomials in a Gaussian Envelope',
      dek: 'ψₙ(x) = Nₙ · Hₙ(ξ) · e^(−ξ²/2). The Gaussian factor traps the particle. The Hermite polynomial determines how many nodes it has. The result is a taxonomy of shapes that underlies all of chemistry.',
      quote: '"ψ₀: no nodes. ψ₁: one node. ψ₂: two nodes. The node count IS the quantum number."',
      bullets: ['n nodes for quantum number n', 'Gaussian envelope: particle never escapes', 'Hermite polynomials: systematic shape growth'],
      accent: '#FF6B35'
    }
  ];

  for (const c of cards) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const html = '<!DOCTYPE html><html lang="en"><head>' +
      '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"><\/script>' +
      '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' +
      `<style>body{font-family:"Outfit",sans-serif;background:#0a0a1a;}</style>` +
      '</head><body class="flex items-center justify-center min-h-screen">' +
      '<div class="w-[1080px] px-16 py-20">' +
      `<p class="text-[13px] font-semibold tracking-[0.2em] mb-4" style="color:${c.accent}">${c.eyebrow}</p>` +
      `<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">${c.title}</h2>` +
      `<p class="text-[22px] text-[#a0a0b0] leading-relaxed mb-8">${c.dek}</p>` +
      `<p class="text-[18px] italic mb-6" style="color:${c.accent}">${c.quote}</p>` +
      '<ul class="space-y-2">' +
      c.bullets.map(b => `<li class="text-[16px] text-[#d0d0e0]">• ${b}</li>`).join('') +
      '</ul></div></body></html>';
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(articleDir, `card-${c.num}.png`), fullPage: true });
    await page.close();
    console.log(`Card ${c.num} saved`);
  }
  await browser.close();
  console.log('All cards done');
})();
