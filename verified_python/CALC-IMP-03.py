import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', real=True, positive=True)
for m_val in range(2, 10):
    # Verify Euler-Laplace improper integral symbolically with sp.oo
    i_euler_sym = sp.integrate(x**3 * sp.exp(-x / m_val), (x, 0, sp.oo))
    i_power_sym = sp.integrate(2 * (m_val**3) / x**3, (x, 1, sp.oo))
    l_sym = int(i_euler_sym + i_power_sym)
    n_conv = 2 * m_val - 1
    t_expected = 6 * (m_val**4) + (m_val**3) + 2 * m_val - 1
    assert l_sym + n_conv == t_expected, f'SymPy mismatch at m={m_val}'
    # Verify numerically with scipy.integrate.quad
    i_euler_num, _ = quad(lambda t: (t**3) * np.exp(-t / m_val), 0, np.inf)
    i_power_num, _ = quad(lambda t: 2 * (m_val**3) / (t**3), 1, np.inf)
    assert abs((i_euler_num + i_power_num + n_conv) - t_expected) < 1e-5
    # Also check K_alpha(m) convergence at interior alpha = m
    k_mid_num, _ = quad(lambda t: (t**(m_val - 1)) / (1 + t**(2 * m_val)), 0, np.inf)
    assert abs(k_mid_num - np.pi / (2 * m_val)) < 1e-7
print('VERIFIED_OK: CALC-IMP-03 passed symbolic (sp.oo) and numeric (quad) verification for m in [2..9]')
