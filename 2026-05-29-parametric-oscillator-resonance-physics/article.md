---
title: Why a Swing Works Only When You Push at Exactly the Right Frequency
---

A child learning to pump a swing asks a parent for help, and the parent asks a question that sounds obvious: *when do you push?* The child soon learns: not whenever. Not harder, not faster. You push once every two swings, at the moment the seat is at its lowest point — and the swing grows. No one mentions resonance, no one writes an equation, and yet the result is exactly what the Mathieu equation predicts. A periodic push at exactly twice the swing's natural frequency takes almost no energy to build an enormous amplitude.

Parametric resonance is that kind of phenomenon. It is a form of oscillation growth that requires no driving force at the system's own frequency. Instead, it requires a parameter — something in the system itself — to change periodically at twice that frequency. The swing's parameter is the effective gravitational force as the child shifts body weight at the right moment. The driving force is zero. The amplitude grows anyway.

## The Ordinary Resonance Problem

Most people have heard of resonance: when you drive a system at its own natural frequency, the amplitude builds. A singer shattering a wine glass. A bridge swaying in wind. The classic formula is straightforward — a sinusoidal force `F cos(ωt)` applied to a harmonic oscillator, and when the driving frequency ω matches the natural frequency ω₀, the amplitude peaks sharply.

Parametric resonance is different. Here, no external force acts directly on the mass. Instead, one of the parameters in the equation of motion — the restoring coefficient, which might be proportional to a spring constant — is made to oscillate. If that oscillation is fast enough and strong enough, the system goes unstable not despite the absence of a driving force, but because of the way the parameter change deposits energy into the motion.

The equation for a parametric oscillator looks like this:

`m · d²x/dt² + 2γ · dx/dt + [k₀ + k₁ · cos(2ω₀ t)] · x = 0`

The term `k₁ · cos(2ω₀ t)` is the time-varying stiffness. It is zero on average — it neither adds nor removes net energy over a full cycle. But over half a cycle, during exactly those moments when the displacement is zero and the velocity is maximum, the stiffness is such that the restoring force works *with* the motion rather than against it. The integral of power over a full period is positive. The system grows.

## The Mathieu Equation and the Stability Chart

This differential equation is known as the **Mathieu equation**. Its solutions are mathematically rich and were studied in detail by Henri Poincaré in the 1880s, long before anyone imagined using them to design circuits or explain playground physics.

The key parameter governing the behavior is the ratio `p = 2ω₀ √(k₀/m)` — the ratio between the parametric drive frequency and twice the natural frequency of the system — combined with a dimensionless strength `ε = k₁/k₀`. The result is a **stability chart**, also called a Floquet diagram: a two-dimensional map in (p, ε) space where every point is either stable (bounded oscillation) or unstable (growing oscillation). The unstable regions are narrow tongues that fan out from integer and half-integer values of p. The most prominent tongue sits at `p ≈ 1`, which means the parametric drive frequency is exactly twice the natural frequency.

This is the playground result, made precise: a parametric drive at `2ω₀` is the most dangerous frequency for a system with stiffness oscillation. Not at ω₀, as in ordinary resonance — at `2ω₀`.

## Why the Growth Happens When It Does

Consider the energy balance over one drive period. The parametric stiffness `k(t) = k₀ + k₁ · cos(2ω₀ t)` modulates the potential energy. When `k(t)` is high, the effective spring is stronger and the restoring force acts to slow the mass as it passes through equilibrium — the system stores potential energy. When `k(t)` is low, the restoring force is weaker and the mass is moving fastest through the equilibrium point. The work done by the stiffness against the motion over the high-stiffness half of the cycle is negative. The work done over the low-stiffness half is positive. If the drive phase is tuned so that the low-stiffness half coincides with maximum velocity, the net work per cycle is positive. Energy flows in.

This is not obvious. The stiffness modulation is symmetric in time — the same positive and negative contributions each cycle — but the system's own motion breaks the symmetry. Because the mass moves fastest when displacement is zero, and the restoring force is proportional to displacement, the product of stiffness and displacement is not symmetric over the period. The system "remembers" whether it was accelerating or decelerating at the moment the stiffness changed, and acts accordingly.

