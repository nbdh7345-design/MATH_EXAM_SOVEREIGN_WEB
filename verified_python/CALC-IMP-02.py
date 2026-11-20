import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', real=True, positive=True)
for m_val in range(2, 10):
    # Verify convergence threshold on (0, 1) and via x = 1/t on (1, oo)
    p_max_val = m_val - 1
    conv_int = sp.integrate(1 / x**(sp.Rational(p_max_val, m_val)), (x, 0, 1))
    conv_improper1 = sp.integrate(1 / x**(2 - sp.Rational(p_max_val, m_val)), (x, 1, sp.oo))
    assert conv_int == m_val and conv_improper1 == m_val
    # Verify J(m) symbolically and numerically
    j_sym = sp.integrate(sp.sqrt(m_val) * (m_val + 1) / (2 * sp.sqrt(x)), (x, 0, m_val))
    j_num, _ = quad(lambda t: np.sqrt(m_val) * (m_val + 1) / (2 * np.sqrt(t)), 0, m_val)
    s_expected = m_val**2 + 2 * m_val - 1
    assert int(j_sym) + p_max_val == s_expected
    assert abs((j_num + p_max_val) - s_expected) < 1e-7
print('VERIFIED_OK: CALC-IMP-02 passed symbolic and numeric improper integral checks for m in [2..9]')
