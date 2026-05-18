# Why Everything Falls at the Same Speed: The Surprising Physics of Free Fall

Drop a bowling ball and a tennis ball from the same height. Most people expect the heavier one to hit the ground first — intuition screams it. Galileo disagreed, and gravity doesn't care about your intuition either.

This is the story of what actually happens when things fall, why the math is deceptively elegant, and how an interactive free fall simulator makes the abstract tangible.

## The Equation That Governs Everything Falling

The motion of free fall comes straight from Newton's second law. A mass m under gravity g experiences a force mg, so:

**a = F/m = mg/m = g**

The mass cancels out. Every object in free fall accelerates at approximately 9.8 m/s² near Earth's surface — regardless of mass, shape, or what it's made of.

From this, the position and velocity follow cleanly:

**h(t) = h₀ + v₀t − ½gt²**

**v(t) = v₀ − gt**

Where h₀ is initial height, v₀ is initial velocity, and g = 9.8 m/s². The sign convention (positive upward) is your choice — what matters is that acceleration is constant.

## The Drop Test: What 100 Meters Looks Like

Set initial height to 100 meters with zero initial velocity. Here's what the simulation reveals:

- **Time to impact**: t = √(2h₀/g) = √(200/9.8) ≈ **4.52 seconds**
- **Velocity at impact**: v = gt ≈ **44.3 m/s** (about 159 km/h)

The height chart shows the familiar parabola — position drops increasingly fast as time goes on. The velocity chart shows a straight line downward — constant acceleration means linear velocity change. These two different-looking curves are exactly linked: velocity is the derivative of position, acceleration is the derivative of velocity.

## Energy: Where the Real Surprise Lives

Here's what most people don't expect. As the object falls, potential energy converts to kinetic energy — but the **total energy stays constant**.

- **Potential energy**: PE = mgh (decreases as height decreases)
- **Kinetic energy**: KE = ½mv² (increases as velocity increases)
- **Total energy**: PE + KE = constant (ignoring air resistance)

The free fall simulator shows this with real-time energy bars. Watch the green kinetic bar climb as the blue potential bar shrinks. The total energy bar barely budges. This is energy conservation in its purest form — no friction, no air drag, just the cleanest transaction in physics.

## Why Heavier Things Don't Fall Faster

This is the part that trips everyone up. If you drop a hammer and a feather, the feather floats down while the hammer plummets. Galileo said they'd hit together in vacuum. Apollo 15 proved it on the Moon in 1971 — hammer and feather fell side by side in the lunar atmosphere, hitting the dust at the same instant.

The intuition that heavier things fall faster comes from mixing up mass and weight, and forgetting about air resistance. In vacuum, there is no difference. On Earth, for most practical objects, the air resistance effect is small enough that we barely notice — a 1 kg steel ball and a 1 kg aluminum ball fall at nearly the same rate.

The equation a = g tells you why. The m in F = ma cancels with the m in F = mg. More mass means more gravitational force, but also more inertia. They cancel perfectly.

## The Physics in the Code

The simulation's core calculation is a direct translation of the equations:

```javascript
// Height: h(t) = h₀ - ½gt² + v₀t
const height = h0 - (0.5 * g * time * time) + (v0 * time);

// Velocity: v(t) = v₀ - gt
const velocity = v0 - (g * time);

// Energies
const potentialEnergy = mass * g * Math.max(0, height);
const kineticEnergy = 0.5 * mass * velocity * velocity;
const totalEnergy = potentialEnergy + kineticEnergy;
```

Default parameters: initialHeight = 100m, initialVelocity = 0, mass = 1.0kg, gravity = 9.8 m/s². The simulation tracks position, velocity, and energy at each timestep, drawing the falling object, its trail, and live charts of height vs. time and velocity vs. time.

## Galileo's Insight, 400 Years Later

Galileo couldn't measure fast enough to see free fall clearly. He rolled balls down inclined planes to slow things down, then extrapolated. We can do better — a real-time simulation with 60fps charts shows exactly what he predicted: constant acceleration, mass-independent fall, and energy trading like a transaction at a vault.

The next time someone tells you a heavier object falls faster, point them to the equation. Or better yet, open the simulator, set the initial height to 100 meters, and watch the energy bars do the talking.

Physics doesn't negotiate.
