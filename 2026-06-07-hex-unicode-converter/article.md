---
title: Why Every Character on Your Screen Is Secretly a Number
slug: hex-unicode-converter-secret-number
---

A colleague of mine pasted a string into a chat window and it broke. The string was "Beyoncé" and the chat client swallowed the é. They switched clients, retried, watched the same character vanish. The cause was a ten-year-old serialization bug the client never fixed: it accepted UTF-8 on input, treated the bytes as Latin-1 on the way through, then re-encoded them as UTF-8 on output. The fix was one line: encode the string as `\u00e9` before sending. The receiving end turned the escape back into the right glyph. Have you ever watched a single accent vanish from a name?

That single line — `\u00e9` for `é` — is the entire reason escape sequences exist. Every text system on Earth has a moment when it must hand a character to another system that may not speak its language. **A backslash followed by a number is the contract.** Everything else is history.

## The character is a number — always has been

When you type "A" on a keyboard, your computer does not see the letter A. It sees the integer 65. When you type "é", it sees 233 (in Latin-1) or, more usefully, 233 in decimal but 0x00E9 in hex and `\u00e9` in the 16-bit Unicode escape that JSON adopted. When you type the snowman ☃, your computer sees the integer 9731 — or, in the UTF-8 byte stream that travels over the wire, three bytes: 0xE2, 0x98, 0x83.

This isn't a metaphor. Inside the memory of every program, every glyph is an integer. The integer has a standardized name (a "code point") assigned by the Unicode Consortium. The integer has a standardized wire format (UTF-8, UTF-16, or UTF-32) that turns the integer into bytes a wire can carry. The integer has a standardized escape representation (`\xXX` for one byte, `\uXXXX` for one code point) for places that can't carry the original bytes at all.

The escape forms exist for one specific reason: not every medium can carry arbitrary bytes. A C string literal in source code can't safely contain a raw null byte. A JSON file can't safely contain a raw control character. A Windows-1252-encoded CSV opened in Excel will mis-interpret a smart quote. In each case, the sender **encodes** the character as a backslash sequence — the smallest, most portable representation of "this character" that any text-handling system is guaranteed to understand. The receiver **decodes** the backslash sequence back into the character before doing anything else with it.

The escape is the contract. The contract is the number. The number is the character. The whole system runs on this single, load-bearing fact.

## Why hex and Unicode look like different systems

If you stare at enough log files and config files, you'll see two flavors of escape: `\xXX` and `\uXXXX`. They look different, and they answer different questions.

`\xXX` (or `\xXX\xXX` for characters that need more than one byte) speaks the language of **bytes**. Each pair of hex digits is one byte. The string "Hi" in hex escape is `48 69` — two bytes, four hex characters. The string "é" in UTF-8 hex escape is `c3 a9` — two bytes, four hex characters. You can think of `\x` as a way to write bytes when you can't write the actual byte. C string literals use this form. Most low-level file formats use this form. When you see a hex dump of a file and ask "what's at offset 0x42?", the answer is a byte, and `\x42` is the literal.

`\uXXXX` speaks the language of **code points**. Each group of four hex digits is one Unicode scalar value, regardless of how many bytes the encoding uses to transmit it. The string "é" in Unicode escape is `\u00e9` — always six characters, always one code point, regardless of the underlying encoding. JSON adopted this form for the JavaScript Object Notation specification in 2002. XML, JavaScript, and most modern config formats followed. When you see `\u2014` in a JSON file, you don't need to know which encoding the receiver expects — you have the number, and the receiver turns the number into the right bytes.

A snowman `☃` in JSON is always `\u2603`. The same snowman in C is `"\xe2\x98\x83"` (three bytes) or `"\u2603"` (one code point, depending on the compiler). **Both forms are correct. The question is whether the receiver wants bytes or code points.** A regex engine that operates on UTF-8 bytes wants `\x` escapes. A JSON parser that operates on Unicode code points wants `\u` escapes. Sending the wrong one to the wrong system is a category of bug older than most of the engineers debugging it.
## What actually happens when a log file shows `\xe2\x98\x83`

Picture an application that catches an unhandled exception in a string. The string is the three-byte UTF-8 sequence for the snowman — call it `bytes([0xE2, 0x98, 0x83])`. The exception handler logs the string with a `repr()`-style formatter that doesn't know the destination is a non-UTF-8 terminal. The formatter writes one byte at a time, escapes anything that isn't printable ASCII, and produces the log line:

```
ERROR: failed to render snowman glyph \xe2\x98\x83 in row 42
```

A developer reading the log has just received a hex-encoded UTF-8 sequence. The first instinct is to ask what character `\xe2\x98\x83` is. The answer requires three steps:

1. Group the hex digits into bytes: `0xE2`, `0x98`, `0x83`.
2. Check whether the bytes form a valid UTF-8 sequence. The first byte `0xE2` has the bit pattern `11100010`, which is the lead byte of a three-byte UTF-8 sequence. The next two bytes must each be of the form `10xxxxxx`. `0x98` is `10011000` — valid. `0x83` is `10000011` — valid.
3. Concatenate the lower six bits of the three bytes: `0010 011000 000011` → regroup as `00100110 00000011` → `0x2603` in hex → the Unicode code point U+2603, named "SNOWMAN".

The three-byte sequence that arrived as `0xE2 0x98 0x83` collapses to one code point U+2603, which renders as ☃. The log line was never broken; it was **transmitting a non-ASCII character through a channel that speaks only hex**. Once you decode the hex, the snowman is right there.

