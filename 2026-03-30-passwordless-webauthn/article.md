# Passwordless Is Here: 4 WebAuthn Implementations That Actually Work

81% of hacking-related breaches involve weak or stolen passwords (Verizon DBIR). We've heard "passwords are dying" for a decade. This time it's different — and WebAuthn is why.

The Web Authentication API (WebAuthn) is now supported in every major browser and OS. No polyfills. No vendor lock-in. Passkeys — the consumer-friendly implementation of WebAuthn — are already replacing passwords at Google, Apple, Microsoft, and hundreds of other services. If you're not building with WebAuthn, you're behind.

Here are 4 production-ready WebAuthn implementations on ElysiaTools that you can copy, paste, and ship today.

---

## 1. WebAuthn Hello World — Your First Passwordless Login

Start here. This is the minimal viable WebAuthn implementation — registration and authentication in ~150 lines of JavaScript.

**What it does:**
- Generates a cryptographic key pair (private key stays on device, public key goes to server)
- Supports platform authenticators (Touch ID, Windows Hello, Android biometrics) and cross-platform keys (security keys via USB/NFC/BLE)
- Handles the base64url encoding dance between browser and server

**Use it when:** You want to understand the core flow before adding complexity. This is the WebAuthn equivalent of "Hello World" — no room management, no backup codes, no enterprise features. Just the bare minimum to register a credential and authenticate.

**The key insight most tutorials get wrong:** WebAuthn has two distinct phases — `navigator.credentials.create()` (registration) and `navigator.credentials.get()` (authentication). Each requires a fresh challenge from your server. Reusing challenges is a security vulnerability.

```javascript
// Register: create a credential
const credential = await navigator.credentials.create({
  publicKey: {
    challenge: base64URLToArrayBuffer(serverChallenge),
    rp: { name: "Your App", id: window.location.hostname },
    user: { id: base64URLToArrayBuffer(btoa(userId)), name: username, displayName },
    pubKeyCredParams: [
      { alg: -7, type: "public-key" },   // ES256
      { alg: -257, type: "public-key" }  // RS256
    ],
    authenticatorSelection: { userVerification: "required" },
    timeout: 60000
  }
})
```

**Try it:** https://elysiatools.com/en/samples/webauthn-samples

---

## 2. Passkeys Manager — Multi-Device, Backup-Ready

The Hello World example has one device. Real users have three. The Passkeys Manager adds everything production needs: multiple credentials per user, IndexedDB storage, credential backup eligibility detection, and cross-device sync semantics.

**What it does:**
- Stores credentials in IndexedDB with a clean API
- Detects whether each authenticator is "backup eligible" (can be synced via iCloud Keychain, Google Password Manager, etc.)
- Supports both platform-attached (built-in biometric) and cross-platform (security key) authenticators
- Exports credentials as JSON for user-controlled backups

**Use it when:** You're building a consumer app where users need to log in from their phone, laptop, and their partner's tablet. The backup eligibility flag tells you whether to prompt users to add a second authenticator as backup.

**The feature that surprised me:** The `largeBlob` extension. WebAuthn can store up to ~256KB of data alongside the credential. This is how password managers sync the "password" part of a passkey. Most implementations skip it, but if you're building a hybrid system (passkey for MFA + traditional password for account recovery), this is your bridge.

```typescript
// Check what's available before prompting registration
const compatibility = PasskeysManager.checkCompatibility()
// { supported: true, platformAuthenticator: true, largeBlob: true }
```

**Try it:** https://elysiatools.com/en/samples/webauthn-samples

---

## 3. WebAuthn MFA Integration — Enterprise-Grade Auth

This is the full system. TOTP backup codes, device fingerprinting for risk-based step-up, session management, and a security event log. If you're building anything that needs to meet SOC2 or similar compliance, start here.

**What it does:**
- Layered MFA: passkey (something you have) + optional TOTP or backup code (something you know)
- Risk scoring: flags logins from new devices or suspicious IPs
- Session tokens with configurable timeout and trusted deviceremembering
- Generates 10 one-time backup codes, each valid for a year
- Security event log: every login, passkey addition, and suspicious activity, timestamped and attributed

**Use it when:** You need to issue compliance reports. Or when a single passkey isn't enough — think banking apps, admin panels, or any system where account recovery needs a human process.

**The underrated part:** The security report generator. It calculates a user security score (0-100) based on number of passkeys, MFA methods enabled, and recent failed login attempts. You can use this to prompt users ("Your security score is 40 — add a backup passkey to reach 80") or to detect compromised accounts.

**Try it:** https://elysiatools.com/en/samples/webauthn-samples

---

## 4. WebSocket Chat — When Passwordless Meets Real-Time

Authentication doesn't happen in isolation. This WebSocket implementation integrates JWT-based WebAuthn authentication into a full real-time chat system with Socket.IO, room management, and private messaging.

**What it does:**
- WebAuthn registration/login via REST API, JWT issuance via Socket.IO handshake
- Room creation with optional passwords
- Private messaging with typing indicators
- Presence tracking (who's online, who went offline)
- File sharing via presigned URLs

**Use it when:** You're building anything with real-time features. The authentication pattern here — REST for registration/auth, WebSocket for everything else, with JWT passed during socket handshake — is the standard production approach for hybrid apps.

**The auth pattern worth stealing:** The Socket.IO middleware that verifies the JWT before allowing the socket connection. This means you can't even open a WebSocket connection without a valid session — much cleaner than handling auth failures inside message handlers.

```javascript
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token
  try {
    const decoded = jwt.verify(token, JWT_SECRET)
    socket.userId = decoded.userId
    next()
  } catch {
    next(new Error('Invalid token'))
  }
})
```

**Try it:** https://elysiatools.com/en/samples/websocket-samples

---

## Where to Start

Here's my recommendation, depending on where you are:

- **First WebAuthn integration:** Start with Hello World. Understand the create/get flow before touching anything else.
- **Consumer app, < 1M users:** Start with Passkeys Manager. Add backup codes and device management before launch, not after.
- **Enterprise or regulated industry:** Start with MFA Integration. Compliance auditors want audit logs, session timeouts, and risk scoring — all here.
- **Real-time app:** Grab the WebSocket auth pattern regardless of whether you're doing passwordless. The JWT handshake approach works with any auth system.

The tooling is mature. The browser support is universal. The only thing holding most teams back is unfamiliarity — and that's a solvable problem.

---

## The Problem No One Has Solved Yet

WebAuthn solves the "user picks a weak password" problem. It doesn't solve the "user loses all their authenticators and gets locked out" problem.

Backup codes work, but they're static — if someone steals them, they work once and then you're alerted. TOTP requires a separate app. SMS fallback is a known security weakness.

The unsolved challenge: **adaptive, risk-aware account recovery that doesn't weaken the authentication model**. When a user genuinely loses all their second factors, how do you restore access without creating a phishing-prone backdoor? Self-sovereign identity protocols like Decentralized Identifiers (DIDs) are promising, but the UX is still years away from mainstream.

Until then, have a support process and document it before you need it.

---

**Tools used in this post:** [WebAuthn Passwordless Authentication](https://elysiatools.com/en/samples/webauthn-samples) · [WebSocket Real-time Communication](https://elysiatools.com/en/samples/websocket-samples) · [Playwright E2E Testing](https://elysiatools.com/en/samples/playwright-testing-samples) · [OpenTelemetry Observability](https://elysiatools.com/en/samples/opentelemetry-samples)
