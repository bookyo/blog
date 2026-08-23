import sys
sys.path.insert(0, '/Users/quyue/.hermes/skills/wordpress-rest-api-publishing/templates')

from pil_poster_and_cards_network_theme import render_poster, render_card_5tile, render_card_audit
from render_card_4tile_compact import render_card_4tile_compact
from render_card_audit_6row import render_card_audit_6row
from custom_pil_card_layouts import render_card_input_output_2col
from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = '/Users/quyue/www/blog/2026-08-23-image-to-spectrogram-audio'

# ====== Poster ======
poster_path = f'{ASSET_DIR}/poster.png'

# Pre-measure subtitle against W-40 = 1040 to avoid clip (WP 5683/6109/6129/6149/6171)
def measure_w(s, font):
    bb = ImageDraw.Draw(Image.new('RGB', (10, 10))).textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]

# Match the canonical poster font sizes by inspection
from pil_poster_and_cards_network_theme import F_MED
sub = "Bitmap to time-frequency grid audio. Ships with verification spectrogram."
w = measure_w(sub, F_MED)
print(f'subtitle width: {w} (limit 1040)')
if w > 1040:
    sub = "Bitmap to time-frequency audio with verification spectrogram."
    print(f'shortened subtitle width: {measure_w(sub, F_MED)}')
if measure_w(sub, F_MED) > 1040:
    sub = "Bitmap to time-frequency audio. Verification spectrogram included."
    print(f'shortened2: {measure_w(sub, F_MED)}')

render_poster(
    poster_path,
    eyebrow='MEDIA / SONIFICATION',
    title_lines=('Image To', 'Spectrogram Audio'),
    subtitle=sub,
    callout_lines=('Width is time, height is frequency bins,',
                   'brightness is amplitude. Verify with the preview.'),
    url_bar='elysiatools.com/en/tools/image-to-spectrogram-audio',
)

# ====== Card 1: 5-tile — Mapping Rules (anchor H2 #1) ======
card1_path = f'{ASSET_DIR}/card1.png'
render_card_5tile(
    card1_path,
    title='Five Mapping Rules That Decide The Reconstruction',
    subtitle='Width / height / brightness / orientation / row direction',
    items=(
        ('01', 'Width = Time', 'Pixel columns become time slices across the audio duration'),
        ('02', 'Height = Freq Bins', 'Pixel rows map to frequency bins between floor and ceiling'),
        ('03', 'Brightness = Amp', 'Bright pixels drive louder partials; black stays near silence'),
        ('04', 'Top = High Freq', 'Default puts high frequencies at the top row (toggle to invert)'),
        ('05', 'Resize Mode', 'Stretch, contain with padding, or cover and crop the source'),
    ),
    notes=(
        'columns -> time',
        'rows -> bins',
        'luma -> amplitude',
        'orientation toggle',
        'stretch / contain / cover',
    ),
    takeaway='Pin the three axes (time, frequency, amplitude) once and every export round-trips cleanly.',
    highlight_last=True,
)

# ====== Card 2: input/output 2-col worked example (anchor H2 #6) ======
card2_path = f'{ASSET_DIR}/card2.png'
render_card_input_output_2col(
    card2_path,
    title='A 6-Second FLAC From A Single Glyph',
    subtitle='Log spacing + Viridis verification + threshold at 0.08',
    left_header='Input Bitmap',
    left_rows=(
        'Source: 480 x 160 PNG',
        'Background: solid black',
        'Subject: single letter glyph',
        'Floor: 120 Hz',
        'Ceiling: 14,000 Hz',
        'Scale: logarithmic',
    ),
    right_header='Output Audio',
    right_rows=(
        'Format: FLAC (lossless)',
        'Sample rate: 48 kHz',
        'Duration: 6.0 seconds',
        'Time slices: 720',
        'Freq bins: 160',
        'Palette: Viridis',
    ),
    takeaway='Sharper letters, denser upper detail, and the verification spectrogram is the proof.',
)

# ====== Card 3: 4-tile audit (anchor H2 #8 — Three Checks) ======
card3_path = f'{ASSET_DIR}/card3.png'
# Use render_card_audit with 3 rows? No, audit has fixed structure. Use 4-tile compact instead.
render_card_4tile_compact(
    card3_path,
    title='Three Checks Before You Ship The Export',
    subtitle='Read the verification spectrogram with these three questions',
    tiles=(
        ('Check 1', 'Stray', 'lines', 'Scan for horizontal lines that are not in the source — too-low threshold leaks ambient noise.'),
        ('Check 2', 'Corner', 'agrees', 'Top-right of source matches top-right of spectrogram? Toggle flips when it does not.'),
        ('Check 3', 'Listen', 'half speed', 'Play at half speed for clicks — a leading click means a non-zero leftmost pixel.'),
        ('Result', 'Verified', 'round-trip', 'If all three checks pass the audio and the source agree on the same image.'),
    ),
    takeaway='Verification first, export second. The spectrogram preview is the contract.',
)

print('All 4 assets rendered.')