from PIL import Image, ImageDraw, ImageFont
import math, random

width, height = 1200, 630
img = Image.new('RGB', (width, height), color=(10, 14, 23))
draw = ImageDraw.Draw(img)

cx, cy = width // 2, height // 2 - 20

# Draw phase circle rings
for i in range(60):
    angle = 2 * math.pi * i / 60
    x1 = cx + int(180 * math.cos(angle))
    y1 = cy + int(180 * math.sin(angle))
    x2 = cx + int(240 * math.cos(angle))
    y2 = cy + int(240 * math.sin(angle))
    draw.line([(x1, y1), (x2, y2)], fill=(30, 50, 80), width=1)

# Synchronized cluster (blue)
random.seed(42)
for i in range(25):
    angle = 0.3 + random.uniform(-0.15, 0.15)
    r = 100 + random.uniform(-20, 20)
    x = cx + int(r * math.cos(angle))
    y = cy + int(r * math.sin(angle))
    draw.ellipse([x-5, y-5, x+5, y+5], fill=(0, 150, 255))

# Scattered chaotic oscillators (red/orange)
for i in range(35):
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(140, 220)
    x = cx + int(r * math.cos(angle))
    y = cy + int(r * math.sin(angle))
    draw.ellipse([x-4, y-4, x+4, y+4], fill=(255, 100, 80))

try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    font_tiny = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
except:
    font_large = ImageFont.load_default()
    font_small = font_large
    font_tiny = font_large

title = "The Mystery of How Nature Syncs Without a Conductor"
subtitle = "Kuramoto Synchronization Model"

bbox = draw.textbbox((0, 0), title, font=font_large)
title_width = bbox[2] - bbox[0]
draw.text((width//2 - title_width//2, height - 160), title, font=font_large, fill=(255, 255, 255))

bbox = draw.textbbox((0, 0), subtitle, font=font_small)
sub_width = bbox[2] - bbox[0]
draw.text((width//2 - sub_width//2, height - 110), subtitle, font=font_small, fill=(0, 180, 255))

bbox = draw.textbbox((0, 0), "ElysiaTools", font=font_tiny)
ew = bbox[2] - bbox[0]
draw.text((width//2 - ew//2, height - 50), "ElysiaTools", font=font_tiny, fill=(100, 120, 150))

img.save("poster.png", "PNG")
print("Poster created successfully")
