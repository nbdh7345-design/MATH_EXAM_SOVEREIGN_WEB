import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [m, 1, 1],
    [1, m, 1],
    [1, 1, m],
])
det_sym = sp.factor(A_sym.det())
expected_sym = (m - 1)**2 * (m + 2)
assert sp.simplify(det_sym - expected_sym) == 0, f"Symbolic mismatch: {det_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [m_val, 1.0, 1.0],
        [1.0, m_val, 1.0],
        [1.0, 1.0, m_val],
    ], dtype=float)
    det_num = round(float(np.linalg.det(A_np)))
    det_exact = (m_val - 1)**2 * (m_val + 2)
    assert det_num == det_exact, f"Numeric mismatch at m={m_val}: {det_num} != {det_exact}"

print(f"VERIFIED_OK: ALG-DET-01 det(A(m)) = {det_sym}, grid m in [2..9] passed, det(A(3)) = {(3-1)**2*(3+2)}")
