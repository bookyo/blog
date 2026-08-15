---STRIP---
<figure class="article-poster"><img src="CARD0_URL" alt="UPC/EAN Barcode Validator field guide poster" /></figure>

<strong>Every barcode on every product on every shelf is one short number with a checksum baked into its last digit.</strong> Miss that last digit by transposing two digits, and the scanner rejects it. Get it right, and the same number moves cleanly across a Walmart in Arkansas, a Tesco in London, and a Carrefour in Paris, all the way to a warehouse in Shenzhen. The [UPC/EAN Barcode Validator](https://elysiatools.com/en/tools/upc-ean-validator) lets you confirm that final digit in milliseconds. Once you see the pattern, you can verify any GTIN-8, GTIN-12 (UPC-A), GTIN-13 (EAN-13), or GTIN-14 by hand.

## What a GTIN actually is

A **GTIN** (Global Trade Item Number) is the GS1 identifier printed under every retail barcode. The format family has four members, all of which are numeric strings ending in a mod-10 weighted checksum. The four variants differ only in total length and the leading prefix that tells a scanner what kind of object it is looking at. The body is just an identifier assigned by GS1 to a manufacturer or product. The trailing digit is computed from the rest. The validator's job is to recompute that trailing digit and check whether it matches what was printed.

## The four GTIN variants

The four lengths each serve a different slot in the supply chain.

- **GTIN-8** (also called EAN-8): 8 digits, used on small packages where there is no room for a 12-digit symbol.
- **GTIN-12** (UPC-A): 12 digits, the canonical North American retail symbol.
- **GTIN-13** (EAN-13): 13 digits, the canonical international retail symbol.
- **GTIN-14**: 14 digits, used on shipping cartons and cases.

The check digit algorithm is identical across all four lengths. The body length is the only structural difference. Once you know the algorithm, you can validate any of the four on a napkin.

## How the mod-10 weighted checksum works

Take the digits, sum every odd-positioned digit from the right multiplied by 3, plus every even-positioned digit multiplied by 1, then pick the smallest non-negative integer that brings the total to a multiple of 10. That integer is the check digit.

For a 13-digit EAN-13 like `4006381333931`:

```
position (from right, 1-indexed): 13 12 11 10  9  8  7  6  5  4  3  2  1
digit:                              4  0  0  6  3  8  1  3  3  3  9  3  1
weight:                             1  3  1  3  1  3  1  3  1  3  1  3  1
product:                            4  0  0 18  3 24  1  9  3  9  9  9  1
```

Sum the products: 4 + 0 + 0 + 18 + 3 + 24 + 1 + 9 + 3 + 9 + 9 + 9 + 1 = 90. The sum is already a multiple of 10, so the check digit is 0. But the trailing digit of `4006381333931` is `1`, which the algorithm reports as invalid. That is exactly the kind of mismatch the [UPC/EAN Barcode Validator](https://elysiatools.com/en/tools/upc-ean-validator) catches in one call.

## Auto-detect versus explicit type

The validator accepts a `type` option with five choices. The default is `Auto-detect`, which means it infers the GTIN length from the input string. The other four values lock the validator to a specific length.

- `gtin-8` (EAN-8)
- `gtin-12` (UPC-A)
- `gtin-13` (EAN-13)
- `gtin-14`

Auto-detect is almost always the right choice for free-form validation. The lock options matter when you are processing a batch of strings and want to fail fast on a length mismatch instead of letting auto-detect silently reclassify them. A column of GTIN-12 codes that contains a few GTIN-13 typos is one common case where locking the length surfaces the bug immediately.

## Real numbers that pass

Three everyday barcodes you can paste into the validator right now.

- `012345678905`, a classic GTIN-12 sample, ends in 5, used in dozens of product-packaging tutorials.
- `5901234123457`, a GTIN-13 starting with `590`, the GS1 prefix assigned to Poland, ends in 7.
- `9780201379624`, a GTIN-13 starting with `978`, the GS1 prefix assigned to ISBNs, ends in 4. This is the same number you would scan on a book. The ISBN `0-201-37962-4` and the GTIN-13 `9780201379624` describe the same product.

All three pass the checksum. The last one is also a nice illustration of why ISBN-13 and EAN-13 are the same format with different GS1 prefixes.

## Common failure modes

Three patterns cause the validator to reject an otherwise reasonable number.

- **Single-digit typo.** A data-entry error in any one position changes the checksum by a predictable amount, so the trailing digit no longer matches. The validator reports the recomputed check digit so you can see what the value should have been.
- **Transposed adjacent digits.** A swap of two adjacent digits keeps the digit sum constant but shifts the weighted positions, so the checksum breaks. This is the most common class of human transcription error.
- **Leading zero dropped.** A GTIN-12 pasted from a spreadsheet cell that stripped the leading zero becomes an 11-digit number. Auto-detect falls through to GTIN-8 and rejects it on length. Locking the type to `gtin-12` surfaces this faster.

A validation category tool like this one is most useful when it returns the computed check digit, not just a boolean. The boolean tells you the input is bad. The computed digit tells you why, and lets you decide whether the original source needs fixing or the input itself.

## How this fits a broader validation workflow

UPC and EAN validation is one slice of a larger identity-validation toolkit. ISBN is the same algorithm under a different prefix (`978` and `979`). Credit card numbers use Luhn, a closely related but distinct algorithm. Bank routing numbers and CUSIP identifiers use mod-10 with different weights. IBAN uses mod-97-10. When you stack these checks against each other you get a fast triage layer that catches the obvious transcription errors before they ever reach a downstream system. That is the same reason an address parser runs ahead of a billing system, and the same reason a phone-number normalizer runs ahead of an SMS gateway.

For a complementary validator that catches credit card typos, the [Luhn Checksum Calculator](https://elysiatools.com/en/tools/luhn-checksum) sits a click away. For a broader sweep across international financial identifiers, the [IBAN Validator](https://elysiatools.com/en/tools/iban-validator) handles the European banking side. Explore the rest of the [Validation category](https://elysiatools.com/en/tools) for sibling tools covering ISBN, VIN, and other mod-10 code families.

## Putting it together

The mod-10 weighted checksum that lives in the last digit of every GTIN is the same algorithm that protects credit card numbers, IMEI codes, and ISBNs. Once you have the pattern, validating a GTIN-8 or GTIN-14 by hand takes about a minute. For any larger batch, the [UPC/EAN Barcode Validator](https://elysiatools.com/en/tools/upc-ean-validator) returns the computed check digit in a fraction of a second and lets you keep moving.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).