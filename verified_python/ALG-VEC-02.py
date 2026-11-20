import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
P_m = sp.Matrix([[1, 1, 2], [0, 1, 1], [1, m, m + 2]])
assert sp.simplify(P_m.det()) == 1, 'Determinant must be identically 1'
x_vec = sp.Matrix([3*m + 4, m + 3, m**2 + 6*m + 2])
coords = sp.simplify(P_m.inv() * x_vec)
assert coords == sp.Matrix([m, 2, m + 1]), f'Unexpected coords: {coords}'
q_expr = sp.simplify(sum(coords))
assert sp.simplify(q_expr - (2*m + 3)) == 0

for m_val in range(2, 10):
    P_np = np.array([[1, 1, 2], [0, 1, 1], [1, m_val, m_val + 2]], dtype=float)
    x_np = np.array([3*m_val + 4, m_val + 3, m_val**2 + 6*m_val + 2], dtype=float)
    c_np = np.linalg.solve(P_np, x_np)
    assert np.allclose(c_np, [m_val, 2, m_val + 1])
    assert np.isclose(np.sum(c_np), 2*m_val + 3)

print(f'VERIFIED_OK: ALG-VEC-02 det=1, coords={list(coords)}, Q(m)={q_expr}')
