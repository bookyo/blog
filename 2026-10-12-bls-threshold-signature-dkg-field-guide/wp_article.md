<strong>BLS signatures are 96 bytes, but a single rogue key can forge the whole aggregate.</strong> In a committee that signs the same message every 12 seconds, the cost of that attack is what made Ethereum 2 switch from naive aggregation to proof-of-possession. The [BLS Threshold Signature Aggregation + DKG Simulator](https://elysiatools.com/en/tools/bls-boneh-lynn-shacham-threshold-signature-aggregation-distributed-key-gen-simulator) walks through the full lifecycle of that defense, from Joint-Feldman DKG to a 96-byte aggregate that verifies in two pairings, with every step grounded in real BLS12-381 scalar arithmetic rather than a black-box library call. This field guide is the manual that explains what that simulator is really showing you, and what each output line means in practice.

## What BLS Looks Like at the Curve Level

BLS is short for Boneh-Lynn-Shacham, and the signatures it produces are tied to a *pairing-friendly* elliptic curve - the simulator hardcodes BLS12-381, which is the same curve Ethereum's beacon chain uses for validator attestations. The two parameters that matter for the rest of this guide are **G1** (the curve where public keys and signatures live) and **G2** (the curve where the message-to-curve hash lands). A single signature is one G1 element, 96 bytes once you serialize it with the canonical big-endian encoding. Verify by checking `e(pk, H(m)) == e(sig, g2)` with two pairings - the cheap precompile path the simulator exposes.

The reason a 96-byte aggregate can replace 96 individual signatures is the *bilinearity* of the pairing: `(a*s1 + b*s2)` is a valid aggregate of two partials with the same message hash. That algebraic closure is the foundation for everything below.

## One Signing Ceremony or n-of-n Honest Participants

The naive case is signing with a *known* group secret. All n participants already share `sk`, so each signer produces `sig_i = sk * H(m)` and the aggregator sums them to `(n * sk) * H(m)`. Verify against the *group public key* `pk = sk * g1`. This works, but shipping `sk` to every participant is the security failure mode - one compromised machine leaks the whole signing key.

That is exactly why every threshold signature protocol exists. The simulator drops this section visually because there is nothing to show: the same-`sk` case is the one you do not want to deploy.

## Why a t-of-n Threshold Needs a DKG

Before any signing can happen *without* anyone holding the whole secret, the group secret has to be *created* in a distributed fashion. Joint-Feldman DKG (DFK-pedersen variant in the simulator's t-of-n path) lets each of n participants deal a random polynomial `f_i(x)` of degree t-1, publish commitments `g1^(f_i(j))` for j = 0..t-1, and hand each peer its share `f_i(j)`. After the ceremony every participant holds a `share_j` that equals the sum of all `f_i(j)`, and the *group secret* `s` is the imaginary `sum_i f_i(0)` that no one has ever seen - it exists only as the discrete log of the group public key `g1^s`.

The Feldman share check is the line you will see most often: `g1^(share_j) == prod_i comm_i[j]`. If this fails for any i, the simulator returns an honest-dealer-vs-discard branch and the entire ceremony is rerun. Optional Pedersen hiding commitments (`g1^(f_i(j))` AND `g2^(f'_i(j))` for a second blinding polynomial) close the subliminal-channel attack on Feldman alone.

## From Two to N: How a DKG Ceremony Stays Honest

After the ceremony the simulator exposes the **3-of-4 Joint-Feldman DKG** scenario. Four committee members each deal a degree-2 polynomial over the real BLS12-381 scalar field. Every Feldman share check passes (`g1^(f_j(i))` matches the published commitments), the group public key equals `g1` raised to the never-materialized group secret, and any 3 signers - here participants 1, 2, 3 - produce partial signatures whose Lagrange-combined `Sigma lambda_i s_i` reconstructs `f(0)` exactly. A 2-signer forgery is rejected, and a different 3-of-4 quorum yields the *identical* aggregate signature - the simulator prints both to show the same-message same-key invariant in action.

This is why DKG ceremonies are the most expensive part of the lifecycle. After the ceremony, signing is cheap - usually two pairings per aggregate regardless of t.

## Threshold Signing: Lagrange Interpolation as the Actual Math

When signers 1, 3, 4 want to produce a 3-of-4 aggregate, they each compute `partial_i = sk_i * H(m)` and the aggregator applies the **Lagrange coefficient** `lambda_i = prod_(j != i, j in Q) (j / (j - i))` to weight each partial. The aggregate is `Sigma lambda_i partial_i` and verifies under the group public key. Bumping any one signer out of the quorum and re-running produces a *different* aggregate with different Lagrange weights, even though the same key signs the same message - that is exactly the property an aggregate should NOT have if you want block-proposer verifiability, but it is what the protocol guarantees.

The simulator precomputes the Lagrange coefficients and prints them alongside the partials, which is the part most implementations hide in a library.

## The 96-Byte Aggregate Signature Behind Every Beacon Vote

Ethereum 2 validator committees often run 128 or 256 signers on the same attestation. The aggregate signature is *still* 96 bytes - a single G1 element - but the verification equation becomes `e(pk_agg, H(m)) == e(sig, g2)`, and the **fast aggregate verification** trick `e(prod pk_i, H(m)) == e(prod sig_i, g2)` reduces 128 pairings to 2. The simulator's same-message attestation aggregation scenario exposes both verify paths and times them on a real BLS12-381 implementation.

Without aggregation a 128-validator block would carry 12 KB of signature data. With BLS aggregation it carries 96 bytes plus 128 48-byte public keys. That ratio is why BLS survived the post-quantum migration debate long enough to anchor most of the active staking ecosystem.

## The Rogue-Key Attack and the Proof-of-Possession Defense

If the simulator's rogue-key branch is enabled, you can watch an attacker register `pk_evil = pk_target - sk_attacker * g1` without ever learning `sk_target`. The naive aggregate `pk_evil + pk_target = sk_attacker * g1` then signs whatever the attacker wants on behalf of `pk_target`. The Ethereum 1.x audit and the academic literature both treat this as the single most catastrophic plain-BLS failure.

The defense is **proof of possession (PoP)**: every public key ships with a BLS signature `pop = sk * H("BLS_POP_CHALLENGE")`, and verification rejects any key whose PoP does not verify under itself. The simulator's PoP defense sub-tab reproduces the attack and its fix side-by-side so you can confirm the PoP enforcement closes both vectors.

## Where to Try the Full BLS Lifecycle Yourself

Open [the BLS Threshold + DKG simulator](https://elysiatools.com/en/tools/bls-boneh-lynn-shacham-threshold-signature-aggregation-distributed-key-gen-simulator) to run the four core scenarios - Joint-Feldman DKG, threshold signing, rogue-key attack + PoP defense, and same-message attestation aggregation - on real BLS12-381 arithmetic. The browser tab is faster than running a Python notebook and prints the same Lagrange coefficients and Feldman checks you would derive by hand. For more pairing-based primitives, browse [all Elysia Tools cryptography entries](https://elysiatools.com/en/tools/cryptography) or [the full tool directory](https://elysiatools.com/en/tools).
