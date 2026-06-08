---
title: Why Every US Social Security Number Has Three Forbidden Numbers Hidden Inside
description: "The first three digits of a US Social Security Number carry a 90-year-old census code. Today, that code is more about what it excludes than what it means — and the rules are weirder than most engineers assume."
tags: ssn, validation, regex, kyc, format-check, government-id, us-government, identity
---

## Why This Matters

A friend in HR once asked me, "We just plugged in `^\d{3}-?\d{2}-?\d{4}$`. What else is there?" The answer is: about 90 years of edge cases the SSA has never bothered to publish as a single spec, scattered across a 1936 census code, a 1940s wallet-card scandal, and a 2011 randomization switch. Format validation for US Social Security Numbers looks trivial until you write the regex, and then it gets interesting in a hurry.

But the format rules didn't disappear. They inverted. The area number is now defined more by what it **can't** be than by what it means. A US SSN validator that only checks for `^\d{3}-\d{2}-\d{4}$` will pass `000-12-3456` and `666-12-3456` — both of which the SSA has explicitly reserved or excluded. Most in-house regex patterns quietly accept numbers the SSA has guaranteed will never be issued.

That gap is the story. Format validation isn't "9 digits and 2 dashes." It's a 90-year-old exclusion list, a forbidden **078-05-1120** that appears in every wallet in America, and a post-2011 randomization that broke the only mapping the number ever had. Any team that writes "validate US SSN" without understanding those rules ships a checker that approves numbers the SSA will reject in production.

