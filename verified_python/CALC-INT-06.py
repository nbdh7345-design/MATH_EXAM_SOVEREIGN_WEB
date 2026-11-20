import mpmath
import sympy as sp

x = sp.symbols('x', real=True)
m = sp.symbols('m', positive=True)
I1 = sp.integrate(x * sp.sqrt(m**2 - x**2), (x, 0, m))
assert sp.simplify(I1 - m**3 / 3) == 0, f'I1 mismatch: {I1}'
I2 = sp.integrate(sp.sqrt(m**2 - x**2), (x, 0, m))
assert sp.simplify(I2 - sp.pi * m**2 / 4) == 0, f'I2 mismatch: {I2}'
for mv in range(2, 10):
    n1 = mpmath.quad(lambda t: t * mpmath.sqrt(mv**2 - t**2), [0, mv])
    n2 = mpmath.quad(lambda t: mpmath.sqrt(mv**2 - t**2), [0, mv])
    assert abs(n1 - mpmath.mpf(mv)**3 / 3) < 1e-8 * mv**3
    assert abs(n2 - mpmath.pi * mv**2 / 4) < 1e-8 * mv**2
print('VERIFIED_OK: CALC-INT-06')
