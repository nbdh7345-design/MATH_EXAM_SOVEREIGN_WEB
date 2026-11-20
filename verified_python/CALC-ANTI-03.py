import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
F = sp.atan((x + 1) / m) / m
assert sp.simplify(sp.diff(F, x) - 1 / (x**2 + 2 * x + m**2 + 1)) == 0, 'Antiderivative check failed'
I = sp.simplify(F.subs(x, m - 1) - F.subs(x, -1))
assert sp.simplify(I - sp.pi / (4 * m)) == 0, f'Integral mismatch: {I}'

for mv in range(2, 10):
    num = mpmath.quad(lambda t: 1 / (t**2 + 2 * t + mv**2 + 1), [-1, mv - 1])
    assert abs(num - mpmath.pi / (4 * mv)) < 1e-12, f'Numeric check failed at m={mv}'

print('VERIFIED_OK: CALC-ANTI-03')
