---
title: Your Fixed-Width File Has 3 Lengths, Not 1
---

Three lines of a padded export. The parser splits them the way I meant: each value lands in the right field, nothing is dropped, no error is raised. And the report says zero valid rows. Then I added one character to one name, and the same parser renamed a column for the whole file, merging two fields into one. The anomaly count moved by one. That is the trap in fixed-width parsing: the report hands you length numbers, but you read them as data numbers.

I ported the 247-line TypeScript source of this parser into Node and replayed its own two published examples first, to prove the port was faithful. Both matched: `rows.0.NAME = Alice`, `rows.1.SCORE = 87`, `anomalyCount = 0` on the explicit-schema example; `schema.0.name = CODE`, `rowCount = 2`, one `extra-data` anomaly on the inference example. What follows is a re-run of that port, not a reading of the description.

## The unit switch is a schema switch

The tool has a `positionMode` selector with two values: `characters` and `utf8-bytes`. It looks like a display preference for offsets. It is not. It decides where columns exist.

Take two records padded with non-breaking spaces instead of ordinary ones, `A<U+00A0><U+00A0>B` and `C<U+00A0><U+00A0>D`, and run them through with no header:

<ul><li><code>characters</code> returns 2 fields. Rows come back as <code>{field_1: "A", field_2: "B"}</code> and <code>{field_1: "C", field_2: "D"}</code>.</li><li><code>utf8-bytes</code> returns 1 field. Rows come back as <code>{field_1: "A&lt;U+00A0&gt;&lt;U+00A0&gt;B"}</code> and <code>{field_1: "C&lt;U+00A0&gt;&lt;U+00A0&gt;D"}</code>. The padding is still inside the value.</li></ul>

Same bytes, same file, different table. The reason is the whitespace test, which is written twice. In character mode it is `/^\s$/`, and JavaScript's `\s` matches U+00A0 and U+3000 happily. In byte mode it is four byte values and nothing else: 9, 10, 13, 32. U+00A0 is two bytes, 0xC2 and 0xA0, and neither appears in that list. So a column of non-breaking spaces is a separator in one mode and payload in the other.

That matters because non-breaking padding is exactly what you get when something such as a spreadsheet export, a Word table, or a PDF-to-text step has been in the file's history. The padding looks identical on screen. Only the unit mode knows the difference, and it will not tell you it made a choice.

## A three-byte character has no middle

Byte mode also means a field boundary can land inside a character. The line `01 東京 99` measures 8 characters and 12 bytes. Slice bytes 3 through 9 and you get clean text back, `東京`. Slice bytes 3 through 8 and you get `東` followed by U+FFFD, the replacement character.

No exception. No anomaly. `validRowCount` counts that row. U+FFFD is a perfectly legal string, so it flows into your warehouse as a city name that matches no lookup table, and the only way you find out is a join that silently returns nothing. For example, a value of `東�` will not join to `東京` in any database, and no row-level length check can see the difference.

The same arithmetic applies at the other end. `01 😀    98` measures 11 code points, 12 UTF-16 units, and 14 bytes. The parser counts code points in character mode, so the emoji is one position. Your database's `LENGTH()` will probably tell you something else again. That is three defensible answers to "how wide is this column", and the file does not pick one for you.

## One long value renames the whole table

Here is the defect I would put on a slide. Column inference walks each position and asks a single question: is this position whitespace on all lines? One line with a value that reaches into the separator answers no, and the separator stops existing for the whole file. Note the scope of that word: whole. A single row breaks the schema for the other thousand.

Start with a header `ID   NAME      SCORE` and two records, `001  Alice     98` and `002  Bobbysonathan 87`. The name in the second record is longer than the column. Inference returns two fields instead of three: ID from 0 to 3, then NAME_SCORE from 5 to 20. The header renamer slices `Alice     98` into a field called NAME_SCORE, and the second record becomes `Bobbysonathan 8`.

Your column names in the output JSON are a function of the worst row in the input. Add a nine-character surname next month and all downstream mapping keys change, with one anomaly logged and no warning that the schema itself moved. Nine characters is a data-entry change, not a schema change, and the parser cannot tell the difference.

## The header sets the last column's width

With the "first row is header" checkbox on, inference measures the header line and uses its width as the total. Not the widest line. The header.

So a header of `ID   NAME` and a record `001  Alice` gives you a last field from 5 to 9, the value `Alic`, and an `extra-data` anomaly, because the row is 10 positions long and 10 is greater than 9. A perfectly ordinary table is reported as truncated data and stray data at the same time.

Read those two fields back: Field range: 5 to 9. Extracted value: `Alic`. Promised value: `Alice`. The fifth character never appears in any output — it is reported as surplus, not as a truncated name.

