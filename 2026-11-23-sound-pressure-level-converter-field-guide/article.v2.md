---
title: 0 dB Is Not Silence. It's 20 Micropascals.
---

Silence on an SPL meter is not the absence of pressure. Zero decibels is a specific 20 micropascals, but 1 pascal reads 93.98 dB, not the round 100 most people expect. Two constants and one logarithm decide whether an acoustic number is a physical fact or an expensive opinion.

## One reference pressure, five units

Each dB SPL figure in the world leans on a single constant, defined by ISO 1683 as p0 = 20 micropascals, or 0.00002 pascal, RMS. According to that standard, the conversion is one line: Lp = 20 log10(p / p0), and the inverse is p = p0 × 10^(Lp / 20). Nothing else enters.

The converter at [Elysia Tools](https://elysiatools.com/en/tools/sound-pressure-level-converter) takes any of five units and hands back all five at once. Their factors to the pascal are short enough to memorize: Pa is 1, micropascal is 0.000001, microbar is 0.1, millibar is 100, and dB SPL is the reference itself.

That last entry is where mistakes cluster, and the worst case is simple. dB SPL is not a dimension like length or mass. It is 20 micropascals, wrapped in a logarithm. Type 1 into the Pa field and one click reports 93.98 dB SPL, 1,000,000 micropascals, 10 microbar, and 0.01 millibar.

## The 94 dB anchor, and why it isn't 100

The arithmetic shows both the anchor and the confusion. Taking 1 pascal against the reference gives 20 log10(1 / 0.00002) = 20 log10(50,000) = 20 × 4.69897 = 93.9794 dB. The calibration tone any acoustic engineer has seen on a sticker is that number, rounded to 94.

Then comes the accident that makes the scale feel arbitrary. The value 2 pascal lands on exactly 100.00 dB, because 2 divided by 0.00002 is 100,000, a clean power of ten. Two points, one decade apart, one of them round and one of them not.

The consequence is small but real. The pressure behind a calibrator stamped 94 dB is 1.0024 pascal, not 1.0000. Rounding it to 1 pascal cuts 0.02 dB from the reading, and against a quoted tolerance of "±0.1 dB" that spends a fifth of the budget before you measure anything.

## Doubling pressure is +6 dB. Doubling sources is +3.

Pressure is an amplitude, and that one fact forces the coefficient to 20 instead of 10. Power goes as pressure squared, so the power ratio inside a 10 log expression becomes a square inside the logarithm: 10 log10(p2 / p02) = 20 log10(p / p0).

So doubling pressure quadruples power and adds 6.02 dB. A factor of ten in pressure adds 20 dB, and 1 dB is a pressure factor of 1.122.

Two loudspeakers singing the same song are a different case. At a microphone in a real room their sound is uncorrelated, so their powers add and their pressures do not. That reduces the bump to 3.01 dB, not 6.02.

## Two 60 dB sources make 63 dB, not 120

This is the first place a raw conversion breaks a normal intuition, so the ladder is worth walking in order.

For example, one talker at 1 meter sits at 60 dB SPL, which is 0.02 pascal. Add a second talker with the same level and uncorrelated speech, and the sum in pascal is 10 log10(10^6 + 10^6) = 63.01 dB, a pressure of 0.0283 pascal. The room did not get twice as loud, because loudness follows the logarithm while the pressures added in quadrature.

Ten equal sources add 10 dB, so ten talkers reach 70 dB. A hundred add 20 dB, and 100 identical sources reach 80 dB. Each pair of 94 dB calibrators sums to 97.01 dB, not 188.

In each case the rule is the same: L + 10 log10(N) for N equal, incoherent sources. Coherent sources break it in the other direction. Two identical signals arriving in phase add pressure directly, reaching +6.02 dB per doubling, and two arriving a half wavelength apart cancel toward nothing.

## The unit field where answers go wrong

The five units are not interchangeable furniture. Microbar and millibar differ by a factor of 1000, a gap one keystroke wide, and changing that selector moves the answer by 60 dB. One microbar is 0.1 pascal, or 73.98 dB. One millibar is 100 pascal, or 133.98 dB.

Weather reports make the trap wider. A sea-level pressure of 1013 millibar is 101,300 pascal, which the converter dutifully reports as 194.08 dB. That figure is not a sound level. It is the weight of the atmosphere, and any reading near it means someone typed a barometric pressure into a sound pressure field.

The reference is the second trap. Air acoustics uses 20 micropascals; underwater acoustics uses 1 micropascal. Replace 20 with 1 and the same physical pressure measures 26.02 dB higher, so a 100 dB reading in water and a 100 dB reading in air sit 20 times apart in pressure.

The third edge is deliberate and easy to miss. Zero pascal returns negative infinity, because the logarithm of zero is undefined. Silence has no dB value, only a pressure of zero.

## Where the converter stops

Honest scope: the tool returns a pressure and its logarithm. It does not know your frequency weighting, so it cannot tell dB(A) from dB(C) or dB(Z). It does not know your time constant, so Fast, Slow, and Impulse readings all convert identically. It does not average a shift into an Leq, remove a distance term, or handle directivity.

It also cannot see whether your number is RMS or peak. The reference is RMS by definition. A sine wave at 94 dB RMS carries a peak pressure of 1.4176 pascal, which is 3.01 dB above the RMS value. Peak and RMS differ by that much on a pure tone and by more on anything with a sharp transient.

Distance is the gap that bites hardest in practice. In a free field, doubling the distance from a point source cuts the level 6.02 dB, as measured at the microphone. The converter never applies that correction, and no unit conversion can.

## The 194 dB ceiling

One atmosphere is 101,325 pascal, and the converter turns that into 194.09 dB SPL. Sound has an arithmetic ceiling right about there. At that level a sine wave's trough sits at absolute zero pressure, and anything stronger implies negative absolute pressure, which is not a wave but a shock front.

Put next to the 94 dB anchor, the ceiling is a neat hundred decibels higher: an entire atmosphere is 100.11 dB above a 1 pascal calibration tone. Rocket tests cross that line and report 194 dB and above. Loudspeakers do not, whatever the marketing page claims.

## What to write beside the number

A dB SPL figure without its reference is a number, not a measurement. Four words fix it: dB SPL re 20 µPa. Add the weighting, the time constant, the distance, and whether the value is RMS or peak, and the reading becomes checkable by anyone with a calculator.

The workflow that keeps you honest is convert, add, convert back. Build the sum in pascal, adding pressures in quadrature for uncorrelated sources and linearly for coherent ones, then convert back to dB. That single habit breaks the worst error in the field, which is averaging decibels directly.

For example, three readings of 70, 74, and 80 dB average to 74.67 dB by arithmetic, and that answer is wrong. The energy average, computed the same way as the two-talker sum, is 76.53 dB. The observed gap of 1.86 dB exceeds most measurement tolerances, and it grows with the spread of the readings.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

So what is the next question worth asking? Not what your meter reads, but what it is referenced to. Whether the number arrives in pascal, microbar, or decibel, it means one thing: a ratio against 20 micropascals. Hold that denominator and no acoustic reading can hide from you.
