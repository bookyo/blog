The cross-border payment hits your invoice queue at 4:47 AM on a Tuesday. The customer swears the IBAN is correct, your bank says the SWIFT is misrouted, and your finance team is going to spend the next ninety minutes pasting fragments into three different bank portals before anyone figures out whether the failure was a checksum, a country code, or a stray space. A single browser-side validator that runs both checks against the same input collapses that ninety-minute detective story into a four-second verdict.

## The Two Codes Look Similar and Behave Nothing Alike

`IBAN` and `SWIFT/BIC` are both bank identifiers, both look like uppercase alphanumeric strings, and both sit in the same invoice field on most ERP templates. That is where the similarity ends. An IBAN identifies an individual account; the SWIFT identifies the bank that holds that account. They are validated by entirely different algorithms, they have different length rules per country, and they are stored in different columns of every banking database that exists. A tool that only checks one of them will silently return "valid" on a string that cannot actually be sent anywhere.

This is the gap the [IBAN & SWIFT Validator](https://elysiatools.com/en/tools/iban-swift-validator) closes. The same input box accepts either format, the auto-detect path picks the right algorithm, and the output tells you which one you actually have. You can run a string through, copy the verdict, and move on.

## IBAN Validation Is mod-97, Not Length and Not Regex

The IBAN checksum is ISO 13616 mod-97. You move the first four characters to the end, convert each letter to a two-digit number (`A=10`, `B=11`, ... `Z=35`), treat the whole string as a big integer, and check that the remainder mod 97 equals 1. The country code, the two check digits, the BBAN, the total length — none of those are validated by the checksum alone. The checksum is what catches a single transposed digit. The length and country structure are what catch the deeper mistakes: an extra digit, a missing digit, or an Irish IBAN that was mangled into a German one.

A real validator has to enforce both layers, and the layers don't always agree. `GB82WEST12345698765432` passes mod-97 with a remainder of 1 and has the correct 22-character UK length; `GB82WEST12345698765433` fails mod-97 by exactly one digit; `GB82WEST1234569876543` has the right checksum but is one character short for a UK IBAN and would be rejected by any clearing system. A regex that only checks `\w{2}\d{2}\w+` accepts all three.

The validator's IBAN path runs the full check, including per-country length rules, so the third case above is caught at the length gate, not at the checksum gate. That distinction matters because it tells you *what to fix*: a checksum failure means a transcription error, a length failure means you are looking at a partial string.

## SWIFT Validation Is Eight or Eleven, Never Nine or Ten

The SWIFT/BIC code is structurally simpler than the IBAN but has its own quirks. The eight-character form is `BBBBCCLL` — four-letter bank code, two-letter country code, two-character location code. The eleven-character form appends a three-character branch code. Nine, ten, and twelve characters are all invalid. So is a SWIFT whose country code disagrees with the IBAN's country code, which the validator flags as a separate warning rather than a hard failure.

The common failure mode here is a SWIFT that passes the length check but encodes a defunct bank. SWIFT assigns and retires bank codes constantly; an eight-character code that was live in 2014 may have been re-issued to a different institution by 2026. A validator that only checks structure cannot catch this — you need an active-code directory. The validator returns a confidence flag and a recommendation to verify against your bank's published list whenever the structure passes but the code is not in any well-known directory.

## Country Codes Disagree and That Is the Bug You Are Hunting

The most expensive mistake in cross-border invoicing is a valid IBAN paired with a SWIFT whose country code does not match. The transfer will be accepted by your local bank, routed into the SWIFT network, and bounced by the receiving correspondent with a `BIC-COUNTRY-MISMATCH` error — usually three to five business days after submission, with the intermediary fees already deducted and non-refundable.

The validator surfaces this mismatch as a top-line warning before you hit submit. You see `IBAN country: DE`, `SWIFT country: FR`, and the red `country mismatch` flag at the top of the result panel. Paste the IBAN alone, you get a green check. Paste the SWIFT alone, you get a green check. Paste both, you get a red flag. This is the case the auto-detect path is designed for: a finance team that pastes whatever is in front of them and expects the tool to figure out what they actually meant.

## A Real Audit Pass Catches What Five Individual Validators Miss

A typical back-office audit runs every IBAN in your AR ledger through one checker, every SWIFT through another, every cross-reference through a third, and reconciles by hand. The [IBAN & SWIFT Validator](https://elysiatools.com/en/tools/iban-swift-validator) collapses that to one input box with both algorithms active, so a single paste performs the cross-check the audit was doing manually. For batch work you can run the tool inside a loop and pipe each row through the validator, then filter on the verdict column.

The [IBAN & SWIFT Codes by Country](https://elysiatools.com/en/samples/iban-swift) sample bundle gives you a known-good test set: real IBANs and SWIFTs from a dozen major jurisdictions, each one with a passing checksum and a known bank code. Run that bundle through your internal check first to confirm your downstream system agrees with the validator, then run your real AR ledger.

## Five Checksum and Format Rules That Catch Ninety Percent of Failures

Five rules, applied in order, catch the bulk of real-world IBAN and SWIFT failures. The validator runs all five as a single pipeline, but knowing the order helps you read the result.

1. **Strip spaces and hyphens first.** `GB82 WEST 1234 5698 7654 32` and `GB82WEST12345698765432` are the same IBAN. A validator that fails on whitespace is broken; a validator that silently strips it is correct.
2. **Uppercase everything.** Lowercase letters are valid inside an IBAN per the spec, but every clearing system uppercases before processing. Normalize at the input gate.
3. **Run mod-97 after the four-character rotation.** This is the only authoritative checksum for IBAN. If it fails, the IBAN is wrong; do not try to "fix" it by adjusting digits.
4. **Enforce per-country length.** UK is 22, Germany is 22, France is 27, Saudi Arabia is 24. There is no universal length.
5. **Cross-check country codes between IBAN and SWIFT.** A passing IBAN and a passing SWIFT can still be incompatible if their country codes disagree.

## Where Auto-Detect Breaks Down and You Have to Pick

The validator's auto-detect works on three signals in order: leading two characters are letters (likely IBAN country code), total length above 14 (likely IBAN), any character outside `[A-Z0-9]` (likely IBAN with formatting). If the input is exactly 8 or 11 uppercase characters with no leading letters that look like a country code, auto-detect picks SWIFT. If the input fails all three signals, you get a "could not auto-detect" verdict and the type selector becomes mandatory.

The two cases where auto-detect consistently picks wrong are: a SWIFT code whose first four letters happen to be a valid ISO country prefix (rare but real), and a German IBAN that was pasted without the leading `DE` because someone stripped the country code by mistake. Both cases are visible in the result panel as a low-confidence auto-detect and an explicit `please verify type` warning. Pick the type manually when you see that warning.

## Beyond Pass/Fail: What the Result Tells You to Do Next

A binary valid/invalid verdict is the minimum useful output. The validator returns five pieces of structured information on success: the detected type, the parsed country, the formatted canonical form (with spaces in the right places), the bank code or BBAN prefix for IBAN, and a confidence flag for SWIFT. On failure it returns the same five plus a `failure_stage` field that says whether the failure was at the format gate, the checksum gate, the length gate, or the country gate. That stage is what tells you what to fix — a format failure means a typo, a checksum failure means a transcription error, a length failure means a truncated string.

The structured output is the part that makes the tool scriptable. Pull the verdict, the country, and the failure_stage into your AR pipeline and you can route the failure into the right queue automatically. A format failure routes to data entry; a checksum failure routes to customer confirmation; a country mismatch routes to a human review queue.

The [IBAN & SWIFT Validator](https://elysiatools.com/en/tools/iban-swift-validator) is the difference between catching a routing error before submission and discovering it three business days later in a correspondent bank's bounce notice. Run every cross-border payment string through it once before you hit submit, and the 4:47 AM detective story stops happening. Explore more bank-code and routing tools at [elysiatools.com](https://elysiatools.com/en/tools).
