<strong>Wilks puts every lifter on one number, so a 60 kg lifter deadlifting 180 kg can finally be compared to a 120 kg lifter pulling 300 kg without anyone arguing about bodyweight.</strong> The Wilks coefficient has been the unofficial fairness layer of raw powerlifting since 1994, and a working calculator is the difference between knowing what you lifted and knowing what you lifted *relative to your bodyweight*. This field guide walks through what the score means, how to read the output, and how to use it without fooling yourself about progress.

The [Wilks Score Calculator](https://elysiatools.com/en/tools/wilks-score) accepts three inputs - gender, body weight in kilograms, and total weight lifted in kilograms - and returns the adjusted Wilks score plus the raw coefficient used to derive it. Three inputs, one number, immediate context.

## What the Wilks Score Actually Measures

The Wilks formula takes your bodyweight in kilograms as `x` and computes a polynomial coefficient `c` using gender-specific constants. The score is then `total / bodyweight ^ c` multiplied by a normalization factor of 600. The original 1994 formula, the 2020 revision by the IPF, and the Wilks 2 coefficient all share the same shape; the constants change, the math doesn't.

Concretely, the polynomial in `x` is:

```
coeff = 500 / (a + b*x + c*x^2 + d*x^3 + e*x^4 + f*x^5)
```

For males the original Wilks constants are `a=-216.0475144, b=16.2606339, c=-0.002388645, d=-0.00113732, e=7.01863e-6, f=-1.291e-8`. Females use a separate set with a much steeper falloff because lighter lifters tend to be relatively stronger in absolute terms. The calculator picks the right set automatically from the gender field, so the only number you actually need to think about is the output.

Two lifters with the same Wilks score are considered equivalent strength, regardless of bodyweight. A 70 kg male totalling 500 kg scores roughly 367 Wilks - classed Elite by most federations. A 100 kg male totalling 700 kg scores roughly 369 Wilks. Same score, very different lifters, same conversation about who is "stronger" once bodyweight is removed from the argument.

## Reading the Three Inputs

The tool exposes exactly three options, and each one is doing real work in the formula.

<ul>
<li><strong>Gender</strong> - selects which coefficient polynomial to use. The 2020 IPF GL Points formula replaced Wilks in federation use, but Wilks remains the lingua franca for gym comparisons, training logs, and informal meets. Same inputs, different scaling - if your federation publishes GL Points instead, the score you see here is the <em>Wilks</em> equivalent.</li>
<li><strong>Body Weight (kg)</strong> - the only variable in the polynomial. Range is 40 to 200 kg in 0.1 steps. Bodyweight in pounds needs to be converted first; the formula is purely metric. A 180 lb lifter is roughly 81.6 kg - close enough that rounding to 82 kg is fine for comparison but worth noting if you are chasing an exact milestone.</li>
<li><strong>Total Lifted (kg)</strong> - the sum of squat, bench, and deadlift at their best single attempts. For raw lifters, this is the bar weight, not including wraps or sleeves. For equipped lifters, the score scales with the equipment - the Wilks formula does not know about equipment, so an equipped 800 kg total and a raw 600 kg total are both scored as written.</li>
</ul>

Default values are 80 kg bodyweight and 400 kg total, which scores around 273 Wilks for a male - respectable intermediate territory.

## What a Good Score Looks Like

Wilks score bands are not standardized the way weight classes are, but a useful reference table for raw male lifters looks like this:

<ul>
<li><strong>Beginner (0-200)</strong> - first year of serious training; total under 2.5x bodyweight</li>
<li><strong>Novice (200-280)</strong> - first multi-year cycle; total around 3x bodyweight</li>
<li><strong>Intermediate (280-340)</strong> - experienced amateur; total around 4x bodyweight</li>
<li><strong>Advanced (340-400)</strong> - competitive amateur or master's-level lifter</li>
<li><strong>Elite (400+)</strong> - national-level amateur or open-class competitor</li>
</ul>

Females score slightly higher on the same relative total because the female polynomial has a steeper falloff. A 60 kg female totalling 300 kg scores around 363 Wilks, which would be roughly 305 Wilks for a 60 kg male - same lifter, different score. The score is calibrated against the entire lifting population, not against single-gender performance, so absolute comparisons across gender are direct.

## Three Worked Examples

Three lifters, same score, three completely different conversations happening on the platform.

**Lifter A: 70 kg male, 455 kg total** - scores roughly 333 Wilks. This is the gym-bro who pulls 200 kg and benches 130 kg; respectable intermediate, room to grow on bench and squat depth. The score tells you that, relative to bodyweight, he is in the middle of the pack - good enough to enter a local meet, not yet at the elite threshold.

**Lifter B: 92.5 kg male, 670 kg total** - scores around 348 Wilks. Heavier lifter, higher absolute total, but bodyweight cuts his coefficient. He would need to lift around 720 kg at the same bodyweight to break 380 Wilks. The score exposes the diminishing returns of bodyweight - every additional kilo you carry costs you coefficient unless your total scales with it.

**Lifter C: 58 kg female, 280 kg total** - scores around 372 Wilks. Lightest class, mid-range total, and the score lands in advanced territory because the female polynomial is steeper. She would not match Lifter A in absolute kilograms, but on the scoreboard she outranks him. This is exactly what Wilks is for.

## Where the Formula Breaks Down

No bodyweight-normalized score is perfect, and Wilks has three known failure modes worth knowing before you build a training plan around the number.

**At the extremes**, the polynomial over-rewards very light lifters and under-rewards very heavy lifters. A 45 kg male totalling 250 kg scores absurdly high - the formula assumes a normal distribution and the tails are statistical fiction. Federations that care about accuracy at the extremes (women's lightweight, super-heavyweight men) have moved to GL Points or DOTS for that reason.

**For equipped lifters**, the score treats the lift as if it were raw. A multi-ply squat suit adds 50-100 kg to a squat; that boost counts in your total but does not represent unassisted strength. Comparing equipped Wilks scores to raw Wilks scores is comparing apples to a juicier apple.

**For masters lifters**, the formula does not age-adjust. A 55-year-old lifter hitting a Wilks score that would be elite at 25 is genuinely impressive; the score does not know the difference.

The calculator does not enforce any of these caveats - it returns the raw Wilks number and lets you apply context. That is the right design choice for a training tool, but worth keeping in mind when comparing scores across populations.

## Using the Calculator in a Training Loop

The fastest way to get useful information out of a Wilks score is to track it across a training block, not to chase a single absolute number.

1. Compute your baseline Wilks at the start of a 12-week block. Note the inputs and the output.
2. Re-test every 4-6 weeks using the same lift attempts. Wilks is sensitive to bodyweight changes - if you cut from 85 to 80 kg, your score may go up even if your total stayed flat.
3. Look for the *coefficient*, not the score, when bodyweight is changing. The coefficient decouples the bodyweight move from the lift performance.
4. Compare against the same bodyweight class across blocks. A 90 kg lifter should only benchmark against other 90 kg lifters for trend purposes.

For meet-day scoring, the formula is the same - but the score matters less than the placement. Wilks is for your training log and your bragging rights; the placing on the day is the meet scoreboard.

## Try It on Real Numbers

The fastest way to internalize what Wilks is doing is to run three different combinations through the tool and watch the score move:

- Same total (500 kg), three bodyweights (70, 85, 100 kg) - watch the score drop as bodyweight climbs
- Same bodyweight (85 kg), three totals (450, 550, 650 kg) - watch the score climb non-linearly with total
- Same total, swap gender - watch the female score come out higher than the male score at the same bodyweight and total

Each of these is a 30-second exercise, and the pattern that emerges is more memorable than any description. The Wilks score is a tool for thinking about strength, not a verdict on it - the scoreboard rewards training that moves the coefficient, and bodyweight moves that help the coefficient are not always the bodyweight moves that help you on the platform.

A few patterns show up consistently when lifters track Wilks over a training cycle: bodyweight cuts that are not matched by total cuts cause the score to spike briefly then crash as the lifter recovers; beginners see huge coefficient gains in the first 6 months as technique improves; returning lifters recover coefficient faster than absolute total because bodyweight loss without strength loss improves the score; equipped lifters running raw blocks see their score drop even when raw strength is unchanged because the equipment is no longer in the equation.

If you want to skip the math and just see your number, the [Wilks Score Calculator](https://elysiatools.com/en/tools/wilks-score) takes three fields and gives you the score in one round trip. Plug in your last meet total, see where you sit, and decide whether the next block is about adding kilos or holding bodyweight.

## Wrapping Up

Wilks is not the most modern formula, but it is the most widely understood. A single number that puts every lifter on the same scale is more useful than three numbers that don't, and the polynomial that powers the calculation has been validated against decades of meet data.

Run your numbers through the [Wilks Score Calculator](https://elysiatools.com/en/tools/wilks-score), track the score across your next training block, and use the coefficient - not the score - to make decisions when bodyweight is moving. The formula is honest about what it can and cannot tell you; the lifters who get the most out of it are the ones who treat it as one input among many.

Explore more strength, math, and unit-conversion tools at [elysiatools.com](https://elysiatools.com/en/tools).
