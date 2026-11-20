import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
C = sp.Matrix([
    [m + 2, -1, 0],
    [-1, m + 2, 0],
    [0, 0, 3*m + 1]
])
eigs_C = C.eigenvals()
sum_sq_C = sp.expand(sum(val**2 * mult for val, mult in eigs_C.items()))
trace_C2 = sp.expand((C * C).trace())
target_C = 11*m**2 + 14*m + 11

assert sp.simplify(sum_sq_C - target_C) == 0, f"Symbolic mismatch: {sum_sq_C}"
assert sp.simplify(trace_C2 - target_C) == 0, f"Trace C^2 mismatch: {trace_C2}"

P = sp.Matrix([
    [1, 1, 0],
    [1, -1, 0],
    [0, 0, 1]
])
D = sp.simplify(P.inv() * C * P)
assert D == sp.diag(m + 1, m + 3, 3*m + 1), f"Diagonalization mismatch: {D}"

for m_val in range(2, 10):
    C_num = np.array([
        [m_val + 2, -1, 0],
        [-1, m_val + 2, 0],
        [0, 0, 3*m_val + 1]
    ], dtype=float)
    eig_num = np.linalg.eigvals(C_num)
    val_num = float(np.sum(eig_num**2))
    expected = float(11*m_val**2 + 14*m_val + 11)
    assert np.isclose(val_num, expected, rtol=1e-9), f"Numeric mismatch at m={m_val}: {val_num} != {expected}"

print(f"VERIFIED_OK: ALG-EIG-03 | eigs={list(eigs_C.keys())} | Tr(C^2)={sum_sq_C} | Tr(C(3)^2)={sum_sq_C.subs(m, 3)}")
