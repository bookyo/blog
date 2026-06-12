---
title: The Hidden Checksum That Catches Every Credit Card Typo Before Your Bank Ever Sees It
description: A 16-digit number carries a single-digit witness. The Luhn algorithm is the reason a fat-fingered purchase fails instantly instead of charging the wrong card.
---

The trick is older than the internet, older than magnetic stripes, older than the chip on your card. Hans Peter Luhn, an IBM engineer, filed the patent in 1960 — two years before the first credit card with a magnetic strip was even issued. He wasn't trying to secure anything. He was trying to make punch-card readers reject typos at the read station instead of corrupting payroll, inventory, and shipping manifests. The algorithm he sketched on a single page of an IBM technical disclosure bulletin became, almost by accident, the front line of fraud defense for a payments industry that didn't exist yet. Every Visa, Mastercard, Amex, Discover, UnionPay, JCB, Maestro, and Diners Club number you have ever typed, swiped, or tapped carries a Luhn checksum in its last digit. Strip that digit and you have a perfectly usable card number — for fraud. Keep it, and you have a number that has declared, on its own, that the other 15 digits are consistent with the rules of arithmetic. The bank never has to call. The number calls for itself.

## What the Luhn algorithm actually computes

A Luhn check is a weighted sum, mod 10, with one twist. Starting from the *second* digit from the right, you double every digit. If doubling pushes a digit past 9, you subtract 9 (the same as adding the two digits of the doubled result — 8 doubled is 16, and 1 + 6 = 7, which is 16 − 9). The rightmost digit — the check digit — is *never* doubled. Sum everything. If the total is divisible by 10, the number passes.

Try it on a real test card — `4242 4242 4242 4242`. Strip the spaces: `4242424242424242`. Walk from the right, leaving the last digit alone: position 1 is 2 (undoubled). Position 2 is 4 → 4 × 2 = 8. Position 3 is 2 (undoubled). Position 4 is 4 → 8. Alternating all 16 digits, you get eight 8s from the doubled 4s and eight 2s from the undoubled 2s. Sum: 8 × 8 + 8 × 2 = 64 + 16 = 80. 80 mod 10 = 0. The number passes.

Now try a typo — `4242 4242 4242 4243`. The only change is the last digit, 2 → 3. Same walk: eight doubled 4s still give 64. Eight undoubled 2s still give 16. Plus the check digit, now 3. Sum: 64 + 16 + 3 = 83. 83 mod 10 = 3. The number fails. One digit flipped, and Luhn catches it.

Now try a *transposition* — a classic data-entry error where you swap two adjacent digits. `4242 4242 4242 4422` instead of `4242 4242 4242 4242`. Positions 13 and 14 from the right are now 4 and 4 instead of 2 and 4 (after working from the right). The doubled-position digit at slot 14 was a 2, now a 4 — 2 × 2 = 4, 4 × 2 = 8. Difference: 4. The undoubled-position digit at slot 13 was a 4, now a 4 — no change. Net effect: +4 to the sum. 80 + 4 = 84. 84 mod 10 = 4. The number fails. Luhn catches the transposition.

This is the property the IBM engineers were after in 1960: a single-line arithmetic test that catches every single-digit typo and almost every adjacent-digit transposition, the two errors that account for the vast majority of human data-entry mistakes. A Luhn check is O(n) in the number of digits, runs in microseconds, and requires no lookup table. The whole algorithm is five lines in any language.

## Why this is enough — and why it isn't

A Luhn check is fast, cheap, and catches roughly 100% of accidental errors. It does not catch deliberate fraud. If you have a valid 15-digit prefix and want to forge a Visa, you can run Luhn forward, compute the correct check digit, and you have a 16-digit number that passes every form validation on the internet. The algorithm was designed to catch *typos*, not theft. The fraud-detection work happens elsewhere: address verification (does the billing ZIP match the bank's record?), CVV matching (do you have the 3-digit number on the back?), 3-D Secure (does the cardholder's bank approve the transaction in real time?), velocity checks (have you tried 14 cards on this account in the last hour?), and the actual settlement network, which has hours to flag a charge as fraudulent after the fact. Luhn is the *doorknob*, not the *lock*.

This is why credit card forms validate the number client-side before the request even leaves the browser. The validation is a courtesy. It tells the user "you mistyped" before the round-trip to the bank, where the real cost of a malformed request would be measured in latency, fraud-engine load, and false declines on legitimate customers who fat-fingered a digit. The whole reason the Luhn check has survived 65 years and four generations of payment technology is that it solves one problem extremely well: *turn a typo into a form error in under a millisecond, on the client, with no network call*.

## How the validator actually knows the card type

The first 6 to 8 digits of a card number are the Issuer Identification Number (IIN), sometimes still called the BIN (Bank Identification Number). The IIN tells the validator which network issued the card and, in many cases, which bank. Visa starts with 4. Mastercard starts with 51–55 or 2221–2720. American Express starts with 34 or 37. Discover starts with 6011, 622126–622925, 644–649, or 65. UnionPay starts with 62. JCB starts with 35. Diners Club starts with 300–305, 36, or 38. Maestro runs across a wide range and is mostly used in Europe. The first digit alone (the Major Industry Identifier, or MII) tells you the industry: 1 and 2 are airlines, 3 is travel and entertainment (Amex, Diners), 4 and 5 are banking and financial (Visa, Mastercard), 6 is merchandising (Discover, UnionPay), 7 is petroleum, 8 is telecom, 9 is national assignment.

