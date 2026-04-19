#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

ARTICLE_DIR = "/Users/quyue/www/blog/2026-04-19-double-slit-quantum-trajectory-visualization"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_gradient_bg(draw, width, height, color1, color2, direction='vertical'):
    """Draw a gradient background"""
    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

def create_poster():
    """Create featured image poster 1200x630"""
    width, height = 1200, 630
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Deep purple to dark blue gradient (quantum theme)
    draw_gradient_bg(draw, width, height, hex_to_rgb('0F0C29'), hex_to_rgb('302B63'), hex_to_rgb('24243E'))
    
    # Accent elements - wave interference pattern circles
    accent_color = (100, 180, 255)
    for i, (x, y, r) in enumerate([(150, 100, 40), (300, 200, 25), (900, 150, 35), (1050, 400, 45), (700, 500, 30), (200, 450, 20)]):
        draw.ellipse([x-r, y-r, x+r, y+r], fill=accent_color + (100,))
    
    # Double slit pattern visualization (simplified)
    slit_color = (150, 200, 255)
    # Draw two slits
    draw.rectangle([(500, 100), (540, 130)], fill=slit_color)
    draw.rectangle([(660, 100), (700, 130)], fill=slit_color)
    # Draw wave lines emanating
    for i in range(8):
        offset = i * 15
        draw.arc([400-offset, 200-offset, 800+offset, 400+offset], 0, 180, fill=(100, 180, 255, 150), width=2)
    
    # Main title
    title = "Double Slit Quantum Trajectory"
    subtitle = "Watch Particles Take Every Path at Once"
    
    # Try to use a font, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw title text with shadow
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x + 3, 400 + 3), title, font=title_font, fill=(0, 0, 0, 128))
    draw.text((title_x, 400), title, font=title_font, fill=(255, 255, 255))
    
    # Draw subtitle
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_width = bbox[2] - bbox[0]
    sub_x = (width - sub_width) // 2
    draw.text((sub_x + 2, 470 + 2), subtitle, font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((sub_x, 470), subtitle, font=subtitle_font, fill=(180, 220, 255))
    
    # Bottom tagline
    tagline = "Interactive Visualization of Quantum Probability Current"
    bbox = draw.textbbox((0, 0), tagline, font=subtitle_font)
    tag_width = bbox[2] - bbox[0]
    draw.text(((width - tag_width) // 2, 560), tagline, font=subtitle_font, fill=(150, 200, 255))
    
    # Save
    img.save(os.path.join(ARTICLE_DIR, "poster.png"))
    print("Created poster.png")

def create_highlight_card(filename, title, body, accent_hex='4A90D9'):
    """Create a highlight card 1200x675"""
    width, height = 1200, 675
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Gradient background - quantum dark theme
    draw_gradient_bg(draw, width, height, hex_to_rgb('0d0d1a'), hex_to_rgb('1a1a2e'))
    
    # Accent bar at top
    accent = hex_to_rgb(accent_hex)
    draw.rectangle([(0, 0), (width, 8)], fill=accent)
    
    # Decorative elements - interference circles
    for i, (x, y, r, c) in enumerate([(100, 550, 60, (80, 160, 255, 50)), (1100, 100, 80, (100, 200, 255, 40)), (600, 600, 40, (90, 180, 255, 60))]):
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)
    
    # Title
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
        body_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Draw title with accent color
    draw.text((80, 80), title, font=title_font, fill=accent)
    
    # Draw body text (word wrap)
    words = body.split()
    lines = []
    current_line = []
    max_width = width - 160
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=body_font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y_offset = 180
    for line in lines[:8]:  # Limit to 8 lines
        draw.text((80, y_offset), line, font=body_font, fill=(220, 220, 230))
        y_offset += 40
    
    # Save
    img.save(os.path.join(ARTICLE_DIR, filename))
    print(f"Created {filename}")

if __name__ == "__main__":
    # Create poster
    create_poster()
    
    # Create highlight cards
    create_highlight_card(
        "highlight-1-opening-hook.png",
        "The Double Slit Paradox",
        "Fire individual electrons through two slits and they form an interference pattern. The pattern requires a wave passing through both slits. But you're firing particles. Single, discrete, countable particles. This visualization doesn't resolve that paradox — but it lets you watch the probability current that guides each particle to its destination."
    )
    
    create_highlight_card(
        "highlight-2-trajectories.png",
        "See Wave Function and Paths Together",
        "Most visualizations show the wave function OR the particle trajectories. This one shows both overlaid. The wave passes through both slits and interferes. The particle trajectories follow the resulting probability current. Watch the particle at any moment and it's in exactly one location — but the flow field guiding it has structure that only makes sense as a wave phenomenon."
    )
    
    create_highlight_card(
        "highlight-3-probability-current.png",
        "Probability Current Reveals Hidden Structure",
        "The probability current J = (ℏ/m)·Im[ψ*∇ψ] is a vector field rendered as a flow field. Arrows show direction and magnitude of probability flow. Particles never cross nodal lines — points where the wave function is exactly zero. The flow field never points to the dark bands on the detector. That's why particles never land there."
    )
    
    create_highlight_card(
        "highlight-4-closing.png",
        "Understanding Starts with Watching",
        "The double-slit experiment has been performed with electrons, atoms, molecules, and even buckminsterfullerene spheres. The interference pattern persists. Watch long enough and the wave-like pattern emerges from particle-like events. That's not a paradox to solve — it's a phenomenon to understand. Understanding starts with watching."
    )
    
    print("All images created successfully!")
