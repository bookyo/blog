# 3 Free tRPC Samples That Make TypeScript APIs Actually Type-Safe

Two weeks. That's how long a silent bug lived in production at a company I worked with. Their backend team renamed a field — `userId` became `user_id`. API docs updated. Frontend didn't. Every affected user saw the same thing: their profile would load, then silently drop the session. Nobody could reproduce it locally because the local frontend still had the old field name cached.

The fix was one line. Finding it took fourteen days.

This is not a logic bug. It's a **communication error between two systems that should never have been out of sync in the first place**. tRPC eliminates this entire class of problems at the architecture level — not through better testing or stricter code review, but by making the API contract itself impossible to violate.

## What tRPC Actually Is

tRPC (TypeScript Remote Procedure Call) lets you call server functions from your frontend as if they were local functions. No REST endpoints. No GraphQL queries. No generated code. You define a router on the server, import its type on the client, and TypeScript enforces the contract automatically.

Because the type flows from the server directly into the client with no build step, changing a response shape immediately surfaces errors at every call site. Not at runtime. At compile time.

## Sample 1: The Basic Router

The [first tRPC sample](https://elysiatools.com/en/samples/trpc) covers the core: queries, mutations, and subscriptions in a single router.

```typescript
const appRouter = t.router({
  hello: t.procedure.query(() => {
    return { greeting: 'Hello tRPC!' };
  }),

  getUser: t.procedure
    .input((val: unknown) => {
      if (typeof val === 'string' || typeof val === 'number') return String(val);
      throw new Error(`Invalid input`);
    })
    .query(({ input }) => {
      return { id: input, name: `User ${input}`, createdAt: new Date().toISOString() };
    }),

  createUser: t.procedure
    .input((val: unknown) => {
      const { name, email } = val as { name?: unknown; email?: unknown };
      if (typeof name !== 'string' || typeof email !== 'string') throw new Error('Invalid');
      return { name, email };
    })
    .mutation(({ input }) => {
      const user = { id: Math.random().toString(36).substr(2, 9), ...input };
      return { success: true, user };
    }),
});

export type AppRouter = typeof appRouter;
```

The exported `AppRouter` type is the only thing the client needs. No codegen. No schema files:

```typescript
const trpc = createTRPCProxyClient<AppRouter>({
  links: [httpBatchLink({ url: 'http://localhost:3000/trpc' })],
});

const user = await trpc.getUser.query('123');
// TypeScript knows the exact shape — compile-time safety, no build step
```

Rename a field on the server, and TypeScript flags every client call site immediately. That two-week bug would have been caught before the code shipped.

## Sample 2: Middleware and Authentication

The [second sample](https://elysiatools.com/en/samples/trpc) shows how tRPC middleware stacks into a production auth layer. JWT verification, role-based access, logging, and rate limiting — each is a reusable middleware that plugs into any procedure.

```typescript
const isAuthed = t.middleware(async ({ next, ctx }) => {
  const token = ctx.req.headers.authorization?.split(' ')[1];
  if (!token) throw new TRPCError({ code: 'UNAUTHORIZED' });

  const decoded = jwt.verify(token, secret);
  const user = db.users.find(u => u.id === decoded.userId);
  if (!user) throw new TRPCError({ code: 'UNAUTHORIZED', message: 'User not found' });

  return next({ ctx: { ...ctx, user } });
});

const hasRole = (role: 'admin' | 'user') => t.middleware(async ({ next, ctx }) => {
  if (ctx.user?.role !== role && ctx.user?.role !== 'admin') {
    throw new TRPCError({ code: 'FORBIDDEN', message: `Requires ${role} role` });
  }
  return next({ ctx });
});

const protectedProcedure = t.procedure.use(errorHandler).use(logger).use(isAuthed);
const adminProcedure = protectedProcedure.use(hasRole('admin'));
```

These compose into a clean, readable router:

```typescript
export const authRouter = t.router({
  getProfile: protectedProcedure.query(({ ctx }) => ctx.user),
  deleteUser: adminProcedure.mutation(({ input }) => { /* admin-only */ }),
  getSensitiveData: protectedProcedure.use(rateLimit).query(() => sensitiveData),
});
```

Because TypeScript carries the user type through the middleware into every procedure, the frontend also knows which routes require auth and which require admin privileges. Conditional rendering of admin panels becomes a type-level constraint, not a runtime check.

## Sample 3: React Integration

The [third sample](https://elysiatools.com/en/samples/trpc) bridges tRPC to React using `@trpc/react-query`. The result is a query/mutation API that feels native to React while preserving full type safety from the server.

```typescript
export const trpc = createTRPCReact<AppRouter>();

function Profile() {
  const utils = trpc.useContext();
  const { data: user, isLoading, error } = trpc.auth.getProfile.useQuery();
  const updateProfile = trpc.auth.updateProfile.useMutation({
    onSuccess: () => utils.auth.getProfile.invalidate(),
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return <ProfileEditor user={user} onSave={updateProfile.mutate} />;
}
```

TanStack Query handles caching and background refetching automatically. The sample also demonstrates optimistic updates for a todo list:

```typescript
const addTodo = trpc.todos.add.useMutation({
  onMutate: async (newTodo) => {
    await utils.todos.list.cancel();
    const previousTodos = utils.todos.list.getData();
    utils.todos.list.setData(undefined, (old) => [...(old || []), newTodo]);
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    utils.todos.list.setData(undefined, context?.previousTodos);
  },
  onSettled: () => utils.todos.list.invalidate(),
});
```

Sixteen lines for optimistic updates with automatic rollback. That same pattern typically requires a separate library in a REST or GraphQL setup.

## Why tRPC Is Worth 20 Minutes

The benefit compounds over time. There are three concrete wins.

First, **no API drift** — the type lives in one place, and the compiler enforces it everywhere. Second, **no codegen** — no generated files to commit, no build step to wait for, no stale output. Third, **deep type safety** — a change to a server response shape surfaces at every call site, across queries, mutations, and subscriptions.

The three samples on [ElysiaTools](https://elysiatools.com/en/samples/trpc) take you from first procedure to production auth to a React app with optimistic updates. Each is self-contained and thoroughly commented.

If you've spent an afternoon tracking down a bug caused by a renamed API field, tRPC pays that time back the first time it catches a mismatch before it reaches production.
