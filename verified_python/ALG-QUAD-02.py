import sympy as sp
import numpy as np

m, k = sp.symbols('m k', real=True)
A = sp.Matrix([
    [1, 2, m],
    [2, 5, 2 * m],
    [m, 2 * m, k]
])
d1 = A[:1, :1].det()
d2 = sp.simplify(A[:2, :2].det())
d3 = sp.simplify(A.det())
assert d1 == 1 and d2 == 1 and d3 == k - m**2

for m_val in range(2, 11):
    k_val = m_val**2 + 1
    A_pos = np.array(A.subs({m: m_val, k: k_val}).tolist(), dtype=float)
    A_bnd = np.array(A.subs({m: m_val, k: m_val**2}).tolist(), dtype=float)
    assert np.all(np.linalg.eigvalsh(A_pos) > 0)
    assert np.min(np.linalg.eigvalsh(A_bnd)) <= 1e-12

print(f'VERIFIED_OK: ALG-QUAD-02 d1={d1}, d2={d2}, d3={d3}, k_min=m**2+1')
