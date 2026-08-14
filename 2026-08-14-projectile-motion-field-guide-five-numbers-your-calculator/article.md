<strong>If you can plug four numbers into a form, you already know enough to read a projectile-motion result.</strong> The rest is just naming what the calculator hands back, and knowing which one actually answers the question you walked in with. The tool at [Elysia Tools](https://elysiatools.com/en/tools/projectile-motion-calculator) takes initial speed, launch angle, gravity, and an optional starting height, and returns five derived values — range, max height, flight time, time-to-apex, and impact speed — in plain SI units. You don't need to memorize PV=nRT or pull out a textbook to use it. The calculator handles the kinematics; you decide which answer is the one that matters.

The shape of this guide is intentionally short. We'll walk through what each output number means, where the 45° "maximum range" rule actually comes from (and when it stops being true), how to sanity-check a result with a single multiplication, and how the optional initial-height field silently flips which angle is best. By the end you should be able to take any one of the calculator's outputs and explain, in one sentence, why it has the value it does.

## What each output actually means

The calculator returns five derived values from your four inputs. They are not interchangeable, and each one answers a different question.

<ul>
<li><strong>Horizontal range (R, meters)</strong> — how far the projectile travels along the ground before it lands at the same height it started. The classical "how far will this throw go" number.</li>
<li><strong>Maximum height (H, meters)</strong> — the highest point the projectile reaches above the ground, including any starting height. Not the same as the height <em>above</em> the launch point.</li>
<li><strong>Time to apex (t_up, seconds)</strong> — how long the projectile spends climbing before it stops going up and starts coming back down. Half of the symmetric-flight case.</li>
<li><strong>Total flight time (t, seconds)</strong> — how long from launch until the projectile reaches the landing level. Includes any extra duration from a non-zero initial height.</li>
<li><strong>Impact speed (|v|, m/s)</strong> — the magnitude of the velocity vector at the instant of landing. Without air resistance this is always equal to the launch speed when the landing level matches the launch level.</li>
</ul>

Pick the one that matches your question. If you're asking "will this throw clear the fence?" you want H, not R. If you're asking "how long until it hits the ground?" you want t, not t_up.

## The five formulas, in one place

The calculator is doing one job of work: decomposing the initial velocity vector, integrating the vertical motion under constant gravity, and recombining. The full derivation lives on the [Elysia Tools detail page](https://elysiatools.com/en/tools/projectile-motion-calculator), but the working set is short enough to memorize in five minutes:

<ul>
<li>Horizontal velocity: <code>vx = v0 &middot; cos(&theta;)</code> &mdash; constant throughout the flight (no horizontal forces).</li>
<li>Initial vertical velocity: <code>vy0 = v0 &middot; sin(&theta;)</code></li>
<li>Time to apex: <code>t_up = vy0 / g</code></li>
<li>Maximum height: <code>H = h0 + vy0&sup2; / (2g)</code></li>
<li>Total flight time: <code>t = (vy0 + &radic;(vy0&sup2; + 2g&middot;h0)) / g</code></li>
<li>Range: <code>R = vx &middot; t</code></li>
<li>Impact speed: <code>|v| = &radic;(vx&sup2; + vy_impact&sup2;)</code></li>
</ul>

Two of these &mdash; the horizontal-velocity and impact-speed ones &mdash; are the ones most students skip, and they're the easiest place to catch a wrong answer on a sanity check.

## The 45&deg; rule and when it stops being a rule

When the projectile starts and lands at the same level (initial height <code>h0 = 0</code>), the range is maximized at exactly <strong>45&deg;</strong>. This is the famous "throw it at 45&deg; to go furthest" result, and it's where almost every textbook leaves the story. There are three real-world situations where the 45&deg; rule is <em>wrong</em>:

<ul>
<li><strong>You're throwing from above ground.</strong> Once <code>h0 &gt; 0</code>, the optimal angle shifts <em>down</em> below 45&deg;. A ball thrown from a 5 m wall reaches maximum range at about 41.7&deg;, not 45&deg;. The calculator will show this directly: type 5 into the initial-height field and re-run at 45&deg;, then drop the angle to 41.7&deg; and watch R climb.</li>
<li><strong>You're throwing at a target above your launch level.</strong> If the target sits higher than <code>h0</code>, you actually want a higher angle than 45&deg; &mdash; sometimes close to vertical &mdash; because you need the extra altitude to reach the target, not the extra horizontal distance.</li>
<li><strong>Air resistance is non-negligible.</strong> This calculator assumes none. Real balls, arrows, and bullets all lose speed to drag, which compresses the optimal angle toward 30&deg;-40&deg;. If you need a drag-aware answer, you're past what a closed-form calculator can give you.</li>
</ul>

In other words: 45° is the right answer when the model assumptions match your situation, and visibly wrong the moment one of them doesn't.

## How to sanity-check a result in ten seconds

Before trusting any projectile answer, plug the numbers back in. Two quick checks catch most arithmetic mistakes:

<ul>
<li><strong>Symmetry check (h0 = 0):</strong> the flight time should be <em>exactly</em> twice the time-to-apex. If you got 2.886 s total and t_up = 1.443 s, you're good. If t_up = 1.500 s and total = 2.886 s, somebody rounded one of them.</li>
<li><strong>Range sanity:</strong> <code>R = vx &middot; t</code>. Multiply those two numbers yourself and compare to the calculator's R. If they disagree, the calculator used a different g or angle than you thought.</li>
<li><strong>Impact-speed symmetry:</strong> with <code>h0 = 0</code>, <code>|v|</code> at landing should equal <code>v0</code> at launch. Drag is what breaks this, and this calculator doesn't model drag, so a mismatch means an input mistake.</li>
</ul>

These three checks take under ten seconds and catch every typo in your four inputs. Run them once and you stop second-guessing the calculator.

## Worked example: a 20 m/s, 45&deg; ball from the ground

This is the canonical demo from the calculator's example gallery. Plug in <code>v0 = 20</code>, <code>&theta; = 45&deg;</code>, <code>g = 9.80665</code>, <code>h0 = 0</code>:

<ul>
<li><code>vx = 20 &middot; cos(45&deg;) = 14.142</code> m/s</li>
<li><code>vy0 = 20 &middot; sin(45&deg;) = 14.142</code> m/s</li>
<li><code>t_up = 14.142 / 9.80665 = 1.4422</code> s</li>
<li><code>H = 0 + 14.142&sup2; / (2 &middot; 9.80665) = 10.194</code> m</li>
<li><code>t = 14.142 + &radic;(14.142&sup2; + 0) / 9.80665 = 2.8844</code> s</li>
<li><code>R = 14.142 &middot; 2.8844 = 40.794</code> m</li>
</ul>

The calculator reports <code>R &asymp; 40.77 m, H &asymp; 10.19 m, t &asymp; 2.886 s</code> &mdash; matches to three significant figures. The symmetry check passes: <code>1.4422 &times; 2 &asymp; 2.8844</code>. The range sanity check passes: <code>14.142 &times; 2.8844 &asymp; 40.794</code>. The impact-speed check passes: <code>|v| = 20.000</code> m/s.

## Worked example: an arrow at 30 m/s, 30&deg;, from a 5 m wall

Now the same calculator with <code>v0 = 30</code>, <code>&theta; = 30&deg;</code>, <code>g = 9.80665</code>, <code>h0 = 5</code>. The arrow starts 5 m above the landing level:

<ul>
<li><code>vx = 30 &middot; cos(30&deg;) = 25.981</code> m/s</li>
<li><code>vy0 = 30 &middot; sin(30&deg;) = 15.000</code> m/s</li>
<li><code>t_up = 15.000 / 9.80665 = 1.5297</code> s</li>
<li><code>H = 5 + 15&sup2; / (2 &middot; 9.80665) = 5 + 11.473 = 16.473</code> m</li>
<li><code>t = (15 + &radic;(225 + 2 &middot; 9.80665 &middot; 5)) / 9.80665 = (15 + &radic;(323.082)) / 9.80665 = (15 + 17.974) / 9.80665 = 3.362</code> s</li>
<li><code>R = 25.981 &middot; 3.362 = 87.348</code> m</li>
</ul>

The calculator reports <code>R &asymp; 87.36 m, H &asymp; 16.47 m, t &asymp; 3.362 s</code>. The flight time is <em>not</em> twice t_up anymore (it can't be &mdash; the arrow has 5 m of free fall after it stops climbing), and that's the diagnostic that tells you <code>h0 &gt; 0</code> is doing real work in the answer.

## What this calculator does not do (and where to go next)

The model is intentionally narrow: <strong>no air resistance, uniform gravity field, point-mass projectile, flat ground</strong>. Those assumptions are right for a backyard ball toss, a physics homework problem, and a rough ballistics sanity check. They are wrong for:

<ul>
<li><strong>A real bullet.</strong> Drag dominates past about 50 m/s and the drag coefficient depends on the projectile shape. Use a dedicated ballistics solver.</li>
<li><strong>A golf shot on a real course.</strong> Spin-induced lift, wind, and altitude all matter. The 45&deg; rule becomes 30-40&deg; with realistic drag.</li>
<li><strong>A rocket or missile.</strong> Thrust during the flight means the velocity isn't constant, and gravity isn't the only force.</li>
<li><strong>Anything in orbit or near another massive body.</strong> Different gravity model entirely.</li>
</ul>

For everything inside that envelope, the calculator is exact to four or five significant figures on typical inputs &mdash; limited mostly by how precisely you know your launch speed and angle. The harder problem is almost always the inputs, not the math.

## Putting it together

A projectile-motion calculator answers five questions with one set of four inputs: how far, how high, how long to climb, how long until it hits, and how fast at impact. The 45&deg; rule is the special case, not the default &mdash; it assumes you launch from the same height you land at, with no air resistance, on flat ground. The moment any of those breaks, the optimal angle shifts, and the calculator will show you where. Run the three sanity checks (flight-time symmetry, range = vx &middot; t, impact speed = launch speed when h0 = 0) once per answer and you stop having to trust the math blindly.

Try it on your own throw: pick a speed you can actually measure, an angle you can actually hold, and a starting height that matches reality. The four numbers go in, the five numbers come out, and the formulas in this guide let you verify every one of them.

Explore more physics and math tools at [elysiatools.com](https://elysiatools.com/en/tools).