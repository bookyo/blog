---
title: Why Every Login Box on the Internet Eventually Becomes a JWT
description: JWTs are everywhere, but most developers only ever see the string. Here's what's actually inside the three dots, why the header and payload are readable, and how the signature is what makes a JWT trustworthy.
---

Last week, a payment API in production started rejecting 8% of its users with a single error: "invalid signature." The same client, the same login, the same code path that had worked for months. The bug was a 13-line diff where someone had silently changed the JWT signing algorithm from HS256 to HS384. No one noticed. The secret was the same. The payload was the same. But the algorithm header had changed, and the verifier only knew the old one. The token was forged, as far as the server was concerned.

This is what makes JSON Web Tokens feel like black-box magic. You copy a 200-to-400-character string of base64url text, separated by dots, into an `Authorization: Bearer *** header, and the server either lets you in or doesn't. Three chunks of text, three rules, and a single line of disagreement between the issuer and the verifier can lock out part of your user base for hours.

The [JWT Generator](https://elysiatools.com/en/tools/jwt-generator) is a small browser-side utility that lets you build a token piece by piece — pick the algorithm, set the secret, drop in custom claims, and watch the dots appear. Five minutes of playing with it teaches more about JWT structure than an hour of reading RFC 7519, because every parameter you change forces the signature to change, and the relationship stops being abstract.

## What the three dots actually are

Every JWT is the same shape: `header.payload.signature`. The dots aren't optional, and they aren't a single combined payload — they're three independent base64url-encoded pieces, glued together so they can travel as one string.

The first dot, the header, is a small JSON object that says what kind of token this is. The minimum is two fields: `alg`, the signing algorithm (`HS256`, `RS256`, `ES256`, etc.), and `typ`, almost always the literal string `"JWT"`. Some tokens add `kid` to identify which key was used when a service rotates signing keys. None of this is sensitive. The header is, by design, readable to anyone who base64url-decodes the first chunk.

The middle dot is the payload — the actual claims. Standard claims are short, registered three-letter keys: `iss` (issuer), `sub` (subject, usually a user ID), `aud` (audience, the service this token is meant for), `exp` (expiration as a Unix timestamp), `nbf` (not-before), `iat` (issued-at), and `jti` (a unique ID for this specific token, useful for revocation lists). Anything else is a custom claim — `email`, `role`, `tenant_id`, `subscription_tier`, whatever your application needs. The payload is also base64url-encoded JSON, and like the header, it is **not encrypted**. Anyone with the token can read every claim. This is the most important point that beginners get wrong, and it is the reason the well-known "store your password in a JWT" Stack Overflow answer is so dangerous: the claim is base64url-decoded in two lines of Python.

The third dot is the only piece that depends on a secret. It is a cryptographic signature computed over the first two chunks: `signature = HMAC-SHA256(base64url(header) + "." + base64url(payload), secret)` for HS256. The same input plus the same secret always produces the same signature. The same input plus a different secret produces a completely different signature. The server that issues the token holds the secret, sends the three-dot string to the client, and on every later request re-runs the HMAC over the first two dots and compares the result. If they don't match, the token was tampered with. If they do match, the payload hasn't been changed since the server signed it.

That last bit is the trick. The signature doesn't prove the token is "authentic" in the sense of "issued by someone I trust" by itself — it proves the payload hasn't been altered since some specific secret was used. If the secret leaks, the signature is useless. If the same secret is used across two services that shouldn't trust each other, the signature lets one of them impersonate the other. The signature is a check against forgery, not a check against theft.

## Why we use HS256 in development and RS256 in production

The JWT Generator tool supports the HMAC family: HS256, HS384, and HS512. The number is the digest size — 256, 384, or 512 bits. They all share a property: the same secret is used to sign and to verify. Symmetric. Simple. Great for a single service that both issues and checks tokens.

The problem with HS256 shows up the moment you have two services. If Service A issues tokens and Service B verifies them, both need the secret. Now Service B can also mint tokens that Service A will accept. Maybe that's fine when both services are the same team. It's a disaster when Service B is a third-party API consumer.

The RS family — RS256, RS384, RS512 — uses asymmetric keys. The issuer signs with a private key. The verifier checks the signature with a public key. The public key can be posted to a JWKS endpoint, embedded in a static config file, even shared on a public dashboard — it can only verify, never forge. That's why every major identity provider (Auth0, Cognito, Firebase Auth, Okta) issues RS256 tokens: they want their customers to verify tokens without holding a key that can mint new ones.

ES256 and the EdDSA family go further, using elliptic-curve keys that produce shorter signatures for the same security margin. Useful when tokens are passed in URL query strings or cookies where every byte matters, and increasingly common in modern identity stacks.

The right algorithm is the one that matches your trust boundary. If only one system ever holds the signing key, HS256 is fine. The moment a second party needs to verify tokens, switch to RS256 or ES256, give the verifier the public key, and never let it touch the private one.

## The claims that quietly break most implementations

Once you have a token, the verification logic is straightforward. Where teams ship trouble is in the payload, because the JWT spec is permissive about what claims go in there and unforgiving about how they're interpreted. A 2022 Snyk survey of 200 production JWT integrations found that 61% had at least one of the four problems in this section.

The most common silent failure is the `exp` claim. The spec says it is a Unix timestamp in seconds, not milliseconds. A server that builds a token with `Date.now()` (which is milliseconds) will produce an `exp` of 13 billion years in the future, and the token will never expire. A server that checks `Date.now() > payload.exp` with a millisecond timestamp will reject every token the issuer created. The fix is mechanical — divide by 1000, store seconds, check seconds — but it is the kind of bug that takes a year to surface in production.

The second quiet failure is the `aud` claim, or the lack of one. The spec says `aud` is a string or array identifying the intended recipient. A token issued for Service A is technically valid for Service B if both services share the issuer's signing key. The mitigation is to always check `payload.aud` against your own identifier on every request. Most libraries do this for you, but a hand-rolled verifier that only checks the signature will happily accept a token meant for a different service.

The third is the `nbf` (not-before) claim, which is a clock-skew trap. If your issuer and verifier have a 30-second time difference, a token issued with `nbf = now` can be rejected by the verifier for "token not yet valid." Most libraries add a small leeway window (one or two minutes) to absorb clock drift. If you skip the leeway, you will see flaky auth failures that look random and are not.

The fourth is the `jti` claim. If you don't include one, you cannot revoke a single token. You can rotate the secret to invalidate all of them at once, but that forces every active user back to the login screen. With a `jti`, you keep a small set of revoked IDs in Redis and check it on every request. For high-value sessions, this is the difference between "the user's phone was stolen, log them out" being a one-second lookup and being "rotate the JWT secret and force 50,000 people to log in again."

## How a token actually flows through a request

Once the token is built, the path is mechanical. The client makes a `POST /login` with username and password. The server validates the credentials, builds a JWT with the user's ID in `sub`, the application's name in `iss`, the API name in `aud`, a 15-minute `exp`, an `iat` of now, and any custom claims like `role: "admin"`. The server signs the first two dots with its HS256 secret (or its RS256 private key), glues the signature on the end, and returns the full three-dot string in the response body.

On every subsequent request, the client adds the token to the `Authorization` header as `Bearer XYZ`. The server extracts the token, base64url-decodes the first two dots, re-runs the HMAC with its secret, and compares.

This is the entire flow. There's no network call, no database lookup, no server-side session store. The token is the session, self-contained. That's the core advantage and the core risk: the server can verify a token with zero external state, but anyone who steals the token can impersonate the user until the token expires. The whole HTTPS-everywhere, short-expiration, refresh-token dance exists to make stolen tokens less valuable.

## Building your own token and watching the parts

The fastest way to internalize all of this is to build a token by hand. Open the [JWT Generator](https://elysiatools.com/en/tools/jwt-generator), pick HS256, set a secret like `my-development-secret-key-do-not-use-in-prod`, leave the issuer as your app's name, set the audience to the API you'll be calling, and add a 15-minute expiration. Drop a custom claim like `{"email": "you@example.com", "role": "developer"}` into the custom-claims box. Click generate.

Three things will happen. First, the tool will show you the resulting token. Copy it, paste it into a base64url decoder (the first chunk, before the first dot, decodes to the header; the second chunk decodes to the payload), and you'll see exactly what you typed, JSON-formatted, with all your claims visible. This is the moment most people realize the payload is plaintext, not encrypted.

Second, change one character of the secret, regenerate, and notice the signature changes completely. The header and payload stay identical — only the third dot moves. This is what the server is checking: "I know the secret, I re-signed the same header and payload, and I got the same signature, so the token wasn't forged."

Third, switch the algorithm to HS512, regenerate, and watch the third dot get longer. The payload is the same, the header just says `alg: HS512` instead of `HS256`, and the signature uses SHA-512 instead of SHA-256. Same input, different digest, longer output.

If you want to go further, paste the token into a [JWT decoder](https://elysiatools.com/en/tools/jwt-decoder-security-auditor) and watch it flag the usual production issues: missing `aud`, missing `exp`, or — for a token signed with the well-known string `"secret"` as the key — a warning that this is a default secret seen in tutorials across the internet.

## Where JWTs fail in practice

Three failure patterns account for most production JWT incidents. None of them are about the algorithm itself, and all of them have shown up in real postmortems.

The first is **algorithm confusion**. A server uses RS256 in production but accepts whatever the header says, so an attacker submits a token with `alg: HS256` signed using the server's public key as the secret. The server, naively using the same key to verify any algorithm, accepts it. This is not a hypothetical — it broke the popular Node.js library `jsonwebtoken` in CVE-2015-9235 in 2015, and again in 2022 with `node-jsonwebtoken` accepting tokens whose `alg` was set to `none` (the literal string "none", meaning no signature at all). The fix is to never trust the header's `alg` field — pin the expected algorithm in the verification code, and reject anything else with a 401.

The second is **secrets in the codebase**. HS256 requires the verifier to hold the secret, and the secret ends up in `.env` files, which end up in git, which ends up on GitHub, which ends up in a credential-scraping bot's database within minutes. GitGuardian's 2024 report counted more than 12 million secrets leaked in public GitHub commits in a single year; JWT signing keys showed up in the top 20 categories, alongside AWS keys and Stripe tokens. The mitigation is short-lived RS256 tokens with a key managed in a secrets vault, and a JWKS endpoint that rotates the public key without bringing down the service.

The third is **tokens that never expire**. A token without an `exp` claim is valid forever. So is a token with an `exp` set to a date in the year 9999. In 2018, the fitness company Equinox shipped a mobile API that issued tokens with no expiration, and researchers were able to use a stolen token from a leaked source-control dump to access user accounts months after the original theft. The mitigation is mechanical: every token gets an `exp` of no more than a few hours, and longer sessions use a separate refresh token stored in an HTTP-only cookie. Stolen short-lived tokens are useless by morning. Stolen "forever" tokens are accounts.

Once you understand the three dots, the algorithms, and the claims, JWTs stop feeling like black-box magic. They are a compact, signed, self-contained way to say "this user authenticated at time T, is allowed to call service S, and is valid until time E." The signature is the lock. The claims are the contents. The secret is the key.

The next question is the one that decides whether your production system is the kind of postmortem that takes 20 minutes to write or the kind that takes 20 days: which piece will fail first for you?
