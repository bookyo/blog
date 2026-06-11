"""Build poster + 3 highlight cards inline (no external skill)."""
ARTICLE_DIR = '/Users/quyue/www/blog/2026-06-11-slug-validator-the-rules-behind-every-clean-url'
ACCENT = '#00B4D8'  # ocean blue
SLUG = 'slug-validator'
TOOL_NAME = 'Slug Validator'
POST_TITLE = 'Three Rules That Decide If Your URL Is Welcome'
POST_TAG = 'Clean URL, Lowercase, Slug Rules'

# ---------------- POSTER ----------------
poster_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>
body {
  font-family: 'Outfit', sans-serif;
  width: 1080px;
  min-height: 900px;
  margin: 0;
}
</style>
</head>
<body class="bg-black flex items-center justify-center">
  <div class="w-[1080px] text-center px-[108px] py-24">
    <p class="text-[24px] font-bold text-[#00B4D8] tracking-widest uppercase mb-8">Slug Validator</p>
    <h1 class="text-[120px] font-black text-white tracking-tight leading-none">3 RULES</h1>
    <p class="text-[80px] font-black text-[#00B4D8] tracking-tight leading-none mt-4">EVERY URL</p>
    <p class="text-[80px] font-black text-white tracking-tight leading-none mt-4">MUST OBEY</p>
    <p class="text-[28px] text-[#999999] mt-12 leading-relaxed">Lowercase. Hyphens only. Bounded length. The smallest, most boring tool you'll ever bookmark — and the one that saves the most links.</p>
  </div>
</body>
</html>
'''

# ---------------- CARDS ----------------
card_htmls = {
'card1': '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; width: 1080px; min-height: 900px; margin: 0; }
.code { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="bg-black flex items-center justify-center">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[24px] font-bold text-[#00B4D8] tracking-widest uppercase mb-6">The Three Rules</p>
    <h2 class="text-[64px] font-black text-white leading-tight mb-10">A valid slug is exactly<br/>this — and nothing else</h2>
    <div class="text-left space-y-5 max-w-[800px] mx-auto">
      <div class="bg-[#0a0a0a] border-l-4 border-[#00B4D8] p-6">
        <p class="code text-[32px] text-white">^[a-z0-9-]+$</p>
        <p class="text-[20px] text-[#999999] mt-2">Lowercase letters, digits, hyphens only — nothing else.</p>
      </div>
      <div class="bg-[#0a0a0a] border-l-4 border-[#00B4D8] p-6">
        <p class="code text-[28px] text-white">no leading/trailing hyphens</p>
        <p class="text-[20px] text-[#999999] mt-2">No <code class="code">--</code> either. Parsers and shells disagree about what that means.</p>
      </div>
      <div class="bg-[#0a0a0a] border-l-4 border-[#00B4D8] p-6">
        <p class="code text-[28px] text-white">length &lt; ~80 chars</p>
        <p class="text-[20px] text-[#999999] mt-2">Fits in a tweet, an email, an analytics dashboard. Beyond that, you lose readers.</p>
      </div>
    </div>
  </div>
</body>
</html>
''',

'card2': '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; width: 1080px; min-height: 900px; margin: 0; }
.code { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="bg-black flex items-center justify-center">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[24px] font-bold text-[#00B4D8] tracking-widest uppercase mb-6">The Four Failure Modes</p>
    <h2 class="text-[64px] font-black text-white leading-tight mb-10">What breaks, and why<br/>no one catches it</h2>
    <div class="grid grid-cols-2 gap-5 max-w-[900px] mx-auto text-left">
      <div class="bg-[#0a0a0a] p-6 border-t-2 border-[#00B4D8]">
        <p class="text-[20px] font-bold text-white">Spaces</p>
        <p class="text-[16px] text-[#999999] mt-2">CMS authors type titles; migrations copy them. <code class="code">%20</code> survives in the wild, breaks social previews.</p>
      </div>
      <div class="bg-[#0a0a0a] p-6 border-t-2 border-[#00B4D8]">
        <p class="text-[20px] font-bold text-white">Uppercase</p>
        <p class="text-[16px] text-[#999999] mt-2">Apache is case-sensitive. Static site generators aren't. The mismatch shows up at the worst time.</p>
      </div>
      <div class="bg-[#0a0a0a] p-6 border-t-2 border-[#00B4D8]">
        <p class="text-[20px] font-bold text-white">Punctuation</p>
        <p class="text-[16px] text-[#999999] mt-2">Smart quotes, em-dashes, emoji — all get stripped, replaced, or URL-encoded differently per framework.</p>
      </div>
      <div class="bg-[#0a0a0a] p-6 border-t-2 border-[#00B4D8]">
        <p class="text-[20px] font-bold text-white">Length</p>
        <p class="text-[16px] text-[#999999] mt-2">250-character slugs from long titles break in email, chat, social unfurls, and analytics dashboards.</p>
      </div>
    </div>
  </div>
</body>
</html>
''',

'card3': '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Outfit', sans-serif; width: 1080px; min-height: 900px; margin: 0; }
.code { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="bg-black flex items-center justify-center">
  <div class="w-[1080px] px-[80px] py-20 text-center">
    <p class="text-[24px] font-bold text-[#00B4D8] tracking-widest uppercase mb-6">CI Pipeline in 30 Lines</p>
    <h2 class="text-[64px] font-black text-white leading-tight mb-8">Run the same checks<br/>in your build</h2>
    <div class="bg-[#0a0a0a] p-8 max-w-[920px] mx-auto text-left">
      <pre class="code text-[24px] text-white leading-snug"><code>function isValidSlug(s, opts={}) {
  const allow = opts.allowUnderscores ?? false;
  const max   = opts.maxLength ?? 200;
  if (!s || s.length &gt; max)        return false;
  if (s.startsWith('-') ||
      s.endsWith('-'))                return false;
  if (s.includes('--'))               return false;
  const re = allow
    ? /^[a-z0-9_-]+$/
    : /^[a-z0-9-]+$/;
  return re.test(s);
}</code></pre>
    </div>
    <p class="text-[22px] text-[#999999] mt-8 leading-relaxed">The same three rules, encoded once, applied on every commit. The tool exists so you don't have to write this — but you can.</p>
  </div>
</body>
</html>
''',
}

with open(f'{ARTICLE_DIR}/poster.html', 'w') as f:
    f.write(poster_html)
for name, html in card_htmls.items():
    with open(f'{ARTICLE_DIR}/{name}.html', 'w') as f:
        f.write(html)

print('HTML files written:')
import os
for f in sorted(os.listdir(ARTICLE_DIR)):
    if f.endswith('.html'):
        print(f'  {f}: {os.path.getsize(ARTICLE_DIR + "/" + f)} bytes')
