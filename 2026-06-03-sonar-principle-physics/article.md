---
title: Why Every Submarine Uses Sound to "See" Through the Ocean
---

On a December night in 1918, a British ship dropped a explosive charge into the Celtic Sea. Divers were out of the question — the water was dark, cold, and hostile to light. But something else was there to listen. The sound traveled outward at 1,500 meters per second, hit the seabed, and returned. From that round-trip time, naval officers calculated depth, range, and the contours of a war they were winning beneath the waves.

That technique is sonar — Sound Navigation and Ranging. It is the dominant sensing method in underwater environments, not because it is the newest or most sophisticated, but because water is opaque to everything except sound.

## Why Light Fails Underwater

Light behaves differently in water than in air. Blue light penetrates furthest — roughly 30 meters on a clear day — before scattering into nothing. Red light vanishes within a few meters. This is not a minor inconvenience; it is a fundamental physical limit. An underwater camera can illuminate only what is very close, and what is very close is usually not what you need to detect.

Sonar sidesteps this problem entirely. Sound at 40 kHz — the typical frequency for naval echolocation — propagates tens of kilometers through seawater. The physics is straightforward: the speed of sound in water (~1,500 m/s) is roughly 4.5 times faster than in air (~343 m/s), and absorption losses are low at these frequencies. The tradeoff is resolution — wavelength and frequency set the diffraction limit. But for range-finding at ocean scale, this is an acceptable compromise.

## How the Ping Works

The sonar equation is simple in structure. A pulse of sound radiates outward from a transducer as a spherical wavefront:

```
Time of arrival = 2 × distance / sound_speed
```

The factor of two accounts for the round trip: outward to the target, then back. If sound travels at 1,500 m/s and the echo returns after 4 seconds, the object is 3,000 meters away.

The actual physics in the simulation works as follows. At each time step, the code computes:

```
radius(t) = soundSpeed × (t − t₀)
```

Where `t₀` is the emission time. As the wavefront expands, it reflects off surfaces and returns to the source, carrying information about what it encountered. The simulation models this via the `sendPing()` method, which emits a wavefront and tracks its expansion as a series of expanding circles emanating from the transducer.

The wavelength matters for resolution. At 50 kHz with sound speed 1,500 m/s:

```
λ = 1500 / (50 × 10³) = 0.03 m = 3 cm
```

This sets the approximate diffraction limit — objects much smaller than 3 cm cannot be reliably resolved at that frequency. Higher frequency means better resolution but shorter range, since absorption increases with frequency.

## The Range Equation

Not all sound returns with equal strength. The sonar equation captures this:

```
SNR = SL − TL − NL + DI
```

Where:
- **SL** (Source Level): how loud the ping is
- **TL** (Transmission Loss): geometric spreading + absorption
- **NL** (Noise Level): ambient ocean noise
- **DI** (Directivity Index): how focused the beam is

Transmission loss has two components. Geometric spreading — the spherical wave losing intensity as it expands — accounts for the 20 log₁₀(R) term. Absorption — conversion to heat — is frequency-dependent. At 50 kHz, absorption is roughly 3–5 dB per kilometer. At 200 kHz, it climbs to 20+ dB per kilometer, sharply limiting range.

This is why naval sonar uses 10–40 kHz for long-range detection while fish finders use 100–200 kHz for near-field precision. The physics is not negotiable: higher frequency gives sharper images but dies faster in water.

## What Sonar Detects

The simulation models three principal target types:

**Specular reflectors** act like mirrors — they return strong echoes when the sonar beam hits head-on, and weak echoes at oblique angles. The returned signal strength follows a Lambertian or specular model depending on surface roughness.

**Volumetric scatterers** — fish schools, bubble clouds, plankton layers — return a diffuse echo spread across a range of angles. The collected signal is an incoherent sum of many small reflectors, producing a characteristic texture in the echogram.

**The seabed** acts as a boundary reflector. The echo strength depends on bottom composition (sand, mud, rock) and the grazing angle. Steeper angles produce stronger returns, a fact used in sub-bottom profilers to image sediment layers beneath the seafloor.

## Why the Delay Is Everything

The most elegant part of sonar is that it never measures distance directly. It measures time. The physics of wave propagation provides the conversion factor — sound speed in water is well-characterized and approximately constant at 1,500 m/s for typical ocean conditions (temperature ~10°C, salinity ~35 ppt, depth ~100 m).

This substitution — time for space — is what makes sonar powerful. A 4-second two-way travel time tells you the target is 3 kilometers away, without ever having to see it, photograph it, or illuminate it with anything faster than sound.

The ping travels at 1,500 meters per second through water — fast enough to cross the Atlantic and back before you finish reading this sentence. That speed is not incidental. It is why sonar works at all: the delay between transmission and return encodes distance, and distance encodes everything from submarine positions to seafloor topology.

What makes sonar elegant is that it measures time to get space. No direct measurement of distance is needed — just a precise clock and a medium where speed is known. That single substitution (time for space) is what makes sound the dominant sensing modality underwater, where light fails and radio waves cannot reach.