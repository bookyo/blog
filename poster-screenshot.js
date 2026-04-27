const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setViewportSize({ width: 1200, height: 630 });
  
  const html = `<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1200px;
    height: 630px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 60px;
    position: relative;
    overflow: hidden;
  }
  .grid-bg {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
  }
  .glow {
    position: absolute;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(79,172,254,0.15) 0%, transparent 70%);
    top: -100px; right: -100px;
  }
  .glow2 {
    position: absolute;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(168,85,247,0.12) 0%, transparent 70%);
    bottom: -80px; left: -80px;
  }
  .badge {
    background: rgba(79,172,254,0.15);
    border: 1px solid rgba(79,172,254,0.3);
    color: #4facfe;
    font-size: 14px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    margin-bottom: 30px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  h1 {
    color: #ffffff;
    font-size: 56px;
    font-weight: 700;
    text-align: center;
    line-height: 1.2;
    margin-bottom: 20px;
    max-width: 900px;
  }
  h1 span {
    background: linear-gradient(90deg, #4facfe, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  p {
    color: rgba(255,255,255,0.6);
    font-size: 20px;
    text-align: center;
    max-width: 700px;
    line-height: 1.6;
  }
  .keyframes-preview {
    margin-top: 35px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 20px 30px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: rgba(255,255,255,0.7);
    text-align: left;
    width: 500px;
  }
  .keyframes-preview .kw { color: #a855f7; }
  .keywords {
    display: flex;
    gap: 10px;
    margin-top: 30px;
    flex-wrap: wrap;
    justify-content: center;
  }
  .kw-tag {
    background: rgba(168,85,247,0.15);
    color: #c084fc;
    font-size: 13px;
    padding: 4px 12px;
    border-radius: 6px;
  }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="glow"></div>
  <div class="glow2"></div>
  <div class="badge">Free CSS Tool</div>
  <h1>Web Interfaces That <span>Move Right</span></h1>
  <p>Generate production-ready CSS animation keyframes and properties in seconds. No sign-up required.</p>
  <div class="keywords">
    <span class="kw-tag">@keyframes</span>
    <span class="kw-tag">fade</span>
    <span class="kw-tag">slide</span>
    <span class="kw-tag">scale</span>
    <span class="kw-tag">rotate</span>
    <span class="kw-tag">bounce</span>
    <span class="kw-tag">easing</span>
  </div>
</body>
</html>`;

  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: '/Users/quyue/www/blog/2026-04-27-css-animation-generator/poster.png', fullPage: false });
  
  await browser.close();
  console.log('Poster saved to poster.png');
})();
