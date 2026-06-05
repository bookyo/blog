---
title: One Regex Pattern, 4 Days of Downtime
description: "Catastrophic backtracking turned a 14-character regex into a 100,000% CPU spike. Here is how to spot the patterns before they hit production."
tags: regex, security, performance
slug: redos-regex-scanner
---

The regex engine does not warn you. It accepts the pattern, returns true or false, and walks away. The damage is not in the answer; it is in the time it took to compute it. A 14-character pattern held Cloudflare's status pipeline hostage for ninety minutes in 2019. A validation regex at Stack Overflow triggered a decade of subtle input lag. The lesson is the same in every case: regex that runs on untrusted input is a code path you have not load-tested, and most teams never do. The patterns are not exotic. They are the kind you and I have written on a Tuesday afternoon: `(a+)+$`, `^(\w+\s?)*$`, a tidy alternation inside a quantified group. The fix is also not exotic. You need a scanner that names the shape, ranks the risk, and gives you a rewrite you can paste back into your editor.

A single line of JavaScript, 14 characters long, took down a piece of Cloudflare's edge logic in 2019. The pattern looked like every other validation regex on the codebase: a tidy alternation, a quantifier, an anchor. It passed code review. It passed the unit tests. It passed the staging environment. Then, on a Tuesday afternoon, someone entered a string that was one character away from a match, and the regex engine entered a state space it could not escape. The CPU on the affected node climbed from 4% to 100% and stayed there for ninety minutes.

The pattern was not malicious. The developer was not careless. The shape of the pattern was simply something the engine had been quietly afraid of, and nobody had asked the right question: can a near-miss input make this loop?

