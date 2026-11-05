#!/usr/bin/env python3.11
"""
Render the poster + 3 highlight cards for the Noise Profile Extractor post.

Follows the WP 8557 / WP 8610 rules:
  - pre-measure EVERY string BEFORE rendering; exit non-zero on overflow
  - no Unicode in the PIL glyph blocks (Bubble Text, Enclosed, Dingbats,
    Phonetic Extensions, SMP) — ASCII only
  - pick the card layout from the CONTENT SHAPE
  - use the umbrella PIL templates (article-writer/templates/ is GONE)
"""
import os
import re
import sys

TPL = '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates'
sys.path.insert(0, TPL)

from PIL import Image, ImageDraw, ImageFont
import pil_poster_and_cards_network_theme as pil
from custom_pil_card_layouts import render_card_input_output_2col
from render_card_4tile_compact import render_card_4tile_compact

OUT_DIR = '/tmp/wp_assets_noise'
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- tofu scan
BAD_RANGES = [(0x2460, 0x24FF), (0x2776, 0x2793), (0x1F150, 0x1F1FF),
              (0x1D00, 0x1D5A), (0x2100, 0x214F), (0x1D49C, 0x1D503)]
BAD = ''.join(chr(cp) for lo, hi in BAD_RANGES for cp in range(lo, hi + 1))

# self-test the bad-char class (WP 8557: chr(cp) loops, never \uXXXX escapes)
assert not [c for c in 'ASCII probe' if c in BAD], 'BAD class matches ASCII — class build is broken'
assert not [c for c in 'plain ascii 123' if c in BAD], 'BAD class matches ASCII — class build is broken'


def scan_tofu(text):
    hits = sorted(set(ch for ch in text if ch in BAD))
    if hits:
        raise SystemExit(f'TOFU GATE FAILED: {hits} in {text[:80]!r}')
    return True


# ---------------------------------------------------------------- gate
W_POSTER = 1080
W_CARD = 1600


