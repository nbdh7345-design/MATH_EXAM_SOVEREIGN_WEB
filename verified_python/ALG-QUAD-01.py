import sympy as sp
import numpy as np

m = sp.Symbol('m', real=True)
A = sp.Matrix([
    [2, 2, 0],
    [2, m + 2, 1],
    [0, 1, m + 1]
])
d1 = A[:1, :1].det()
d2 = sp.expand(A[:2, :2].det())
d3 = sp.expand(A.det())
assert d1 == 2
assert d2 == 2 * m
assert d3 == 2 * m**2 + 2 * m - 2

for m_val in range(2, 11):
    A_num = np.array(A.subs(m, m_val).tolist(), dtype=float)
    eigs = np.linalg.eigvalsh(A_num)
    assert np.all(eigs > 0), f'Not positive definite at m={m_val}'

print(f'VERIFIED_OK: ALG-QUAD-01 d1={d1}, d2={d2}, d3={d3}')
