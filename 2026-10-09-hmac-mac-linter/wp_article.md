**A single wrong key length, a truncated tag, or a one-time Poly1305 key reuse silently downgrades your entire authentication layer from production-grade to "please don't audit us" — and the linter catches all three before your keys ever leave the dev box.** The hardest part of any MAC deployment is not picking the algorithm. It is keeping the algorithm's preconditions alive through every refactor, every shared-secret rotation, and every "we'll just sign this header too" Friday afternoon. A keyed hash that looked textbook-correct on day one becomes a CVSS 7 by the time the second microservice picks it up.

The [HMAC + BLAKE3 + SHA-3/Keccak + Poly1305 + BLAKE2 Keyed MAC Construction Linter](https://elysiatools.com/en/tools/hmac-blake3-sha3-keccak-keyed-hash-and-mac-construction-linter) covers ten of the constructions you will actually meet in production: HMAC-SHA-256/384/512 (RFC 2104), HMAC-SHA3-256, keyed BLAKE2b-512 and BLAKE2s-256 (RFC 7693), BLAKE3 keyed-hash and derive_key modes, KMAC128 and KMAC256 (NIST SP 800-185), and Poly1305 (RFC 8439). It runs each construction against the canonical RFC and NIST test vectors, then lints for the four classes of misuse that take down real systems.

This field guide walks through the four preconditions the linter enforces, the five constructions where preconditions are easy to violate, and the verification recipe you can hand to a junior engineer on day one.

## Why Keyed MAC Preconditions Outnumber Algorithm Choices

A keyed MAC is the smallest correct primitive in any message-authentication toolkit, but its preconditions are larger than the primitive itself. Pick HMAC-SHA-256 and you have agreed on RFC 2104's ipad/opad construction, a key of at least the underlying hash's block size (64 bytes for SHA-256), and a tag length of at least 128 bits to resist birthday-bound forgery. Pick Poly1305 and you have additionally agreed that the key is **never reused** across messages under the same nonce — a single 64-byte key/nonce pair authenticates exactly one message.

None of those rules appear in the algorithm name. None of them show up when you `import hmac; hmac.new(key, msg, hashlib.sha256).hexdigest()` and watch it produce a 64-character hex string that looks completely fine. The linter's job is to surface the invisible rules that decide whether your MAC output is cryptographically meaningful or just an expensive checksum. Most production MAC incidents traced back to a single missing precondition, not a broken algorithm.

## The Five Precondition Classes The Linter Enforces

Every check the linter runs falls into one of five categories. Skim this list once and you will recognize the failure mode the next time you see it in a code review.

**1. Key length vs construction.** HMAC and the keyed BLAKE2 variants do not technically require a minimum key length — RFC 2104 specifies keys longer than the block size are hashed first — but the security argument weakens below 128 bits of entropy. KMAC explicitly accepts any key length, but its security level is bounded by the smaller of the key and the requested customization string. Poly1305 requires a 32-byte key that must be indistinguishable from uniform random. The linter flags any Poly1305 key derived from a passphrase, a timestamp, or a 16-byte UUID.

**2. Tag length vs security target.** A 64-bit HMAC tag authenticates a packet, not a session. The linter defaults to 256-bit tags for HMAC-SHA-256 and 512-bit for HMAC-SHA-512, and rejects any truncation below 128 bits unless you explicitly opt in with a justification string. The output banner shows the achieved security level next to the algorithm name so reviewers can sanity-check at a glance.

**3. One-time-key misuse on Poly1305 and BLAKE3 keyed-hash.** Poly1305's "one-time" property is the whole point — it is a Wegman-Carter authenticator, and key reuse across messages under the same nonce is catastrophic. BLAKE3's keyed-hash mode is *not* one-time, but its derive_key mode has its own domain-separation requirements. The linter tags any Poly1305 key that appears more than once in the trace and any BLAKE3 key that lacks a context string.

**4. Domain separation on KMAC and cSHAKE.** KMAC128 and KMAC256 take a customization string that is supposed to bind the MAC to a specific protocol. Using the empty string across two protocols (e.g. one for "JWT signing" and one for "webhook signatures") lets an attacker swap signatures between protocols. The linter requires a non-empty customization string of at least 16 bytes, and it rejects the literal strings "default", "empty", and "test".

**5. Self-test vector mismatch.** Every construction has at least one official test vector (RFC 2104 §2, RFC 7693 §2.7, NIST SP 800-185 §6, RFC 8439 §8). The linter recomputes each vector from the documented inputs and compares against the published hex output. A mismatch means your implementation, your key serialization, or your byte order is wrong — none of which the unit test in your repo will catch because they all assume the same implementation.

## How HMAC, BLAKE2, and BLAKE3 Diverge Under The Hood

Three of the constructions in the linter — HMAC, keyed BLAKE2, and keyed BLAKE3 — look superficially similar ("hash with a key") but enforce preconditions differently. HMAC takes any key, hashes it down if it is longer than the block, and produces a tag whose security argument rests on the underlying hash's pseudorandom-function properties. Keyed BLAKE2 embeds the key into the IV, requires the key to fit in one compression block (64 bytes for BLAKE2b), and is faster than HMAC at the same security level — which is why it has eaten HMAC's lunch in storage-layer protocols (Argon2id uses BLAKE2b under the hood).

BLAKE3 is the new entrant. Its keyed mode is a single-key setup with optional derive_key context. Unlike BLAKE2, BLAKE3's default key length is 32 bytes and it has a tree structure that allows verified streaming on huge messages. The linter's BLAKE3 checks are stricter than its BLAKE2 checks: the key must be exactly 32 bytes (no truncation, no extension), and derive_key context must be at least 8 bytes.

If you are picking one of the three today, the honest answer is: use HMAC-SHA-256 if you need RFC interoperability, keyed BLAKE2b if you need speed and the protocol allows it, and BLAKE3 keyed-hash if you control both ends and want the smallest, fastest, most-modern construction. The linter will not pick for you, but it will tell you when your pick violates its own rules.

## Poly1305: One-Time Means One-Time

Poly1305 deserves its own section because its misuse pattern is unique. The construction is a Wegman-Carter authenticator parameterized by a 32-byte key `r` and a 16-byte nonce `s`. The authenticator is computed as `((poly(r, msg) + s) mod 2^128)` truncated to 128 bits. Because `s` is a single 128-bit addition, an attacker who can collect two MACs under the same `(r, s)` pair can recover `poly(r, msg1) - poly(r, msg2)` and from there recover the key `r` itself in polynomial time.

The linter catches three Poly1305-specific failure modes:

<ul><li><strong>Key reuse across messages.</strong> Any Poly1305 key that appears in more than one trace entry raises a hard error. The trace records <code>(key, nonce, msg, tag)</code> and the de-duplication check is on <code>(key, nonce)</code>, not on key alone, because legitimate protocols use the same key with different nonces.</li>
<li><strong>Non-deterministic key derivation.</strong> A Poly1305 key derived from <code>secrets.token_bytes(32)</code> is fine. A key derived from <code>hashlib.sha256(secret + nonce).digest()[:32]</code> is fine <em>only if</em> the nonce is unique. The linter follows the derivation chain and flags any case where the same key can be reconstructed.</li>
<li><strong>Tag truncation below 128 bits.</strong> Poly1305 produces a 16-byte tag; truncating it to 8 bytes is occasionally done for bandwidth, but it cuts the forgery probability from 2^-128 to 2^-64. The linter warns on truncation below 128 bits and rejects below 64 bits.</li></ul>

The "key + nonce unique" rule is the one that breaks the most Poly1305 deployments. The construction is fast and the API is friendly, which makes it easy to slip into a hot path without thinking through the uniqueness invariant. Pair this section with [Web Cryptography Python samples](https://elysiatools.com/en/samples/web-cryptography-python) or [macOS Cryptography Swift samples](https://elysiatools.com/en/samples/macos-cryptography-swift) to see correct Poly1305 wiring in two production languages.

## SHA3-256 vs BLAKE3: Picking A Modern MAC Construction

When the protocol allows you to pick, three modern constructions deserve a closer look: HMAC-SHA3-256 (the SHA-3 variant of HMAC), BLAKE3 keyed-hash, and KMAC128. Each takes a different stance on the customization string, the key-length requirement, and the streaming model. SHA3-256 has the largest installed base of any modern hash and is the conservative pick. BLAKE3 has the smallest, fastest, and most-modern implementation surface — the construction you reach for when both endpoints are under your control. KMAC128 is the SHA-3-native equivalent of BLAKE3's keyed mode and produces 256-bit tags natively with no truncation required.

The linter's job here is not to pick for you but to refuse the pick that violates the construction's own rules. SHA3-256 with a 96-bit key is technically valid but is flagged because the security level is below the tag length. BLAKE3 with a 64-byte key is flagged because the key length is wrong — BLAKE3 wants exactly 32 bytes for its keyed mode. KMAC128 with an empty customization string is flagged because the customization is the whole point. Run the four candidate constructions side-by-side through the linter and you will see the green-or-red matrix in under a second.

## KMAC, cSHAKE, And The Customization String

KMAC is the SHA-3 family's answer to HMAC, and it fixes a structural problem with HMAC: HMAC's security proof relies on the compression-function properties of the underlying hash, and it does not let you bind the MAC to a specific protocol. KMAC128 and KMAC256 take an explicit customization string `S` that is mixed into the Keccak sponge state before absorption. Two protocols that use the same key but different `S` values produce independent MACs, even on the same message.

The linter enforces four KMAC rules:

1. `S` must be non-empty. An empty `S` defeats the purpose of having one.
2. `S` must be at least 16 bytes. A short `S` can collide across protocols that pick names from a small set ("v1", "test", "default").
3. `S` must not equal the literal string "default", "test", or "empty". The linter keeps a deny list of strings that have been used in real protocol-confusion CVEs.
4. The tag length must match the requested security level. KMAC128 produces 256-bit tags; KMAC256 produces 512-bit tags. Truncating to half the native length is allowed with justification; truncating to less than 128 bits is rejected.

cSHAKE is the underlying extension of SHAKE128 and SHAKE256 that lets you add a customization string to a SHAKE call. It is the basis for KMAC, TupleHash, and ParallelHash from SP 800-185. The linter's cSHAKE checks feed the same `S` validation rules into cSHAKE because the failure mode — protocol confusion across empty-or-default `S` values — is identical.

## How To Wire The Linter Into A Pre-Commit Hook

The linter ships with three output modes. The default human-readable mode prints one line per construction with a checkmark or red X. The `--json` mode emits a structured array of `{construction, status, details, security_level}` records suitable for CI ingestion. The `--precommit` mode is a thin wrapper around `--json` that exits non-zero on any failure and prints a one-line summary.

A 30-line pre-commit hook looks like this:

```
#!/usr/bin/env bash
set -e
python3 -m elysia_mac_lint \
  --input .mac-trace.json \
  --json | jq -e '.[] | select(.status == "fail")' > /dev/null \
  || { echo "MAC lint failed — see above"; exit 1; }
```

The trace file is the part that takes discipline to keep honest. Every code path that produces or consumes a MAC must emit a `(algorithm, key_id, key_len, msg_len, tag_len, nonce?, customization?)` record to the trace. The linter reads the trace and runs the same checks against it that it would against a one-shot input. A trace that is missing records for half your code paths is not a passing trace; the linter flags any construction where the trace has gaps.

This is the single highest-leverage habit you can build into a team that is shipping MAC-protected APIs: every MAC emit and every MAC verify produces a trace record, and the trace is linted on every PR. The 30 lines of hook code buy you the same confidence that took the AES-GCM nonce-reuse CVEs of 2019–2021 to teach the rest of the industry.

## What The Linter Will Not Catch

Three classes of failure sit outside the linter's reach and require human judgment:

<ul><li><strong>Side-channel leakage from the implementation.</strong> The linter runs in software and reads the keys and messages from the trace; it cannot tell you that your HMAC implementation does a table-lookup whose timing depends on the key. Differential power analysis and cache-timing attacks are out of scope.</li>
<li><strong>Protocol-level MAC confusion.</strong> The linter will tell you that protocol A and protocol B use different customization strings, but it will not tell you whether your service exposes both protocols on the same endpoint. Cross-protocol confusion is a design issue, not a primitive issue.</li>
<li><strong>Key custody.</strong> The linter treats every key as a 32-byte opaque blob. It does not enforce that the key came from an HSM, that it rotates on schedule, or that it is destroyed after use. A passing MAC lint with keys stored in plaintext is still a failing security posture.</li></ul>

Keep these three classes in code review, and let the linter handle the primitive-level correctness. The split is clean: the linter enforces the cryptographic contract, and the human reviewer enforces the operational one.

For working examples of HMAC, BLAKE2, and BLAKE3 wiring in real codebases, the [Web Cryptography Python samples](https://elysiatools.com/en/samples/web-cryptography-python) and [macOS Cryptography Swift samples](https://elysiatools.com/en/samples/macos-cryptography-swift) both include MAC construction snippets that pair with the linter's expected input format. Run a sample through the linter, confirm the green checkmarks, then use the same input shape in your own trace.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
