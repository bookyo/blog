# 8 Elysia.js Examples That Make Building TypeScript APIs Actually Enjoyable

Elysia.js benchmarks look incredible. Bun-powered, end-to-end typed, decorator-free. The numbers on the homepage will make any Node.js developer quietly jealous.

But benchmarks and "hello world" tutorials only get you so far. Real apps need routing patterns, validation, middleware composition, WebSocket connections, auth flows, and plugin architectures. That's where most framework examples abandon you.

These 8 Elysia.js samples don't. Each one is a complete, runnable project that you can copy into a Bun project and actually use.

---

## 1. Hello World — Your First Elysia Server

The entry point. A single file, one import, one route.

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
  .get('/', () => 'Hello, Elysia!')
  .listen(3000)
```

This isn't just a syntax demo. It's the foundation for understanding Elysia's declarative chain API. Every other example extends this pattern. The entire framework is built on this idea: compose small units into a full application.

**Why it matters:** Elysia's startup time is measured in microseconds. Your dev server restarts are instant. This changes how you iterate.

👉 [Try Hello World](https://elysiatools.com/en/samples/elysia)

---

## 2. Routing and Parameters

Static routes only get you so far. Real APIs have dynamic segments, query parameters, and multiple HTTP methods on the same path.

```typescript
const app = new Elysia()
  .get('/users/:id', ({ params }) => params.id)
  .post('/users', ({ body }) => createUser(body))
  .put('/users/:id', ({ params, body }) => updateUser(params.id, body))
  .delete('/users/:id', ({ params }) => deleteUser(params.id))
```

Elysia's routing is fully typed — `params.id` is inferred as a `string`, `body` is inferred from your validation schema. No casting, no `any`.

**Why it matters:** Parameter types flow through the entire request lifecycle. One typo in a route definition gets caught at compile time, not at 3 AM in production.

👉 [Try Routing & Parameters](https://elysiatools.com/en/samples/elysia)

---

## 3. Data Validation

Raw request bodies are a liability. Elysia uses `@sinclair/typebox` for schema validation — your schemas are also TypeScript types, and they double as JSON Schema for API documentation.

```typescript
import { t } from 'elysia'

const app = new Elysia()
  .post('/signup', ({ body }) => signUp(body), {
    body: t.Object({
      email: t.String({ format: 'email' }),
      password: t.String({ minLength: 8 }),
      age: t.Optional(t.Number({ minimum: 13 }))
    })
  })
```

If a request arrives with a missing email field or a password shorter than 8 characters, Elysia rejects it with a structured 400 response before your handler ever runs. No manual `if (!body.email)` guards needed.

**Why it matters:** Validation at the boundary costs you 3 lines of schema code. Validation scattered across your business logic costs you hours of debugging malformed data.

👉 [Try Data Validation](https://elysiatools.com/en/samples/elysia)

---

## 4. Middleware and Hooks

Every production API needs cross-cutting concerns: request logging, authentication checks, CORS headers, error handling. Elysia calls these `onBeforeHandle` and `onAfterHandle` hooks.

```typescript
const app = new Elysia()
  .derive(async ({ headers }) => {
    const token = headers['authorization']?.replace('Bearer ', '')
    return { user: await verifyToken(token) }
  })
  .onBeforeHandle(({ error }) => {
    if (!user) return error(401, 'Unauthorized')
  })
  .get('/profile', ({ user }) => user)
```

`derive` is particularly powerful — it lets you compute per-request state that's available in all subsequent handlers and hooks. Unlike middleware in Express or Fastify, Elysia's hooks are fully typed and composable.

**Why it matters:** `derive` runs once per request, even if the request hits 5 different handlers. Your auth lookup doesn't run twice.

👉 [Try Middleware & Hooks](https://elysiatools.com/en/samples/elysia)

---

## 5. WebSocket Support

Elysia has native WebSocket support. No adapter packages, no separate server setup.

```typescript
import { websocket } from 'elysia/websocket'

const app = new Elysia()
  .use(websocket())
  .ws('/chat', {
    message(ws, message) {
      ws.send(`Echo: ${message}`)
    },
    open(ws) {
      console.log('Client connected')
    },
    close(ws) {
      console.log('Client disconnected')
    }
  })
