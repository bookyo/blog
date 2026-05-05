# Why Atoms Walk Through Walls All the Time — and Why You Can't

There is a phenomenon happening inside every semiconductor chip in your phone, every flash memory card in your camera, and every STM microscope that images individual atoms. Particles are passing through barriers they classically have no energy to overcome. They are quantum tunneling — and it is the reason our entire digital civilization functions.

Your phone contains roughly 10²² atoms. Every one of those atoms is surrounded by electron clouds that are, at the quantum scale, continuously engaged in a form of transit that should be impossible according to everything Isaac Newton understood about the physical world. Electrons tunnel through potential barriers constantly. Not occasionally. Constantly. The transistor that switches your screen on and off works because electrons tunnel through gate oxides that are only a few nanometers thick.

The [Quantum Tunneling visualization at ElysiaTools](https://elysiatools.com/en/visualizations/quantum-tunneling) lets you experience this directly. Adjust barrier height, barrier width, and particle energy. Watch the probability density collapse and rebuild on the other side. The transmission coefficient — the fraction of the wave that makes it through — responds immediately to your changes. This is not an animation of a metaphor. This is the Schrödinger equation running in your browser.

## What Classical Physics Got Wrong

In the classical world, a ball thrown at a wall always bounces back. Give it energy E, encounter a barrier with potential V₀ greater than E, and you get reflection. Full stop. The math is clean, the intuition is obvious, and the result matches everyday experience with perfect reliability.

This is why it was so disorienting when, starting in the 1920s, physicists began encountering phenomena that refused to obey this rule. Radioactive alpha particles were escaping from atomic nuclei with energies lower than the nuclear potential barrier. The barrier should have trapped them completely. It didn't.

The resolution came from wave mechanics. In quantum mechanics, particles are not point objects following definite trajectories. They are described by wave functions — mathematical objects that assign a probability amplitude to every position in space. When this wave function encounters a potential barrier, it doesn't stop at the boundary. It penetrates.

Inside the barrier region, the wave function doesn't travel freely. It decays exponentially. But if the barrier is thin enough — thin relative to the decay length, which depends on the particle's mass and the energy deficit — some fraction of the wave emerges on the other side. The particle, having passed through territory it classically could never enter, reappears.

## The Mathematics That Makes Silicon Work

The transmission coefficient for a rectangular barrier has a clean closed form:

**T ≈ e^(-2κa)** where **κ = √(2m(V₀-E))/ℏ**

Where m is the particle mass, V₀ is the barrier height, E is the particle energy, a is the barrier width, and ℏ is the reduced Planck constant.

Notice what this equation says: tunneling probability falls off exponentially with barrier width. Double the width, and the transmission drops by a factor of e². Increase the barrier height, and the same exponential suppression applies.

This is why semiconductor engineers spend enormous effort controlling oxide thickness in transistors. At 10 nanometers, significant tunneling occurs — current leaks. At 1 nanometer, the leakage becomes catastrophic. This is the physical limit that is currently forcing the semiconductor industry toward new materials and new transistor architectures, because you cannot simply keep shrinking silicon dioxide gates forever.

The [ElysiaTools visualization](https://elysiatools.com/en/visualizations/quantum-tunneling) shows this relationship interactively. Move the barrier width slider and watch the transmission coefficient plummet exponentially. Change the particle energy and watch tunneling become more likely as you approach the barrier height.

## Why This Isn't Just a Curiosity

The applications are not fringe physics. They are the infrastructure of the modern world.

**Scanning Tunneling Microscopy (STM)** — The 1986 Nobel Prize in Physics went to Gerd Binnig and Heinrich Rohrer for inventing this device. An STM works by bringing a sharp metal tip to within a few angstroms of a conducting surface. A small voltage is applied, and electrons tunnel across the vacuum gap between tip and surface. The tunneling current is exponentially sensitive to distance — it falls off over a fraction of an angstrom. Scan the tip across the surface and you get a topographical map of individual atoms. This is the instrument that first let us see atoms directly. It works only because of quantum tunneling.

**Flash Memory** — Every flash memory cell stores bits by trapping charge on a floating gate — a conductor surrounded by insulating oxide. To write a bit, electrons are forced through the oxide barrier by tunneling. To erase, they tunnel back out. The entire NAND flash industry — worth hundreds of billions of dollars annually — depends on precisely controlling this process. Engineers calibrate write and erase voltages specifically to optimize the tunneling probability without damaging the oxide.

**Radioactive Decay** — The original puzzle that launched the field. Uranium-238 decays because alpha particles (helium nuclei) tunnel through the Coulomb barrier created by nuclear strong force. The half-life of uranium — 4.5 billion years — is a direct consequence of how difficult it is to tunnel out of the nucleus. The tunneling probability is extraordinarily small, which is why radioactive decay is slow enough for geological timescales but not slow enough to be irrelevant to nuclear engineering.

**PCR in Medicine** — Polymerase chain reaction, the technique underlying COVID tests, genetic sequencing, and most modern molecular biology, relies on heat-resistant DNA polymerase enzymes. Those enzymes work partly because quantum tunneling occurs during the proton transfer reactions that form the chemical bonds of new DNA strands. Tunneling accelerates certain biochemical reactions in ways that classical transition state theory cannot explain.

## The Interface Between Quantum and Classical

One of the most striking things about quantum tunneling is how sharp the classical-to-quantum transition is. The equations are unambiguous: tunneling probability is nonzero for any barrier, no matter how wide or high. A human being approaching a wall has an exponentially small but technically nonzero probability of appearing on the other side.

The barrier width for a person-sized object is on the order of meters. The mass of a human body is roughly 70 kilograms. Plugging these into the tunneling formula gives a transmission probability of approximately 10^(-10^35) — a number so close to zero that writing it out would require more zeros than there are atoms in the observable universe.

This is the classical limit in action. For macroscopic objects, quantum tunneling is not merely rare. It is effectively nonexistent. The transition occurs because Planck's constant ℏ is extraordinarily small — 1.05 × 10^(-34) joule-seconds — and the exponent 2κa depends on ℏ in the denominator. The smaller ℏ is, the more dramatic the exponential suppression for large objects.

But for electrons and atoms, ℏ is not small enough to suppress tunneling. At nanometer scales and electron mass (9.11 × 10^(-31) kg), tunneling is routine. This is why quantum effects dominate in the atomic and molecular world, and why classical mechanics is a sufficient approximation for bowling balls and planets.

## What the Visualization Actually Shows

The [Quantum Tunneling tool](https://elysiatools.com/en/visualizations/quantum-tunneling) gives you direct access to the wave function itself. Three regions are displayed: before the barrier (incident and reflected waves), inside the barrier (exponentially decaying wave), and after the barrier (transmitted wave). The relative amplitudes tell the story.

Try the wave packet animation — it shows how a localized particle wave packet behaves when it encounters the barrier. Some of the packet reflects. Some penetrates and decays. Some emerges on the far side. The transmitted portion is smaller but recognizable. This is not an approximation or a cartoon. This is what the Schrödinger equation actually does.

The probability density view shows |ψ|² — the probability of finding the particle at each position. Where the wave function is large, you are more likely to find the particle. Inside the classically forbidden region, the probability density is small but not zero. This is the region where, if you measured the particle's position, you might — with low probability — find it inside the barrier itself.

## The Deeper Point

Quantum tunneling is a reminder that our classical intuitions are shaped by the scale we live at. Objects large enough to see and touch behave classically because quantum effects are exponentially suppressed by scale. But at the atomic scale, the classical rules simply stop applying.

The same physics that seemed so shocking in the 1920s — particles appearing where they have no energy to be — is now engineering. It is the operating principle of devices that underpin trillion-dollar industries. The Nobel-winning STM, the flash memory in your phone, the radioactive decay that powers spacecraft in deep space: all of them run on the same quantum weirdness that made physicists uncomfortable a century ago.

Understanding tunneling doesn't make it less strange. But it does make it useful. And that is what physics, at its best, does: takes the deeply counterintuitive and finds a way to make it work.
