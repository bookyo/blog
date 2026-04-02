# 8 Three.js WebGL Examples That Prove Browser Graphics Have Arrived

The browser is no longer a 2D document viewer. With WebGL and Three.js, it is a full 3D platform — and you do not need a native app to run it.

Three.js sits at the center of this shift. It abstracts the complexity of WebGL, giving developers a clean API to create scenes, materials, animations, and interactive 3D experiences that run anywhere a browser does. Today we are going to walk through 8 production-ready Three.js examples that cover everything from your first 3D scene to advanced camera systems.

All examples are live and interactive — no download, no build step, no server required.

---

## 1. Scene Setup — Your First Three.js World

Every Three.js project starts here. You need three things: a **Scene** to hold your objects, a **Camera** to define perspective, and a **Renderer** to draw everything to the screen.

```javascript
import * as THREE from 'three';

class BasicScene {
    init() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x87CEEB);

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.z = 5;

        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        document.body.appendChild(this.renderer.domElement);

        this.addLights();
        this.addObjects();
        this.animate();
    }

    addLights() {
        const ambient = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambient);

        const directional = new THREE.DirectionalLight(0xffffff, 0.8);
        directional.position.set(10, 10, 5);
        directional.castShadow = true;
        this.scene.add(directional);
    }

    addObjects() {
        const cube = new THREE.Mesh(
            new THREE.BoxGeometry(1, 1, 1),
            new THREE.MeshPhongMaterial({ color: 0x00ff00, shininess: 100 })
        );
        cube.castShadow = true;
        this.scene.add(cube);

        const sphere = new THREE.Mesh(
            new THREE.SphereGeometry(0.7, 32, 32),
            new THREE.MeshPhongMaterial({ color: 0xff0000, shininess: 100 })
        );
        sphere.position.x = -2;
        this.scene.add(sphere);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.cube.rotation.x += 0.01;
        this.cube.rotation.y += 0.01;
        this.renderer.render(this.scene, this.camera);
    }
}
```

This pattern scales to any complexity. Add a ground plane, load a 3D model, or drop in thousands of particles — the core loop stays the same. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 2. Interactive Picking — Clicking Objects in 3D Space

Static scenes are display-only. Real interactivity requires **raycasting** — projecting a ray from the mouse into the 3D scene to detect which object the user is pointing at.

```javascript
class InteractiveScene {
    init() {
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();

        window.addEventListener('mousemove', (event) => {
            this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        window.addEventListener('click', () => {
            if (this.intersectedObject) {
                // Spin the clicked object
                this.animateClick(this.intersectedObject);
            }
        });
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));

        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.objects);

        // Reset all objects
        this.objects.forEach(obj => {
            obj.material.color.setHex(obj.userData.originalColor);
            obj.scale.setScalar(obj.userData.originalScale);
        });

        // Highlight hovered object
        if (intersects.length > 0) {
            this.intersectedObject = intersects[0].object;
            this.intersectedObject.material.color.setHex(0xffffff);
            this.intersectedObject.scale.setScalar(1.2);
        }
    }
}
```

Once you can pick objects, you can drag them, change their materials, spawn particles on click, or build entire games. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 3. Particle Systems — Thousands of Moving Points

Three.js handles 10,000+ particles without breaking a sweat using **BufferGeometry**. Each particle is just three floats for position and three for color — stored in typed arrays for maximum efficiency.

```javascript
createParticles() {
    const particleCount = 10000;
    const geometry = new THREE.BufferGeometry();

    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        positions[i3]     = (Math.random() - 0.5) * 100;
        positions[i3 + 1] = (Math.random() - 0.5) * 100;
        positions[i3 + 2] = (Math.random() - 0.5) * 100;

        const color = new THREE.Color();
        color.setHSL(Math.random(), 0.7, 0.5);
        colors[i3] = color.r;
        colors[i3 + 1] = color.g;
        colors[i3 + 2] = color.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color',    new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 1,
        vertexColors: true,
        blending: THREE.AdditiveBlending,
        transparent: true,
        opacity: 0.8
    });

    this.particles = new THREE.Points(geometry, material);
    this.scene.add(this.particles);
}
```

With `AdditiveBlending`, particles glow as they overlap — creating nebulae, fire, smoke, and rain from the same primitive. This means 10,000 particles draw in a single draw call. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 4. Materials and Lighting — Beyond Basic Colors

Three.js ships with 8 material types, each suited for different rendering needs. For realistic surfaces in 2026, you want **MeshStandardMaterial** (PBR) or **MeshPhysicalMaterial** (advanced PBR with clearcoat).

