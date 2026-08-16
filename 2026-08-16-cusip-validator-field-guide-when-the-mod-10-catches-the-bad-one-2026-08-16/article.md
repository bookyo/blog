**Every North American stock, bond, and ETF ticker rides on a nine-character code, and the last digit is a checksum that quietly rejects typos and fat-fingered transcriptions.** A CUSIP, just like an ISBN or an IBAN, is built to be self-checking — and the [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) runs the mod-10 pass in one shot, including the issuer-number breakdown you usually only get from a paid feed.

## Why a nine-character code still matters in 2026

Stock tickers come and go, but the CUSIP does not. CUSIPs flow through broker reconciliation files, mutual fund prospectuses, IRS filings, the DTCC clearing system, and almost every fixed-income trade ticket. Most retail brokerages never display them, but the back offices of every custodian rely on them every day. When two CUSIPs disagree by a single character, the entire reconciliation pipeline can fail.

The format was introduced in 1969 by the American Bankers Association and is now maintained by FactSet (formerly Standard & Poor's) and CUSIP Global Services. Every identifier encodes three pieces of information in nine base-36 characters:

- **Issuer number (6 chars).** Identifies the company or fund. The first three digits are an issuer-category prefix assigned by the ABA; the next three identify the specific entity within that category.
- **Issue number (2 chars).** Identifies a particular class of security — common stock, preferred, a specific bond series, a fund share class.
- **Check digit (1 char).** A mod-10 sum over the first eight characters, using a positional weighting that doubles every other digit starting from the right. The check digit is the only piece a validator can compute without an issuer database.

The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) reports all three pieces on a successful check and flags exactly which slice went wrong on a failure.

## The four operations the tool exposes

The CUSIP validation workflow fits one of four shapes, and a tool that does all four saves you from writing the mod-10 routine yourself every time:

- **Validate a CUSIP.** Paste the nine characters with or without dashes/spaces; get a pass/fail, the issuer-number breakdown, and a flag for the obsolete CUSIP-6/NSIN forms.
- **Compute the check digit.** Enter the first eight characters and receive the missing check digit. Useful when generating a new CUSIP for a test fixture or a CSV import.
- **Validate the issuer portion.** Pre-flight the six-digit issuer prefix against the structure rules (length, character set, category-prefix shape) without computing the check digit — useful for batch-import validation where you only have the issuer number.
- **Distinguish CUSIP, CUSIP-6, and NSIN.** Some inputs are truncated issuer-only identifiers; the tool reports which form you actually have so downstream code does not assume nine characters.

For an overview of how the four operations slot into a reconciliation pipeline, see the [CUSIP Validator tool page](https://elysiatools.com/en/tools/cusip-validator).

## The check-digit algorithm in one paragraph

The CUSIP mod-10 routine is not the same as a credit-card mod-10 or an ISBN-10 mod-11. The standard works like this:

- Take the first eight characters. Each is a base-36 digit: `0`-`9` for the numerals, then `A`-`Z` mapped to values 10-35.
- From the RIGHTMOST of the eight (position 8), apply a multiplier: 2 to even positions (2, 4, 6, 8), 1 to odd positions (1, 3, 5, 7). Wait — it is the reverse: position 8 gets multiplier 2, position 7 gets 1, position 6 gets 2, etc., counting from the right of the eight.
- For each multiplied value: if the result is two digits (because 10 or higher), add the two digits together to reduce it to a single digit. So `24` becomes `2 + 4 = 6`.
- Sum all eight reduced values. The check digit is `(10 - (sum mod 10)) mod 10`. The full nine-character CUSIP is the eight characters + this check digit.

Two consequences trip up home-grown implementations. First, the alphabet mapping is base-36, not base-26 plus digits — `A` is 10, `B` is 11, ..., `Z` is 35. Second, the doubled-digit reduction (`24 -> 6`) is the same rule as Luhn, but the positional weighting starts from the right of the eight, not the left of the nine. The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) implements the full algorithm and accepts the full base-36 alphabet including the `*`, `@`, and `#` characters CUSIP allows in the issue-number slot.

## Real examples on common input shapes

A few inputs that show up constantly in reconciliation work:

<ul>
<li><strong>Apple Inc. (AAPL) common stock.</strong> <code>037833100</code>. The first three digits <code>037</code> are Apple’s issuer-category prefix; <code>833</code> is the within-category identifier; <code>100</code> is the issue number for common stock. Run through the validator: passes, check digit <code>0</code>, base-36 alphabet clean.</li>
<li><strong>Microsoft Corp. (MSFT) common stock.</strong> <code>594918104</code>. Same structure; the validator will produce the check digit <code>4</code> if you feed it only the first eight characters <code>59491810</code>.</li>
<li><strong>CUSIP with dashes.</strong> <code>037833-DT-0</code> (a fictional example). Real CUSIPs often arrive dashed in legacy data feeds. The validator strips the dashes before computing the check digit — a common silent failure in older reconciliation code that does not.</li>
</ul>

