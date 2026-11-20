import sympy as sp
import numpy as np
from scipy.integrate import quad

x = sp.Symbol('x', positive=True)
a = sp.Symbol('a', positive=True)
F_a = sp.integrate(x**(a - 1), (x, 0, 1))
d2F_da2 = sp.diff(F_a, a, 2)
for m_val in range(2, 10):
    sym_val = sp.integrate(x**(m_val - 1) * sp.log(x)**2, (x, 0, 1))
    leibniz_val = d2F_da2.subs(a, m_val)
    expected = sp.Rational(2, m_val**3)
    assert sp.simplify(sym_val - expected) == 0, f'SymPy mismatch at m={m_val}'
    assert sp.simplify(leibniz_val - expected) == 0, f'Leibniz mismatch at m={m_val}'
    num_val, _ = quad(lambda t: (t**(m_val - 1)) * (np.log(t)**2), 0.0, 1.0)
    assert np.isclose(num_val, float(expected), rtol=1e-9, atol=1e-12), f'Quad mismatch at m={m_val}'
print('VERIFIED_OK: CALC-INT-02 passed SymPy, Leibniz diff & SciPy quad across m in [2..9]')
