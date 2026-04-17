from PIL import Image, ImageDraw, ImageFont
import math

width, height = 1200, 630
img = Image.new('RGB', (width, height), color=(10, 14, 23))
draw = ImageDraw.Draw(img)

cx, cy = width // 2, height // 2 - 30

# Background circle (the "denominator")
draw.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], fill=(20, 25, 40))

# Draw the 4 quadrants with probability labels
# True Positive (sick + positive) - small blue section
tp_cx, tp_cy = cx - 80, cy - 80
draw.ellipse([tp_cx - 90, tp_cy - 90, tp_cx + 90, tp_cy + 90], fill=(0, 100, 200))
draw.text((tp_cx - 40, tp_cy - 8), "TP", fill=(255, 255, 255))

# False Negative (sick + negative) - medium blue section  
fn_cx, fn_cy = cx + 80, cy - 80
draw.ellipse([fn_cx - 90, fn_cy - 90, fn_cx + 90, fn_cy + 90], fill=(0, 50, 120))
draw.text((fn_cx - 35, fn_cy - 8), "FN", fill=(200, 200, 200))

# False Positive (healthy + positive) - LARGE red section
fp_cx, fp_cy = cx - 80, cy + 80
draw.ellipse([fp_cx - 120, fp_cy - 120, fp_cx + 120, fp_cy + 120], fill=(180, 40, 40))
draw.text((fp_cx - 40, fp_cy - 8), "FP", fill=(255, 255, 255))

# True Negative (healthy + negative) - medium green section
tn_cx, tn_cy = cx + 80, cy + 80
draw.ellipse([tn_cx - 90, tn_cy - 90, tn_cx + 90, tn_cy + 90], fill=(0, 140, 70))
draw.text((tn_cx - 40, tn_cy - 8), "TN", fill=(255, 255, 255))

# Formula display
formula_y = cy + 200
draw.text((cx - 200, formula_y), "P(Disease|+) = TP / (TP + FP)", fill=(100, 200, 255))

# Title
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    font_tiny = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
except:
    font_large = ImageFont.load_default()
    font_small = font_large
    font_tiny = font_large

title = "Why a Positive Test Doesn't Mean What You Think"
bbox = draw.textbbox((0, 0), title, font=font_large)
title_width = bbox[2] - bbox[0]
draw.text((width//2 - title_width//2, 60), title, font=font_large, fill=(255, 255, 255))

subtitle = "Bayes' Theorem & The False Positive Paradox"
bbox = draw.textbbox((0, 0), subtitle, font=font_small)
sub_width = bbox[2] - bbox[0]
draw.text((width//2 - sub_width//2, 115), subtitle, font=font_small, fill=(100, 180, 255))

# Bottom attribution
bbox = draw.textbbox((0, 0), "ElysiaTools", font=font_tiny)
ew = bbox[2] - bbox[0]
draw.text((width//2 - ew//2, height - 50), "ElysiaTools", font=font_tiny, fill=(80, 100, 140))

img.save("poster.png", "PNG")
print("Poster created successfully")
