# Why Like Charges Repel and Opposites Attract: The Physics Behind Coulomb's Law

Two protons pushed close together will violently repel. Two electrons do the same. But drop a proton near an electron and they sprint toward each other. The universe has a simple rule: **like charges repel, opposites attract.**

Coulomb's Law quantifies this force. It describes every static electricity shock you've felt, every bolt of lightning, and every signal traveling through a semiconductor. It is F = k_e · |q₁q₂| / r² — the same inverse-square structure as Newton's gravity, but operating on a property called charge instead of mass.

## The Three Scenarios the Simulation Shows

The visualization demonstrates all three possible charge combinations:

**Positive–Positive:** Two protons. The force pushes them apart along the line connecting them. The stronger the charge or the closer the distance, the more violent the repulsion. This is why atomic nuclei — packed with positively charged protons — need the strong nuclear force to hold together. The electrostatic repulsion is trying to blow them apart.

**Negative–Negative:** Two electrons. Identical behavior — repulsion — but electrons are much lighter than protons, so they accelerate faster under the same force. This is why electron beams in old television CRTs could be steered so precisely: the same repulsion law applies, just with different mass.

**Positive–Negative:** A proton and an electron. Now the force reverses direction — it pulls them together instead of pushing apart. This is what holds atoms together. The electron orbits the proton in a hydrogen atom not because of gravity, but because opposite charges attract via Coulomb's Law.

## The Inverse Square: Why Distance Matters So Much

The r² in the denominator is the critical feature. Double the distance between two charges and the force drops to one quarter — not half. Triple the distance and you get one ninth the force. This inverse-square relationship is the same one that governs light intensity, sound pressure, and gravitational attraction.

This is why insulators (materials where charges can't move freely) can hold static electricity for hours. The electrons stuck on the surface of a balloon feel almost no force once they're even a few centimeters from the material that lost them. The force fades fast.

It also explains why semiconductors work. In a PN junction, positive "holes" and negative electrons are separated by a depletion zone of just a few micrometers. That small distance means the electrostatic attraction across the junction is strong enough to prevent carriers from crossing without a voltage threshold. Push the right voltage and you overwhelm the attraction — current flows.

## The Scaled Constant: Why k = 1000 in the Visualization

The real Coulomb constant is k_e = 8.99 × 10⁹ N·m²/C². This enormous number exists because charge in the SI system is measured in coulombs, where one coulomb is ~6.24 × 10¹⁸ electrons. Two electrons repelling with 1 coulomb each would produce roughly 10¹⁰ newtons of force — enough to accelerate a car from 0 to 100 km/h in a fraction of a second.

The visualization scales this down to k = 1000 for visual clarity. The *structure* of the law — inverse square, direction along the line of centers, sign determined by q₁q₂ — remains exactly the same. This is the fundamental thing Coulomb's Law tells us: force is proportional to the product of the charges and inversely proportional to the square of their separation.

## What the Force Vectors and Field Lines Reveal

Toggle "Show Force Vectors" and you see arrows pointing along the line connecting the two charges, pointing outward for repulsion and inward for attraction. Toggle "Show Field Lines" and you see the electric field pattern — field lines emerge from positive charges and converge on negative ones. The density of lines encodes the field strength: closer lines means a stronger field.

The field line pattern is why lightning bolts zigzag: the electric field doesn't smoothly decrease in all directions from a charge. Instead, it concentrates along paths where the field geometry creates a cascade of ionization in the air. The step leader of a lightning bolt is a guided ionization channel finding the path of least resistance toward the ground — all because the field is strongest along certain directions.

## The Energy Perspective

When two like charges drift apart, the system gains potential energy. When opposite charges attract and move closer, the system loses potential energy — energy that becomes kinetic, heat, or light. This conservation of energy is what makes the simulation visually coherent: watch the motion when you set "Enable Motion" on and see the kinetic energy convert back to potential as they bounce or collide.

The bottom display panel shows potential energy and force type in real time — watch how energy climbs as the charges separate under repulsion and drops as they fall together under attraction.

## The Three-Body Problem of Charge

The simulation works with exactly two charges. Add a third and the math becomes nonlinear — three charges mutually influencing each other's forces with no closed-form solution. This is why plasma physics (where countless charged particles interact simultaneously) requires computational simulation rather than formula-solving.

Every complex electromagnetic phenomenon — from tokamak fusion reactors to the ionosphere — is ultimately a many-body Coulomb problem solved by iteration. The two-charge simplicity of this visualization is the foundation for understanding all of them.