import sympy as sp
import numpy as np

n = sp.Symbol('n', integer=True, positive=True)

for m_val in range(2, 10):
    R_val = m_val * (m_val + 1)
    a_n = (n**2 + m_val) / ((m_val**2 + m_val)**n)
    a_n1 = ((n + 1)**2 + m_val) / ((m_val**2 + m_val)**(n + 1))
    rho = sp.limit(a_n1 / a_n, n, sp.oo)
    R_sym = sp.simplify(1 / rho)
    assert R_sym == R_val, f'Limit mismatch at m={m_val}: {R_sym} != {R_val}'
    # Verify convergence inside radius (x = 0.5 * R) via partial sums & symbolic summation
    x_in = sp.Rational(R_val, 2)
    s_exact = sp.summation(a_n * (x_in**n), (n, 1, sp.oo))
    k = np.arange(1, 60, dtype=np.float64)
    s_num = np.sum((k**2 + m_val) * (0.5**k))
    assert abs(float(s_exact) - s_num) < 1e-8

print('VERIFIED_OK: CALC-SER-02 radius of convergence R(m)=m(m+1) verified across m in [2..9]')