That question is what a ReDoS scanner is built to answer. The tool at [Elysia Tools](https://elysiatools.com/en/tools/redos-regex-scanner) is one of the clearer ones I have used: you paste patterns in, it runs a static shape check, generates near-miss attack strings, simulates them against the engine, and returns a risk score, a level, and a safer rewrite. This article is about the shape of the problem, the heuristics that catch it, and what the rewrite actually looks like.

## The Three Patterns That Keep Biting Engineers

Across the postmortems I have read, three shapes account for the majority of catastrophic backtracking. None of them look dangerous in isolation. Each one becomes dangerous when combined with a specific kind of input.

The first is the **nested quantifier**: `(a+)+$`. The outer `+` says "one or more of the inner group." The inner `+` says "one or more `a`." When the input is `aaaaaaaab`, the engine is forced to try every possible split of the `a`s between the two quantifiers, and there are exponentially many. This is the canonical example, and it is in every regex safety talk. It is also the one I have seen in production most often, because it shows up in patterns that try to validate a sequence of repeated tokens.

The second is the **alternation inside a repeated group**: `(a|a)+$` or `^(\w+\s?)*$`. The alternation forces the engine to consider two paths for each character. Combined with repetition, the number of paths explodes. The Cloudflare 2019 incident was this shape, dressed up with a few more pipes.

The third is the **greedy-wildcard sandwich**: `.*foo.*bar.*` and its cousins. Two greedy wildcards, separated by a literal, are enough to force the engine to backtrack across the whole string for every near-miss of the literal. A pattern like `.*error.*` against a long log line that never contains the word error will, given enough input length, melt a CPU.

The reason these patterns survive code review is that they pass the tests. The test inputs are short and clean. The dangerous inputs are long, repetitive, and slightly off. A regex that takes 0.2 milliseconds on `aaaa` can take 200 milliseconds on `aaaaa`. The ratio is the thing.

## How the Scanner Actually Works

The Elysia Tools scanner combines two passes. The first is a static check, and it is the cheap one. It walks the pattern and looks for the three shapes above, plus a few other tells: a `(a+)+`-style nested quantifier, multiple greedy `.*` or `.+` in the same pattern, alternation inside a quantified group, and unanchored patterns that do not begin with `^` or end with `$`. Each shape contributes a weight to a risk score.

The second pass is the expensive one, and it is where the tool earns its keep. It generates near-miss attack strings — repetitions of a character the pattern cares about, followed by a single mismatched character — and runs the actual `RegExp` against them, several times, measuring the worst-case execution time. If a probe exceeds 40 milliseconds, the scanner marks the pattern as `benchmarkTimedOut` and stops probing. This matters because running the obvious dangerous patterns for too long would freeze the process running the scanner, which would defeat the purpose of having a scanner in the first place.

The output is a per-pattern report: a risk score from 0 to 100, a level (`safe`, `watch`, `high`, `critical`), a list of static findings, the worst measured execution time, a preview of the near-miss input that triggered the worst case, and a safer rewrite. For the canonical example `(a+)+$`, the rewrite is "use explicit upper bounds, atomic grouping, or a more specific character class" — which is, in practice, the right advice.

## Reading a Real Report

Suppose I paste two patterns into the tool. The first is the canonical `(a+)+$`, with no flags, a max evil-input length of 32, and 200 simulation runs. The second is `^\d{3}-\d{2}-\d{4}$`, the familiar US Social Security number shape.

For the first pattern, the static check fires on the nested-quantifier signature, adds 40 to the score, and adds 20 more for the unanchored alternation tell. The benchmark loop times out almost immediately, the `benchmarkTimedOut` flag is set, and the score lands in the 70s. The level is `high` or `critical`. The rewrite tells me to use atomic grouping or an upper bound.

For the second pattern, the static check finds nothing. The benchmark probes a string of `1`s followed by an `x`, finds that the engine rejects it in microseconds, and reports a worst-case time under a millisecond. The level is `safe`. The rewrite is the boilerplate "prefer anchored and specific subpatterns" line.

That contrast is the point. The tool does not just say "your regex might be slow." It says "this exact pattern, against this exact shape of input, takes 200 milliseconds, and here is the input that produced that number." The number is what gets pasted into the PR comment that finally gets the rewrite prioritized.

## Why Static Checks Alone Are Not Enough

You might reasonably ask: why bother with the benchmark loop if the static check already catches the three dangerous shapes? Two reasons.

The first is coverage. Static rules are written against the patterns we already know are dangerous. New shapes get discovered in postmortems, not in static-rule releases. The benchmark catches them at runtime, against real engine behavior, before they ship.

The second is calibration. A nested quantifier inside a `^...$` anchor against a 6-character input is not the same risk as the same shape against a 200-character input. Static rules cannot see the input. The benchmark can.

The trade-off the Elysia Tools scanner makes is conservative: if the static score is high enough, the benchmark skips the long probes entirely. This keeps the scanner from becoming the thing it is trying to protect you from. It also means a high static score is a strong signal on its own, and the absence of a benchmark number is not a clean bill of health — it is a refusal to test further, which is the next-worst thing.

## What the Rewrite Usually Looks Like

Three rewrites cover most of the cases I have seen. The first is **anchoring**: add `^` and `$` (or `\A` and `\z` in stricter engines) to fix the input range. The second is **replacing greedy quantifiers with specific character classes**: `.*` becomes `[^"]*` when you are inside a quoted string, because the engine no longer has to consider the whole document. The third is **atomic grouping**, which most JavaScript engines do not support natively but can be approximated with lookahead and a single possessive quantifier emulation.

For the canonical `(a+)+$`, the practical fix is usually to drop the outer quantifier: `a+$` does the same work in linear time. The engine never has to consider the second group because there is no second group. The pattern is shorter, faster, and easier to read. The cost is the loss of the "group of groups" abstraction, which is usually not load-bearing.

For the `^(\w+\s?)*$` shape, the rewrite is to think about what the pattern is actually trying to match. If it is trying to match a sequence of words separated by optional whitespace, the right fix is often a non-capturing group with an explicit upper bound on the word count, or a different token entirely. The pattern as written is asking the engine to enumerate splits, and the engine will happily do so until the input is long enough to make that enumeration expensive.

## Putting the Tool in Your Workflow

The scanner fits naturally in three places. The first is the pre-commit hook: paste the patterns from your codebase into the tool, sort the report by risk level, fix the critical and high ones. The second is the CI step: every pull request that touches a regex runs the scanner against the changed patterns and fails the build on a critical result. The third is the postmortem: when a service degrades, the question "could a regex be doing this?" gets asked earlier, and the scanner is the answer.

None of those placements are particularly novel. The reason I keep coming back to the tool is that the report is short, the rewrite is in the report, and the worst-case time is in the report. A security tool that tells you what to do next is rare. A security tool that tells you what to do next and gives you the input that demonstrated the problem is rarer.

## The Shape of a ReDoS Bug in One Sentence

A regex that requires the engine to enumerate paths on near-miss input is a regex that someone, eventually, will hit with the right kind of long string. The patterns are not exotic. The inputs are not exotic. The combination is the bug, and the combination is what a scanner is for.

If you write regex against untrusted input, the question is not whether you have a dangerous pattern. The question is which one, and how long until someone finds it. The [ReDoS scanner](https://elysiatools.com/en/tools/redos-regex-scanner) is a fast way to answer that question before someone else does. The [samples page](https://elysiatools.com/en/samples/redos-regex-scanner) has worked examples you can paste in to see the report shape on patterns you probably have in your codebase right now.

The next time you are about to merge a regex, the question to ask is not "does it match?" It is "what does it do on a string that almost matches, and how long is the longest string someone can send me?" The answer to the second question is what the scanner is for. The patterns are not going to get safer on their own.
