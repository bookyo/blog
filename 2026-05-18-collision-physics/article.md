# Why the Same Crash Looks Different Depending on How Hard You Hit

Every collision is a physics experiment. Two balls collide, momentum swaps, energy redistributes — but the outcome depends on a single number that most people never hear about.

That number is the **coefficient of restitution**. And once you understand it, you start seeing collisions everywhere: in the crack of a billiard break, the crunch of a car crash, the satisfying thwack of a baseball bat.

---

## The Two Laws That Never Break

Before anything else, there are two rules that govern every collision in the universe — no exceptions.

**Conservation of momentum** states that the total momentum before impact equals the total momentum after. Momentum is mass times velocity, so if a 2 kg ball moving at 3 m/s hits a 1 kg ball at rest, the combined momentum (6 kg·m/s) stays the same no matter what happens to the balls afterward.

This law never takes a day off. Whether the collision is gentle or violent, whether the objects bounce off each other or fuse together, momentum is always conserved.

**Conservation of kinetic energy** is different. It only applies to a special class of collisions called *elastic* collisions. In an elastic collision, kinetic energy is also conserved — the total energy of motion before equals the total after.

In the real world, perfectly elastic collisions are rare. Billiard balls come close. Hard spheres at low speeds approach it. But even the most carefully engineered system loses some energy to sound, heat, and deformation.

---

## The Coefficient of Restitution: The Number That Classifies Every Collision

The coefficient of restitution, abbreviated **e**, is a number between 0 and 1 that classifies how bouncy a collision is.

- **e = 1**: Perfectly elastic. Kinetic energy is fully conserved. Balls bounce off each other with no energy lost.
- **e = 0**: Perfectly inelastic. The objects stick together and move as one. Maximum energy is lost.
- **0 < e < 1**: Everything in between. This is where most real-world collisions live.

The definition: e = relative speed of separation / relative speed of approach. If two objects approach each other at 5 m/s and separate at 3 m/s, e = 3/5 = 0.6.

This single number tells you almost everything about the collision outcome. Given the masses and initial velocities, the final velocities are fully determined by e.

---

## What Actually Happens in Different Regimes

### Perfectly Inelastic (e = 0): Maximum Energy Loss

When e = 0, the objects stick together. A classic example is a lump of clay dropped on the floor — it deforms, loses its shape, and stops moving.

In terms of equations, two masses m1 and m2 with initial velocities v1 and v2 become one combined mass (m1 + m2) moving at:

**v_final = (m1·v1 + m2·v2) / (m1 + m2)**

The momentum is conserved, but half or more of the kinetic energy is typically lost to deformation and heat.

This regime is where car crash tests live. Engineers don't want elastic bouncing — they want the car to crumple and absorb energy, protecting the passengers by converting kinetic energy into controlled deformation.

### Perfectly Elastic (e = 1): No Energy Lost

When e = 1, both momentum and kinetic energy are conserved. The classic textbook case is two billiard balls colliding head-on.

For two equal masses where one is stationary, the moving ball stops completely and the stationary ball leaves with the same velocity the first one had. This is why a billiard break works — you strike the cue ball, it hits the stationary ball, and the cue ball stops while the target ball shoots forward.

The velocity exchange formula for equal masses in a 1D elastic collision:
- v1_final = v2_initial
- v2_final = v1_initial

### The Middle Ground: Partially Elastic

Most collisions fall between 0 and 1. A baseball bat hitting a ball has e ≈ 0.4–0.5. A tennis racket on a ball reaches e ≈ 0.7–0.8. A Super Ball can have e ≈ 0.9.

The higher the e, the "bouncier" the collision. And because kinetic energy scales with velocity squared, small changes in e near 1 produce large changes in energy loss.

---

## 2D Collisions: When Objects Hit at an Angle

The simulations become much more interesting when collisions aren't head-on. A 2D collision adds an **impact angle** parameter — the angle at which the two objects approach each other relative to a reference line.

In 2D, the problem splits into two components:
- The **normal direction** (along the line connecting the two centers): where the coefficient of restitution applies
- The **tangential direction** (perpendicular to the normal): where objects slide past each other, typically with friction

This is why a pool ball struck at an angle doesn't just stop — it curves off at a specific angle determined by the geometry of impact. The cue ball transfers momentum in the normal direction according to the coefficient of restitution, while retaining its tangential velocity.

In simulations like the Collision Simulator, you can set the impact angle in degrees and watch how the trajectories change. The same two masses at the same speeds can produce dramatically different outcomes depending on the angle of approach.

---

## Why This Matters Beyond Textbooks

Understanding collisions isn't academic. Every safety system in vehicles is built on collision physics:

- **Airbags** deploy based on predicted deceleration — which depends on the collision's energy absorption
- **Crumple zones** are designed to achieve a specific e ≈ 0.1–0.2, absorbing maximum energy while keeping the passenger compartment intact
- **Seat belts** work with the collision physics — they control the deceleration and prevent e from becoming 0 (which would mean the passenger stops instantly, causing massive internal injuries)

In sports, athletes instinctively understand restitution. Golf club faces are engineered for high e. Tennis players seek "sweet spots" where the collision is nearly elastic. Boxing gloves reduce e to protect the opponent — but also the puncher's hand.

---

## The Simulator as a Physics Laboratory

The interactive collision simulator lets you test scenarios that would be difficult to set up physically:

- Change the coefficient of restitution and watch energy loss change in real time on the kinetic energy chart
- Adjust the impact angle and see how the 2D trajectories shift
- Toggle slow motion to observe the exact moment of contact and separation
- Compare elastic (e=1) and inelastic (e=0) outcomes for identical starting conditions

The key insight the simulator reveals is that **momentum is always the same regardless of e** — but the trajectories and energy distributions are radically different. The momentum chart looks identical for e=0 and e=1, but the kinetic energy chart diverges immediately after impact.

This is perhaps the most counterintuitive aspect of collision physics: the thing that feels most "energetic" (a bouncy elastic collision) actually preserves more energy, while the "violent" inelastic collision dissipates energy into heat and deformation.

---

## The Bottom Line

Every collision in the universe is governed by two facts: momentum is always conserved, and energy loss is classified by a single number — the coefficient of restitution.

That number e is the difference between a ball that bounces back to your hand and one that sticks. Between a car that crumples safely and one that rebounds dangerously. Between a sport that rewards precision and one that rewards power.

The physics is simple. The consequences are everywhere.
