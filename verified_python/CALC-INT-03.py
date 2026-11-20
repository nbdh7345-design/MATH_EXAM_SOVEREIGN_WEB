import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', real=True, nonnegative=True)
for m_val in range(2, 10):
    i1_sym = sp.integrate(x * (1 - x**2)**(m_val - 1), (x, 0, 1))
    i2_sym = sp.integrate((x**2) * sp.exp(-m_val * x), (x, 0, sp.oo))
    assert sp.simplify(i1_sym - sp.Rational(1, 2 * m_val)) == 0
    assert sp.simplify(i2_sym - sp.Rational(2, m_val**3)) == 0
    s_sym = sp.simplify(i2_sym / i1_sym)
    expected_s = sp.Rational(4, m_val**2)
    assert sp.simplify(s_sym - expected_s) == 0
    i1_num, _ = quad(lambda t: t * ((1.0 - t**2)**(m_val - 1)), 0.0, 1.0)
    i2_num, _ = quad(lambda t: (t**2) * np.exp(-m_val * t), 0.0, np.inf)
    assert np.isclose(i2_num / i1_num, float(expected_s), rtol=1e-9, atol=1e-11)
print('VERIFIED_OK: CALC-INT-03 passed SymPy & SciPy quad for I1, I2, S across m in [2..9]')
