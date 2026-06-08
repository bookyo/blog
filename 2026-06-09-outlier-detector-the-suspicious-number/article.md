---
title: Why Your Best Sales Rep Is Quietly an Outlier in Your Spreadsheet
---

The "weird" data point you almost deleted this morning might be the most important number in your dataset. Pick the wrong definition of "outlier" — say, a $1.2M deal in a column where the rest is $50K — and you can quietly fire your best salesperson, miss a fraud signal, or scrap a breakthrough experiment. We will look at all three common methods — IQR, Z-score, and modified Z-score — through one spreadsheet, and you will see why two of them quietly agree for the wrong reason. Which method should you trust when the answer matters?

## A sales dashboard and a quiet panic

A regional sales manager pulls last quarter's numbers into a spreadsheet. Eleven reps closed between forty-eight and sixty-two deals. One rep, Maria, closed eighty-four. The bar chart has a single bar that looks like it wandered in from a different dataset. Before the manager fires off a Slack message asking Maria to "explain the data," she pastes the column into an [outlier detector](https://elysiatools.com/en/tools/outlier-detector) and runs three methods back to back.

The IQR rule, the workhorse taught in any intro stats class, says: Maria is in. The Z-score rule, the default in Excel's data analysis pack, says: Maria is in. The modified Z-score rule — the one nobody runs by default — says: Maria is in too, but the threshold is much tighter, and the exact same numbers in a smaller dataset would have flagged her.

That quiet difference is the whole game. Two of those three answers were produced by methods that assume your data is roughly bell-shaped. If it isn't, the methods agree with each other for the wrong reason.

## The definition hides an assumption

A statistical outlier is a value that is unlikely under the model you've assumed for the rest of the data. Notice the load-bearing word: *assumed*. The definition does not say "unusually large" or "unusually small" in the day-to-day sense. It says: improbable given the distribution I have chosen to fit. Change the distribution, change the verdict.

This is why two analysts can look at the same column of numbers and disagree about which rows are outliers. Both are running math correctly. They are applying different assumptions about what "normal" means, and the data is not telling them which assumption is right. That indirection is the source of most practical mistakes people make with outlier detection. The tools don't return a single answer. They return a verdict conditional on a model you didn't know you were picking. Change the model, prove the data fits it, and the verdict shifts.

## The IQR rule: simple, stubborn, and quietly biased

The interquartile range method sorts the data and splits it into four equal pieces. The middle 50% sits between the first quartile (Q1) and the third quartile (Q3). Anything below Q1 minus 1.5 times the IQR, or above Q3 plus 1.5 times the IQR, gets flagged.

The rule has a strange property. It assumes the data is roughly symmetric and ignores how far the extreme values are from the bulk. A point 0.1 units past the fence is treated identically to a point 100 units past it. The flag is binary — fence or no fence — and the actual magnitude of the deviation is thrown away.

For Maria's sales numbers, IQR works well. The dataset is small, roughly symmetric, and the extreme value is far enough from the next-highest that the fence cleanly separates them. The rule does what the textbook promises. Where it breaks down is on small samples (under roughly twenty points) and on heavy-tailed distributions, where the fence itself becomes unstable because Q1 and Q3 shift around as you add or remove a single row. If you can change the result by changing one row, the rule is not detecting structure — it is amplifying noise.

The reason IQR is still the default in box plots, in Tukey's original framework, and in most data science courses is not that it is the most accurate. It is that it does not require you to assume a shape for the data. It is the most *assumption-light* rule, and that is a virtue in exploratory work where you do not yet know what the data is doing.

## The Z-score rule: Gaussian, fragile, and everywhere

The Z-score rule computes the mean and standard deviation of the column, then flags any point that is more than 2 or 3 standard deviations from the mean. It is the workhorse of quality control, anomaly detection pipelines, and the "anomaly" function in any database built after 2010.

The Z-score rule has a hidden dependency. It assumes the data is approximately Gaussian — the famous bell curve. Under that assumption, a threshold of 2 standard deviations catches about 5% of points in a clean distribution. A threshold of 3 catches about 0.3%. These numbers are why the Z-score rule feels so satisfying in textbooks. The math is closed-form, the cutoffs are clean, and the answer comes with a confidence interval.

In the real world, the Gaussian assumption is almost always wrong. Sales data is log-normal, not Gaussian. Page load times are exponential. Insurance claims follow a Pareto tail. The moment you apply a Z-score rule to a heavy-tailed distribution, two things happen simultaneously: the standard deviation inflates because the extreme values pull the mean, and the resulting Z-scores compress, so genuinely anomalous points look normal. The rule is built for a world that does not exist.

