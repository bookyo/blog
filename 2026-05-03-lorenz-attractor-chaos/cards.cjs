const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  
  const cardHtml = fs.readFileSync(path.join(__dirname, 'cards.html'), 'utf8');
  
  // Extract each card HTML - split by card divs
  const cardRegex = /<div class="card bg-\[#0D0D0D\] p-16[^>]*>[\s\S]*?<\/div>\n\n/g;
  const cardMatches = [...cardHtml.matchAll(cardRegex)].map(m => m[0]);
  
  console.log('Found', cardMatches.length, 'cards');
  
  for (let i = 0; i < cardMatches.length; i++) {
    const cardInner = cardMatches[i];
    const cardIndex = String(i+1).padStart(2,'0');
    
    const singleCardHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Card ${i+1}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Outfit', sans-serif; background: #000; margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
</style>
</head>
<body>
<div style="width:1080px;min-height:900px;background:#0D0D0D;padding:4rem;display:flex;flex-direction:column;justify-content:space-between;">
${cardInner.replace(/<div class="card bg-\[#0D0D0D\] p-16 /, '').replace(/<\/div>\n\n$/, '</div>')}
</div>
</body>
</html>`;
    
    const cardPath = path.join(__dirname, `card-${cardIndex}.html`);
    fs.writeFileSync(cardPath, singleCardHtml);
    console.log('Written:', cardPath);
  }
  
  // Now screenshot each card
  for (let i = 0; i < cardMatches.length; i++) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 900 } });
    const cardIndex = String(i+1).padStart(2,'0');
    const cardPath = path.join(__dirname, `card-${cardIndex}.html`);
    const outputPath = path.join(__dirname, `card-${cardIndex}.png`);
    
    await page.goto(`file://${cardPath}`);
    await page.waitForTimeout(2000);
    
    await page.screenshot({ path: outputPath, fullPage: true });
    console.log(`Card ${i+1} saved to:`, outputPath);
    await page.close();
  }
  
  await browser.close();
  console.log('All cards generated.');
})();
