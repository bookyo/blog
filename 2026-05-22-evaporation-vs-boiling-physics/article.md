# Why Your Laundry Dries at Room Temperature: The Physics of Evaporation and Boiling

Open a pot of water on the stove and it bubbles violently at 100°C. Leave your laundry hanging on a line and it dries at 20°C. Same substance — water. Same process — a liquid turning into gas. But one requires intense heat, and the other happens silently in the background of everyday life. The difference is not magic. It is a matter of pressure, energy, and where exactly molecules decide to make their escape.

This is the story of two phase transitions that look identical from a distance but operate on completely different physical rules.

## The Surface Phenomenon: How Evaporation Works

When you hang wet clothes to dry, you are watching evaporation in action. No bubbles form. No steam rises in dramatic columns. Molecules at the surface of the water absorb energy from the surrounding air and from collisions with their neighbors. When a molecule near the surface picks up enough kinetic energy to overcome the attractive forces holding it in the liquid, it breaks free and escapes into the air.

This happens at *any* temperature. Even ice-cold water evaporates, albeit slowly. The molecules in a glass of water at 20°C follow a Maxwell-Boltzmann distribution of kinetic energies — some have very low energy, some have very high energy. The ones with the highest energy are the ones most likely to escape. Evaporation is, fundamentally, a selection process: the fastest molecules leave, and the ones left behind are, on average, slightly cooler. This is why a breeze feels cold on wet skin — the wind carries away the escaped molecules, preventing the vapor from recondensing and releasing its latent heat back onto your skin.

The heat of vaporization for water at 25°C is approximately **2,260 kJ/kg**. That is the energy required to turn one kilogram of liquid water into vapor at the same temperature — not to heat it, just to change its phase. It is a staggeringly large number. To evaporate a single kilogram of water at room temperature requires roughly the same energy as lifting a car three meters off the ground.

## When the Whole Liquid Goes Mad: The Physics of Boiling

Boiling is categorically different. At boiling point, the vapor pressure inside bubbles formed within the liquid equals the ambient external pressure. When that happens, the bubbles are no longer crushed by the weight of the surrounding water. They expand rapidly, rise, and burst at the surface. That is the churning pot of boiling water you see on the stove.

The key condition for boiling is not a specific temperature — it is a specific *pressure equality*. At standard atmospheric pressure (1 atm, approximately 101.3 kPa), water boils at 100°C. But climb to high altitude where the pressure is lower, and water boils at a lower temperature. In Denver, the "Mile High City," atmospheric pressure is about 83 kPa and water boils at approximately **94°C**. This is why high-altitude cooking requires adjustments: the boiling point is lower, so foods that rely on prolonged submersion in boiling water take longer.

Conversely, increase the pressure and the boiling point rises. In a pressure cooker, where pressure can reach 2 atm (about 200 kPa), water does not boil until approximately **120°C**. This higher temperature cooks food significantly faster, which is why pressure cookers became kitchen staples long before home cooks understood the thermodynamics behind them.

The relationship between pressure and boiling point is not linear. The simplified calculation in the interactive simulation uses a log-pressure factor:

```
Boiling Point ≈ 100°C + (ln(pressure / 1 atm) × 25°C)
```

This logarithmic dependence means that even modest pressure changes produce noticeable shifts in boiling temperature. At 0.5 atm, water boils at about 83°C. At 2 atm, it boils at about 117°C. The curve is steep at low pressures and flattens at high pressures.

## Why the Distinction Matters

Understanding the difference between evaporation and boiling is not merely academic. It shapes how engineers design cooling systems, how chefs approach high-altitude baking, how meteorologists model humidity, and how power plant engineers design steam turbines.

In cooling towers — the tall hyperbolic structures next to nuclear power plants — water is circulated to absorb heat, then exposed to ambient air where it evaporates partially. Evaporation is the cooling mechanism, not boiling. The water temperature in the basin is well below 100°C; the cooling happens precisely because each kilogram of evaporated water carries away 2,260 kJ of heat from the remaining water. A large power plant cooling tower can evaporate thousands of tonnes of water per hour, transferring enormous amounts of heat in the process.

In semiconductor fabrication, controlled boiling is used in a technique called **pool boiling**, where silicon wafers are heated in a bath of dielectric fluid. The formation and departure of bubbles at the heater surface creates a highly efficient heat transfer regime. The transition from smooth boiling to vigorous nucleate boiling — and the eventual onset of critical heat flux where vapor blankets the surface and dramatically reduces heat transfer — is a major concern in thermal management design.

## The Phase Diagram Connection

Both evaporation and boiling are manifestations of the same underlying physics described by the **phase diagram** of water. Every point on that diagram represents a specific combination of temperature and pressure where water exists in equilibrium — as a liquid, as a solid, or as a gas. The boundary between the liquid and gas phases is called the **phase boundary** or **coexistence curve**. Evaporation describes movement across that boundary at temperatures below the critical point when the vapor pressure is less than atmospheric pressure. Boiling describes the same crossing when the vapor pressure equals ambient pressure.

Water's phase diagram has a distinctive feature: its melting and boiling lines have a negative slope in a particular pressure range — a consequence of the fact that ice is less dense than liquid water. This is why ice floats, and it is the same physics that allows ice skaters to glide: the pressure of the blade on the ice melts a thin film of water beneath it, providing lubrication.

## The Interactive Simulation

The simulation lets you manipulate two parameters: temperature and pressure. Watch how changing pressure shifts the boiling point in real time. Increase pressure to 1.5 atm and observe the bubbles forming at a higher temperature. Drop it to 0.7 atm and watch boiling begin at around 91°C — visibly different from the 100°C you expect at sea level.

Evaporation, being a surface phenomenon, responds differently. It is always happening, but raising the temperature accelerates it by increasing the fraction of molecules with enough energy to escape. The high-energy molecules in the simulation are colored red; low-energy ones are blue. Watch how the red fraction grows as temperature increases, and how the escaped molecule count climbs.

The most counterintuitive thing the simulation reveals: evaporation is not stopped by cold. It slows, but molecules continue to escape as long as the air above the surface is not saturated with vapor. This is why frost can form on a cold window while the glass is still evaporating moisture from the room. The vapor pressure gradient drives the process regardless of temperature — it just moves faster when things are warm.

## What Stays With You

Two processes, one substance, two very different sets of rules. Evaporation is a surface-level escape, driven by the energetic tail of the molecular distribution, happening at any temperature. Boiling is a volumetric transformation, requiring that vapor pressure inside bubbles match external pressure — a condition that occurs at a temperature that depends on altitude, weather, and whether you are using a pressure cooker.

The next time you watch a pot come to a boil, or notice that the laundry has dried even on a cloudy afternoon, you are watching these two physical stories unfold in parallel. One is gentle and constant. The other is explosive and threshold-driven. Both are water leaving the liquid phase. Both are driven by the same fundamental impulse: molecules seeking a state of lower density and higher entropy. The difference is entirely a matter of whether they are pushing against a surface or against the weight of an entire atmosphere.
