import math
import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
I = sp.integrate(x * sp.exp(m * x), (x, 0, 1))
assert sp.simplify(I - ((m - 1) * sp.exp(m) + 1) / m**2) == 0, f'Integral mismatch: {I}'
for mv in range(2, 10):
    num = mpmath.quad(lambda t: t * mpmath.exp(mv * t), [0, 1])
    exact = ((mv - 1) * math.exp(mv) + 1) / mv**2
    assert abs(num - exact) < 1e-9 * exact
    e = math.exp(mv)
    opts = [((mv + 1) * e - 1) / mv**2, exact, (mv - 1) * e / mv**2, ((mv - 1) * e + 1) / mv]
    assert len({round(o, 9) for o in opts}) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-INT-05')