```javascript
const materials = [
    new THREE.MeshBasicMaterial({ color: 0xff0000 }),
    new THREE.MeshLambertMaterial({ color: 0x00ff00 }),
    new THREE.MeshPhongMaterial({ color: 0x0000ff, specular: 0x444444, shininess: 100 }),
    new THREE.MeshStandardMaterial({
        color: 0xffd700,
        metalness: 0.5,
        roughness: 0.5
    }),
    new THREE.MeshPhysicalMaterial({
        color: 0xff1493,
        metalness: 0.7,
        roughness: 0.3,
        clearcoat: 1.0,
        clearcoatRoughness: 0.0
    }),
    new THREE.MeshToonMaterial({
        color: 0x00ff7f,
        gradientMap: this.createGradientMap()
    }),
];
```

The difference between `roughness: 0.1` and `roughness: 0.9` on the same metallic sphere is the difference between chrome and clay. Physical accuracy is not an accident — it is tuned. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 5. Shadows — The Detail That Makes 3D Real

Flat objects look cardboard. Shadows make them grounded. Three.js uses **PCFSoftShadowMap** by default, which produces soft edges that look natural rather than pixelated.

```javascript
// Enable shadows on the renderer
this.renderer.shadowMap.enabled = true;
this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Each light that casts shadows
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;

// Each object that casts or receives
cube.castShadow = true;
cube.receiveShadow = true;
ground.receiveShadow = true;
```

One directional light with shadow casting enabled can transform a flat scene into something that feels dimensional. The cost: shadow maps are expensive. Limit shadow casters to 1–3 key lights. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 6. Advanced Animation — Bounce, Orbital, Particle Fountain

Three.js animation is not a framework — it is a pattern. You update object properties inside `requestAnimationFrame`, and the browser handles timing. The skill is knowing what to animate and how.

```javascript
// Bouncing ball with squash-and-stretch
animate() {
    const time = this.clock.getElapsedTime();
    const bounceHeight = Math.abs(Math.sin(time * frequency)) * amplitude;
    ball.position.y = baseY + bounceHeight;

    const squashFactor = 1 - (bounceHeight / amplitude) * (1 - squash);
    ball.scale.y = squashFactor;
    ball.scale.x = ball.scale.z = 1 / squashFactor;
}

// Orbital system — planets around a sun
planets.forEach((planet) => {
    const angle = time * planet.speed;
    planet.mesh.position.x = center.x + Math.cos(angle) * planet.distance;
    planet.mesh.position.z = center.z + Math.sin(angle) * planet.distance;
});

// Particle fountain with gravity
positions[i + 1] += velocities[i + 1] * deltaTime;
velocities[i + 1] += gravity; // gravity = -0.02
```

Animation brings objects to life. A cube rotating on its axes is geometry. A bouncing ball with squash on impact and stretch at peak height is physics you can feel. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 7. Camera Controls — Orbit, Fly, and FPS Modes

Different applications need different camera behaviors. A product showcase wants orbit controls. A flight simulator wants free movement. Three.js supports both — and you can switch between them at runtime.

```javascript
// Orbit — rotate around a target point
case 'orbit':
    spherical.theta -= deltaX * 0.01;
    spherical.phi += deltaY * 0.01;
    spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));
    this.camera.position.setFromSpherical(spherical);
    this.camera.lookAt(0, 0, 0);
    break;

// Fly — free movement with WASD
case 'fly':
    forward.applyQuaternion(this.camera.quaternion);
    if (this.keys['w']) this.camera.position.addScaledVector(forward, speed);
    if (this.keys['a']) this.camera.position.addScaledVector(right, -speed);
    break;
```

The same Three.js camera, two completely different experiences — and both are under 20 lines of code. [Try it live →](https://elysiatools.com/en/samples/threejs)

---

## 8. Wireframe Scenes — Debugging Meets Design

Wireframe mode renders only the edges of geometry — no surfaces, no textures, just structure. It is the fastest way to debug complex scenes, but it is also an aesthetic choice in its own right.

```javascript
const wireframeMaterial = new THREE.MeshBasicMaterial({
    color: 0x00ff00,
    wireframe: true
});

const torus = new THREE.Mesh(
    new THREE.TorusGeometry(1, 0.4, 16, 100),
    wireframeMaterial
);

// Add a grid helper for orientation
const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
this.scene.add(gridHelper);
```

In a single afternoon, you can go from "I want a 3D scene" to a particle nebula orbiting a glowing wireframe planet — all in the browser. The tools have caught up to the ambition.

---

## Explore All Three.js Examples

Every example above is live, interactive, and open-source. No account, no API key, no setup.

👉 **[https://elysiatools.com/en/samples/threejs](https://elysiatools.com/en/samples/threejs)**

Or browse the full library — there are **200+ tools, visualizations, and code samples** covering everything from Babylon.js to signal processing.

---

*All examples run entirely in the browser. No build tools, no server, no install — just open and explore.*
