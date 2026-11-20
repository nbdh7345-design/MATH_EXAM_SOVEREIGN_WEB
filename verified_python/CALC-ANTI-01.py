import math
import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
pf = sp.apart(1 / ((x + 1) * (x + 3)), x)
assert sp.simplify(pf - (sp.Rational(1, 2) / (x + 1) - sp.Rational(1, 2) / (x + 3))) == 0

for mv in range(2, 10):
    I = sp.integrate(1 / ((x + 1) * (x + mv)), (x, 0, 1))
    exact = sp.log(sp.Rational(2 * mv, mv + 1)) / (mv - 1)
    assert abs(float(I - exact)) < 1e-12, f'Symbolic integral mismatch at m={mv}: {I}'
    num = mpmath.quad(lambda t: 1 / ((t + 1) * (t + mv)), [0, 1])
    assert abs(num - float(exact)) < 1e-12
    opts = [math.log(2 * mv / (mv + 1)) / (mv - 1), math.log(2 * mv / (mv + 1)) / (mv + 1),
            math.log((mv + 1) / 2) / (mv - 1), math.log((mv + 1) / (2 * mv)) / (mv - 1)]
    assert len({round(o, 12) for o in opts}) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-ANTI-01')
