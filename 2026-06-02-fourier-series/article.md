---
title: Why Every Periodic Function Hides Inside Circles
---

In 1807, Joseph Fourier submitted a paper to the French Academy claiming something that made the mathematicians in the room uncomfortable: any repeating waveform — a square wave, a sawtooth, even the jagged output of a broken switch — could be reconstructed exactly by adding together nothing but pure circular motion.

The referees rejected it, calling it insufficiently rigorous. They were wrong. And the visualization below shows exactly why.

## The Idea in One Sentence

When you add enough sine waves together — each one a perfect, smooth oscillation — you can approximate any repeating pattern. The more waves you add, the closer you get. With infinitely many waves at just the right amplitudes, you reach the exact original shape.

Mathematically, a periodic function f(t) with period T can be written as:

f(t) = a₀/2 + Σₙ[aₙ cos(2πnt/T) + bₙ sin(2πnt/T)]

The terms aₙ and bₙ are the Fourier coefficients — numbers that tell you how much of each frequency is present in the original signal.

## How the Epicycles Draw the Wave

The interactive tool uses the Discrete Fourier Transform (DFT). Instead of analyzing a continuous mathematical formula, it takes a user-drawn curve and extracts the Fourier coefficients from it. Each coefficient corresponds to an epicycle — a circle riding on the edge of another circle, both spinning at constant speeds.

Start with a circle spinning at the fundamental frequency (once per cycle). Add a second circle spinning at twice that speed, whose radius encodes the first harmonic's strength. Then add a third at three times speed, and so on. The endpoint of the last circle traces the reconstructed waveform. Watch enough epicycles spinning, and you see a square wave emerge from pure circular motion.

## Why This Works: Orthogonal Bases

The reason you can isolate each frequency independently is that sines and cosines form an orthogonal basis for periodic functions. Orthogonal means each frequency component lives in its own dimension, completely independent of the others. When you project your waveform onto each basis function, you get a coefficient encoding how much of that frequency is present.

This orthogonality is what makes Fourier analysis universal:
- Decomposes an audio recording into a spectrum of frequencies
- Extracts signal from noisy sensor data in an MRI machine
- Predicts tidal variations in harbor engineering
- Enables JPEG compression by isolating frequency coefficients

## The Warm-Up: Adding Two Circles

Before complex waveforms, start with the simplest case: two circles. Take one circle spinning once per cycle. Attach a second circle at its edge, spinning twice as fast with a smaller radius. The endpoint traces a Lissajous figure — a preview of how harmonics combine.

The square wave is built from only odd harmonics: 1× fundamental, 1/3× third, 1/5× fifth, 1/7× seventh, and so on. Every even harmonic has coefficient zero. That restriction is what creates the sharp corners — a discontinuous jump that no finite sum of smooth waves can perfectly reproduce, but that the infinite series does reproduce exactly.

## The Deeper Surprise: Discontinuity from Continuity

Here is the paradox: each term in the Fourier series is continuous — smooth sine waves, infinitely differentiable everywhere. Yet the sum of infinitely many smooth terms can produce a discontinuity. This was the property that made 18th-century mathematicians uncomfortable, and why Fourier's result required nearly a century of development before it was fully justified.

The Gibbs phenomenon is the signature of this: when you truncate the series to N terms, you get overshoot near the discontinuity. The overshoot is about 9% of the jump height, regardless of how many terms you use. It never fully disappears until infinity.

## Why the Interactive Graph Reveals More Than the Formula

The static formula tells you what the coefficients are. The interactive visualization shows you what they mean. Seeing the epicycles spin — watching the output point jump from chaos into order as you increase the number of terms — gives intuition that the equation alone cannot.

Once you've watched a discontinuous waveform require infinite terms, the Gibbs phenomenon becomes a design constraint, not just a curiosity. The visualization makes the abstract concrete in a way the formula never could.

## The Takeaway

Fourier's 1807 rejection was not a failure of the math — it was a failure of imagination. The circles were always there, waiting in any repeating pattern you chose to examine. Now you have the tool to find them yourself.
