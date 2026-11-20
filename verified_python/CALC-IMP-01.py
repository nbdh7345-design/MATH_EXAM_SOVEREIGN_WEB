import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', real=True, positive=True)
for m_val in range(2, 10):
    integrand_sym = 2 * (m_val**2) / (x + 1)**(m_val + 1) + 2 * (m_val**2) * x * sp.exp(-m_val * x)
    val_sym = sp.integrate(integrand_sym, (x, 0, sp.oo))
    expected = 2 * m_val + 2
    assert int(val_sym) == expected, f'SymPy mismatch at m={m_val}: {val_sym} != {expected}'
    val_num, _ = quad(lambda t: 2*(m_val**2)/((t+1)**(m_val+1)) + 2*(m_val**2)*t*np.exp(-m_val*t), 0, np.inf)
    assert abs(val_num - expected) < 1e-7, f'SciPy mismatch at m={m_val}: {val_num} != {expected}'
print('VERIFIED_OK: CALC-IMP-01 passed symbolic (sp.oo) and numeric (quad) verification for m in [2..9]')