For more input-output pairs and edge cases, browse the [samples gallery](https://elysiatools.com/en/samples).

## What the validator catches (and what it does not)

The validator catches three classes of problem and explicitly does not catch a fourth:

- **Wrong check digit.** The most common error in any reconciliation file — a single character transcription mistake in positions 1-8. The validator computes the expected check digit and reports which position disagrees.
- **Forbidden characters outside the base-36 alphabet plus the CUSIP-allowed <code>*</code>, <code>@</code>, <code>#</code> characters in the issue-number slot.** A CUSIP with a lowercase letter or a punctuation mark other than the three allowed is rejected outright.
- **Wrong length.** A six-character issuer-only identifier is reported as such, not as a failed nine-character CUSIP.
- **Semantic problems the validator does NOT catch.** The validator cannot tell you that the CUSIP refers to a delisted security, that the issue number was retired last quarter, or that the issuer was acquired three years ago. Treat validator-pass output as "well-formed" rather than "still active." For real-time status checks, the [EIN Validator](https://elysiatools.com/en/tools/ein-validator) covers US tax identifiers; the [IBAN Validator](https://elysiatools.com/en/tools/iban-validator) covers international bank account numbers; the [ISBN Validator](https://elysiatools.com/en/tools/isbn-validator) and [Credit Card Validator](https://elysiatools.com/en/tools/credit-card-validator) cover the same self-checking pattern for books and payment cards.

## Common mistakes when hand-rolling the CUSIP check

Four patterns look like they work but quietly fail on real reconciliation traffic:

1. **Using Luhn (mod-10) weighting from the left.** Luhn is the credit-card check and looks similar, but Luhn doubles the second-from-right digit, while CUSIP doubles the rightmost of the eight unchecked characters. Mixing them up is a one-line bug that produces a validator that passes every input you test it on.
2. **Forgetting the doubled-digit reduction.** Without reducing `12 -> 3`, `24 -> 6`, the sum comes out too high and the check digit is wrong on every CUSIP that contains a letter.
3. **Treating the issue-number slot as plain alphanumeric.** CUSIP allows `*`, `@`, `#` only in positions 7-8 of the issue slot; rejecting them turns valid CUSIPs into false negatives. Conversely, accepting lowercase letters is wrong.
4. **Not tolerating dashes, spaces, or omitted leading zeros.** Real CSV exports from custodian systems format CUSIPs in at least four different ways. A validator that requires exactly nine characters with no separators will silently break every imported file.

The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) implements all four corrections in one pass and runs the check entirely in the browser.

## Where CUSIP sits alongside other self-checking identifiers

Five families of self-checking identifier show up in financial and reference data, and a tooling stack that knows the differences saves you a debugging session every quarter:

<ul>
<li><strong>CUSIP</strong> covers North American stocks and bonds. The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) is the canonical entry point for individual checks; the [IBAN &amp; SWIFT Validator](https://elysiatools.com/en/tools/iban-swift-validator) covers international bank identifiers.</li>
<li><strong>ISIN</strong> is a 12-character wrapper around a CUSIP (or a non-US identifier), prefixed by a two-letter country code and validated with the same mod-10 over the last 11 characters — including the embedded CUSIP. The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) returns the CUSIP slice on a well-formed ISIN so a downstream ISIN check does not have to redo the work.</li>
<li><strong>EIN</strong> is the IRS Employer Identification Number, formatted `XX-XXXXXXX`. The [EIN Validator](https://elysiatools.com/en/tools/ein-validator) checks format only — the IRS does not publish a checksum for EINs.</li>
<li><strong>Credit card numbers</strong> (PAN) are mod-10 validated by the Luhn algorithm; the [Credit Card Validator](https://elysiatools.com/en/tools/credit-card-validator) is a separate tool because Luhn’s weighting is reversed from CUSIP’s.</li>
<li><strong>ISBN-10 and ISBN-13</strong> are book identifiers with their own mod-11 (ISBN-10) and mod-10-with-weights-1-and-3 (ISBN-13) routines; the [ISBN Validator](https://elysiatools.com/en/tools/isbn-validator) handles both.</li>
</ul>

For a broader inventory of identifier-format tooling, the [Validation hub](https://elysiatools.com/en/tools/validation) lists the rest of the family.

## A 30-second sanity check before shipping

Run this checklist on any CUSIP-handling code before it leaves your system:

1. The input is normalized to nine characters before any check-digit math runs — dashes and leading-zero padding handled.
2. The base-36 alphabet mapping is correct: `A=10`, `B=11`, ..., `Z=35`, digits `0-9` unchanged.
3. The doubled-digit reduction is applied: `12 -> 3`, `24 -> 6`, not skipped.
4. The positional weighting starts from the right of the unchecked eight, not from the left of the nine.
5. The issue-number slot accepts `*`, `@`, `#` and rejects everything else outside the base-36 alphabet.
6. The output includes the issuer-number and issue-number breakdown so downstream code does not have to re-parse the string.

If any of those fail, you are looking at a Luhn-style check that was repurposed without the CUSIP-specific changes, or a parser that does not normalize separators. The [CUSIP Validator](https://elysiatools.com/en/tools/cusip-validator) catches all six classes on every input.

Explore more identifier-format tools at [elysiatools.com](https://elysiatools.com/en/tools), or browse the [samples gallery](https://elysiatools.com/en/samples) for input-output pairs across the family.
