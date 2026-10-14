PKCE Code Verifier & Challenge Generator Field Guide: When Three Modes and Four Entropy Tiers Decide Whether the OAuth Handshake Survives a Network Sniffer

<strong>PKCE is the line between a secure public-client OAuth handshake and one that leaks the authorization code to the next person on the Wi-Fi.</strong> Mobile apps, SPAs, and CLIs do not have a client secret, so they prove intent with a one-shot verifier-plus-challenge pair. Get the math wrong and the authorization code is the only credential an attacker needs; get it right and the worst case is a stolen code that still cannot be redeemed. The [Elysia Tools PKCE Code Verifier & Challenge Generator](https://elysiatools.com/en/tools/pkce-code-verifier-generator) folds the three RFC 7636 jobs into one box: generate fresh pairs from 256/384/512/768-bit entropy, audit a verifier you already have against length, charset, and entropy rules, and verify a verifier/challenge pair by recomputing BASE64URL(SHA256(verifier)).

## What PKCE actually defends against

PKCE was finalized in [RFC 7636](https://elysiatools.com/en/samples/oauth-openid-connect) to fix a 2015 problem: the authorization code interception attack. A native app running on Android or iOS opens a custom URL scheme to receive the auth code, but if another app has registered the same scheme, the code lands in the attacker's process. Without PKCE the attacker redeems the code immediately. With PKCE they also need the verifier, which was generated inside the legitimate client and never left its memory.

The defense only works if the verifier is unguessable and the challenge cannot be reversed. RFC 7636 nails the two together: generate between 43 and 128 characters of `[A-Za-z0-9-._~]`, hash it with SHA-256, and send the BASE64URL-encoded digest as the challenge. The authorization server stores the hash, not the plaintext. When the client redeems the code, it sends the original verifier; the server re-hashes and compares. An attacker holding only the intercepted code cannot derive the verifier from the challenge because SHA-256 is a one-way function.

## Three modes you actually use

The PKCE generator collapses the workflow into three modes you toggle in the same input box.

- <strong>Generate mode</strong> emits a fresh `code_verifier` and the matching `code_challenge_method = 'S256'` `code_challenge`. You drop the verifier into your client config and the challenge into the `code_challenge` query parameter of the authorization request.
- <strong>Audit mode</strong> validates a verifier you already have. It checks the length window (43 to 128 chars), the character class (`[A-Za-z0-9-._~]`), and the entropy budget (≥ 256 bits). A common defect this catches is the "I padded my UUID verifier with zeros" mistake: a UUID with dashes is only 122 bits of entropy, well under the RFC floor.
- <strong>Verify mode</strong> accepts a verifier and a challenge and recomputes BASE64URL(SHA256(verifier)) to confirm they match. This is the offline equivalent of what the server does on token exchange; running it before shipping catches drift between a stored verifier and the challenge the front-end is sending.

## Why entropy matters more than length

The RFC says 43 to 128 characters, but that floor is misleading. A 43-character verifier drawn from 64 symbols gives 43 × 6 = 258 bits; a 43-character verifier drawn from a 10-symbol alphabet gives 43 × ~3.3 = 142 bits, under the floor. The PKCE generator's entropy selector does the math for you and labels each tier with its bit budget.

- <strong>256-bit entropy</strong> is the RFC minimum. Passes every compliance audit. Generated from 32 random bytes.
- <strong>384-bit entropy</strong> is a common choice for high-value SPA tokens. Generated from 48 random bytes.
- <strong>512-bit entropy</strong> matches the SHA-512 block size and leaves no room for future brute-force surprises. Generated from 64 random bytes.
- <strong>768-bit entropy</strong> is the practical ceiling for PKCE. Generated from 96 random bytes; emitted as a 128-character string exactly hitting the RFC length ceiling.

The trap is using entropy as a vanity metric. A 512-bit verifier still fails RFC 7636 if your generator emits `[A-Z0-9]` instead of `[A-Za-z0-9-._~]`. The audit mode catches both classes of failure in one pass.

## What a malformed verifier audit looks like

Running audit mode against a hand-rolled verifier exposes the gaps that the eye misses. The audit returns a per-rule report: length pass/fail, charset pass/fail, and entropy pass/fail, with the recomputed bit count. A 64-character hex (`[0-9a-f]`) verifier reports entropy as 256 bits because the alphabet is 16 symbols, which the eye treats as "long enough" but the audit flags as RFC-compliant on length and charset but undersized on alphabet diversity.

A separate failure mode is the padded verifier. Java's `UUID.randomUUID().toString()` is 36 characters and uses 16 hex symbols plus 4 dashes. Padded to 43 with `=` signs it passes length and charset but the entropy is only 122 bits, far below the 256-bit floor. The audit flag surfaces as "entropy FAIL (122 < 256 bits)". Replacing the source with `SecureRandom` and emitting BASE64URL[5] from 32 bytes is the canonical fix.

## How the verifier-to-challenge transform lands

The math is short. Take a 43-character string from `[A-Za-z0-9-._~]`, decode it as bytes, hash with SHA-256, then BASE64URL-encode the digest. The output is a 43-character challenge (no padding, URL-safe alphabet). In pseudo-shell, the workflow is:

- <strong>Input:</strong> 43-char verifier like `dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk`
- <strong>SHA-256 hex:</strong> `293e6cc24fcf2a96ea9d2e3a8c40f5d2a4f5a3a8e6f9b1c4d6e7f8a9b0c1d2e3f` (truncated for display)
- <strong>BASE64URL:</strong> `LS6mY9P1x9B_KoSq5LM3vx_r_q8FSxhOJf4_GCNFRBg`
- <strong>Authorization request:</strong> `https://auth.example.com/authorize?response_type=code&client_id=...&code_challenge=LS6mY9P1x9B_KoSq5LM3vx_r_q8FSxhOJf4_GCNFRBg&code_challenge_method=S256&state=...&redirect_uri=...`

The server stores `code_challenge` on the authorization request and re-hashes the verifier at token exchange. If they match the token lands; if they do not, the server returns `invalid_grant` and the attack is foiled.

## Building the authorization request URL

The PKCE generator also assembles the full authorization URL so the only thing you have to type by hand is the redirect URI. You give it client ID, scope, state, and the freshly generated challenge; it returns a URL you can paste into a WebView or `openURL()` call. A typical built URL looks like:

- <strong>Scheme:</strong> `https://auth.example.com/authorize`
- <strong>Parameters:</strong> `response_type=code`, `client_id=<your-client>`, `redirect_uri=<your-scheme>`, `scope=openid profile`, `state=<csrf-token>`, `code_challenge=<43-char-base64url>`, `code_challenge_method=S256`

Stitching these by hand is how state tokens leak and `code_challenge_method` typos propagate into production. Letting the generator own the assembly keeps the parameter names in one place and emits percent-encoded output that survives copy-paste.

## Why the verify mode catches integration drift

The audit and verify modes are not just developer paranoia; they catch the drift that happens when a front-end and a back-end share state through a database or a cache. The drift pattern: a verifier is generated on day one, stored in a session table; a year later a mobile client picks up the row and tries to redeem the code; the server rejects because the stored verifier was truncated or rehashed. Running verify mode against the stored pair before redeploying surfaces the mismatch in seconds, not at 3 a.m. when the integration tests are red.

The verifier-mode second use is debugging authorization servers you do not control. If you have a hand-written verifier from a closed-source client and you want to know what challenge the server expects, generate mode plus verify mode is enough: paste the verifier into verify mode, ask it to compute the challenge, compare against the URL the closed-source client is sending. If they differ, the integration has a state-desync bug.

## What to check before you ship

PKCE is one of the few security primitives where the verifier can fail in three orthogonal ways and still produce a "valid-looking" handshake. Pre-flight the verifier with the [Elysia Tools PKCE Code Verifier & Challenge Generator](https://elysiatools.com/en/tools/pkce-code-verifier-generator) audit mode before shipping: 43 to 128 chars, `[A-Za-z0-9-._~]` charset only, ≥ 256 bits of entropy. Run verify mode against the verifier and challenge stored in your session table to catch drift. Then run the full flow once with a real authorization server in a non-prod tenant and watch the `code_challenge` parameter land exactly as you sent it.

The defense stops working the moment any of those three checks is skipped. A 41-character verifier will pass visual inspection and trip the authorization server at token exchange. A `[A-Z0-9]` verifier will pass your local length test and trip the server's charset check. A 200-bit verifier will pass your CI lint and trip a hardened penetration test. The generator's audit mode catches all three at once; the verify mode proves the integration is wired correctly; the generate mode keeps the bytes uniform across platforms.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).