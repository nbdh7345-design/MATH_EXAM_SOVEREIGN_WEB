import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [m, 1, 0],
    [1, m, 1],
    [0, 1, m],
])
det_sym = sp.expand(A_sym.det())
adj_sym = A_sym.adjugate()
trace_adj_sym = sp.expand(adj_sym.trace())
S_sym = sp.expand(det_sym + trace_adj_sym)
expected_S = m**3 + 3*m**2 - 2*m - 2
assert sp.simplify(S_sym - expected_S) == 0, f"Symbolic mismatch: {S_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [m_val, 1.0, 0.0],
        [1.0, m_val, 1.0],
        [0.0, 1.0, m_val],
    ], dtype=float)
    det_val = float(np.linalg.det(A_np))
    inv_np = np.linalg.inv(A_np)
    adj_np = det_val * inv_np
    s_num = round(det_val + float(np.trace(adj_np)))
    s_exact = m_val**3 + 3 * m_val**2 - 2 * m_val - 2
    assert s_num == s_exact, f"Numeric mismatch at m={m_val}: {s_num} != {s_exact}"

print(f"VERIFIED_OK: ALG-DET-02 S(m) = {S_sym}, grid m in [2..9] passed, S(3) = {int(expected_S.subs(m, 3))}")
