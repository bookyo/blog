# The Law of Cosines Visualized: When Pythagoras Isn't Enough

c² = a² + b². It works for right triangles. But what happens when your triangle doesn't cooperate?

The Law of Cosines handles every triangle — acute, obtuse, and right — with one clean formula:

**c² = a² + b² − 2ab·cos(C)**

That little cosine term is the whole story. When C = 90°, cos(C) = 0, and you get Pythagoras. When C > 90°, cos(C) turns negative, and the formula correctly predicts that the opposite side grows larger than a² + b². The geometry adapts. No special cases.

I found a free interactive tool that makes this tangible: the [Law of Cosines Visualization](https://elysiatools.com/en/visualizations/law-of-cosines) on ElysiaTools. You drag the triangle vertices, watch the formula update in real time, and work through a step-by-step proof. Here's what makes it worth bookmarking.

---

## What the Tool Does

The visualization has four tabs:

**Explore** — Drag any vertex of a triangle and watch every measurement update instantly. Side lengths, angles, and the formula itself recalculate as you move. It tells you whether the triangle is acute, right, or obtuse, and verifies the Law of Cosines numerically on screen.

**Proof** — A 5-step animated derivation starting from the Pythagorean theorem. Drop an altitude, apply Pythagoras to both smaller triangles, equate them, and solve for x using the cosine definition. Each step has an explanation and a live canvas visualization.

**Examples** — Pre-loaded triangles showing the SAS case (two sides + included angle), the SSS case (three sides), and each triangle type. Load any example with one click.

**Practice** — Randomly generated problems. You supply the missing side or angle, then check your answer. Problems alternate between "find the side" and "find the angle" modes.

---

## Why the Cosine Term Matters

The formula c² = a² + b² − 2ab·cos(C) has a geometric interpretation. The term 2ab·cos(C) projects side *a* onto side *b*. When C is acute, this projection is positive and shrinks the effective combined length of a and b — so c² < a² + b². When C is obtuse, the projection is negative, and c² actually exceeds a² + b².

This is why the Law of Cosines works for navigation, surveying, and game physics. You don't need a right angle. You just need two sides and the angle between them — or three sides and a target angle.

---

## 5 Scenarios Where It Replaces Multiple Steps

**1. Surveying a plot** — Measure two fence lines and the included angle, then calculate the boundary diagonal without pacing it out.

**2. Game physics** — Determine the distance between two moving objects when you know their speed vectors and the angle between those vectors.

**3. Robotics arm reach** — Given two arm segments of lengths a and b, find how far the gripper can reach at a given joint angle C.

**4. Astronomy** — Calculate the distance to a star when you know Earth's orbital radius, the star's parallax angle, and the angle between observations.

**5. Photography** — Find the diagonal field of view of a camera lens given the sensor width (a), height (b), and the angle between them.

---

## The Step-by-Step Proof (What the Tool Shows)

The proof tab walks through five stages:

1. **Drop altitude from angle B** — this splits side c into segments x and (b−x), creating two right triangles.
2. **Apply Pythagorean theorem** — left triangle gives h² = a² − x²; right triangle gives h² = c² − (b−x)².
3. **Equate the two** — a² − x² = c² − (b−x)².
4. **Simplify** — a² = c² − b² + 2bx, solving for x = (a² − c² + b²) / (2b).
5. **Use cosine definition** — x = a·cos(A), and after substitution: c² = a² + b² − 2ab·cos(C).

The canvas shows these steps visually as you advance through them.

---

## What You Can Do Right Now

Head to **[Law of Cosines Visualization](https://elysiatools.com/en/visualizations/law-of-cosines)** and try the following:

- Set C to exactly 90°. Watch c² = a² + b² emerge naturally.
- Set C above 90° (obtuse). Notice that c² becomes *larger* than a² + b².
- Load the SAS example and try solving it by hand before checking the tool's answer.
- Generate a practice problem in SSS mode — finding an angle from three known sides.

The tool is free, browser-based, and requires no account. It works in English, Chinese, Spanish, French, German, Russian, and Portuguese.

---

## The Gap Nobody Talks About

Geometry education has no shortage of Pythagorean theorem practice sheets. But the transition to non-right triangles — which is where most real-world geometry actually happens — often relies on memorization rather than intuition.

Interactive visualizations like this one close that gap. You see why the formula works, not just what it says. And that changes how you apply it.

If you want to explore more math concepts this way, ElysiaTools has over 200 interactive visualizations — Fourier transforms, neural network training, game theory equilibria, and more. The Law of Cosines is a good place to start.
