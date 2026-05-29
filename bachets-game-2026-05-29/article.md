---
title: Why 21 Stones Guarantees a Win — The Mathematics of Bachet's Game
---

# Why 21 Stones Guarantees a Win — The Mathematics of Bachet's Game

There is a game so clean, so stripped of luck and hidden information, that its entire structure can be summarized in a single number. You start with a pile of stones. Two players take turns removing between one and four stones. The player who takes the last stone wins. On the surface, it feels like a coin toss. It is not. One of the two players can force a win every time — if they know the trick.

That trick is the cold position.

## The Cold Position: Where Winning Begins

A cold position is any pile size where the player about to move cannot force a win, assuming optimal play from the opponent. In Bachet's Game, the cold positions follow a single, elegant rule: they are exactly the multiples of (M+1), where M is the maximum number of stones you can take.

With M = 4, the cold positions are 0, 5, 10, 15, 20, 25... The pattern repeats every 5 stones.

The reason is not magic — it is modular arithmetic. When you are at a cold position, any legal move (removing 1 to 4 stones) lands the opponent in a winning position, called a hot position. From a hot position, you can always remove exactly the right number of stones to return the game to the nearest cold position. The two players who understand this dance — leaving your opponent at a cold position after every one of your moves — are the only two who have ever truly played the game.

## Why 21 Is a Guaranteed Win

Start with 21 stones. The key number is the cold position just below 21 — which is 20. Because 20 is a multiple of 5, it is cold. 

Your winning first move: remove 1 stone, leaving 20.

Whatever your opponent removes next (1–4 stones), you mirror their move: if they take 2, you take 2, leaving 16. If they take 4, you take 4, leaving 12. This strategy — always moving to a cold position after your turn — is called mirroring, and it is the complete winning strategy when you are the player who moves second from a multiple of (M+1).

The pattern holds for any N and M. The cold positions are always N = k·(M+1). The player who moves first wins if and only if N is not already a cold position — and their first move is to remove N mod (M+1) stones, landing the game at the nearest cold position below.

## The Interactive Visualization: See the Pattern Collapse

The Bachet's Game visualization lets you play against an AI opponent at three difficulty levels. In hard mode, the AI always plays optimally — it will exploit every deviation from the cold-position strategy, and it will never give you a winning path once it has a winning position.

What makes the visualization worth running is the hint system. When you enable hints, the cold positions glow green — watch how every optimal move from the AI lands precisely on those green squares. Then play a sub-optimal move intentionally and watch the AI punish you immediately. The transition from confused to certain happens in about three games.

## The Deeper Connection: Nim and Combinatorial Game Theory

Bachet's Game is not a mathematical curiosity — it is a direct ancestor of Nim, one of the most studied objects in combinatorial game theory. Nim's solution, published by Charles Bouton in 1902, applies the same cold-position logic to multi-pile games. Every impartial game — a game where the legal moves are identical for both players — has a Grundy number that reduces it to a Nim heap of equivalent size.

The full generalization: for a subtraction game where you can remove any number from a set S = {s₁, s₂, ..., sₖ}, the cold positions are those n for which no move leads to another cold position. This is computed by a simple bottom-up dynamic programming pass. The pattern for S = {1, 2, ..., M} yields exactly the M+1 cycle: 0, M+1, 2(M+1), 3(M+1)...

## The Interactive Element: Playing Before Understanding

There is a reason the visualization comes before the explanation in this article — and why the game lets you experiment freely. Mathematical intuition is built from concrete examples, not from definitions. You could read the cold-position rule a hundred times and not feel it the way you feel it when the AI wins for the seventh consecutive time and you still do not see why.

Open the interactive version. Set N to 25 and M to 4. Play first. Lose. Then read the section above again, and play again. The game does not change. Your understanding does.

---

*This article is based on the Bachet's Game interactive visualization at Elysia Tools.*
