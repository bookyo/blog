# The Algorithm Nature Uses to Grow Lightning, Crystals, and Blood Vessels

In 1981, two physicists at the University of Michigan published a two-page paper that would never leave my mind. Thomas Witten and Leonard Sander were trying to explain something visually obvious but theoretically elusive: why electrodeposited metals grow in lacy, branching patterns instead of smooth, compact ones. Their answer was a model so stripped-down it sounds like a party trick. Place a seed particle at the center. Launch random walkers from the perimeter. Let them stick wherever they hit. Done.

The structures this model generates look exactly like lightning strikes. They look like the frost on your windshield. They look like the capillary networks threading through living tissue. They look like mineral dendrites pulled from cooling lava. Same fractal shape across three completely unrelated physical processes. That is the thing about DLA — Diffusion-Limited Aggregation — that still unsettles physicists forty-five years later.

## A Seed, Some Random Walkers, and a Branching Miracle

Here is the mechanism. Start with one stationary particle. Draw an invisible circle around it. From that circle, emit new particles — one at a time. Each new particle performs a random walk: step, step, random direction, step again. This is Brownian motion, the same erratic motion Einstein used to prove atoms existed in 1905.

The walker drifts. It stumbles. Most walkers drift too far and disappear. But some — the ones that happen to stumble into the cluster — stop permanently. They stick. They become the aggregate.

Do this ten thousand times. What emerges is a fractal: a branching, tree-like structure with self-similarity at every scale. Zoom in on a branch and you see smaller branches. Zoom in further and you see tinier ones still. The cluster looks statistically identical whether it spans ten pixels or ten meters.

## The Dimension That Shouldn't Exist

DLA clusters in two dimensions have a fractal dimension of approximately 1.71. That number is strange in the best possible way. A line has dimension 1. A plane has dimension 2. DLA clusters land between the two — too sparse to be surfaces, too dense to be curves. They inhabit a fractional dimension that only makes sense because of how you measure it.

You can measure it with box-counting. Cover the cluster with a grid of squares of side length s. Count the boxes that contain any part of the cluster — call this N(s). Shrink the box size and N(s) grows following a power law: N(s) ~ s^(-D). For DLA, D ≈ 1.71. This holds whether you grow the cluster for ten minutes or ten hours, whether you simulate it in water or in mineral solution. DLA is a universality class — wide range of systems, same abstract behavior.

## Lightning, Electroplating, and Tumor Angiogenesis

Here is where it stops being a math curiosity. In electrochemistry, when you electrodeposit copper from a copper sulfate solution onto a zinc surface, the copper dendrites that form branch in exactly this way. In geology, crystals growing in cooling basaltic magma produce mineral dendrites that match DLA simulations so closely that geologists use the model to study ore deposit formation. In oncology, the blood vessel networks that grow around tumors — driven by VEGF signaling between cancer cells and endothelial tissue — follow branching dynamics structurally identical to DLA clusters.

The physics are entirely different. Electron transfer at an electrode surface. Thermal diffusion in molten rock. Biochemical signaling. Nothing in common. Yet the same branching mathematics appears in all three.

You also see DLA in river delta formation, in the growth of fungal hyphae networks, in lightning strike branching, and in dielectric breakdown — when insulation fails electrically and the failure channel trees outward.

## Run It in Your Browser

The [Diffusion-Limited Aggregation tool on ElysiaTools](https://elysiatools.com/en/visualizations/diffusion-limited-aggregation) lets you grow DLA clusters in real time. Watch the cluster evolve particle by particle. Adjust the emission rate and diffusion step size. Switch between monochrome and multi-species color modes. Observe the live fractal dimension as the cluster grows.

Live statistics include particle count, estimated fractal dimension via box-counting, aggregate radius, and active walker population. Presets let you explore different growth regimes — the classic center-seed, dense-forest mode with high emission rates, asymmetric off-center growth, and a fast-preview mode for quickly growing large clusters.

Watching a cluster grow — particles drifting, sticking, branches extending — builds an intuition that equations alone cannot. The model is three sentences. The behavior is not.

## Why This Model Still Haunts Physicists

DLA belongs to a family — Self-Organized Criticality (Bak, Tang, Wiesenfeld, 1987), percolation theory, the Ising model — that share a single, unsettling idea: simple local rules between many agents produce global structures of startling richness. No master plan. No central director. No intent. Just random walkers and sticky boundaries, and from that, lightning and crystals and blood vessels.

The lightning bolt outside your window, the frost on your windshield, the branching of trees visible from an airplane — all may be running the same algorithm. Not by design. By the inevitable mathematics of diffusion meeting an irreversible threshold.

Witten and Sander's two-page paper has been cited over 4,000 times. People are still running DLA simulations in their browsers, watching clusters grow, and finding the same 1.71 dimension in all of them. Some models are too beautiful to stop looking at. And too instructive to forget.
