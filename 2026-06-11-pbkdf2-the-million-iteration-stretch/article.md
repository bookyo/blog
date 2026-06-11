---
title: Why Every Password Hash Runs Itself a Million Times Before It Ever Stores You
---

In the end, the password you typed in is not what gets stored. What gets stored is the version of your password that survived a hundred thousand SHA-256 rounds, then a hundred thousand more, then a hundred thousand more. The string you remember is gone the instant you click submit. What lives in the database is something only the slowest possible computer in the world can produce. That slowness is the point. It is the only thing standing between your account and a ten-gigabyte crack file.

---

A login form does not compare your password to a stored password. The thing the database holds is a *derived key* — a fixed-length string that is mathematically unrelated to your actual password but is statistically unique to it. To check whether you typed the right password, the server re-runs the same derivation against what you submitted, and compares the two derived keys. If they match, the original password was almost certainly the same in both cases.

The function that does that derivation is **PBKDF2**, the Password-Based Key Derivation Function 2. It is the oldest of the modern password hashers and the most widely deployed. Every iPhone, every Mac running Common Crypto, every Java backend that uses `PBKDF2WithHmacSHA256`, every browser's WebCrypto API, every Node.js process, and every WPA2 Wi-Fi handshake uses it. It is so unremarkable that most engineers never think about it. But the design of PBKDF2 contains a single, deliberate trick that makes brute-force attacks a thousand times more expensive, and that trick is the *iteration count*.

## The single trick that changes everything

The naive approach to password storage is to hash the password once and store the result. The problem is that a modern GPU can compute billions of SHA-256 hashes per second. A 12-character password with letters, numbers, and symbols is astronomically large as a search space, but if the attacker has the hash, they do not have to test every password against your login form. They can test billions of candidates per second against the hash itself. The math stops working in their favor only if the hash is slow.

PBKDF2 is just a hash that has been told to be slow. The algorithm takes your password, prepends a random value called the *salt*, runs the result through HMAC-SHA-256, takes that output, prepends the salt again, runs it through HMAC-SHA-256 again, and repeats the process *N* times. With a typical web-app default of 600,000 iterations, the operation is roughly 600,000 times slower than a single hash. To a user, that is 250 milliseconds — an imperceptible delay. To an attacker trying 10 billion candidates, that is 250 milliseconds times 10 billion, which is 79 years.

This is the central trade-off: you have made the legitimate login 600,000 times slower to make the offline attack 600,000 times slower. You accept the cost on the right side of the equation. The attacker has to bear the cost on the wrong side.

## Why the salt is the other half of the bargain

The iteration count makes each individual guess slow. The salt makes guessing at scale impossible. When two users pick the same password — and millions of people do pick `password123` — without a salt, the server stores identical hashes for both of them. The attacker can build one giant table of "here is the hash for every common password" and crack everyone in one pass. The salt, which is a 16-byte random value generated per user, makes this attack structure collapse.

The salt does not need to be secret. It is stored in plaintext next to the hash. What it does is *prevent reuse*. A user with the password `password123` and a salt of `8a3f...c2b9` has a totally different derived key than a user with the same password and a salt of `f104...a8e0`. The attacker cannot reuse any precomputed table. They have to do the full 600,000-iteration work for every single user, and they get a different result to compare against every time. Salt is the difference between "I cracked one user and got the password for 200,000 others" and "I cracked one user and I have to start over for the next one."

