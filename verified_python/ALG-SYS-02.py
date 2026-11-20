import sympy as sp
import numpy as np

m, k = sp.symbols('m k')
x, y, z = sp.symbols('x y z')
A = sp.Matrix([[1, 1, 1], [1, 2, 3], [2, 3, 4]])
assert A.det() == 0 and A.rank() == 2
A_aug = sp.Matrix([[1, 1, 1, m], [1, 2, 3, 2 * m + 1], [2, 3, 4, k]])
rref_mat, _ = A_aug.subs(k, 3 * m + 1).rref()
assert rref_mat[2, 3] == 0

for m_val in range(2, 10):
    k_val = 3 * m_val + 1
    sol_set = sp.linsolve((A, sp.Matrix([m_val, 2 * m_val + 1, k_val])), (x, y, z))
    assert len(sol_set) == 1
    A_sub = np.array([[1.0, 1.0], [1.0, 2.0]])
    b_sub = np.array([float(m_val), float(2 * m_val + 1)])
    xy0 = np.linalg.solve(A_sub, b_sub)
    assert np.isclose(2.0 * xy0[0] + 3.0 * xy0[1], k_val)

print('VERIFIED_OK: ALG-SYS-02 Kronecker-Capelli condition k = 3m + 1 verified.')
