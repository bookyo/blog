# 8 Free Supabase Sample Projects That Replace Firebase — And Run Locally

Firebase locked you in. Supabase doesn't.

In the last year, Supabase has become the go-to backend-as-a-service for developers who want PostgreSQL power without the vendor lock-in. But the hardest part isn't choosing Supabase — it's bootstrapping a project fast enough to validate your architecture before committing to it.

[ElysiaTools](https://elysiatools.com) offers **three free, comprehensive Supabase sample projects** covering database operations, authentication, and real-time subscriptions — complete with TypeScript, React hooks, and schema definitions. No Firebase, no proprietary SDK lock-in, no "contact sales" to unlock features.

---

## 1. Supabase Basic Operations — Your First Database Class

Every app starts with CRUD. This sample gives you a production-ready `SupabaseManager` class with:

```typescript
// Create operation
async createRecord(tableName, data) {
    const { data: insertedData, error } = await this.client
        .from(tableName)
        .insert([data])
        .select();
    // ...
}
```

The class handles filtering, ordering, pagination, and error management out of the box. **Use it when:** You're building a new app and need a clean pattern for database access before your schema stabilizes.

[Try Basic Operations Sample →](https://elysiatools.com/en/samples/supabase)

---

## 2. Full-Text Search — The Query That Makes Users Stay

Standard `LIKE` queries don't scale. This sample shows how to implement PostgreSQL full-text search in Supabase:

```typescript
async searchRecords(tableName, searchTerm, columns = ['name', 'description']) {
    const { data, error } = await this.client
        .from(tableName)
        .select('*')
        .or(columns.map(col => `${col}.ilike.%${searchTerm}%`).join(','));
    // ...
}
```

It searches across multiple columns simultaneously and handles empty results gracefully. **Use it when:** Your users expect Google-like search across product catalogs, article archives, or user-generated content.

[Try Full-Text Search Sample →](https://elysiatools.com/en/samples/supabase)

---

## 3. Authentication Patterns — More Than Just "Sign In"

Supabase Auth is powerful. This sample shows how to build complete authentication flows:

- **Sign up with metadata** — attach role, name, and custom fields
- **OAuth integration** — GitHub, Google, Facebook with proper redirect handling
- **Session persistence** — automatic token refresh and URL-based session detection
- **Password management** — reset, update, and session invalidation

```typescript
async signUp(email: string, password: string, metadata?: Record<string, any>) {
    const response = await this.supabase.auth.signUp({
        email, password,
        options: { data: { name: metadata?.name, role: metadata?.role || 'user' } }
    });
    // Creates user profile in database automatically
}
```

**Use it when:** You need user accounts with roles (admin/moderator/user) and don't want to build auth from scratch.

[Try Authentication Sample →](https://elysiatools.com/en/samples/supabase)

---

## 4. React Auth Hook — The 20-Line Solution to Session Management

Copy-paste this hook and stop rewriting auth state logic:

```typescript
export function useAuth() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Initialize from persisted session
        const initializeAuth = async () => {
            const currentUser = await authService.getCurrentUser();
            setUser(currentUser);
            setLoading(false);
        };
        initializeAuth();
        // Listen for auth changes
        const unsubscribe = authService.onAuthStateChange((event, session) => {
            setUser(session?.user ?? null);
        });
        return unsubscribe;
    }, []);
    // Returns { user, loading, signUp, signIn, signOut, resetPassword, updatePassword }
}
```

**Use it when:** You have a React app and want auth that survives page refreshes, tab closes, and token expiry without Redux or context boilerplate.

[Try Auth Hook Sample →](https://elysiatools.com/en/samples/supabase)

---

## 5. Authorization Service — RBAC Without the Headache

Most auth tutorials stop at "logged in or not." This sample implements full role-based access control:

```typescript
async hasRole(userId: string, requiredRole: string): Promise<boolean> {
    const { data: profile } = await this.supabase
        .from('user_profiles')
        .select('role')
        .eq('id', userId)
        .single();
    return profile.role === requiredRole;
}
```

It supports role hierarchies (admin > moderator > user), permission grants/revocation, and resource-level access checks. **Use it when:** Your app has different permission levels and you need to protect routes and API calls without middleware spaghetti.

[Try Authorization Sample →](https://elysiatools.com/en/samples/supabase)

---

## 6. Real-time Subscriptions — The WebSocket Pattern That Actually Works

Supabase's real-time engine is underrated. This sample shows how to subscribe to database changes:

```typescript
subscribeToTable(tableName, event, callback, filter?) {
    const channel = this.supabase
        .channel(subscriptionName)
        .on('postgres_changes', {
            event, schema: 'public', table: tableName, filter
        }, callback)
        .subscribe((status) => {
            if (status === 'SUBSCRIBED') {
                console.log(`Subscribed to ${tableName} ${event} events`);
            }
        });
}
```

Supports INSERT, UPDATE, DELETE events, column filters, and automatic reconnection. **Use it when:** You need live updates — collaborative editing, dashboards, notifications, or multiplayer features.

[Try Real-time Sample →](https://elysiatools.com/en/samples/supabase)

---

## 7. File Storage — With Progress Tracking

Supabase Storage handles files. This sample adds the missing pieces:

```typescript
async uploadWithProgress(bucket, path, file, onProgress) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                onProgress((event.loaded / event.total) * 100);
            }
        });
        // ...
    });
}
```

Includes signed URLs for private files, public URL generation, file listing, and deletion. **Use it when:** You need user uploads (avatars, documents, attachments) with real progress feedback instead of silent uploads.

[Try Storage Sample →](https://elysiatools.com/en/samples/supabase)

---

## 8. Collaborative Editor — The Pattern Behind Google Docs

Real-time collaboration sounds scary until you see the pattern. This sample implements:

- **Document subscription** — auto-updates content when other users edit
- **Presence tracking** — see who's currently viewing/editing
- **Cursor broadcasting** — show where collaborators are working

```typescript
export function useCollaborativeEditor(documentId) {
    // Subscribes to document changes
    const documentChannel = realtimeService.subscribeToTable(
        'documents', 'UPDATE', `id=eq.${documentId}`,
        (payload) => { setContent(payload.new.content); }
    );
    // Tracks user presence
    const presenceChannel = realtimeService.subscribeToPresence(
        `document_${documentId}`,
        (state, presence) => { setCollaborators(Object.values(presence).flat()); }
    );
    // ...
}
```

**Use it when:** You're building any collaborative feature — document editing, shared boards, real-time forms, or multiplayer games.

[Try Collaborative Editor Sample →](https://elysiatools.com/en/samples/supabase)

---

## Why Supabase Over Firebase?

Firebase charges based on usage and locks you into Google's ecosystem. Supabase gives you:

- **Real PostgreSQL** — not a simplified document store
- **Row-level security** — fine-grained access control at the database level
- **Open-source SDKs** — no proprietary vendor lock-in
- **Local development** — run the entire stack on your laptop with Docker
- **Transparent pricing** — usage-based but predictable, not "contact sales"

The Supabase samples on ElysiaTools get you from zero to a working backend in under an hour. Each sample is a complete, runnable TypeScript file — not a truncated snippet.

**What Firebase feature are you still paying for that Supabase gives you free?**