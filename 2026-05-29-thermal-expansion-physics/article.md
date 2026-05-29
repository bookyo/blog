---
title: Why a 48-Millimeter Gap Stops Bridges From Collapsing: The Thermal Expansion Equation
---

## The Number That Prevents Bridge Collapses

Every structural engineer carries a number in their head: 12. Not a phone extension, not a safety factor — 12 parts per million per degree Celsius. That is the coefficient of thermal expansion for structural steel. A 100-meter steel bridge deck will grow 48 millimeters longer on a hot summer day than it was when engineers bolted it together in cooler weather. That number is small enough to ignore in casual conversation and large enough to buckle a bridge deck if the design doesn't account for it.

The same physics is operating in your mouth right now. The fine cracks in your tooth enamel — the ones dentists call craze lines — are not cavities. They are thermal fatigue fractures, the accumulated result of thousands of hot-cold cycles over decades. Coffee at 70°C, ice water at 5°C, repeat, for years. Enamel has roughly half the thermal expansion coefficient of the dentin beneath it, so when dentin contracts faster during cooling, it pulls on the enamel and creates those characteristic craze lines. Every crack is a thermal expansion event, frozen in place.

Thermal expansion is not a curiosity. It is a primary design constraint for bridges, railroad tracks, engine blocks, and space telescopes. The James Webb Space Telescope's 6-meter mirror had to maintain micron-level precision across a sunshield that shifts shape by millimeters as it cools to -233°C in deep space. Engineers succeeded because they designed *for* thermal expansion, not around it.

## One Equation, Three Scales

The core formula fits on one line:

**ΔL = α · L₀ · ΔT**

ΔL is the change in length, L₀ is the original length, ΔT is the temperature change, and α is the **linear coefficient of thermal expansion** — a material-specific constant that tells you what fraction of its length a material gains per degree. For steel, α ≈ 12 × 10⁻⁶ /°C. For aluminum, α ≈ 23 × 10⁻⁶ /°C. For glass, α ≈ 9 × 10⁻⁶ /°C.

Multiply these small numbers by a 100-meter bridge deck and a 40°C temperature swing and you get 48 millimeters of growth. That doesn't sound dramatic — but the bridge has nowhere to go except upward or against its neighbors. Without expansion joints, the compressive stress would buckle the deck. The same principle scales to two other geometries: **area expansion** uses β ≈ 2α, and **volume expansion** uses γ ≈ 3α. A copper pot lid that fits snugly when cold will seal itself permanently when heated, because the lid's diameter expands faster than the pot's opening. This is not a defect. It is the equation behaving exactly as predicted.

## What the Simulation Shows

The interactive model below simulates a 1-meter bar heated from 20°C to 70°C. You can select from six materials: aluminum, copper, steel, glass, concrete, and water.

At the magnification used in the simulation, aluminum's expansion is clearly visible — the bar grows by over a millimeter. Steel expands less than half as much. Glass barely registers a change. Water behaves anomalously: it contracts when heated from 0°C to 4°C (the same property that causes ice to float), then expands normally above 4°C. The coefficient comparison chart makes the relative differences between materials immediately visible. The length-vs-temperature graph is a straight line across all six materials — thermal expansion is linear, which is why a single equation captures it completely.

## Three Cases Where It Matters

**Railroad tracks** are laid in sections with deliberate gaps between rails. In the 19th century, when engineers didn't yet account for thermal expansion systematically, track buckling was a routine and dangerous problem. Modern high-speed rail avoids this through continuous welded rails tensioned at a calculated "neutral temperature" — pre-stressing the rail so that thermal expansion and contraction from that baseline produces manageable forces rather than destructive buckling. The neutral temperature is chosen so the rail is in mild tension in summer and mild compression in winter, keeping forces within the rail's design envelope year-round.

**The Bessemer process** shows the reverse effect being useful. Molten steel poured into a mold and cooled by water spray contracts on the outer shell first, leaving the inner core in tension. This creates compressive residual stresses that make the finished steel harder and tougher than if it had cooled uniformly. Thermal contraction doing useful structural work — engineered, not accidental.

**Dental craze lines** are the same physics at a smaller scale. Enamel and dentin have different coefficients of thermal expansion. Over years of hot-cold cycles, the differential contraction between these two bonded materials creates the characteristic fine cracks. Dentists call them craze lines. They are not decay, but they are evidence of thermal fatigue operating on a bonded material pair that any materials engineer would recognize immediately.

## The Atomic Origin

At the atomic scale, thermal expansion is a direct consequence of how atoms vibrate in bonds. Heat a material and atoms vibrate more vigorously, pushing each other further apart on average. Stronger bonds mean less expansion per degree — which is why tungsten, with its extremely strong atomic bonds, has one of the lowest coefficients of any pure metal. Invar, an iron-nickel alloy, is even more remarkable: it has a near-zero coefficient of thermal expansion at room temperature, discovered through systematic alloy research because engineers needed a material that would not expand noticeably across normal temperature ranges. It is used in precision balances, metronomes, and quartz crystal mounts — every time a watch keeps accurate time, it is in part because of an engineered alloy that thermal expansion cannot easily perturb.

## The Bigger Picture

The coefficient α varies with temperature — it is not truly constant, just approximately constant over limited ranges. The Clapeyron equation for phase transitions includes a volume-change term precisely because expansion behaves differently on either side of a phase boundary. When water freezes, it expands by about 9% — the opposite of almost every other liquid-solid transition, and the reason ice floats. Every expansion joint in every bridge is a daily reminder that this anomalous property of water determines which life forms can survive in a frozen lake.

The bridges have their gaps because atoms push each other apart when heated, because bond strength determines how much, because engineering that ignores this collapses. Next time you feel a craze line on a tooth or walk across an expansion joint, you are feeling the thermal expansion equation operating at human scale — the same one that governs whether a space telescope holds its shape in deep cold, whether a pot lid seals itself when heated, and whether a copper wire breaks when you cool it too fast.
