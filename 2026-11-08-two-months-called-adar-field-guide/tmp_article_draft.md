---
title: Two Months Called Adar, and One Line That Chooses Wrong
---

**The Hebrew calendar's hardest arithmetic is not where it breaks.** Four postponement rules, mean lunations counted in eighteenths of a minute, a nineteen-year cycle that has to stay in step with the sun: I rebuilt all of it from the specification and every date agreed with the published calendar. Then I typed `14 Adar 5784` into the same converter and it returned February 23, 2024. Purim that year was March 24. One claim, thirty days apart, on the same screen.

The engine was not confused about leap years. It knew. It had the leap-year test written into a different line, forty lines further down.

## The hard part is the part that works

The Hebrew calendar has a reputation for being unreasonable, and the reputation is earned at the specification level: it is a completely fixed arithmetic scheme, decided in advance, with no observation of the moon required. You can compute the date of Passover for the year 7000 without looking up at anything.

The unit of the arithmetic is the part, or chelek, which is one eighteenth of a minute, about 3.3 seconds. The calendar's mean month is 29 days, 12 hours and 793 parts. Multiply that out and you get 765,433 parts, or 29.5305941 days.

The modern measured synodic month is 29.5305889 days. The gap is 0.46 seconds per month, which sounds like a rounding error until you notice it was fixed in the eleventh century, by hand, without a spreadsheet. Keep dividing and the calendar drifts about one day every sixteen thousand years.

Then there is the nineteen-year cycle. Seven of those years get an extra month, for 235 months in total, and 235 of these lunations come to 6,939.6896 days. Nineteen tropical years come to 6,939.6016 days. The excess is 0.088 days, or a little over two hours, per nineteen years.

## 793 parts is not a decorative number

Two properties of that 29 days 12 hours 793 parts are worth holding onto, because they are what make the rest of the calendar possible.

The first is its remainder in weeks. 29 days is four weeks and one day, so every month the starting point of the lunation moves forward by one day plus twelve hours and 793 parts. In weekday terms it advances by either one or two days, never more.

That single fact is why Rosh Hashanah can only ever fall on four weekdays out of seven. If the anniversary of creation could land anywhere, the calendar would need a very different set of rules. Because the miss is bounded to one or two days, four rules are enough to keep every year a legal length.

The second property is that the mean month is slightly too long for the solar year it has to live inside. Two hours per cycle is not a problem you fix; it is a problem you absorb, which the calendar does by letting the whole structure float against the equinox slowly enough that nobody notices inside a lifetime.

## Four rules stop Rosh Hashanah from landing on Sunday

The postponement rules have names, and each one exists to prevent a specific broken year rather than to be elegant.

<ul><li><strong>Molad Zaken</strong> — if the mean lunation falls at or after the eighteenth hour of the day (noon, counting the halachic day from 6 p.m.), Rosh Hashanah is pushed one day. Otherwise the new year would be declared before the moon it is counting.</li><li><strong>Lo ADU Rosh</strong> — Rosh Hashanah may not fall on Sunday, Wednesday or Friday. Each of those would create a year of an illegal length.</li><li><strong>GaTaRaD</strong> — in a common year, if the lunation itself falls on Tuesday at or after 9 hours 204 parts, Rosh Hashanah moves to Thursday, which would otherwise produce a 356-day year.</li><li><strong>BeTU-TaKPaT</strong> — after a leap year, a lunation on Monday between 15 hours 589 parts and 18 hours sends Rosh Hashanah to Tuesday, which would otherwise produce a 382-day leap year.</li></ul>

Four consecutive years show how rarely the machinery has to do anything:

<ul><li><strong>5784</strong> — lunation on Friday at 11h 882p. Lo ADU Rosh fires, Friday is not allowed, and Rosh Hashanah lands on Saturday, September 16, 2023. The year runs 383 days and is leap.</li><li><strong>5785</strong> — lunation on Thursday at 9h 391p. Nothing fires. Rosh Hashanah lands on Thursday, October 3, 2024. The year runs 355 days and is common.</li><li><strong>5786</strong> — lunation on Monday at 18h 187p. Molad Zaken fires on the eighteenth hour exactly, and Rosh Hashanah moves to Tuesday, September 23, 2025. The year runs 354 days.</li><li><strong>5787</strong> — lunation on Saturday at 2h 1063p. Nothing fires. Rosh Hashanah lands on Saturday, September 12, 2026. The year runs 385 days and is leap.</li></ul>

Two of four years needed no intervention at all. The rules are not doing constant work; they are a guard rail that catches roughly half the cases.

## I rebuilt it from scratch, and the arithmetic agreed

I expected the fault to be here. Fixed calendars are exactly the kind of thing where a sign error survives for decades because nobody outside the community checks, so I ported the whole engine into Python from the specification rather than reading the implementation, and compared it against published dates.

Rosh Hashanah came out right for 5784 through 5788, five out of five. Passover, the fifteenth of Nisan, came out right for 5784 through 5787, four out of four. That is nine dates and nine agreements.

