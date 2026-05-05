# The Algorithm Newton Invented in 1669 Produces the Most Beautiful Fractals You've Never Heard Of

You've probably used Newton's method without knowing it. Engineers use it to find roots of equations. Scientists use it to calibrate models. It shows up inside machine learning optimizers, circuit simulators, and physics engines. The formula — z_{n+1} = z_n - f(z_n)/f'(z_n) — is one of the quiet workhorses of applied mathematics.

But there's a version of this algorithm that almost nobody teaches: what happens when you run Newton's method not on regular numbers, but on *complex* numbers?

The answer is a fractal so intricate, so unexpected, that it remained hidden for over 300 years after Newton first wrote down the method.

## What Newton Actually Invented

In 1669, Isaac Newton described a technique for finding roots of polynomial equations — values of x where f(x) = 0. The idea is intuitive: make a guess, draw a tangent line, follow it to where it hits the x-axis, repeat. Each step gets you closer. It converges quadratically fast, meaning the number of correct digits roughly doubles every iteration.

Joseph Raphson refined it in 1690. Together they gave us the Newton-Raphson method — elegant, fast, and ubiquitous. Every scientific computing course teaches it. Most engineers reach for it instinctively when they need to solve an equation numerically.

Here's what Newton and Raphson never imagined: their method doesn't just work on the number line. It works equally well on the *complex plane* — the two-dimensional landscape where numbers have both a real and an imaginary part.

## Complex Polynomials and Their Roots

A polynomial like f(z) = z³ - 1 has three roots in the complex plane. For z³ - 1 = 0, those roots are 1, -1/2 + i√3/2, and -1/2 - i√3/2. The fundamental theorem of algebra guarantees that a degree-n polynomial always has exactly n roots in the complex plane (counting multiplicity).

When Newton's method starts from a point z₀ in the complex plane, it follows the same tangent-line logic — but now the "plane" is two-dimensional. The iteration either spirals inward toward one of the polynomial's roots, or it diverges.

The critical question: *which starting point converges to which root?*

For a simple polynomial like z³ - 1, you might expect the complex plane to split neatly into three regions — one for each root, with clean boundaries between them. Something like a Voronoi diagram, where each root claims its territory.

That's not what happens.

## The Fractal Boundary

Run Newton's method on z³ - 1 from every point in the complex plane, color each starting point by which root it converges to, and you get something astonishing. The boundaries between the three basins of attraction aren't clean lines at all. They're infinitely intricate — zooming in reveals more structure, zooming in again reveals even more, forever.

Two points that start incredibly close to each other can end up at *completely different roots*. A tiny perturbation in your starting position — smaller than any measurement error you'd reasonably expect — can flip which root you converge to.

This is sensitive dependence on initial conditions: the same property that makes weather unpredictable and that defines chaos theory. But Newton fractals aren't chaotic in the usual sense — they converge, just not to the same place as your neighbors.

The fractal dimension of these boundaries exceeds 1 (the dimension of a smooth curve), meaning they're more "space-filling" than any ordinary line. They're genuinely between a line and a plane — somewhere in between dimensions.

## Why Nobody Found These Fractals for 300 Years

Newton published his method in 1669. The complex plane wasn't fully understood until the 19th century. And even after mathematicians like Gauss and Cauchy had developed the theory of complex functions, nobody thought to iterate Newton's method on complex polynomials and look at the resulting patterns.

Part of the reason is visual: you can work through the algebra and nothing unusual appears. The complex iteration formula looks exactly like the real one. The surprising structure only emerges when you *plot* millions of points and color them — a computationally intensive task that required modern computers.

The first published images of Newton fractals appeared in the early 1980s. Scientists who first rendered them on screen described genuine surprise — the expectation was of simple regions, not infinite intricacy.

## The Newton Fractal vs. the Mandelbrot Set

If this sounds familiar — complex iteration, fractal boundaries, infinitely detailed — that's because it echoes the Mandelbrot set. Both involve iterating a formula across the complex plane and coloring by behavior. Both produce breathtaking fractal geometry.

But there's a crucial difference.

