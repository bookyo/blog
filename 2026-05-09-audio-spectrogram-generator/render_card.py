#!/usr/bin/env python3
"""Render highlight cards as HTML and screenshot them."""

import subprocess
import os

WORKDIR = '/Users/quyue/www/blog/2026-05-09-audio-spectrogram-generator'
NODE = '/Users/quyue/.nvm/versions/node/v24.13.0/bin/node'
NODE_PATH = '/Users/quyue/.hermes/hermes-agent/node_modules'

CARDS = [
    {
        'slug': 'card-01',
        'theme': 'ocean',
        'eyebrow': 'CORE PRINCIPLE',
        'title': 'The Fourier Foundation',
        'dek': 'A spectrogram is not a recording. It is a decomposition — a mathematical unwrapping of sound into its most fundamental parts.',
        'bullets': [
            'Time runs left to right; frequency runs top to bottom',
            'Color intensity = volume at that frequency and moment',
            'The Fourier transform makes the invisible visible',
        ],
        'quote': 'The result looks almost like a topographical map, with bright ridges and valleys that trace patterns invisible to the naked waveform.',
    },
    {
        'slug': 'card-02',
        'theme': 'ember',
        'eyebrow': 'MUSIC & SOUND',
        'title': 'One Chord, A Thousand Lines',
        'dek': 'A piano chord sounds like a single entity. A spectrogram shows a precise constellation of horizontal lines at mathematically related frequencies.',
        'bullets': [
            'Fundamental note at the bottom — the perceived pitch',
            'Harmonic overtones ascend in diminishing brightness',
            'These overtone ratios define the instrument\'s timbre',
        ],
        'quote': 'The relative strength of these overtones is what gives a piano its characteristic timbre — why it sounds different from a guitar playing the same note.',
    },
    {
        'slug': 'card-03',
        'theme': 'forest',
        'eyebrow': 'ACCESSIBILITY',
        'title': 'Audio Literacy for Everyone',
        'dek': 'What once required specialized software and acoustic expertise is now available in a browser tab, free, in seconds.',
        'bullets': [
            'Upload any audio format — MP3, WAV, FLAC, OGG, and more',
            'Choose from 8 color palettes for different analytical needs',
            'Magma for quick scanning; Viridis for scientific accuracy',
        ],
        'quote': 'Understanding spectrograms is, in a meaningful sense, understanding how audio actually works — bridging the gap between passive listening and technical comprehension.',
    },
]

THEMES = {
    'forest': {'accent': '#00FF94', 'bg': '#001A0D', 'muted': '#00CC77'},
    'ocean': {'accent': '#00B4D8', 'bg': '#000D1A', 'muted': '#0090B8'},
    'ember': {'accent': '#FF6B35', 'bg': '#0D0D0D', 'muted': '#CC5529'},
}

def render_card(card):
    t = THEMES[card['theme']]
    bullets_html = '\n'.join(f'<li class="text-[18px] text-[#d0d0e0]">• {b}</li>' for b in card['bullets'])

    html = '<!DOCTYPE html><html lang="en"><head>' \
        + '<meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script>' \
        + '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">' \
        + f'<style>body{{font-family:"Outfit",sans-serif;background:{t["bg"]};}}</style>' \
        + '</head><body class="flex items-center justify-center min-h-screen">' \
        + '<div class="w-[1080px] px-16 py-14">' \
        + f'<p class="text-[13px] text-[{t["accent"]}] font-semibold tracking-[0.2em] mb-4">{card["eyebrow"]}</p>' \
        + f'<h2 class="text-[72px] font-black text-white leading-[1.0] mb-6">{card["title"]}</h2>' \
        + f'<p class="text-[22px] text-white/70 leading-relaxed mb-8">{card["dek"]}</p>' \
        + '<ul class="space-y-2 mb-10">' + bullets_html + '</ul>' \
        + f'<blockquote class="border-l-4 border-[{t["accent"]}] pl-6">' \
        + f'<p class="text-[18px] text-white/80 italic leading-relaxed">"{card["quote"]}</p>' \
        + '</blockquote></div></body></html>'
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
}})();'''

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