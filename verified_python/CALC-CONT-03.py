import math
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)

Lf = sp.limit((1 - sp.cos(m * x)) / x**2, x, 0)
assert sp.simplify(Lf - m**2 / 2) == 0, f'lim f mismatch: {Lf}'

Lr = sp.limit(sp.atan(m / x), x, 0, '+')
Ll = sp.limit(sp.atan(m / x), x, 0, '-')
assert sp.simplify(Lr - sp.pi / 2) == 0 and sp.simplify(Ll + sp.pi / 2) == 0, f'one-sided limits: {Ll}, {Lr}'
assert sp.simplify(Lr - Ll - sp.pi) == 0

for mv in range(2, 10):
    h = 1e-4
    approx = 2 * math.sin(mv * h / 2)**2 / h**2
    assert abs(approx - mv**2 / 2) < 1e-4 * mv**2, f'Numeric lim f failed at m={mv}'
    assert abs(math.atan(mv / 1e-9) - math.pi / 2) < 1e-6
    assert abs(math.atan(mv / -1e-9) + math.pi / 2) < 1e-6

print('VERIFIED_OK: CALC-CONT-03')
