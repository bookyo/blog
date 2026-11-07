---
title: Two Months Called Adar, and One Line That Chooses Wrong
---

**The Hebrew calendar's hardest arithmetic is not where it breaks.** Four postponement rules, mean lunations counted in eighteenths of a minute, a nineteen-year cycle that has to stay in step with the sun: I rebuilt the whole engine from the specification and each date agreed with the published calendar. Then I typed `14 Adar 5784` into the same converter and it returned February 23, 2024. Purim that year fell on March 24. One claim, thirty days apart, on the same screen.

The engine was not confused about leap years. It knew. It carried the leap-year test in a different line, forty lines further down.

## The hard part is the part that works

The Hebrew calendar has a reputation for being unreasonable, and the reputation is earned at the specification level: it is a completely fixed arithmetic scheme, settled in advance, with no observation of the moon required. You can compute the date of Passover for the year 7000 without looking up at anything.

The unit of the arithmetic is the part, or chelek, one eighteenth of a minute, about 3.3 seconds. The molad, the "birth" of the moon, is the mean conjunction, and the calendar's mean month is 29 days, 12 hours and 793 parts. Multiply that out and you get 765,433 parts, or 29.5305941 days.

According to the measured value, the synodic month runs 29.5305889 days. The gap comes to 0.46 seconds per month, which reads as a rounding error until you notice it was settled in the eleventh century, by hand, without a spreadsheet. Carry the division further and the calendar drifts about one day per sixteen thousand years.

Then there is the nineteen-year cycle. Seven of those years take an extra month, for 235 months in total, and 235 of these lunations come to 6,939.6896 days. Nineteen tropical years come to 6,939.6016 days. The excess reaches 0.088 days, a little over two hours, per nineteen years.

## 793 parts is not a decorative number

Two properties of that 29 days 12 hours 793 parts build the rest of the calendar.

The first is its remainder in weeks. Twenty-nine days is four weeks and one day, so each month the start of the lunation moves forward one day plus twelve hours and 793 parts. In weekday terms it advances by one or two days, never more.

That single fact explains why Rosh Hashanah can only fall on four weekdays out of seven. If the anniversary of creation could land anywhere, the calendar would need a different rulebook entirely. Because the miss stays inside one or two days, four rules prove sufficient to hold each year to a legal length.

The second property is that the mean month runs slightly long against the solar year it has to live inside. Two hours per cycle is not a problem you remove; it is a problem you absorb, which the calendar does by letting the whole structure float against the equinox slowly enough that nobody notices inside a lifetime.

## Four rules stop Rosh Hashanah from landing on Sunday

The postponement rules carry names, and each one is designed to prevent a specific illegal year.

<ul><li><strong>Molad Zaken</strong> — when the mean lunation falls at or after the eighteenth hour of the day (noon, counting the halachic day from 6 p.m.), the rule forces the new year forward one day. Otherwise the calendar would declare the new year before the moon it is counting.</li><li><strong>Lo ADU Rosh</strong> — Rosh Hashanah may not fall on Sunday, Wednesday or Friday. Each of those three forces a year of an illegal length.</li><li><strong>GaTaRaD</strong> — in a common year, when the lunation itself falls on Tuesday at or after 9 hours 204 parts, Rosh Hashanah moves to Thursday. Left alone, that combination creates a 356-day year.</li><li><strong>BeTU-TaKPaT</strong> — after a leap year, a lunation on Monday between 15 hours 589 parts and 18 hours sends Rosh Hashanah to Tuesday. The unguarded version creates a 382-day leap year.</li></ul>

Four consecutive years show how rarely the machinery has to intervene:

<ul><li><strong>5784</strong> — lunation on Friday at 11h 882p. Lo ADU Rosh fires, Friday is barred, and Rosh Hashanah lands on Saturday, September 16, 2023. The year runs 383 days and is leap.</li><li><strong>5785</strong> — lunation on Thursday at 9h 391p. Nothing fires. Rosh Hashanah lands on Thursday, October 3, 2024. The year runs 355 days and is common.</li><li><strong>5786</strong> — lunation on Monday at 18h 187p. Molad Zaken fires on the eighteenth hour exactly, and Rosh Hashanah moves to Tuesday, September 23, 2025. The year runs 354 days.</li><li><strong>5787</strong> — lunation on Saturday at 2h 1063p. Nothing fires. Rosh Hashanah lands on Saturday, September 12, 2026. The year runs 385 days and is leap.</li></ul>

Two of those four years needed no intervention at all. The rules do not labor constantly, and the numbers show they catch roughly half the cases.

## I rebuilt it from scratch, and the arithmetic held

I expected the fault to sit here. Fixed calendars belong to the class of software where a sign error survives for decades because nobody outside the community checks, so I ported the engine into Python from the specification instead of reading the implementation, then tested it against the published data.

Rosh Hashanah came out right for 5784 through 5788, five of five. Passover, the fifteenth of Nisan, came out right for 5784 through 5787, four of four. Nine dates, nine agreements, and nine is a thin benchmark. So I went wider.

Then a structural census across two hundred years, 5700 to 5899. Only six year lengths appeared: 353, 354 and 355 for common years, 383, 384 and 385 for leap years, which is exactly the legal set. The distribution ran 18, 50 and 58 for common years and 33, 9 and 32 for leap years.

