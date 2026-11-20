import sympy as sp
import numpy as np

m, x1, x2, x3 = sp.symbols('m x1 x2 x3', real=True)
A = sp.Matrix([
    [1, -1, m],
    [-1, m + 1, 0],
    [m, 0, m**2 + 3*m - 1]
])
d1 = A[:1, :1].det()
d2 = sp.expand(A[:2, :2].det())
d3 = sp.expand(A.det())
assert d1 == 1
assert d2 == m
assert d3 == 2*m**2 - m

X = sp.Matrix([x1, x2, x3])
Q_mat = sp.expand((X.T * A * X)[0])
Q_lag = sp.expand((x1 - x2 + m*x3)**2 + m*(x2 + x3)**2 + (2*m - 1)*x3**2)
assert sp.simplify(Q_mat - Q_lag) == 0

for m_val in range(2, 11):
    A_num = np.array(A.subs(m, m_val).tolist(), dtype=float)
    eigs = np.linalg.eigvalsh(A_num)
    assert np.all(eigs > 0), f'Not positive definite at m={m_val}'

print(f'VERIFIED_OK: ALG-QUAD-03 d1={d1}, d2={d2}, d3={d3}, Lagrange=OK')
