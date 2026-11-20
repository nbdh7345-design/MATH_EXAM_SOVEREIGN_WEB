import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
A = sp.limit((sp.log(1 + m * x) - m * x) / x**2, x, 0)
assert sp.simplify(A + m**2 / 2) == 0, f'A mismatch: {A}'
lnB = sp.limit(sp.log(sp.cos(m * x)) / x**2, x, 0)
assert sp.simplify(lnB + m**2 / 2) == 0, f'ln B mismatch: {lnB}'
for mv in range(2, 10):
    h = 1e-4
    assert abs((math.log1p(mv * h) - mv * h) / h**2 + mv**2 / 2) < 1e-2 * mv**2
    assert abs(math.cos(mv * h) ** (1 / h**2) / math.exp(-mv**2 / 2) - 1) < 1e-3
print('VERIFIED_OK: CALC-LIM-06')
