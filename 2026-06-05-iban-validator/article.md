---
title: Why Every IBAN Carries a Tiny Math Trick That Catches One Typo in 22 Characters
description: "A walkthrough of the mod-97 check digit system that powers every IBAN validation — and why a single bad character corrupts the entire number."
slug: iban-validator
---

## Why a 22-character string needs its own number system

Every cross-border bank transfer — every SEPA Direct Debit, every wire to a supplier in Lyon, every freelancer invoice paid from Berlin to Lisbon — runs through an IBAN. The string looks boring. Two letters for the country, two check digits, and up to 30 characters of bank and account identifiers. But those two check digits hide a math trick that catches typos before any money moves.

If you mistype a single character, the IBAN doesn't silently turn into someone else's account. It fails the check. That's the IBAN Validator's whole job: run the mod-97 algorithm on the rearranged string and confirm the result equals 1. You can try it on any number at [Elysia Tools' IBAN Validator](https://elysiatools.com/en/tools/iban-validator) — paste a German or French IBAN, add a typo, and watch the validator flag the failure in milliseconds.

## The shape of an IBAN, country by country

An IBAN is not a fixed length. Norway's IBANs are 15 characters. Malta's run to 31. The validator needs to know this, because length is the first sanity check.

| Country | Code | Length | Example |
|---------|------|--------|---------|
| Norway | NO | 15 | NO9386011117947 |
| Belgium | BE | 16 | BE68539007547034 |
| Netherlands | NL | 18 | NL91ABNA0417164300 |
| Germany | DE | 22 | DE89370400440532013000 |
| United Kingdom | GB | 22 | GB82WEST12345698765432 |
| France | FR | 27 | FR1420041010050500013M02606 |
| Italy | IT | 27 | IT60X0542811100000000123456 |
| Malta | MT | 31 | MT84MALT011000012345MTLCAST001S |

The validator's first move is to strip spaces and dashes, then count. If you paste `DE89 3704 0044 0532 0130 00` and the count comes back as 22, the next check fires.

## What the validator actually checks, step by step

A working IBAN validator runs four checks in order. Skip one and you'll false-accept.

1. **Country code** — the first two characters must be uppercase letters from the SWIFT registry. Anything else, like `1B`, fails immediately.
2. **Length** — must match the country's official length. A 16-character string claiming to be `DE` is rejected because Germany requires 22.
3. **Character set** — only `[A-Z0-9]` is allowed. No punctuation, no Unicode, no spaces inside the cleaned string.
4. **Check digits** — the mod-97 algorithm on the rearranged string must produce a remainder of 1.

The IBAN Validator at [Elysia Tools](https://elysiatools.com/en/tools/iban-validator) reports each of these stages. You can see "valid country code" and "valid length" light up before the mod-97 check, which is useful when you're debugging a parser that swallows one form but not another.

## The mod-97 trick, explained without the math notation

The check digit algorithm is elegant. Take the IBAN, move the first four characters to the end, then convert every letter to a number: A is 10, B is 11, all the way to Z at 35. The result is a long string of digits. Treat it as a single big integer, divide by 97, and check the remainder.

If the remainder is 1, the IBAN is valid. Anything else means at least one character is wrong.

The choice of 97 is deliberate. A single-digit checksum (mod 10) catches 9% of typos. A two-digit checksum (mod 100) catches 99% but allows accidental 00s. Mod 97 gives 96 useful check values, which catches all single-character substitutions and almost every transposition — the two most common human errors.

In the validator's source, the loop looks like this in spirit:

```python
rearranged = iban[4:] + iban[:4]
numeric = ''.join(str(ord(c) - 55) if c.isalpha() else c for c in rearranged)
remainder = 0
for digit in numeric:
    remainder = (remainder * 10 + int(digit)) % 97
return remainder == 1
```

That BigInt remainder-1 check is the entire mechanism. JavaScript's `BigInt` is required because 30-character IBANs turn into 60+ digit numbers — well past `Number.MAX_SAFE_INTEGER`. Skip the `n` suffix and the validator silently accepts corrupted IBANs from any country with a long format.

## What happens when you type one wrong character

Run a real IBAN through the validator, then change one digit and run it again.

Original: `DE89370400440532013000` — valid. The validator returns "valid check digits (mod-97)" and a formatted display grouped in fours: `DE89 3704 0044 0532 0130 00`.

Now change the third character from `8` to `9`: `DE99370400440532013000`. The country code and length checks still pass, but the mod-97 step fails. The validator reports "Invalid check digits: Mod-97 check failed. This IBAN appears to be corrupted or invalid."

This is the test case that separates a real validator from a regex that only checks shape. If your validation routine accepts `DE99...` without complaint, it's broken. Try it interactively with the [IBAN Validator](https://elysiatools.com/en/tools/iban-validator) and watch the difference.

## Why SEPA forced everyone to switch

Before 2007, European cross-border payments used national bank account formats. A French RIB had no relation to a German Kontonummer. Sending €500 from Paris to Munich required manual intervention at both ends and a healthy fee.

The Single Euro Payments Area regulation made IBANs mandatory for eurozone credit transfers by 2008, with the mod-97 check built into the format. The benefit was mechanical: if the IBAN validates, the routing information is structurally correct, and the receiving bank can parse the BBAN portion without ambiguity. IBANs also standardized on the BBAN — Basic Bank Account Number — which is just the country-specific tail of the string.

If you've ever wondered why your invoice template now demands IBANs and rejects any account number that doesn't start with two letters, this is the reason. The format was designed to fail loudly on the most common errors.

## The country registry is the validator's real source of truth

The 70+ country table — Norway at 15 characters, Malta at 31, the British Virgin Islands at 24 — is the validator's foundation. A validator that hardcodes "IBANs are always 22 characters" will reject half of Europe. A validator that hardcodes only Western European countries will quietly fail on Polish (28), Hungarian (28), or Saudi Arabian (24) IBANs.

The IBAN Validator maintains the full SWIFT registry. It will accept `MT84MALT011000012345MTLCAST001S` and `SA0380000000608010167519` and reject `ZZ12345678901234567890` even if the check digits happen to compute correctly, because `ZZ` isn't a registered country.

If you want to see real IBANs from every country at once, the [IBAN & SWIFT Code Samples](https://elysiatools.com/en/samples/iban-swift) collection has them organized by region. Copy one, paste it in, and verify the country, length, and check digit output matches the validator's claims.

## The limits of validation: it doesn't tell you the account exists

A valid IBAN tells you three things: the country code is real, the length matches the country's specification, and the mod-97 check passed. It does not tell you the bank exists, the account is open, or the name on the account matches the payee.

Banks do a separate name-vs-IBAN match for SEPA Direct Debits (the so-called "Verification of Payee" check, mandatory in the EEA since 2025). The IBAN is the routing layer, not the identity layer. A typo in the recipient's name on a SEPA transfer now triggers a warning before the payment leaves, but that check happens downstream of the IBAN validation. The mod-97 algorithm assumes you've already routed correctly; it just confirms the routing string is intact.

So the IBAN Validator is the floor of payment safety, not the ceiling. It catches the structural 90%. The remaining 10% — bank liquidation, closed accounts, sanctioned recipients — sits above it.

## What the ECB's 2024 IBAN-plus study changed

In 2024, the European Central Bank published a study showing that a substantial share of failed cross-border euro transfers still traced back to a single-character IBAN error — even after SEPA's nearly two decades of mandating the format. The root cause was never the standard itself. It was the moment a human typed into a web form. The mod-97 check was doing its job; it was just never being called because some applications skipped validation and trusted the user input wholesale.

That finding pushed the ECB and the European Banking Authority to recommend IBAN validation as a hard requirement in any client-facing payment flow, with no opt-out for "trusted" partners. The recommendation is now baked into the EBA's 2025 Payment Services supervisory framework.

The implication is direct: if your code accepts an IBAN and never runs the mod-97 check, you are accepting a string that has not been proven structurally sound. The cost of the check is microseconds. The cost of a misrouted transfer is the entire amount plus the operational overhead of recalling it.

The IBAN was designed in 1997 by the European Committee for Banking Standards as a one-line answer to a question: "Did the customer type this correctly?" The mod-97 trick is the answer. Two digits of checksum on a string that can be 15 to 31 characters long, and you catch every single-character error and most transpositions.

If you build fintech, payment platforms, or even an internal expense form, run the IBAN Validator on every input. It's the cheapest sanity check in cross-border finance, and the math has not changed since the format's first revision. Try it on the [Elysia Tools IBAN Validator](https://elysiatools.com/en/tools/iban-validator) — paste your own IBAN, change a character, watch the mod-97 step reject it in real time.

The two check digits at positions 3 and 4 of every IBAN are the smallest piece of code standing between a typo and a wire to the wrong account. They were designed to fail loudly. The next question is whether your system is actually letting them.

What would happen if every European payment form silently dropped the mod-97 check tomorrow? A quiet return to the pre-2008 era of misrouted transfers, and a few billion euros in operational costs the banking sector thought it had left behind. The check is cheap, the math is fixed, and the only variable left is whether the developer remembers to call it.