Uncheck the box and the same bytes produce a different answer: width becomes 10, the last field runs 5 to 10, the value is `Alice`, and the two length complaints become `short-row` instead. The checkbox does not relabel columns. It changes what gets extracted.

## validRowCount counts padding

Back to the three lines I opened with. Header `ID  NAME  SCORE`, records `01  Ann   98` and `02  Bob   87`. Both records parse perfectly: `Ann` and `Bob`, `98` and `87`, no truncation, no replacement characters.

`expectedLength` is the largest field end, which is 15, because that is where the header's SCORE label ends. Both records are 12 positions long. Both are flagged `short-row`. `validRowCount` is 0.

Nothing is wrong with the data. The rows are short of the header by three spaces each, and "short" is defined as an error. The tool's own first published example avoids this by padding its records out to 20 characters, which is a fine thing to do and is exactly the habit that hides the problem. Put that `valid: 0` on a dashboard and someone spends a day chasing a corruption that is a trailing-space convention.

## What it cannot see at all

Three blind spots are worth memorising, because each one ships clean.

An overlong value that stays inside the total row width is truncated in silence. A record whose name overflows its field but whose line is still the expected length produces zero anomalies, and the value stops at the field boundary. Length checks are a property of the row; truncation is a property of the field, and only one of those is being measured.

A file with lone carriage returns never gets split. Only `\r\n` is normalised. A CR-only export, which is what some legacy systems still emit, arrives as a single line, so a 500-record file parses as one row with one column and no anomaly that names the cause.

A tab-separated file is accepted. Tab is byte 9, and byte 9 is in the whitespace list. Feed the parser a tab-separated header and it returns field_2 as the literal string `NAME<TAB>SCORE`, because the tab positions do not line up across records. The wrong tool for the job gets a plausible table back instead of an error.

One more unit mismatch, in the guard, not the parser: the 100,000-character input cap is tested with `text.length`, which counts UTF-16 units, while the measurements inside count code points. Sixty thousand emoji are sixty thousand characters and a hundred twenty thousand units, so that input is rejected as too long while sitting comfortably inside the stated limit.

## A schema you can defend

Inference is a convenience. For anything that runs on a schedule, switch to schema mode and write the ranges down.

Ranges are half-open, start inclusive and end exclusive, which is the only convention that lets `0..5` and `5..15` sit next to each other without a gap. The validator rejects zero or negative starts, end at or below start, more than 100 fields, and any overlap. It also sorts the fields by start position, silently. That sort means your output key order follows byte position, not the order you typed in the JSON array, so a schema written `score, id, name` comes back as ID, NAME, SCORE.

Field names taken from a header pass through a sanitiser you should know before you rely on them. `Order ID` becomes `Order_ID`, because runs of whitespace become single underscores. `Qty (ea)` becomes `Qty_ea`, with the parentheses dropped. `ID #` becomes `ID_`, trailing underscore intact, which is the kind of detail that breaks a strict column list. A bare `#` collapses to the fallback `field_1`. Two header cells with the same text become `ID` and `ID_2`. Letters outside ASCII survive, including a euro sign.

And decide about padding explicitly. `trimValues` defaults to on. Switch it off and `001  ` keeps its trailing spaces, which is what you want if the padding is itself meaningful and what you do not want if you are about to compare the value against a key.

Explore the tool at [Elysia Tools](https://elysiatools.com/en/tools/fixed-width-column-parser), and the wider set of text-handling utilities in the [Text Processing category](https://elysiatools.com/en/categories/text-processing).

## Deterministic checks that survive all of this

Four checks, in order of how much they buy you.

Print the measured length of each extracted value, in the unit you promised, next to the value. A row-level count cannot see field-level truncation; a per-value length can, because `Alic` is four characters where you expected five to twelve.

Run the same fixture through both position modes in CI and diff the inferred schemas. If they disagree, the file contains non-ASCII padding or a multi-byte character crossing a boundary. That is a decision someone must make once, instead of a bug that breaks a batch at three in the morning.

Put a check column at the end of each record, such as a count or a checksum. A missing or misaligned column then shows as a check failure that names the record, instead of a renamed field that surfaces as a mystery three joins downstream.

Assert that the field count in the output equals the field count in your schema, per row, and fail the batch when it does not. Schema mode makes this cheap, and it converts the silent-merge class of defect into a hard stop.

I came to this wanting a better row count. What I found is that the count never measured data at all: it measured padding, and padding is the one thing a fixed-width file is allowed to get wrong without anyone noticing. That means the fix is not a stricter parser. It is a column in your own output, the byte length of each value, asserted against the width you promised. Once that column exists, the schema stops moving under you.

Which of your extraction jobs, right now, would survive if you printed that column?
