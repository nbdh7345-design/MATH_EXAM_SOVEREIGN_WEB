import sympy as sp
import numpy as np

a = sp.Symbol('a', real=True)
for m_val in range(2, 10):
    A_sym = sp.Matrix([[1, 0, a - 2*m_val], [0, m_val, m_val - 1], [0, 0, 1]])
    # Check rank(A - I) == 1 iff a = 2*m_val
    a0_val = 2 * m_val
    A_diag_sym = A_sym.subs(a, a0_val)
    assert A_diag_sym.is_diagonalizable(), f'Should be diagonalizable at a={a0_val}'
    A_nondiag_sym = A_sym.subs(a, a0_val + 1)
    assert not A_nondiag_sym.is_diagonalizable(), 'Should not be diagonalizable when a != 2m'
    P, D = A_diag_sym.diagonalize()
    assert P * D * P.inv() == A_diag_sym
    # NumPy power check
    A_np = np.array(A_diag_sym.tolist(), dtype=np.int64)
    P_np = np.array(P.tolist(), dtype=np.float64)
    D_np = np.array(D.tolist(), dtype=np.float64)
    assert np.allclose(np.linalg.matrix_power(A_np, 4), P_np @ np.linalg.matrix_power(D_np, 4) @ np.linalg.inv(P_np))
    s_val = int(a0_val + sp.trace(D))
    assert s_val == 3 * m_val + 2
print('VERIFIED_OK: ALG-DIAG-01 passed across grid m in [2..9]')
