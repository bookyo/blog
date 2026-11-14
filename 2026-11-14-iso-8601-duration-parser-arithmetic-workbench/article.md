---
title: P1M Is Not P30D: A Duration Is a Recipe, Not a Number
---

Three durations walk into a sort function: `P1M`, `P30D`, `P4W`. A naive parser answers 30, 30, 28 days and calls the week the shortest. Anchored at 2026-01-15 the real order is `P4W` at 28 days, `P30D` at 30, and `P1M` at 31 — but anchor the same three at 2026-02-15 and `P1M` collapses to 28 days and ties the week. A duration is a recipe, not a number.

## The letter P marks a boundary, not a prefix

All of what follows depends on one structural fact: an ISO 8601 duration is not a scalar with a unit attached. It is a short program that says walk this far, in this order, from whatever date you start on. The `P` is the entry point, and the grammar around it is narrower than most string formats people handle daily.

The designators are case-sensitive. `p1d` is not a lenient spelling of `P1D`; it is a rejection with its own message, because the standard treats letter case as load-bearing. The tool's own error text shows how deliberate that is — "the designator must be an uppercase P (ISO 8601 designators are case-sensitive)". Order is fixed at years, months, weeks, days, then a `T` gate, then hours, minutes, seconds. The `T` is a boundary and not a separator, so a duration with no time part has no `T`, and `PT` on its own is not a duration at all: the standard requires a number after the gate.

Zero is a special case with exactly one correct spelling: `P0D`. Any path that ends with no remaining components collapses to it, which is why `PT0S` comes back as `P0D` and not as an empty string. That single rule kills a whole family of bugs where a computed duration of nothing serializes as a bare `P`.

## A duration is a recipe with an anchor stapled on

Take `P1Y2M3DT4H5M6S` and ask how long it is. There is no answer until you name a start. Anchor it at 2026-01-15T00:00:00Z and the tool walks the calendar in component order and lands on 2027-03-18T04:05:06Z.

The walk is worth doing by hand once, because it shows where the seconds come from:

<ul><li>One year from 2026-01-15 is 2027-01-15 — 365 days, because 2026 is not a leap year.</li><li>Two more months reach 2027-03-15 — another 59 days, being 31 in January and 28 in February.</li><li>Three more days reach 2027-03-18.</li><li>The time part adds 4 hours, 5 minutes and 6 seconds, which is 14,706 seconds.</li></ul>

That is 427 days and 14,706 seconds, or 36,907,506 seconds of elapsed time. The number is exact, and it is only exact for that anchor. Shift the start to 2027-01-15 so the year step crosses 29 February and the same string measures 36,993,906 seconds, because the year component silently picks up an extra day. One string, two answers: 36,907,506 seconds versus 36,993,906, decided entirely by the reader's start date. The year in a duration is not 365.25 days. It is "the same date, one year later", and that operation has no fixed length.

Here is the first real break from a timestamp pair. A timestamp pair is two points, and the distance between them is one number. A duration is a set of instructions for moving between points, and different instructions can produce the same displacement from one anchor and different displacements from another.

## Weeks fold into days. Hours refuse to.

The canonical form is where the format admits which units are interchangeable. The tool normalizes hard: `P3W` becomes `P21D`, `P2W3D` becomes `P17D`, `P14M` becomes `P1Y2M`, `PT90M` becomes `PT1H30M`. Each of those is a definitional conversion — a week is exactly seven days, twelve months is exactly one year, sixty minutes is exactly one hour.

Then the pattern stops. `PT36H` stays `PT36H`. It does not become `P1DT12H`, and `PT24H` never becomes `P1D`. That asymmetry is not an oversight, it is the whole point of the format: a day is not twenty-four hours in a calendar, it is twenty-three or twenty-five depending on whether a clock change lands inside it. Hours are exact and continuous. Days are nominal and local. A serializer that folds 24 hours into a day makes a timezone assumption on the reader's behalf.

The practical consequence for anyone storing durations: if you see `P1D` and `PT24H` as different strings, they are different claims. One says "same wall-clock time tomorrow". The other says "86,400 seconds from now". Around a daylight-saving transition those are an hour apart, and a system that normalizes one into the other has baked in an error that shows up twice a year and never on the test date.

## The anchor decides which duration is longer

Sorting durations is where the recipe metaphor stops being cute and starts costing you a bug. Feed `P1M`, `P30D` and `P4W` into a comparator that converts all units to days and you get 30, 30, 28 — `P1M` and `P30D` tie, and the week is smallest.

Anchor the sort at 2026-01-15 and the measured lengths are 31, 30 and 28 days, so the month is the longest of the three. Anchor it at 2026-02-15 and the month is 28 days, exactly tying `P4W` while `P30D` becomes the largest. The ordering of three fixed strings changes because nothing about the strings changed.

The only defensible reading is that a duration has no intrinsic length. "Sort these durations" is an incomplete request until you supply a date, and the request is well defined only relative to that date. This is why the tool's sort mode takes an anchor as a required input instead of offering a sort-them-all option. Any dashboard that ranks a duration column without exposing its anchor is showing you an ordering that may reverse next month.

## Fractions are exact below the T and vanish above it

