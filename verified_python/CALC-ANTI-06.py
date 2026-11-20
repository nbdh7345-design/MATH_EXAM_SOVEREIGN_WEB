import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
I = sp.integrate(sp.sin(m * x) * sp.cos(m * x), (x, 0, sp.pi / (2 * m)))
assert sp.simplify(I - 1 / (2 * m)) == 0, f'I mismatch: {I}'
for mv in range(2, 10):
    J = sp.integrate(x / sp.sqrt(x + 1), (x, 0, mv**2 - 1))
    assert sp.simplify(J - sp.Rational(2 * mv**3 - 6 * mv + 4, 3)) == 0, f'J mismatch at m={mv}: {J}'
    n = mpmath.quad(lambda s: s / mpmath.sqrt(s + 1), [0, mv**2 - 1])
    assert abs(n - mpmath.mpf(2 * mv**3 - 6 * mv + 4) / 3) < 1e-9 * mv**3
print('VERIFIED_OK: CALC-ANTI-06')
