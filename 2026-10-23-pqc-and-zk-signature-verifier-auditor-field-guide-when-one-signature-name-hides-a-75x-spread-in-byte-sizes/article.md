<strong>A signature scheme's byte size is not a spec footnote; it is the number your CDN, your HSM, and your 2030 signing deadline all have to hold at once.</strong> Teams auditing a post-quantum migration almost always start with algorithm names, because names are what the standards documents lead with. Sizes are what break the plan. ML-DSA signs in 2420, 3309, or 4627 bytes depending on the parameter set; FN-DSA Falcon-512 signs in 666; SLH-DSA-SHAKE-256f needs 49856. That is a 75x spread hiding inside one phrase, "post-quantum signature", and no single certificate envelope, header budget, or TLS record survives all of it without a deliberate decision.

## The FIPS Numbering Error That Starts Most Migrations Wrong

The cheapest audit finding in this field is a number that is off by one digit. ML-DSA is FIPS 204. It is not FIPS 203, because FIPS 203 is ML-KEM, a key-encapsulation standard that solves a different problem entirely. SLH-DSA is FIPS 205. FN-DSA, the Falcon family, is FIPS 206 and is still a draft.

Getting this wrong is not a typo in prose. It sends a team looking for a signature standard that does not exist, and it is common enough that blog posts and internal wikis repeat it. The PQC and ZK Signature Verifier Auditor pins the mapping in one line of every output, so the correction travels with the audit instead of living in somebody's head. You can check the sizes matrix yourself at [Elysia Tools](https://elysiatools.com/en/tools/ml-dsa-slh-dsa-fn-dsa-pqc-bbs-plus-plonk-halo2-zk-verifier).

## Thirteen Schemes, Four Families, One Byte-Length Table

The audit matrix in scope-all mode returns 13 schemes, sorted into four families. The lattice family holds ML-DSA-44, ML-DSA-65, ML-DSA-87, FN-DSA-512, and FN-DSA-1024. The hash family holds four of the twelve SLH-DSA parameter sets, chosen because they span the useful size range. The pairing family contributes BBS signatures. The zero-knowledge family contributes Groth16, PLONK over KZG, and Halo2 over IPA.

Each lattice row carries an exact triple: public key, secret key, signature. ML-DSA-44 is 1312 / 2560 / 2420. ML-DSA-65 is 1952 / 4032 / 3309. ML-DSA-87 is 2592 / 4896 / 4627. RFC 9964 registered the three sets as COSE and JOSE algorithm identifiers negative 48, negative 49, and negative 50, which is the value that ends up in a signed header rather than the human-readable name.

<figure class="highlight-card" data-placeholder="CARD1_URL"><img decoding="async" src="CARD1_URL" alt="Highlight card: five post-quantum signature sizes from the standards table, ranging from Falcon-512 at 666 bytes to SLH-DSA-SHAKE-256f at 49856 bytes" loading="lazy" /></figure>

The hash family looks nothing like the lattice family, and that is the point. SLH-DSA-SHA2-128s has a 32-byte public key and a 7856-byte signature. SLH-DSA-SHA2-128f has the same 32-byte key and a 17088-byte signature. The f-family trades signature size for signing speed, which is the same tradeoff the lattice family makes in a different currency.

## The 75x Signature Spread Between Falcon-512 and SLH-DSA-256f

Put the smallest and largest standard signatures side by side. FN-DSA-512 publishes a 897-byte public key and a 666-byte signature, small enough that a signature still fits comfortably in ordinary structured logs and cookie-free headers. SLH-DSA-SHAKE-256f publishes a 64-byte key and a 49856-byte signature, which is the largest standardized post-quantum signature in the table.

The consequence is that "adopt post-quantum signatures" is not a single engineering task. For data-plane signing inside a request, the 666-byte option is cheap and the 49856-byte option is not. For long-lived document or firmware signing, where a 50 KB signature appears once per artifact, the size argument largely disappears and the stateless-hash-based security model carries the decision instead.