The validator's job is straightforward: take the first few digits, look up the IIN in a table, return the network name. Luhn-valid + IIN-match = the number is *plausibly* a real card. Luhn-valid + IIN-mismatch = the number is *probably* a typo. Luhn-invalid = the number is *definitely* mistyped, or it isn't a credit card number at all (it could be an IMEI, a Canadian SIN, a US National Provider Identifier, or a tracking number — all of which also use Luhn).

This is why a "credit card validator" tool, as a category, is really three checks stacked on top of each other: Luhn for typo detection, IIN lookup for network identification, and length validation for the specific network (Visa and Mastercard are 16 digits, Amex is 15, Diners is 14, UnionPay is 13–19). All three run in microseconds. All three run client-side. None of them contact the issuing bank. The form on the merchant's page does this in your browser before you even hit Submit.

## Where the algorithm lives in real code

A Luhn check in JavaScript is the kind of thing every developer has written at least once, usually in a checkout flow, usually at 2 AM, usually without tests:

```js
function luhnValid(num) {
  const digits = num.replace(/\D/g, '').split('').map(Number);
  if (digits.length < 12) return false;
  let sum = 0;
  let alt = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = digits[i];
    if (alt) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
    alt = !alt;
  }
  return sum % 10 === 0;
}
```

That `alt = !alt` flag is the whole algorithm. Everything else is bookkeeping — stripping spaces and dashes, handling 13-digit vs 19-digit numbers, returning a useful error. The check is O(n) in the number of digits, runs in well under a millisecond, and has no dependencies. You can paste it into any frontend, any backend, any mobile app, any form library. It is, in some real sense, the most widely deployed piece of arithmetic in commerce.

The interesting design choice is `alt = !alt` starting at the rightmost digit. The flag flips on every iteration, but the *first* digit processed (rightmost) is left undoubled. This is the convention: the check digit sits at position 1, positions 2, 4, 6, ... are doubled, positions 1, 3, 5, ... are not. The `alt` flag is initialized to `false` precisely so the rightmost digit skips the doubling. The same algorithm in Python or Go or Rust looks almost identical. It is the algorithmic equivalent of a folk song: the same five notes in the same order, in every language, since 1960.

## The samples you'd actually test against

Real test card numbers are not "Luhn-valid numbers I made up." They are issued by the card networks, documented in every payment processor's developer docs, and safe to use in development because they will never charge a real account. Stripe publishes `4242 4242 4242 4242` (Visa), `5555 5555 5555 4444` (Mastercard), `3782 822463 10005` (Amex), and `6011 1111 1111 1117` (Discover). Adyen publishes the same set, plus regional variants. Every one of these passes Luhn. Every one has a future expiry date in the issuer's docs (often `12 / 34`). Every one rejects any CVV except the documented ones (often `123` or any 3 digits). And every one declines with a clear error in the sandbox if you try to use it in production.

A test credit card number that fails Luhn is *not a test card number* — it is a typo. The whole point of test cards is that they pass every layer of validation that a real card would, so the developer's checkout flow gets exercised end-to-end without anyone paying for the privilege. If your "test" number fails the Luhn step, the form rejects it, the user sees an error, and you have no idea whether the rest of your checkout works. A good credit card validator gives you both the Luhn check and a sample library, so you can copy-paste a working number into your sandbox and move on.

## What the Luhn check doesn't do

Luhn is silent on three things that matter. First, it does not check the *expiry date* — a card that expired in 2019 can still pass Luhn. Second, it does not check the CVV — a card whose back-number is `000` will pass Luhn. Third, it does not check whether the card has been *issued* by the network at all. Luhn-valid + future expiry + any 3-digit CVV is enough to pass every form validation, but it will fail at the bank. This is by design: the form's job is to catch typos, not to authorize charges. Authorization is the bank's job, and it happens after the form is submitted.

The privacy property is also worth noting. A Luhn check reveals nothing about the cardholder. It does not contact any server. It does not log the number. It does not even need the number in cleartext — the validator can run on a hashed form, on a tokenized form, on a number passed through a CDN edge function. The card number never has to leave the user's browser for the form to say "this looks like a Visa." This is why every modern checkout flow validates locally first. It is faster, cheaper, and more private than a server-side check.

## Try it on your own card

Take any credit card in your wallet. Strip the spaces. Strip the last digit. Run the Luhn walk on what remains — alternate double-and-leave starting from the right, subtract 9 from anything that lands above 9, sum the lot, add back the check digit. The total should be a multiple of 10. You can do this with the 5-line JavaScript function above, or with a 30-second pencil calculation if you trust your arithmetic. The fact that the algorithm is short enough to do by hand is exactly why it has survived: the original IBM engineers could verify it in their heads, and so can you, 65 years later, in a coffee shop, on the back of a receipt, with no internet connection.

This is what the Luhn algorithm actually is — a one-page arithmetic trick, published in 1960 to keep punch-card readers honest, that turned out to be exactly the right shape to catch typos in 16-digit card numbers that wouldn't be invented for another two years. Every checkout form on earth runs it. Every payment processor relies on it as the first filter. Every credit card number you have ever typed has been Luhn-checked before the form was even submitted. The algorithm predates the use case, the use case has outgrown the algorithm many times over, and the algorithm is still there, doing the only job it was ever asked to do: catching typos before they cost anyone money.

Validate your own card number against the [Credit Card Validator](https://elysiatools.com/en/tools/credit-card-validator) and the [Credit Card Samples](https://elysiatools.com/en/samples/credit-card) library, and try a few synthetic numbers to see which prefixes the IIN table picks up. The next time a checkout form rejects your card before you even hit Submit, you'll know exactly which 5 lines of code just said no — and why saying no was free.

---

*Explore more validation tools at [elysiatools.com](https://elysiatools.com/en/tools).*