You can explore the [US SSN Validator on Elysia Tools](https://elysiatools.com/en/tools/us-ssn-validator) to see the full set of constraints — area, group, and serial — checked in one pass.

## The AAA-GG-SSSS Structure

A US SSN is three numeric fields: **AAA-GG-SSSS** — area, group, serial. None of them may be all zeros, but each carries a different exclusion list.

The **area number** (AAA) used to encode the state of issuance. After 2011 randomization, the SSA keeps three hard exclusions on this field: it can never be `000`, never be `666` (reserved — and culturally conspicuous), and never be `900–999` (the range used for **ITINs**, the Individual Taxpayer Identification Number issued to people who aren't eligible for an SSN but need to file US taxes). The combined "valid" area range is therefore **001–665 and 667–899**, with 9-digit anchors reserved by the IRS rather than the SSA.

The **group number** (GG) used to encode a sequence within an area. Two rules: it can never be `00` (which would leave the middle two digits as zeros in many legacy systems), and — in pre-randomization data — odd groups were issued before even groups. After 2011, both rules still apply, but the sequence is no longer geographical.

The **serial number** (SSSS) is the simplest. It can be `0001` through `9999` within its group, with the only exclusion being `0000`. That's a generous range, and most validators get this one right.

A working regex looks like `^(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}$` — three negative lookaheads, each enforcing one of the rules above. It's 49 characters long and covers every constraint the SSA publishes publicly. It's also longer than most engineers expect, which is why simpler patterns ship by accident.

[Try the full validator yourself](https://elysiatools.com/en/tools/us-ssn-validator) to see how the exclusion layers interact on edge cases like `000-12-3456` or `900-45-6789`.

## The 078-05-1120 Story

If you've ever seen a sample Social Security Number in a textbook, a sample form, a default config file, or a test fixture, it was almost certainly `078-05-1120`. That number was the **real SSN of Mrs. Hilda Schrader Whitcher**, an office worker at a wallet manufacturer in New Hampshire, whose employer printed her number on tens of thousands of wallet-card inserts distributed to bank customers as promotional samples in the 1940s. By the time the SSA realized the leak, the number was already in millions of pockets.

The number itself is technically well-formed. The area `078` is valid. The group `05` is valid. The serial `1120` is valid. It passes every structural check. But the SSA has effectively marked it as "used" forever — the IRS, banks, and credit bureaus all flag it as a placeholder. A validator that returns "valid format" on `078-05-1120` is, in practice, returning wrong information, because real-world systems will reject it downstream.

This is the trap with format validation in general: **structural validity and issuance validity are not the same thing.** A number can pass the regex, pass the area rules, pass the group and serial rules, and still be a number the SSA will never assign to a real person. A trustworthy validator should at minimum flag the well-known placeholder.

## What 2011 Broke

Before June 2011, you could sometimes guess where someone was issued their SSN by the area number. The 213 area meant Southern California. The 040 meant New York. The 700 range meant the railroad board. Employers, debt collectors, and identity thieves all used that mapping. The **Social Security Number itself was never supposed to be a public ID**, but the geographical pattern was leaking location data through the front door.

The fix was randomization. New SSNs since 2011 have a random area number drawn from the **001–665 and 667–899** pool, a random non-`00` group, and a random non-`0000` serial. The total addressable space is roughly **900 million × 99 × 9999 ≈ 890 billion** possible numbers, of which the SSA issues a small fraction each year (about 5–6 million new SSNs annually in the 2010s, dropping since).

For validators, this is mostly good news. The "no 000, no 666, no 900–999" rule is now a hard format constraint, not a soft heuristic. The "group cannot be 00" rule is the same. But it also means that **historical data is no longer consistent with new data**: an SSN issued in 1995 in California might have an area number that overlaps with one issued in 2024 in Florida. A validator that tries to be too clever — flagging "this looks like a 1990s California number" — will produce false negatives on modern input.

## Beyond the Regex: Real KYC Pipelines

Format validation is the cheapest layer of identity verification, and the most limited. A real KYC pipeline for a US financial product does at least four things on top of format checking:

1. **Format validation** — the regex above. Catches typos, transcription errors, and obvious garbage.
2. **Date-of-birth cross-check** — the SSA's records link SSNs to birth dates. The credit bureaus maintain this. A valid format on a number issued in 1980 doesn't match a 2005 birth date.
3. **Death Master File check** — the SSA publishes a public list of deceased individuals' SSNs (the "Death Master File"). Format alone will happily pass an SSN whose owner died in 1998.
4. **Knowledge-based authentication** — out-of-wallet questions: which of these addresses did you live at, which of these cars did you finance. Format is unrelated.

For a payroll or HR system, format validation is enough to catch the most common data-entry errors and reject numbers that look like placeholders. For credit, banking, or healthcare, format is a 1-second check at the front door of a much deeper pipeline. Treating the two as interchangeable is a common engineering mistake.

A free online tool like the [Elysia Tools SSN Validator](https://elysiatools.com/en/tools/us-ssn-validator) is the right scope for the format layer: it tells you "this is structurally valid per the SSA's current public rules, and it's not a known placeholder." It is the wrong tool for "is this person who they say they are." Conflating those two questions is how identity systems get breached.

## The Engineering Mistake That Ships

The most common SSN validator in production is a regex like `^\d{3}-?\d{2}-?\d{4}$`. It checks digit count and optional dashes. It does not check the area exclusions, does not check the group exclusion, does not check the serial exclusion, and certainly does not flag `078-05-1120`. It will accept `000-00-0000` as a valid SSN. It will accept `666-00-0000`. It will accept `900-12-3456` — an ITIN range, not a Social Security Number at all.

The cost of this mistake is not catastrophic in the moment — the data flows into the system, gets stored, and gets cleaned up later. The cost compounds when downstream systems — tax filing, credit reporting, healthcare eligibility — start treating structurally-valid-but-impossible numbers as real. A W-2 issued to SSN `000-00-0000` is a paper-trail problem that takes months to untangle. A loan application filed under an ITIN-as-SSN is a regulatory problem.

The fix is one additional negative lookahead. Three of them, total. None of them is hard. The engineering mistake isn't technical — it's the assumption that "9 digits and 2 dashes" is the whole format.

## The Tool, In Practice

The [US SSN Validator on Elysia Tools](https://elysiatools.com/en/tools/us-ssn-validator) implements all three area exclusions (`000`, `666`, `900–999`), the group exclusion (`00`), and the serial exclusion (`0000`). It flags `078-05-1120` as a known placeholder. It returns a structured result showing which rule passed and which failed, so you can tell at a glance whether the failure was a typo or a structurally-impossible number. For an HR data-entry form, a customer onboarding flow, or a research dataset that needs to flag "this looks fake," that level of detail is the difference between catching errors at the source and cleaning them out downstream.

For something deeper than format — actual identity verification — the SSN validator is the first line, not the answer. The structure tells you the number is shaped right. The next four checks force you to ask whether the person exists, whether they're alive, whether the name and date of birth line up, and whether they've been flagged for fraud. None of those questions can be answered by a 9-digit regex, and the right tools make that boundary explicit.

## The Three-Layer Format

A US SSN carries three layers, and most validators check only the first. The **structural layer** is `^\d{3}-?\d{2}-?\d{4}$` — nine digits, two optional dashes. The **exclusion layer** is the rules the SSA publishes: area not in `000`, `666`, or `900–999`; group not `00`; serial not `0000`; and the well-known `078-05-1120` flagged as a wallet-card placeholder. The **randomization layer** is the post-2011 guarantee: new numbers carry no state-of-region information, so any validator that tries to "decode" the area number is reading a map that no longer exists. A spell-checker for numbers catches typos. A structural linter knows the SSA's grammar well enough to flag words that will never appear in the official dictionary. The 890-billion-number addressable space is mostly empty, and the right validator refuses to call the empty corners valid. The interesting work in US SSN validation isn't counting digits. It's knowing which numbers the government will never, ever issue — and the next question, the one every compliance team eventually has to answer, is whether your downstream system can tell the difference between a valid format and a real person. Format is where you start. It is not where you stop. Explore more validators in the [Elysia Tools collection](https://elysiatools.com/en/tools) if you're building a full identity-verification stack — the SSN check is the entry point, not the answer.
