import mpmath
import sympy as sp

x = sp.symbols('x', positive=True)
m = sp.symbols('m', positive=True)
y = sp.Rational(2, 3) * x**sp.Rational(3, 2)
L = sp.integrate(sp.sqrt(1 + sp.diff(y, x)**2), (x, 0, m**2 - 1))
assert sp.simplify(L - 2 * (m**3 - 1) / 3) == 0, f'Length mismatch: {L}'
V = sp.pi * sp.integrate(x, (x, 0, m))
assert sp.simplify(V - sp.pi * m**2 / 2) == 0
for mv in range(2, 10):
    Ln = mpmath.quad(lambda t: mpmath.sqrt(1 + t), [0, mv**2 - 1])
    assert abs(Ln - mpmath.mpf(2) * (mv**3 - 1) / 3) < 1e-9 * mv**3
print('VERIFIED_OK: CALC-APP-06')
