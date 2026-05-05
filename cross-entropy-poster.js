const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const html = `
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
.container {
  text-align: center;
  padding: 40px;
  max-width: 900px;
}
.label {
  color: #e94560;
  font-size: 14px;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 20px;
  font-weight: 600;
}
.title {
  color: #ffffff;
  font-size: 56px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 30px;
  letter-spacing: -1px;
}
.formula {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 12px;
  padding: 24px 40px;
  display: inline-block;
  margin-bottom: 30px;
}
.formula-text {
  color: #00d4ff;
  font-size: 32px;
  font-family: 'Courier New', monospace;
  font-weight: 600;
}
.desc {
  color: rgba(255,255,255,0.6);
  font-size: 20px;
  line-height: 1.5;
  max-width: 700px;
  margin: 0 auto 40px;
}
.bottom {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255,255,255,0.4);
  font-size: 14px;
}
.bottom span {
  color: #e94560;
  font-weight: 600;
}
</style>
</head>
<body>
<div class="container">
  <div class="label">Machine Learning Loss Function</div>
  <h1 class="title">Cross-Entropy Loss</h1>
  <div class="formula">
    <div class="formula-text">H(P,Q) = -Σ P(x) · log(Q(x))</div>
  </div>
  <p class="desc">The function that tells a neural network how wrong it was —<br>and drives it to be less wrong next time.</p>
  <div class="bottom">
    <span>elysiatools.com</span>
    <span style="color:rgba(255,255,255,0.2)">—</span>
    Free Interactive Tool
  </div>
</div>
</body>
</html>`;

  await page.setContent(html);
  await page.waitForTimeout(1000);
  
  const screenshotPath = '/Users/quyue/www/blog/2026-04-28-cross-entropy-loss/poster.png';
  await page.screenshot({ path: screenshotPath, width: 1200, height: 630 });
  
  console.log('Screenshot saved to:', screenshotPath);
  await browser.close();
})();