The grammar allows a decimal fraction on the smallest unit present and flags the shape when the fraction sits higher up. `P1.5Y2M` still parses, but it comes back tagged non-conformant; according to the standard the fraction belongs on the smallest unit, and the tool reports "a fraction is only allowed on the smallest present unit". A decimal comma is accepted and converted, so `PT1,5H` reads as `PT1.5H` with a note.

So far so reasonable. Here is where I stopped trusting the string, and the honest part of this piece.

`P1.5Y` parses cleanly. It canonicalizes as `P1.5Y`. Anchor it at 2026-01-15 and the absolute length comes back as 31,536,000 seconds — exactly 365 days. The half-year is gone. Not rounded, not converted into roughly 182 days: dropped, because calendar arithmetic takes whole years and whole months and leaves the fractional remainder behind. `P1.5M` behaves the same way, measuring 31 days, not the 45.7 a literal reading would suggest.

Below the `T`, fractionality is real and exact. `PT1.5H` measures 5,400 seconds. `P0.5D` measures 43,200 seconds. The line is the `T` gate: time components convert to milliseconds losslessly, calendar components truncate by design, because there is no such thing as half a month.

None of the structural warnings fire here — they cover the sign, week-mixing, fraction placement and decimal commas, not truncation. I measured the truncation by porting the parser's arithmetic to Python and running both implementations on the same inputs; I observed matching second counts from both. Treat this as the one place where a well-formed duration says more than it means.

## Month-end clamping costs you invertibility

Add one month to 2026-01-31 and you cannot land on 2026-02-31. The tool clamps to the last valid day: 2026-02-28. For example, in a leap year the same operation on 2024-01-31 gives 2024-02-29, and 2026-03-31 plus one month gives 2026-04-30.

The alternative, overflowing into the next month, would move the date to 2 or 3 March and invent days that were never in the interval. Clamping keeps the answer inside the month you named, which is what a billing cycle or a subscription renewal needs. This is the rule Temporal.Duration uses, and the reason the format is worth taking seriously for anything financial.

The cost is that clamping is not reversible. Both 2026-01-30 and 2026-01-31 land on 2026-02-28 after `P1M`. Two distinct inputs, one output, no way to recover which you started from. If you need round-tripping, store the anchor date next to the duration, and stop trying to reconstruct one from the other.

## Why one year, two months, plus eleven months, minus ninety days is not minus ninety days

Component arithmetic looks associative and is not. The tool evaluates an expression term by term, carrying a cursor through the calendar, which is the only way to reach an answer that can be written as a duration.

Starting from 2026-01-15, `P1Y2M` reaches 2027-03-15. Adding `P11M` reaches 2028-02-15. Subtracting `P90D` lands on 2027-11-17. The calendar difference from the anchor back to that endpoint is `P1Y10M2D`, and the net elapsed time is 57,974,400 seconds, or 671 days.

Sum the components naively and you get zero years, zero months, minus ninety days. The naive answer is not merely imprecise, it cannot be printed as the correct duration at all, because months turned into days somewhere inside the walk and nothing in the string records where.

Two verified demonstrations of the same breakage, both from the port I ran against the tool's own arithmetic:

<ul><li>2026-01-31 plus `P1M` plus `P1M` is 2026-03-28. 2026-01-31 plus `P2M` is 2026-03-31. Three days apart, because the first step clamped and the second started from an already-clamped date.</li><li>2026-01-31 plus `P3M` then minus `P90D` is 2026-01-30. Subtract the ninety days first and then add the three months and you get 2026-02-02.</li></ul>

The order of operations in calendar arithmetic is part of the answer, and not an implementation detail. If your pipeline sums durations in a database and applies the total once, it will disagree with a pipeline that applies them one at a time — and both will look correct on a test date that never clamps.

## What to check before you trust a duration string

Five questions catch nearly each defect I found while working through this format:

<ul><li>Is the anchor stated wherever a duration is compared, sorted or totalled? Without it, the comparison is undefined.</li><li>Does a duration carry a fraction on years or months? That fraction gets dropped during calendar arithmetic.</li><li>Does the string start with a sign, or mix weeks with other units? Both are ISO 8601-2 extensions that plain 8601-1 parsers reject outright, so one file can validate in one service and break another.</li><li>Are two durations with different designators being ranked directly, like `P1M` against `P30D`? Convert both against a real anchor first.</li><li>Does the pipeline add months before or after subtracting days? The answer differs, and the difference reaches production.</li></ul>

For a scratchpad covering all five, the [ISO 8601 Duration Parser and Arithmetic Workbench](https://elysiatools.com/en/tools/iso-8601-duration-parser-arithmetic-workbench) runs parse, expression, sort and diff modes against a single anchor field you control. For the reverse direction, going from a human phrase like "three years two months fourteen days" to a conformant string, the [duration builder](https://elysiatools.com/en/tools/iso-8601-duration-builder) covers the same edge cases from the other side; its own reported example, `P1WT12H`, is a weeks-plus-time mix that plain 8601-1 rejects. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

I opened this piece expecting a formatter — a tool that takes `P1Y2M3D` and hands back something tidier. That was wrong. Each number here is conditional: 36,907,506 seconds if you start on 2026-01-15; 28 days for `P1M` if the month is February. So what is your duration column storing — a length, or a promise about a calendar you never passed in? Keep the calendar in the loop, or keep explaining the missing day.
