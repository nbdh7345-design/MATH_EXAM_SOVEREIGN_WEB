import sympy as sp
import numpy as np

x, m = sp.symbols('x m', real=True)
expr = 12 * (sp.exp(-m**2 * x**2 / 2) - sp.cos(m * x)) / x**4
series_num = sp.series(12 * (sp.exp(-m**2 * x**2 / 2) - sp.cos(m * x)), x, 0, 5).removeO()
lim_symbolic = sp.simplify(sp.limit(expr, x, 0))
assert sp.simplify(lim_symbolic - m**4) == 0, f'Expected m**4, got {lim_symbolic}'
assert sp.simplify(series_num / x**4 - m**4) == 0

for m_val in range(2, 10):
    h = 5e-3
    num_val = 12.0 * (np.exp(-0.5 * (m_val**2) * (h**2)) - np.cos(m_val * h)) / (h**4)
    exact_val = float(m_val**4)
    assert abs(num_val - exact_val) / exact_val < 1e-2, f'Numeric check failed at m={m_val}'
    opts = [0.5 * m_val**4, float(m_val**4), 2.0 * m_val**4, 3.0 * m_val**4]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-LIM-02')
