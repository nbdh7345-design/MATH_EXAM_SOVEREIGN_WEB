import sympy as sp
import numpy as np

lam, m = sp.symbols('lam m')
A = sp.Matrix([[lam, 1, 1], [1, lam, 1], [1, 1, lam]])
b = sp.Matrix([m, m, m])
assert sp.factor(A.det()) == (lam + 2) * (lam - 1)**2
sol = A.LUsolve(b)
for comp in sol:
    assert sp.simplify(comp - m / (lam + 2)) == 0
S_sym = sp.simplify(4 * sum(sol.subs(lam, 2)))
assert S_sym == 3 * m

for m_val in range(2, 10):
    A_np = np.array([[2.0, 1.0, 1.0], [1.0, 2.0, 1.0], [1.0, 1.0, 2.0]])
    b_np = np.array([float(m_val)] * 3)
    xyz = np.linalg.solve(A_np, b_np)
    assert np.isclose(4.0 * np.sum(xyz), 3.0 * m_val)

print('VERIFIED_OK: ALG-SYS-03 Full parametric discussion & S = 3m verified.')
