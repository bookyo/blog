# Why Smart People Make Irrational Choices — and Why Math Explains It Better Than Psychology

You and your partner in crime are in separate interrogation rooms. The prosecutor has enough evidence to put you both away for 3 years — but if one of you confesses and testifies against the other, that person walks free while the other gets 5 years. If both confess, both get 4 years. If neither confesses, both get 1 year thanks to lack of evidence.

What do you do?

This is the Prisoner's Dilemma, and almost everyone who hears it reaches the same conclusion: *stay silent, both walk out with 1 year.* It's the obvious collective choice.

Then John Nash — yes, the Nash from *A Beautiful Mind* — looked at this problem and found something deeply unsettling: even when everyone knows cooperation is best for the group, rational individual thinking drives everyone straight into a worse outcome. No player can improve their result by unilaterally changing strategy — so nobody does. Both get 4 years instead of 1.

This isn't a psychology problem. It's a mathematics problem. And it's been haunting economists, biologists, and political scientists ever since 1950.

## What Is Nash Equilibrium, Exactly

Nash equilibrium is a situation in a game where no player can improve their outcome by changing their own strategy alone. Every player is doing the best they can *given what everyone else is doing*.

The formal definition looks intimidating:

> uᵢ(sᵢ*, s₋ᵢ*) ≥ uᵢ(sᵢ, s₋ᵢ*) for all i and all sᵢ

But the intuition is simple: imagine you're playing rock-paper-scissors. If your opponent has settled on always playing rock, your best response is paper. But once you switch to paper, their best response is scissors. Once they switch to scissors, your best response is rock. The game never settles — because there's no equilibrium.

Now consider the Prisoner's Dilemma. If your partner stays silent, your best move is to betray them (0 years vs 1 year). If your partner betrays you, your best move is still to betray them (4 years vs 5 years). Betrayal is your dominant strategy — it beats the alternative in every scenario. And since your partner faces the same logic, betrayal is *their* dominant strategy too.

