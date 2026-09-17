**A naive title caser that capitalizes every word will publish "A Guide to the Wonders of the Ancient World"** when the editorial standard is "A Guide to the Wonders of the Ancient World" — and that one missing capital on "of" is the kind of detail a copy editor notices before anyone else does. Title Case Converter solves this with three editorial style guides (AP, Chicago, Wikipedia) that know which short function words to leave lowercase and which words to always capitalize, and it handles the messy real-world cases — hyphenated compounds, contractions, words after colons, subtitles — that a simple capitalize-every-word script gets wrong.

[Try it yourself in the live editor at Elysia Tools](https://elysiatools.com/en/tools/title-case-converter).

## What the four styles actually disagree about

The biggest source of inconsistency between style guides is the list of words that stay lowercase in the middle of a title. Here is the short version:

<ul>
<li><strong>AP</strong> keeps a tight list lowercase: <code>a</code>, <code>an</code>, <code>and</code>, <code>as</code>, <code>at</code>, <code>but</code>, <code>by</code>, <code>for</code>, <code>in</code>, <code>nor</code>, <code>of</code>, <code>on</code>, <code>or</code>, <code>the</code>, <code>to</code>, <code>up</code>, <code>with</code>. Short coordinating conjunctions and short prepositions. The <code>to</code> in infinitives is treated as a preposition and stays lowercase.</li>
<li><strong>Chicago</strong> adds longer prepositions to that list (<code>about</code>, <code>above</code>, <code>across</code>, <code>after</code>, <code>against</code>, <code>along</code>, <code>among</code>, <code>around</code>, <code>before</code>, <code>behind</code>, <code>below</code>, <code>beneath</code>, <code>beside</code>, <code>between</code>, <code>beyond</code>, <code>despite</code>, <code>down</code>, <code>during</code>, <code>except</code>, <code>inside</code>, <code>into</code>, <code>like</code>, <code>near</code>, <code>off</code>, <code>onto</code>, <code>opposite</code>, <code>outside</code>, <code>over</code>, <code>past</code>, <code>since</code>, <code>through</code>, <code>toward</code>, <code>under</code>, <code>underneath</code>, <code>until</code>, <code>upon</code>, <code>versus</code>, <code>via</code>, <code>with</code>, <code>within</code>, <code>without</code>). The Chicago lowercase list is roughly twice the size of AP's.</li>
<li><strong>Wikipedia</strong> is a middle ground. Its lowercase set includes coordinating conjunctions, the article <code>the</code>, and short prepositions — but excludes some of the longer ones Chicago lowercase rules out.</li>
<li><strong>Simple</strong> ignores all of that. Every word capitalizes. Useful for button labels and one-off UI strings where you do not want surprises.</li>
</ul>

The **first** and **last** words of a title are always capitalized in all four styles — even when they would otherwise be a function word. The word after a colon, em-dash, or sentence-ending punctuation is also capitalized, because it starts a subtitle. These two rules together catch most of the edge cases where a quick script produces something embarrassing.

## How a clean converter handles hyphenated compounds

Take the input `a well-balanced approach to machine learning`. The naive capitalize-every-word approach gives you `A Well-balanced Approach To Machine Learning`. Three of those five words are wrong: `Well-balanced` should be `Well-Balanced` (both parts of a hyphenated compound are capitalized), and `To` should be `to` because it is part of the infinitive phrase and AP/Chicago/Wikipedia all lowercase `to` in that position.

[Run the same string through the Chicago-style editor to compare](https://elysiatools.com/en/tools/title-case-converter). The output `A Well-Balanced Approach to Machine Learning` matches what a copy editor would write, and `Well-Balanced` does not look like a typo. Contractions survive intact — `Don't` stays `Don't`, `O'Connor` stays `O'Connor`, and possessives like `Tom's` are not split. The converter does not lowercase the second letter of `McDonald` or `iPhone` because those are proper nouns, and the title-casing rule does not apply to letters inside a word.

## Subtitles, colons, and em-dashes

A title like `the lord of the rings: return of the king` is the test case that breaks most homegrown title casers. The colon introduces a subtitle, and the rules split cleanly: in the main title (before the colon), `of` and `the` stay lowercase in AP; in the subtitle (after the colon), the first word `Return` is capitalized and the function-word rules resume. The expected output is `The Lord of the Rings: Return of the King`. A script that just capitalizes everything produces `The Lord Of The Rings: Return Of The King`, which reads like a textbook example of how not to headline a sentence.

Em-dashes work the same way. `an introduction — what you need to know` becomes `An Introduction — What You Need to Know`. The first word after the em-dash starts a new clause and gets a capital. The function-word rules resume afterward.

## Why this is not the same as "capitalize every word"

A capitalize-every-word script has three real failure modes:

<ul>
<li><strong>It capitalizes function words that should be lowercase</strong>, producing <code>Of</code>, <code>The</code>, <code>And</code>, <code>To</code> in positions where they should stay small. The visual effect is a headline that looks like a first-grade worksheet.</li>
<li><strong>It mangles hyphenated compounds</strong>, either lowercasing the second part (<code>Well-balanced</code>) or treating each half as a separate word and applying inconsistent capitalization.</li>
<li><strong>It mishandles subtitles and colon-separated phrases</strong>, because the rule "always capitalize" does not encode the "first word after a colon is a fresh clause" rule.</li>
</ul>

Title Case Converter is opinionated about all three. The 1400-character `detail` panel in the source lays out the exact function-word list per style, the hyphenation rule, the colon rule, and the contractive-possessive handling — see the live tool for the full reference.

## A practical test set to compare styles

If you want to see the four styles diverge in one screen, run these inputs through the [Title Case Converter](https://elysiatools.com/en/tools/title-case-converter) editor and toggle between AP, Chicago, Wikipedia, and Simple:

| Input | AP | Chicago | Wikipedia | Simple |
| --- | --- | --- | --- | --- |
| `the art of war` | The Art of War | The Art of War | The Art of War | The Art Of War |
| `a guide to style` | A Guide to Style | A Guide to Style | A Guide to Style | A Guide To Style |
| `inside the c++ object model` | Inside the C++ Object Model | Inside the C++ Object Model | Inside the C++ Object Model | Inside The C++ Object Model |
| `what's next for ai?` | What's Next for AI? | What's Next for AI? | What's Next for AI? | What's Next For AI? |

The contractions stay clean, the function words stay small, and only Simple has every word capitalized. For the `C++` and `AI` cases, note that the converter recognizes common acronyms and applies the chosen style consistently — AP normalizes `NASA → Nasa` in running text but leaves `AI` as `AI` because it is a recognized initialism.

## Common pitfalls when implementing your own

If you are writing a title caser yourself, the five rules worth implementing first are:

<ul>
<li>Always capitalize the first and last words of the title.</li>
<li>Lowercase the function words in the chosen style, but only in interior positions.</li>
<li>Capitalize the word after every <code>:</code>, <code>&mdash;</code>, <code>?</code>, or <code>!</code> that splits the title.</li>
<li>Treat each half of a hyphenated word as its own token for capitalization.</li>
<li>Leave contractions and possessives alone.</li>
</ul>

The fifth rule catches the edge case where a naive script decides to "clean up" <code>O'Connor</code> into <code>O'connor</code> or <code>Don't</code> into <code>Don'T</code>. Title Case Converter handles these as opaque tokens: anything that already contains an apostrophe is treated as a single word, and its existing capitalization is preserved unless the word is at the start or end of the title.

## Edge cases the four styles agree on

Most real titles do not contain enough function words to surface differences between AP, Chicago, and Wikipedia. Run `the art of war` through the converter and all three editorial styles agree on `The Art of War` — none of them touch `of` differently. Same with `inside the c++ object model` (all three render it as `Inside the C++ Object Model`) and `a guide to style` (all three render `A Guide to Style`).

The styles diverge only when the title contains a function word that one guide treats as lowercase and another treats as uppercase. Chicago's longer preposition list is the most common source of disagreement: `above`, `across`, `behind`, `beneath`, `beyond`, `despite`, `during`, `inside`, `outside`, `through`, `toward`, `underneath`, `versus`, and `via` lowercase in Chicago but stay capitalized in AP. Try `the view from above` in both styles to see Chicago produce `The View from Above` and AP produce `The View From Above`.

## When to use which style

For newsroom-style headlines and feature titles, use **AP**. For book titles, paper titles, and academic work, use **Chicago**. For blog post titles that are also URLs (Wikipedia article titles, for instance), **Wikipedia** is the middle ground that matches how search engines tend to render article titles. **Simple** is for UI strings and button labels that need consistent capitalization regardless of grammar.

The choice affects the look more than the meaning. A reader will not notice the difference between `The Art of War` and `The Art Of War` in isolation, but a publication's house style is the difference between a well-edited title page and a list of capitalized random words. Title Case Converter encodes those four houses in a single editor so you do not have to remember which function words go lowercase where.

The four style guides are English-centric, and the function-word lists assume English-language articles and conjunctions. For French, German, Spanish, and other languages with different article systems, the same four style options give you different results because the lowercase lists do not transfer cleanly. If you are working in another language, the cleaner workflow is to apply Title Case for English-only titles and to use a language-specific casing tool for non-English text. For multilingual content, run Title Case Converter on the English portion and accept that non-English titles need manual review — the function-word lists are not a localization file you can swap out.

Explore more text-formatting tools at [elysiatools.com](https://elysiatools.com/en/tools).
