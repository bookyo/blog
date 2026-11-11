---
title: "PDF Formula Extractor Field Guide: When the Font Name Is the Proof"
---

**A PDF does not store equations. It stores glyphs, positioned.** The gap between those two facts is the whole engineering problem, and the font name is where the answer hides. I ran the [PDF Formula Extractor on Elysia Tools](https://elysiatools.com/en/tools/pdf-latex-mathml-mathjax-formula-extractor-and-equation-number-preserver) against its own bundled sample and read the tool's implementation, and the thing that surprised me is how little guessing is involved. LaTeX writes its equations in dedicated math fonts, and if you know what those font names look like, the equations announce themselves.

The number that stayed with me was not a formula. It was the census. On a two-page paper, 529 characters carry text, and 34 of them sit in a font the tool recognises as mathematical. That is 6.43 percent of the document. Every equation, every Greek letter, every integral sign lives inside that sliver, and the other 495 characters are prose.

## What the extractor actually reads, and what counts as math

The tool takes a PDF and returns three things per formula: a LaTeX string, a presentation MathML rendering of it, and an equation number when one exists. What makes that possible is that it never looks at the picture of the equation. It reads the PDF's text operators and asks which font each run of characters was drawn in.

That distinction matters more than it first appears. Optical character recognition reads pixels, so it has to guess at every ambiguous glyph, and a fraction bar and a division slash look identical in a photograph. A vector PDF does not have this problem. The characters are already text. The only question is how they were drawn, and the PDF answer records the answer.

So the pipeline has two halves. The first half reads the operator list to recover the true font name behind each internal font identifier. On the sample, the internal handles are `g_d0_f1` through `g_d0_f8`, and behind them sit `Helvetica-Bold`, `Helvetica`, `KaTeX_Math-Italic-2804`, `KaTeX_Main-Regular-5373`, `KaTeX_Size2-Regular-1836`, and `KaTeX_Caligraphic-Regular-763`. The handle tells you nothing; the resolved name tells you everything.

The second half reads the positioned text items and groups them by geometry. The font name answers what is mathematical, and the geometry answers how it is arranged.

Once the font names are recovered, the tool scores every line. A line counts as a math line when at least half of its characters read as mathematical and it carries at least two such characters. Mathematical means one of five things: the run is in a math font, the run contains a character from the Unicode math blocks, the run is Greek, the run contains only operators and digits, or the run is a known function name.

That last clause is doing quiet work. A bare run reading `tan` in Helvetica is not automatically prose. It becomes mathematical because `tan` is on a list of 32 recognised function names, alongside `sin`, `cos`, `ln`, `exp`, `det`, `ker`, and `gcd`.

The font families the detector recognises fall into three groups, and the sample exercises two of them. Computer Modern gets an explicit prefix list: `CMMI`, `CMSY`, `CMEX`, `MSAM`, `MSBM`, `EUSM`, `EUFF`, `EUTF`, `RSFS`, `LASY`, `WASY`, plus the `tx` and `px` variants. Anything containing the substring `math` matches next, which catches Cambria Math and MathJax output. And the KaTeX families get their own pattern covering Math, Size, AMS, Caligraphic, and Fraktur.

The sample is rendered in KaTeX, and the split is informative. Page one carries five fonts, of which two are marked mathematical: `KaTeX_Math-Italic-2804` for variables and `KaTeX_Size2-Regular-1836` for the large integral sign. `KaTeX_Main-Regular-5373` is not marked, because the pattern matches Math, Size, AMS, Caligraphic, and Fraktur but not Main. Page two adds `KaTeX_Caligraphic-Regular-763`, and that single character is the `L` in `\mathcal{L}`.

## How a superscript becomes a superscript

Once a line is classified, the tool decides what part of it is raised or lowered. It does not look for size differences, even though that would be the obvious approach, because a subscript in LaTeX is often set at a similar size to its base. It looks at baseline position instead.

The mechanism is a dominant baseline for the whole zone, chosen as the line carrying the most text mass. Every chunk is then measured against that baseline. A chunk raised above it by more than 22 percent of the base line height, but not more than 95 percent, and not taller than 80 percent of the base, is a superscript. The same distance below is a subscript.

That rule has a clean result on the sample. In `E = mc²`, the base line sits at y 152 with a height of 14 points, and the `2` sits at y 142 with a height of 9. Its offset is 10 points, which is 71.43 percent of the base height. That lands inside the window on all three conditions: above the 3.08-point floor, below the 13.30-point ceiling, and short enough to satisfy the 11.20-point size cap. The result is `E = mc^{2}`, and the whole superscript sits inside braces so a multi-character exponent would survive.

The same geometry handles the integral's limits, and this is where the ordering rule earns its keep. In equation 2, the base line has eight chunks and a text mass of 145, which makes it the dominant baseline. The `0` sits 10 points below it and the `∞` sits 10 points above it, and both are 8 points tall. Both qualify as scripts, and both want to attach to the integral.

The tool breaks the tie by preferring a subscript when two chunks claim the same x position. The `0` and the `∞` sit at the same x coordinate of 204, which means an identical sort key of 408, and the tie-break puts the subscript first. That is why the reconstructed formula reads `\int_{0}^{\infty}` and not `\int^{\infty}_{0}`. It is a small rule, and it is the difference between a formula you can paste into a document and a formula you have to fix by hand.

## Why the right margin is worth more than the equation

Here is the part that changes what you can do with the output, and it has almost nothing to do with mathematics. AMS numbering places equation numbers in the right margin. The tool captures them by looking for a text run that matches the shape of a parenthesised number and sits past 62 percent of the page width.

On the sample, page width is 612 points, so the threshold is 379.44 points, or 379 when rounded. Every equation number in the document sits at either 494 or 500 points, comfortably past it. The numbers found are `(1)`, `(2)`, `(3)`, `(4a)`, `(4b)`, `(5)`.

Six numbers for seven display equations. The seventh display equation has no number at all, and that is correct: it is the unnumbered `κ = tan α` that follows the prose about parameter bounds.

The `(4a)` and `(4b)` pair is the case that matters, because a subequation group is not a numbering quirk. It means two separate display equations share one number, which is how a multi-part derivation gets referenced. The tool detects this by stripping the trailing letter and grouping: two or more numbers that share a numeric stem and all carry a letter suffix become a subequation group. The sample has exactly one such group, and it is the `(4a)/(4b)` pair.

Preserve the number and you preserve the citation. Lose it and your reference to equation 4 no longer resolves to anything, because there are now two formulas with no way to tell them apart. This is why the tool's output includes the number as a first-class field rather than burying it in a comment, and why the `.tex` bundle writes each numbered formula into an `equation` environment with a matching label.

## The three scopes, and what each one costs

The scope option is the one decision that changes your bill. `display` returns only display equations: 7 formulas, 6 numbered, 1 subequation group. `all` returns display plus inline runs: 12 formulas, of which 5 are inline, and the inline ones are the ones buried in prose.

The inline runs are where the honest limits show up. On page one the prose reads that the damping ratio `ζ` is small, and the tool returns three separate inline fragments: `ζ`, then `ζ \geq 0`, then `λ \neq 0`. The first is a bare Greek letter standing alone, and the second repeats the `ζ` that the first fragment already captured.

That duplication is not a bug in the extractor. It is a consequence of how inline runs are found: a run begins at a chunk that is unambiguously mathematical and ends when the text turns back into prose. The sentence `ζ is small` yields a run containing `ζ`; the later sentence `ζ ≥ 0 and λ ≠ 0 for all modes` yields a run containing `ζ ≥ 0` and another containing `λ ≠ 0`. Different sentences, different runs, and the same symbol appearing in both.

The `numbered` scope exists for a third audience. Filter to numbered equations only and you get the citation backbone of the paper with none of the inline noise. Cap the scan at one page and you get exactly `(1)`, `(2)`, `(3)`, with a maximum equation number of 3.

## Where the reconstruction stops being exact

The honest gap belongs here, and it is worth being precise about, because the tool's own documentation does not dwell on it. Complex matrices and multi-line aligned environments are best-effort reconstructions. The pipeline understands a single display line, a subscript, a superscript, and a two-line stacked fraction. It does not understand a three-row matrix or a five-line align block.

The stacked fraction is detected by a geometric rule: exactly two math lines in a zone, their centres within 45 percent of the wider line's width, and their baselines separated by more than 1.3 times the taller line's height. On the sample, `Δk` sits at y 310 with a height of 10 and `1 + η` at y 342 with a height of 10. The gap is 32 points against a threshold of 13, and the two centres are 218.77 and 217.49, a difference of 1.29 points against a tolerance of 12.14. The result is `\frac{\Delta k}{1 + \eta}`.

The rule that works for one fraction has a cost. A zone with exactly two math lines that happens to be two separate equations, not a numerator over a denominator, would be merged into a fraction. The sample does not contain that case, so I cannot tell you how often it fires in the wild. That is the limit of what I verified.

There is a second limit worth naming, and it is the one that decides whether the tool applies to your PDF at all. Scanned and image-only PDFs have no text layer, so the extractor finds zero formulas and rejects the file with a message telling you to run OCR first. I confirmed this by building a page with no text operators at all and reading it back through the same PDF engine: zero text items with content, and therefore zero formulas.

OCR, in other words, gets you the characters. It does not get you the font names, the baseline offsets, or the right-margin positions. Running OCR first and feeding the result back in does not restore any of the three, because all three are properties of the vector PDF that the scan threw away.

## The bundle that made the number checkable

The final output is a downloadable `.tex` bundle, and it is the artefact that made every claim in this piece checkable. It opens with `\documentclass{article}` and `\usepackage{amsmath}`, then walks the formulas in document order.

Each numbered display formula becomes an `equation` environment with a label derived from the number: `\begin{equation}\label{eq:4a} % (4a)`. Unnumbered display formulas become a bare display block using the square-bracket delimiters. Inline runs are written as comments rather than live math, which is a deliberate choice, since a display equation environment cannot hold inline material.

Here is the bundle the tool writes for the sample, in the order the formulas are found:

```latex
% Extracted by pdf-latex-mathml-mathjax-formula-extractor-and-equation-number-preserver
\documentclass{article}
\usepackage{amsmath}
\begin{document}
% inline (page 1): $\zeta$
\begin{equation}\label{eq:1} % (1)
E = mc^{2}
\end{equation}
\begin{equation}\label{eq:2} % (2)
F(x) = \int_{0}^{\infty} e^{-\alpha x} dx
\end{equation}
\begin{equation}\label{eq:3} % (3)
\frac{\Delta k}{1 + \eta}
\end{equation}
\[
\kappa = \tan \alpha
\]
% inline (page 1): $\zeta \geq 0$
% inline (page 1): $\lambda \neq 0$
\begin{equation}\label{eq:4a} % (4a)
\sigma(\omega) = \sigma_{0} + \sigma_{1} \omega^{2}
\end{equation}
\begin{equation}\label{eq:4b} % (4b)
\lambda_{\max} = \Gamma / 2 \pi
\end{equation}
% inline (page 2): $\omega / \pi$
% inline (page 2): $\tau \to 0$
\begin{equation}\label{eq:5} % (5)
\mathcal{L} \geq 2
\end{equation}
\end{document}
```

Two things in that bundle are worth pausing on. The label `eq:4a` carries a letter in a LaTeX label, which is legal but unusual; amsmath will happily cross-reference it, though you are inventing a label namespace that no original document defined. And the `\[` block for the unnumbered formula has no matching `\begin{equation}`, which is the correct choice for an unnumbered display.

Before any of this is worth trusting, every reconstructed LaTeX string is validated through temml, the TeX-to-MathML renderer that MathJax and KaTeX build on. A string that fails to render is reported as an error rather than quietly shipped. I ran all twelve reconstructed formulas from the sample through temml myself, and twelve of twelve passed, with no error annotations in the MathML output.

That validation is what makes the MathML half of the output safe to use downstream. The tool exports presentation MathML, and MathJax v3 accepts MathML as direct input, so the same reconstruction can feed a web renderer without a second LaTeX round trip. The [AsciiMath LaTeX MathML Equation Converter](https://elysiatools.com/en/tools/asciimath-latex-mathml-equation-converter) covers the other direction of that same pipeline, from a plain-text math syntax into LaTeX and MathML.

## What to do when the tool says no

There are two failure modes worth planning for, and both produce a clear refusal rather than a wrong answer.

The first is the image-only PDF, already covered. The tool refuses, and the fix is upstream: run OCR to get a text layer, and accept that the font-level signals will not survive.

The second is a PDF whose text layer exists but whose mathematics was typeset in ordinary fonts. The tool's own description advertises STIX and Cambria Math support, and here is where I found a gap worth knowing about. The detector's middle rule matches any font name containing the substring `math`, so `Cambria Math` and `STIXTwoMath` are recognised. But a bare `STIXGeneral` contains no such substring and no recognised prefix, so it is not marked as mathematical. A Word document using plain STIX will therefore have its equations missed by the font signal.

The font inventory panel is where you spot this before you rely on the output. It lists every font in the document with the mathematical ones marked, so a document with zero math font families tells you the answer before you read a single formula. Read that panel first, and treat an empty one as a verdict rather than a bug.

For the extraction path itself, the [PDF OCR Text Layer](https://elysiatools.com/en/tools/pdf-ocr-text-layer) and [Scanned PDF OCR to Word](https://elysiatools.com/en/tools/scanned-pdf-ocr-to-word) tools cover the image-only side, and the [OCR PDF to Structured JSON Bridge](https://elysiatools.com/en/tools/ocr-pdf-to-structured-json-bridge) turns a recognised document into a structured record. None of them recover font names, and none of them claim to.

The [PDF Samples collection on Elysia Tools](https://elysiatools.com/en/samples/pdf-samples) has the document shapes worth testing against, and the [Document Tools category](https://elysiatools.com/en/categories/document-tools) groups the neighbouring converters.

## The part that does not fit the neat story

Every equation in the sample survived the round trip, and 12 of 12 reconstructed strings passed temml validation. If you stop there, the story is tidy: a vector PDF, a font name, a baseline offset, a right margin, and out comes LaTeX.

But the sample is a two-page document rendered by KaTeX, and KaTeX is unusually well behaved. It embeds distinct fonts per role, it positions limits and scripts with real baselines, and it puts equation numbers at a consistent margin. A LaTeX-produced paper using Computer Modern does the same thing, and a Word document using Cambria Math comes close. The PDF where the neat story breaks is the one you will actually be handed: a publisher's file where the fonts were subset and renamed, where the equations were converted to outlines so they cannot be copied at all, or where a table of formulas was rasterised during typesetting.

I could not reproduce those cases here, because I had one sample. What I can tell you is what to check, and the check is cheap: read the font inventory before you read the formulas. If the math font count is zero, the extractor is working correctly and there is nothing for it to find.

The proof is in the font name. It was in the file all along, in the one field most extractors throw away.
