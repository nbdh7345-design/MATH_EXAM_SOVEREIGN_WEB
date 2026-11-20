import math
import sympy as sp

x, y, z, lam = sp.symbols('x y z lambda', real=True)
m = sp.symbols('m', positive=True)
L = x + 2 * y + 2 * z + lam * (m**2 - x**2 - y**2 - z**2)
sols = sp.solve([sp.diff(L, v) for v in (x, y, z, lam)], [x, y, z, lam], dict=True)
vals = sorted([sp.simplify((x + 2 * y + 2 * z).subs(s)) for s in sols], key=lambda e: float(e.subs(m, 1)))
assert len(vals) == 2 and sp.simplify(vals[-1] - 3 * m) == 0 and sp.simplify(vals[0] + 3 * m) == 0, f'Values: {vals}'
for mv in range(2, 10):
    opts = [5 * mv, math.sqrt(5) * mv, 9 * mv**2, 3 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-LAG-06')