This is exactly what a [Hex/Unicode converter](https://elysiatools.com/en/tools/hex-unicode-converter) does. You paste the escaped sequence, choose the direction (hex → text, text → hex, Unicode → text, text → Unicode), and the tool collapses the bytes or expands the code points for you. For a three-byte sequence the round trip is "read three escape pairs, group them, decode the UTF-8, look up the code point." For a long string it's the same operation repeated N times — the kind of thing a tool should do for you, with the [hex/unicode sample set](https://elysiatools.com/en/samples/text-hex-unicode-formats) shipping eighteen canned inputs you can paste to confirm symmetry.

## The case where you have to encode, not decode

Sometimes the situation is the reverse. You're building a JSON payload, an SQL parameter, or a config file that downstream systems will parse strictly as ASCII. You need to ship the string "Beyoncé — Café ☕" through a parser that will mis-interpret the bytes, and you cannot fix the parser. The safe move is to escape every character that isn't 7-bit ASCII before sending it.

The encoding is mechanical. For every character in the source string, look up the code point, convert to UTF-8 bytes, then for each byte write `\x` followed by the two-digit hex value. The snowman `☃` becomes `\xe2\x98\x83`. The `é` becomes `\xc3\xa9`. The "—" em-dash becomes `\xe2\x80\x94`. The output is a string consisting only of ASCII printable characters and the escape character itself — a string any text-handling system on Earth can store, transmit, and parse without surprise.

The trade-off is size. A snowman is 3 UTF-8 bytes. In hex escape it's 12 characters (3 escape pairs of 4 characters each — backslash, x, two hex digits). The expansion factor is 4×. For a few dozen emoji in a UI string, this is fine. For a million log lines, the bandwidth and the storage cost matter — which is exactly why engineers invented base64, snappy, and other higher-density encodings. But for the common case — a config file, a log line, a one-off payload — `\x` escape is the cheapest portable representation. The size penalty is the price of compatibility.

## Why the JSON spec is built on `\u`

The JSON specification (RFC 8259, section 7) is explicit: a string is a sequence of Unicode characters, and any character may be escaped as `\uXXXX`. The motivation is interoperability. JSON was designed as a data interchange format that any parser on any platform, written in any language, could read. Most parsers in 2002 defaulted to ASCII or Latin-1. Forcing the spec to use raw UTF-8 bytes would have broken those parsers. Forcing the spec to use raw UTF-16 code units would have been inefficient for ASCII-heavy payloads. The `\uXXXX` form is the lowest common denominator: a fixed-width, four-hex-digit escape that any parser can implement with a 200-line switch statement and zero knowledge of variable-width encodings.

This is why the JSON spec calls `\u` the only required escape. `\b`, `\f`, `\n`, `\r`, `\t`, `\"`, `\\`, and `\/` are conveniences (they each map to one specific code point that could also be written as `\uXXXX`). The `\uXXXX` form is the *core*. Every other escape is shorthand for a code point a parser could have read by counting hex digits.

If you've ever had a JSON parser reject your payload because it contained a raw control byte — a 0x0A in a multi-line string, a 0x00 in a name field, a 0x1F somewhere you didn't expect — you've hit exactly the case the `\u` escape exists for. The fix is the same: encode the offending byte as `\u00XX` and resubmit. The parser will see ASCII, accept it, and reconstruct the right code point on the way out. This works in every JSON parser on Earth, because the spec is unambiguous about the contract: **every character in a string is either a printable non-control character or a `\uXXXX` escape.** A byte that is neither is, by definition, not a valid JSON string.

## The four commands a hex/Unicode tool actually exposes

Strip away the UI and a hex/Unicode converter is four operations, in pairs. Encode to hex: every byte in the source string becomes `\xXX`, output is ASCII-only. Decode from hex: the tool finds every `\xXX` escape in the input, replaces it with the corresponding byte, and returns the original bytes interpreted as UTF-8. Encode to Unicode: every code point in the source string becomes `\uXXXX` (or, for code points beyond U+FFFF, a surrogate-pair form), output is ASCII-only. Decode from Unicode: the tool finds every `\uXXXX` escape, looks up the code point, encodes it as UTF-8, and returns the bytes.

A good tool handles edge cases without complaining. The byte 0x00 (the null terminator) round-trips. The code point U+0000 round-trips. A character in the supplementary plane (above U+FFFF, like most emoji) is encoded as a surrogate pair in JSON's strict form, and as a single `\uXXXX` in JSON's relaxed form. The output format flag — `with prefix`, `compact`, `array` — is a styling choice: do you want `\x48\x69` or `[0x48, 0x69]`? Both are correct; both are ASCII; both round-trip identically. **Build** a small battery of these tests and you have proven the tool is sound.

Every character you have ever read, sent, or stored was a number. Every escape you have ever seen — `\n`, `\t`, `\xe2`, `\u00e9`, `\u2603` — was a sender's promise that the number would survive the trip. The backslash means one thing: *trust the next few characters, I have the number.* When the contract breaks, glyphs vanish and log files lie. When the contract holds, "Beyoncé" travels intact across a wire that was built in 1972 and has never heard of an accented vowel. The next time a log line shows `\xe2\x98\x83` and your editor balks, **decode** it. The next time a JSON payload hides a non-ASCII name, **encode** it before you ship. So the next question is yours: what is the most surprising string you have ever seen in a log file, and what number was hiding behind it?
