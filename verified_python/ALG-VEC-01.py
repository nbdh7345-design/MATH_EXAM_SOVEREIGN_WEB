import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True)
A = sp.Matrix([[1, 2], [2, 3], [-1, 1]])
v_m = sp.Matrix([4*m + 3, 7*m + 4, 3 - m])
alpha1, alpha2 = sp.symbols('alpha1 alpha2')
sol = sp.solve(A * sp.Matrix([alpha1, alpha2]) - v_m, (alpha1, alpha2))
sum_expr = sp.simplify(sol[alpha1] + sol[alpha2])
assert sp.simplify(sum_expr - (3*m + 1)) == 0, f'Symbolic mismatch: {sum_expr}'

for m_val in range(2, 10):
    A_np = np.array([[1.0, 2.0], [2.0, 3.0], [-1.0, 1.0]])
    v_np = np.array([4*m_val + 3, 7*m_val + 4, 3 - m_val], dtype=float)
    coeffs, residuals, rank, _ = np.linalg.lstsq(A_np, v_np, rcond=None)
    assert rank == 2 and np.allclose(A_np @ coeffs, v_np)
    assert np.isclose(np.sum(coeffs), 3*m_val + 1)

print(f'VERIFIED_OK: ALG-VEC-01 S(m) = {sum_expr}, m=3 -> {sum_expr.subs(m, 3)}')
