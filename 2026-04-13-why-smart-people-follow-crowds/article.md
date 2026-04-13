# Why Smart People Follow Crowds (And Why It Breaks Everything)

You are choosing a restaurant. Option A is empty. Option B has a line of twenty people. You open your phone to check ratings—but before you read anything, you look at the line. Which one do you pick?

If it was B, you just participated in an information cascade. Your decision was rational. That is exactly the problem.

![Information Cascade: Your Decision Was Rational](https://blog.flowrust.com/wp-content/uploads/2026/04/cascade-hook.png)

The Information Cascade Simulator on ElysiaTools lets you test this yourself. Built on the 1992 Bikhchandani-Hirshleifer-Welch model, it shows how cascades form, persist, and occasionally break—across financial markets, social movements, and everyday choices. No install. No signup. Just open and run.

## The Mechanism

A group makes sequential binary decisions. Each person sees a private signal about which option is better. They also see what everyone before them chose.

Early people follow their private signals. Normal. By the fourth or fifth chooser, something shifts. They look at the pattern and think: these people probably have good signals. Even if mine says B is better, the crowd is more informative now. So they follow the crowd.


![The Cascade Locks In](https://blog.flowrust.com/wp-content/uploads/2026/04/cascade-lockin.png)

The cascade locks in. Option B might be objectively better—but the chain has already converged. Private information gets discarded. Not because anyone is irrational. Because everyone, individually, made the locally correct call. The collective result is a disaster.

## The Financial Version

This plays out at scale in financial markets. An asset starts at fair value. Early investors buy based on fundamentals. Their buying draws attention. Later investors see the activity and pile in—not because they have private evidence the asset is worth more, but because watching others pile in is itself evidence worth following.


![$10 Trillion: One Cascade](https://blog.flowrust.com/wp-content/uploads/2026/04/2008-cascade.png)

This is the structural mechanism behind the 2008 financial crisis. Every major institution held mortgage-backed securities because every other major institution held them. Rating agencies used models that assumed the same crowd behavior. When the cascade broke, global markets lost roughly $10 trillion in value in weeks. The theory was published in 1992. Sixteen years later, the world ran the experiment at full scale.

Social movements follow the same logic. Revolutions seem sudden because the cascade was invisible until it hit critical mass—then everyone appeared to move simultaneously.

## The Presets Show Where It Gets Dangerous

The simulator ships with six scenarios. Run each one twice and notice how outcomes diverge based on which early choices went where.

Weak Signal is the dangerous regime. When private signals are noisy, cascades form fast and become stubborn. The system amplifies early randomness into durable collective errors. Financial bubbles operate here.

High Threshold does the opposite. When individuals require more confirming signals before following the crowd, cascades become fragile and intervention starts to work.

The most useful exercise: let a scenario cascade, flip one early decision, rerun. One early choice changes the entire trajectory. This is cascade amplification in its purest form—and it is surprisingly hard to predict without running the model.

## The implication

The people in a cascade are not irrational. They make the best decision available given their information—including the observed behavior of others. The tragedy is that individually rational behavior produces collectively catastrophic outcomes. The crowd is wrong not because its members are foolish, but because they are all running the same rational calculation simultaneously and landing in the same wrong place.

Knowing about cascades does not make you immune. The people who believe they are immune are often the most dangerous participants, because they over-trust their private signals at exactly the moment when social signals have become the more reliable guide.

Next time you catch yourself joining a crowd because everyone else seems to know something you do not, ask: am I making a decision, or has the cascade already decided?

Try the Information Cascade Simulator: https://elysiatools.com/en/visualizations/information-cascade