Two further checks passed and proved the structure sound. The month lengths summed to the year length in all two hundred years, with no year left a day short by a rounding slip. And 74 of the two hundred years were leap, giving 37.0 percent against the 36.84 percent that seven leap years in nineteen implies.

The arithmetic is sound. I could not break it, and I tried for an hour.

The honest gap: I verified against published dates for nine points in a five-year window, not against all three thousand years of the fixed era. A drift that only surfaces in the year 6000 would not show up in this test.

## Then there are two months called Adar

Which brings us to the part that broke, and it is not arithmetic that matters. It is a month name.

In a common year the calendar has twelve months, and the twelfth is Adar, twenty-nine days. In a leap year the calendar inserts a thirteenth month before it: Adar I at thirty days, plus Adar II at twenty-nine. Adar I is the inserted one. Adar II is the Adar that counts.

Each practice that hangs off a date uses Adar II in a leap year. Purim falls on the fourteenth of Adar II. A yahrzeit observed in Adar is observed in Adar II. A bar or bat mitzvah date recorded as bare Adar belongs to Adar II. This is not a scholar's refinement but the ordinary convention, and it explains why Hebrew date inputs so often arrive with an unqualified month name.

So the question a converter has to answer is narrow and answerable: given the bare word "Adar", which of the two did the person mean? Thirty-seven of the one hundred and one years from 5780 to 5880 are leap years, so the ambiguity lands in 37 percent of all years.

## One lookup, one direction, thirty days

The converter carries a table mapping month names to month numbers, and it registers the bare name "Adar" with a sentinel value of minus one. A single line then resolves that sentinel:

<code>if (month === -1) month = 12;</code>

Month twelve is Adar I. Month thirteen is Adar II. So the bare name resolves to Adar I in each year, without exception.

In a common year that answer is correct, because no month thirteen exists and month twelve is Adar. In a leap year it is wrong, and wrong in one direction: it returns a date exactly thirty days early.

For example, in 5784, a leap year, the fourteenth of Adar I falls on February 23, 2024. The fourteenth of Adar II falls on March 24, 2024. The second is Purim. The first is a date a month before Purim that nobody celebrates.

The fix takes the branch that was omitted: resolve the sentinel as month thirteen when the year is leap, and replace it with month twelve otherwise. One conditional, and the difference between a correct answer and a plausible one.

## The same page answers both ways

What makes this a report and not a bug hunt is that the same engine already knows the rule.

The festival schedule is assembled a few dozen lines away, and the code builds the Purim entry with an explicit leap-year test: month thirteen in a leap year, month twelve otherwise. That is the correct branch, written by the same author, in the same file.

So the tool contradicts itself, and the contradiction sits in plain view. Ask it for the festivals of 5784 and it reports Purim on March 24. Ask it to convert the fourteenth of Adar in 5784 and it answers February 23. Two panels, one screen, thirty days, and neither one reported an error.

Nor is this a tool that stays vague about month lengths. Take, for instance, the thirteenth month in a common year: the tool removes it with a precise error naming the month and its length, ending "no Adar II". It knows that a thirtieth of Adar in a common year is the first of Nisan, and rolls it forward instead of rejecting it. The month-length machinery is careful work.

The defect is narrower than ignorance. One resolution path never received the leap-year test its neighbour received.

## Where this shape of bug hides next

The pattern deserves a name, because it recurs in each date tool, currency converter and unit calculator you will ever use. The numeric core gets written once from a specification, reviewed against known values, and defended by tests. The input adapter gets written to be forgiving, because users type things, and forgiving code has no known values to check against.

So the core is where you look for defects and the adapter is where they live. Forgiving code builds a surface where a wrong answer arrives looking exactly like a right one.

The practical test takes ten seconds: pick a date whose answer you already know, and pick it in a leap year. If the converter gets that right, the arithmetic is probably sound. If it fails, you have found the seam without reading a line of source.

Two honest limits survive even after the month name gets fixed. The converter maps whole civil days, so if you were born after sunset the civil date on your birth certificate sits one day behind your Hebrew birthday, and no whole-day converter closes that gap without a location and a time. And the parasha schedule has to be told whether you want the Israel or Diaspora reading, because the extra festival day in the Diaspora shifts some weeks by a full portion.

Used with an explicit Adar I or Adar II, this tool earns its place: the postponement panel that shows which rule fired and why is what a bare date lookup cannot give you, and the festival schedule with its evening before each day goes further than most converters bother to. You can [try the converter here](https://elysiatools.com/en/tools/hebrew-calendar-bilingual-date-converter) and check the four postponement rules against dates you already know, or browse [the wider tool catalogue](https://elysiatools.com/en/tools) for other date and calendar work.

I started this expecting to find the fault in the arithmetic. Mean lunations, 793 parts, four postponements, a nineteen-year cycle that has to stay in step with the sun — that is where calendars usually break, and that is exactly where this one held. Nine published dates, two hundred years of year lengths, not one disagreement.

What broke was a dictionary entry. One lookup, one direction arrow, thirty days of drift.

So here is the question worth carrying away: when a converter hands you a confident, specific, perfectly formatted date, what has it told you about whether it understood the request? Nothing. The only way to catch a wrong month is to test it on a date whose answer you already know, and to test it in a leap year.
