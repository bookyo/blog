<strong>Poker math collapses to a single number once you split it into named hand classes.</strong> Anyone who's stared at a flop and tried to back-of-the-envelope their outs has hit the same wall: there are 2,598,960 distinct five-card hands from a 52-card deck, and the hand you actually want to hit (a straight, a flush, a set) is a vanishingly small slice of that. The temptation is to memorize ratios, but ratios rot fast and the wrong one loses money at the table. The cleaner approach is to classify hands into the ten canonical poker classes — royal flush down to high card — and let a calculator do the combinatorial arithmetic. The [Card Probability Calculator](https://elysiatools.com/en/tools/card-probability) on Elysia Tools computes exact probabilities for any of the ten standard hands from a single 52-card deck, in either specific-hand mode (you pick the hand, you get the probability) or all-hands mode (the tool enumerates every named class in one shot). This field guide walks through the math, the two operating modes, the hand-class taxonomy, and the four edge cases where the named-hand shortcut can quietly mislead you.

## What "probability of a poker hand" actually means

Every probability the calculator reports is the count of five-card hands that match a target class, divided by the total number of distinct five-card hands from a single 52-card deck. The denominator is fixed at C(52, 5) = 2,598,960 — the number of ways to choose five cards from 52 without regard to order. The numerator depends on the hand class. The ten canonical classes are:

<ul>
<li><strong>Royal flush</strong> — the ten, jack, queen, king, and ace of the same suit. There are exactly 4 royal flushes (one per suit), so the probability is 4 / 2,598,960 ≈ 1 in 649,740.</li>
<li><strong>Straight flush</strong> — five sequential cards of the same suit, excluding royal flushes. There are 36 such hands (ten rank choices × 4 suits − 4 royals).</li>
<li><strong>Four of a kind</strong> — all four cards of one rank plus any fifth card. There are 624 hands (13 ranks × 12 kicker choices).</li>
<li><strong>Full house</strong> — three of a kind plus a separate pair. There are 3,744 hands.</li>
<li><strong>Flush</strong> — five cards of the same suit, not forming a straight or straight flush. There are 5,108 hands.</li>
<li><strong>Straight</strong> — five sequential cards of mixed suits, with the ace playing either high or low. There are 10,200 hands.</li>
<li><strong>Three of a kind</strong> — three cards of one rank plus two unmatched cards. There are 54,912 hands.</li>
<li><strong>Two pair</strong> — two distinct pairs plus a fifth unmatched card. There are 123,552 hands.</li>
<li><strong>One pair</strong> — exactly one pair and three unmatched cards. There are 1,098,240 hands.</li>
<li><strong>High card</strong> — five unmatched cards that do not form any of the above. There are 1,302,540 hands.</li>
</ul>

The ten probabilities sum to exactly 1.0 because the ten classes partition the sample space. If the calculator ever reports a class with a numerator that doesn't match the count above, the model is wrong — the recipe relies on these combinatorial counts being canonical.

## Specific-hand mode versus all-hands mode

The calculator exposes two operating modes through the `calculationType` option. **Specific-hand** (`specific-hand`) asks the calculator to compute the probability of a single named hand class. You pick the class via `specificHand` (royal-flush, straight-flush, four-of-a-kind, full-house, flush, straight, three-of-a-kind, two-pair, one-pair, high-card), and the response is one number — the exact count and the decimal probability. This mode is what you want when teaching the math or when a single hand class is the question. **All-hands** (`all-hands`) ignores the `specificHand` selector and returns the full ten-class breakdown in one response. This mode is what you want when comparing the rarity of multiple hands at once, or when building a frequency chart for documentation.

The two modes share the same denominator (2,598,960) and the same hand-class taxonomy, so the numbers reconcile: the `all-hands` sum equals the individual `specific-hand` answers added together. The mode is just a packaging choice — one class versus ten.

## How the calculator returns the answer

The calculator's JSON response is intentionally minimal: a count (the number of 5-card hands in the class) and a probability (the decimal between 0 and 1). Specific-hand mode returns one count/probability pair; all-hands mode returns ten pairs, keyed by the canonical hand class name. The response shape mirrors the model — count divided by C(52, 5) = 2,598,960. There is no "as a percentage" toggle in the output; if you want percent, multiply by 100 client-side. The decimal is also a high-precision float, so the trailing-digit noise that 1-in-N expressions introduce is gone. This matters when two classes are very close in probability (flush at 1 in 509 versus full house at 1 in 694, for example) — the raw decimals distinguish them cleanly.

## Where the combinatorial shortcuts break down