The consequence: a small periodic drive at `2ω₀` can cause exponential growth in amplitude — not linearly, but exponentially, with a growth rate given by the Floquet exponent of the Mathieu equation. In a lossless system (`γ = 0`), the amplitude grows as `e^(λt)` where λ is a positive constant determined by the instability tongue.

## Where It Shows Up

The parametric oscillator is not merely a curiosity. It appears across physics, engineering, and nature.

**The playground swing** is the most intuitive example. The child shifts weight to modulate the effective length and gravitational restoring force. Pumping at the right frequency (once every two natural swings) adds energy every half cycle. The child does not push against the direction of motion — they effectively lower the system at the right moment, so gravity works with the swing rather than against it.

**Quartz crystal resonators** in watches and clocks exploit parametric resonance at radio frequencies. A quartz crystal has a time-varying electric field applied at twice its mechanical resonance frequency, causing it to vibrate at its mechanical resonance with very low power consumption. This is the principle behind the crystal-controlled oscillator — without it, wristwatches would drift minutes per day.

**Optical frequency combs** — the Nobel Prize-winning invention by John L. Hall and Theodor Hänsch — use parametric amplification in laser cavities. A continuous-wave laser is modulated at twice its cavity frequency, producing a comb of equally spaced frequencies that can be used to measure other frequencies with extraordinary precision. Atomic clocks are calibrated this way.

**Faraday waves** are surface waves that appear on a fluid when its container is oscillated vertically at a frequency that is twice the natural frequency of the fluid surface. The parametric instability creates a standing wave pattern with a wavelength set by the container geometry. The same mathematics describes ripples in a coffee cup on a vibrating table.

**Particle accelerators** use radio-frequency cavities to impart energy to particles. The accelerating gap voltage is modulated at a frequency matched to the particle's orbital frequency — effectively a parametric drive at the subharmonic of the revolution frequency. The particles receive energy in phase with their passage through the cavity.

**Biology?** There is evidence that the human proprioceptive system can detect parametric resonance frequencies. A dancer or gymnast who "feels" the natural frequency of a swing-like motion and times their pushes accordingly is solving the Mathieu equation without writing it down.

## The Threshold and the Sweet Spot

Not every parametric drive creates growth. There is a **threshold**: the product of the drive strength `ε` and the quality factor `Q = ω₀ / (2γ)` must be large enough to overcome damping. Below the threshold, the system is stable — a small parametric drive produces a small bounded oscillation. Above the threshold, the instability tongue opens and the amplitude grows exponentially.

The threshold condition for the first instability tongue (near `p = 1`) is approximately:

`ε > 2γ / ω₀`

Or in terms of Q: `ε · Q > 2`. A system with high Q (low damping) goes unstable more easily. A playground swing, which has very low damping, requires only a small weight shift from the child — the threshold is easily crossed. A heavily damped system requires a large parametric drive or a very precise frequency match.

This is also why parametric oscillators are useful as frequency dividers: a signal at frequency `2ω₀` goes in, and a clean oscillation at `ω₀` comes out, with the system acting as an amplifier for the subharmonic. The output frequency is half the input — a division by two that costs very little power, which is why it is standard in radio frequency signal processing.

## What You Actually Need to Remember

Two facts about parametric resonance are worth carrying forward. First, the critical frequency is `2ω₀` — not ω₀ as in ordinary resonance. A parameter oscillating at exactly twice the natural frequency of the system is the one that can grow without bound, because that is the frequency at which energy is deposited into the system during exactly those moments when the velocity is maximum and the restoring force has no resistance left to offer.

Second, there is a threshold: the parametric drive must be strong enough relative to the damping to open the instability tongue. Below the threshold, the system is merely perturbed. Above it, the amplitude grows exponentially. Most real systems sit close to the threshold, which is why parametric devices like quartz resonators are designed to operate precisely in this regime — stable enough not to oscillate spontaneously, unstable enough to amplify a clean injected signal.

The swing your child pumps, the quartz in your watch, the laser in a frequency comb — all of them run on the same principle, one that looks like magic until you see the Mathieu equation, and then looks like the most elegant thing you have ever seen in physics.