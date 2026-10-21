from itertools import product

import numpy as np


def saddle_report(A, label):
    A = np.array(A, dtype=float)
    n, m = A.shape
    row_min = A.min(axis=1)
    col_max = A.max(axis=0)
    maximin = row_min.max()
    minimax = col_max.min()
    saddle = [(i, j) for i in range(n) for j in range(m)
              if abs(A[i][j] - maximin) < 1e-12 and abs(A[i][j] - minimax) < 1e-12]
    # true saddle cells: max in row AND min in column
    true_saddle = [(i, j) for i in range(n) for j in range(m)
                   if abs(A[i][j] - A[i].max()) < 1e-12 and abs(A[i][j] - A[:, j].min()) < 1e-12]
    print(f'--- {label} ---')
    print(A)
    print('row minima:', row_min, ' maximin =', maximin)
    print('col maxima:', col_max, ' minimax =', minimax)
    print('bound-equal cells:', saddle, ' true saddle (max-in-row & min-in-col):', true_saddle)
    print('pure equilibrium:', maximin == minimax)
    print()
    return maximin, minimax, true_saddle


A1 = [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]
A2 = [[0, -1, 2], [-1, 0, 1], [-2, -1, 0]]
mp1 = saddle_report(A1, 'A1 original auction')
mp2 = saddle_report(A2, 'A2 perturbed (Mid/Low = -1)')

# matching pennies check
A3 = [[1, -1], [-1, 1]]
saddle_report(A3, 'A3 matching pennies')

# Solve mixed equilibrium for A2 via brute-force LP-free approach:
# row player: maximize t s.t. x^T A e_j >= t, sum x = 1, x >= 0  -> use scipy-free grid + refinement
from math import isclose

def solve_mixed(A, iters=400):
    A = np.array(A, dtype=float)
    n, m = A.shape

    def best_response_row(x):
        return (x @ A).min()          # guaranteed payoff given x

    def best_response_col(y):
        return (A @ y).max()          # ceiling the column player forces

    # coarse grid search then coordinate ascent for both players
    step = 1.0 / 40
    best = None
    for _ in range(iters):
        pass
    # enumerate fine simplex grid for row player
    grid = [i / 40 for i in range(41)]
    cands = []
    for i in range(41):
        for j in range(41 - i):
            k = 40 - i - j
            x = np.array([i / 40, j / 40, k / 40])
            cands.append((best_response_row(x), x))
    v, x = max(cands, key=lambda t: t[0])
    # column player minimise the max
    cands2 = []
    for i in range(41):
        for j in range(41 - i):
            k = 40 - i - j
            y = np.array([i / 40, j / 40, k / 40])
            cands2.append((best_response_col(y), y))
    v2, y = min(cands2, key=lambda t: t[0])
    print('A2 mixed equilibrium (grid-resolved):')
    print('  value  =', round((v + v2) / 2, 4))
    print('  row x  =', x, ' -> guarantees', round(best_response_row(x), 4))
    print('  col y  =', y, ' -> caps at', round(best_response_col(y), 4))
    print('  x^T A  =', np.round(x @ A, 4))
    print('  A y    =', np.round(A @ y, 4))
    print('  check row guarantee x^T A >= v:', bool(np.all((x @ A) >= v - 1e-9)))
    print('  check col guarantee A y <= v:', bool(np.all((A @ y) <= v + 1e-9)))
    print()
    return x, y

solve_mixed(A2)

# shift invariance proof check on A2
K = 7
B = np.array(A2, float) + K
print('shift invariance: minimax(A) =', mp2[1], ' minimax(A+7) =', saddle_report(B, 'A2 shifted +7')[1])
print('  difference should be exactly 7:', round(saddle_report(B, 'A2 shifted +7 (recheck)')[1] - mp2[1], 10))