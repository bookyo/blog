<strong>Three modes, one verifier, one rule that catches every mistake the spec already lets through.</strong> RFC 7636 says your `code_verifier` is unreserved ASCII between 43 and 128 chars, derived from at least 256 bits of entropy. Most SPA authorization flows ship a verifier that satisfies all three and still fails the round-trip because the front end computes `code_challenge` from a string the back end never re-hashes. The [PKCE Code Verifier & Challenge Generator](https://elysiatools.com/en/tools/pkce-code-verifier-generator) bundles generate, audit, and verify into one page that puts the verifier, the challenge, and the recomputed check next to each other so you can read the round-trip while you copy the URL.

## Why PKCE Exists at All

The OAuth 2.0 Authorization Code flow was designed for confidential clients, a back-end server that holds the client secret and never lets the browser see it. Single-page apps changed that. The same JavaScript that asks for the authorization code also receives it in the URL fragment, and a network attacker who intercepts that fragment in a public Wi-Fi redirect chain has the only credential it needs to swap the code for a token. PKCE (Proof Key for Code Exchange, RFC 7636) introduces a per-request random string the client generates locally and a one-way hash the authorization server stores against the code. When the client swaps the code for the token, it has to present the original string; the server hashes it and compares. The hash is what the network sees during the redirect; the original string is what the attacker would need to redeem the code, and the attacker never has it.

## What the RFC Actually Mandates

The spec is short but specific. `code_verifier` is a high-entropy cryptographically random string using the unreserved character set `[A-Z] / [a-z] / [0-9] / - / . / _ / ~`, length 43 to 128 characters. The minimum entropy is 256 bits, which translates to 32 raw bytes before base64url encoding (43 chars after encoding, with no padding). `code_challenge` is `BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))`. The `code_challenge_method` is `S256`. (The spec allows the legacy `plain` method, where the challenge equals the verifier; every modern server should refuse it and every modern client should refuse to send it.)

If any of those three rules breaks, the token endpoint returns `invalid_grant`, the user sees a generic "Something went wrong" toast, and you spend the next hour wondering whether the SHA-256 implementation, the base64url padding, or the verifier itself is wrong.

## The Three Modes Side by Side

**Generate** builds a fresh pair. Pick 256, 384, 512, or 768 bits of entropy; the tool draws bytes from `crypto.getRandomValues`, base64url-encodes them, and shows the verifier and the S256 challenge side by side. The output also includes a complete authorization-request URL with `code_challenge` and `code_challenge_method` pre-filled, ready to drop into a `window.location.assign()` call.

**Validate** audits an existing verifier. Paste a candidate from a log line, a colleague's commit, or a server-side generator, and the tool checks length, charset, and entropy estimate (Shannon entropy over the byte distribution, which is what most off-the-shelf audit libraries actually compute). If the verifier passes, it also shows the challenge that verifier would produce, so you can confirm the front-end and the back-end agree on the source string.

**Verify** closes the loop. Paste the verifier and the challenge you want to check it against, and the tool recomputes `BASE64URL(SHA256(verifier))` and string-compares it to the challenge. This is the round-trip you run when a token exchange is failing and you cannot tell whether the front end computed the challenge before the redirect or after, whether a CDN rewrote the URL fragment, or whether the verifier got truncated by a query-string parser that stopped at the first `&`.

## The Pitfalls the Spec Lets Through

The RFC compliance check is necessary but not sufficient. Three classes of failure pass `validate` and break `verify`.

**Padding characters.** JavaScript's `btoa()` inserts `=` padding that base64url forbids. Some libraries strip it, some leave it, and a verifier with `=` at the end silently fails the SHA-256 step because the SHA-256 is over the raw bytes, not the printable string. The audit panel flags `=` anywhere in the string as a warning, even though the spec only forbids it inside the verifier itself.

**Method mismatch.** The front end sends `S256`; the back end, behind a feature flag or a proxy rewrite, sends `plain`. The token endpoint receives a hash it expects to match the raw string, hashes it again, and rejects the result. The verify panel surfaces both `S256(challenge)` and `plain(challenge)` so you can see at a glance which one matches.

**Verifier drift across the redirect.** The browser's URL parser may percent-decode, fragment-strip, or re-encode the verifier between the moment it lands in `window.location.hash` and the moment the SPA reads it. The audit panel shows the byte length and the SHA-256 hash of the parsed string alongside the verifier you expected, and any mismatch is a one-line debugging breadcrumb.

## Where PKCE Fits in the OAuth Stack

PKCE is not a replacement for client authentication, and it is not a substitute for state validation. It is the layer that protects the authorization code itself in flows where the client cannot keep a secret. The companion [OAuth 2.0 samples](https://elysiatools.com/en/samples/oauth2-samples) collection shows full request and response bodies for the authorization-code, client-credentials, and device-code flows, including the PKCE pair on the request line and the `code_verifier` on the token-exchange body. For OpenID Connect flows layered on top of OAuth 2.0, the [OAuth 2.0 & OpenID Connect samples](https://elysiatools.com/en/samples/oauth-openid-connect) show the same PKCE pair plus the `id_token` validation steps that come after the token lands.

If you are working at a lower level, the [cryptography samples](https://elysiatools.com/en/samples/cryptography) cover the underlying primitives: SHA-256 over arbitrary input, base64url encoding with and without padding, and entropy estimates across different byte distributions. Together with the verifier generator they give you a reproducible reference for every byte in the round-trip.

## Wiring It into a SPA Authorization Request

The standard pattern is to call `crypto.getRandomValues(new Uint8Array(64))`, base64url-encode the result, store the verifier in `sessionStorage` under a request-scoped key, and immediately build the challenge with `crypto.subtle.digest('SHA-256', bytes)`. The verifier stays in the SPA; the challenge goes to the authorization server. When the redirect lands back at the callback page, the SPA reads the verifier from session storage, finds it, and posts it to the token endpoint.

The generator's output mode 1 (generate) shows every step of that pipeline: the random bytes (hex), the base64url verifier, the SHA-256 hash (hex and base64url), and the full authorization-request URL. If your SPA framework does the digest in a Web Worker or in a service worker, you can copy the bytes and the hash and confirm the worker is producing the same string the page-level code would produce.

## When to Audit a Verifier You Did Not Generate

Audit mode is the most common day-two use. A verifier appears in a log line from a customer support escalation, in a server-side token-exchange retry loop, or in a CI artifact from a build that hit the authorization endpoint through a proxy. Without an audit step, the only way to know whether the verifier is RFC-compliant is to read the spec and check by hand. With audit mode, you paste the candidate, see length, charset, and entropy estimate, and either confirm it or replace it with a freshly generated one. The verify step then confirms the challenge it implies matches the one stored against the code.

## Closing the Round-Trip

The verify panel is where most debugging time gets saved. Paste the verifier from session storage and the challenge from the failed token-exchange log, and the tool computes `BASE64URL(SHA256(verifier))` and compares it to the challenge. If they match, the issue is upstream (redirect parsing, query-string encoding, request-body construction). If they do not match, the issue is local (the SPA regenerated the verifier between authorization and token exchange, or a second tab overwrote session storage). Either way, the answer is one paste and one click away.

For a deeper look at the broader OAuth 2.0 and OpenID Connect ecosystem, including token lifetimes, refresh-token rotation, and PKCE interaction with PAR (Pushed Authorization Requests), the [OAuth 2.0 samples](https://elysiatools.com/en/samples/oauth2-samples) and [OpenID Connect samples](https://elysiatools.com/en/samples/oauth-openid-connect) collections walk through the full request and response for each grant type, with the PKCE pair on every authorization-code request.

The generator is built for the day-two case: the audit, the round-trip, and the verifier you did not write yourself. Try it at [Elysia Tools](https://elysiatools.com/en/tools/pkce-code-verifier-generator), or browse more security and authentication tooling at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).
