# 7 Free Design Tools for Photo Editing That Run in Your Browser

Your next design project probably involves three or four paid tools. But 252 of them are free — and they run in a browser tab.

Most developers know ElysiaTools as a utility collection: JSON validators, regex testers, date calculators. But the **Design** category holds 252 image processing tools that can replace a surprising amount of what Photoshop or Figma charges for. I've been digging through the full list, and seven of them stand out for day-to-day photo editing and effects work.

Here's what actually works:

---

## 1. Image Negative Effect — Instant Film Inversion

This one's straightforward: it inverts every color in your image. Upload a JPEG, pick a mode, download the result. But "straightforward" undersells it — there are **five distinct modes**:

- **Standard Negative**: Classic photo negative look
- **Full Negative (with alpha)**: Preserves transparency in PNGs
- **Color Only**: Inverts color while keeping alpha intact
- **Partial Negative**: Subtle inversion for a ghostly, muted effect
- **Artistic Negative**: Inverts + boosts contrast and saturation for a punchy, stylized look

The artistic mode is the surprise here. It applies negative inversion, then cranks brightness to 1.1x and saturation to 1.2x, then applies a 1.3x contrast linear transform. The result looks closer to cross-processed film than a clinical negative — usable for album art, social posts, or design mockups.

**Best for**: Quick film-negative aesthetics, photo manipulation, creating contrast in flat images.
[Try it →](https://elysiatools.com/en/tools/image-negative)

---

## 2. Image Edge Detection — 7 Algorithms in One Tool

This one surprised me with its depth. It implements **seven different edge detection algorithms** — most tools give you one or two:

- **Sobel**: The standard. Fast, reliable, good all-around results.
- **Prewitt**: Similar to Sobel but with different kernel weights — slightly less edge emphasis.
- **Laplacian**: Second-derivative detector — picks up fine detail but sensitive to noise.
- **Canny**: Multi-step process (blur → gradient → non-maximum suppression → hysteresis thresholding). The gold standard for clean, thin edges.
- **Roberts Cross**: Diagonal gradient operator — good for high-frequency detail.
- **Scharr**: Better than Sobel at detecting diagonal edges — rotational symmetry is improved.
- **Gradient Magnitude**: Simple directional gradient.

Beyond algorithm choice, you get threshold controls (0–255), aperture size (3–15), output modes (edges-only, colored direction map, or magnitude+thickness), custom edge colors (any hex or RGB), and a side-by-side original comparison view.

**Best for**: UI design, technical illustration overlays, extracting outlines for masking.
[Try it →](https://elysiatools.com/en/tools/image-edge-detect)

---

## 3. Image Gradient Overlay — Linear, Radial, and Diamond

Most gradient tools give you one gradient type. This one gives you three with **12 blend modes** to combine them:

**Types:**
- **Linear**: Directional gradient at any angle (0–360°)
- **Radial**: Center-out gradient
- **Diamond**: Elliptical gradient starting from center

**Blend modes**: Normal, Multiply, Screen, Overlay, Darken, Lighten, Color Dodge, Color Burn, Hard Light, Soft Light, Difference, Exclusion

Each mode fundamentally changes how the gradient interacts with your image. Multiply darkens; Screen lightens; Overlay adds contrast without blowing out highlights; Soft Light is subtle and photographic. If you've used blend modes in Photoshop or Figma, you know how much creative range this unlocks.

Opacity is adjustable from 0 to 1 in 0.1 steps. Output as PNG (recommended for transparency), JPEG, WebP, or AVIF.

**Best for**: Adding mood lighting, vintage overlays, creating depth on flat UI mockups.
[Try it →](https://elysiatools.com/en/tools/image-add-gradient)

---

## 4. High Pass Filter — Detail Enhancement Without the Guesswork

High-pass filtering is a professional retouching technique. The idea: subtract a blurred version of your image from the original, leaving only the high-frequency detail. The result is a sharpening/enhancement effect that works without the halo artifacts of naive unsharp masking.

This tool implements it with two parameters:

- **Radius** (0.1–20.0): How large the blur kernel is. Small radius isolates fine detail like skin texture; large radius affects broader structural elements.
- **Strength** (0.1–3.0): How aggressively to boost the extracted details.

Then choose a blend mode for combining the enhanced details with your original: Overlay (recommended), Soft Light, Hard Light, Screen, or Multiply. Or output the details-only result — useful as a texture overlay for another project.

In other words: the same technique that professional portrait photographers use to smooth skin while keeping detail crisp — no Photoshop subscription required.

**Best for**: Portrait retouching, architectural photography, making flat images pop without over-sharpening noise.
[Try it →](https://elysiatools.com/en/tools/image-high-pass)

---

## 5. Image Trim — Auto-Detect and Remove Borders

This isn't a crop tool. It's an **auto-border remover** that detects and cuts away unwanted edges:

- **Auto-detect**: Scans the image and removes any consistent border color
- **Transparent areas**: Strips empty alpha space
- **White borders**: Common with scanned documents or export artifacts
- **Black borders**: Common with photo prints
- **Custom color**: Specify exactly what color to treat as background

The threshold slider (1–255) controls sensitivity — lower values aggressively trim, higher values only remove obvious borders. The tool reports how many pixels were removed and the percentage size savings, so you can see exactly what was cut.

**Best for**: Cleaning up scanned documents, removing white/black margins from exported graphics, trimming transparent padding from PNGs.
[Try it →](https://elysiatools.com/en/tools/image-trim)

---

## 6. Image Normalize — Histogram Stretching for Better Contrast

Ever have a photo that looks flat and gray, even though you can see detail should be there? That's a contrast problem, and this tool solves it with **histogram normalization**.

The algorithm stretches the image's intensity range to use the full 0–255 spectrum. By default it ignores the darkest 1% and brightest 1% of pixels (to avoid clipping outliers), then remaps everything between those bounds across the full range.

If auto-contrast mode is too blunt, you can set custom percentiles — lower bound (0.1–10%) and upper bound (90–99.9%). This preserves more shadow or highlight detail in high-dynamic-range scenes.

The effect on a flat, low-contrast photo is dramatic: colors saturate naturally, shadows gain visible detail, highlights stop looking washed out.

**Best for**: Fixing underexposed photos, improving scanned images, preparing photos for print or presentation.
[Try it →](https://elysiatools.com/en/tools/image-normalize)

---

## 7. Image Multiply Blend — Create Real Shadow Layers

Multiply is one of the fundamental blend modes in design — it darkens by multiplying pixel values, creating natural shadow effects without the artificial look of a dark overlay. This tool applies it between **two images of your choice**.

Use cases that actually come up:

- **Textured shadows**: Multiply a noise or texture image over your design to add grain/shadow
- **Double exposure**: Multiply a portrait with a landscape for that classic analog photography effect
- **Toning**: Multiply a color overlay to tint an image without the harshness of opacity blending

The tool auto-resizes both images to the same dimensions, supports opacity control on the overlay (0–1), and outputs PNG to preserve transparency.

**Best for**: Creating drop shadows, double exposure effects, texture overlays, design compositing.
[Try it →](https://elysiatools.com/en/tools/image-multiply)

---

## What You're Not Replacing

These seven tools won't replace Photoshop for complex masking, layer compositing, or color grading. But for the **quick adjustments and effects** that eat up half your time — negative effect for an aesthetic, edge detection for a UI mockup, trimming the white border off a scan — they're doing the job without a browser tab asking you to sign up.

All 252 Design tools are at [elysiatools.com/en/tools](https://elysiatools.com/en/tools) with no account required.
