import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', real=True)
for m_val in range(2, 10):
    integrand = (m_val**3) * x * (1 - x)**(m_val - 1)
    sym_val = sp.integrate(integrand, (x, 0, 1))
    expected = sp.Rational(m_val**2, m_val + 1)
    assert sp.simplify(sym_val - expected) == 0, f'SymPy mismatch at m={m_val}'
    num_val, _ = quad(lambda t: (m_val**3) * t * ((1.0 - t)**(m_val - 1)), 0.0, 1.0)
    assert np.isclose(num_val, float(expected), rtol=1e-10, atol=1e-12), f'Quad mismatch at m={m_val}'
    opts = [sp.Rational(m_val**2, m_val + 1), sp.Rational(m_val, m_val + 1),
            sp.Rational(m_val**2, m_val - 1), sp.Rational(m_val**3, (m_val + 1) * (m_val + 3))]
    assert len(set(opts)) == 4, f'Duplicate options at m={m_val}'
print('VERIFIED_OK: CALC-INT-01 passed SymPy & SciPy quad across m in [2..9]')
