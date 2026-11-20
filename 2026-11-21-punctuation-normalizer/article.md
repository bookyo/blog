---
title: The Punctuation Pass That Turns 3.14 Into 3. 14
---

<strong>A period is punctuation right up until it is a decimal point.</strong> The same holds for the comma inside 1,204, the hyphen in a date stamp, and the question mark that opens a query string. [Punctuation Normalizer](https://elysiatools.com/en/tools/punctuation-normalizer) exists to make quotes, commas and brackets consistent across a corpus, and it does that job well. But it also ships with a toggle labeled "Normalize Spaces" turned on by default, and I measured what that toggle does: a value of 3.14159 came back as 3. 14159.

That finding lands hardest for anyone who treats normalization as a safe pre-step. That is the case for prose. It is not the case for identifiers, and most real text holds both.

## A glyph has a job in prose and a job in data

The full stop earns its place in a sentence. In 3.14159 it marks a decimal, in example.com it separates domain labels, and in v2.5.1 it carries version structure. It also delimits an IP address and an extension.

Five roles, one codepoint, and a character-level mapping table cannot tell them apart. That is the honest constraint of this class of tool, not a defect in this one. Any normalizer that rewrites characters without parsing context will collide with data punctuation somewhere.

The useful question is narrower. Which settings collide, with what, and can you turn the collision off before a corpus goes through it.

I read the tool's source instead of guessing from its label, then ported the logic to a second implementation and compared outputs on fixed inputs. Each pair below was measured that way.

## Two tables, thirty-two pairs, one ordering decision

The converter is two hand-written lookup tables applied as ordered global replacements. The Chinese-to-English table carries thirty-two entries, and the English-to-Chinese table carries eighteen. Both are exhaustive enough for prose and coarse enough to deserve a read before you trust them.

Three details in the tables change how the pass behaves. For example, the euro sign maps to itself, a no-op entry that reveals a table assembled by hand. The degree-celsius sign maps to a bare C, which is a unit conversion wearing punctuation clothes. And the double em dash maps to two hyphens before the single full-width hyphen maps to one, which is why the dash pair survives intact.

The English-to-Chinese direction digs deeper. It converts a hyphen to a double em dash, an asterisk to a reference mark, and angle brackets to CJK book-title marks. Those three mappings are fine for CJK prose and destructive for technical text.

## The default toggle that eats your decimals

Space normalization runs one rule with no exemption list: A comma, period, question mark, exclamation mark, semicolon or colon followed by a non-space character gets a space inserted after it. Here is the observed effect on one ordinary sentence, using the tool's defaults.

<ul>
<li>A decimal expands: 3.14159 became 3. 14159. </li>
<li>A thousands separator splits: 1,000,000 became 1, 000, 000. </li>
<li>A domain breaks apart: example.com?x=1 became example. com? x=1. </li>
<li>A version fragments: v2.5.1 became v2. 5. 1. </li>
</ul>

The input was 73 characters and the output was 80. In one case I ran the same sentence with spaces off and it came back byte-identical, with zero reported changes. That comparison pins the damage on the toggle alone.

This is the trap worth internalizing. The resulting text still reads like English, so it passes a visual scan. A decimal turns into a sentence break, a separator turns into a list, and a domain turns into two words. Nothing throws an error, and ten thousand product records later a price column has become prose.

## Chinese style is not a punctuation setting for mixed corpora

I observed a different failure on the same source text converted to Chinese style with spaces off. A date like 2026-11-21 becomes 2026——11——21. A comparison like 5 * 3 < 10 becomes 5 ※ 3 《 10. A price of $5.00 becomes $5。00, terminated by a full-width period. A negative number of -42 becomes ——42.

None of those results are wrong for a Chinese-language document, where full-width marks belong. They are wrong the moment the buffer also contains a date, an expression or a price, which is nearly always. The mode is a typography choice for prose and a hazard for everything else in the same buffer.

## Mixed mode is the one mode that leaves correct text alone

The mode listed as "Smart Mixed (Auto-detect)" earns that label. It splits the input on sentence terminators, both the ASCII trio and the CJK trio, then tests each fragment for any CJK ideograph and applies the matching table per fragment.

I fed it a bilingual line with the toggle off: a Chinese clause followed by an English clause containing a dollar amount. It returned the input unchanged, with zero changes. That is the correct answer, and it is the only mode here that produces it.

The limitation sits in the split. Only sentence terminators divide the text, so an ASCII comma inside an English fragment of a mostly-Chinese sentence still converts to full width. The filter that drops empty fragments also drops whitespace-only ones, so a pair of adjacent marks separated by a space closes up and the space disappears.

## What the pass does to line breaks and to Markdown

Line-break normalization is the second toggle, and it works in three steps. Windows line endings and lone carriage returns become plain newlines. Runs of three or more newlines collapse to two. Each line is then right-trimmed.

The first two steps match what you want. The third quietly breaks Markdown, because two trailing spaces are the syntax for a hard line break. Feed the tool a block of lines ending in double spaces and it returns them bare, so the block reflows into a single paragraph when rendered. Tabs collapse to one space as well, while non-breaking spaces survive untouched. That last gap will still show up in a diff after a cleanup that otherwise looked complete.

## The change counter reports a number that is not a change count

The number printed under "changes" is the most misleading part of the output, and the reason is four lines of logic. The counter walks both strings by index and compares one character against one character.

That works while edits preserve length. The moment a substitution changes length, each character after it registers as different. An ellipsis expansion on an eleven-character string reported nine changes for a single substitution, and a two-word input reported three. Neither number is wrong about the strings, since both strings do differ at those positions. Neither is a count of substitutions either, and reading it as one inflates a two-hundred-record cleanup into a catastrophe.

## The order to do these things in

A short checklist, built from the measurements above.

<ul>
<li>Run ten representative lines through the tool before the corpus, and diff the digits, not the words alone. </li>
<li>Turn space normalization off for anything holding numbers, versions, addresses or prices. Turn it on for CJK prose, where full-width spacing is the point. </li>
<li>Keep custom replacements to a single pass, because they apply in listed order and cascade. A pair that rewrites one token to a second, followed by a pair rewriting the second to a third, turns the first token into the third. </li>
<li>A replacement target containing an equals sign truncates at the first separator, so a three-part rule rewrites only the first token and drops the rest. </li>
<li>Prefer mixed mode over a forced style when a buffer holds more than one language, and skip normalization when the buffer is a data file. </li>
</ul>

The tool deserves a place in a cleanup pipeline, because the mapping tables save real editing time on quoted and bracketed text. The safe pattern is to read both toggles before the first run instead of after the first bad diff. You can [try it on a sample of your own text](https://elysiatools.com/en/tools/punctuation-normalizer) and compare the digit count before and after, which takes about thirty seconds. More text utilities live at [elysiatools.com](https://elysiatools.com/en/tools).

Two years ago I would have called punctuation normalization a solved problem: one table of character pairs, one button, no judgment required. I do not believe that anymore. The glyphs a normalizer edits are the same glyphs that hold numbers together, and the setting that decides whether your text survives is not the one labeled with a language. It is the small checkbox beside it, and that checkbox ships enabled. The question worth asking before your next cleanup is not which style you want. It is whether your output would still round to the same number.