FN-DSA also carries a warning the sizes table alone will not give you: the FFT Gaussian sampler behind Falcon is notoriously fiddly to implement correctly. Small signatures are not free. For comparison, the classical-style tooling you would otherwise reach for remains available at [Digital Signature Generator](https://elysiatools.com/en/tools/digital-signature-generator), which is a reasonable way to keep a control path while the post-quantum path matures.

## Trusted Setup Is the Line Your Migration Cannot Cross Back

The zero-knowledge rows answer a different question from the signature rows, and conflating them is how teams schedule themselves a rewrite. Groth16 needs a per-circuit ceremony; change the circuit and you owe the ecosystem a new phase-2 ceremony. PLONK over KZG needs a universal but updatable Powers of Tau setup, so one structured reference string serves many circuits up to a size bound. Halo2 needs nothing at all: the IPA construction over the Pasta curves is transparent, which is why zkEVM rollups use it.

The audit lists STARKs alongside the three named systems for the same reason. STARKs are hash-based and transparent, so they are post-quantum plausible with no ceremony, at the cost of larger proofs. Groth16 carries a second caveat: its proof is 192 bytes and compact, but bn254 is not post-quantum safe. Compact and post-quantum are independent properties.

Every row in the lattice, hash, and pairing families needs no setup whatsoever. That asymmetry is worth stating plainly during planning, because a ceremony is a schedule item with humans in it while a signature migration is not. Threshold aggregation behaves differently again, and [the BLS threshold simulator](https://elysiatools.com/en/tools/bls-boneh-lynn-shacham-threshold-signature-aggregation-distributed-key-gen-simulator) is a useful companion when your design assumes many signers and one aggregate.

## The CNSA 2.0 Timeline Has Five Milestones and Two Already Matter

CNSA 2.0 is the schedule that turns this from an academic question into a procurement one. The advisory published in September 2022. New NSS acquisitions must support CNSA 2.0 from 2027-01-01. Software and firmware signing must be post-quantum exclusively by 2030-12-31, with LMS and XMSS encouraged immediately rather than at the deadline. Browsers, servers, cloud, and operating systems move to exclusive use in 2033, and NSM-10 reaches a fully quantum-resistant endpoint in 2035.

Two of those five milestones are already inside the planning horizon of most organizations, and only one of them is the famous 2035 one. Reading the deadline as a single far-future date is the expensive misreading; the 2027 acquisition gate is the one that lands first.

## Running a Real Sign and Verify Cycle in a Browser Tab

The second mode of the auditor does not print a table. It generates a keypair from a deterministic SHAKE256-based DRBG with fixed seed material, signs your message with a pure TypeScript FIPS 204 implementation, verifies the signature, then flips one bit at byte offset 10 and verifies again to confirm the tampered copy is rejected.

For ML-DSA-65 the result is fixed and checkable. The public key is 1952 bytes, the secret key is 4032, the signature is 3309. The public key prefix reads `03f4799f4417a0e24062e746f5ec7a80` and the signature prefix reads `c7d49c04c0d5990657be9cf57afb1c6c`. Verify returns valid and the tampered copy is rejected, because that is what a correct implementation does and what a broken one quietly does not.

Those bytes were cross-checked against locally compiled PQClean reference binaries for all three parameter sets, with the rejection loop matching iteration for iteration. That matters more than it sounds: most browser crypto demos are a toy implementation with a self-consistency check, which proves only that the code agrees with itself. When a signature length and a key prefix are reproducible against an external reference, you have evidence about interoperability, not just about determinism.

## Identifying an Unknown Key or Signature by Its Length Alone

The third mode answers a question that comes up during incident triage, vendor conversations, and log archaeology: what is this blob? Paste hex or base64 and the auditor measures the decoded length, then matches it against every public key, secret key, and signature size in the table. A 1312-byte blob is an ML-DSA-44 public key. A 3309-byte blob is an ML-DSA-65 signature. A 49856-byte blob is an SLH-DSA-SHAKE-256f signature.

<figure class="highlight-card" data-placeholder="CARD2_URL"><img decoding="async" src="CARD2_URL" alt="Highlight card: the same byte length maps to different scheme and object types, so a blob identifier reports the scheme, the object kind, and the byte count" loading="lazy" /></figure>

Length is a strong signal for post-quantum objects precisely because the sizes are unusual and well separated. It is a weaker signal for classical material, where a 256-byte blob could be a P-256 public key, an Ed25519 public key, or a padded key of some other kind. The same caveat applies when you decode a JWT to check its algorithm, since the header still has to be read for the answer to mean anything. A [JWK Generator and Parser](https://elysiatools.com/en/tools/jwk-generator) is the right tool for the classical side of that comparison.

## What to Audit Before You Commit a Signing Pipeline

Fix the standard mapping before you write any code, then take sizes from a table rather than from memory. Decide your signature budget from the largest scheme you might ever deploy, not the smallest one you deploy today, and document which row in the table justifies it. Separate the zero-knowledge questions from the signature questions entirely, because only the zero-knowledge systems carry a ceremony in their critical path.

Then read the deadline list in order and work backwards from the 2027 acquisition gate, not the 2035 endpoint. Whatever you decide, make it reproducible. A standards matrix that prints the exact key and signature lengths next to their FIPS numbers and COSE identifiers is worth more than a paragraph asserting that migration is straightforward, and it costs one page. The same discipline applies to the artefacts that carry your signatures: a [certificate decoder](https://elysiatools.com/en/tools/certificate-decoder) will tell you whether an existing chain was ever built for post-quantum sizes at all.

Explore the rest of the cryptography tooling at [elysiatools.com](https://elysiatools.com/en/categories/cryptography).