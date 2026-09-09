<strong>Five pixels of #1d4ed8 look "royalblue" to the eye and "mediumblue" to RGB math.</strong> The CSS Color Name Resolver closes that gap by ranking all 148 named CSS keywords against your hex input with perceptual distance metrics — CIEDE2000, CIE94, CIE76, and Euclidean RGB — and showing you the family trail of every near-relative in the same color block.

You can paste any `#rgb`, `#rrggbb`, or one of the 148 keywords. The tool returns the closest name with a ΔE score per metric, the second match, and the whole blue/red/green/etc. cluster around your anchor so you can see why "the spreadsheet" and the eye disagree. Use the [CSS Color Name Resolver](https://elysiatools.com/en/tools/css-color-name-resolver) when picking token names, when reviewing hex literals in PR diffs, and when deciding whether two near-identical swatches in a Figma frame are "the same color" or different enough to matter.

## Why Hex Math And The Human Eye Disagree On The Same Five Pixels

`#1d4ed8` is `R=29 G=78 B=216`. `mediumblue` is `R=0 G=0 B=205`. The Euclidean RGB distance between them is `sqrt((29-0)^2 + (78-0)^2 + (216-205)^2) = sqrt(841 + 6084 + 121) = sqrt(7046) = 83.94`. To the spreadsheet, `#1d4ed8` and `mediumblue` are 84 raw RGB units apart. To your eye, sitting at the same screen brightness, the two swatches read as "the same blue" — both look like a slightly-oversaturated royal-leaning blue, and the difference feels cosmetic, not categorical.

That gap — 84 on paper, "same color" in practice — is what perceptual color science exists to fix. The eye does not sum R+G+B like a spreadsheet. It weights luminance (the L* channel in CIELAB) far more than chroma, and it treats the blue-violet axis as a single dimension rather than two independent numbers. `royalblue` (`#4169e1`) and `mediumblue` (`#0000cd`) sit at almost identical perceived lightness because their L* values are 33.96 and 20.79 — close enough that the eye lumps them into the same color band. The raw RGB delta is 84, but the perceptual delta is closer to 8-12 ΔE.

This is the problem every design-token PR review runs into. You write `--brand: #1d4ed8`. A teammate pastes the swatch into a "name that color" tool and gets back "mediumblue" because the tool uses Euclidean RGB. They ask you to rename the token to `--brand-mediumblue`. You reject the change because `--brand-royalblue` reads more accurately to your eye. The disagreement is not about taste — it's about which distance metric each of you used. The Resolver shows all four metrics side by side so the conversation stops being about preference and starts being about which metric you actually want your design system to follow.

The same gap shows up in contrast-checker audits. WCAG defines contrast as `(L1 + 0.05) / (L2 + 0.05)` where L is relative luminance. Two hex values that score 4.8:1 in WCAG can have a raw RGB delta of 12 or 200 depending on which channel they differ in — luminance-weighted math and RGB math are not interchangeable. The [Color Contrast Checker](https://elysiatools.com/en/tools/color-contrast-checker) shares the same underlying L* math so the numbers reconcile cleanly.

## What The Resolver Returns For A Single Hex Input

You paste `#1d4ed8`. The Resolver returns:

- The closest name: `royalblue` (ΔE 6.2 under CIEDE2000, 84.0 under Euclidean RGB — same input, two answers)
- The second match: `mediumblue` at ΔE 12.4 CIEDE2000 versus 84.0 raw RGB (the rankings diverge here — RGB thinks mediumblue is closer than royalblue, CIEDE2000 flips it)
- A family trail of every named CSS color whose ΔE is under 35 from your anchor
- All four metrics side by side for the top 8 matches so you can see exactly where RGB math lies

The key insight is that the **rankings** follow CIEDE2000, not raw RGB. The classic trap: `crimson` (`#dc143c`) and `mediumvioletred` (`#c71585`) are 50.7 RGB units apart, but CIEDE2000 puts them at ΔE 23.1 — different colors to the eye. Conversely, `dodgerblue` (`#1e90ff`) and `cornflowerblue` (`#6495ed`) are 79.5 RGB units apart but only ΔE 7.6 — same color band to the eye. RGB math is wrong about both pairs; CIEDE2000 is right about both.

The same family-trails view also works in reverse: paste the named color and the Resolver tells you the hex that's perceptually closest to it. `royalblue` → `#4169e1` (exact match, ΔE 0), `dodgerblue` → `#1e90ff`, `mediumseagreen` → `#3cb371`. The round-trip is lossless for exact keyword matches, and the trail tells you which near-neighbor named colors are perceptually adjacent — useful when picking a token name from a hex.

## Four Distance Metrics, One Ranking — When CIEDE2000 Beats CIE76

The Resolver computes four distances per pair:

1. **RGB Euclidean** — `sqrt((Δr)^2 + (Δg)^2 + (Δb)^2)`. Fast, wrong for almost every perceptual question.
2. **CIE76** — `sqrt((ΔL*)^2 + (Δa*)^2 + (Δb*)^2)`. First perceptual metric (1976), ignores chroma/hue weighting.
3. **CIE94** — weighted CIE76 (1994), used in textile and print color matching, weights chroma less than lightness.
4. **CIEDE2000** — current standard (2001), accounts for the blue-region distortion, hue rotation, and chroma compression. Matches human perception within ~1 ΔE for 95% of pairs.

For most design-token work, CIEDE2000 is the metric you want. The cases where RGB wins are vanishingly narrow — adjacent shades in the same named block (e.g. picking between `darkblue` and `midnightblue` for a dark-mode background) where the differences are sub-perceptual anyway. For everything else, RGB is a liability: it makes near-identical colors look far apart (the royalblue/mediumblue case), and far-apart colors look close (the dodgerblue/cornflowerblue case).

A practical rule: if a name-vs-hex lookup gives you a different name under RGB than under CIEDE2000, trust CIEDE2000. The eye-side math has had 25 years of peer review and refinement; the RGB math has none.

## The 148 Named Colors And Why Browsers Honor A Subset

CSS Color Module Level 4 specifies 148 named colors. Of those, 17 are `transparent`, `currentcolor`, or system colors that resolve at render time (`Canvas`, `CanvasText`, `LinkText`, etc.). The remaining 131 are stable, cross-browser hex-equivalent keywords — `aliceblue`, `antiquewhite`, `aqua`, ..., `yellowgreen`. They are NOT the X11 color set: the X11 list has 138 names with duplicates and platform-dependent shades, and CSS explicitly removed `darkgray`/`darkgrey` aliasing, `cyan`/`aqua` ambiguity, and a handful of macOS-specific greys.

Browsers honor all 148 keywords, but only the 131 stable ones are safe to ship as tokens. `transparent` and `currentcolor` are reserved words; the system colors (`Canvas`, `ButtonFace`) work in modern browsers but are not portable to older Safari or any non-browser CSS context (email templates, PDF renderers, design tools' export). The Resolver distinguishes them by accepting any of the 148 in the input box, but the family trails highlight only stable names by default.

If your token system uses `--surface: Canvas;` it works in Chrome, Firefox, Safari, Edge — but the rendered color depends on the user's OS theme, so two screenshots from different machines can disagree. If you swap `Canvas` for `white`, you get a portable, predictable surface color but lose the dark-mode hand-off. The Resolver helps you see exactly which named keyword matches a hex like `#fafafa` — and `whitesmoke` (`#f5f5f5`) is closer than `white` (`#ffffff`) in CIEDE2000, even though the spreadsheet says `white` is exact.

## Color Family Trails: How Related Names Cluster Around One Anchor

When you paste `#1d4ed8`, the family trail shows every named CSS color whose ΔE is under 35, sorted by ΔE ascending:

- `royalblue` `#4169e1` ΔE 6.2
- `dodgerblue` `#1e90ff` ΔE 8.3
- `mediumblue` `#0000cd` ΔE 12.4
- `cornflowerblue` `#6495ed` ΔE 14.8
- `blue` `#0000ff` ΔE 18.1
- `darkblue` `#00008b` ΔE 24.7
- `midnightblue` `#191970` ΔE 31.1

These are not random neighbors — they are the 7 named "blues" in the CSS palette, clustered in luminance order. Reading the trail tells you "I picked a saturated mid-tone blue, the CSS palette has 6 other blues within perceptual reach, and naming this `royalblue` is closest but `dodgerblue` is in the same color band." That decision changes how the token reads in code review: `--brand-blue` is too generic, `--brand-royalblue` is the closest match, and `--brand-blue-600` (a Tailwind-style scale) is fine if you commit to the whole scale.

The trails are useful for picking between near-identical shades, too. `seashell` `#fff5ee` and `linen` `#faf0e6` are both off-whites with a warm cast; the trail shows `moccasin`, `papayawhip`, `oldlace`, and `antiquewhite` as the next four neighbors. Reading the trail lets you pick the name that actually matches your intent (`seashell` for a pinkish white, `linen` for a beige white, `antiquewhite` for a cream) without cycling through hex values one at a time.

The Resolver also reverse-lookups: paste the name and get the hex, or paste any of the 148 keywords to confirm the Resolver recognizes it as a CSS color (vs a near-miss hex). Open the [CSS Color Name Resolver](https://elysiatools.com/en/tools/css-color-name-resolver) and try `rebeccapurple` — a CSS keyword added in CSS Color Module Level 4 in honor of Rebecca Meyer, the daughter of CSS Working Group member Eric Meyer. Hex `#663399`, ΔE 0 from the named keyword.

## Round-Trip Loss When You Map Hex → Name → Hex

Take a screenshot-pixel hex like `#3b6fbe`. The Resolver names it `steelblue` (`#4682b4`). You commit the token as `--accent: steelblue;`. Six months later someone reads the CSS, sees `steelblue`, converts it to `#4682b4`, and the rendered color is 16 ΔE away from the original `#3b6fbe`. Round-trip loss.

The [CSS Color Name Resolver](https://elysiatools.com/en/tools/css-color-name-resolver) mitigates this in two ways. First, the family trail shows the original hex, the named color, and the named color's hex together, so the loss is visible — you can see that `steelblue` is "close to but not exactly" your `#3b6fbe`. Second, the 4-metric display lets you see which metric is saying "round-trip is fine" and which is saying "you're losing 12 ΔE" — RGB thinks the round-trip is identical if both hex values are byte-equal after the swap; CIEDE2000 catches the loss.

For lossless round-tripping, pick a hex first and name the token after the perceptual family (`--blue-600`, `--blue-700`) instead of after a CSS keyword. Tailwind's scale (`blue-500` = `#3b82f6`, `blue-600` = `#2563eb`, `blue-700` = `#1d4ed8`) maps cleanly to a CSS palette family, and the hex stays authoritative. The Resolver helps you find the family name that matches your hex; once you have that, you can use either the family name (`--brand-blue-600`) or the hex (`--brand: #1d4ed8`) and the loss is contained.

## Reverse Lookup: Finding Every Hex Close To A Given Name

The reverse direction is useful for cleaning up existing tokens. Paste `darkblue` and the Resolver shows every hex in the CSS palette within 5 ΔE of `#00008b`: only `midnightblue` at ΔE 9.7 and `mediumblue` at ΔE 16.2. The "near-miss hex" view lets you see which tokens in your design system are perceptually redundant with `darkblue` — useful for consolidation, dangerous if you delete a token that's actually a distinct brand color.

For accessibility audits, the reverse view surfaces which named colors are "the same to the eye but different on paper." A token system with `--gray-100: #f5f5f5`, `--gray-200: #eeeeee`, and `--gray-300: #e0e0e0` is fine because the gaps are 8-12 ΔE per step. A token system with `--gray-100: #fafafa`, `--gray-200: #f8f8f8`, and `--gray-300: #f5f5f5` is broken — the gaps are 2-4 ΔE, sub-perceptual, and you have three tokens for what the eye sees as one color. The Resolver makes these hidden duplicates visible.

The Resolver is one tool in the design system. Pair it with the [Hex to HSL Converter](https://elysiatools.com/en/tools/hex-to-hsl-converter) for format translation. The [Color Code Samples](https://elysiatools.com/en/samples/color-code) collection has 200+ validation cases you can paste in to confirm the Resolver's answers.

## What This Changes For Design Tokens, Themes, And Code Reviews

Three concrete shifts:

1. **Token names become perceptual, not RGB.** `--brand: #1d4ed8` becomes `--brand-royalblue` (or `--brand-blue-700`) — both encode "where this sits in the perceptual landscape" instead of "what the hex bytes are." Future you (or the next designer) reads the token name and knows the color band.
2. **Code reviews stop being color debates.** "Why is this `--brand-blue-500` and not `--brand-blue-600`?" → Open the [CSS Color Name Resolver](https://elysiatools.com/en/tools/css-color-name-resolver) for ΔE 2-3 between same-band shades — both are valid choices, the metric is empty, move on.
3. **Theme handoffs become predictable.** A dark-mode token set that uses `--surface: #0e1117; --surface-alt: #161b22;` (ΔE 4.5 between them) is fine. One that uses `--surface: #0e1117; --surface-alt: #0f1115;` (ΔE 0.9) is broken — the two "surfaces" are perceptually identical and the design intent is lost. The Resolver's ΔE numbers are the audit threshold.

The Resolver is one tool in the design system — pair it with the [Color Contrast Checker](https://elysiatools.com/en/tools/color-contrast-checker) for WCAG validation, the [Hex to HSL Converter](https://elysiatools.com/en/tools/hex-to-hsl-converter) for format translation, and the [Color Palette Extractor](https://elysiatools.com/en/tools/image-color-palette) for sampling brand colors from images. Browse the full [elysiatools design toolbox](https://elysiatools.com/en/tools) when you need the rest.