The Mandelbrot set asks: for a given starting value c, does iterating z² + c stay bounded or diverge? The structure that emerges is a single set — remarkable for its self-similarity and daughter bulb.

Newton fractals are *parameter-dependent*. Choose a different polynomial — z⁴ - 1, z⁵ - 1, z³ - 2z + 2 — and you get an entirely different fractal. The polynomial defines the geometry. The Mandelbrot set is one object; Newton fractals are an infinite family.

This makes them a richer canvas for exploration. Each polynomial has its own character. z⁴ + 1, with roots at e^{iπ/4}, e^{3iπ/4}, e^{5iπ/4}, e^{7iπ/4}, produces a four-way symmetry. Higher-degree polynomials produce more elaborate patterns.

## What the Brightness Means

In most Newton fractal visualizers, brightness varies within each basin. Brighter regions converge *faster* to their root; darker regions take more iterations to settle.

This is another layer of structure that pure topology hides. You're not just seeing which root wins — you're seeing *how quickly* it wins. The fastest-converging regions cluster around the root itself and along certain rays. The slowest regions hug the fractal boundaries, where points are almost equidistant from two or more roots and iterations bounce back and forth before finally committing.

The interplay of color (which root) and brightness (how fast) creates a three-dimensional visual richness that still images don't fully capture. Animated explorations — slowly changing the polynomial or panning across a boundary — reveal the structure in ways that static views can't.

## Why It Matters Beyond Beauty

Newton fractals aren't just a mathematical curiosity. They have practical implications.

**Numerical analysis**: Understanding the basins of attraction matters when designing global root-finding algorithms. If your initial guess lands in the wrong basin, Newton method converges to the wrong root. Knowing the shape and size of basins helps you choose better starting points.

**Complex dynamics**: The study of Newton fractals contributed to the broader understanding of complex dynamical systems — the field that studies what happens when you iterate functions in the complex plane. The Newton fractal is a canonical example of a system where the boundary between basins has non-integer dimension.

**Physics**: The sensitivity to initial conditions that creates fractal boundaries appears in phase transitions. Near a critical point, tiny perturbations can tip a system into one phase or another — the same mathematical mechanism as a Newton fractal basin boundary.

**Art and design**: The aesthetic appeal is genuine. Newton fractals have inspired generative art, mathematical visualization projects, and design work. The patterns are simultaneously structured and unpredictable — useful for design that needs to feel both ordered and alive.

## How to Explore It Yourself

The [Newton Fractal interactive visualization on ElysiaTools](https://elysiatools.com/en/visualizations/newton-fractal) lets you explore these fractals directly in your browser. You can:

- Select from preset polynomials (z³ - 1, z⁴ - 1, z⁵ - 1, z⁶ - 1, z⁴ + 1, z³ - 2z + 2)
- Click and drag to pan across the complex plane
- Use mouse wheel to zoom in on boundary regions
- Switch between color schemes (rainbow, pastel, neon, earth tones, cool colors)
- Toggle root displays and animation
- Adjust iteration count and convergence tolerance

Zooming into a boundary region is the best way to develop intuition. You'll see the same infinite intricacy at every scale — small copies of the larger structure, points that "should" converge to one root but don't, spirals and filigree that seem to go on forever.

## The Unexpected Gift of Looking Twice

What makes Newton fractals so remarkable isn't the formula — mathematicians have known that formula for 350 years. It's the fact that applying it *exactly as written* to the complex plane produces something no one predicted.

A deterministic, well-understood algorithm, run on the simplest possible inputs, yields infinite complexity.

This is a reminder that in mathematics, "we know what this does" and "we have fully characterized what this does" are very different statements. The complex plane isn't an exotic edge case — it's the natural home for polynomials. Newton method works there exactly as it does on the real line. The fractal boundaries are a consequence of the mathematics itself, not a flaw or an edge effect.

The next time you use Newton method in practice — or any root-finding algorithm — consider that somewhere in the complex plane, the boundary of its convergence regions might be plotting an infinitely detailed portrait of the problem.

You just have to know where to look.
