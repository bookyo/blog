---
title: A=1 Is Easy. Decoding It Back Is Not.
---

Two inputs, one output. Encode `AB` with A1Z26 and pick "no separator" and you get `12`. Decode it and you get `L` — silently, with no warning. One character instead of eleven and the word is gone. Is that a bug? No. It is the shipped default of the simplest cipher on the internet. Change one setting and the same cipher round-trips perfectly.

## The mapping fits in one line

A1Z26 assigns each Latin letter its position in the alphabet: A=1, B=2, C=3, through Z=26. The encoder walks the string, reads each code point, and subtracts 64 for uppercase or 96 for lowercase. Two branches, thirty characters of logic. There is no key, no table to ship, and nothing to negotiate between sender and receiver.

The interesting behaviour is not the mapping. It is what the encoder does with all that is not a letter.

Encode `Hello, World!` and the tool returns `8-5-12-12-15-23-15-18-12-4` and reports `3` skipped characters. Thirteen input characters became ten numbers. The comma, the space, and the exclamation mark were discarded — counted, but not carried.

That skip counter is the only evidence those characters ever existed. Encode `A1` and you get `1`, with `1` skipped. Encode `A` and you get `1`, with `0` skipped. Same output, different inputs, and the only thing separating them is an integer in a metadata field. If you log the numbers and drop the counter, the difference disappears.

## The Case dropdown changes nothing

The workbench offers three case modes: uppercase, lowercase, and preserve original. Try all three on `Hello` and the output is `8-5-12-12-15` each time. The letter sum is `52` in all three modes as well.

The reason is in the order of operations. The encoder normalizes the string first, then applies two separate branches — `A`–`Z` subtracts 64, `a`–`z` subtracts 96 — and both land on the same integer. Normalizing to lowercase before the walk feeds the second branch. Normalizing to uppercase feeds the first. `preserve` skips the normalization and feeds whichever branch matches. Three roads, one destination.

Decode ignores the setting entirely and always emits uppercase.

This matters more than it looks. A control that implies a decision and carries none forces users to distrust the rest of the interface. If you build a variant of this tool, do not add a case flag to the encode path. It has no semantic content, and it invites the reasonable-but-wrong assumption that `a1z26` and `A1Z26` somehow differ.

## `sep: none` is the only irreversible choice

Four separator options sit in a dropdown: hyphen, space, comma, none. Three of them are framing. The fourth is destruction.

Decode splits its input on any run of non-digits. With a hyphen, `8-5-12-12-15` becomes five tokens and decodes to `HELLO`. With no separator, the same message becomes a single token — the number `85121215` — which fails the 1-to-26 range test and lands in the invalid counter. The letters are gone.

Short words break worse, because they break quietly:

<ul>
<li>`AB` encodes to `12`, which decodes to `L`. One letter out, zero warnings.</li>
<li>`HI` encodes to `89`, which decodes to nothing and reports one invalid token.</li>
<li>`CAB` encodes to `312`, above the range, rejected.</li>
<li>`YO` encodes to `2515`, above the range, rejected.</li>
</ul>

So there are two distinct failure modes, and only one of them announces itself. A joined number at or below 26 decodes to a plausible letter — wrong, confident, and indistinguishable from a correct answer. A joined number above 26 gets rejected, which at least tells you something broke. The safe-looking outputs are the dangerous ones.

The separator is not cosmetic decoration on the output. It is the framing that makes the message readable at all. Try the round trip yourself at [Elysia Tools](https://elysiatools.com/en/tools/a1z26-letter-number-workbench).

## Decode is looser than encode in three ways

The decoder validates each token with two tests: it must consist only of digits, and its numeric value must fall between 1 and 26. It never checks the token's length. Three consequences follow.

<ul>
<li>Leading zeros are accepted. `007` decodes to `G`, and `00008` decodes to `H`.</li>
<li>`026` decodes to `Z` — correct value, wrong width. `027` is rejected, because 27 is out of range regardless of formatting.</li>
<li>Any non-digit run counts as a separator. `20-8-5`, `20 8 5`, `20,8,5`, `[20][8][5]` and `20_8_5` all decode to `THE`.</li>
</ul>

The second point is the useful one for debugging. `007` and `7` decode identically, which means a decode cannot be reversed back to the exact token string you started from. If your pipeline re-encodes decoded text and compares it to the original tokens, it will report a mismatch on inputs that were never wrong.

The third point explains why text pasted from a spreadsheet column or a chat message usually works. The decoder is forgiving about delimiters by design, and it treats each bracket, dash, and underscore as one.

## Round-tripping is a property of the settings, not the cipher

Plainly: with hyphen, space, or comma, `encode` then `decode` returns the original letters, provided the original contained only letters. With `none`, it does not.

That is an honest gap, not a defect. The encoder has no pass-through path for punctuation — non-letters increment a counter and are dropped — so no separator setting fixes the loss. Worth stating before you build on it.

## Letter sum answers a different question

The third mode skips encoding entirely and adds up the letter values. `ABC` is 6. `Z` is 26. `AZ` is 27, and so is `ZA`. `Hello, World!` is 124 across ten counted letters.

The sum ignores non-letters, ignores order, and ignores case — `Hello` returns 52 in all three case modes. That combination means the sum is a many-to-one map: a huge family of distinct strings reduces onto each total. `AZ`, `ZA`, `BY`, and `YB` all land on 27.

So the sum can never confirm a string. It can only reject one. Only a mismatch proves anything. If a puzzle states that a phrase sums to 124 and your candidate sums to 118, you have learned something real. If your candidate sums to 124, you have learned almost nothing.

## Where this belongs, and where it does not

A1Z26 is a warm-up. It shows up as the first stage of puzzle hunts, as an ARG breadcrumb, as a classroom exercise in substitution ciphers, and as the arithmetic behind gematria-style letter-value tools.

It is not encryption. Twenty-six symbols, no key, no confusion layer, and a frequency distribution you can read off a paragraph of English by hand. Treat any use of it as obfuscation and nothing more.

What it does show is the distinction that this page is about: an encoding can look like a number system and still be a format with framing rules. Morse has its gaps. Base64 has its padding. A1Z26 has its separator, and the day you drop it you cut the message in half.

## The four checks before you trust a decode

Run these checks and most surprises disappear before they cost you a message.

<ul>
<li>Count the delimiters in the input. Zero delimiters in a multi-letter message means one token, and one token means at most one letter.</li>
<li>Compare the token count to the expected letter count. A message that should be eleven letters but yields one token has already failed.</li>
<li>Check the skip counter against the original length. Ten numbers from thirteen characters means three characters vanished, and they were not letters.</li>
<li>Read the decoded text for letter frequency. A decode that produced a single `L` where you expected a word is a framing failure, not a cipher failure.</li>
</ul>

The workbench reports all four numbers directly, which is the main reason to use a purpose-built page instead of a regex in your scratchpad. The parse is three lines of JavaScript; the diagnostics are what you need.

Browse the rest of the catalog at [elysiatools.com](https://elysiatools.com/en/tools), or start from the [text processing category](https://elysiatools.com/en/categories/text-processing) if you are working through a puzzle pipeline.

For years I described A1Z26 as "the alphabet in numbers" — true, and useless. The retraction is smaller. It is the alphabet in numbers only while you keep the separators. Drop them and `AB` and `L` stop being different words; keep them and the cipher round-trips each time you try. So what should you carry away? One character stands between a code and a guess. If you take nothing else from this page, take the hyphen.
