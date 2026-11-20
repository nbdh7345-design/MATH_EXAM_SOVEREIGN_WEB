import mpmath
import sympy as sp

x = sp.symbols('x', positive=True)
m = sp.symbols('m', positive=True)
y = 2 * sp.sqrt(x)
integrand = sp.simplify(y * sp.sqrt(1 + sp.diff(y, x)**2))
assert sp.simplify(integrand**2 - 4 * (x + 1)) == 0, f'Integrand mismatch: {integrand}'
S = 2 * sp.pi * sp.integrate(2 * sp.sqrt(x + 1), (x, 0, m**2 - 1))
assert sp.simplify(S - 8 * sp.pi * (m**3 - 1) / 3) == 0, f'Surface mismatch: {S}'
for mv in range(2, 10):
    num = 2 * mpmath.pi * mpmath.quad(lambda t: 2 * mpmath.sqrt(t) * mpmath.sqrt(1 + 1 / t), [0, 1, mv**2 - 1])
    exact = 8 * mpmath.pi * (mv**3 - 1) / 3
    assert abs(num - exact) < 1e-7 * exact, f'Numeric surface failed at m={mv}'
    opts = [4 * (mv**3 - 1), 8 * mv**3, 8 * (mv**3 - 1), 2 * (mv**3 - 1)]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-APP-05')
