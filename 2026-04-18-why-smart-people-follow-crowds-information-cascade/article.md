# Why Smart People Follow Crowds: The Math That Explains Every Viral Trend and Market Bubble

You walk past two restaurants. One is empty. The other has a line out the door. Which do you choose?

If you said the busy one, you just participated in an information cascade — and so did everyone else in that line.

The counterintuitive part: every single person in that crowd may have independently decided to go there based on their own research, reviews, and instincts. The line formed not because the food is better, but because the first few people happened to choose it, and everyone after that rationally ignored their own signals to follow the crowd. Each individual made a smart decision. The group behavior was irrational.

This is not a failure of human reasoning. It is a predictable mathematical consequence of it.

## The 1992 Paper That Explained Crowds

In 1992, three economists — Bikhchandani, Hirshleifer, and Welch — published a model that explained exactly how rational people create irrational herds. Their paper introduced the **information cascade**, and it won a decade's worth of economics prizes.

The setup is clean. Imagine a casino with two games, A and B, that are equally likely to win. You know the odds are fair. Before choosing, you get a private signal: a subtle hint that game A is slightly better. You trust your signal. You play A.

The next person got the same fair odds but their private signal suggested game B. They play B.

The third person sees: one vote for A, one vote for B. Their signal says A. They play A.

The fourth person sees: two votes for A, one for B. Their signal says B — but two people both ignored the same signal and chose A. They think: "They must know something I don't." They play A.

The cascade has begun. From this point forward, private signals stop mattering. The public count overwhelms everything.

## The Mathematics of Ignorance

The BHW model formalizes this with Bayesian updating. Each person computes:

**P(Good | previous choices, private signal)**

When the accumulated public count exceeds a threshold — usually just 2 or 3 votes — the posterior probability favoring the majority choice crosses 50%, and no private signal can overcome it. The individual becomes mathematically forced to follow the crowd, even when their own information screams otherwise.

Run the model 1,000 times with random signals, and a cascade forms roughly 60–70% of the time — even when both options are equally good. The crowd is not wisdom. It is arithmetic.

## Where This Happens in Real Life

**Financial markets** are the clearest example. In a rising market, early buyers profit. Later buyers see profits and jump in — not because their analysis says to, but because the pattern of others' success is the strongest signal available. Eventually the market overshoots any fundamental value. One piece of bad news breaks the cascade, and everyone rushes for the exit simultaneously. The crash looks sudden. The conditions were built in from the third buyer.

**The Dot-com bubble of 1999–2000** fits this perfectly. Pets.com, WebVan, and dozens of money-losing companies went public and surged in price — not because fundamentals supported it, but because the public count of rising stocks created an overwhelming signal. Following the crowd was individually rational right up until the moment it wasn't.

**Technology adoption** follows the same logic. Betamax was technically superior to VHS. But early VHS sales created a public count that overwhelmed private assessments of quality. Once the cascade tipped, even people who knew Betamax was better had strong rational reasons to choose VHS — because the compatible media ecosystem would follow the crowd.

**Social media virality** is pure cascade. A post with 10,000 shares looks more worth reading than an equally good post with 10. The 10,001st share is not based on the content — it is based on the count. This is why the first few engagements matter disproportionately, and why campaigns work hard to manufacture early momentum.

## The Fragility of Cascades

Here is what makes information cascades genuinely interesting: they are fragile by design.

A small external shock — a piece of public information, an authoritative statement, a visible crack in the crowd's logic — can collapse the entire structure. This is why financial bubbles burst suddenly rather than gradually deflating. The cascade held until it didn't, and the collapse happened faster than the buildup.

Bikhchandani and Welch called this **cascade fragility**. The same property that makes cascades powerful — their ability to concentrate behavior with minimal individual commitment — also makes them vulnerable to disruption. One credible whistleblower can collapse a corporate fraud cascade. One verified fact can collapse a viral misinformation cascade.

## The Information Cascade Simulator

The [Information Cascade Simulator](https://elysiatools.com/en/visualizations/information-cascade) puts the BHW model in your browser. Set the number of participants, the prior probability, the signal accuracy, and the cascade threshold. Watch the cascade form in real time — or watch it break.

Try the **Financial Bubble** preset to see how market herding plays out. Switch to **Strong Signals** and watch the cascade resist formation because private information stays reliable enough to override public counts. Push to **Weak Signals** and watch the cascade form almost immediately.

The simulator runs batch simulations — 1,000 runs at a click — so you see cascade rates, correct cascade rates (how often the crowd happened to be right), and incorrect cascade rates (how often the crowd was wrong and kept going anyway).

## The Real Problem Is Not the Crowd

The uncomfortable truth is that information cascades do not disappear with better information or smarter people. They are a structural feature of sequential decision-making — and the internet has made the structure worse, not better.

Every like, share, upvote, and view count is a public signal. Every recommendation algorithm amplifies cascade effects by surfacing what is already popular. The internet was supposed to give everyone a voice; what it actually created is an environment where the first few voices create signals that overwhelm everything that follows.

Understanding information cascades does not make you immune to them. You are still rational when you follow the crowd — the math compels it. But understanding the structure means you can recognize when you are in one. And recognizing it is the first step toward deciding whether your private signal has something worth saying.

Try running the [Information Cascade Simulator](https://elysiatools.com/en/visualizations/information-cascade) with different parameters. Watch how small changes in signal accuracy or threshold shift the entire outcome. Then ask yourself: when did I last check whether my choices were signal — or just someone else's arithmetic?

---

**Try it:** [Information Cascade Simulator](https://elysiatools.com/en/visualizations/information-cascade) — no signup, no download. Change any parameter and watch the cascade form or break in seconds.
