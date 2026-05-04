# The Quiet Math Behind Every Icon on Your Phone

In 1818, a French mathematician named Gabriel Lamé wrote down a deceptively simple equation. It looked like an ellipse — but with an exponent that could change everything. He had no way of knowing that his curve would one day end up on every iPhone sold worldwide.

That curve is the superellipse. And it is hiding in plain sight everywhere.

## The Problem With Circles and Rectangles

Circles are mathematically clean, but they don't tile efficiently. Rectangles fit together perfectly, but they feel harsh and rigid. For centuries, designers and mathematicians alike wrestled with the gap between these two shapes — the geometry that sits between "too round" and "too square."

Lamé's equation solved it in one line:

|x/a|^n + |y/b|^n = 1

The exponent n is the whole story. When n = 2, you have a standard ellipse. Push n higher — say, n = 4 — and the sides start to straighten while the corners remain soft. Pull n below 2, and the shape opens into a star. The entire spectrum from circle to diamond to square lives inside a single parameter.

You can explore this spectrum interactively at the [Superellipse (Lamé Curve) visualization on ElysiaTools](https://elysiatools.com/en/visualizations/superellipse).

## Why n = 4 Changed Icon Design

Apple's design team faced a real problem in 2007. Rounded rectangles — the standard approach for icon backgrounds — looked clunky. The corners were too round in some places, too sharp in others. Nothing felt continuous.

They found the superellipse, specifically with n ≈ 4. This value — the "squircle" — strikes a precise middle ground: the corners are smooth and continuous with the sides, yet the overall shape reads as a rectangle. It satisfies both the mathematical definition of "round" and the perceptual expectation of "square."

This wasn't a design accident. Apple's engineers explicitly chose the superellipse. The squircle isn't just a rounded rectangle — it is a different shape entirely. A rounded rectangle uses circular arcs at the corners. A squircle has no circular arcs. Its curvature flows continuously from edge to edge.

Try it yourself at the interactive visualization: move the shape exponent slider from n = 2 (a perfect circle) all the way up to n = 10. Watch how the geometry transforms. Then hold at n = 4 and observe how the transition from straight to curved feels most natural to the eye.

## The Man Who Built a Plaza Out of Math

Two centuries after Lamé discovered his curve, Danish architect Piet Hein fell in love with it. In the 1960s, Stockholm was planning a new central plaza — Sergels Torg — and the city wanted something that wasn't a circle but wasn't a square either.

Hein proposed the superellipse. The plaza was built using his curve, and it became one of the most recognizable public spaces in Scandinavia. He went further: he designed tables, chairs, and even a race track using the same shape. The superellipse, Hein argued, was the most aesthetically pleasing intermediate between a circle and a rectangle. He had data to back it up — or at least a compelling argument: the human visual system, he said, prefers shapes where the radius of curvature changes smoothly, not abruptly.

Modern designers call this quality "continuity of curvature." It's why the iOS app icon feels satisfying to look at. It's why the superellipse table looks right in a room in a way that a regular rectangular table doesn't.

## The Math Is Simpler Than You Think

Despite its elegant applications, the superellipse's mathematics are straightforward:

- n = 1: a diamond (rhombus)
- n = 2: a standard ellipse (or circle if a = b)
- n = 3: a curve between ellipse and star
- n = 4: the squircle — what Apple uses
- n = 5 and above: approaching a rectangle with increasingly sharp corners

The parameters a and b control the horizontal and vertical radii independently, which means you can stretch the superellipse into any aspect ratio while preserving its core mathematical character.

This simplicity is precisely what makes it so useful. Any programmer can implement it in a few lines. The rendering is efficient. The shape is analytically tractable — you can compute any point on the curve, its tangent, its curvature, without approximation.

## Where Else the Superellipse Shows Up

Beyond icons and plazas, the superellipse has quietly colonized many domains:

**Robotics and motion planning:** Robot paths that use superelliptical arcs feel more natural than those using straight lines and circular arcs, because the curvature transition never jerks.

**Typography:** Several typefaces use superelliptical forms in their letter shapes. The "o" in certain geometric sans-serif fonts is closer to a squircle than a true circle.

**Vehicle design:** The structural cross-sections of certain train cars and aircraft fuselages approximate superellipses, because this shape distributes stress more evenly than either rectangles or ellipses.

**Data visualization:** Superelliptical pie charts and gauge arcs feel less aggressive than sharp angles, a phenomenon designers describe as "visual warmth."

## One Parameter, Infinite Shapes

The superellipse's greatest trick is its economy. One equation. Three parameters. A spectrum of shapes that stretches from the softness of a circle all the way to the rigidity of a rectangle, with the whole world of organic intermediate forms in between.

Lamé never saw his equation appear on a smartphone screen. He couldn't have imagined Piet Hein's plaza. But the mathematics was always there, waiting — like all the best mathematics, patient and precise, until someone needed exactly what it had to offer.

The next time you unlock your phone, you're looking at 1818.