![Prisoner's Dilemma Payoff Matrix](https://blog.flowrust.com/wp-content/uploads/2026/04/prisoners-dilemma-payoff.png)

The result: mutual betrayal. Mutual 4-year sentences. A Nash equilibrium that everyone walking in the room knew was worse than cooperation.

## The Four Games That Explain Every Political Fight, Salary Negotiation, and Arms Race

Nash equilibrium isn't just one scenario. It's a framework for understanding four archetypal games that repeat across human experience.

**1. The Prisoner's Dilemma (Mutual Betrayal)**

This is the default. Two players, dominant strategies that lead to mutual destruction. The classic example: two companies racing to undercut each other on price until both are selling at a loss. Each knows they'd both be better off maintaining price — but each also knows that the other has an incentive to cheat. So both cheat. Both lose.

The insight: sometimes the rational path and the smart path are opposites.

**2. The Coordination Game (Align or Collide)**

Not every game is destructive. In a coordination game, players want to match each other — the payoff peaks when everyone chooses the same strategy. Think of driving: left-hand traffic and right-hand traffic are both functional *as long as everyone agrees*. The danger is that nobody can coordinate on the better option if they can't communicate.

The Nash equilibrium here isn't unique — there are multiple stable states. The challenge isn't finding a dominant strategy; it's coordinating on which equilibrium to lock into. This is why highway signs matter, why USB standards finally ended the chaos of dozens of incompatible connectors, and why the QWERTY keyboard layout has survived decades of seemingly superior alternatives.

**3. The Hawk-Dove Game (Escalation vs. Retreat)**

What happens when two players compete for a resource but fighting is costly? The Hawk-Dove game — also called Chicken — shows how both aggressive and passive strategies can coexist in equilibrium.

If both play Hawk (aggressive), they fight and both get hurt. If both play Dove (passive), they split the resource. But if one plays Hawk while the other plays Dove, the Hawk takes the whole resource and the Dove gets nothing. The result: a mixed-strategy equilibrium where players randomize, each playing Hawk a calculated percentage of the time.

This model shows up everywhere — in evolutionary biology (aggressive vs. conciliatory animals in a population), in military strategy (arms races), and in labor negotiations (strike vs. accept).

**4. The Stag Hunt (Trust and Risk)**

Imagine two hunters. One can catch a rabbit alone. But catching a stag requires both working together. If you trust your partner, you wait for the stag and both eat like royalty. If you betray your partner for the rabbit, you eat but they go hungry.

The Stag Hunt, described by Rousseau, models situations where cooperation is more rewarding — but also more risky. Unlike the Prisoner's Dilemma, mutual cooperation here is a Nash equilibrium too. The problem is that stag hunt also has a second equilibrium: both hunt rabbits. And rabbit-hunting is safer, even if it's worse for everyone.

This is the game behind most failed team projects. You know the big collaborative win is possible. But you also know that if your teammate abandons ship, you should have built your solo fallback. So you build it. They build theirs. The stag starves.

![The Stag Hunt: Trust vs Safety](https://blog.flowrust.com/wp-content/uploads/2026/04/stag-hunt-conclusion.png)

It also explains why companies get locked into legacy software they hate: switching costs are real, but so is staying. Both the defector and the loyalist have a point. And so nobody moves.

## Tit for Tat: The Strategy That Won Evolution

If Nash equilibrium explains why rational people get stuck in bad outcomes, is there any way out?

Robert Axelrod, a political scientist, ran the most famous tournament in game theory history. He invited academics to submit computer programs that would play iterated Prisoner's Dilemma against each other — multiple rounds, where past decisions were remembered. The programs would compete, and the highest-scoring one would win.

The winner: a strategy called **Tit for Tat**. Its rules were three:

1. Start by cooperating
2. Copy your opponent's last move
3. Never be the first to betray

That's it. Simple, readable, retaliatory when needed, forgiving when not.

The interesting part: Tit for Tat didn't *win* by scoring the highest against its opponents. It won because it invited the least retaliation. Programs that played against Tit for Tat *also* scored well, because it prompted them to cooperate. Programs that defected aggressively did well against soft targets but tanked their scores when matched against each other.

Axelrod's conclusion: in evolutionary terms, nice strategies — ones that don't betray first — tend to dominate over the long run. Not because evolution is moral, but because cooperation, once established, is self-reinforcing. The returns on defection look better on paper and worse in practice.

## The Problem That Nash Himself Couldn't Solve

Here's what nobody tells you about Nash equilibrium: it tells you *where* the stable points are, but not *how to get there*.

Consider the global economy. Almost every country knows that coordinated action on climate policy is better for everyone. But each country also knows that if others cheat on their commitments while they honor theirs, they're worse off. So each country underinvests in climate commitments. The result is a Nash equilibrium of insufficient action — stable in the mathematical sense, catastrophic in the real one.

This is what Eliezer Yudkowsky called "inadequate equilibria" in his book of the same name: situations where the game-theoretic stable outcome is far worse than what decentralized coordinated action could achieve. Institutions exist partly to try to escape these traps — through binding agreements, third-party enforcement, and social norms that make defection socially costly.

But institutions themselves can become inadequate equilibria. A company that refuses to change its culture might be in equilibrium — no individual employee can improve their situation by unilaterally changing behavior, so nobody does — even when the collective cost is enormous.

The uncomfortable truth: knowing you're in a bad equilibrium doesn't tell you how to escape it. That's not a math problem anymore. It's a leadership problem.

## What Nash Equilibrium Can't Tell You

Here's the part that should keep you up at night: Nash equilibrium explains *where* you get stuck. It says nothing about *how to leave*.

Consider climate change. Almost every country knows coordinated action is better for everyone. But each country also knows that if others cheat on their commitments while they comply, they're punished. So each country complies partially, and all of us are stuck in a 2°C warming trajectory that nobody chose.

Consider your company's planning meetings. Everyone knows the cross-functional initiative would create enormous value. But no single team can be sure others will follow through. So each team builds its own silo. The bad equilibrium persists because it's individually rational.

This is what Yudkowsky called *inadequate equilibria* — stable states that are far worse than what coordinated human effort could achieve. Knowing you're trapped doesn't free you. But it does show you where the bars are.

![Nash Equilibrium: Inadequate Equilibria](https://blog.flowrust.com/wp-content/uploads/2026/04/inadequate-equilibria.png)

## See It for Yourself

The [Nash Equilibrium Visualizer](https://elysiatools.com/en/visualizations/nash-equilibrium) puts you inside these games. Switch between Prisoner's Dilemma, Coordination, Hawk-Dove, and a custom payoff matrix. Gold cells show you exactly where the equilibrium locks in. Slide the mixed-strategy probabilities and watch expected payoffs shift in real time.

The [Game Theory Simulator](https://elysiatools.com/en/visualizations/game-theory-simulator) runs iterated tournaments — including a replica of Axelrod's famous Tit for Tat competition. Watch cooperation emerge or collapse depending on the starting population.

Both are free, browser-based, and take about 90 seconds to start breaking your assumptions.

---

*Nash equilibrium is the most honest model economists ever built: it proves that rational people routinely reach irrational outcomes, and that the trap isn't a character flaw — it's a structural one. The exit exists. It's just harder to see from inside the game.*
