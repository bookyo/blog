---
title: Why Light Bounces Back Instead of Passing Through
---

When light hits the boundary between two materials, it usually splits — some reflects, some refracts. Push the angle steeper, though, and something strange happens: **all of it reflects**. Nothing escapes. This is total internal reflection, and it is the reason your fiber optic internet works.

## The Setup: Two Media, One Boundary

Imagine a ray of light traveling through glass (refractive index n₁ ≈ 1.50) toward the surface touching air (n₂ ≈ 1.00). The light starts in the denser medium and approaches the boundary at some angle θ₁ measured from the normal — the line perpendicular to the surface.

At small angles, most light passes through into the air. Some reflects back into the glass. As the angle increases, less and less light makes it through — until, at a specific threshold, something changes. No light exits at all.

## The Critical Angle

The threshold is called the **critical angle** θc. It is defined by Snell's law:

n₁ · sin(θ₁) = n₂ · sin(θ₂)

When the refracted angle θ₂ reaches 90°, the light ray skims along the boundary rather than entering the second medium. Solve for θ₁ at this limit:

θc = arcsin(n₂ / n₁)

For glass-to-air (n₁ = 1.50, n₂ = 1.00):

θc = arcsin(1.00 / 1.50) = arcsin(0.667) ≈ **41.8°**

Any incident angle **greater than 41.8°** produces total internal reflection.

## What the Interactive Graph Shows

The simulation at the top of this page lets you adjust the incident angle and watch what happens in real time. Two canvases show different views:

**Ray Tracing View** — A single incoming ray strikes the interface between a blue-shaded upper medium (denser) and a gold-shaded lower medium (less dense). The normal line, the incident ray, the reflected ray, and — when applicable — the refracted ray are all displayed with angle measurements. Toggle the normal, angles, critical angle marker, and grid on or off.

**Fiber View** — A bundle of parallel rays enters a curved fiber. As each ray hits the inner wall at an angle greater than θc, it reflects again and again, trapped inside the fiber. This is exactly how optical fibers guide light over kilometers.

**The critical angle marker** (when enabled) shows a dashed line at θc from the normal. As you drag the incident angle past that marker, you can see the refracted ray disappear entirely — it simply ceases to exist beyond the boundary.

## Why No Refraction at Super-Critical Angles

Refraction is governed by the spreading of wavefronts. When sin(θ₂) = n₁/n₂ · sin(θ₁) exceeds 1, the right-hand side of Snell's law is greater than 1 — which is impossible for a real sine value. The wave equation has no solution for θ₂. Physically, the incident wave's energy cannot couple into a propagating wave in the second medium, so it reflects back with essentially zero loss (in a perfect material).

The reflectivity at TIR is theoretically 100% for lossless media. Real materials absorb a tiny fraction, but even then, TIR is far more efficient than any metallic mirror.

## Applications

**Optical fibers** are the most important application. A fiber's core (n ≈ 1.48) has a slightly higher refractive index than its cladding (n ≈ 1.46), so light injected at the right angle bounces down the fiber with minimal loss — modern silica fibers lose less than **0.2 dB/km at 1,550 nm**, enabling transoceanic communication without repeaters for hundreds of kilometers.

**Prism binoculars and camera prisms** use TIR to redirect light inside compact optical paths without needing mirrors — reflectivity near 100% versus ~85–95% for aluminum mirrors.

**Diamond gemstones** are cut so that most incoming light undergoes TIR inside the diamond (n ≈ 2.42, θc ≈ 24.4°) and exits only through the top facets, producing the characteristic sparkle that distinguishes a well-cut diamond.

Total internal reflection is not a curiosity — it is one of the most efficient light-guiding mechanisms in nature and technology.
