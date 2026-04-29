# Why Nature Loves the Game Rock-Paper-Scissors

## The counterintuitive reason cyclic dominance keeps ecosystems alive

On a hillside in California, you might find three types of male lizards engaged in a silent, generations-long battle. Orange-throated males are aggressive and dominate harems. Blue-throated males are loyal defenders who guard mates. Yellow-throated males are sneaky sneakers who mimic females to sneak copulations. Each strategy defeats one and loses to another: orange beats blue, blue beats yellow, yellow beats orange. And somehow, after decades of study, all three survive together in stable equilibrium.

This is not a coincidence. It is a universal pattern that mathematicians call **cyclic dominance** — and it shows up everywhere biology refuses to obey simple competitive exclusion.

## The Problem with "Survival of the Fittest"

The standard story of natural selection says the fittest competitor drives others to extinction. One species outperforms another, takes over, and that's that. Gause's competitive exclusion principle formalized this: two species competing for the same resource cannot coexist indefinitely. The better competitor wins. The loser goes extinct.

But nature is messier than that. In 1975, Robert May and Leonard Som said something radical: what if winning is not transitive?

In a Rock-Paper-Scissors (RPS) game, rock beats scissors, scissors beats paper, and paper beats rock. There is no best strategy. The outcome depends entirely on what your opponent plays. Add spatial structure — competitors occupying a 2D lattice instead of a well-mixed tank — and the system spontaneously produces something visually stunning: **spiral waves**.

You can see this unfold in the [Spatial Rock-Paper-Scissors simulator on ElysiaTools](https://elysiatools.com/en/visualizations/spatial-rps). Start with a random grid of red, green, and blue cells. Hit play. Within a few dozen generations, the disorder resolves into rotating spiral arms — each color chasing the one it beats, fleeing from the one that beats it. The spirals persist for thousands of generations, far longer than neutral drift models predict.

## How Spiral Waves Emerge from Simple Rules

The rules are minimal. Each cell on a grid holds one of three strategies. During each generation, a cell looks at its neighbors and may adopt a neighbor's strategy if that neighbor is winning against it. The key parameter is **invasion probability** — how likely a cell is to copy a neighbor's strategy each tick.

Low invasion probability: strategies form small stable clusters.
Moderate invasion probability: clusters grow, meet at angles, and spiral arms emerge.
High invasion probability: the system becomes well-mixed, spirals dissolve, and you get a noisy equilibrium.

This is the **May-Leonard model** in action. In a perfectly mixed (mean-field) system, the replicator dynamics spiral inward toward a coexistence fixed point. But the mean-field prediction underestimates how long coexistence lasts. Local interactions on a spatial lattice break the mean-field assumption. Protective clusters form. Strategies shield each other from extinction. The result is coexistence that can outlast any biologically realistic timescale.

## Real-World RPS Is Everywhere

The lizard story (Uta stansburiana) is the most famous natural example. But cyclic dominance appears across biology:

**Marine organisms**: Corals, algae, and sponges on subtidal rocks compete cyclically for space. Remove one, and another previously suppressed competitor explodes — then crashes when its own predator recovers.

**E. coli toxin-antitoxin systems**: Some bacterial plasmids produce both a toxin and an antitoxin. The toxin kills neighboring cells without the plasmid. Cells with the plasmid produce less antotoxin as they grow, making them vulnerable to toxin-only cells. The three-way interaction produces cycling at the microscale.

**Trees in forests**: Some forests show cyclic dominance through fungal pathogen transmission, where different tree species protect and threaten each other in turn.

**Theoretical extensions**: Replicator dynamics on graphs has been applied to ecological commons, traffic flow, and even opinion dynamics in social systems.

The spiral waves in the ElysiaTools simulator are not just a metaphor. They are the same mathematical structure that appears in Belousov-Zhabotinsky chemical reactions, cardiac tissue propagation, and oscillatory neural cultures. Cyclic dominance at the ecological scale and spiral wave patterns at the dynamical systems level share a common underlying architecture.

## Why Spatial Structure Is the Key Ingredient

Without space, RPS games converge to a neutrally stable coexistence point that is easily destabilized by random drift. Any perturbation can start a extinction cascade.

With space, **local interactions create protected refugia**. When a strategy is rare, its surviving clusters are physically isolated from its predator. This spatial self-organization buys time. The rare strategy does not go extinct before a disturbance somewhere else in the system tips the odds back in its favor.

This is why spatial structure is considered one of the fundamental mechanisms for maintaining biodiversity. The global coexistence we observe in many ecological communities may not require any niche differentiation or frequency-dependent selection at all — it may simply require enough space for local interactions to do their work.

The mutation rate matters too. Very low mutation lets strategies settle into static domain walls. Very high mutation destroys spatial structure entirely, producing a well-mixed noisy state. The interesting pattern formation happens in between — where selection and mutation are in tension, continuously seeding new clusters that can nucleate fresh spiral waves.

## What You Can Explore

The [Spatial Rock-Paper-Scissors simulator](https://elysiatools.com/en/visualizations/spatial-rps) gives you direct control over the key parameters:

- **Grid size** (50–300): Larger grids allow more spiral arms and more complex dynamics
- **Invasion probability** (1–100%): Controls how fast strategies spread
- **Mutation rate** (0–50%): Seeds new clusters and prevents static equilibrium
- **Speed** (1–30): Watch the spiral waves evolve in real time
- **Paint mode**: Draw your own initial conditions

Try setting invasion to around 70%, mutation to 5%, and painting a diagonal stripe of one color. Watch how the stripe breaks into spiral arms within 20 generations. Now increase mutation to 30% and watch the pattern fragment. The richness of emergent behavior from so few parameters is itself a lesson in how complex ecological dynamics can arise from simple spatial rules.

## The Broader Message

Rock-Paper-Scissors is not a toy model. It is a minimal representation of any system where three or more strategies are locked in cyclic dependence — where A beats B, B beats C, and C beats A. These systems are common in ecology, evolutionary biology, economics, and social dynamics.

What the spatial version reveals is that **the geometry of competition matters as much as the outcome**. When competitors are fixed in space and interact locally, they self-organize into patterns that stabilize coexistence. The same logic applies to markets, ecosystems, and political systems: distributed, locally interacting agents can sustain diversity that centralized control or perfect mixing would destroy.

Open the simulator, watch the spirals form, and ask yourself what other systems in your life are governed by non-transitive cycles hiding in plain sight.