```

Elysia's WebSocket implementation integrates cleanly with its request lifecycle — hooks, derive, and error handling all work inside WebSocket handlers too. This is harder to achieve with Express-based solutions that bolt WebSocket on as an afterthought.

**Why it matters:** You get one server, one app, one TypeScript project. No port 3000 for HTTP and port 3001 for WebSocket. No coordinating two separate processes.

👉 [Try WebSocket Support](https://elysiatools.com/en/samples/elysia)

---

## 6. Plugin Development

Elysia's plugin system is its most underrated feature. A plugin is just a function that returns an `Elysia` instance — you can package routing, hooks, decorators, and state into a reusable unit.

```typescript
const cachePlugin = (ttl = 60_000) => new Elysia()
  .state('cache', new Map())
  .onAfterHandle(({ body, body: cacheEntry }) => {
    const cached = cache.get(cacheEntry?.key)
    if (cached && Date.now() - cached.timestamp < ttl)
      return cached.value
  })

const app = new Elysia()
  .use(cachePlugin(30_000))
  .get('/data', () => ({ key: 'expensive-query', value: computeIt() }))
```

This pattern means you can build, test, and distribute framework-agnostic plugins. The community already has plugins for rate limiting, JWT, Svelte integration, and more.

**Why it matters:** The plugin interface is a contract. When your plugin works, every Elysia app can use it with one line of code.

👉 [Try Plugin Development](https://elysiatools.com/en/samples/elysia)

---

## 7. JWT Authentication

Stateless auth with JSON Web Tokens is straightforward to get wrong. Elysia's JWT plugin handles the signing, verification, and expiry edge cases.

```typescript
import { jwt } from '@elysiajs/jwt'

const app = new Elysia()
  .use(jwt({ secret: Bun.env.JWT_SECRET }))
  .post('/login', async ({ body, jwt }) => {
    const user = await verifyCredentials(body.email, body.password)
    return {
      token: await jwt.sign({ sub: user.id, email: user.email }),
      expiresIn: 3600
    }
  })
  .get('/profile', ({ jwt }) => jwt.verify, {
    beforeHandle: ({ jwt, error }) =>
      jwt.verify ? true : error(401, 'Invalid token')
  })
```

The `jwt.sign()` call is cryptographically sound by default. The token expiry, algorithm, and claims are handled for you. What you'd normally reach for `jsonwebtoken` to do takes 3 lines in Elysia.

**Why it matters:** JWT setup is one of those things that looks simple and isn't. Elysia's plugin pins the security defaults to sensible values so you don't have to research which algorithm to use.

👉 [Try Authentication](https://elysiatools.com/en/samples/elysia)

---

## 8. GraphQL Integration

You need a GraphQL endpoint but don't want Apollo Server? Elysia pairs with `graphql-yoga` for a first-class GraphQL experience.

```typescript
import { createYoga, createSchema } from 'graphql-yoga'
import { Elysia } from 'elysia'

const schema = createSchema({
  typeDefs: `
    type Query { hello: String }
  `,
  resolvers: {
    Query: { hello: () => 'Hello from GraphQL!' }
  }
})

const app = new Elysia()
  .any('/graphql', ({ request }) =>
    yoga.handle(request)
  )
```

The key win here is that your GraphQL endpoint lives alongside your REST endpoints. You can gradually migrate an endpoint from REST to GraphQL without running two separate servers or managing CORS across multiple origins.

**Why it matters:** GraphQL and REST are not mutually exclusive. Elysia lets you use both in the same app, with the same plugin ecosystem, with the same deployment target (Bun).

👉 [Try GraphQL Integration](https://elysiatools.com/en/samples/elysia)

---

## Run All of Them in One Place

All 8 examples are collected at [elysiatools.com/en/samples/elysia](https://elysiatools.com/en/samples/elysia). You can browse each one, see the code, understand the theory, and run them directly in the browser.

No npm installs. No `bun add`. No scrolling through documentation hoping the example compiles.

---

## What's Missing

Elysia.js is still young. Database ORM integrations (Drizzle, Prisma), graceful shutdown handling, cluster mode, and comprehensive test utilities are areas where the ecosystem is catching up to Express/Fastify.

If you're building something that needs a battle-tested middleware ecosystem at scale, that's a real consideration. But for new projects where you want speed of iteration and end-to-end TypeScript, Elysia is worth the bet.

The 8 examples above give you a production-grade foundation to start from — not a toy tutorial that breaks the moment you deviate from the happy path.
