import sympy as sp
import numpy as np

for m_val in range(2, 10):
    A_sym = sp.Matrix([[m_val, 1], [2*m_val, m_val + 1]])
    I2 = sp.eye(2)
    # Verify Cayley-Hamilton directly
    P_A = A_sym**2 - (2*m_val + 1)*A_sym + (m_val**2 - m_val)*I2
    assert P_A == sp.zeros(2, 2), 'Cayley-Hamilton failed'
    M_sym = A_sym**3 - 2*m_val*(A_sym**2) + (m_val**2 - 3*m_val - 1)*A_sym + (m_val**2 + m_val + 2)*I2
    assert M_sym == (2*m_val + 2)*I2
    # NumPy matrix_power verification
    A_np = np.array([[m_val, 1], [2*m_val, m_val + 1]], dtype=np.int64)
    M_np = (np.linalg.matrix_power(A_np, 3)
            - 2*m_val*np.linalg.matrix_power(A_np, 2)
            + (m_val**2 - 3*m_val - 1)*A_np
            + (m_val**2 + m_val + 2)*np.eye(2, dtype=np.int64))
    tr_val = int(np.trace(M_np))
    assert tr_val == 4*m_val + 4
print('VERIFIED_OK: ALG-DIAG-02 passed across grid m in [2..9]')
