import sympy as sp
import mpmath

x, m = sp.symbols('x m', positive=True)
V = sp.pi * sp.integrate((x * (m - x))**2, (x, 0, m))
assert sp.simplify(V - sp.pi * m**5 / 30) == 0, f'Volume mismatch: {V}'

for mv in range(2, 10):
    approx = mpmath.pi * mpmath.quad(lambda t: (t * (mv - t))**2, [0, mv])
    exact = mpmath.pi * mv**5 / 30
    assert abs(approx - exact) < 1e-9 * exact, f'Numeric volume failed at m={mv}'
    opts = [sp.pi * mv**5 / 15, sp.pi * mv**5 / 60, sp.pi * mv**5 / 30, sp.pi * mv**5 / 20]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'

print('VERIFIED_OK: CALC-APP-02')
