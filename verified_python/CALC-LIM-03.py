import sympy as sp
import numpy as np

x, m, a, b = sp.symbols('x m a b', real=True)
num_expr = 4 * (sp.log(1 + m * x) - sp.sin(m * x) + a * x**2 + b * x**3)
ser = sp.series(num_expr, x, 0, 5).removeO()
c2 = sp.Poly(ser, x).nth(2)
c3 = sp.Poly(ser, x).nth(3)
sol = sp.solve([c2, c3], (a, b))
assert sp.simplify(sol[a] - m**2 / 2) == 0, f'Wrong a: {sol[a]}'
assert sp.simplify(sol[b] + m**3 / 2) == 0, f'Wrong b: {sol[b]}'

expr_sub = num_expr.subs(sol) / x**4
lim_val = sp.simplify(sp.limit(expr_sub, x, 0))
assert sp.simplify(lim_val - (-m**4)) == 0, f'Wrong limit: {lim_val}'

for m_val in range(2, 10):
    a_val = 0.5 * (m_val**2)
    b_val = -0.5 * (m_val**3)
    h = 2e-3
    approx = 4.0 * (np.log(1.0 + m_val * h) - np.sin(m_val * h) + a_val * h**2 + b_val * h**3) / (h**4)
    exact = -float(m_val**4)
    assert abs(approx - exact) / abs(exact) < 5e-2, f'Numeric check failed at m={m_val}'

print('VERIFIED_OK: CALC-LIM-03')
