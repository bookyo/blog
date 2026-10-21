<strong>No row is safe and no column is dangerous.</strong> Most people meet the minimax theorem as an abstraction — a payoff matrix, a saddle-point test, then a shrug. This guide starts where people actually get stuck: a real 3×3 bidding game where neither player has a pure move and the only rational answer is a mixture. The Zero-Sum Game Solver at [elysiatools.com](https://elysiatools.com/en/tools/game-theory-zero-sum) does that work in one paste. What follows is about reading what it hands back.

## The Game That Has No Pure Answer

Take three bidders competing for one contract, each choosing a bid level, with the payoff written as gain to the bidder:

<table style="border-collapse:collapse;width:100%;margin:1em 0;">
<thead><tr>
<th style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;background:#f5f7fb;font-weight:600;">Bid</th>
<th style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;background:#f5f7fb;font-weight:600;">Low</th>
<th style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;background:#f5f7fb;font-weight:600;">Mid</th>
<th style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;background:#f5f7fb;font-weight:600;">High</th>
</tr></thead>
<tbody>
<tr>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;"><strong>Low</strong></td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">0</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">1</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">2</td>
</tr>
<tr>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;"><strong>Mid</strong></td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">-1</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">0</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">1</td>
</tr>
<tr>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;"><strong>High</strong></td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">-2</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">-1</td>
<td style="border:1px solid #cfd6e4;padding:8px 12px;text-align:left;vertical-align:top;">0</td>
</tr>
</tbody>
</table>

Row minima are `0, -1, -2`, so the row player can guarantee `0`. Column maxima are `0, 1, 2`, so the column player can hold the row player to `0`. The bounds meet, so a pure equilibrium exists at the `Low`/`Low` cell.

Now change one entry — `Mid`/`Low` moves from `1` to `-1` — and the tidy case collapses. Row minima become `-1, -1, -2` (maximin `-1`), while column maxima become `0, 0, 2` (minimax `0`). Since `maximin < minimax`, no cell is optimal for both players, and the only remaining answer is a mixture. The solver returns value `-0.5` with both players putting probability `0.5` on `Low` and `0.5` on `Mid`.

## Why Pure Equilibria Are the Exception

The correct saddle test is easy to get backwards. Because the row player maximises, an equilibrium cell must be the **largest entry in its column** (nothing else in that column beats it) and the **smallest entry in its row** (nothing else in that row is worse). A cell that is largest in its row is not an equilibrium candidate at all — the column player would simply avoid it.

That conjunction is a strong coincidence in a 2×2 game and close to impossible in a 6×6. Real competitive settings make it rarer still. When you model competitors or customers you are usually encoding structural facts: one firm has a cost advantage, one platform has a larger installed base. Structural advantages produce matrices where each side's best move is predictable, and that is precisely the shape that destroys pure equilibria.

The practical warning: if you plan against a competent opponent using a single fixed strategy, you are probably playing the game with your information advantage already spent.

## What a Mixed Strategy Actually Means

A mixed strategy is a probability distribution over your pure actions — a vector `x` with one non-negative component per row, summing to 1. The column player gets `y`, one component per column, also summing to 1. The value of the game is the payoff where the two meet: `v = xᵀAy`.

Two inequalities define a correct solution, and the solver checks both numerically:

<ul>
<li><strong>Row guarantee:</strong> `xᵀA ≥ v` componentwise — no column choice can pull the row player below the value.</li>
<li><strong>Column guarantee:</strong> `Ay ≤ v` componentwise — no row choice can push the payoff above the value.</li>
</ul>

For the perturbed game above, `x = y = (0.5, 0.5, 0)` gives `xᵀA = (-0.5, -0.5, 1.5)`, which sits above `v = -0.5`, and `Ay = (-0.5, -0.5, -1.5)`, which sits below it. Neither player can deviate profitably.

Compare matching pennies on `[[1, -1], [-1, 1]]`, where the row minima are both `-1` and the column maxima are both `1`. There is a gap of two and the solver returns value `0` with both players mixing `0.5/0.5`: a fair coin, where neither side can do better than an even split. Mixing is not a trick — it is the shape of rational play when someone is watching.

## The Shift Trick, and Why Every Entry Must Go Positive

The mixed solver reaches `x` and `y` through linear programming, and LP needs a non-negative feasible region. Bidding games routinely contain negative payoffs, which would make the problem infeasible for no good reason. The solver adds a constant `K` to every entry so the smallest becomes exactly `1`, then solves the shifted matrix `B = A + K`. For the game above the minimum entry is `-2`, so `K = 3`.

Adding `K` everywhere changes no strategy at all. Each player's mix sums to 1, so the expected payoff shifts by exactly `K·(xᵀ1)(1ᵀy) = K` — a constant that does not depend on how the mixture is chosen. The optimal `x` and `y` are identical in `A` and `B`; only the reported value moves. Solving the shifted game gives value `2.5`, exactly `3` above the original `-0.5`, with identical mixes.

That is why you can paste a matrix full of negative entries and get a correct mixture instead of an infeasibility error, and why the solver reports the shift it applied. If you ever see the value move unexpectedly when you add a constant to every entry, check that report first.

## One Solve, Two Strategies

The most elegant property of the LP formulation is that both players fall out of a single solve. With the column player maximising and constraints `Bz ≤ 1` for shifted matrix `B`:

<ul>
<li>The <strong>primal slack variables</strong> give the column player's mix `y` directly.</li>
<li>The <strong>dual variables</strong> — the shadow prices on the `Bz ≤ 1` constraints — give the row player's mix `x`.</li>
</ul>

Duality guarantees the two are consistent, so one simplex pass yields a complete, verified equilibrium pair. The solver uses Bland's rule for its pivot choice, which guarantees termination instead of cycling, and its final verification step re-evaluates `xᵀA` and `Ay` against the reported value before showing you anything. Recovering a four-by-four dual solution by hand is error-prone in a way that is genuinely hard to notice; a solver that checks both inequality families turns a silent mistake into a visible one. For the same two-phase machinery applied to general constraints rather than a payoff matrix, the [Linear Programming Simplex Solver](https://elysiatools.com/en/tools/linear-programming-simplex) is the natural companion.

## Sizing the Problem Before You Solve It

Matrix shape tells you how much structure there is to exploit:

<ul>
<li><strong>2×2 with a saddle point</strong> — arithmetic only. Compare four cells and you are done.</li>
<li><strong>2×2 without one</strong> — the classic mixing case, where four probabilities fall out of a cross-multiplication rule.</li>
<li><strong>3×3 and up</strong> — LP territory, with as many constraints as rows and much less pleasant algebra.</li>
</ul>

Non-square matrices are legitimate: 3×6 is a real game with six column actions against three row actions. One caution — a large matrix full of near-equal payoffs is harder to *estimate* than to *solve*. Your answer is limited by how well you know the payoffs, not by the linear programming.

A cheap sanity check before trusting any result: perturb one payoff and see whether the mix moves at all. If a single edit swings the answer wildly, the game is nearly degenerate and the numbers deserve more scepticism than the exact arithmetic would suggest.

## From Numbers to a Randomisation Policy

The solver returns probabilities, not a policy. Turning them into repeatable play needs three more decisions:

<ul>
<li><strong>Randomisation method.</strong> Use a private seed per decision. A predictable pseudo-random sequence is not a mixed strategy — it is a pure strategy with extra steps.</li>
<li><strong>Timing.</strong> Commit to the full mix for the whole game or redraw each round. Redrawing weakens your opponent's inference, which is usually the goal in repeated play.</li>
<li><strong>Estimation honesty.</strong> Payoff entries are usually estimates. Ask how far the mix moves when the entries that matter shift by ten percent, because the mix is often far more sensitive than the value is.</li>
</ul>

To see how a distribution-based payoff estimate behaves under uncertainty, feed the entry into the [Monte Carlo Simulation Builder](https://elysiatools.com/en/tools/monte-carlo-simulation-builder) and watch the equilibrium move as a distribution instead of a single number.

## A Compact Reference and the Model's Limits

<ul>
<li><strong>Saddle test:</strong> `max(row minima)` versus `min(column maxima)`; equality means a pure equilibrium exists.</li>
<li><strong>Equilibrium cell:</strong> largest in its column <em>and</em> smallest in its row.</li>
<li><strong>Mixed solution:</strong> `xᵀA ≥ v` for the maximiser, `Ay ≤ v` for the minimiser, both summing to 1.</li>
<li><strong>Shift invariance:</strong> adding `K` to every entry moves the value by exactly `K` and changes no strategy.</li>
<li><strong>Dual recovery:</strong> primal slack variables give one player's mix, shadow prices give the other's.</li>
</ul>

Zero-sum also assumes the payoff is exactly opposite for both sides, which real competition rarely honours. Price wars leave both firms worse off; bidding wars transfer surplus to a leftover bidder who is not a player at all. That leak makes a zero-sum model conservative in a useful direction — it assumes your opponent is maximising purely against you with no outside option, so the equilibrium it produces is a floor you can usually beat rather than a ceiling. When a third party profits from the interaction, model that surplus explicitly or add a player, because no amount of linear programming precision repairs a payoff matrix that allocates the money to nobody in the game.

The solver also assumes both strategies are chosen without observing the other. In sequential games — where one player moves, sees the reply, then moves again — you want backward induction instead, and the equilibrium is usually sharper and easier to compute than the mixed strategy of the simultaneous version.

The Zero-Sum Game Solver at [elysiatools.com](https://elysiatools.com/en/tools) takes a matrix of 2×2 to 6×6, runs the saddle-point test first, falls through to the shifted single-phase simplex when pure play fails, and verifies both players' security strategies numerically before reporting. Paste the matrix, read the value and the two mixes, and check the verification line — that is the whole workflow.