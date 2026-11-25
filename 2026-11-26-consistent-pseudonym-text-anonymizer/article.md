---
title: "Two Redactions, One Join: Why Masking Your Logs Breaks the Query"
---

Two engineers redact the same 40 MB log before it leaves the building. One replaces each email with a row of asterisks. The other replaces it with EMAIL_7, in all 4,318 places that address appears. Both files pass privacy review, but only one still answers the question that triggered the review: which account drove the 4,000 failed logins. I rebuilt the pipeline below to check that claim on the real code. Erasure is not the same operation as redaction, and the join is what separates them.

That difference is not a matter of taste. It is a property of the pipeline, and it is decided by three things that are easy to get wrong: the order of the passes, the normalization step, and which replacement mode you picked. The tool that gets this right is [Elysia Tools](https://elysiatools.com/en/tools/consistent-pseudonym-text-anonymizer), and its source is short enough to read in one sitting.

## Detection and rewriting are two separate passes

Consistency requires seeing the whole document before you change a single byte.

If you replace matches as you find them, each replacement shifts the offset of all later bytes. A 12-character email becomes a 7-character label, and now each recorded start position after it is off by five. The fix is to collect all matches first, then rewrite from the end backwards.

The decoder does exactly that. Findings are sorted in descending offset order and spliced into the output one at a time, so no earlier edit can invalidate a later position. In practice the expensive part is not the detection regexes. It is remembering that detection and rewriting are separate phases at all.

There is a hard limit worth knowing before you plan a chunking strategy. The tool accepts up to 200,000 characters per call. Anything larger has to be split, and the split has consequences covered further down.

## Consistency is won in normalization, not in the replacement

Two addresses that look different usually are the same person, and the tool decides that before it ever picks a label.

Each detected value is normalized into a comparison key. Emails, API keys and passport numbers are lowercased. Phone numbers, card numbers, national IDs and IPv4 addresses are stripped down to digits. Names are whitespace-collapsed and lowercased. The mapping table is then keyed on type plus normalized value.

I measured the effect on one line holding an address in mixed case twice, plus a phone number written two ways:

```
Alice@Example.com | phone +1 415-555-0132 | ALICE@EXAMPLE.COM | phone 14155550132
```

Four matches. Two entities: `EMAIL_1 | phone PHONE_1 | EMAIL_1 | phone PHONE_1`. Normalization cut the count in half before any label was generated, because the dotted formatting and the case difference never survive it.

For example, the same rule keeps a card number stable whether it arrives with spaces or dashes. That is the join being won, and it happens several functions before anything is substituted. The mapping table records an observed occurrence count per entity, which is how you check the fold worked without reading the diff.

## When two scanners claim the same bytes

Overlaps are resolved by position, not by how specific the detector is.

Matches are sorted by start offset, longest first at the same start, and then a match is kept only if it begins at or after the end of the previous kept match. The rule is simple: earliest match wins, and a later detector never overrides an earlier one.

Here is the case where that gets uncomfortable. An 18-digit national ID number that happens to satisfy the Luhn check is reported as a credit card, with the label CREDIT_CARD_1. Both spans are identical, so the tie is broken by scanner registration order, and the credit-card scanner runs before the national-ID scanner.

The redaction is still safe. The label is wrong, and a reviewer who trusts it will report a card count that is off by one. If your reviewer is counting card numbers in the output, they will count an ID document, and the number will be plausible enough that nobody queries it.

## Three replacement modes and the audience each one serves

The mode is not cosmetic. It decides whether the output can be joined to anything else.

<strong>Stable labels.</strong> `EMAIL_1`, `PHONE_2`, numbered per entity type in order of first appearance. Readable, stable inside one document, and the right choice when a human has to review the result against the original.

<strong>Synthetic placeholders.</strong> A lowercase type prefix plus 10 hexadecimal characters derived from a seeded SHA-256 digest, so the output still looks like a field value. Ten hex characters is 40 bits of digest.

<strong>Deterministic hashes.</strong> `[EMAIL:0a2c5cd81144]` for alice@example.com under the default seed. Twelve hex characters, 48 bits, marked as a pseudonym, not a bare value.

The digest covers seed, type and normalized value: 16 hex characters, sliced again per mode. That is the whole mechanism, and it is short enough to prove by reimplementation.

## Stable labels stop being stable at the second document

Numbering follows first appearance. That ordering is document-local, and it quietly breaks any join you attempt across two files.

I ran two documents through label mode. The first was `bob@x.com then alice@y.com`; the second was the same two addresses in reversed order. Both outputs read `EMAIL_1 then EMAIL_2`.

So bob is EMAIL_1 in one file and EMAIL_2 in the other. Any join on that column returns rows, not an error. I measured that on two seven-word documents, and the reported unique count was identical in both runs. Worse, it returns rows that look correct, which is the failure mode that costs a day of debugging instead of five minutes.

Hash mode does not have this problem. Bob keeps `[EMAIL:7da15274eea2]` in both files, and alice keeps `[EMAIL:6bf361a73f9c]`, because the pseudonym depends on the value and the seed, never on position.

The consequence is direct. Label mode is a single-document tool. Hash mode is a corpus tool. And a 40 MB log split into 200,000-character chunks is a corpus, so chunking with labels reintroduces the same defect at each boundary.

## What a consistent hash leaks instead

Consistency is itself a disclosure, and the honest way to ship it is to name what it discloses.

Equal pseudonyms mean equal originals, which is the property the whole file is built on. Anyone holding the file learns that these 900 rows are one customer, without learning who. Frequency is preserved too: the entity with the most occurrences in your output is the entity with the most occurrences in the input, which for a support log is usually the noisiest customer and sometimes the most interesting one.

Truncation adds a collision risk that is easy to bound. At 48 bits and 10,000 entities, the probability of at least one collision is about 1.8 in 10 million, measured against the binomial approximation. At 40 bits in synthetic mode it is about 4.5 in 100,000, still small, and worth knowing before you claim the mapping is one to one.

The seed is the real secret: 16 hex characters of digest do not help without it. The default is `elysia`, and according to the source the same address hashes differently when you change it: `elysia` gives `[EMAIL:0a2c5cd81144]`, `demo` gives `[EMAIL:c37b04610155]`. Against a public default seed, an attacker who suspects an address can hash candidates until one matches. Set your own seed, and store it the way you store a key, because that is what it is.

The mapping export deserves the same care. It is off by default, and when you turn it on the result carries the original plaintext beside each pseudonym. That file is the only thing that undoes the whole exercise, so it should never travel with the output.

## The detectors that will miss your hardest case

Pattern matching is a floor, not a ceiling, and the tool reports that limit in a field called `warnings`.

Person names are only extracted after a label, in the form `name: Alice`, plus the Chinese equivalent of that same label word. There is no named-entity model in the pipeline, so a name mentioned in prose stays in prose. Passport detection looks for 8 to 9 alphanumeric tokens that contain at least one letter and one digit, which will find machine-readable passport numbers and will also find a few things that are not passports.

The response includes a heuristic flag and a warning that pattern-based detection may miss context-dependent personal data. For instance, a customer's name inside a free-text support note is exactly the case that survives, and it is exactly the case that gets copied into a bug report.

Read that warning as a design statement. This tool removes the identifiers you can enumerate. It does not decide what identifying means for your data.

## A pre-flight list before the log leaves the building

Five checks cover the failure modes above.

Choose hash mode whenever the output will be joined, aggregated, or chunked, and accept that the labels are ugly. Set a non-default seed and record it outside the export. Leave the mapping disabled unless a reviewer needs it for a single sitting. Grep the result for an at-sign and for runs of 13 or more digits before you call it clean. And if you split the input, split it in hash mode, because labels renumber at each boundary.

If you want to check any of this against your own text, [run it here](https://elysiatools.com/en/tools/consistent-pseudonym-text-anonymizer) and compare the mapping tab to the output. The whole run happens in the tool, with no model call and no upload to a third party, which is the other half of why this class of tool is worth keeping close.

The privacy review asks whether the file is safe to share. The engineering question is whether it is still useful, and those two answers come from the same three decisions: how values are normalized, which mode you picked, and whether the seed is yours.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

I spent years grading anonymizers by how much they hid. The better question is what they keep, and then what the kept thing still tells you. A stable label is a promise that two rows are the same person. That promise is why the export is useful and why it is dangerous. In the end, the setting that matters is the seed: yours, not the default, and not shipped alongside the file.
