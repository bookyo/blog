# The Giant Squid That Changed Everything: How One Neuron Won a Nobel Prize

In 1939, Alan Hodgkin jammed a metal electrode into the giant axon of a squid — a nerve fiber thick enough to poke with a pencil. He was 25, working at a marine lab on the English coast, trying to answer one of biology's most basic questions: what exactly is a nerve impulse?

What he and his student Andrew Huxley found over the next thirteen years — a set of four equations describing how charged atoms flow through protein pores in a cell membrane — won them the 1963 Nobel Prize in Physiology or Medicine. It remains one of the most important single discoveries in modern biology.

Sixty-five years later, you can run Hodgkin and Huxley's model in your browser, tweak the current, and watch neurons fire in real time. No lab required.

## The Problem With Nerves

Before Hodgkin and Huxley, nobody really understood how neurons transmitted signals. The prevailing view was vague — something electrical happened, somehow. But the details were missing.

The breakthrough was methodological as much as scientific. Hodgkin and Huxley used the squid's giant axon (up to 1mm in diameter — unusually large, making it easier to penetrate with electrodes) to take precise electrical measurements. They systematically varied the injected current and observed how the membrane voltage responded.

What they found defied expectation: nerve signals weren't electricity flowing passively through a wire. They were self-amplifying waves. Once the membrane voltage crossed a threshold (~6.3 μA/cm²), the signal raced down the axon at ~100 m/s without fading. Something in the membrane was actively pushing it.

## The Four Equations That Explained Life

The model Hodgkin and Huxley built centers on a single membrane equation:

**Cm · dV/dt = I_ext − g_Na · m³ · h · (V − E_Na) − g_K · n⁴ · (V − E_K) − g_L · (V − E_L)**

![The Four Equations That Describe Every Nerve Impulse](https://blog.flowrust.com/wp-content/uploads/2026/04/the-equation.png)

It looks intimidating. But each term is doing something intuitive:

- **Cm · dV/dt** is the rate of change of membrane voltage — the membrane capacitance storing charge.
- **I_ext** is the external current you inject to stimulate the neuron.
- **g_Na · m³ · h · (V − E_Na)** is the sodium current. Sodium ions carry positive charge into the cell (depolarizing it). The m³·h term means three "activation gates" must be open AND one "inactivation gate" must be closed for sodium to flow.
- **g_K · n⁴ · (V − E_K)** is the potassium current. Potassium flows out (repolarizing the cell). Four gates must all be open.
- **g_L · (V − E_L)** is a small "leak" current that accounts for all other ion flows.

The three gating variables m, h, and n each follow first-order kinetics — they open or close at rates that depend on voltage. This voltage-dependence is what makes the system tick. Sodium channels open fast; potassium channels open slower. This timing mismatch creates the spike.

## The Spike, Step by Step

![Four Milliseconds. Four Steps.](https://blog.flowrust.com/wp-content/uploads/2026/04/the-spike-process.png)

At rest, the membrane voltage sits around −65 mV. Sodium activation gates are mostly closed; potassium gates are mostly closed. The cell is silent.

Inject current.

1. **Depolarization**: The injected current pushes the voltage upward. As voltage rises, sodium activation gates (m) snap open rapidly. Sodium floods in. The membrane voltage shoots up toward +30 mV.

2. **Sodium inactivation**: About 1 millisecond into the spike, the sodium inactivation gates (h) close. Sodium flow cuts off just as the voltage peaks.

3. **Potassium activation**: Meanwhile, the potassium gates (n) — slower to respond — are opening wide. Potassium rushes out. The membrane voltage swings back negative, often overshooting slightly below the resting potential (hyperpolarization).

4. **Recovery**: All gates reset. The system is ready for the next spike.

The whole event lasts about 5 milliseconds. Every action potential in every neuron in your brain follows essentially this sequence.

## Why It Matters Beyond Neuroscience

![The Same Math Runs Your Heart](https://blog.flowrust.com/wp-content/uploads/2026/04/beyond-neurons.png)

Hodgkin and Huxley's equations were the first quantitative description of a biological process at the molecular level. They proved that protein channels — later called ion channels and confirmed to exist in the 1970s with the advent of the patch clamp technique — were the fundamental units of electrical signaling in cells.

This was not obvious at the time. The idea that specific proteins controlled specific ion flows was radical. The model made testable predictions that took decades to confirm experimentally. When they were confirmed, the field of molecular physiology was born.

The same conceptual framework extends far beyond neurons:

- **Cardiac pacemakers** use similar currents (though with different ion species and channel types) to generate the rhythmic heartbeat.
- **Insulin secretion** in pancreatic beta cells depends on ion channel activity.
- **Understanding epilepsy, arrhythmia, and chronic pain** all trace back to ion channel dysfunction.
- Modern drug development for these conditions is literally about designing molecules that block or enhance specific channel types.

## The Interactive Model

The [Hodgkin-Huxley Neuron Model](https://elysiatools.com/en/visualizations/hodgkin-huxley-neuron) at ElysiaTools lets you explore the equations directly.

You can:

- **Adjust the injected current** and watch the neuron transition from silent to spiking as it crosses the threshold
- **Toggle between Full and Reduced modes** — Full shows gating variables, conductances, and a phase portrait; Reduced focuses on the voltage trace
- **Choose presets** covering resting, threshold, regular spiking, fast spiking, and strong drive regimes
- **Watch the phase portrait** (dV/dt vs V) reveal the limit cycle that underlies repetitive spiking

The phase portrait is particularly illuminating. When the neuron is at rest, the trajectory sits at a stable fixed point. When you drive it above threshold, the trajectory spirals onto a closed loop — the limit cycle — and keeps circling as long as the current flows. Every spike is one lap around that loop.

## The Question That Lingers

Hodgkin and Huxley's model describes the action potential with remarkable accuracy. But it doesn't explain *why* the channel proteins have the precise structures they do — or why evolution converged on this particular mechanism across virtually all animal nervous systems.

The equations tell you *how* the system works. Understanding *why* it works that way — what constraints shaped the molecular machinery over hundreds of millions of years — is a deeper problem that remains open.

If you want to develop intuition for one of biology's most important mechanisms, start by playing with the simulation. Inject a little current. Watch the spikes appear. Then ask yourself: what would have happened if evolution had chosen a different set of ions?
