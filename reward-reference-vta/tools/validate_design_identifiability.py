"""Algebraic identifiability guardrail for Reward Contrast.
This is a design-matrix smoke test, not a neural-data reanalysis.
"""
from itertools import product

def rank(matrix, tol=1e-10):
    a = [list(map(float, row)) for row in matrix]
    n, m = len(a), len(a[0])
    p = 0
    for c in range(m):
        if p == n:
            break
        i = max(range(p, n), key=lambda k: abs(a[k][c]))
        if abs(a[i][c]) <= tol:
            continue
        a[p], a[i] = a[i], a[p]
        scale = a[p][c]
        a[p] = [v / scale for v in a[p]]
        for k in range(n):
            if k == p: continue
            fac = a[k][c]
            a[k] = [a[k][j] - fac*a[p][j] for j in range(m)]
        p += 1
    return p

factorial = list(product((-1, 1), repeat=3)) # R, cue expectation E, actual U
base = [[1, U, R, E] for R, E, U in factorial]
with_derived = [[1, U, R, E, U-R, U-E] for R, E, U in factorial]
assert len(factorial) == 8
assert rank(base) == 4
assert rank(with_derived) == 4
assert all(abs((a[1]-a[2])-a[4]) < 1e-12 for a in with_derived)
assert all(abs((a[1]-a[3])-a[5]) < 1e-12 for a in with_derived)
print("DESIGN_MATRIX_QA=PASS")
print("factorial_cells=8; rank(1,U,R,E)=4; rank(1,U,R,E,C,cue_RPE)=4")
print("Compare U+R vs constrained C, cue-RPE vs augmented-state TD/RNN; never fit all derived columns freely.")
