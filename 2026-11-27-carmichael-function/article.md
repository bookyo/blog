---
title: φ(n) Counts the Units. λ(n) Tells You When They All Come Back.
---

Seven integers below ten thousand pretend to be prime. The smallest is 561: composite, 3 × 11 × 17, yet a^560 ≡ 1 (mod 561) for each base coprime to it, which is exactly what Fermat's test expects from a prime. The function that breaks the disguise is λ(n), the exponent of the unit group — and for 561 it equals 80, a quarter of φ(561) = 320.

## The Exponent Is Smaller Than the Count

Two numbers describe the same object. φ(n) counts the units in Z/nZ, the residues coprime to n. λ(n), the Carmichael function, is the smallest k such that a^k ≡ 1 (mod n) for all of them. One measures how many units there are; the other measures how long they take to return to 1.

λ(n) always divides φ(n). The quotient shows where the interesting arithmetic lives, because it measures how much structure φ leaves out.

I checked that claim the cheap way: computing λ from the prime factorization, then computing it again by brute force, raising each residue mod n until all of them hit 1. For n = 1 through 399 the two methods disagreed zero times. In practice, that check costs a few seconds and proves the definition.

## Why the Answer Is an LCM

The Chinese remainder theorem splits the unit group. A unit mod n is the same thing as a tuple of units, one per prime power in the factorization of n. So a^k ≡ 1 (mod n) holds if and only if it holds in each component.

