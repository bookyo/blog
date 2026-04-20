# Why a Simple Glass Triangle Creates Every Rainbow You've Ever Seen

In 1666, a 23-year-old Isaac Newton shut himself in a darkened room, punched a small hole in the shutters, and angled a glass prism until a beam of sunlight hit it. On the wall behind, white light fanned out into a spectrum — red, orange, yellow, green, blue, violet. The same colors in every sunset. The same colors in every rainbow. He had broken white light open and found it was made of hidden colors all along.

Three hundred and fifty years later, [ElysiaTools](https://elysiatools.com) hosts an interactive [Prism Dispersion simulator](https://elysiatools.com/en/visualizations/prism-dispersion) that lets you manipulate the same variables Newton could only guess at — prism material, apex angle, incident beam angle — and watch the spectrum separate in real time inside your browser.

Here's what that simulation reveals about why prisms, rainbows, and your camera lens all run on the same physics.

![Why a Simple Glass Triangle Creates Every Rainbow](https://blog.flowrust.com/wp-content/uploads/2026/04/opening-hook-52.png)

## Light Slows Down — But Not All Colors Slow Down Equally

When a beam of sunlight enters glass, it bends. That's refraction. But blue light bends more than red light, and that asymmetry changes everything.

The reason is wavelength. Blue light has a shorter wavelength (around 470 nanometers) than red light (around 700 nm). Shorter wavelengths interact more strongly with the glass material, which delays them more during the crossing. This wavelength-dependent slowdown is what makes white light fan out into a spectrum.

Physicists call this **dispersion**. It follows Cauchy's equation:

n(λ) = A + B/λ²

Where A and B are constants that differ for each material. Crown glass has different constants than flint glass. Diamond has yet another set — and its extreme dispersion is exactly why a well-cut diamond throws rainbow flashes across a room, while a plain glass prism barely separates colors at all. In spectroscopic instruments, scientists use this same relationship to identify the chemical elements present in a star's atmosphere by tracking where each wavelength lands on a detector.

![From Diamonds to Distant Stars](https://blog.flowrust.com/wp-content/uploads/2026/04/spectroscopy-connection.png)

## The Two Refractions That Do All the Work

Light entering a prism refracts once at the first surface. That begins separating colors, but the real spread happens at the second boundary — when light exits the prism back into air.

At that second refraction, the angles diverge further. Red exits at one angle, violet at another, and every wavelength in between occupies its own narrow slice of space. What you see projected on the wall is a map of which wavelength took which path.

The **apex angle** controls the spread. A 70° apex fans the spectrum wide. A 30° apex keeps colors tightly packed. This is why the triangular shape isn't decorative — it determines the geometry of separation.

The **material** determines how much each color diverges. Glass has an Abbe number around 55. Heavy flint glass sits at 30–40, producing vivid rainbow spreads. Diamond's Abbe number hits 60–70, which is why a diamond cutter positions facets so incoming light bounces around inside and exits in ways that maximize sparkle.

## Where the Same Physics Shows Up in Your Daily Life

![Your Camera Lens Fights the Same Physics](https://blog.flowrust.com/wp-content/uploads/2026/04/rainbow-revelation.png)

**Your camera lens** produces chromatic aberration — that faint colored fringing at the edges of a photo — because glass can't focus all wavelengths at the same point. Different colors land at slightly different distances from the lens center. The same dispersion, working against you.

**Binoculars and telescopes** use multiple lenses made from different glass types specifically to cancel this out. Pair a crown glass element with a flint glass element and the color separation from the first lens gets partially reversed by the second. Without this, looking through glass would feel like looking at a smeared rainbow.

**Rainbows** are water droplet prisms. Sunlight enters a roughly spherical water droplet, refracts, reflects off the inner back surface, and exits — and at each boundary, dispersion fans the light out. The red you see from one droplet arrives at a different angle than the violet from the same droplet, which is why colors stack vertically across the sky.

The [ElysiaTools simulation](https://elysiatools.com/en/visualizations/prism-dispersion) lets you explore all of this by dragging the incident angle, changing materials, and adjusting the apex angle. A live diagram shows normal lines, angle labels, and a deviation table that updates in real time, listing the exact exit angle for each of seven wavelengths from red (700nm) down to violet (400nm).

## The Configuration Scientists Actually Use

![You Can't Eliminate Dispersion](https://blog.flowrust.com/wp-content/uploads/2026/04/minimum-deviation.png)

There's a beam angle called the **minimum deviation position** — when the incoming and outgoing angles are symmetric with respect to the prism's bisector. At this configuration, the total angular spread reaches its smallest possible value for that geometry. This is the setup used in laboratory spectrometers, because it gives the most precise measurements.

The catch: minimum deviation is different for every color. You can't eliminate dispersion — you can only know exactly where each wavelength lands. The ElysiaTools simulator shows this numerically in its deviation table, making the trade-off visible in a way a textbook diagram never quite does.

## Why This Matters Beyond the Physics Lab

Dispersion sounds like an academic curiosity. But it shapes things you interact with constantly:

- **Eyeglass and camera optics** are designed around dispersion profiles — manufacturers select glass types to reduce color fringing, even if they can't eliminate it entirely
- **LED displays** show color separation at sharp brightness transitions for the same wavelength-dependent reason
- **Fiber optic cables** carry different wavelengths at slightly different speeds, which forces long-haul systems to actively compensate for pulse broadening

The same equation Newton stumbled onto in a dark room in 1666 governs all of it. One relationship — between refractive index and wavelength — cascading through every optical system we've built since.

---

**Try it:** The [Prism Dispersion simulator](https://elysiatools.com/en/visualizations/prism-dispersion) at ElysiaTools is free to use. No account, no plugins. Just open the page, move the sliders, and watch the spectrum respond in real time. Newton would have spent hours doing exactly this if he'd had a browser.