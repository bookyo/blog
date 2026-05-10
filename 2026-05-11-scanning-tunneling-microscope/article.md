# See Atoms with Your Own Eyes: The Scanning Tunneling Microscope

In 1981, two IBM researchers held a metal needle so finely sharpened that its tip was literally one atom wide. They brought it close enough to a piece of gold — less than a nanometer, about the width of a strand of DNA — and something remarkable happened. Electrons tunneled through the vacuum gap between the needle and the surface. By measuring that current, they could map the location of individual atoms.

That invention — the Scanning Tunneling Microscope — won Gerd Binnig and Heinrich Rohrer the 1986 Nobel Prize in Physics. For the first time in history, humans could see atoms in real space.

Today, you can run a real STM simulation right in your browser, adjusting bias voltage, switching between constant-current and constant-height modes, and watching electrons tunnel across a graphene surface.

## The Core Insight: Exponential Sensitivity

The fundamental equation governing STM is deceptively simple:

I ∝ V · exp(-2κd)

The tunneling current I depends exponentially on the tip-sample distance d. A change of just 0.1 nanometers — one-tenth the diameter of a hydrogen atom — produces a tenfold change in current. This extreme sensitivity is what makes atomic resolution possible.

In constant current mode, the STM's feedback system adjusts the tip height to maintain a fixed current as it scans. The tip height then traces the surface topography at atomic resolution. In constant height mode, the tip stays fixed and current variations reveal the local electronic structure — a map of electron density rather than geometry.

## The Three Numbers That Define Every STM Experiment

Every STM operation boils down to three parameters:

- **Bias voltage (V)**: Typically 10mV to 2V. Sets the energy of tunneling electrons and determines whether you're probing filled or empty electronic states.
- **Setpoint current (I₀)**: Usually 1–10 nA. Defines the "touch" the microscope maintains — lower currents mean less disturbance of delicate surfaces.
- **Tip-sample distance (d)**: Approximately 0.5–1 nm. This is the vacuum gap electrons must tunnel through. The entire instrument is designed to control this distance to sub-picometer precision.

## What You Can Actually Do with the Visualization

The interactive STM tool gives you hands-on control over these parameters and more:

**Material presets** let you switch between graphene, silicon (111), gold (111), and copper (111) surfaces — each with different electronic properties and atomic spacings. Graphene's hexagonal lattice is particularly striking; you can watch the honeycomb pattern emerge as the scan rasterizes across the surface.

**Spectroscopy mode** reveals the local density of electronic states at a specific surface location. As you sweep the bias voltage, the dI/dV curve exposes energy gaps, resonances, and the quantum states unique to that material.

**Scan size and speed** let you explore at different scales — from large-area surveys showing step edges and terraces, down to atomically resolved imaging where individual atoms appear as bright spots separated by the characteristic lattice constant of the material.

## Why This Matters Beyond the Nobel Trophy Case

STM is not just a microscopy technique. It is a platform for quantum manipulation. The most famous demonstration came in 1989, when Don Eigler used an STM tip to drag 35 xenon atoms across a nickel surface and spell "IBM" — a stunt that required moving atoms one by one using the same tunneling current that powers imaging.

In 1993, researchers built a "quantum corral" — 48 iron atoms arranged in a circle on copper. The surface electrons inside the corral formed a standing wave pattern, confirming that electrons behave as quantum waves. This was literally watching quantum mechanics unfold at human-visible scales.

Today, STM is finding new relevance at the frontier of quantum materials:

- **Topological insulators**: STM maps the protected surface states that conduct electricity without resistance.
- **Superconductors**: Vortices in high-Tc superconductors are directly imaged, revealing the pairing symmetry of Cooper pairs.
- **2D materials**: Graphene, MoS₂, and boron nitride are routinely characterized at atomic resolution, including the twist-angle engineered "moiré" patterns in magic-angle graphene.

## The Instrument in Your Browser

The practical challenge of building a real STM is instructive: it requires ultra-high vacuum (~10⁻¹⁰ mbar), vibration isolation better than 0.01 nm, and a tip sharpened to single-atom sharpness. No wonder most people never interact with one directly.

The visualization sidesteps these engineering barriers. It demonstrates the core physics — the exponential tunneling current, the two imaging modes, the spectroscopic response — in an interactive form factor. You can develop intuition for how STM works by varying parameters and watching the results, which is more than you can say for reading about it in a textbook.

Try setting a low bias voltage with a large tip-sample distance, then slowly decreasing the gap. Watch how the tunneling current — too small to detect at large distances — suddenly appears and then grows explosively as you cross the atomic-scale threshold.

That exponential curve is the entire basis of atomic-resolution microscopy. Now you can feel it for yourself.

---

*Explore the interactive STM simulation at [ElysiaTools](https://elysiatools.com/en/visualizations/stm-microscope).*