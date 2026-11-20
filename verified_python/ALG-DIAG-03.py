import sympy as sp
import numpy as np

for m_val in range(2, 10):
    A_sym = sp.Matrix([[m_val + 1, 1 - m_val], [0, 2]])
    P, D = A_sym.diagonalize()
    assert P * D * P.inv() == A_sym
    for n_pow in range(1, 6):
        An_diag = P * (D**n_pow) * P.inv()
        An_formula = sp.Matrix([[(m_val + 1)**n_pow, 2**n_pow - (m_val + 1)**n_pow], [0, 2**n_pow]])
        assert An_diag == An_formula
        A_np = np.array([[m_val + 1, 1 - m_val], [0, 2]], dtype=np.int64)
        An_np = np.linalg.matrix_power(A_np, n_pow)
        assert np.array_equal(An_np, np.array(An_formula.tolist(), dtype=np.int64))
    k_val = int(sp.trace(A_sym**2))
    assert k_val == m_val**2 + 2*m_val + 5
print('VERIFIED_OK: ALG-DIAG-03 passed across grid m in [2..9]')
