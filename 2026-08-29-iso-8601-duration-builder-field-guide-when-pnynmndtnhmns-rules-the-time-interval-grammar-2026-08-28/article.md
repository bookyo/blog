# ISO 8601 Duration Builder: A Field Guide to PnYnMnDTnHnMnS Without the Edge-Case Foot-Guns

ISO 8601 durations — the `PnYnMnDTnHnMnS` family — look deceptively simple until you try to parse one in production. They use one shared grammar that five different libraries parse five different ways, and three of those five will silently accept `P1M30D` as if month-and-day arithmetic were well-defined. The **ISO 8601 Duration Builder** at [Elysia Tools](https://elysiatools.com/en/tools/iso-8601-duration-builder) sits squarely on this seam: it converts both directions between natural-language durations and the ISO grammar, and enforces the four edge-case rules that the standard actually publishes. This guide walks the grammar from spec to working code, highlights the four traps that ruin most naive parsers, and shows when a duration API call beats a hand-rolled regex — and when it costs you a year and a half of phantom bookings.

## Why ISO 8601's duration format exists alongside its timestamp format

ISO 8601 separates *points in time* (timestamps like `2026-08-28T17:25:32Z`) from *intervals* (durations like `P3Y2M14D`). Same standard, two different problems. Timestamps answer "when"; durations answer "how long". Most stacks store durations as either seconds-since-epoch integers (loses the meaning of months) or vendor objects (`java.time.Duration`, `moment.duration`, Python `timedelta`) that don't serialize into anything portable.

The ISO 8601 duration grammar fills that gap. It is a *descriptive* format — it does not encode a fixed number of seconds, because years and months have variable lengths. The trade-off is that arithmetic on months is calendar-aware: `P1M` plus `P1M` is `P2M`, not `P60D`. That property is exactly what subscription billing, lease terms, and service-level agreements need, and exactly what naive seconds-based systems get wrong. You can try the conversion yourself at [Elysia Tools](https://elysiatools.com/en/tools/iso-8601-duration-builder), where natural language like `3 years 2 months 14 days` resolves to `P3Y2M14D` in either direction.

The tradeoff the standard asks you to accept: any `P` string with a `Y`, `M`, or `W` component is a *calendar* interval, not a fixed-length clock interval. The library must respect calendar arithmetic to round-trip correctly.

## The five-second grammar that becomes a five-hour parser

The grammar, on paper, fits in a single regex: `^P(([0-9]+Y)?([0-9]+M)?([0-9]+W)?([0-9]+D)?)(T([0-9]+H)?([0-9]+M)?([0-9.]+S)?)?$`. The `P` opens the period, optional `T` switches into the time-of-day half, and each letter is a component. Capital `P` and `T` are mandatory. Lowercase letters are not interchangeable.

Three rules trip almost every naive implementation. First, the `T` separator must come before any time components, never before a date component — `P1DT1H` means one day plus one hour, while `P1H` is invalid because `H` is a time component requiring a preceding `T`. Second, `W` (weeks) is mutually exclusive with `Y`, `M`, and `D` because weeks are calendar-agnostic only when no other date units are around. Third, decimal fractions belong only on the smallest component — `PT1.5H` is fine, `PT0.5H30M` is not, because once you have a non-zero minutes component, the smallest granularity is minutes. The tool's detail panel at [Elysia Tools](https://elysiatools.com/en/tools/iso-8601-duration-builder) flags all three and a fourth (an empty `P` with zero components is rejected outright).

If you must hand-roll a parser, walk the string character by character with a small state machine rather than chaining regex assertions — the grammar has too many mutually-exclusive states for a single regex to catch.

## When months are months and when they are days — the calendar problem

The classic ISO 8601 debate: is `P1M` equivalent to `P30D`? Strictly, no. The standard treats months as calendar months, so `P1M` starting from `2026-01-15` lands on `2026-02-15`, which has 28 days; starting from `2026-02-15`, it lands on `2026-03-15`, which has 31 days. Same duration string, two answers.

Most stacks pick one of three resolutions. **Java's `Period`** honours calendar months exactly and refuses to compute a total-days count. **JavaScript's `Temporal.Duration`** stores components as `(years, months, days, …)` and requires an anchor date to totalise. **`java.time.Duration.seconds` conversion** silently assumes `1 month ≈ 30.4375 days` and rounds. None of them is wrong; all of them are mutually incompatible. Pick one contract for your domain and document it in the API.

The [ISO 8601 Duration Builder](https://elysiatools.com/en/tools/iso-8601-duration-builder) follows the third convention by default — `1 month ≈ 30.4375 days` and `1 year ≈ 365.25 days` — and surfaces the approximation in the "approximate total" column. For billing APIs where contracts reference "1 month of service", anchor on a calendar and stay there. For analytics where you need to bucket sessions, the approximate total is good enough.

The single best gift you can give your future self in this domain: never compute "what date is one month from now" inside a SQL query without anchoring the start date. Store the start date alongside the duration and let application code resolve the math.

## Natural-language input is the surprise second product

Type "3 years 2 months 14 days", "2.5 hours", "36 hours", or "1 week 12 hours" and the same tool emits canonical `P3Y2M14D`, `PT2H30M`, `PT36H`, `P1WT12H`. It also accepts Chinese numerals (`3天2小时`), number-words (`two`), and glued forms (`2h30m`). The parser tokenizes on whitespace and on letter-followed-by-number boundaries, then dispatches each token to either the date half or the time half based on the `T` boundary the *output* requires, not the input.

The interesting design decision: the input grammar is *lenient* and the output grammar is *strict*. A user can type "two and a half hours" and the tool resolves it. The output `PT2H30M` will never include an alternative representation. That asymmetry is what most hand-rolled formatters fail at — they either match the input pattern exactly (rigid, breaks on user variation) or roundtrip cleanly (forgiving, but emits ungrammatical outputs like `PT150M` instead of `PT2H30M`).

The other surprise: `1 week 12 hours` parses as `P1WT12H` because `W` is a calendar-agnostic component and mixing it with hours (which need a `T` separator) is allowed only by treating the week as a date unit. Validate this case before trusting any library that claims full ISO 8601 compliance.

## Where the seconds count actually starts

For most duration use cases, the *total in seconds* column is the only number downstream services read. `P3Y2M14DT36H` becomes `101,584,800` seconds (give or take a leap-year wobble). When you only need that number — metrics, TTLs, rate limit windows — the calendar semantics can be quietly dropped.

ISO 8601 distances itself from fixed-length seconds for a reason: a duration defined as "1 month" is not a fixed number of seconds, so reading `P1M` as `2,592,000` seconds breaks the next time February rolls around. The standard explicitly recommends anchoring an interval to a date when seconds matter. The [duration-builder](https://elysiatools.com/en/tools/iso-8601-duration-builder) reports both — the structured `P3Y2M14DT36H` and an approximate seconds/minutes/hours/days total — so you can decide which one your downstream actually needs.

If your consumer is a database column or a wire format, store the structured `P` string, not the seconds total. Round-tripping loses information; serialising doesn't.

## When a library call beats a regex — and when it costs you a year and a half

`java.time.Duration.parse("PT36H")` works. `moment.duration("P3Y2M14D")` also works. `libiso8601.parse` works on Linux but ships out of coredlls on Windows. The decision to depend on a parser library is not a free one.

Three cases where you absolutely want a library: production code that handles user-supplied duration strings, code that needs calendar-aware arithmetic, and code that has to round-trip the same string with the same value across process boundaries. Three cases where a regex is honestly fine: validating that an input *looks like* a duration (gate it before sending to a real parser), extracting one component from a known-shape string (`^PT(\d+)H$`), and config-file default values you control entirely on both sides of the boundary.

The grey zone is around `W`. Library support for weeks is inconsistent — some treat `P1W` as `7 days` and refuse other components; some accept `P1WT12H` and others reject it. If your code touches weeks, write a test suite of canonical input/output pairs first, then pick the library that passes it.

The honest rule of thumb: reach for a library when correctness matters more than the bytes you save, and reach for a regex when rejection is more valuable than acceptance. The duration builder at [Elysia Tools](https://elysiatools.com/en/tools/iso-8601-duration-builder) handles both directions with the validation rules baked in, which makes it useful as a reference oracle when comparing two libraries that disagree.

## Quiet landmines: the four edge cases that ruin most parsers

Even with a library, four ISO 8601 duration rules trip implementations that otherwise look correct. List them in your test suite:

1. **`PT0.5S`** — a decimal in the smallest component is valid; `PT0.5H0.5M` is not.
2. **`P` alone** — zero components is invalid; the spec requires at least one numeric component.
3. **`P1WT`** — `T` with no time components is invalid; the trailing `T` is an error, not an empty time half.
4. **`PT36H1.5M`** — decimal fractions only on the *last* component; mid-stream fractions require re-ordering the input.

The [ISO 8601 Duration Builder](https://elysiatools.com/en/tools/iso-8601-duration-builder) flags all four and includes a "natural-language → ISO" path that won't even let you type most of them — the input parser rejects `P` alone or `PT` alone, and the natural-language input skips the `T`-boundary question entirely.

If you are debugging a duration-parsing failure in production, run the suspect string through the builder and compare your library's behaviour to the tool's output. The mismatch usually points straight at the rule being broken.

## Closing the loop: pick one stack, document it, don't blend

Two engineering decisions will save you a year of debugging. First, pick *one* duration representation for your domain — `PnYnMnDTnHnMnS` strings, vendor objects, or seconds-since-epoch integers — and reject the others at your API boundary. Blending libraries is the root cause of "the same duration looks different in two services" tickets. Second, when you store a duration with months or years, *always* store the start date next to it. Without an anchor, the duration string's meaning is underdetermined, and any code that touches it later will round it the way it was taught.

The duration format is small. The semantics are not. [Try the ISO 8601 Duration Builder at Elysia Tools](https://elysiatools.com/en/tools/iso-8601-duration-builder) to round-trip your real production strings, and use the four landmines in §7 as a regression test whenever a parser upgrade is on the table. Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).
