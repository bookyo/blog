You Test Positive for a Rare Disease. The Doctor Says You Probably Don't.

Here's the number that surprises most people: a test for a rare disease can be 99% accurate and still produce a positive result that's wrong more than 90% of the time.

That sounds like a contradiction. It isn't. It's Bayes' theorem in action — and once you see how it works, you'll never look at medical test results, weather forecasts, or spam filters the same way again.

## The Paradox Nobody Expects

Imagine a disease that affects 1 in 1,000 people. You take a test that's 99% accurate — meaning it catches 99% of actual cases (true positive rate) and produces false alarms only 1% of the time (false positive rate).

Your result comes back positive. The doctor tells you the test is very accurate.

So how worried should you be?

Most people answer: very worried. The test is 99% accurate, after all.

But let's run the numbers on 10,000 people:

- **Truly sick:** 10 people (1%)
- **Test catches them:** 10 × 99% = 10 (all of them, roughly)
- **Healthy people:** 9,990
- **False alarms from them:** 9,990 × 1% = ~100 people

Out of 110 positive results, only 10 are truly sick. That's about **9%**. If you tested positive, the odds you actually have the disease are roughly 1 in 11.

The test isn't lying. You're just a victim of the base rate — the disease is so rare that most positive results come from the false positive pool, not the truly sick pool.

## The Formula That Fixes Your Intuition

Bayes' theorem is the mathematical tool that makes this precise. It describes how new evidence should update your beliefs:

**P(A|B) = P(B|A) × P(A) / P(B)**

Where:

- **P(A)** is your prior probability — what you believed before seeing the evidence
- **P(B|A)** is the likelihood — how probable the evidence is if the hypothesis is true
- **P(B)** is the normalizing constant — the total probability of seeing this evidence under all scenarios
- **P(A|B)** is the posterior — your updated belief after seeing the evidence

The theorem tells you exactly how much any piece of evidence should shift your confidence. It forces your intuition to be consistent.

In the disease example:

- Prior P(disease) = 0.001 (0.1%)
- Likelihood P(positive|disease) = 0.99 (99% sensitivity)
- Normalizing P(positive) = 0.001 × 0.99 + 0.999 × 0.01 ≈ 0.01098
- Posterior P(disease|positive) = (0.99 × 0.001) / 0.01098 ≈ 9%

The math and the intuition both converge on 9%.

## Why This Matters Beyond Medicine

The false positive paradox is just one instance of a pattern that shows up everywhere.

**Spam filters.** An email filter that catches 99% of spam with a 1% false positive rate sounds great — until you realize your inbox gets 10 spam emails a day and 1,000 legitimate emails. That's 10 false positives per day. The filter that seems accurate actually creates more problems than it solves.

**Airport security.** Metal detectors have a small false positive rate. But with millions of passengers, even a 0.1% false positive rate creates thousands of daily "alarms" that are actually innocent. Security staff learn to calibrate their response not to the nominal accuracy, but to the base rate of actual threats.

**Weather forecasts.** A 20% chance of rain doesn't mean "it will rain on 20% of the Earth's surface" or "20% of the day will be rainy." It means that when conditions have historically been like this, rain occurred 20% of the time. The forecast is a Bayesian update on prior odds, not a physical description.

**Legal reasoning.** In court, DNA matches are often presented as near-certain proof. But if the suspect pool is large (the true culprit could be anyone in a city of millions), a match that seems 99.9% accurate can still produce a high proportion of false convictions. The base rate of guilt in the suspect pool matters enormously.

## The Iterative Power of Bayesian Updating

Here's where Bayes gets even more interesting: the posterior from one round becomes the prior for the next.

Suppose you test positive. Your probability of having the disease, given one positive result, is about 9%. That's your new prior.

Now you take a second, independent test from a different lab. It also comes back positive. What happens now?

Now your prior is 0.09. The likelihood of a second positive (assuming the same test characteristics) is still 0.99 for someone truly sick, and 0.01 for someone healthy.

The new posterior becomes: (0.99 × 0.09) / (0.99 × 0.09 + 0.01 × 0.91) ≈ 0.91 or **91%**.

Two independent positives together are now strong evidence. This is why confirmatory testing matters — a single result in a low-base-rate environment is weak evidence; repeated confirmation moves the needle dramatically.

## The Most Important Number You're Ignoring

There's a broader lesson here that applies far beyond medical testing.

Whenever you encounter new evidence — a performance review, a stock tip, a political claim, a diagnostic result — the first question to ask isn't "how accurate is this test?" It's "how rare is what it's testing for?"

A 99% accurate test for a common condition is powerful. The same test for a rare condition is misleading in isolation. The accuracy number is only meaningful in the context of the base rate.

This is why experienced clinicians always ask about prior probability before ordering a test. They know that a test result doesn't exist in isolation — it updates a prior, and the prior shapes how much weight the new evidence carries.

It's also why good decision-makers seek corroboration before acting on single sources of information, and why the smartest people update their views incrementally rather than making dramatic leaps on one data point.

Bayes' theorem is ultimately a formal statement of intellectual humility: new evidence shifts your beliefs, but only by as much as the evidence actually warrants. Let the numbers tell you how much.

---

*Explore this interactively at [ElysiaTools — Bayes' Theorem](https://elysiatools.com/en/visualizations/bayes-theorem).*
