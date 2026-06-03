---
title: Why Every Sharp Point Builds a Field It Cannot Contain
---

The same physics that makes your hair stand up near a Van de Graaff generator is hard at work inside every lightning rod, photocopier, and smoke-stack precipitator. It is called **point discharge** — and it begins the moment geometry becomes extreme.

On a smooth sphere, surface charge spreads evenly. On a needle tip, there is almost no surface — so the charge density becomes enormous. The electric field at the surface follows a simple rule: *E = σ/ε₀*, where σ (sigma) is the surface charge density. Squeeze charge onto a tip with a radius of one millimeter and σ shoots up. Squeeze it onto a tip of one micrometer and the field strength crosses a fundamental threshold.

That threshold is the **dielectric strength of air** — roughly 30 kilovolts per centimeter. At that field strength, air molecules ionize. Electrons are torn from their orbits, accelerated, and collide with other molecules, creating a cascade. The air stops being an insulator and starts being a conductor. What happens next depends on the voltage: a faint blue-violet corona glow at moderate excess, or a visible spark when the field really climbs.

This is the same breakdown that lights the sky during thunderstorms — just happening on a scale of millimeters instead of kilometers. A lightning rod does not attract lightning by magic. It creates a region where the local field is so concentrated that the air breaks down preferentially, providing a conductive channel for charge to dissipate safely into the sky.

The polarity matters. A **positive corona** — where the tip is positively charged — produces a more diffuse, less luminous discharge. A **negative corona** from a negatively charged tip generates more intense localized ionization and a brighter visible glow. Both are used in industrial contexts, but they behave differently, and understanding which one you have determines whether you are designing a lightning protection system or an electrostatic precipitator.

The shape of the conductor is the entire story. A sphere of radius *r* at voltage *V* produces a surface field of roughly *V/r*. Halve the radius, double the field. A needle tip with a radius of 0.1 mm produces a field 100 times stronger than a sphere of 10 mm at the same voltage. This geometry-electric field relationship explains why smooth surfaces hold charge quietly while sharp points seem to leak it into the surrounding air — literally, through ionized corona.

The practical applications are everywhere. **Lightning rods** exploit the concentration effect to provide a preferred discharge path during storms. **Electrostatic precipitators** use corona discharge to charge dust particles in industrial smokestacks, then pull them toward oppositely charged collection plates. **Photocopiers** and laser printers charge the photoconductive drum via corona wires. Even the **Van de Graaff generator** — the classic science museum machine that makes your hair stand on end — relies on corona at its collecting comb to transfer charge onto the moving belt.

One formula ties all of these together:

> **E_breakdown ≈ 30 kV/cm** (in dry air at standard temperature and pressure)

When the local field at a conductor surface exceeds this value, you get ionization. The air becomes plasma. Charge bleeds away.

The reason this matters beyond the laboratory is scale. At sea level, the breakdown threshold is about 30 kV/cm. At high altitude, where air is thinner, the threshold drops — which is why corona discharge happens more easily in low-pressure environments. This is why high-voltage power lines buzz and crackle on humid days: the moisture in the air reduces the effective breakdown threshold, making corona more likely.

Engineers who design high-voltage systems spend a great deal of time managing this effect. They choose conductor radii carefully, smooth joints, and use corona rings — metal rings placed at the ends of high-voltage transmission hardware — to distribute the field and prevent localized breakdown. Without these design choices, the concentrated fields at hardware terminations would erode conductors and waste power continuously through silent corona losses.

Point discharge is one of the clearest examples of how purely geometric properties — curvature, radius, shape — determine whether a system quietly holds charge or actively discharges it into the surrounding medium. No other variable matters as much. Change the geometry, and the field follows.

The same principle that makes lightning rods work — charge accumulating at sharp points — shows up everywhere from electrostatic precipitators that clean factory smoke to the photocopier that once made every office hum with ozone. At its core, point discharge is just physics doing what physics does: geometry shapes field. A sphere spreads charge across its surface. A needle concentrates it at the tip. And when that concentration crosses the breakdown threshold — about 30 kilovolts per centimeter in air — the air itself becomes a conductor, and corona forms. The world doesn't need complicated machinery to move charge. It just needs a sharp point and enough voltage to let geometry do the rest.