The ten-class model is exact for a single deck and a five-card hand. It quietly stops being exact in four situations that show up in real play. **Multiple decks** — blackjack and some home games use 2-8 decks. The five-card-probability table assumes 52 unique cards. With two decks, the probability of being dealt a pair from your first two cards changes because there are 104 cards and pairs overlap; the poker-hand probabilities shift similarly. **Cards already on the table** — if you're computing the probability of a hand class on the turn after seeing the flop, the deck is no longer a clean 52. Conditional probabilities (given what's been dealt) require a different model. **Joker / wild cards** — the hand-class taxonomy assumes no wild cards. With jokers, the count of valid hands grows and the named-class boundaries blur. **Community-card games** — Texas Hold'em and Omaha use a 7-card or 9-card pool, not a 5-card hand. The hand-class definitions apply to the best 5-card subset, which means different numerators and a much larger denominator.

If any of these conditions apply, the named-hand shortcut is a useful sanity check but not the answer. The calculator's output is the cleanest possible number for the 5-card, 1-deck, no-wild scenario.

## The probabilities at a glance

The table below pairs each named hand with its exact 5-card count and probability. The numbers are the canonical references that any poker math resource should match.

<ul>
<li>Royal flush — count 4 — probability 0.00000154 — odds 1 in 649,740.</li>
<li>Straight flush — count 36 — probability 0.0000139 — odds 1 in 72,193.</li>
<li>Four of a kind — count 624 — probability 0.000240 — odds 1 in 4,165.</li>
<li>Full house — count 3,744 — probability 0.00144 — odds 1 in 694.</li>
<li>Flush — count 5,108 — probability 0.00197 — odds 1 in 509.</li>
<li>Straight — count 10,200 — probability 0.00392 — odds 1 in 255.</li>
<li>Three of a kind — count 54,912 — probability 0.0211 — odds 1 in 47.4.</li>
<li>Two pair — count 123,552 — probability 0.0475 — odds 1 in 21.0.</li>
<li>One pair — count 1,098,240 — probability 0.423 — odds 1 in 2.37.</li>
<li>High card — count 1,302,540 — probability 0.501 — odds 1 in 2.00.</li>
</ul>

The distribution is heavily right-skewed — high card and one pair together cover 92.4% of all five-card hands, while the rare classes (royal flush through straight) account for less than 0.4% combined. That skew is why memorized ratios for "rare" hands drift: the gap between 1-in-509 (flush) and 1-in-694 (full house) is small enough that misremembering which is rarer is easy.

## When the named-class shortcut is the right tool

The 5-card, 1-deck model is the right fit for three concrete situations. **Classroom probability exercises** — introductory combinatorics units that ask students to compute hand probabilities benefit from a calculator that returns the canonical count and the decimal probability side by side, so the student can verify their binomial coefficient arithmetic against a trusted answer. **Pre-flop equity estimates in single-deck draw games** — five-card draw, video poker, and stud variants use the exact 5-card denominator, and the named-class shortcut gives the right prior for "what's the chance this hand class shows up at all". **Sanity checks on Monte Carlo simulations** — when a poker bot's equity numbers look off, the named-class answers from a single deck give the floor; any deviation suggests a simulation bug.

## When the shortcut isn't enough

Three situations need more than the named-class shortcut. **Texas Hold'em equity** requires 7-card enumerations (2 hole cards + 5 community cards), not 5-card enumerations; the hand-class taxonomy still applies to the best 5-card subset, but the denominator jumps to C(52, 7) = 133,784,560 and the numerators are larger. **Shorthanded or shortdeck games** (Six Plus Hold'em, for example) remove some cards from the deck and the hand-class counts shift — a flush is rarer relative to a straight because there are fewer suited cards. **Conditional and sequential probability** (probability of making a flush given you have four to a flush on the flop) requires turn-and-river enumeration, which the 5-card model doesn't capture.

For those cases, the named-class probabilities are still useful as a baseline — they tell you what 5-card, 1-deck, no-wild play looks like — but the actual decision math needs a deeper model.

## Closing thought

The 5-card, 1-deck, no-wild poker probability model is one of the cleanest examples of how combinatorial arithmetic collapses to a small set of named classes. Once you have the ten class counts and the single denominator, every named probability is a division. The [Card Probability Calculator](https://elysiatools.com/en/tools/card-probability) handles the bookkeeping; your job is to know which mode (`specific-hand` vs `all-hands`) and which class fits the question. Run the numbers before the table, sanity-check them against the count list above, and treat any deviation as a signal that the underlying game isn't a clean 5-card, 1-deck draw.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
