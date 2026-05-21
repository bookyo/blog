# Why Colloidal Gold Stays Suspended: The DLVO Theory Behind Nanoparticle Stability

The gold nanoparticles in your lab have been floating in solution for six months. No settling, no clumping. You adjust the pH slightly — and they aggregate overnight. What changed?

The answer lives in a theory developed independently by two pairs of scientists in the 1940s: Derjaguin and Landau, Verwey and Overbeek. Together, their framework explains why some particles stay suspended indefinitely while others coalesce into aggregates. It's called **DLVO theory**, and it predicts the stability of colloidal systems with a simple idea: all particles in liquid experience two competing forces — electrostatic repulsion and van der Waals attraction.

## The Two Forces Every Particle Feels

Imagine two charged nanoparticles approaching each other in water. As they draw closer, two things happen simultaneously.

**Van der Waals attraction** is always present. It arises from correlated fluctuations in the electron clouds of atoms on each particle surface. Every material experiences it. The Hamaker constant for gold is around 3–5 × 10⁻¹⁹ J — a small number, but it adds up across millions of atoms. The attraction grows stronger as particles get closer, following a power law that makes it negligible at large separations but overwhelming at atomic scales.

**Electrostatic repulsion** emerges from the electrical double layer. Most particles in aqueous solution carry surface charge — from ion adsorption, surface group dissociation, or electron transfer. In water, counter-ions cluster around each charged surface, forming a diffuse cloud. When two particles approach, their double layers overlap, and the resulting osmotic pressure pushes them apart. The characteristic decay length of this pressure is the **Debye length**, which shrinks as ionic strength increases.

The total interaction energy is the sum of these two contributions. And it produces a curve with a distinctive shape.

## The Energy Curve: A Roadmap of Particle Behavior

Plot the total interaction energy between two identical particles against their center-to-center distance, and you get a curve with at least two distinct features:

**A primary minimum** at very short range (typically under 1 nm). Here, van der Waals attraction dominates completely. Particles that fall into this minimum form irreversible aggregates — what chemists call coagulation. Breaking free would require energy greater than the depth of the well.

**An energy barrier** in the intermediate range. This is the obstacle that keeps stable colloids suspended. If the barrier is large enough relative to thermal energy kBT (roughly 4 × 10⁻²¹ J at room temperature), particles cannot surmount it. They bounce off each other like molecules in an ideal gas, remaining in stable suspension indefinitely.

**A secondary minimum** at larger separations, which is shallower and longer-ranged. Particles can fall into it temporarily, forming loose reversible aggregates called flocs — but thermal agitation or gentle stirring can break them apart again.

The height of the barrier relative to kBT is the key metric in DLVO theory. A barrier of 10–15 kBT at room temperature is considered the threshold for long-term stability. Below 5 kBT, aggregation proceeds rapidly.

## Why pH and Ionic Strength Matter

The energy barrier is not fixed. Two parameters have outsized influence:

**Zeta potential** — the electrical potential at the slipping plane of the double layer — controls the magnitude of electrostatic repulsion. A zeta potential above roughly ±30 mV typically confers good stability. Near the isoelectric point, where zeta potential approaches zero, the barrier collapses and particles aggregate rapidly.

**Ionic strength** determines the Debye length. Adding salt compresses the double layer, reducing the range of electrostatic repulsion. In the classic Schulze-Hardy rule, the coagulating power of different electrolytes follows their valency: trivalent ions are roughly 1000× more effective at destabilizing colloids than monovalent ions.

This is why simply adding table salt (NaCl) to a stable gold nanoparticle solution causes immediate aggregation. The electrolyte screens the surface charge and collapses the repulsive barrier.

## DLVO in the Real World

DLVO theory was developed to understand industrially important systems: inks, paints, ceramics, pharmaceuticals. But its applications extend further.

**Water treatment** relies on deliberately breaking colloidal stability. Adding alum (Al³⁺) or ferric chloride (Fe³⁺) introduces high-valency counter-ions that compress double layers and neutralize charges, allowing suspended particles to aggregate and settle.

**Pharmaceutical formulation** of colloidal drug carriers (liposomes, polymeric nanoparticles) requires careful control of ionic strength and pH to maintain stability in biological fluids, where electrolyte concentrations are high.

**Soil science** uses DLVO concepts to understand how clay particles aggregate or remain dispersed in response to pore-water chemistry — directly affecting water retention and permeability.

## Where DLVO Breaks Down

DLVO theory has limits. It treats particles as rigid spheres with smooth surfaces, and it assumes that only electrostatic and van der Waals forces matter. In practice, several additional forces can dominate:

**Steric hindrance** from adsorbed polymers or surfactants can provide additional stabilization far beyond what DLVO predicts. Many "sterically stabilized" colloids remain stable at ionic strengths that would completely destabilize a purely electrostatic system.

**Hydration forces** near hydrophilic surfaces can create repulsive barriers that DLVO misses entirely.

**Roughness and heterogeneity** on real particle surfaces alter the functional form of both the attractive and repulsive potentials.

For the gold nanoparticles in your lab, the most likely explanation for their six-month suspension is a combination of electrostatic stabilization (surface charge creating a barrier of 15+ kBT) and possibly steric stabilization from citrate or polymer capping agents commonly used in synthesis.

The moment you adjusted the pH, you moved the surface charge toward its isoelectric point — and the barrier dropped below the threshold. The rest was thermodynamics.