Worse, the rule is self-censoring. The same outliers that should be flagged are the ones inflating the threshold that would have flagged them. The rule is robust to noise and blind to signal in exactly the situations where you most want it to work. A security team that monitors page latency with a Z-score rule will quietly miss the exact spikes that matter, because the spikes from last month inflated the threshold that should have caught them this month.

## The modified Z-score: what statisticians reach for when the data is dirty

The modified Z-score replaces the mean and standard deviation with the median and the median absolute deviation, or MAD. The MAD is the median of the absolute deviations from the median. Where the standard deviation squares the deviations and amplifies outliers, the median-based estimator effectively ignores them.

The cost is interpretive. The MAD has a 0.6745 scale correction that turns it into a "robust" standard deviation equivalent, and the threshold of 3.5 is the modified rule's version of "Z equals three." The numbers look arbitrary unless you have seen them derived, which is why the rule is taught late in most curricula and is rarely the default in GUI tools.

The benefit is decisive. The modified Z-score is the only one of the three that does not change its answer when you add a single genuinely extreme point to the dataset. If Maria's eighty-four were eight hundred and four, the IQR rule would shift, the Z-score rule would shift, and the modified Z-score rule would, in most cases, simply flag the new value and stay silent about the rest.

For log-normal sales data, for latency monitoring, for any dataset where the bulk and the tail behave differently, the modified Z-score is the rule of last resort. The reason it is not the default in most tools is partly historical and partly because the median calculation is harder to vectorize. There is no statistical reason to prefer the Z-score over the modified Z-score on real-world data, only a computational one.

## A small dataset, three different verdicts

Suppose the column is `[12, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 95]`. Twelve points, the last one set apart from the rest.

- IQR: Q1 is 14, Q3 is 17, the IQR is 3. The upper fence is 21.5. Ninety-five is in, far past the fence, flagged.
- Z-score: mean is about 19.8, standard deviation is about 22.6. Ninety-five has a Z-score of 3.34, past the 3-sigma threshold, flagged.
- Modified Z-score: median is 15.5, MAD is 2. The modified Z is 0.6745 times (95 minus 15.5) divided by 2, which is roughly 26.8. Flagged, decisively.

All three agree, and the agreement is not surprising. The data is small, the outlier is dramatic, and the three methods converge on the easy cases. The disagreement shows up in harder territory: small datasets, mild outliers, and any distribution that is not roughly bell-shaped.

## A dataset where they disagree

Now consider `[12, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 28]`. Twelve points, but the high value is twenty-eight — within plausible range, just noticeably higher than the rest. The three rules split their verdict.

- IQR: same fences as before, twenty-eight is above 21.5, flagged.
- Z-score: the standard deviation is now about 4.4, the Z-score of twenty-eight is 1.86, below the 2-sigma threshold, not flagged.
- Modified Z-score: the median is 15.5, the MAD is roughly 1.5, the modified Z of twenty-eight is 0.6745 times 12.5 divided by 1.5, about 5.6, flagged.

Two methods say outlier, one says not. This is the case where the choice of rule matters most, and it is also the case where the right answer depends on the data shape. If the column is a sample of normally distributed measurements, the Z-score is the right tool and twenty-eight is not an outlier. If the column is a sample from a heavier-tailed distribution, twenty-eight is a signal worth investigating. The numbers do not tell you which world you are in. They can only answer the question you have already committed to.

## Picking the right rule for your data

For most exploratory work, run all three. The disagreements are more informative than the agreements. When all three flag a point, it is almost certainly worth a closer look. When only one flags a point, the disagreement is usually a sign that your assumption about the data shape is shaky. The point is not the verdict. The point is the conversation between the verdicts.

For automated pipelines, pick the rule that matches the data you expect to see. If the data is bounded and symmetric — physical measurements, survey responses on a fixed scale — IQR is a safe default. If the data is roughly Gaussian by construction and the sample is large, the Z-score is the right choice. If the data is heavy-tailed, has occasional extremes, or comes from a process you do not fully control — sales, latency, claims, sensor readings — the modified Z-score is the rule that will not quietly mislead you.

## Closing

The next time a chart shows a single suspicious bar, resist the urge to delete the row. Paste the column into an [outlier detector](https://elysiatools.com/en/tools/outlier-detector), run the three rules, and read the disagreements. The method you choose encodes an opinion about what "normal" means, and the wrong opinion can quietly delete your most valuable data point. The right opinion is rarely obvious in advance, and the safest habit is to ask the data the same question three different ways before you trust the answer.

The detector is one piece of a larger toolkit. It works best when paired with the box plot generator, the dataset quality profiler, and the quartile calculator — each one offers a different lens on the same question. The most reliable answers come from looking through more than one. So the next time the question is *is this row an outlier?*, the answer that matters is: which rule did you run, and which assumption did it encode? For a wider view of how detection rules interact with real data shapes, [browse the rest of the Elysia Tools collection](https://elysiatools.com/en/tools).