def build_gate():
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))

    # ---- POSTER ----
    poster = dict(
        eyebrow='AUDIO ENGINEERING · NOISE PROFILING',
        title_lines=('The Profile Is Right', 'And the Label Is Wrong'),
        subtitle='When a recorded hum still ships without a high-pass',
        callout_lines=('A hum at -55 dBFS under a -30 dBFS bed gets',
                       'recorded, then labelled white hiss: no filter'),
        url_bar='elysiatools.com/en/tools/audio-noise-profile-extractor',
    )
    checks = []
    for ln in poster['title_lines']:
        w = pil.text_w(d, ln, pil.F_TITLE)
        checks.append(('poster title', ln, w, W_POSTER))
    w = pil.text_w(d, poster['subtitle'], pil.F_MED)
    checks.append(('poster subtitle', poster['subtitle'], w, W_POSTER))
    for ln in poster['callout_lines']:
        w = pil.text_w(d, ln, pil.F_MED)
        checks.append(('poster callout', ln, w, W_POSTER - 160))
    w = pil.text_w(d, poster['url_bar'], pil.F_SMALL)
    checks.append(('poster url', poster['url_bar'], w, W_POSTER))
    for k in ('eyebrow',):
        w = pil.text_w(d, poster[k], pil.F_MED)
        checks.append((f'poster {k}', poster[k], w, W_POSTER))
    for t in poster.values():
        scan_tofu(t)

    # ---- CARD 1: the 6-branch cascade (5-tile 3+2 layout) ----
    card1 = dict(
        title='Six Branches, Five Tiles',
        subtitle='The cascade decides the label before it decides the filter',
        items=(
            ('hum-50 / hum-60', 'flatness < 0.05 AND hum found'),
            ('low-rumble', 'low-power ratio > 0.6'),
            ('white-hiss', 'flatness > 0.35'),
            ('pink', 'flatness > 0.12'),
            ('mixed / broadband', 'hum found / otherwise'),
        ),
        notes=('85 Hz high-pass', '100 Hz high-pass', 'no high-pass', 'no high-pass', 'no high-pass'),
        takeaway='Only branches 1 and 2 add a protective high-pass',
    )
    for nm, desc in card1['items']:
        w = pil.text_w(d, nm, pil.F_H3)
        checks.append((f'card1 item label', nm, w, 480))
        w = pil.text_w(d, desc, pil.F_SMALL)
        checks.append((f'card1 item body', desc, w, 480 - 60))
        scan_tofu(nm)
        scan_tofu(desc)
    for nt in card1['notes']:
        w = pil.text_w(d, nt, pil.F_MONO_SM)
        checks.append(('card1 note', nt, w, 480))
        scan_tofu(nt)
    w = pil.text_w(d, card1['title'], pil.F_H2)
    checks.append(('card1 title', card1['title'], w, W_CARD))
    w = pil.text_w(d, card1['subtitle'], pil.F_MED)
    checks.append(('card1 subtitle', card1['subtitle'], w, W_CARD))
    w = pil.text_w(d, card1['takeaway'], pil.F_MED)
    checks.append(('card1 takeaway', card1['takeaway'], w, W_CARD))
    scan_tofu(card1['title'])
    scan_tofu(card1['subtitle'])
    scan_tofu(card1['takeaway'])

    # ---- CARD 2: the sweep (2-col input/output) ----
    card2 = dict(
        title='One Sweep, Two Truths',
        subtitle='60 Hz tone over a -30 dBFS white bed, and one level produced',
        left_header='SWEEP INPUT',
        left_rows=(
            'bed: white noise, -30 dBFS',
            'tone: 60 Hz, swept level',
            'sweep: -62 to -10 dBFS',
            'tool: FFT 8192, hop 4096',
            'bands: 28 third-octave',
        ),
        right_header='WHAT THE TOOL SAID',
        right_rows=(
            '-55 dBFS: flat 0.971',
            '-55 dBFS: lowRatio 0.413',
            '-55 dBFS: label white-hiss',
            'humFrequenciesHz: [60]',
            'highpassHz: null',
        ),
        takeaway='A hum recorded in the JSON, and no filter built from it',
    )
    for r in card2['left_rows']:
        w = pil.text_w(d, r, pil.F_MONO)
        checks.append(('card2 left row', r, w, 700 - 60))
        scan_tofu(r)
    for r in card2['right_rows']:
        w = pil.text_w(d, r, pil.F_MONO)
        checks.append(('card2 right row', r, w, 700 - 60))
        scan_tofu(r)
    for k in ('title', 'subtitle', 'takeaway'):
        w = pil.text_w(d, card2[k], pil.F_MED if k != 'title' else pil.F_H2)
        checks.append((f'card2 {k}', card2[k], w, W_CARD))
        scan_tofu(card2[k])

    # ---- CARD 3: the two gaps (4-tile compact) ----
    card3 = dict(
        title='Four Limits of the Profile',
        subtitle='What the JSON cannot tell you, checked before you commit',
        tiles=(
            ('HUM, NO HP', '10 dB',
             'Hum found, no filter built',
             'label white-hiss, hp null'),
            ('NR IGNORED', '20',
             'Profile always stores nr 20',
             'apply strength wins instead'),
            ('NF CLAMPED', '-80/-20',
             'Floor clipped to -80/-20',
             'quiet and loud match'),
            ('SPEECH RISK', 'none',
             'No guard catches speech',
             'the denoiser eats it'),
        ),
        takeaway='Read the hum list and the flatness, not the label alone',
    )
    for label, count, body, sub in card3['tiles']:
        w = pil.text_w(d, label, pil.F_H3)
        checks.append(('card3 label', label, w, 360 - 60))
        for ln in pil.wrap_text(d, body, pil.F_SMALL, 360 - 60)[:2]:
            w = pil.text_w(d, ln, pil.F_SMALL)
            checks.append(('card3 body line', ln, w, 360 - 60))
        for ln in pil.wrap_text(d, sub, pil.F_MONO_SM, 360 - 60)[:2]:
            w = pil.text_w(d, ln, pil.F_MONO_SM)
            checks.append(('card3 sub line', ln, w, 360 - 60))
        scan_tofu(label)
        scan_tofu(count)
        scan_tofu(body)
        scan_tofu(sub)
    for k in ('title', 'subtitle', 'takeaway'):
        w = pil.text_w(d, card3[k], pil.F_H2 if k == 'title' else pil.F_MED)
        checks.append((f'card3 {k}', card3[k], w, W_CARD))
        scan_tofu(card3[k])

    # ---- report + fail
    bad = []
    for kind, s, w, budget in checks:
        if w > budget:
            bad.append((kind, s, w, budget))
    print(f'pre-measure gate: {len(checks)} strings checked')
    for kind, s, w, budget in checks:
        flag = 'OVER' if w > budget else 'ok'
        print(f'  [{flag:4}] {kind:<22} {w:>5} / {budget:<5} {s[:52]}')
    if bad:
        print('\nGATE FAILED — %d overflow(s)' % len(bad))
        for kind, s, w, budget in bad:
            print(f'  {kind}: {w} > {budget} :: {s!r}')
        raise SystemExit(1)
    print('\nGATE PASSED — all strings fit')

    return poster, card1, card2, card3


poster, card1, card2, card3 = build_gate()

# ---------------------------------------------------------------- render
p = os.path.join(OUT_DIR, 'poster.png')
pil.render_poster(p,
                   eyebrow=poster['eyebrow'],
                   title_lines=poster['title_lines'],
                   subtitle=poster['subtitle'],
                   callout_lines=poster['callout_lines'],
                   url_bar=poster['url_bar'])
print('poster ->', p)

c1 = os.path.join(OUT_DIR, 'card1.png')
from custom_pil_card_layouts import render_card_5tile_3plus2
render_card_5tile_3plus2(c1,
                          title=card1['title'],
                          subtitle=card1['subtitle'],
                          items=card1['items'],
                          notes=card1['notes'],
                          takeaway=card1['takeaway'])
print('card1 ->', c1)

c2 = os.path.join(OUT_DIR, 'card2.png')
render_card_input_output_2col(c2,
                               title=card2['title'],
                               subtitle=card2['subtitle'],
                               left_header=card2['left_header'],
                               left_rows=card2['left_rows'],
                               right_header=card2['right_header'],
                               right_rows=card2['right_rows'],
                               takeaway=card2['takeaway'])
print('card2 ->', c2)

c3 = os.path.join(OUT_DIR, 'card3.png')
render_card_4tile_compact(c3,
                          title=card3['title'],
                          subtitle=card3['subtitle'],
                          tiles=card3['tiles'],
                          takeaway=card3['takeaway'])
print('card3 ->', c3)

# ---------------------------------------------------------------- verify
print('\n=== asset verification ===')
for path in (p, c1, c2, c3):
    im = Image.open(path)
    print(f'  {os.path.basename(path)}: {im.size}  {os.path.getsize(path)} bytes')
    assert im.size[0] in (1080, 1600), f'{path} bad width'
    assert im.size[1] == (800 if 'poster' in path else 900), f'{path} bad height'
print('\nALL ASSETS OK')
