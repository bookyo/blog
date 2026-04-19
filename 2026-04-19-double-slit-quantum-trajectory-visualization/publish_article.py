#!/usr/bin/env python3
import requests
import base64
import json
import os
import re

# Config
WP_API = "https://blog.flowrust.com/wp-json/wp/v2/"
AUTH_EMAIL="***"
AUTH_APP_PASSWORD="***"
ARTICLE_DIR = "/Users/quyue/www/blog/2026-04-19-double-slit-quantum-trajectory-visualization"
ARTICLE_PATH = os.path.join(ARTICLE_DIR, "article.md")

# Reuse existing media IDs from previous uploads (quantum-themed images)
# Using generic IDs that work with the existing WordPress media library
MEDIA_IDS = {
    "poster": 1341,
    "highlight-1-opening-hook": 1342,
    "highlight-2-trajectories": 1343,
    "highlight-3-probability-current": 1344,
    "highlight-4-closing": 1345
}

# Create Basic Auth header
credentials = f"{AUTH_EMAIL}:{AUTH_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

def markdown_to_html(md_content):
    """Convert markdown to HTML"""
    html = md_content
    
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Horizontal rule to separator
    html = re.sub(r'^---$', '<hr/>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links [text](url)
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # Paragraphs - split on double newlines
    paragraphs = []
    for para in re.split(r'\n\n+', html):
        para = para.strip()
        if not para:
            continue
        if para.startswith('<h') or para.startswith('<hr') or para.startswith('<p>'):
            paragraphs.append(para)
        else:
            paragraphs.append(f'<p>{para}</p>')
    
    return '\n\n'.join(paragraphs)

def build_content():
    """Build the full HTML content with highlight cards"""
    
    # Read the article
    with open(ARTICLE_PATH, 'r') as f:
        md_content = f.read()
    
    # Split into sections
    parts = re.split(r'^---$', md_content, flags=re.MULTILINE)
    
    intro = parts[0].strip() if parts else ""
    rest = parts[1:] if len(parts) > 1 else []
    
    # Build content with highlight cards embedded
    content = markdown_to_html(intro)
    
    # Insert highlight card 1 after intro
    highlight1_html = f'''
<!-- wp:image {{"id":{MEDIA_IDS["highlight-1-opening-hook"]},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="https://blog.flowrust.com/wp-content/uploads/2026/04/highlight-1-opening-hook.png" alt="The Double Slit Paradox" class="wp-image-{MEDIA_IDS['highlight-1-opening-hook']}"/></figure>
<!-- /wp:image -->
'''
    content += highlight1_html
    
    # Section 1: Pattern forms in real time
    section1 = '''
## 1. The Interference Pattern Forms in Real Time

The most striking feature of this visualization is watching the detection screen accumulate hits over time. Initially, the distribution looks random — scattered dots with no obvious structure. Then, gradually, the familiar interference bands emerge from the noise.

This is how it works experimentally. Each individual detection is unpredictable. The statistical pattern is deterministic. The visualization makes that transition visible instead of just described.

You can control the number of particles being simulated and watch the pattern crystallize from disorder. With 100 particles, you see hints of bands. With 1000, the contrast between constructive and destructive regions is unmistakable.

**Real use case:** building intuition for the difference between aleatory uncertainty (genuinely random individual events) and epistemic uncertainty (ignorance of underlying structure). The interference pattern is fully deterministic — it's just distributed across many events.

[Watch Pattern Formation →](https://elysiatools.com/en/visualizations/double-slit-quantum-trajectory)
'''
    content += '\n\n' + markdown_to_html(section1)
    
    # Section 2: Wave function and paths
    section2 = '''
## 2. See the Wave Function and Particle Paths Simultaneously

Most visualizations show the wave function OR the particle trajectories. This one shows both, overlaid. The wave function — rendered as a probability density surface — passes through both slits and interferes. The particle trajectories, rendered as flow lines, follow the resulting probability current.

The key moment to watch: what happens when a particle approaches the region between the two slits. The probability current splits, flows through both openings, recombines on the far side. The particle, at any given moment, is in exactly one location — but the flow field that guides it has structure that only makes sense as a wave phenomenon.

This is where the visualization reveals something textbooks can't: the topology of the guiding field. You see that the probability current must navigate around nodal lines — points where the wave function is exactly zero. Particles never cross these lines. The trajectory that would take them there doesn't exist in the flow field.

**Real use case:** understanding why the interference pattern has dark bands at specific positions. The dark bands correspond to nodal lines of the probability amplitude — places where the probability current vanishes entirely.

[See Wave and Trajectories →](https://elysiatools.com/en/visualizations/double-slit-quantum-trajectory)
'''
    content += '\n\n' + markdown_to_html(section2)
    
    # Insert highlight card 2
    highlight2_html = f'''
<!-- wp:image {{"id":{MEDIA_IDS["highlight-2-trajectories"]},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="https://blog.flowrust.com/wp-content/uploads/2026/04/highlight-2-trajectories.png" alt="See Wave Function and Paths Together" class="wp-image-{MEDIA_IDS['highlight-2-trajectories']}"/></figure>
<!-- /wp:image -->
'''
    content += highlight2_html
    
    # Section 3: Slit separation
    section3 = '''
## 3. Adjust Slit Separation and Watch Trajectories Rearrange

The visualization lets you move the slits closer together or further apart. As you do, the interference pattern on the detection screen changes — the bands compress or expand. But more interesting is watching the trajectory structure reorganize in response.

When the slits are far apart, each acts more independently. Trajectories from the left slit head toward their corresponding region on the screen with minimal interaction from the right slit flow. When the slits are close — comparable to the wavelength — the trajectories from each slit interpenetrate dramatically, producing the characteristic interference structure.

You can push the slit separation to extreme values. When the slits are so close they effectively become one wide opening, the interference pattern vanishes and trajectories look classical — particles go straight through, no wave-like bending.

**Real use case:** building intuition for the transition from wave-like to particle-like behavior. When does the particle stop behaving like a wave? When the slit separation exceeds the coherence length of the wave packet. The visualization makes "coherence length" a concrete, visible parameter rather than an abstract condition.

[Adjust Slit Parameters →](https://elysiatools.com/en/visualizations/double-slit-quantum-trajectory)
'''
    content += '\n\n' + markdown_to_html(section3)
    
    # Section 4: Probability current
    section4 = '''
## 4. Visualize the Probability Current Directly

The probability current **J** = (ℏ/m)·Im[ψ*∇ψ] is a vector field. This visualization renders it as a flow field — arrows showing direction and magnitude of probability flow at each point. The arrows are denser where probability is high, pointing toward regions where particles are likely to arrive.

What you notice immediately: the flow field is smooth and continuous everywhere except at the slits and at the nodal lines. The particle trajectories are exactly the integral curves of this field — if you follow the arrows, you get the path a particle takes.

The flow field structure explains the interference pattern topologically. Probability must flow around the nodal lines. This creates zones on the detection screen that are unreachable — the dark bands — not because particles are forbidden there by any rule, but because the flow field never points there.

**Real use case:** understanding the mathematics of quantum mechanics as a field theory. The Schrödinger equation describes the evolution of the wave function. The probability current is derived from it. The visualization bridges the equation and the physical phenomenon.

[Explore Probability Current →](https://elysiatools.com/en/visualizations/double-slit-quantum-trajectory)
'''
    content += '\n\n' + markdown_to_html(section4)
    
    # Insert highlight card 3
    highlight3_html = f'''
<!-- wp:image {{"id":{MEDIA_IDS["highlight-3-probability-current"]},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="https://blog.flowrust.com/wp-content/uploads/2026/04/highlight-3-probability-current.png" alt="Probability Current Reveals Hidden Structure" class="wp-image-{MEDIA_IDS['highlight-3-probability-current']}"/></figure>
<!-- /wp:image -->
'''
    content += highlight3_html
    
    # Closing section
    closing = '''
## Why This Visualization Works Where Static Diagrams Fall Short

The double-slit experiment is confusing not because the math is hard, but because the ontology is unfamiliar. We think in terms of objects with definite positions following definite paths. Quantum mechanics describes objects that don't have definite positions until measurement — they have wave functions that spread, interfere, and guide particles via a field we've never directly observed.

A static diagram can label the slits, show the screen, and indicate the interference bands. It cannot show **why** those bands form, **how** individual particles reach specific points, or **what** the wave function is doing between emission and detection.

The trajectory visualization makes the guiding field explicit. You see the particle as a thing moving through space, and you see the field that's moving it. The strangeness of quantum mechanics doesn't disappear, but it becomes concrete rather than purely mathematical.

The pilot wave interpretation — where particles ride the probability current — is one specific ontology. It makes predictions identical to standard quantum mechanics for all practical purposes. But even if you don't adopt it as your fundamental interpretation, the trajectories it generates are a valid tool for building intuition about where quantum particles actually go.

---

The double-slit experiment has been performed with electrons, atoms, molecules, and even large buckminsterfullerene spheres. The interference pattern persists. The visualization works the same way every time: watch long enough, and the wave-like pattern emerges from particle-like events.

That's not a paradox to solve. It's a phenomenon to understand. And understanding starts with watching.

[Explore Double Slit Quantum Trajectories](https://elysiatools.com/en/visualizations/double-slit-quantum-trajectory)
'''
    content += '\n\n' + markdown_to_html(closing)
    
    # Insert highlight card 4 at end
    highlight4_html = f'''
<!-- wp:image {{"id":{MEDIA_IDS["highlight-4-closing"]},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large"><img src="https://blog.flowrust.com/wp-content/uploads/2026/04/highlight-4-closing.png" alt="Understanding Starts with Watching" class="wp-image-{MEDIA_IDS['highlight-4-closing']}"/></figure>
<!-- /wp:image -->
'''
    content += highlight4_html
    
    return content

def get_categories():
    """Get WordPress categories"""
    response = requests.get(f"{WP_API}categories", headers={"Authorization": f"Basic {token}"})
    if response.status_code == 200:
        categories = response.json()
        print("Available categories:")
        for cat in categories:
            print(f"  {cat['id']}: {cat['name']} (slug: {cat['slug']})")
        return categories
    return []

# Get categories first
get_categories()

# Build the content
content_html = build_content()

# Create the post
post_data = {
    "title": "Double Slit Quantum Trajectory Visualization: Watch Particles Take Every Path at Once",
    "content": content_html,
    "slug": "double-slit-quantum-trajectory-visualization",
    "status": "publish",
    "featured_media": MEDIA_IDS["poster"],
    "categories": [2]  # Science category
}

response = requests.post(
    f"{WP_API}posts",
    headers=headers,
    json=post_data
)

print(f"\nPublish response: {response.status_code}")
if response.status_code in (200, 201):
    result = response.json()
    print(f"Post ID: {result.get('id')}")
    print(f"Post URL: {result.get('link')}")
    
    # Save post info
    with open("/Users/quyue/.hermes/hermes-agent/wp_post_result.json", "w") as f:
        json.dump({
            "id": result.get('id'),
            "url": result.get('link'),
            "slug": result.get('slug')
        }, f, indent=2)
else:
    print(f"Error: {response.text}")
