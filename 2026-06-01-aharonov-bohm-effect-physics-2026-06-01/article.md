---
title: Why the Aharonov-Bohm Effect Proves That "Empty" Space Has Structure
---

A solenoid is placed between two slits. The magnetic field outside the coil reads zero. No instrument attached to the electron's path detects anything unusual. And yet, when the current through the solenoid increases, the interference pattern on the detection screen shifts — visibly, repeatably, in proportion to the magnetic flux through the coil.

This is the Aharonov-Bohm effect, and it remains one of the most counterintuitive predictions in quantum mechanics.

## What the Experiment Actually Shows

Imagine a standard double-slit setup. Electrons travel from a source, pass through two narrow slits, and land on a detection screen. The pattern that builds up over time is an interference pattern — alternating bright and dark bands that reflect the wave nature of the electron.

Now place a long solenoid between the two slits, oriented perpendicular to the plane of the electron paths. The solenoid carries an electric current, which produces a magnetic field inside it. Outside the solenoid — in the region where the electrons actually travel — the magnetic field is zero. No matter how strong the current inside the solenoid, a magnetometer placed in the electron's path reads nothing.

And yet the interference pattern changes. The fringes shift in proportion to the magnetic flux passing through the solenoid, even though the electrons never enter the region of non-zero field.

This was predicted by Yakir Aharonov and David Bohm in 1959, and it was confirmed experimentally in the 1960s and 1980s with increasing precision. The effect is real.

## The Phase Shift: What the Math Says

The physics is captured by a single equation:

δφ = 2π · (Φ / Φ₀)

Here, δφ is the phase difference between the two electron paths, Φ is the magnetic flux through the solenoid (measured in webers), and Φ₀ = h/e ≈ 4.14 × 10⁻¹⁵ Wb is the flux quantum — the fundamental unit of magnetic flux in quantum systems.

The phase shift is proportional to the flux, and it is an integer multiple of 2π. That integer is the winding number: the number of times the electron's path winds around the solenoid.

Notice what is not in the equation: the magnetic field strength B. The field is zero in the electron's region, but the phase still shifts. What matters is the **total flux**, which depends on the field inside the solenoid and the cross-sectional area of the coil — not on what the field does outside it.

## Why the Vector Potential Does the Work

In classical electromagnetism, the magnetic field B is the fundamental quantity. The vector potential A is a mathematical convenience — you can add the gradient of any scalar field to A without changing B, so A itself has no direct physical meaning.

In quantum mechanics, this changes.

The phase accumulated by an electron traveling through a region with vector potential A is proportional to the line integral of A along the electron's path. Even when B = ∇ × A = 0 everywhere the electron goes, the line integral of A around a closed loop that encircles the solenoid is not zero — it equals the flux Φ. This is a topological property: the integral depends on how many times the path winds around the coil, not on the details of the field at any specific point.

So the electron's phase is sensitive to the global topology of the situation — to whether its path encircles the solenoid or not — even though the local magnetic field is zero throughout.

This is what makes the Aharonov-Bohm effect topological rather than local.

## What This Means for the Double-Slit Pattern

The double-slit interference pattern is produced by the superposition of two electron wavefunctions — one that passes through the upper slit, one that passes through the lower slit. Each path accumulates phase as the electron travels.

When the solenoid is present, the two paths enclose different amounts of magnetic flux. The path that goes above the solenoid encircles it once; the path that goes below does not. This means they accumulate different phase shifts, even though both pass through field-free regions.

The interference pattern on the screen reflects the phase difference between these two paths. As the flux increases, the phase difference increases, and the fringes shift sideways.

The fringe shift is proportional to the flux. You can count the shift in fringe widths and read out the flux in terms of the flux quantum Φ₀ — without ever directly measuring a magnetic field.

## Why This Matters: Fields vs. Potentials

The Aharonov-Bohm effect is the clearest experimental evidence that electromagnetic potentials are not just mathematical auxiliaries in quantum mechanics — they have direct physical effects that fields do not.

In classical physics, if B = 0 in a region, a charged particle in that region feels no force and its trajectory is unaffected. The vector potential might be non-zero, but since F = qv × B = 0, the particle doesn't respond to it.

In quantum mechanics, the particle responds to the phase shift induced by the vector potential, even though no classical force acts on it. The interference pattern shifts even though the particle's trajectory, in the classical sense, is not deflected.

This is a genuine physical difference between classical and quantum dynamics — not an artifact of how we describe the system.

### SQUIDs: The Effect You Use Every Day

The most practical consequence of the Aharonov-Bohm effect is the SQUID — Superconducting Quantum Interference Device. A SQUID contains a superconducting ring interrupted by a Josephson junction. The critical current through the junction depends on the total magnetic flux threading the ring, which is measured in units of Φ₀.

Because the effect is topological — the phase shift depends on the winding number, not on the exact path — SQUIDs are extraordinarily stable and sensitive. Modern SQUID magnetometers can detect magnetic fields as weak as a few femtotesla (10⁻¹⁵ T). They are used in medical imaging (magnetoencephalography), geophysical surveys, and fundamental physics experiments.

## The Deeper Point: Topology Over Locality

What makes the Aharonov-Bohm effect especially striking is its topological character. The phase shift depends on the winding number — an integer that counts how many times the electron's closed path encircles the solenoid. Change the flux by any integer multiple of Φ₀, and the phase returns to its original value. The winding number is robust against continuous deformations of the path; only the topological information (whether the path encircles the coil or not) matters.

This topological sensitivity is what makes the effect so interesting for modern applications. It explains why the Aharonov-Bohm effect underlies the operation of SQUID magnetometers — the most sensitive magnetic field detectors available. It also appears in the physics of mesoscopic rings, where persistent currents can flow due to topological phase effects, and in certain formulations of geometric phase (Berry phase) in condensed matter systems.

The solenoid is a simple device. But the principle it illustrates — that quantum systems can be sensitive to the global topology of a situation in ways that classical physics cannot describe — has proven to be one of the most productive ideas in modern physics.

## The Counterintuitive Core

You place a solenoid between two slits. The magnetic field outside the solenoid is zero. You measure no force on the electrons. And yet the interference pattern shifts.

What is reaching across the empty space to affect the electron's phase? Nothing travels through the field-free region. The vector potential A does not carry energy or momentum in the classical sense. But it does carry phase information — in a way that is global, topological, and invisible to any local measurement.

The Aharonov-Bohm effect shows that the classical description of electromagnetic phenomena — fields and forces — is incomplete. In the quantum regime, the potentials themselves become the relevant quantities. And the way they affect particles depends not on what happens at any particular point, but on the topology of the entire path.

That is why the field you cannot see still changes the pattern.