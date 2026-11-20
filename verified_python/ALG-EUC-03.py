import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
u1 = sp.Matrix([1, 1, 1, 1])
u2 = sp.Matrix([1, 3, -1, 1])
v = sp.Matrix([3*m, 4*m, 0, m])

e1 = u1
e2 = u2 - (u2.dot(e1) / e1.dot(e1)) * e1
assert sp.simplify(e1.dot(e2)) == 0

p = (v.dot(e1) / e1.dot(e1)) * e1 + (v.dot(e2) / e2.dot(e2)) * e2
z = sp.simplify(v - p)
assert sp.simplify(z.dot(e1)) == 0 and sp.simplify(z.dot(e2)) == 0

dist_sq = sp.simplify(z.dot(z))
assert sp.simplify(dist_sq - 2*m**2) == 0, f"Mismatch dist_sq: {dist_sq}"
assert sp.simplify(p.dot(p) + z.dot(z) - v.dot(v)) == 0, "Pythagoras failed"

for m_val in range(2, 10):
    A = np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 3.0, -1.0, 1.0]]).T
    v_n = np.array([3.0 * m_val, 4.0 * m_val, 0.0, 1.0 * m_val])
    p_n = A @ np.linalg.lstsq(A, v_n, rcond=None)[0]
    z_n = v_n - p_n
    assert abs(np.dot(z_n, z_n) - 2.0 * (m_val ** 2)) < 1e-9

print(f"VERIFIED_OK: ALG-EUC-03 dist_sq={dist_sq}")
