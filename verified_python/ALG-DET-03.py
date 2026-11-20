import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A_sym = sp.Matrix([
    [1, 1, 1],
    [1, m, 1],
    [1, 1, m**2],
])
det_sym = sp.factor(A_sym.det())
expected_det = (m - 1)**2 * (m + 1)
assert sp.simplify(det_sym - expected_det) == 0, f"Det mismatch: {det_sym}"

adj_sym = A_sym.adjugate()
assert sp.simplify(A_sym * adj_sym - A_sym.det() * sp.eye(3)) == sp.zeros(3, 3)
sum_adj_sym = sp.factor(sum(adj_sym))
assert sp.simplify(sum_adj_sym - expected_det) == 0, f"Adjugate sum mismatch: {sum_adj_sym}"

for m_val in range(2, 10):
    A_np = np.array([
        [1.0, 1.0, 1.0],
        [1.0, float(m_val), 1.0],
        [1.0, 1.0, float(m_val**2)],
    ], dtype=float)
    det_num = round(float(np.linalg.det(A_np)))
    det_exact = (m_val - 1)**2 * (m_val + 1)
    assert det_num == det_exact, f"Numeric det mismatch at m={m_val}: {det_num} != {det_exact}"
    inv_np = np.linalg.inv(A_np)
    assert abs(float(np.sum(inv_np)) - 1.0) < 1e-9, f"Inverse sum mismatch at m={m_val}"

print(f"VERIFIED_OK: ALG-DET-03 det(A(m)) = {det_sym}, sum(adj(A(m))) = {sum_adj_sym}, sum(A^-1(m)) = 1 for m in [2..9]")
