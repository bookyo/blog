# Permutation / Combination / Subset Generator (With Repeats) — Field Guide

## Lead

**Counting distinct arrangements of repeated items is the kind of math that looks elementary until you actually have to compute it.** Three A's and one B yields six subsets, not eight; two A's and one B yield three permutations, not six. The math is exact, but only when the formulas account for repeated elements — `n!` over `Π(mᵢ!)` for permutations, `Π(mᵢ + 1)` for subsets. This field guide walks through when those two formulas apply, why naive counting silently over-counts multisets, and how the [Permutation / Combination / Subset Generator](https://elysiatools.com/en/tools/combinatorial-generation) tool returns exact counts up to n=12 alongside the deduplicated, lexicographically ordered listings.

## When the multiset count is the only thing that matters

You have the letters A, A, B, and you want to know how many distinguishable three-letter arrangements exist. The naive `3! = 6` answer is wrong because two of the three letters are identical. The correct count is `3! / 2! = 3` — the permutations AAB, ABA, BAA, and that's it.

The general formula is `n! / Π(mᵢ!)` where `mᵢ` is the multiplicity of the `i`-th distinct item. For `[A, A, B]` that's `3! / (2! · 1!) = 3`. For `[A, A, A, B]` it becomes `4! / (3! · 1!) = 4`. The factorial division cancels out the permutations that swap identical items, which the underlying counting otherwise double-counts.

This is the classic case where intuition overcounts by a factor of `Π(mᵢ!)`. It's also where most "how many anagrams does this word have?" Stack Overflow answers go wrong — they treat each letter as distinct. Try the [Permutation / Combination / Subset Generator](https://elysiatools.com/en/tools/combinatorial-generation) with the multiset `[A, A, B]` and you'll see exactly three permutations, not six.

## Combinations as generating-function coefficients

For distinct items, the number of ways to choose `k` from `n` is `C(n, k)`. For multisets with repeated items, the answer comes from a different place: the generating-function coefficient.

For `[A, A, B]` with `k = 2`, expand `(1 + x + x²)(1 + x)`. The coefficient of `x²` is `1 + 1 = 2` — the two combinations AA and AB. Note that AB and BA collapse to the same combination because order does not matter. The coefficient formula extends naturally: for a multiset with multiplicities `m₁, m₂, ..., mₖ`, the coefficient of `x^j` in `Π(1 + x + x² + ... + x^(mᵢ))` is the number of distinct combinations of size `j`.

The tool handles this in code rather than symbolically, but the resulting count matches the coefficient exactly. For practical purposes, that means you can hand it `[1, 1, 2, 3]` and ask for `k = 3` and you will get the same number you'd get from expanding the generating function and reading off the coefficient.

## Subsets are the simplest case — and the easiest to miscount

The number of distinct subsets of a multiset `[m₁, m₂, ..., mₖ]` is `Π(mᵢ + 1)`. Each item can appear 0, 1, 2, ..., or `mᵢ` times in a subset, and those choices multiply.

For `[A, A, B]` that's `(2+1)(1+1) = 6`. The six subsets are: `{}`, `{A}`, `{A,A}`, `{B}`, `{A,B}`, `{A,A,B}`. Note that `{A}` and `{A,A}` are distinct subsets because the multiset distinguishes them by count — a subset of a multiset is a function from items to non-negative integers, not a set of items.

The empty set is always included, so the formula gives at least 1 for any non-empty input.

## Why the display cap matters when n gets large

The tool caps displayed permutations at 200 entries even though it can count them exactly up to n=12. For `n = 12` distinct items, that's `12! = 479,001,600` permutations — far more than any human wants to scroll through. The count stays exact because the formula `n! / Π(mᵢ!)` is closed-form; the listing is what's truncated.

This split between "what we can compute" and "what we can show" is a feature, not a bug. If you need the full listing, you'll need to either reduce `n` or accept the truncation. If you only need the count, the formula is exact up to the factorial-precision ceiling of the runtime (Python integers are arbitrary-precision, so the practical limit is RAM and patience).

## Combinations mode enforces k <= n

The tool requires `1 <= k <= n` for combinations mode. This is not arbitrary — when `k > n` you are asking for combinations of more items than you have, and the answer is 0 for distinct items or undefined for multisets with the generating-function formulation. Rejecting the input at parse time is cleaner than silently returning 0 and letting you wonder whether your configuration was wrong.

For multisets, the constraint is similar but slightly more forgiving: `k = 0` is always valid (yielding the empty combination), and `k = sum(mᵢ)` is the largest valid value (yielding the multiset itself as a single combination).

## Common pitfalls when working with multisets

Three traps that show up in real-world combinatorics problems:

1. **Treating distinct items as a multiset** — the letter "M" appears once in "MISSISSIPPI", not eleven times. Tools that take a list of items treat each position as distinct unless you deduplicate first.
2. **Confusing combinations and subsets** — combinations fix a size `k`; subsets cover all sizes `0` to `sum(mᵢ)`. They are related but not interchangeable.
3. **Ignoring the empty case** — for multisets with multiplicities summing to `n`, the total number of combinations across all sizes is `Π(C(mᵢ + j, j))` summed over `j`, which is usually much larger than the subset count.

The [Permutation / Combination / Subset Generator](https://elysiatools.com/en/tools/combinatorial-generation) handles all three correctly by keeping the three modes separate and computing each via its own formula. You do not have to pre-deduplicate or pre-pick `k` — you pick the mode that matches your question and let the tool apply the right formula.

## When to use this tool versus a full programming environment

For exploratory work, the tool is faster than writing Python: paste your multiset, pick a mode, get the count and (up to 200) the actual listings in a single step. For production-grade work — say, generating all combinations of a 12-item set with constraint pruning — you'll want a real programming language with backtracking and early termination. The tool is best for verification and exploration; for performance-critical enumeration, drop to code.

A useful pattern: use the tool to verify your hand-computed formula on small cases (`n <= 6`), then port the validated logic to code for the larger runs. The closed-form formulas (`n! / Π(mᵢ!)` for permutations, generating-function coefficient for combinations, `Π(mᵢ + 1)` for subsets) are the same regardless of where you compute them — the tool just gives you a sanity check without the compile-run cycle.

## Closing — three things to remember

The two key formulas — `n! / Π(mᵢ!)` for permutations and `Π(mᵢ + 1)` for subsets — handle the multiset case correctly where naive `n!` and `2^n` over-count. Combinations sit between them, with the generating-function coefficient as the canonical source. And the [Permutation / Combination / Subset Generator](https://elysiatools.com/en/tools/combinatorial-generation) keeps these three cases in separate modes so you do not have to pre-pick which formula applies.

For deeper work, the lex-ordered output (`next_permutation` based) makes it easy to verify that the count matches the listing — you can scroll the first 10, count them, and divide by the over-counting factor to see why the formula gives what it gives.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
