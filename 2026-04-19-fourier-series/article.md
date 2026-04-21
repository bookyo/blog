# The Math Behind Why a Circle Can Draw Anything

In 1822, Joseph Fourier submitted a 570-page manuscript to the French Academy of Sciences. It contained a claim that sounded like numerology: any repeating pattern — a jagged sawtooth, a square wave, even a rough sketch — could be constructed entirely from circles spinning at different speeds. The academy initially rejected it. Fourier spent years defending the idea before it was finally accepted.

Today, every MP3 file you stream, every JPEG image you view, and every 4G/5G base station your phone connects to runs on Fourier's insight.

The [Fourier Series visualization at ElysiaTools](https://elysiatools.com/en/visualizations/fourier-series) lets you watch circles draw anything in real time.

## The Premise

The formula looks deceptively simple:

**f(t) = a₀ + Σ(aₙcos(nt) + bₙsin(nt))**

What it says: take sine and cosine waves at integer multiples of a base frequency (1x, 2x, 3x...), scale each by its own coefficient, and add them all together. The result approximates any periodic function you want.

The geometric version is more intuitive. Take a circle. Spin it. Attach another circle to its edge, spinning at twice the speed. Attach a third at three times speed. Keep going. The endpoint of the last circle traces a shape. That's the whole idea: circles spinning at harmonic frequencies can draw squares, sawtooths, and surprisingly recognizable approximations of nearly anything.

## What the Visualization Does

The [Fourier Series tool](https://elysiatools.com/en/visualizations/fourier-series) splits the screen. On the left, epicycles — a chain of spinning circles, each attached to the previous one. On the right, a drawing area.

Draw anything closed with your mouse. A circle. A star. A rough triangle. Hit play and watch the epicycles reconstruct your shape. The tool runs a Discrete Fourier Transform (DFT) on your drawing, extracts the frequency coefficients, and feeds them to the circles. Your lines emerge from pure rotation.

A preset waveform selector handles square and sawtooth waves. The number-of-terms slider (N = 1 to 100) is the real insight dial — drag it and watch the approximation sharpen in real time.

## Why This Underpins Four Major Industries

**Signal processing.** When MP3 compression arrived in the late 1980s, it worked by decomposing audio into frequency bands using a modified Fourier transform. The encoder discards frequencies masked by louder nearby frequencies — a property called auditory masking. A 128 kbps MP3 is roughly 11x smaller than uncompressed CD audio, and most listeners cannot reliably distinguish them on consumer equipment.

**Image compression.** JPEG uses a two-dimensional discrete cosine transform. It separates image content into frequency components: low frequencies carry broad shapes and gradients; high frequencies carry edges and fine detail. The encoder quantizes high frequencies aggressively, producing the blocky artifacts visible in heavily compressed JPEGs — but at a 10:1 compression ratio, most viewers don't notice.

**Electrical power systems.** Power grids operate at 50 or 60 Hz, but nonlinear loads inject harmonics at 150 Hz, 250 Hz, 350 Hz, and higher. These harmonics cause transformers to overheat, capacitors to fail prematurely, and protective relays to misoperate. IEEE Standard 519-1992, which governs harmonic limits for utility interconnection, is entirely built on Fourier methods.

**Quantum mechanics.** The Schrödinger equation — the fundamental equation of atomic physics — has solutions that form Fourier pairs. The Heisenberg uncertainty principle (you cannot simultaneously know a particle's exact position and momentum) is mathematically rooted in the same Fourier relationships Fourier originally developed to understand heat flow.

## The Gibbs Phenomenon: A Beautiful Flaw

There's a fascinating artifact when approximating a square wave. A square wave has sharp discontinuities — it jumps instantly from -1 to +1. The Fourier series converges everywhere *except* at those jumps. It overshoots by about 9%, rings briefly, then settles. This is the **Gibbs phenomenon**.

The overshoot never disappears, no matter how many terms you add. Increase N and the spike narrows, but its height stays at roughly 9% of the total amplitude.

In the visualization, set the waveform to square wave, start with N=3, and watch the overshoot at transitions. Increase to N=20 and the spike doesn't vanish — it just tightens.

This caused real confusion in the 1890s. Early telephone engineers building smoothing circuits were baffled when their equipment produced unexpected oscillations at signal edges. They had accidentally built physical Fourier synthesizers without knowing it.

## What to Try

Start with a circle. At N=1, the epicycles collapse to a single spinning circle. Now draw something asymmetric — a rounded triangle. Watch how quickly the coefficients decay: the first few terms dominate, and the higher frequencies contribute progressively less. Smooth curves are cheap in Fourier terms; sharp corners require many high-frequency components.

Drag the terms slider from 1 to 50 slowly. Notice where the approximation breaks down first: at corners and edges, where the function changes direction abruptly. These are exactly the frequencies that are hardest to represent with a finite sum of smooth sine waves — and that's not a limitation of the math, it's a fundamental property of smoothness itself.

Here's a question worth sitting with: if Fourier decomposition is essentially breaking shapes into rotations, what does that tell you about the relationship between geometry and motion — between the static shapes we draw and the spinning machinery that generates them?

The [Fourier Series visualization](https://elysiatools.com/en/visualizations/fourier-series) at ElysiaTools lets you test your own answers to that question.
