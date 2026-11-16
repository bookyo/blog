---
title: Your Footnote Proves a Source Exists, Not That It Supports the Claim
---

A citation checker returned a 3-row table for a 3-claim paragraph: 2 rows said sourced, 1 said ambiguous. I opened the third footnote and found a landing page with no numbers on it. The table was not wrong about the words, but it was answering a narrower question: who was named, not what the source says. A footnote proves a source exists. It does not prove the source supports the claim.

That gap is why the [Claim–Evidence–Citation Mapper](https://elysiatools.com/en/tools/claim-evidence-citation-mapper) is worth reading the way you read a compiler warning, not the way you read a verdict. It lives under Text Processing at [Elysia Tools](https://elysiatools.com/en/categories/text-processing). What follows is where the measurement stops, and what the four flags buy you.

## One regex decides what counts as a citation marker

Before any model is called, a local pass walks the raw document data looking for three shapes: bracketed numbers, Markdown links, and whatever pattern you supply.

The bracket pattern accepts `[1]`, `(1)` and `{1}`, and it treats the opening and closing characters as independent, so `[1)` and `(2]` are markers too. Two consequences follow. A bracketed year is not a marker, because the pattern caps at three digits, so `[1880]` stays prose. And a parenthetical number in a mathematics sentence, `(2)` as "case two", becomes a citation marker the document never made. The badge inflates, nothing warns you, and a stray amplitude label increases the count without adding a single source.

Markdown links count only inside a narrow window: link text of 1 to 60 characters, URL of 4 to 200. A short `[x](y)` is invisible to the scan, and a footnote written as a bare superscript, for instance, never appears in the count at all.

Your own regex runs after those two passes, compiled in global mode. An invalid pattern is swallowed silently, so you get the two built-in passes and no error telling you the pattern you wrote never ran. Test it on a sample first. A pattern that matches nothing produces the same output as a document with no citations.

## The marker count includes your bibliography

The local pass reads the whole document string, so the count is measured over text you may have pasted for context. When your reference list sits in that same field, each entry starting `[1]` or `[2]` is a marker as well.

A twelve-claim section with a twelve-entry bibliography pasted into the text field reports twenty-four markers. Move the same bibliography to the citations field, which the tool keeps separate, and the badge drops to twelve. Same document, half the number. Neither reading is wrong. Only one of them is the number you wanted. One rule covers all of it: Remove the bibliography from the text field before you run anything.

## Claim extraction stops silently at 24,000 characters

The form accepts up to 30,000 characters. The model call sends the first 24,000 of them through `text.slice(0, 24000)`.

The consequence is a table that quietly describes the top of your document. Paste 28,000 characters of literature review and append your discussion, and the discussion gets zero rows, with nothing in the output saying why. The badge counts markers across all 30,000 characters while claim extraction covers 24,000, so the two figures are not even measured over the same span. Cut the document yourself before the ceiling forces an arbitrary split.

Five minutes per section buys the guarantee that no claim was skipped. That is the cheapest insurance in the workflow, and the panel will never suggest it.

## Four risk flags, none of them a measurement

Each row is labelled `sourced`, `weak source`, `no source` or `ambiguous scope`, and the summary panel shows counts grouped by label. All four labels come from the model, at temperature zero, each with a short reason string in the note column.

No code in the tool compares your sentence to the reference data. So "0 unsourced" is a statement about the labels the model chose, not a statement that your claims are supported. The count is reported by the model, graded by the model, and scored by the model. Replace the label with one read citation and the claim becomes yours to defend.

Two of the flags are cheap to falsify by hand. Open the citation the model called sourced, read the abstract, and compare it to your sentence. In the worst case you find a study that says something adjacent, which is how most weak sources earn their label.

The larger asymmetry is what never reaches the table. A factual claim the model did not extract has no row, no label, and no place in any count. Each number in the summary is a fraction of extracted claims, and the denominator moved without announcement.

## The claim badge and the summary rows can disagree

The top badge prints the length of the claims array. The summary counts by status through a lookup with four keys. When the model returns a status outside that set, the row falls back to "no source" for display while the counter writes a fifth key that no summary row prints.

The result is a badge reading nine claims above four rows that sum to eight. It is a small defect, and it matters because it is the reason to reconcile totals by hand, never by squinting at the panel, and to clarify which figure you quote in a report.

The same all-or-nothing rule governs the model reply. The parser matches a greedy brace span and hands it to `JSON.parse`. When the reply is truncated at the 6,000-token ceiling, parsing throws, the catch block discards the entire result, and the footer reads "AI mapping unavailable". You see zero claims and a note about the API, while the model had labelled most of your document. A forty-claim paper hits that ceiling long before it hits the character limit.

## Local-only mode is the honest default

The AI checkbox starts off, and the local result is more useful than it sounds, because it is the only deterministic part of the tool. It touches no model and interprets none of your data.

With AI off you get a marker count, a citation count, and a note that claim extraction needs the model. Those two figures catch one class of problem cheaply: markers that outnumber references, or references that never appear in the text. Twelve markers against twelve references is your benchmark. They do not tell you which marker is orphaned, since pairing markers to entries is the model's job, so treat the pair as a tripwire, not a diagnosis. Two observed counts beat one inferred label. Build the habit of running it local-only before you switch the model on.

## A run through the tool's own climate fixture

The shipped example is three sentences and two references:

<ul><li>Global temperatures rose about 1.1°C since 1880 [1].</li><li>Sea level may reach +1 m by 2100 (2).</li><li>Renewable capacity tripled last decade.</li></ul>

The local pass finds two markers, both bare digits underneath the brackets: 1 and 2. Citations count two. With AI enabled the mapping table has three rows, and one of them is unsourced, because the third sentence carries no marker at all. Evidence for the other two resolves to the reference line the position points at.

That third row is the whole argument for running the tool. Not the two confirmations, which you could have produced yourself, but the one sentence you wrote from memory and never sourced. A checker that finds that row and nothing else has earned its place in the workflow. The example is also a fair benchmark for the ceiling: three claims fit inside the 6,000-token reply with room to spare, and a real paper will not. [Run your own draft through it](https://elysiatools.com/en/tools/claim-evidence-citation-mapper) and watch which rows come back empty.

## Treat the table as a question list, not a verdict

Read the output as questions for your own document. Is this citation the right one? Does that ambiguous marker cover the whole sentence or only half of it? Which claim did I state with more confidence than the research supports?

That reading changes what a low unsourced count means. It is not a grade. It is the number of claims the model happened to notice and could not attach to anything. According to the footer of the panel, each mapping is a suggestion to verify, and that line is more honest than the counts above it. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

None of this makes the mapping table wrong. It makes the table smaller than the document, and it makes each label an opinion with a reason attached. Run it before you submit, fix the rows it complains about, and then read the three citations you were most sure of. The point is that the ones you are sure of are the ones you never checked. Which citation in your draft have you not opened since you pasted it?
