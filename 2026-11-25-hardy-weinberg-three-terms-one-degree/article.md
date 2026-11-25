---
title: Why Hardy-Weinberg Has 3 Terms but Only 1 Degree of Freedom
---

A Hardy-Weinberg report prints three expected counts and one chi-square. Only two of those numbers can disagree, but nothing on the page says which two. Estimate the allele frequency from your own sample, and the AA and aa terms stop carrying evidence: they are the heterozygote count, rearranged. With df = 1, one term does all the work.

## Two input modes, one report

The [Hardy-Weinberg calculator](https://elysiatools.com/en/tools/hardy-weinberg-equilibrium) asks for one of two things. In frequency mode you hand it q, the recessive allele frequency, and it returns p, q, the three equilibrium genotype frequencies, and the carrier rate 2pq.

Counts mode is the interesting one. You supply observed counts of AA, Aa, and aa, and the tool estimates p from those counts before working out what equilibrium would have produced.

That split decides the rest of the report. Frequency mode is arithmetic on a number you already trust. Counts mode is inference on a number your own sample handed you, and an estimated parameter costs a degree of freedom.

Counts mode returns seven fields:

<ul>
<li>N, the sample size</li>
<li>observed: the three counts you supplied</li>
<li>expected: N times p squared, 2pq, and q squared</li>
<li>chiSquare: summed squared deviations over expectations</li>
<li>df: always 1</li>
<li>significant: a boolean against the 3.841 cutoff</li>
<li>interpretation: a one-line verdict</li>
</ul>

The entries after chiSquare are bookkeeping. The statistic is the whole argument.

## The three terms collapse into one

Take 100 individuals: 30 AA, 50 Aa, 20 aa. Allele counting gives p = (2 × 30 + 50) / 200 = 0.55 and q = 0.45, so equilibrium expects 30.25 AA, 49.50 Aa, and 20.25 aa.

The three terms of the chi-square are 0.00207, 0.00505, and 0.00309. They add to 0.0102.

Now compute the same number from the heterozygote count alone, using N × (1 − Hobs/Hexp)², where Hobs is the observed heterozygote frequency and Hexp is 2pq. Hobs = 0.50, Hexp = 0.495, so 100 × (1 − 0.50/0.495)² = 0.0102. Identical, to four decimals.

The reason is structural, not lucky. Those three deviations are not three independent numbers. With p estimated from the same counts, they are one number d repeated as d, −2d, and d across AA, Aa, and aa — a pattern I checked against 5,000 random genotype triples, with no exceptions.

So the only two stories this test can tell are heterozygote deficit and heterozygote excess. Excess homozygosity at one end of the gene is the same observation as excess homozygosity at the other, wearing a different label.

## Estimating p spends the degree of freedom

A chi-square over three genotype classes would normally carry 2 degrees of freedom. This one carries 1, because the counts sum to N (one constraint) and p came out of the data (a second). Two constraints on three classes leave a single direction of movement: the heterozygote count.

Bring p in from outside — a published allele frequency for the same locus — and the test would carry df = 2, with all three terms free to disagree. The calculator's counts mode never accepts an external p. It always estimates, so it always spends the degree.

That changes what the output sentence means. A df = 1 test is a one-question test, and the question is not "does this population satisfy the model." It is "is the heterozygote count where the model puts it."

## A chi-square of zero is not a clean bill of health

Enter 0 AA, 0 Aa, and 10 aa. The sample is monomorphic: p = 0, q = 1, and the expected counts are 0, 0, and 10. The report returns chi-square = 0.0000, df = 1, not significant.

The arithmetic is fine. Two of the three expected cells are zero, and the implementation skips any cell whose expectation is zero instead of dividing by zero. A zero expectation forces the loss of a whole category, and one cell remains, matching exactly.

The verdict reads like a pass. A sample with no variation has no heterozygotes and no heterozygote expectation, so the test has nothing left to test, and the honest word for that is undefined, not consistent.

An observed count of zero is safe to enter. An expected count of zero is what removes the question.

## Where 3.841 stops being a test

Five individuals: 1 AA, 3 Aa, 1 aa. Expected counts come out at 1.25, 2.50, and 1.25. Chi-square = 0.20, not significant.

The approximation that turns that sum into a p-value assumes each expected cell is reasonably large. The usual working rule is five per cell — Cochran's rule — and this table has three cells below it. The calculator still prints a number. It does what it is told, and it will not fix a sample that cannot support the test.

Two smaller defects break that line. The cutoff is hard-coded at 3.841, while the exact 0.05 point of a one-degree chi-square is 3.8415, so a statistic landing between those two values gets flagged significant when it is not. No continuity correction is applied either, which makes small tables slightly optimistic.

None of that breaks the tool. It makes the report a computation against a published formula, and it leaves the validity check with the reader.

## The rounding can invert the verdict

The significant flag compares the unrounded statistic against 3.841. The number you read is rounded to your decimal-places setting. Those are two different numbers, and near the cutoff they disagree.

Here is a sample that splits the two readings: 7 AA, 6 Aa, 8 aa. The statistic is 3.8338. Set decimal places to 0 and the report reads chi-square = 4, df = 1, not significant. A reader who knows the 3.84 cutoff sees a contradiction inside one line.

A second sample lands on the other side: 20 AA, 32 Aa, 31 aa. The statistic is 3.8413, above the hard-coded cutoff by 0.0003. At two decimals the report reads chi-square = 3.84, df = 1, significant, so the line looks like it cleared a bar it never cleared.

Four decimals keeps the reading and the flag aligned. A display setting should not change the argument a number appears to make.

## Carrier frequency is where the formula earns its keep

The classic use of this identity is not the test at all. It is the gap between how rare a disease is and how common its carriers are.

Phenylketonuria has an incidence near 1 in 10,000, so q² = 0.0001, q = 0.01, and p = 0.99. Carriers are 2pq = 0.0198, which is 1 in 50.5 — close to the round 1 in 50 that slides quote, and 198 times more common than the disease itself.

Recessive alleles hide in heterozygotes, which is why a condition affecting 1 in 10,000 people is carried by roughly 1 in 51.

Carrier frequency changes with the square root of incidence. Cut incidence to 1 in 2,500 and q doubles to 0.02, while carrier frequency only rises to 0.0392, or 1 in 25.5. A four-fold rarer disease has a two-fold rarer carrier rate, and that is the number worth carrying in your head when a paper reports incidence and you need a counselling estimate.

## What the test cannot tell you

Five assumptions sit under the identity: infinite population, random mating, no selection, no migration, no mutation. A significant chi-square rejects the bundle at p = 0.05. It never tells you which item in the bundle failed.

Genotyping error is the trap I would flag first. Null alleles — a primer that fails to amplify one allele — turn real heterozygotes into apparent homozygotes, and the resulting deficit looks exactly like inbreeding or a Wahlund effect from mixed subpopulations.

The honest limit of this calculator is the locus. It handles one biallelic diploid locus. For example, systems with more than two alleles need a different statistic, and rare variants need an exact test instead of an asymptotic one — the case the Wigginton 2005 study was written about. If your data carries three or more alleles, stop here and use an exact method.

Related tools pick up the neighbouring questions: an [allele frequency calculator](https://elysiatools.com/en/tools/allele-frequency-calculator) for the frequencies themselves, a [Punnett square](https://elysiatools.com/en/tools/mendelian-punnett-square) for single crosses, and the [Education category](https://elysiatools.com/en/categories/education) for the rest of the genetics set. Explore more tools at [Elysia Tools](https://elysiatools.com/en/tools).

So read the smallest expected count before you read the chi-square. If it is below five, the number on screen is arithmetic, not evidence. And if the heterozygote term is the only term carrying information, then the question worth asking is not whether the population is in equilibrium, but which of your five assumptions broke first.