This is why the [PBKDF2 Generator on Elysia Tools](https://elysiatools.com/en/tools/pbkdf2-generator) lets you provide your own salt in hex format. The salt is a public input, not a secret. The whole point is that *every* call to derive the same password will produce a different output, and the storage format is `(algorithm, iterations, salt, derivedKey)`. All four pieces are required to check a password later.

## The math that nobody else will explain to you

The "PB" in PBKDF2 stands for Password-Based. The "KDF" stands for Key Derivation Function. The "2" is because this is the second version of the standard, published as RFC 2898 in September 2000. The algorithm itself is not exotic. The two important operations are `U_1 = HMAC(password, salt)` and `U_n = HMAC(password, U_(n-1))`. The final derived key is the XOR of `U_1` through `U_N`. The HMAC uses the password as the key and the previous output as the message, which means that to compute round *N*, you have to have computed round *N-1* first. There is no parallelization. There is no shortcut. The chain is forced to be sequential.

This is why the iteration count is a knob you can turn. Modern guidance from OWASP recommends 600,000 iterations for PBKDF2-HMAC-SHA256 and 210,000 for HMAC-SHA512, because the SHA-512 version has a wider internal block and gets slower faster. The year these numbers were recommended, they took about 250 milliseconds on a server-class CPU. Every three years, the recommended number roughly doubles, because hardware gets faster and the same wall-clock time requires more rounds. In 2010, the standard recommendation was 1,000 iterations. In 2017, it was 10,000. The drift is not because the algorithm got weaker. It is because computers got faster, and the cost of the attack dropped by orders of magnitude while the cost of the legitimate login stayed the same.

## What the actual output looks like

When you run the tool on a password like `correct horse battery staple` with 100,000 iterations and a SHA-256 algorithm, the output is two hex strings: a 16-byte salt and a 32-byte derived key. The salt is randomly generated by the tool on the server. The derived key is computed deterministically from those four inputs. The whole point is reproducibility — given the same password, salt, algorithm, and iteration count, anyone, anywhere, can verify the derived key. That is what makes it a *function* and not just an encryption.

What the output is *not* is reversible. There is no math operation that takes the derived key and produces the password. The only way to recover the password is to try candidates one at a time. With a 32-byte derived key, the search space for direct inversion is 2^256, which is more than the number of atoms in the observable universe. The function is one-way by design.

## Why this is not the best password hasher anymore

PBKDF2 is twenty-five years old. It works. It is fast enough that users do not notice, slow enough that attackers do. But it has a serious weakness: it is *GPU-friendly*. A modern graphics card can run thousands of HMAC-SHA-256 operations in parallel because each round has a small fixed cost. PBKDF2 does not require much memory per candidate. The newer alternatives — Argon2, scrypt, bcrypt — were designed to be *memory-hard*. They force the attacker to dedicate a large chunk of RAM per candidate, which makes the parallelization story collapse. You cannot fit a thousand Argon2 computations in the memory of a single GPU the way you can fit a thousand PBKDF2 computations.

That is why the [PBKDF2 Validator](https://elysiatools.com/en/tools/pbkdf2-validator) exists as a separate tool from the generator. Validation — re-deriving the key from a stored hash and a login attempt — uses the exact same algorithm with the exact same parameters. The two are paired because the validator's input is the generator's output, and any drift in the four input parameters produces a different derived key. The validator is also the place where the iteration count choice lives: if you set 100,000 iterations in the generator, the validator must use the same 100,000 to reproduce the result. The derived key is the proof that all four inputs matched.

## What every password hasher is really trying to defend against

The actual threat model is not a single attacker trying to log into your account. The threat model is a stolen database. If an attacker gets a copy of the user table, they have every hash and every salt. They cannot reverse the hashes. They can only try candidates. The cost of each candidate attempt is the cost of the iteration count, and that cost is what stands between your account and a credential-stuffing attack that takes 20 minutes per user instead of 20 minutes for ten million users.

This is the reason every recommendation page in the last decade has moved toward 600,000 iterations. It is not security theater. It is the slowest reasonable cost that a server can pay on every login, multiplied by the number of candidates an attacker is willing to try, and the product has to be larger than the value of the account. That is the only equation that matters. The rest of the cryptography is just the language we use to express it.

Try the derivation yourself on a real password and see how the same input produces a totally different output the moment the salt changes. That experiment is worth more than a thousand pages of standards documents. The slowness is the security, the salt is the anti-reuse, and the iteration count is the dial you turn as hardware gets faster. Everything else is implementation detail.
