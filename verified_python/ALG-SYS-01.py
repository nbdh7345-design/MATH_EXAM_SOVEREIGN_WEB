import sympy as sp
import numpy as np

m = sp.Symbol('m', integer=True, positive=True)
x, y, z = sp.symbols('x y z')
A = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 3, 6]])
b = sp.Matrix([6 * m, 14 * m, 25 * m])
assert A.det() == 1
sol = A.LUsolve(b)
T_expr = sp.simplify(2 * sol[0] + sol[1] + sol[2])
assert T_expr == 7 * m, f'Symbolic mismatch: {T_expr}'

for m_val in range(2, 10):
    A_np = np.array([[1.0, 1.0, 1.0], [1.0, 2.0, 3.0], [1.0, 3.0, 6.0]])
    b_np = np.array([6.0 * m_val, 14.0 * m_val, 25.0 * m_val])
    xyz = np.linalg.solve(A_np, b_np)
    T_num = 2.0 * xyz[0] + xyz[1] + xyz[2]
    assert np.isclose(T_num, 7.0 * m_val)

print('VERIFIED_OK: ALG-SYS-01 Cramer 3x3 system verified symbolically and numerically.')
