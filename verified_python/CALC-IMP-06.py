import mpmath
import sympy as sp

x = sp.symbols('x', positive=True)
m = sp.symbols('m', positive=True)
I = sp.integrate(1 / (x**2 + m**2), (x, 0, sp.oo))
assert sp.simplify(I - sp.pi / (2 * m)) == 0, f'I mismatch: {I}'
for mv in range(2, 10):
    J = sp.integrate(x**sp.Rational(-1, mv), (x, 0, 1))
    assert J == sp.Rational(mv, mv - 1), f'J mismatch at m={mv}: {J}'
    nI = mpmath.quad(lambda t: 1 / (t**2 + mv**2), [0, mpmath.inf])
    assert abs(nI - mpmath.pi / (2 * mv)) < 1e-10
print('VERIFIED_OK: CALC-IMP-06')
