import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
expr = (sp.exp(m * x**2) - 1) / (1 - sp.cos(x))
L = sp.limit(expr, x, 0)
assert sp.simplify(L - 2 * m) == 0, f'Limit mismatch: {L}'

for mv in range(2, 10):
    h = 1e-3
    approx = math.expm1(mv * h * h) / (2 * math.sin(h / 2)**2)
    assert abs(approx - 2 * mv) < 1e-3 * mv, f'Numeric check failed at m={mv}'
    opts = [mv, mv / 2, 2 * mv, 4 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-CONT-02')
