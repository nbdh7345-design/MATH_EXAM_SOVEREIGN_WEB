import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
U = sp.Matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]])
V_m = sp.Matrix([[2, 2, 2*m + 3], [1, 2, m + 3], [0, 1, 2]])
C_m = sp.simplify(U.inv() * V_m)
expected_C = sp.Matrix([[1, 0, m], [1, 1, m + 1], [0, 1, 2]])
assert C_m == expected_C, f'Mismatch transition matrix: {C_m}'
assert sp.simplify(C_m.det()) == 1, 'det(C_m) must be 1'
w_Bp = sp.Matrix([1, 1, 1])
w_B = sp.simplify(C_m * w_Bp)
r_expr = sp.simplify(sum(w_B))
assert sp.simplify(r_expr - (2*m + 7)) == 0

for m_val in range(2, 10):
    U_np = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1]], dtype=float)
    V_np = np.array([[2, 2, 2*m_val + 3], [1, 2, m_val + 3], [0, 1, 2]], dtype=float)
    C_np = np.linalg.inv(U_np) @ V_np
    assert np.isclose(np.linalg.det(C_np), 1.0)
    w_B_np = C_np @ np.ones(3)
    assert np.allclose(w_B_np, [m_val + 1, m_val + 3, 3])
    assert np.isclose(np.sum(w_B_np), 2*m_val + 7)

print(f'VERIFIED_OK: ALG-VEC-03 det(C)=1, [w]_B={list(w_B)}, R(m)={r_expr}')
