import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
u1 = sp.Matrix([1, 1, 0])
u2 = sp.Matrix([2*m, 0, m])

e1 = u1
e2 = u2 - (u2.dot(e1) / e1.dot(e1)) * e1
assert sp.simplify(e2.dot(e1)) == 0, "e1 and e2 must be orthogonal"
norm_e2_sq = sp.simplify(e2.dot(e2))
assert sp.simplify(norm_e2_sq - 3*m**2) == 0, f"Mismatch: {norm_e2_sq}"

for m_val in range(2, 10):
    u1_n = np.array([1.0, 1.0, 0.0])
    u2_n = np.array([2.0 * m_val, 0.0, 1.0 * m_val])
    e1_n = u1_n
    e2_n = u2_n - (np.dot(u2_n, e1_n) / np.dot(e1_n, e1_n)) * e1_n
    assert abs(np.dot(e1_n, e2_n)) < 1e-9
    assert abs(np.dot(e2_n, e2_n) - 3.0 * (m_val ** 2)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-02 norm_e2_sq={norm_e2_sq}")
