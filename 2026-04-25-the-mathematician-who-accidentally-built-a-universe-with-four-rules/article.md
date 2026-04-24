# The Mathematician Who Accidentally Built a Universe with Four Rules

In April 2020, John Conway died of COVID-19. He was 82, and by then he had largely stopped thinking about the thing that made him famous. "I vaguely remember being pleased about getting some result," he told an interviewer when asked about his most celebrated creation. "I didn't think it was that important."

What he had built, almost by accident in 1970, was a grid of squares governed by four rules. No players. No score. Within two years of publication, people had built machines inside this grid that fired endless streams of moving objects into a void. Conway found this amusing but wasn't particularly interested in where it went next.

He should have been.

![Conway's Game of Life - Opening](https://blog.flowrust.com/wp-content/uploads/2026/04/opening-death.png)

**[Conway's Game of Life](https://elysiatools.com/en/visualizations/game-of-life)** is a cellular automaton — a grid where each cell lives or dies based on how many neighbors it has. That description makes it sound like a biology simulation. It isn't. It's closer to a proof that simple rules, applied without judgment, produce irreducible complexity. And 55 years after Conway published it, people are still finding new things in his grid.

## The Four Rules

A living cell survives only if it has 2 or 3 neighbors. It dies otherwise — from isolation or overcrowding. A dead cell comes back to life if exactly 3 neighbors surround it.

That's the entire system. No randomness. No player decisions after the initial setup. The grid runs on autopilot.

The counterintuitive insight is buried in rule four: cells that are dead can come back. In most simulations, death is an endpoint. In Conway's grid, it's often a prerequisite for birth. The grid doesn't conserve life. It recycles it.

Conway spent roughly two years tuning the parameters before settling on these exact thresholds. He was looking for something specific — a middle ground between a system that dies out immediately and one that fills up and stays full. He wanted "interesting" behavior. The numbers 2 and 3 aren't physics. They're a feel, tuned by hand.

## The 37% Ceiling Nobody Predicted

The most surprising property of the Game of Life is one that Conway didn't predict: a randomly seeded grid almost never exceeds about 37% population density. The system self-regulates. Dense clusters collapse from overpopulation. Sparse regions die from isolation. The grid finds its own equilibrium — and that equilibrium is never full.

This is not obvious from the rules. Nobody, looking at rule three ("overpopulation kills"), would confidently predict a hard ceiling on density. But run the simulation, and the ceiling appears every time.

![The 37% Density Ceiling](https://blog.flowrust.com/wp-content/uploads/2026/04/density-ceiling.png)

## The Creatures That Shouldn't Exist

Once the grid is running, patterns emerge. Players in the early 1970s named them:

**Still lifes** don't change between generations. The 2×2 block is stable forever. The beehive looks like a honeycomb cell. The loaf resembles its name. These are the grid's rocks — they exist but don't do anything.

**Oscillators** cycle. The blinker (three horizontal cells flipping to three vertical and back) is the smallest. The pulsar has a three-generation period and looks like a spinning asterisk. These are the grid's clocks.

**Spaceships** move. The glider — five cells in a diagonal arrangement — travels one cell diagonally every four generations. It was the first moving pattern discovered and remains the most iconic.

**Guns** produce spaceships indefinitely. Bill Gosper discovered the Gosper Glider Gun in 1970: a static configuration that fires a new glider every 30 generations. Forever. A finite machine producing infinite output.

This is where Conway's grid stops being a curiosity and starts being unsettling. A pattern that doesn't move, sitting on a grid following rules designed to prevent chaos — and it produces an endless stream of moving objects. The gun doesn't violate any rule. It simply uses the rules in a way nobody anticipated.

![The Gosper Glider Gun - Finite Machine, Infinite Output](https://blog.flowrust.com/wp-content/uploads/2026/04/glider-gun.png)

## Turing's Ghost in a Grid of Squares

The Game of Life is Turing complete. Any calculation any computer can perform, the Game of Life can perform. Given the right starting configuration, it can simulate any algorithm.

This was proved in the 1990s by a research team that showed how to construct logic gates using the grid's patterns. Stack enough logic gates together, and you have a processor. The Gosper Glider Gun demonstrates that the system can produce infinite output. Turing completeness proves the system can, in principle, produce any computation.

This is emergence at its most extreme: computation emerging from a grid, four rules, and nothing else. No intention. No design. Just rules, iterated.

## What It Teaches About Complexity

The Game of Life is useful beyond mathematics because it's a simplified model of how complexity arises in the real world.

**Biology.** The rules capture something real about population dynamics — isolation kills, overcrowding kills, and the middle ground sustains life. Ecosystems, economies, and immune responses all operate on feedback loops that resemble these rules.

**Physics.** Phase transitions — water freezing, metal becoming superconducting — behave like the Game of Life near critical points. Small changes in parameters produce sudden, large changes in outcome.

**AI.** Language models take simple rules (predict the next token) and produce something that resembles understanding when iterated at scale. The complexity isn't in the rule. It's in what the rule, applied billions of times, creates.

Conway was surprised by how much his system produced. In later interviews, he expressed genuine wonder at discoveries made decades after his original publication — structures he couldn't have predicted from the rules alone.

## The Question Nobody Has Answered

Here is what still isn't known: given an arbitrary starting pattern, can you predict whether it will produce long-lived complexity or collapse within a few dozen generations?

You cannot. In the general case, this is computationally undecidable — the same class of problem as the halting problem for Turing machines. You have to run the simulation to find out.

A deterministic system, governed by four fixed rules, producing answers that cannot be predicted without running it. Conway built this by accident. The universe Conway built inside a grid does not care about his intentions — it simply follows the rules, generation after generation, long after Conway himself is gone.

![The Undecidable Question](https://blog.flowrust.com/wp-content/uploads/2026/04/undecidable.png)

Try it yourself. Draw something. Press start. See what happens.
