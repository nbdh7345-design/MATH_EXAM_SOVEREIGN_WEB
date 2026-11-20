import mpmath
import sympy as sp

x, t = sp.symbols('x t', real=True)
m = sp.symbols('m', positive=True)
L = sp.limit(sp.sin(m * x**2) / (3 * x**2), x, 0)
assert sp.simplify(L - m / 3) == 0, f'L Hospital limit mismatch: {L}'
ser = sp.integrate(sp.series(sp.sin(m * t**2), t, 0, 8).removeO(), (t, 0, x))
assert sp.simplify(sp.limit(ser / x**3, x, 0) - m / 3) == 0

for mv in range(2, 10):
    h = mpmath.mpf('1e-3')
    num = mpmath.quad(lambda s: mpmath.sin(mv * s**2), [0, h]) / h**3
    assert abs(num - mpmath.mpf(mv) / 3) < 1e-4 * mv, f'Numeric check failed at m={mv}'
    opts = [mv, mv / 6, mv / 2, mv / 3]
    assert len(set(opts)) == 4

print('VERIFIED_OK: CALC-ANTI-02')
