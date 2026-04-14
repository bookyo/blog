# 8 Astro Code Examples That Make Modern Web Development Actually Simple

Astro ships **zero JavaScript by default**. Yet you can embed React, Vue, or Svelte components wherever you need interactivity. That's the "islands architecture" — and it's changing how we think about web performance.

Most tutorials teach Astro basics. This post goes deeper: 8 real-world code patterns you'll actually use building production sites.

---

## 1. Hello World — Components, Routing, and Frontmatter

Every framework has a starting point. Astro's is unusually clean.

```astro
---
// Frontmatter: runs at BUILD time, not runtime
const title = "Welcome to Astro";
const features = [
  "Zero JS by default",
  "Islands Architecture",
  "Multi-framework support",
];
---

<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
</head>
<body>
  <h1>{title}</h1>
  <ul>
    {features.map(f => <li>{f}</li>)}
  </ul>
</body>
</html>
```

That `---` fence is the frontmatter. Any JavaScript between the fences runs at **build time** — not in the browser. This means your pages are pure HTML and CSS by default. No hydration overhead.

**When to use this**: Any static page where content is known at build time. A blog post, a product page, a documentation entry.

Try it → [Astro Hello World](https://elysiatools.com/en/samples/astro)

---

## 2. Islands Architecture — React, Vue, and Svelte on the Same Page

So far, everything is pure HTML. Now here's where Astro gets interesting.

Here's the deal: static content ships as HTML. Interactive widgets ship as **islands** — isolated JavaScript components that hydrate independently.

```astro
---
import ReactCounter from '../components/ReactCounter.tsx';
import VueTodo from '../components/VueTodo.vue';
---

<!-- Only these components send JS to the browser -->
<ReactCounter client:load initialCount={10} />
<VueTodo client:visible />
```

The `client:*` directives control hydration timing:
- `client:load` — hydrate immediately on page load
- `client:visible` — hydrate when the component scrolls into view
- `client:idle` — hydrate when the browser is idle

This means a page with 10 components, where only 1 is interactive, sends JavaScript for **1 component**. Not 10.

**When to use this**: Dashboards with widgets, e-commerce product pages, any page with a mix of static content and interactive elements.

Try it → [Astro Islands Integration](https://elysiatools.com/en/samples/astro)

---

## 3. Content Collections — Type-Safe Content Management

Now that you can build pages, you need a way to manage content. That's where collections come in. Astro validates your content frontmatter against a TypeScript schema at build time. Typos in your metadata? Build failure — not a broken page in production.

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    author: z.object({
      name: z.string(),
      email: z.string().email(),
    }),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```markdown
# src/content/blog/getting-started.md
---
title: "Getting Started with Astro"
pubDate: 2024-01-15
tags: ["astro", "tutorial"]
author:
  name: "Jane Smith"
  email: "jane@example.com"
draft: false
---

Content here...
```

Query it in any page:

```astro
---
import { getCollection } from 'astro:content';

const posts = await getCollection('blog', ({ data }) => {
  return !data.draft && data.pubDate <= new Date();
});
---
```

**When to use this**: Blogs, documentation sites, any project where content structure matters and you'd rather catch schema violations at build time than in production.

Try it → [Astro Content Collections](https://elysiatools.com/en/samples/astro)

---

## 4. Dynamic Routes — One Template, Many Pages

Once your content lives in collections, you'll want to render each piece as its own page. Astro makes this surprisingly simple.

Generate thousands of pages from a single template. Astro's `getStaticPaths()` runs at build time and produces static HTML for every route.

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = [
    { slug: "getting-started", title: "Getting Started with Astro" },
    { slug: "islands-architecture", title: "Islands Architecture Explained" },
    { slug: "performance-optimization", title: "Performance Optimization in Astro" }
  ];

  return posts.map(post => ({
    params: { slug: post.slug },
    props: { title: post.title }
  }));
}

const { title } = Astro.props;
const { slug } = Astro.params;
---

<h1>{title}</h1>
<p>Article slug: {slug}</p>
```

This generates `/blog/getting-started`, `/blog/islands-architecture`, and `/blog/performance-optimization` as static HTML files — no server needed.

**When to use this**: E-commerce product pages, documentation with many entries, any site where content comes from a CMS or database at build time.

Try it → [Astro Dynamic Routes](https://elysiatools.com/en/samples/astro)

---

## 5. API Endpoints — Serverless Functions Without a Server

Static pages cover a lot. But you'll eventually need server-side logic — form submissions, live data, authentication. Astro handles this too, without a separate backend.

Turn any `.ts` file in `src/pages/api/` into an API endpoint. No separate backend required.

```typescript
// src/pages/api/posts.json.ts
export async function GET() {
  const posts = [
    {
      id: 1,
      title: "Getting Started with Astro",
      author: "John Doe",
      date: "2024-01-15",
      tags: ["astro", "tutorial"]
    }
  ];

  return new Response(JSON.stringify(posts), {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

Visit `/api/posts.json` and you get JSON. Build the API as part of your Astro project, deploy to any host that supports Node.js or edge functions.

**When to use this**: Contact forms, search APIs, any lightweight backend logic that doesn't need a separate server.

Try it → [Astro API Endpoints](https://elysiatools.com/en/samples/astro)

---

## 6. Layouts — DRY Page Architecture

With pages, components, collections, and APIs in place, you'll notice every page shares the same HTML structure. That's where layouts save you.

Astro layouts are `.astro` components that wrap your pages. One layout, many pages — change the layout once, update everything.

```astro
---
// src/layouts/MainLayout.astro
export interface Props {
  title: string;
}
const { title } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title} - My Site</title>
</head>
<body>
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/blog">Blog</a>
      <a href="/about">About</a>
    </nav>
  </header>

  <main>
    <slot /> <!-- Page content is injected here -->
  </main>

  <footer>
    <p>&copy; {new Date().getFullYear()} My Site</p>
  </footer>
</body>
</html>
```

Use it in any page:

```astro
---
import MainLayout from '../layouts/MainLayout.astro';
---

<MainLayout title="Blog">
  <h1>My Blog Post</h1>
  <p>Content here...</p>
</MainLayout>
```

**When to use this**: Every site. Layouts are the foundation of a maintainable Astro project.

Try it → [Astro Layouts](https://elysiatools.com/en/samples/astro)

---

## 7. MDX — Interactive Markdown

Layouts handle structure. But what about the content itself? MDX brings Markdown and components together.

MDX extends Markdown with JSX components. Write content in Markdown, embed interactive React or Vue components anywhere in the prose.

```mdx
# My Blog Post

Here's a counter embedded in my article:

import ReactCounter from '../components/ReactCounter';

<ReactCounter client:load initialCount={5} />

And here's the rest of the article text...
```

Your content authors write Markdown. Your developers embed components. Both workflows coexist without conflict.

**When to use this**: Documentation with live demos, blog posts with interactive examples, any content-heavy site that needs selective interactivity.

Try it → [Astro MDX Integration](https://elysiatools.com/en/samples/astro)

---

## 8. Partial Hydration — Performance by Default

Astro's hydration directives give you granular control over what ships JavaScript:

| Directive | When it hydrates |
|---|---|
| `client:load` | Immediately on page load |
| `client:idle` | When browser is idle |
| `client:visible` | When component enters viewport |
| `client:media` | When a CSS media query matches |
| `client:only` | Client-side only (skip SSR) |

```astro
<!-- Hydrate when visible — below the fold -->
<HeavyChart client:visible data={chartData} />

<!-- Hydrate only on mobile -->
<MobileMenu client:media="(max-width: 768px)" />

<!-- Never hydrate — static HTML only -->
<StaticCallout content={calloutText} />
```

This is the practical difference between a 100ms page load and a 2s page load. Ship JS only where it's needed.

**When to use this**: Everywhere. The mental model is simple: components are HTML by default, interactive only when you explicitly opt in.

Try it → [Astro Hydration Directives](https://elysiatools.com/en/samples/astro)

---

## The Shift That Changes Everything

Here's the mental model that flips performance on its head: most frameworks ask "how do I reduce JavaScript?" Astro asks "why would I add it?"

It reframes every architectural decision. Instead of code-splitting your way to a fast React app, you start from zero JavaScript and add only what the user actually needs.

A typical Astro blog scores **Lighthouse 100** out of the box. A comparable React SPA needs careful optimization to reach 80. That's not a knock on React — it's a testament to what happens when you default to no JavaScript instead of fighting to remove it.

What would your site look like if you shipped no JavaScript by default?

Start exploring → [Browse all Astro samples on ElysiaTools](https://elysiatools.com/en/samples/astro)