Then a structural census over two hundred years, 5700 to 5899. Only six year lengths appeared: 353, 354 and 355 for common years, 383, 384 and 385 for leap years, which is exactly the legal set. The distribution was 18, 50 and 58 for common years and 33, 9 and 32 for leap years.

Two more checks passed. The month lengths summed to the year length in all two hundred years, with no year left one day short by a rounding slip. And 74 of the two hundred years were leap, which is 37.0 percent against the 36.84 percent that seven leap years in nineteen implies.

The arithmetic is sound. I could not break it, and I tried.

## Then there are two months called Adar

Which brings us to the part that broke, and it is not arithmetic. It is a month name.

In a common year the Hebrew calendar has twelve months, and the twelfth is Adar, twenty-nine days. In a leap year the calendar inserts a thirteenth month before it: Adar I at thirty days, plus Adar II at twenty-nine. Adar I is the extra one. Adar II is the Adar that matters.

Every practice that hangs off a date uses Adar II in a leap year. Purim is the fourteenth of Adar II. A yahrzeit observed in Adar is observed in Adar II. A bar or bat mitzvah date recorded simply as Adar falls in Adar II. This is not a scholar's refinement; it is the ordinary convention, and it is why Hebrew date inputs so often arrive with an unqualified month name.

So the question a converter has to answer is narrow and answerable: given the bare word Adar, which of the two did the person mean? Thirty-seven of the one hundred and one years from 5780 to 5880 are leap years, so the question comes up in 37 percent of all years.

## One lookup, one direction, thirty days

The converter has a table mapping month names to month numbers, and it registers the bare name with a sentinel value of minus one. A single line then resolves the sentinel:

<code>if (month === -1) month = 12;</code>

Month twelve is Adar I. Month thirteen is Adar II. So the bare name resolves to Adar I in every year without exception.

In a common year that is correct, because there is no month thirteen and month twelve is Adar. In a leap year it is wrong, and wrong in a specific direction: it returns a date exactly thirty days early.

For 5784, a leap year, the fourteenth of Adar I falls on February 23, 2024. The fourteenth of Adar II falls on March 24, 2024. The second of those is Purim. The first is a date about a month before Purim that nobody celebrates.

The fix is the branch that was omitted: resolve the sentinel as month thirteen when the year is leap, and month twelve otherwise. One conditional, two characters of intent, and the difference between a correct answer and a plausible one.

## The same page answers both ways

Here is what makes this a report rather than a bug hunt. The same engine already knows the rule.

The festival schedule is built a few dozen lines away, and the Purim entry is assembled with an explicit leap-year test: month thirteen in a leap year, month twelve otherwise. That is the correct branch, written by the same author, in the same file.

So the tool contradicts itself, and it does so visibly. Ask it for the festivals of 5784 and it tells you Purim is on March 24. Ask it to convert the fourteenth of Adar in 5784 and it tells you February 23. Two panels, one screen, thirty days.

Nor is this a tool that is vague about month lengths. It refuses the thirteenth month in a common year with a precise error naming the month and its length. It knows that a thirtieth of Adar in a common year is really the first of Nisan, and rolls it forward rather than rejecting it. The month-length machinery is careful and correct.

The defect is narrower than ignorance. One resolution path never received the leap-year test its neighbour received.

## Where this shape of bug hides next

The pattern is worth naming because it recurs in every date tool, currency converter and unit calculator you will ever use. The numeric core gets written once from a specification, reviewed against known values, and defended by tests. The input adapter gets written to be forgiving, because users type things, and forgiving code has no known values to check against.

So the core is where you look for bugs and the adapter is where they are.

The practical test takes ten seconds: pick a date whose answer you already know, and pick it in a leap year. If the converter gets that right, the arithmetic is probably fine. If it does not, you have found the seam without reading a line of source.

Two honest limits remain even after the month name is fixed. The converter maps whole civil days, so if you were born after sunset the civil date on your birth certificate is one day behind your Hebrew birthday, and no whole-day converter can close that gap without a location and a time. And the parasha schedule has to be told whether you want the Israel or Diaspora reading, because the extra festival day in the Diaspora shifts some weeks by a full portion.

Used with an explicit Adar I or Adar II, this tool is genuinely good: the postponement panel that shows which rule fired and why is the sort of thing you cannot get from a bare date lookup, and the festival schedule with the evening before each day is more than most converters bother with. You can [try the converter here](https://elysiatools.com/en/tools/hebrew-calendar-bilingual-date-converter) and read the four postponement rules against your own known dates.

I started this expecting to find the fault in the arithmetic. Mean lunations, 793 parts, four postponements, a nineteen-year cycle that has to stay in step with the sun: that is where calendars usually fall apart, and it is exactly where this one held. Nine published dates, two hundred years of year lengths, and not one disagreement.

What broke was a dictionary entry. One lookup, one direction arrow, thirty days of drift.

Which is the uncomfortable part. When a date converter hands you a confident, specific, perfectly formatted answer, it has told you nothing about whether it understood the question. The only way to catch a wrong month is to ask the tool about a date whose answer you already know, and to ask it in a leap year.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
