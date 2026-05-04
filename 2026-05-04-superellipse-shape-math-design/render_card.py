#!/usr/bin/env python3
"""Render highlight cards as HTML and screenshot them."""

import subprocess
import os

WORKDIR = '/Users/quyue/www/blog/2026-05-04-superellipse-shape-math-design'
NODE = '/Users/quyue/.nvm/versions/node/v24.13.0/bin/node'
NODE_PATH = '/Users/quyue/.hermes/hermes-agent/node_modules'

CARDS = [
    {
        'slug': 'card-01',
        'theme': 'forest',
        'eyebrow': 'Design',
        'title': 'The Squircle Fix',
        'dek': 'Apple engineers discovered the superellipse in 2007 — not by accident, but by design.',
        'bullets': [
            'n = 4 creates the perfect balance',
            'No circular arcs — pure continuous curvature',
            'Every iOS icon uses it today',
        ],
        'quote': 'It satisfies both the mathematical definition of "round" and the perceptual expectation of "square."',
    },
    {
        'slug': 'card-02',
        'theme': 'ocean',
        'eyebrow': 'Architecture',
        'title': 'One Equation, One Plaza',
        'dek': 'Piet Hein built Sergels Torg in Stockholm from the superellipse in the 1960s.',
        'bullets': [
            "Stockholm's central plaza since 1968",
            'Shape rejected both circle and square',
            'Hein: "The eye prefers continuous curvature"',
        ],
        'quote': 'The superellipse, Hein argued, was the most aesthetically pleasing intermediate between a circle and a rectangle.',
    },
    {
        'slug': 'card-03',
        'theme': 'ember',
        'eyebrow': 'Mathematics',
        'title': 'n Is the Whole Story',
        'dek': 'From diamond to squircle in one parameter.',
        'bullets': [
            'n = 1 → diamond (rhombus)',
            'n = 2 → standard ellipse/circle',
            'n = 4 → squircle (iOS icons)',
            'n >= 10 → approaches rectangle',
        ],
        'quote': 'One equation. Three parameters. A spectrum of shapes from circle to rectangle.',
    },
]

THEMES = {
    'forest': {'accent': '#00FF94', 'bg': '#001A0D', 'muted': '#00CC77'},
    'ocean': {'accent': '#00B4D8', 'bg': '#000D1A', 'muted': '#0090B8'},
    'ember': {'accent': '#FF6B35', 'bg': '#0D0D0D', 'muted': '#CC5529'},
}

def render_card(card):
    t = THEMES[card['theme']]
    bullets_html = '\n'.join(f'<li>{b}</li>' for b in card['bullets'])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
<style>body {{ font-family: 'Outfit', sans-serif; background: {t['bg']}; }}</style>
</head>
<body class="bg-[{t['bg']}] flex items-center justify-center min-h-screen">
<div class="w-[1080px] px-16 py-14">
  <p class="text-[18px] font-semibold tracking-[0.2em] text-[{t['accent']}] mb-4">{card['eyebrow']}</p>
  <h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">{card['title']}</h2>
  <p class="text-[26px] text-white/70 leading-relaxed mb-8">{card['dek']}</p>
  <ul class="space-y-3 mb-10">
    {bullets_html}
  </ul>
  <blockquote class="border-l-4 border-[{t['accent']}] pl-6">
    <p class="text-[22px] text-white/80 italic leading-relaxed">"{card['quote']}"</p>
  </blockquote>
</div>
</body>
</html>'''
    return html

def main():
    os.makedirs(WORKDIR, exist_ok=True)
    
    for card in CARDS:
        html = render_card(card)
        slug = card['slug']
        html_path = os.path.join(WORKDIR, f'{slug}.html')
        png_path = os.path.join(WORKDIR, f'{slug}.png')
        
        with open(html_path, 'w') as f:
            f.write(html)
        
        script = f'''const {{ chromium }} = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage({{ viewport: {{ width: 1080, height: 900 }} }});
  const html = fs.readFileSync('{html_path}', 'utf8');
  await page.setContent(html, {{ waitUntil: 'networkidle' }});
  await page.waitForTimeout(2000);
  await page.screenshot({{ path: '{png_path}', fullPage: true }});
  await browser.close();
  console.log('{slug} done');
}})();
'''
        script_path = os.path.join(WORKDIR, f'{slug}-screenshot.cjs')
        with open(script_path, 'w') as f:
            f.write(script)
        
        result = subprocess.run(
            [NODE, script_path],
            env={'NODE_PATH': NODE_PATH},
            capture_output=True, text=True, timeout=120
        )
        print(result.stdout, result.stderr[:200] if result.stderr else '')
    
    print("All cards done!")

if __name__ == '__main__':
    main()
