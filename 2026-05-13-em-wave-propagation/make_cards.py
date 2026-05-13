from PIL import Image, ImageDraw, ImageFont
import os

article_dir = '/Users/quyue/www/blog/2026-05-13-em-wave-propagation/'

def get_font(size, bold=False):
    font_path = '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def get_mono(size):
    try:
        return ImageFont.truetype('/System/Library/Fonts/Supplemental/Courier New Bold.ttf', size)
    except:
        return get_font(size)

def create_card(slug, eyebrow, label, title, quote, bullets, accent_color, bg_color, output_name):
    w, h = 1080, 900
    card = Image.new('RGB', (w, h), bg_color)
    draw = ImageDraw.Draw(card)
    
    font_eye = get_mono(11)
    draw.text((80, 80), eyebrow.upper(), fill=accent_color, font=font_eye)
    
    font_label = get_mono(10)
    draw.text((80, 108), label, fill=(85, 85, 85), font=font_label)
    
    font_title = get_font(72, bold=True)
    title_lines = title.split('\n')
    y = 160
    for line in title_lines:
        draw.text((80, y), line, fill=accent_color, font=font_title)
        y += 80
    
    font_quote = get_font(20)
    draw.text((80, y + 24), '"' + quote + '"', fill=(200, 200, 200), font=font_quote)
    
    font_bullet = get_font(17)
    y = y + 80
    for bullet in bullets:
        draw.ellipse([80, y + 6, 88, y + 14], fill=accent_color)
        draw.text((100, y), bullet, fill=(220, 220, 220), font=font_bullet)
        y += 36
    
    card.save(os.path.join(article_dir, output_name))
    print(f"Saved {output_name}")

create_card(
    slug='transverse',
    eyebrow='Core Principle',
    label='Part 01',
    title='E \u22a5 B \u22a5 k',
    quote='The electric and magnetic fields oscillate perpendicular to each other and to the direction of propagation',
    bullets=[
        'Electric field swings in one plane while magnetic field swings in the perpendicular plane',
        'Wave travels along the axis perpendicular to both — denoted k in physics notation',
        'Transverse structure makes polarization possible and distinguishes EM from sound waves'
    ],
    accent_color=(0, 180, 216),
    bg_color=(0, 13, 26),
    output_name='card-01.png'
)

create_card(
    slug='wave-equation',
    eyebrow='Field Equations',
    label='Part 02',
    title="Maxwell's\nWave Equation",
    quote='uE = uB at every point in the wave — energy is split equally between electric and magnetic fields',
    bullets=[
        'The wave equation emerges directly from Maxwell\'s four equations in vacuum',
        'Poynting vector S = E x H gives the direction and magnitude of energy flow',
        'Maxwell derived c = 1/sqrt(u0*e0) — the speed of light from first principles'
    ],
    accent_color=(0, 255, 148),
    bg_color=(0, 26, 13),
    output_name='card-02.png'
)

create_card(
    slug='spectrum',
    eyebrow='The Spectrum',
    label='Part 03',
    title='One Wave,\nMany Frequencies',
    quote='Radio waves and gamma rays are the same phenomenon — they differ only in oscillation rate',
    bullets=[
        'f * lambda = c holds for all EM waves regardless of frequency or wavelength',
        'Radio (MHz), microwaves (GHz), visible light (THz), gamma (Hz) — same physics',
        'Wireless communication exploits different parts of the spectrum for different applications'
    ],
    accent_color=(255, 107, 53),
    bg_color=(26, 13, 0),
    output_name='card-03.png'
)

print("All cards done")