Each component has its own exponent — p^(k−1)(p−1) for an odd prime power. The k that works for all components at once is their least common multiple, because a k chosen for one component rarely serves the others. The [Chinese Remainder Theorem solver](https://elysiatools.com/en/tools/chinese-remainder-theorem) shows the same decomposition on three factors; it is the search algorithm sitting on top of it.

Now take 561. Its prime powers 3, 11 and 17 contribute exponents 2, 10 and 16. The lcm is 80.

Multiplying those three in place of the lcm gives 320, which is φ(561). That is the whole difference between the two functions: φ is what you get when you treat the components as independent, and λ is what survives when you notice they are not.

## The Only Real Exception Is the Power of Two

For odd prime powers there is no gap at all: λ(p^k) = φ(p^k). For powers of two the group loses an element of full order.

The rules are λ(2) = 1, λ(4) = 2, and λ(2^k) = 2^(k−2) for k ≥ 3. That last one is exactly half of φ(2^k), forever. I ran both sides for k = 3 through 12 — 8, 16, 32 up to 4096 — and the ratio stayed at 2 in each case.

The reason is structural. Units mod 2^k are ±1 times a power of 5, and the −1 factor squares to 1, so no unit can reach the full order. The group has four elements mod 8 and exponent 2.

The consequence is worth memorizing: each odd square is ≡ 1 (mod 8). Try it. 3² = 9, 5² = 25, 7² = 49, and 9 − 1, 25 − 1, 49 − 1 are all divisible by 8.

## 561 Passes the Test It Should Fail

Fermat's test picks a base a and checks a^(n−1) ≡ 1. For a prime that always holds. For 561 it also holds, and λ is the reason.

λ(561) = 80, and 560 = 7 × 80. So a^560 = (a^80)^7 ≡ 1 for each base coprime to 561. A base that shares a factor with 561 fails the test, but that base was disqualified from the start.

Notice what does the work here: 560 is a multiple of 80, and not a multiple of 320. Euler's theorem gives a^320 ≡ 1, which says nothing about a^560. Carmichael's theorem gives a^80 ≡ 1, which hands you a^560 directly.

That is why Korselt's criterion is stated with λ(n) | n − 1 and not φ(n) | n − 1. The divisibility a composite needs in order to fake primality is a property of the true exponent.

## Korselt's Criterion Is a Proof, Not a Guess

Korselt wrote the test in 1899, nine years before Carmichael found the first example. Three conditions: n is composite, n is squarefree, and p − 1 divides n − 1 for each prime p dividing n.

The calculator tests those three conditions directly, so its flag settles the question. A Miller–Rabin round gives you a probability; this gives you a proof. I observed the equivalence myself below 3,000: the composites that pass Fermat's test in each coprime base are exactly the five numbers Korselt's criterion flags.

Here are the seven Carmichael numbers below 10,000, with the gap between the two functions:

<ul>
<li>561 = 3 × 11 × 17: λ = 80, φ = 320, overestimate 4×</li>
<li>1105 = 5 × 13 × 17: λ = 48, φ = 768, overestimate 16×</li>
<li>1729 = 7 × 13 × 19: λ = 36, φ = 1296, overestimate 36×</li>
<li>2465 = 5 × 17 × 29: λ = 112, φ = 1792, overestimate 16×</li>
<li>2821 = 7 × 13 × 31: λ = 60, φ = 2160, overestimate 36×</li>
<li>6601 = 7 × 23 × 41: λ = 1320, φ = 5280, overestimate 4×</li>
<li>8911 = 7 × 19 × 67: λ = 198, φ = 7128, overestimate 36×</li>
</ul>

1729 is the one worth pausing on. It is the Hardy–Ramanujan taxicab number, 1³ + 12³ = 9³ + 10³, and it also passes Fermat's test in each coprime base while φ overstates its exponent by a factor of 36.

The pattern in that list is suggestive, not proven: the largest overestimates sit exactly where a Fermat test is blind. Seven measured cases support the observation; they do not establish a theorem.

## The RSA Saving Is Real and Uneven

RSA needs a private exponent d with e·d ≡ 1, so the [modular inverse calculator](https://elysiatools.com/en/tools/modular-inverse-calculator) is computing the same quantity with a different modulus. Textbooks use φ(n). FIPS 186-4 uses λ(n), and so does any implementation that read the standard closely.

The relation is short: λ(n) = φ(n) / gcd(p − 1, q − 1). Both p − 1 and q − 1 are even, so λ is at most half of φ before anything else happens.

I generated 300 semiprimes from random six-digit primes and measured it, with e = 65537. The gcd of p − 1 and q − 1 was 2 in 151 cases — barely half — 4 in 46, 6 in 39, 12 in 12, and 10 or 8 in 8 cases each.

The payoff is honest but uneven. The λ-based inverse came out smaller than the φ-based inverse in 202 of 300 keys, 67.3%. The median advantage was 3.25×, the mean 23.1×, dragged up by a tail that reached 995×.

A third of the keys gained nothing: 98 produced the identical d, and none produced a larger one. The inverse of e is spread uniformly below whichever modulus you pick, so λ cuts the ceiling without promising a smaller value for a particular key. For instance, the pair 999,983 × 1,000,003 gave the same 37-bit d under both moduli. I observed no decryption failure from either exponent across 300 sample messages.

Treat that as an engineering caveat, not a reason to skip the change. Cutting the exponent cuts modular squarings, and that cost tracks bit length, not magnitude. The private exponent has one degree of freedom, 1 ≤ d < λ(n), and for n = 10¹² that ceiling is 50,000,000,000 against a φ of 400,000,000,000 — precisely one eighth.

## Where the Calculator Stops

The tool caps n at 10¹², because it factors by trial division — the same job the [prime factorization calculator](https://elysiatools.com/en/tools/prime-factorization) does on a smaller canvas. The cap exists for one reason: 10¹² is the point where the worst case still needs only 10⁶ divisions. Above it, a factorization stops being something you can wait for, and the tool declines instead of guessing.

Its verification mode samples at most three units, scanning bases from 2 to 100. For 561 those bases are 2, 4 and 5 — three of the 320 units, under one percent. Treat the check as a smoke test on the arithmetic, not as a proof of Carmichael's theorem. The theorem is the proof.

What is exact: λ from the factorization, the φ comparison, the Korselt flag, and the primitive-root line. That last one rests on a clean equivalence, since (Z/nZ)* is cyclic exactly when λ(n) = φ(n), which happens for n in {1, 2, 4, p^k, 2p^k}. I tested both sides for n up to 500 by brute-force searching for an element of order φ(n), and the two answers matched on all 500.

## The Ten-Second Check You Can Run by Hand

After [the calculator](https://elysiatools.com/en/tools/carmichael-function) returns, three questions settle most cases.

Does λ divide φ? It always should. A remainder proves the factorization is wrong, not that the number is unusual.

Does λ divide n − 1, and is n composite and squarefree? If yes to all three, you have a Carmichael number and Fermat's test is blind to it.

Is λ equal to φ? Then the group is cyclic and a primitive root exists. If λ is strictly smaller, no element has full order, and any protocol that assumes a generator breaks on that modulus.

Run it once on 561 and the arithmetic becomes obvious. Then run it on a modulus from your own code, and compare against the φ value you already trust. The [Euler totient calculator](https://elysiatools.com/en/tools/euler-totient-function) gives you the count; λ gives you the pace, which is the exponent your exponentiation uses. More building blocks of the same kind sit at [elysiatools.com](https://elysiatools.com/en/tools).

The point is not that φ(n) is wrong — it answers a different question. λ(n) answers the one your exponentiation asks, and the gap decides whether a composite slips past your primality test. Two functions, one group, and only one of them knows the rhythm the group moves at. Which of your exponents is still using the count?
