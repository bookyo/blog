# Why Your Body Is Already a Thermoelectric Generator (And Why NASA Uses the Same Physics for Deep Space)

The Voyager 1 probe is more than 23 billion kilometers from Earth. It is still running — not because of solar panels, but because of a chunk of plutonium and a physical effect that has been hiding inside your body the entire time. That effect is the thermoelectric effect, and it converts heat directly into electricity without any moving parts.

Forty-seven years after launch, Voyager's radioisotope thermoelectric generator (RTG) is still putting out about 250 watts. No solar panel at that distance could collect enough sunlight to matter. The RTG works because heat flows through special materials and some of that heat energy spontaneously becomes electricity. Your body runs the same trick internally, using the exact same Seebeck effect that NASA exploits in deep space.

## Three Effects, One Physical Origin

Thermoelectricity is not one effect — it is three, and they all flow from the same underlying reality: charge carriers in a material carry both electrical current and heat current. When a temperature difference exists across two different materials joined together, electrons or holes drift from the hot side to the cold side, creating a voltage. That is the **Seebeck effect**, discovered by Thomas Seebeck in 1821.

Flip the picture around. Run an electrical current through the same junction and you can pump heat from one side to the other, cooling the cold side. That is the **Peltier effect**, discovered the same year. The third effect — **Thomson cooling** — is more subtle: a current-carrying wire that also has a temperature gradient along its length either absorbs or releases heat depending on the direction of current flow relative to the temperature gradient.

The three effects share a common origin in the fact that electrons at different energies carry different amounts of entropy. When they diffuse from hot to cold, they carry extra entropy with them. This is why thermoelectric materials always generate voltage in proportion to temperature difference, and why running current through them always moves heat — the two processes are thermodynamic mirrors of each other.

## The Key Equation: Seebeck Coefficient and Figure of Merit

The Seebeck coefficient S (measured in µV/K) describes how much voltage a material generates per unit of temperature difference. Most metals have Seebeck coefficients between 1 and 10 µV/K. The best thermoelectric semiconductors reach 150–250 µV/K. A higher Seebeck coefficient means more voltage per degree of temperature difference — the core of what makes a good thermoelectric material.

But voltage alone does not determine efficiency. The thermoelectric figure of merit is a dimensionless number:

**ZT = S²σT / κ**

Here σ is electrical conductivity, κ is thermal conductivity, and T is absolute temperature. The numerator S²σ is called the power factor — a material's ability to generate voltage and conduct electricity simultaneously. The denominator κ fights against this: a high thermal conductivity lets heat leak through before it can be converted to electricity.

For decades, ZT was stuck below 1 for most materials — too inefficient to compete with mechanical refrigeration or generator technologies. Modern nanostructured materials have pushed ZT above 2, and some laboratory demonstrations have exceeded 3. At ZT = 1, a thermoelectric generator converts roughly 8–10% of the heat drop between hot and cold sources into electricity. At ZT = 3, that number climbs toward 18–20%.

The maximum theoretical efficiency of any heat engine — including a thermoelectric one — is set by the Carnot limit: η_Carnot = 1 − T_cold/T_hot. Thermoelectric efficiency approaches a fraction of this Carnot efficiency, specifically:

**η = η_Carnot × (√(1+ZT) − 1) / (√(1+ZT) + T_cold/T_hot)**

This formula tells you everything about why thermoelectrics are hard. Raising ZT moves the factor closer to 1. Raising the temperature difference (T_hot) also raises the factor because Carnot efficiency increases. In practice, a temperature difference of 500 K across a material with ZT = 1.5 gives an efficiency around 12% — a meaningful fraction of the theoretical maximum.

## The Three Modes in One Device

The interactive visualization at Elysia Tools shows all three thermoelectric modes operating simultaneously. The Seebeck mode converts heat gradients directly into voltage: set the hot junction to 500 K and the cold to 300 K, and the Seebeck coefficient of 150 µV/K generates about 30 mV across the junction — small but measurable. The efficiency shown in the simulation confirms the formula: at those temperatures with ZT ≈ 1.5, the Carnot-relative efficiency factor is roughly 0.5.

Switch to Peltier mode and the visualization demonstrates active cooling. Current flowing through the junction drives heat from the cold side to the hot side. The Peltier heat Q_p = S × T × I (where I is current) tells you that higher Seebeck coefficient and higher temperature both increase the cooling capacity per amp of current. This is how thermoelectric coolers (TECs, or Peltier coolers) work inside wine chillers, portable car fridges, and CPU coolers.

Thomson mode is the least familiar. When current flows through a wire that already has a temperature gradient along its length, the current carriers either absorb or release heat depending on whether they are moving "uphill" or "downhill" relative to the temperature profile. The Thomson coefficient µ relates the heat absorbed or released per unit current per unit temperature gradient. In most thermoelectric analysis, Thomson contributions are folded into the effective Seebeck coefficient measured across a temperature difference — they are real but small compared to Seebeck and Peltier.

## Why NASA Has Used This Since 1961

