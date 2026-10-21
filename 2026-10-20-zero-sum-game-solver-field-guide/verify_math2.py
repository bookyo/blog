import numpy as np


def analyse(A, label):
    A = np.array(A, dtype=float)
    n, m = A.shape
    row_min = A.min(axis=1)     # column player picks the worst column for the row
    col_max = A.max(axis=0)     # row player picks the best row for the column
    maximin = row_min.max()
    minimax = col_max.min()
    # CORRECT saddle definition:
    #   row player maximises -> cell must be MAX within its column
    #   column player minimises -> cell must be MIN within its row
    saddles = [(i, j) for i in range(n) for j in range(m)
               if abs(A[i][j] - A[:, j].max()) < 1e-12 and abs(A[i][j] - A[i].min()) < 1e-12]
    print(f'--- {label} ---')
    print(A)
    print('  row minima :', row_min, '-> maximin =', maximin)
    print('  col maxima :', col_max, '-> minimax =', minimax)
    print('  pure equilibrium:', maximin == minimax, ' saddle cells:', saddles)
    return maximin, minimax, saddles


def mixed_eq(A, steps=60):
    """Resolve the mixed equilibrium by simplex grid search for both players."""
    A = np.array(A, dtype=float)
    n = A.shape[0]

    def grid(n):
        if n == 2:
            return [(k / steps, 1 - k / steps) for k in range(steps + 1)]
        out = []
        # simple recursive coarse enumeration for n=3
        def rec(i, rem, cur):
            if i == n - 1:
                out.append(tuple(cur + [rem / steps]))
                return
            for k in range(rem + 1):
                rec(i + 1, rem - k, cur + [k / steps])
        rec(0, steps, [])
        return out

    cands = grid(n)
    v_row, x = max(((min(np.array(p) @ A), np.array(p)) for p in cands), key=lambda t: t[0])
    v_col, y = min(((max(A @ np.array(p)), np.array(p)) for p in cands), key=lambda t: t[0])
    print(f'  mixed: value = {round((v_row + v_col) / 2, 4)}')
    print(f'    row x = {x}  -> x^T A = {np.round(x @ A, 4)} (min {round((x @ A).min(), 4)})')
    print(f'    col y = {y}  -> A y  = {np.round(A @ y, 4)} (max {round((A @ y).max(), 4)})')
    print(f'    row guarantee x^T A >= v :', bool(np.all((x @ A) >= v_row - 1e-9)))
    print(f'    col guarantee A y  <= v :', bool(np.all((A @ y) <= v_col + 1e-9)))
    return x, y, (v_row + v_col) / 2


A1 = [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]
A2 = [[0, -1, 2], [-1, 0, 1], [-2, -1, 0]]
A3 = [[1, -1], [-1, 1]]

print('=' * 70)
mp1 = analyse(A1, 'A1  three-option contest (diagonal zero)')
print()
mp2 = analyse(A2, 'A2  A1 with Mid/Low flipped to -1')
print()
mp3 = analyse(A3, 'A3  matching pennies')
print()
print('=' * 70)
print('A1 claims to verify:')
print('  row minima [0,-1,-2], maximin 0  ->', np.array(A1).min(axis=1).tolist(),
      np.array(A1).min(axis=1).max())
print('  col maxima [0,1,2],  minimax 0  ->', np.array(A1).max(axis=0).tolist(),
      np.array(A1).max(axis=0).min())
print()
print('A2 claims to verify:')
print('  row minima [-1,-1,-2], maximin -1 ->', np.array(A2).min(axis=1).tolist(),
      np.array(A2).min(axis=1).max())
print('  col maxima [0,0,2],   minimax 0  ->', np.array(A2).max(axis=0).tolist(),
      np.array(A2).max(axis=0).min())
mixed_eq(A2)
print()
mixed_eq(A3)
print()
print('=' * 70)
print('SHIFT INVARIANCE (the claim that +K changes value by exactly K and no strategy)')
for K in [3, 7]:
    B = (np.array(A2, float) + K)
    _, _, vA = mixed_eq(A2) if K == 3 else (None, None, -0.5)
    xA, yA, vA = mixed_eq(np.array(A2, float))
    xB, yB, vB = mixed_eq(B)
    print(f'  K={K}: value {round(vA,4)} -> {round(vB,4)}  delta = {round(vB - vA, 10)} (expect exactly {K})')
    print(f'       row mix identical: {np.allclose(xA, xB)}   col mix identical: {np.allclose(yA, yB)}')
    print(f'       smallest entry after shift: {B.min()} (K=3 makes it 1: {B.min() == 1})')