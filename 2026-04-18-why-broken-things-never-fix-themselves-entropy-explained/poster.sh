#!/bin/bash
# Create entropy poster

# Step 1: Create background gradient
convert -size 800x450 gradient:"#1a1a3a"-"#0a0a1a" canvas.png

# Step 2: Left box (ordered particles - low entropy)
convert canvas.png \
  -fill none -stroke "#4fc3f7" -strokewidth 2 \
  -draw "rectangle 80,80 320,370" \
  left_box.png

# Step 3: Draw ordered particles (6x5 grid) in left box
convert left_box.png \
  -fill "#4fc3f7" -stroke none \
  -draw "circle 120,130 120,115" \
  -draw "circle 160,130 160,115" \
  -draw "circle 200,130 200,115" \
  -draw "circle 240,130 240,115" \
  -draw "circle 280,130 280,115" \
  -draw "circle 120,180 120,165" \
  -draw "circle 160,180 160,165" \
  -draw "circle 200,180 200,165" \
  -draw "circle 240,180 240,165" \
  -draw "circle 280,180 280,165" \
  -draw "circle 120,230 120,215" \
  -draw "circle 160,230 160,215" \
  -draw "circle 200,230 200,215" \
  -draw "circle 240,230 240,215" \
  -draw "circle 280,230 280,215" \
  -draw "circle 120,280 120,265" \
  -draw "circle 160,280 160,265" \
  -draw "circle 200,280 200,265" \
  -draw "circle 240,280 240,265" \
  -draw "circle 280,280 280,265" \
  -draw "circle 120,330 120,315" \
  -draw "circle 160,330 160,315" \
  -draw "circle 200,330 200,315" \
  -draw "circle 240,330 240,315" \
  -draw "circle 280,330 280,315" \
  particles_ordered.png

# Step 4: Right box (scattered - high entropy) with random dots
convert -size 800x450 xc:"#1a1a3a" \
  -fill "rgba(79,195,247,0.1)" -stroke "#4fc3f7" -strokewidth 2 \
  -draw "rectangle 80,80 320,370" \
  left_low.png

convert -size 800x450 xc:"#1a1a3a" \
  -fill "rgba(255,107,107,0.1)" -stroke "#ff6b6b" -strokewidth 2 \
  -draw "rectangle 480,80 720,370" \
  right_box.png

# Combine into final poster
convert -size 800x450 gradient:"#1a1a3a"-"#0a0a1a" \
  \( -fill none -stroke "#4fc3f7" -strokewidth 2 -draw "rectangle 80,80 320,370" \) \
  \( -fill none -stroke "#ff6b6b" -strokewidth 2 -draw "rectangle 480,80 720,370" \) \
  -fill "#4fc3f7" \
  -draw "circle 120,130 120,115" -draw "circle 160,130 160,115" \
  -draw "circle 200,130 200,115" -draw "circle 240,130 240,115" \
  -draw "circle 280,130 280,115" \
  -draw "circle 120,180 120,165" -draw "circle 160,180 160,165" \
  -draw "circle 200,180 200,165" -draw "circle 240,180 240,165" \
  -draw "circle 280,180 280,165" \
  -draw "circle 120,230 120,215" -draw "circle 160,230 160,215" \
  -draw "circle 200,230 200,215" -draw "circle 240,230 240,215" \
  -draw "circle 280,230 280,215" \
  -draw "circle 120,280 120,265" -draw "circle 160,280 160,265" \
  -draw "circle 200,280 200,265" -draw "circle 240,280 240,265" \
  -draw "circle 280,280 280,265" \
  -draw "circle 120,330 120,315" -draw "circle 160,330 160,315" \
  -draw "circle 200,330 200,315" -draw "circle 240,330 240,315" \
  -draw "circle 280,330 280,315" \
  poster_temp.png

echo "Basic elements created"