The first radioisotope thermoelectric generator (RTG) in space flew on the Transit satellite in 1961. NASA has used RTGs ever since because they produce power reliably for decades without moving parts or sunlight. The Curiosity rover on Mars runs on an RTG. The Perseverance rover too. Voyager 1 and 2. Cassini. The New Horizons probe that flew past Pluto. None of these missions could have used solar power at their distances from the Sun or in Mars's frequent dust storms.

An RTG works by surrounding a quantity of plutonium-238 with thousands of thermoelectric couples. The radioactive decay of Pu-238 produces heat; the Seebeck effect converts that heat into electricity. Pu-238 has a half-life of 87.7 years, so the power output declines slowly — Voyager's RTG now produces about a quarter of its original 470 watts, but that is still enough to keep the transmitter running and the instruments alive.

The figure of merit that matters for RTGs is not just peak ZT — it is the product of ZT and the absolute temperature, called the thermoelectric material quality factor. At the temperatures inside an RTG (roughly 800–1000 K at the hot junction), silicon-germanium alloys have ZT around 1 and have been used for decades. New skutterudite compounds and half-Heusler alloys are pushing into the 1.5–2 range at those temperatures, which would improve RTG efficiency meaningfully.

## The Quiet Power Inside You

Your body is a thermoelectric generator right now. Every cell that maintains a temperature gradient across its membrane is doing a tiny version of the Seebeck effect. The ion channels that govern nerve impulses, the mitochondrial membranes that couple nutrient oxidation to ATP synthesis, and the skin's response to ambient temperature changes all involve thermoelectric coupling at some level. Your nervous system uses essentially the same thermodynamic logic that Voyager uses to phone home.

This is not just an analogy. The thermoelectric equations describe the coupling between thermal and electrical fluxes in any material where charge carriers carry entropy. In physiological systems, the charge carriers are ions (Na⁺, K⁺, Ca²⁺, Cl⁻) moving across concentration gradients. The Seebeck coefficient for ion flow in electrolyte solutions is measurable and significant — it is part of why your skin temperature sensors respond the way they do to environmental gradients.

When you step from a warm room into cold outside air and feel a sharp sensation of cool, part of that signal comes from the thermoreceptor cells in your skin using a thermoelectric-like coupling to convert the temperature difference into a neural signal. The ion flow through the cell membrane is gated by a temperature-dependent electrochemical gradient — in thermodynamic language, a Seebeck-like coupling between temperature and chemical potential.

The connection sounds surprising, but the physics is not selective about what carries the charge. Electrons in metal, holes in semiconductor, ions in electrolyte — the same formalism applies to all of them. Seebeck discovered his effect by measuring the voltage produced when two different metals had their junctions at different temperatures. He had no idea that the same physics would describe how your eyes detect temperature gradients, how plutonium powers deep space probes, and how the next generation of wearable devices might charge themselves from body heat.

## The Frontier: Wearable Energy Harvesting

If a temperature difference of even 5 K between your body and the surrounding air can produce a measurable Seebeck voltage, then a wearable thermoelectric generator can harvest microwatts to milliwatts from body heat alone. The challenge is not voltage — a 5 K gradient with S = 40 µV/K gives 200 µV, which is easy to boost with a DC-DC converter. The challenge is getting enough power: a typical thermoelectric module with 10 thermocouples, a 5 K temperature difference, and a load matched to its internal resistance might produce 10–50 µW per square centimeter of skin contact.

That sounds tiny, but it adds up. A smartwatch that draws 30 mW during active use and 0.5 mW in sleep mode could harvest enough energy from a 10 K body-to-air gradient to extend battery life by 20–30% in a day. For medical sensors that need to run continuously, even 100 µW of harvested power can eliminate the need to replace batteries in implanted devices.

The thermoelectric materials being developed for this purpose are not like the silicon in computer chips. They are complex layered structures — filled skutterudites, clathrates, half-Heusler alloys — engineered to decouple electrical and thermal conductivity. The electrical conductivity is kept high (so current flows freely) while the thermal conductivity is kept low (so the temperature gradient does not collapse by heat leaking backward). This decoupling is the fundamental materials science challenge of thermoelectrics, and it is what makes the field active: every year, new structured materials push ZT higher.

## The Number That Determines Everything: ZT

If you remember one number from this article, make it ZT — the thermoelectric figure of merit. It is the single dimensionless metric that determines how useful a thermoelectric material is. ZT = 1 means modest efficiency, useful for cooling applications where convenience outweighs energy cost. ZT = 2 means generators can compete with small engines for remote power. ZT = 3+ means thermoelectric generators at scale can make sense for industrial waste heat recovery.

The best natural materials top out below ZT = 1. The best engineered nanostructured materials in laboratories have reached ZT = 3 and above — but only at specific temperatures, only in small samples, and often with manufacturing processes that do not scale. The engineering frontier is getting those high-ZT properties into producible bulk material at a cost that makes economic sense.

That is where the next decade of thermoelectric research is focused. And in the meantime, Voyager keeps flying — held together by the quiet, reliable physics that has been operating in your body since you were born.
