---
title: A PDF Does Not Store Equations: Only Glyphs at Coordinates
---

**I pasted a fraction out of a paper and got `k1` back.** Not a garbled fraction, but two symbols where a ratio used to be. The PDF is not broken and the reader is not lazy: a PDF does not store equations at all. It stores glyphs at coordinates, in named fonts, sitting on baselines, and it trusts your eye to rebuild the structure that the text layer never carried.

## The page reports three signals, and the text layer reports none

This is not a rendering problem. Three things on the page carry the math, and none of them is the character string that copy selects: the font family attached to a run, the vertical offset of that run from its line's baseline, and a short bracketed number parked at the right margin.

Reading those three takes a different API. `pdf.js` hands out internal font ids through `getTextContent()`, then exposes the real family names through the page operator list and the `commonObjs` map, which is the only route to a name like `KaTeX_Math`. Subset fonts prefix six uppercase letters and a plus sign, so the first pass strips `[A-Z]{6}+` before any classification happens.

## The font name is the strongest evidence in the file

The classifier leans on a short list of families that only math typesetting produces: `CMMI`, `CMSY`, `CMEX`, `MSAM`, `MSBM`, `EUSM`, `EUFF`, `EUTF`, `RSFS`, `LASY`, `WASY`, `CMMIB` and `CMBSY`, plus the `txmi`, `txsy`, `pxmi` and `pxsy` families that pdfTeX and XeTeX emit.

Two looser patterns cover the rest. A plain `/math/i` test picks up `Cambria Math`, `STIX Two Math` and `Latin Modern Math`, and a third pattern matches `KaTeX_(Math|Size|AMS|Caligraphic|Fraktur|Script)`. Prose does not wear a family called Math.

That is why the font name beats a visual guess. A roman paragraph stays in CMR or a Times clone; the instant a run switches to CMMI it is math by construction, and the file records the switch as a fact. Confidence follows the evidence: a page with a detected math family scores high, and a page without one drops to medium.

## A superscript is an offset from the baseline, measured in glyph heights

Scripts need one anchor: the dominant baseline of a zone, taken as the line with the largest text mass, where mass is non-space characters multiplied by glyph height. From there the test is a ratio, not a pixel count. A chunk becomes a superscript or subscript when its lift is above `0.22` times the base height, at most `0.95` times it, and its own height is no more than `0.8` times the base.

Each bound earns its place. Under `0.22` the offset is kerning or rounding noise. Past `0.95` the chunk belongs to the next line, and a chunk taller than `0.8` of the base is a full-size symbol sitting low instead of an index. Ties at equal x go to the subscript, which is how `\int_{0}^{\infty}` comes back with its lower limit written before its upper one.

The bounds look arbitrary until you watch them break. For example, a body set at 10 pt with 4 pt subscripts lifts those subscripts by roughly 3 pt, which is 0.3 of the base height and safely inside the band; a superscript riding above a fraction line lifts further, and past `0.95` the same rule refuses to call it a script. I observed both shapes inside a single two-page sample.

## A fraction is two lines that share a center

A stacked fraction leaves no character behind. There is no glyph for the bar, so the only witness is geometry: when a zone holds exactly two math lines, the baseline gap must exceed `1.3` times the taller line and the two line centers must sit within `0.45` times the wider line's width. When both hold, the zone ships as `\frac{...}{...}`.

The tool's bundled academic sample shows the shape in practice. Two pages of LaTeX-style paper, numbered `(1)` through `(5)` with a subequation pair, one stacked fraction and one integral: display scope returns 7 formulas, 6 of them numbered, with `\frac{\Delta k}` and `\int_{0}^{\infty}` both intact.

## The equation number sits in the right margin

`amsmath` parks `(4a)` at the right edge of the text block, and the extractor looks for exactly that shape: a chunk matching `^\((\d{1,3}[a-zA-Z]?)\)$` whose x position is past `62%` of the page width. The matched chunk is blanked after capture, so the number never leaks into the LaTeX it belongs to.

The suffix carries the citation value. A set counts as a subequation group only when at least two numbered cards sit together and carry a letter suffix, and the strip removes that trailing letter before parsing. Without it, `(4a)` and `(4b)` would push the maximum past the last number the page printed.

A missed number is easy to spot: 6 numbered cards should agree with the largest number the page carries. When they diverge, the cause is often a tag set in a roman family while the equation beside it sits in Cambria Math, so the font inventory is the first place to look. I have seen that split on Word exports, where one run carries the math and the next carries the label.

## Display or inline: a 28-point indent decides

The page's own left margin is the reference. The smallest x among roman-font chunks becomes the body margin, and a math line becomes a display candidate when it starts more than `28` units past that margin, or when an equation number was captured in the same zone. Lines merge into zones while the vertical gap stays within `2.0` times the taller line's height.

Scope changes the count and leaves the page alone. I measured the same two-page sample at both settings: 7 formulas in display scope, 12 with scope set to all. The difference is 5 inline runs living inside prose, bridged from connector-only chunks such as digits, `+ - = < > / ( ) [ ] | . , ! :` and trimmed at both ends; those runs increase the count without adding a display equation.

## Where the method breaks, and what it costs

Scanned PDFs get refused first. With no text layer there is no font name to read, so the tool rejects the file instead of returning an empty report that reads like a clean page. The wording is worth quoting: "No formulas were detected. If this PDF is a scan (image-only) it has no text layer: run OCR first, then retry." That is a case where a hard failure beats a soft one, because an empty result on a scanned page looks like a bill of health. The caps are blunt as well: 25 MB per file, 20 pages by default and 200 at most, 800 formulas before the scan stops with a warning.

Two softer limits matter more. Matrices and multi-line alignment environments are best-effort, because their geometry does not reduce to stacked or offset runs. Pages whose operator list will not resolve lose their font hints and drop to medium confidence, which is the extractor reporting a guess instead of hiding one.

## What the output is good for

Each card carries three products: copyable LaTeX, presentation MathML, and a line in a `.tex` bundle you can download. The LaTeX is validated by rendering it through `temml`, so an unparseable string is flagged, not shipped as broken markup, and the MathML goes into MathJax v3 or a KaTeX pipeline with no conversion step.

What it does not hand you is the argument. You get equations and their printed numbers, not a map from equation to claim, and a cross-reference like "see (4b)" stays in the prose where it was written. For documents that never carried machine-readable math, that is a fair trade: [run one of your own papers through it](https://elysiatools.com/en/tools/pdf-latex-mathml-mathjax-formula-extractor-and-equation-number-preserver) and compare the reported count against the numbers you can see on the page. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

I spent a year treating this as a reading problem: better OCR, a bigger model, more of the page pushed through it. It is a layout problem. The PDF never lost your equation, because it never stored one. What it stored was the evidence, the math family and the baseline lift and the `(4a)` sitting in the right margin. So the next time a paste returns `k1`, what happens if you open the font inventory first?
