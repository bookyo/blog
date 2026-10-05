**The browser formal-verification stack that runs without cvc5 or Z3** is becoming a real option for engineers who need a quick sanity check on a hardware invariant before reaching for a heavy native solver. The [SMT-LIB 2.7 / AIGER / BTOR2 Formal Verification Orchestrator](https://elysiatools.com/en/tools/smt-smtlib-2-7-cvc5-z3-btor2-aiger-k-induction-cddr-dbg-invariant-synthesis-orchestrator) bundles a hand-written CDCL solver with a Tseitin bit-blasting front end, an AIGER reader, a BTOR2 word-level reader, and the four proof techniques most verification engineers actually reach for: bounded model checking, k-induction, Craig interpolation, and an IC3/PDR-lite frame loop. The whole thing runs in your tab, parses the inputs a verification engineer already has on disk, and produces the counterexample trace or the invariant certificate you'd otherwise have spent half an afternoon coaxing out of a CLI solver. No Docker, no native binary, no license server.

## The Three Input Formats Cover The Hardware Stack

The orchestrator accepts the three formats the hardware-verification community actually uses, which is what makes it useful as a starting point. **SMT-LIB 2.7** in the `QF_BV` (quantifier-free bit-vector) theory with the Bool core is the universal interchange format — most property languages compile down to it, and most model checkers accept it directly. **AIGER** (`aag` ASCII and `aig` binary, including the delta-encoded variant) is the format hardware model checkers emit after synthesis from Verilog or VHDL. **BTOR2** is the word-level format the Boolector / hardware model-checking ecosystem produces. Together the three formats cover the path from RTL synthesis to bit-level SAT.

The front end parses SMT-LIB into a Tseitin-encoded bit-blasted CNF: every `FixedSizeBitVectors` operator — add, sub, mul, udiv, urem, the shifts, the comparators, concat, extract, extend, ite — is expanded into a flat AND/OR/NOT form. The AIGER reader lifts an and-inverter graph straight into the same CNF, and the BTOR2 reader bit-blasts word-level operators before they hit the SAT core. Three formats, one solver under the hood.

## The CDCL Engine Is The Same Family cvc5 And Z3 Sit On

Underneath the front ends sits a hand-written CDCL SAT engine. Two-watched literals, VSIDS-style activity scoring, 1-UIP clause learning, periodic restarts. Anyone who has read the MiniSat paper or thumbed through the cvc5 source recognizes the design. The point is that the same algorithmic core powers the orchestrator's four verification modes, so the certificates it produces come from the same conflict-driven learning loop the heavy native solvers rely on.

The CNF is shared across modes, which means the engine pays the parsing cost once even when you switch algorithms. Switching from BMC to k-induction, or from interpolation to IC3, reuses the watched-literal state and the learnt-clause database.

## Bounded Model Checking Finds Counterexamples Fast

**Bounded model checking (BMC)** unrolls the transition relation a fixed number of steps and asks the SAT engine for an assignment that violates the property at any unrolling depth. The orchestrator reports the satisfying assignment as a counterexample-witness trace — the input sequence of state values that drives the design to the bad state. When the property is actually false, BMC is usually the fastest path to the witness, because SAT can find a satisfying assignment without proving its absence at all unrolling depths.

The witness trace is what a verification engineer actually needs when they're debugging. A counterexample without a witness is just a "found bug" message; a counterexample with the trace tells you which input sequence on which cycle triggers the violation, which is what you take back to the design.

## K-Induction Proves Properties, Not Just Refutes Them

When the property might actually hold, BMC alone cannot give you an answer — the absence of a counterexample at depth k does not prove the property. **K-induction** closes the loop. It proves a property by induction on the unrolling depth: show the property holds at depth 0 (the initial state), then show that if it holds for k consecutive steps it also holds at step k+1. The orchestrator strengthens the inductive step with unique-state information — a configuration fingerprint check that prevents the induction from trivially failing because the same state recurs.

The unique-state strengthening matters in practice. Without it, k-induction often needs a depth much larger than the natural recurrence period of the design, because two distinct paths can lead back to the same state. With it, the induction typically converges at a much smaller k.

## Craig Interpolation Delivers Compact Inductive Lemmas

When the SAT engine returns a refutation for a BMC query, that refutation contains more than just "no witness exists" — it contains a proof of unsatisfiability structured as an implication graph over the input variables. **McMillan-style Craig interpolation** extracts from that proof a compact propositional formula — the interpolant — that is implied by the antecedents, contradicts the consequents, and is expressed only in the variables shared between the two sides.

The orchestrator computes the interpolant from the refutation and then **independently re-certifies it by SAT** before reporting it as a lemma. The re-certification step matters: an interpolant derived from a buggy refutation is itself buggy, and a verification pipeline that trusts an unverified interpolant is just propagating the upstream error. The independent check closes the loop.

## IC3 / PDR-Lite Builds A Frame Sequence Incrementally

For properties where k-induction stalls — typical for designs with deep reachable state spaces — the orchestrator falls back to an **IC3/PDR-lite frame loop**. IC3 maintains a sequence of frames `F_0, F_1, ..., F_k` where each frame over-approximates the set of states reachable in at most that many steps, and each frame is required to be a subset of the previous one. The frame loop blocks predecessors of bad states by adding clauses — "predecessor cubes" — that prevent the bad transition from being reachable.

The "lite" suffix is honest: this is the IC3 algorithm with the predecessor-blocking core, not the full Bradley-Manna-Sipma IC3 with ternary simulation and generalization heuristics. It handles a meaningful class of industrial properties, and it runs in the browser, which is the right tradeoff for a teaching and quick-check tool.

## When To Reach For This Stack And When Not To

The orchestrator is the right tool for **sanity checks, teaching, prototyping, and CI gates on small-to-medium bit-vector properties**. The bit-vector widths are bounded (Tseitin encoding explodes past a few hundred bits), the front-end theories are limited to `QF_BV` plus Bool, and the proof techniques are the textbook algorithms rather than the latest research. When the property you need to check involves arrays, floating-point arithmetic, or nonlinear integer arithmetic, you need a real SMT solver with the matching theory support.

For the day-to-day "is this obviously broken?" question — is this FIFO's full/empty logic sound, does this arbiter grant at most one requester, does this counter wrap correctly — the orchestrator answers in seconds without any infrastructure. That is what it's for. Reach for cvc5, Z3, or a commercial model checker when the answer to the obvious question needs to hold against a real industrial design.

## Pairing The Orchestrator With The Rest Of The Stack

The orchestrator slots into a larger verification pipeline as the **first gate**, not the final authority. Generate a property in your design's native format, compile it to SMT-LIB 2.7, push it through the orchestrator, and let the result route the design to either a quick-fix iteration or a heavier proof session. The orchestrator's counterexample-witness format is a useful input to a follow-up debugging session even when the final proof goes through a different tool.

For engineers who are still learning the formal-verification landscape, the orchestrator is also a teaching tool — you can step through BMC, k-induction, Craig interpolation, and IC3 on the same property and watch the SAT core handle each. The browser constraint forces the implementations to be lean, which makes the algorithmic decisions legible. Compare the same property across the four modes and the tradeoffs become concrete: BMC finds the counterexample in one round, k-induction proves the lemma in two, interpolation re-uses the refutation for a compact invariant, IC3 builds the frame sequence one cube at a time.

The complete input-to-certificate path lives at [elysiatools.com](https://elysiatools.com/en/tools). For the broader verification-and-reasoning category, the [Elysia Tools hub](https://elysiatools.com/en/tools) lists the related tooling — proof checkers, model visualizers, and the smaller dedicated solvers that cover the cases the orchestrator's four-mode stack leaves to a specialist tool.
