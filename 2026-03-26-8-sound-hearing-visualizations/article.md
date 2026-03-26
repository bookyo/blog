# 8 Audio Physics Visualizations That Will Change How You Hear the World

Why does a siren's pitch drop the moment it passes you? Why do two slightly-off frequencies create a pulsing "beating" sound? Why does closing your eyes at a concert change how the music feels?

Sound is invisible — but it doesn't have to be. These 8 interactive visualizations make the physics of sound tangible, clickable, and playable with real audio.

---

## 1. Musical Intervals — See Why Harmony Sounds Good

When two notes play together, your brain isn't just hearing "two sounds." It's comparing ratios.

A perfect fifth (3:2 frequency ratio) sounds stable and resolved. A major third (5:4) sounds bright and happy. A minor third (6:5) sounds darker, sadder. The visualization shows you exactly why: simple frequency ratios produce harmonics that line up, while complex ratios create friction.

**Try it:** Hit "Play Interval" on the virtual piano keyboard. Watch the two waveforms add together. See how an octave (2:1) creates perfectly aligned harmonics while a tritone (√2:1) creates chaotic interference.

This is the same math behind every instrument, every chord, every harmony in every song you've ever heard.

🔗 [Explore Musical Intervals →](https://elysiatools.com/en/visualizations/musical-intervals)

---

## 2. Standing Waves — Where Sound Gets trapped

A standing wave is what you get when a wave reflects off a boundary and interferes with itself. The result: certain points ("nodes") stay perfectly still, while other points ("antinodes") oscillate at maximum amplitude.

This is exactly how guitar strings produce sound. The string vibrates at specific resonant frequencies — the 1st harmonic, 2nd harmonic, 3rd harmonic — each with a fixed pattern of nodes and antinodes. Pluck a string at different points and you excite different harmonics, which is why plucking near the bridge sounds brighter than plucking near the neck.

**The formula:** f_n = n × f₁. The nth harmonic's frequency is n times the fundamental. Adjust the harmonic slider from 1 to 5 and watch the pattern transform in real time.

The same physics applies to organ pipes, wine glasses, and the air in a microwave oven (don't do this).

🔗 [Explore Standing Waves →](https://elysiatools.com/en/visualizations/standing-wave)

---

## 3. Beat Frequency — Why Two Notes Creates a Pulsing Sound

Play 440 Hz and 442 Hz simultaneously. What you hear isn't two distinct pitches — it's one pitch with a rhythmic pulsing at 2 Hz. This is the "beat frequency," and it equals the difference between the two source frequencies: |f₁ - f₂|.

The visualization shows both waveforms separately, then their sum. The dotted envelope traces the amplitude modulation — the "loud-loud-loud" pulsing you hear.

**Why it matters:** Piano tuners use beat frequencies to tune instruments precisely. They listen for the beats to disappear completely. A guitar string is "in tune" when its frequency exactly matches the reference, producing zero beats.

Tuning fork preset: 440 + 442 Hz gives you a slow, deliberate 2-beats-per-second pulse. At 4 Hz the beating becomes nervous. At 8 Hz it's rapid and harsh.

🔗 [Explore Beat Frequency →](https://elysiatools.com/en/visualizations/beat-frequency)

---

## 4. Wave Superposition — How Waves Add and Cancel

Before you can understand beats, you need the foundation: what happens when two waves meet?

The principle of superposition is elegant: at any point, the combined amplitude equals the sum of individual amplitudes. Add a peak to a peak — you get a bigger peak. Add a peak to a trough — they can cancel completely.

**Constructive interference:** amplitudes align → larger amplitude. **Destructive interference:** peak meets trough → reduced or zero amplitude.

The interactive visualization lets you drag frequency, amplitude, and phase sliders independently for two waves and watch the third "resultant" wave update in real time. When frequencies are close, watch the beat pattern emerge naturally from the superposition.

This is the same math behind noise-canceling headphones (destructive interference), concert hall acoustics (constructive interference at some frequencies, destructive at others), and sonar.

🔗 [Explore Wave Superposition →](https://elysiatools.com/en/visualizations/wave-superposition)

---

## 5. Wave Reflection — What Happens When Sound Hits a Wall

Sound doesn't disappear when it meets a boundary. It reflects — but the reflection's behavior depends critically on whether the boundary is fixed (like a wall) or free (like the open end of a tube).

At a **fixed end**, the wave inverts on reflection. A pulse heading up a rope toward a wall comes back upside-down. This is why closed-end pipes only support odd harmonics (1st, 3rd, 5th...) — the closed end is always a node with zero displacement.

At a **free end**, there's no inversion. The pulse returns right-side-up. This is why open-end pipes support all harmonics — the open end is always an antinode.

Adjust the boundary type, pulse width, and amplitude, and watch the incident and reflected pulses animate in real time. The phase inversion at fixed ends becomes viscerally obvious.

🔗 [Explore Wave Reflection →](https://elysiatools.com/en/visualizations/wave-reflection)

---

## 6. Doppler Effect — Why the Siren Drops Pitch as It Passes

This is the one everyone "knows" but few truly feel. When an ambulance drives toward you, its sound waves compress — each successive wavefront leaves the source slightly closer to you than the last. Your ear receives them faster than the source is actually producing them. The pitch is higher.

When it passes and drives away, the distance is increasing. Wavefronts arrive slower. The pitch drops.

The formula for the approaching case: f' = f₀ × v / (v - v_s). For receding: f' = f₀ × v / (v + v_s).

The interactive visualization animates circular wavefronts from a moving source, color-coded by frequency (blue = higher pitch, red = lower). The real-time frequency display shows the exact shift as you adjust source velocity.

**Beyond sirens:** This same math explains why stars' light is redshifted as galaxies recede (proof of the expanding universe), why radar guns measure car speed, and why ultrasound tech measures your blood flow velocity.

🔗 [Explore the Doppler Effect →](https://elysiatools.com/en/visualizations/doppler-effect)

---

## 7. Sound Attenuation — Why You Have to Shout Across a Football Field

Sound doesn't just fade linearly with distance. It follows an inverse-square law in open space: double the distance, quarter the intensity.

I₀ / I = r² / r₀²

This means at 10 meters you might have 80 dB. At 40 meters (4× farther), you're down to roughly 68 dB. At 160 meters, you're at 56 dB. Each doubling of distance costs you about 6 dB.

Beyond geometric spreading, absorption in the medium (especially humid air) adds exponential decay: I = I₀ × e^(-αx). Fog, humidity, and temperature all affect how well sound travels outdoors.

The visualization shows a decibel meter that updates in real time as you adjust source intensity, distance, and medium type. It's the difference between whispering across a quiet library and shouting across a windy field.

🔗 [Explore Sound Attenuation →](https://elysiatools.com/en/visualizations/sound-attenuation)

---

## 8. Wave Refraction — Why Sound Bends Around Corners (Sort Of)

When a wave crosses from one medium to another, its speed changes. This causes the wave to bend — a phenomenon called refraction. The angle changes according to Snell's law:

n₁ × sin(θ₁) = n₂ × sin(θ₂)

In air, temperature gradients cause sound refraction: on a hot day, the air near the ground is warmer, so sound bends upward (warmer air = lower sound speed near ground = wave bends away from slower medium). On cold nights, the reverse happens — sound bends downward, which is why sound travels farther over cold water at night.

The visualization shows wavefronts crossing a boundary between two media with different wave speeds. Watch the wavelength compress on the slow side and expand on the fast side — while frequency stays constant (the source dictates frequency, not the medium).

This is the same principle behind lens optics, prisms splitting white light into rainbows, and why oceanographers can map the seafloor using sound.

🔗 [Explore Wave Refraction →](https://elysiatools.com/en/visualizations/wave-refraction)

---

## Sound Is Math You Can Hear

Every phenomenon in this list — harmony, beats, resonance, reflection, Doppler shifts, attenuation, refraction — is governed by a handful of mathematical relationships that have been understood for centuries. What makes ElysiaTools powerful is that it lets you *feel* them.

Most people interact with sound passively. Musicians, audio engineers, physicists, and acousticians interact with it actively. These visualizations close that gap — no equipment needed, no textbook equations to decode in the abstract.

The next time you hear a distant thunderclap, a hotel corridor that carries your conversation 30 meters down, or a perfectly in-tune guitar chord — you'll see the math behind the moment.

**Explore all 8 visualizations at [ElysiaTools.com](https://elysiatools.com) — completely free, no sign-up required.**
