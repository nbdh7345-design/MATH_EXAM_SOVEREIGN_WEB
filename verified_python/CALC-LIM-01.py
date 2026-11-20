import sympy as sp
import numpy as np

x, m = sp.symbols('x m', real=True)
expr = 6 * (sp.exp(m * x) - 1 - sp.sin(m * x) - (m**2 * x**2) / 2) / x**3
lim_symbolic = sp.simplify(sp.limit(expr, x, 0))
expected = 2 * m**3
assert sp.simplify(lim_symbolic - expected) == 0, f'Symbolic mismatch: {lim_symbolic} != {expected}'

for m_val in range(2, 10):
    h = 1e-4
    num_approx = 6 * (np.exp(m_val * h) - 1.0 - np.sin(m_val * h) - 0.5 * (m_val**2) * (h**2)) / (h**3)
    exact_val = 2 * (m_val**3)
    assert abs(num_approx - exact_val) / exact_val < 1e-2, f'Numeric check failed at m={m_val}'
    opts = [2*m_val**3, m_val**3, 3*m_val**3, 4*m_val**3]
    assert len(set(opts)) == 4, f'Duplicate options at m={m_val}'

print('VERIFIED_OK: CALC-LIM-01')
