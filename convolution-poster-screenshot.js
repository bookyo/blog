const { chromium } = require('playwright');
const fs = require('fs');

const html = [
  '<!DOCTYPE html><html><head><style>',
  '* { margin: 0; padding: 0; box-sizing: border-box; }',
  'body { background: #0a0a1a; font-family: Segoe UI, Arial, sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }',
  '.container { width: 1200px; height: 630px; background: linear-gradient(135deg, #0d0d2b 0%, #1a1a3e 50%, #0d0d2b 100%); position: relative; padding: 48px 56px; display: flex; flex-direction: column; }',
  '.top-label { position: absolute; top: 32px; left: 56px; background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.4); color: #a5b4fc; font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; padding: 6px 16px; border-radius: 4px; }',
  '.main-title { color: #ffffff; font-size: 48px; font-weight: 700; line-height: 1.2; margin-top: 40px; max-width: 760px; }',
  '.title-accent { background: linear-gradient(90deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }',
  '.main-subtitle { color: #94a3b8; font-size: 20px; margin-top: 20px; max-width: 640px; line-height: 1.5; }',
  '.bottom-bar { position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #c084fc); }',
  '.badge { position: absolute; bottom: 36px; right: 56px; background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); color: #a5b4fc; font-size: 14px; padding: 10px 20px; border-radius: 6px; }',
  '.formula-box { position: absolute; bottom: 36px; left: 56px; background: rgba(0,0,0,0.3); border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 14px 24px; font-family: Courier New, monospace; color: #e0e7ff; font-size: 18px; letter-spacing: 1px; }',
  '.visual-preview { position: absolute; top: 32px; right: 56px; width: 320px; height: 180px; background: rgba(0,0,0,0.2); border: 1px solid rgba(99,102,241,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; overflow: hidden; }',
  '.signal-viz { display: flex; align-items: center; gap: 3px; padding: 20px; }',
  '.bar { width: 7px; border-radius: 2px; }',
  '</style></head><body>',
  '<div class="container">',
  '<div class="top-label">Signal Processing &middot; Interactive Visualization</div>',
  '<div class="main-title">The <span class="title-accent">Four-Step Math</span> That Powers Every Photo Filter, Audio Effect, and AI Vision System</div>',
  '<div class="main-subtitle">Flip &middot; Slide &middot; Multiply &middot; Sum &mdash; The elegant operation hiding inside convolution, CNNs, and half the technology you use daily</div>',
  '<div class="visual-preview"><div class="signal-viz" id="viz"></div></div>',
  '<div class="formula-box">FFT(x * h) = FFT(x) &middot; FFT(h)</div>',
  '<div class="badge">elysiatools.com</div>',
  '<div class="bottom-bar"></div>',
  '</div>',
  '<script>',
  'var viz = document.getElementById("viz");',
  'var signals = [',
  '[20,35,55,70,85,95,100,95,85,70,55,35,20,10,5,3,1,0,1,3,5,10,20,35,55,70,85,95,100,95,85,70,55,35,20],',
  '[5,10,20,40,60,80,95,100,95,80,60,40,20,10,5,2,0,2,5,10,20,40,60,80,95,100,95,80,60,40,20,10,5],',
  '[0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]',
  '];',
  'var colors = ["#6366f1","#8b5cf6","#a855f7"];',
  'for (var s = 0; s < signals.length; s++) {',
  '  var group = document.createElement("div");',
  '  group.style.display = "flex";',
  '  group.style.alignItems = "center";',
  '  group.style.gap = "3px";',
  '  group.style.marginRight = "16px";',
  '  var mx = Math.max.apply(null, signals[s]);',
  '  for (var i = 0; i < signals[s].length; i++) {',
  '    var bar = document.createElement("div");',
  '    bar.className = "bar";',
  '    var h = (signals[s][i] / mx) * 80 + 5;',
  '    bar.style.height = h + "px";',
  '    bar.style.background = "linear-gradient(to top, " + colors[s] + ", " + colors[(s+1)%3] + ")";',
  '    group.appendChild(bar);',
  '  }',
  '  viz.appendChild(group);',
  '}',
  '<\/script>',
  '</body></html>'
].join('\n');

fs.writeFileSync('/tmp/poster.html', html);

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto('file:///tmp/poster.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-28-convolution-interactive-visualization/poster.png', type: 'png' });
  await browser.close();
  console.log('Screenshot saved');
})();
