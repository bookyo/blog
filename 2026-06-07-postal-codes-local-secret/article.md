---
title: Why Every Postal Code in the World Is Quietly a Local Secret
description: Postal codes look universal. They are not. A look at the regex zoo hiding behind 90210, SW1A 1AA, and 100-0001.
tags: postal-codes, regex, international, addresses, validation, geography
---

## What postal codes actually do

A postal code is a promise. The sender writes it, the carrier believes it, and a sorting machine somewhere in the network reads it and decides which truck the letter rides for the next leg of the journey. That is the entire job. It is not a database key, not a geographic coordinate, not a unique address identifier. It is a routing label — and every country in the world has invented its own.

This is why the US uses `90210`, why the UK uses `SW1A 1AA`, why Japan uses `100-0001`, why Brazil uses `01310-100`, and why the Netherlands — a country the size of a US county — once wanted to use exactly four digits and one letter per postcode. There is no global standard. There never has been. The Universal Postal Union has been meeting about it since 1874, and the only thing the member post offices have ever agreed on is that they each have a good reason for the system they have, which is true and also completely unhelpful if you are trying to validate a form.

## Why a "simple" validator is not simple

A postal-code validator that just checks "is this a number" is wrong for almost every country on earth. The German system is five digits. The Canadian system alternates `A1A 1A1`, with letters in fixed positions. Argentina uses four digits with a space, then three letters and three digits. The UK's postcode grammar has six discrete positional cases, and that is the version Royal Mail published *after* simplifying it in 1990.

The Global Postal Code Validator encodes this diversity. It ships a table of patterns, country by country, and matches the input against the pattern that belongs to the country you tell it. Pass `SW1A 1AA` to the German rule and you get rejected. Pass `10115` to the UK rule and you also get rejected, even though 10115 is a perfectly valid Berlin postcode. The tool knows the difference because it carries the rules. Without those rules, validation is theatre.

## The regex zoo

Peek under the hood of any serious postal-code validator and you find a regex zoo. Australia is `[0-9]{4}`. Brazil is `[0-9]{5}-[0-9]{3}`. France is `[0-9]{5}`. India is `[1-9][0-9]{5}`. Norway is `[0-9]{4}`. Russia is `[0-9]{6}`. The UK, in 2024, after the Royal Mail change, is `^([A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2})$` with seven validations layered on top. Japan is the deceptively tame `[0-9]{3}-[0-9]{4}` until you remember that the leading three digits of a Japanese postcode encode the prefecture, and a code without a valid prefecture prefix is, technically, a number — but not a real address.

So when the validator returns "valid," it means one of two things: the string matches a known pattern, or the string looks like a known pattern. Neither guarantee is the same as "this address exists." Postal-code validation is a syntax check, not a deliverability check. The two get confused constantly, and that confusion costs shipping companies real money.

## The pattern that breaks most validators

The one that breaks naive validators is the UK postcode. It is the only national system where the *position* of letters and digits matters at the character level, where there are exactly six valid letter positions in the inward code, where the letters `C`, `I`, `K`, `M`, `O`, `V` are deliberately excluded because they look like digits, and where the entire grammar cannot be expressed in fewer than about thirty characters of regex. According to the Royal Mail specification published in 2011, the modern UK postcode grammar has six positional variants for the outward code and three for the inward code, with a small set of disallowed letter positions to keep machine reading reliable. It is the only postal system that grew out of an address scheme designed before machine reading existed.

This is why most off-the-shelf postal-code regex you find on Stack Overflow is wrong for the UK. It will accept `AA1 1AA` (correct), and it will *also* accept `ZA1 1AQ` (incorrect — Z is not a valid first letter of a UK outward code, except in a small set that no general regex captures). The Global Postal Code Validator gets this right by carrying a curated table of UK outward-code prefixes, which is the part the regex is silently compensating for.

## What the validator cannot do

It cannot tell you that a postcode has been retired. It cannot tell you that the street no longer exists. It cannot tell you that the building at that address was demolished last Tuesday, or that a town was renamed, or that a postal worker in Tbilisi decided the new district gets a fresh prefix. Postal systems are living things. The code in your database from 2019 may technically still pass validation in 2026 because the syntax is intact, and the letter you send to it will still travel — it will just land in the dead-letter office.

This is the part that surprises people. A postal code is a routing contract, and routing contracts have an expiration date, but the contract never tells you what that date is. The validator confirms the form. The deliverability depends on a system the validator cannot see.

## What it is good for

It is good for exactly what it claims. Form validation on a checkout page. Cleaning a CSV of customer addresses before import. Rejecting obvious typos — `SWlA 1AA` with a lowercase L, `100-000l` with a lowercase L again, `9021O` with a letter O where a zero should be. A surprising amount of "bad data" in real address tables is just the digits 0 and 1 swapped for the letters O and l, and a syntactic check catches most of it. The validator catches it for twenty-something countries at once, which is the part that earns its keep.

If your form has a country dropdown, the validator is the cheapest way to make that dropdown mean something.

## What the rest of the world tells us

Postal codes are a window into how a country thinks about itself. According to the U.S. Postal Service's 1963 implementation memo, ZIP codes were designed around the Optical Character Reader limitations of the day — the readers could not distinguish letters, only digits, which is why the entire US system is numeric. Japan made them numeric and seven-digit for the same reason. The UK kept letters in the postcode because the Royal Mail had to be readable by a human walking the route in 1959. Germany uses five digits and nothing else because the Bundespost decided, in 1993, that a postcode should be memorizable, and five digits is the most a person can hold. Argentina uses a four-three split because the Argentine post wanted a province code in the front and a district code in the back, and the split is a small piece of national accounting.

You can read a country's history in its postcode. Try the Global Postal Code Validator across a few dozen codes from a few dozen countries, and you will see — sometimes literally, sometimes by pattern — the postal service each country wanted to be. The tool does not explain any of this. It just checks the syntax. The story is the side effect.

## How to use it without lying to yourself

A few practical rules. Always pass a country code alongside the postcode. Never validate an address without also knowing the country the address is from. Treat "valid format" as a floor, not a ceiling. If you ship physical goods, verify the high-value destinations against a real address database; the syntax check is your first gate, not your last. And if you ever see a regex that says "match postal codes worldwide," assume it matches nothing useful and replace it with the curated table that the Global Postal Code Validator ships with. The replacement takes one afternoon. It saves you years of "but our form said the address was fine" tickets.

There is a deeper lesson hiding inside the postcode table, and it generalizes. Whenever a piece of data looks universal — phone numbers, postal codes, dates, names, addresses, currency codes — assume it is not. The thing that looks universal is almost always a polite fiction maintained by a small set of rules that someone, somewhere, keeps up to date. The Global Postal Code Validator is one of those small maintenance jobs, and the people who maintain it do the world a quiet service by refusing to pretend the fiction is real. The next time your form accepts `SW1A 1AA` and rejects `100-0001` and you trust both, you are trusting the table. The table is doing more work than the form, and a more honest piece of software would tell you that out loud.

What you do with that knowledge is up to you. The form will keep doing what forms do. The postal service will keep doing what postal services do. The only thing that changes is whether you treat the five-digit number on the envelope as a fact or as a polite guess — and once you have seen the regex table, you can never quite go back to treating it as a fact again. If you want to see for yourself, the [Global Postal Code Validator](https://elysiatools.com/en/tools/global-postal-code-validator) is the table, made interactive.
